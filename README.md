> [!WARNING]
> **Deprecated: no longer maintained.** Last updated in January 2026; kept for reference.

# Flotrafic Flask backend (legacy)

The original Flask backend for Flotrafic: a small API that receives website enquiries, summarises them with OpenAI and emails them to the business.

Status: deprecated. Superseded by [flotrafic-fastapi-backend](https://github.com/JoeWat2005/flotrafic-fastapi-backend), a FastAPI rebuild with JWT authentication, business-scoped APIs, bookings, enquiries and automated notifications.

## Features

- `POST /api/enquiry/<site_id>` accepts an enquiry (`name`, `email`, `message`) for a registered client site
- Each enquiry is summarised with OpenAI (`gpt-4o-mini`) and stored alongside the summary
- The client is emailed the summary and the original message through the Resend API
- `GET /admin/` lists stored enquiries with their AI summaries

## Tech stack

- Python 3.11 (the Docker base image is `python:3.11-slim`)
- Flask and Flask-SQLAlchemy
- OpenAI Python SDK
- Resend email API, called with `requests`
- SQLite by default, with `psycopg2-binary` installed for PostgreSQL
- Gunicorn

## Getting started

### Prerequisites

- Python 3.11
- An OpenAI API key and a Resend API key

### Installation

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt` does not pin any versions.

### Configuration

`create_app()` loads variables from the environment or from a `.env` file through python-dotenv. `.env` files are ignored by git.

| Variable | Purpose |
| --- | --- |
| `DATABASE_URL` | SQLAlchemy database URL (default `sqlite:///local.db`) |
| `FLASK_SECRET_KEY` | Flask secret key (default `dev`) |
| `OPENAI_API_KEY` | OpenAI API key used to summarise enquiries. Enquiry requests fail without it. |
| `RESEND_API_KEY` | Resend API key used to send notification emails |

### Running locally

From the repository root:

```bash
python -m website_manager.run
```

This starts Flask's development server in debug mode, by default at `http://127.0.0.1:5000`, which is the address `website_manager/scripts/test_api.py` uses. With the server running, send a sample enquiry:

```bash
python website_manager/scripts/test_api.py
```

The script posts to site ID `plumber123`, so a `Client` with that `site_id` must already exist (see Notes).

### Docker

```bash
docker build -t flotrafic-flask .
docker run -p 8000:8000 --env-file .env flotrafic-flask
```

The image runs `gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app`.

### Notes

- There is no table creation or migration step. Nothing calls `db.create_all()`, so the tables have to be created before the first request.
- No route or script registers clients, so `Client` rows have to be added to the database directly.
- `GET /admin/` has no authentication.
- There are no automated tests. `website_manager/scripts/test_api.py` is a manual smoke test.

## How it works

1. `wsgi.py` (for Gunicorn) and `website_manager/run.py` (for development) both call `create_app()` in `website_manager/app/__init__.py`. It loads `.env`, applies `Config` from `config.py`, initialises SQLAlchemy and registers the `api` and `admin` blueprints.
2. `routes.py` looks up the `Client` by `site_id`, calls `summarise_enquiry()` in `ai.py`, saves an `Enquiry` and calls `send_email()` in `email.py`.
3. `ai.py` sends the message to the OpenAI chat completions API with a short "summarise the enquiry" system prompt.
4. `email.py` posts the email to the Resend API from `onboarding@resend.dev`, Resend's shared test sender.
5. `admin.py` renders `templates/admin.html` with all enquiries, newest first.

The data model in `models.py` has two tables. `Client` holds a name, an email and a unique `site_id`. `Enquiry` holds the site ID, name, email, message, AI summary and creation time.

## Project structure

```
website_manager/
  app/
    __init__.py    Application factory
    admin.py       Admin blueprint (enquiry list)
    ai.py          OpenAI summarisation
    config.py      Configuration from environment variables
    email.py       Resend email sender
    models.py      Client and Enquiry models
    routes.py      Enquiry API blueprint
    templates/     Admin page template
  scripts/
    test_api.py    Manual test that posts a sample enquiry
  run.py           Development server entry point
wsgi.py            WSGI entry point for Gunicorn
Dockerfile         Production image
requirements.txt   Python dependencies
```

## Related repositories

- [flotrafic-fastapi-backend](https://github.com/JoeWat2005/flotrafic-fastapi-backend): the FastAPI rebuild that replaces this backend
- [flotrafic-react-frontend](https://github.com/JoeWat2005/flotrafic-react-frontend): the Flotrafic React frontend
- [deskcaptain](https://github.com/JoeWat2005/deskcaptain): the later AI receptionist product
