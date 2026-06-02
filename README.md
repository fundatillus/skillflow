# Skillflow

**Skillflow** is a self-hosted web app for tracking professional certifications. Log your certs, monitor renewal dates with automatic status alerts, and record continuing education hours — all in one place. Built with Django, designed for IT and security professionals managing multiple active certifications.

## Installation

### Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

1. Clone the repository and enter the project directory.

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Apply database migrations:
   ```bash
   uv run python manage.py migrate
   ```

4. Create an admin account:
   ```bash
   uv run python manage.py createsuperuser
   ```

5. Start the development server:
   ```bash
   uv run python manage.py runserver
   ```

6. Visit `http://localhost:8000/` in your browser.

### Configuring Social Login (Optional)

Skillflow supports sign-in via Google, Apple, GitHub, and Reddit through [django-allauth](https://docs.allauth.org/). To enable a provider:

1. Register your app with the provider's developer console and obtain a **Client ID** and **Client Secret**.
2. In the Django admin (`/admin/`), go to **Sites** and update `example.com` to your domain (`localhost` for local development).
3. Go to **Social Applications → Add** and enter the credentials for each provider you want to enable.

### Populating the Certification Library

Users can only add certifications that exist in the admin-managed library. To add certifications:

1. Log in to the Django admin (`/admin/`).
2. Add a **Certification Vendor** (e.g., CompTIA, ISC2).
3. Add a **Certification** under that vendor with its renewal period and CE unit requirement.

## License

Copyright (C) 2026 Adam Clements

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. See [LICENSE.md](LICENSE.md) for the full text.

## AI Attribution
This project was built with AI assistance. Development tools used include: 
- Claude 

Human review was applied to all generated code before merging.