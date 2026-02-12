# OpenAI Q&A API (Render-ready)

A minimal Python API that accepts a question and responds using the OpenAI API.

## Endpoints

- `GET /` → healthcheck (`{"status":"ok"}`)
- `POST /ask` → ask a question

Example request:

```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Render?"}'
```

Example response:

```json
{
  "answer": "Render is a cloud platform ...",
  "model": "gpt-4o-mini"
}
```

If `question` is missing/empty, API returns HTTP `400`.

## Environment variables

- `OPENAI_API_KEY` (**required**) — your OpenAI API key.
- `OPENAI_MODEL` (optional) — defaults to `gpt-4o-mini`.

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="your_api_key_here"
# optional:
# export OPENAI_MODEL="gpt-4o-mini"
python app.py
```

Local test:

```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Write a one-line hello"}'
```

## Deploy on Render (secure key management)

This repo includes `render.yaml`, so use **Blueprint Deploy**:

1. Push this repository to GitHub.
2. In Render, click **New +** → **Blueprint** and select the repo.
3. Render creates service `openai-qa-api`.
4. In Render dashboard, open the service **Environment** tab.
5. Add `OPENAI_API_KEY` as a secret environment variable (the blueprint has `sync: false`, so the key is never committed in code).
6. Redeploy if needed.

Render build/start:

- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app`
