# Skillflow — Agent Instructions

This file provides context for AI agents and coding assistants working on this codebase.

## Project Overview

Skillflow is a self-hosted Django web app for tracking professional certifications (e.g., CompTIA Security+, ISC2 CISSP). It solves the problem of managing multiple certification renewal cycles and continuing education (CE) requirements.

## Tech Stack

- **Language:** Python 3.14
- **Framework:** Django 6.0.5
- **Package manager:** uv (not pip, not poetry)
- **Database:** SQLite (development)
- **Auth:** django-allauth 65.x (social + username/password)
- **Frontend:** Bootstrap 5 via CDN (no build step)
- **License:** GNU AGPLv3

## Project Structure

```
project/        # Django project config (settings, urls, wsgi, asgi)
pages/          # Public-facing landing pages (index, about)
skillflow/      # Core certification tracking app
templates/      # Project-level templates (base.html, account/, registration/)
```

The `skillflow` app contains all business logic. The `pages` app is for static/informational content only.

## Key Architecture Decisions

- `CertificationRecord.exp_date` and `.status` are computed `@property` fields — not stored in the database. Do not add DB columns for these.
- All skillflow views are function-based (not class-based).
- `get_object_or_404(Model, pk=pk, user=request.user)` is used on every detail/edit/delete view as an ownership guard. Never fetch a record without this guard.
- The `applicable_certs` M2M queryset on `ContinuingEducationRecordForm` must always be filtered to `CertificationRecord.objects.filter(user=request.user)` in the view — failure to do so would allow cross-user data access.

## Data Model Summary

- `CertificationVendor` — admin-managed issuer (e.g., CompTIA)
- `Certification` — admin-managed cert template with renewal period and CE requirements
- `CertificationRecord` — a user's held certification (links user → Certification)
- `ContinuingEducationRecord` — a CE activity, with optional file upload and M2M link to CertificationRecord

## URL Namespacing

The `skillflow` app uses `app_name = 'skillflow'`. Always use namespaced URLs in templates and views: `{% url 'skillflow:dashboard' %}`, `redirect('skillflow:dashboard')`.

Auth URLs are provided by `allauth` at `/accounts/` and use names like `account_login`, `account_logout`, `account_signup`.

## Development Commands

```bash
uv sync                                      # install dependencies
uv run python manage.py migrate              # apply migrations
uv run python manage.py createsuperuser      # create admin user
uv run python manage.py runserver            # start dev server
uv run python manage.py test                 # run tests
uv run python manage.py check                # system check
uv run python manage.py makemigrations       # generate migrations after model changes
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DJANGO_SECRET_KEY` | Production | Django secret key. A dev fallback is hardcoded in settings.py for local use only. |

## Conventions

- Copyright notice headers appear at the top of all project-authored `.py` files.
- Django-generated boilerplate files (`wsgi.py`, `asgi.py`, `apps.py`, `manage.py`) do not carry the project copyright notice.
- Migration files are committed to the repository.
- Uploaded files go to `media/ce_certificates/` (excluded from git via `.gitignore`).
