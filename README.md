# OpenAI Agent Q&A API (Render-ready)

A minimal Flask API that answers questions using an OpenAI agent-style workflow with tools enabled:

- **Web search** (`web_search`)
- **Code interpreter** (`code_interpreter`)

## Endpoints

- `GET /` → healthcheck (`{"status":"ok"}`)
- `GET /hello?name=Alice` → returns `{"message":"Hello Alice"}`
- `POST /ask` → asks the agent a question

Example request:

```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Find the latest Python release and compare 2^10 vs 10^2"}'
```

Example response:

```json
{
  "answer": "...",
  "model": "gpt-4.1"
}
```

If `question` is missing/empty, API returns HTTP `400`.

## Environment variables

- `OPENAI_API_KEY` (**required**) — your OpenAI API key.
- `OPENAI_MODEL` (optional) — defaults to `gpt-4.1`.
- Uses OpenAI Responses API with `web_search` and `code_interpreter` tools (requires modern `openai` SDK).

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="your_api_key_here"
# optional:
# export OPENAI_MODEL="gpt-4.1"
python app.py
```

## Deploy on Render

This repository includes `render.yaml`, so the easiest option is Render Blueprint deploy:

1. Push this repo to GitHub.
2. In Render, click **New +** → **Blueprint**.
3. Select your repository.
4. Add `OPENAI_API_KEY` in the Render service environment variables.
5. Deploy.
