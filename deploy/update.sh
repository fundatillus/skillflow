#!/usr/bin/env bash
# Deploy an update: pull latest code, sync deps, migrate, collect static, restart.
# Run as root from the server: bash /var/www/skillflow/deploy/update.sh
set -euo pipefail

APP_DIR="/var/www/skillflow"
APP_USER="skillflow"
ENV_FILE="/etc/skillflow/env"

cd "$APP_DIR"

git pull --ff-only

sudo -u "$APP_USER" bash -c "
    cd '$APP_DIR'
    set -a; source '$ENV_FILE'; set +a
    uv sync --no-dev
    uv run python manage.py migrate --noinput
    uv run python manage.py collectstatic --noinput
"

systemctl restart skillflow
echo "Skillflow updated and restarted."
