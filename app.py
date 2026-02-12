import os

from flask import Flask, jsonify, request
from openai import OpenAI
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_client() -> OpenAI:
    """Create an OpenAI client using the API key from environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    return OpenAI(api_key=api_key)
@app.get("/hello")
def hello() -> tuple:
    """Return a greeting for the provided name query parameter."""
    name = request.args.get("name", "World").strip()
    if not name:
        return jsonify({"error": "Query parameter 'name' is required."}), 400
    return jsonify({"message": f"Hello {name}"}), 200


@app.get("/")
def healthcheck() -> tuple:
    """Basic endpoint to verify the API is running."""
    return jsonify({"status": "ok"}), 200


@app.post("/ask")
def ask() -> tuple:
    """Ask a question and get an AI-generated response."""
    body = request.get_json(silent=True) or {}
    question = (body.get("question") or "").strip()

    if not question:
        return jsonify({"error": "JSON body field 'question' is required."}), 400

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    try:
        client = get_client()
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 500

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a concise and helpful assistant.",
                },
                {"role": "user", "content": question},
            ],
        )
        answer = completion.choices[0].message.content or ""
        return jsonify({"answer": answer, "model": model}), 200
    except Exception as exc:  # keep response JSON even when provider errors
        return jsonify({"error": "OpenAI request failed", "details": str(exc)}), 502
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a concise and helpful assistant.",
            },
            {"role": "user", "content": question},
        ],
    )

    answer = completion.choices[0].message.content or ""
    return jsonify({"answer": answer, "model": model}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
