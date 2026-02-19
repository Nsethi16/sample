import os

from flask import Flask, jsonify, request
from openai import OpenAI

app = Flask(__name__)


AGENT_INSTRUCTIONS = (
    "You are a concise and helpful assistant. "
    "Use available tools when they improve answer quality."
)


def get_client() -> OpenAI:
    """Create an OpenAI client using the API key from environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    return OpenAI(api_key=api_key)


@app.get("/")
def healthcheck() -> tuple:
    """Basic endpoint to verify the API is running."""
    return jsonify({"status": "ok"}), 200


@app.get("/hello")
def hello() -> tuple:
    """Return a greeting for the provided name query parameter."""
    name = request.args.get("name", "World").strip()
    if not name:
        return jsonify({"error": "Query parameter 'name' is required."}), 400
    return jsonify({"message": f"Hello {name}"}), 200


@app.post("/ask")
def ask() -> tuple:
    """Ask a question and get an agent-style response with tool support."""
    body = request.get_json(silent=True) or {}
    question = (body.get("question") or "").strip()

    if not question:
        return jsonify({"error": "JSON body field 'question' is required."}), 400

    model = os.getenv("OPENAI_MODEL", "gpt-5-mini")

    try:
        client = get_client()
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 500

    try:
        response = client.responses.create(
            model=model,
            instructions=AGENT_INSTRUCTIONS,
            input=question,
            tools=[
                {"type": "web_search"},
                {"type": "code_interpreter"},
            ],
        )
        return jsonify({"answer": response.output_text, "model": model}), 200
        # openai>=1.55 exposes `client.responses`. Older SDKs only support
        # `chat.completions`, so we gracefully fall back to avoid hard failures.
        if hasattr(client, "responses"):
            response = client.responses.create(
                model=model,
                instructions=AGENT_INSTRUCTIONS,
                input=question,
                tools=[
                    {"type": "web_search_preview"},
                    {"type": "code_interpreter"},
                ],
            )
            answer = response.output_text
        else:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": AGENT_INSTRUCTIONS},
                    {"role": "user", "content": question},
                ],
            )
            answer = response.choices[0].message.content

        return jsonify({"answer": answer, "model": model}), 200
    except Exception as exc:  # Keep response JSON even when provider errors.
        return jsonify({"error": "OpenAI request failed", "details": str(exc)}), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
