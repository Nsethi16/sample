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


## Browser testing tips

If you test using browser console, avoid assuming every response is JSON. When the server returns an error page, `response.json()` can fail with `Unexpected token '<'`.

Use this safer snippet:

```js
fetch("https://gotit.onrender.com/ask", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ question: "What is Render?" })
})
  .then(async (r) => {
    const text = await r.text();
    try {
      return { status: r.status, data: JSON.parse(text) };
    } catch {
      return { status: r.status, data: text };
    }
  })
  .then(console.log)
  .catch(console.error);
```

If status is `500/502`, check Render logs and verify `OPENAI_API_KEY` is correctly set in the Render Environment tab.


## Render error fix (`unexpected keyword argument 'proxies'`)

If Render logs show:

- `TypeError: Client.__init__() got an unexpected keyword argument 'proxies'`

this is a dependency mismatch between `openai` and a newer `httpx`.

This repo pins `httpx==0.27.2` to keep compatibility with `openai==1.51.2`.

Also, this repo includes `runtime.txt` to force Python `3.11.9` on Render (your logs showed Python 3.14).

After pulling these changes:

1. Redeploy the service on Render.
2. Confirm build log shows Python 3.11.9.
3. Re-test `POST /ask`.
