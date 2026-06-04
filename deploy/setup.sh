#!/usr/bin/env bash
# One-time server setup for Skillflow on Debian 13.
# Run as root: bash setup.sh
set -euo pipefail

REPO_URL="https://github.com/fundatillus/skillflow.git"  # update if different
APP_DIR="/var/www/skillflow"
APP_USER="skillflow"
ENV_DIR="/etc/skillflow"

# ── System packages ──────────────────────────────────────────────────────────
apt-get update
apt-get install -y \
    git curl ca-certificates \
    nginx certbot python3-certbot-nginx \
    postgresql postgresql-client libpq-dev \
    build-essential

# ── App user ─────────────────────────────────────────────────────────────────
if ! id "$APP_USER" &>/dev/null; then
    useradd --system --shell /usr/sbin/nologin --home "$APP_DIR" --create-home "$APP_USER"
fi
usermod -aG www-data "$APP_USER"

# ── PostgreSQL ────────────────────────────────────────────────────────────────
systemctl enable --now postgresql

DB_PASS=$(openssl rand -hex 24)
sudo -u postgres psql <<SQL
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '$APP_USER') THEN
        CREATE ROLE $APP_USER WITH LOGIN PASSWORD '$DB_PASS';
    END IF;
END
\$\$;
SELECT 'CREATE DATABASE skillflow OWNER $APP_USER'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'skillflow')\gexec
SQL

# ── Clone repo ────────────────────────────────────────────────────────────────
if [ ! -d "$APP_DIR/.git" ]; then
    git clone "$REPO_URL" "$APP_DIR"
else
    echo "Repo already cloned at $APP_DIR — skipping clone."
fi
chown -R "$APP_USER:www-data" "$APP_DIR"
chmod -R 750 "$APP_DIR"

# ── uv + Python ───────────────────────────────────────────────────────────────
if ! command -v uv &>/dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | UV_INSTALL_DIR=/usr/local/bin sh
fi

sudo -u "$APP_USER" bash -c "
    cd '$APP_DIR'
    uv python install
    uv sync --no-dev
"

# ── Environment file ──────────────────────────────────────────────────────────
mkdir -p "$ENV_DIR"
chmod 750 "$ENV_DIR"
chown root:"$APP_USER" "$ENV_DIR"

if [ ! -f "$ENV_DIR/env" ]; then
    SECRET_KEY=$(python3 -c "import secrets, string; print(''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(64)))")
    cat > "$ENV_DIR/env" <<EOF
DJANGO_SECRET_KEY=$SECRET_KEY
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=skillflowapp.io,www.skillflowapp.io
DJANGO_CSRF_TRUSTED_ORIGINS=https://skillflowapp.io,https://www.skillflowapp.io
DB_NAME=skillflow
DB_USER=$APP_USER
DB_PASSWORD=$DB_PASS
DB_HOST=localhost
DB_PORT=5432
EOF
    chmod 640 "$ENV_DIR/env"
    chown root:"$APP_USER" "$ENV_DIR/env"
    echo ""
    echo ">>> Environment file written to $ENV_DIR/env"
    echo ">>> PostgreSQL password: $DB_PASS  (also stored in env file)"
    echo ""
else
    echo "Env file already exists at $ENV_DIR/env — skipping."
fi

# ── Django setup ──────────────────────────────────────────────────────────────
sudo -u "$APP_USER" bash -c "
    cd '$APP_DIR'
    export PATH=\"\$HOME/.local/bin:\$PATH\"
    set -a; source '$ENV_DIR/env'; set +a
    uv run python manage.py migrate --noinput
    uv run python manage.py collectstatic --noinput
    echo 'Django setup complete.'
"

mkdir -p "$APP_DIR/media"
chown -R "$APP_USER:www-data" "$APP_DIR/media"

# ── systemd service ───────────────────────────────────────────────────────────
cp "$APP_DIR/deploy/skillflow.service" /etc/systemd/system/skillflow.service
systemctl daemon-reload
systemctl enable --now skillflow

# ── Nginx ─────────────────────────────────────────────────────────────────────
cp "$APP_DIR/deploy/nginx.conf" /etc/nginx/sites-available/skillflow
ln -sf /etc/nginx/sites-available/skillflow /etc/nginx/sites-enabled/skillflow
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

# ── SSL (Let's Encrypt) ───────────────────────────────────────────────────────
echo ""
echo ">>> Run the following to obtain your SSL certificate:"
echo "    certbot --nginx -d skillflowapp.io -d www.skillflowapp.io"
echo ""
echo ">>> Setup complete. Once SSL is configured, Skillflow will be live at https://skillflowapp.io"
