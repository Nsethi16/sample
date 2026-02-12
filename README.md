# Hello Name API

A minimal Python API that returns `Hello <name>` and is ready to deploy on [Render](https://render.com/).

## Endpoints

- `GET /` → healthcheck
- `GET /hello?name=Alice` → returns:

```json
{
  "message": "Hello Alice"
}
```

If `name` is empty (for example, `/hello?name=`), the API returns a `400`.

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Server runs on `http://localhost:5000`.

## Deploy on Render

This repository includes `render.yaml`, so the easiest option is Render Blueprint deploy:

1. Push this repo to GitHub.
2. In Render, click **New +** → **Blueprint**.
3. Select your repository.
4. Render auto-detects `render.yaml` and creates the web service.

Render will run:

- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app`
