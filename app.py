from flask import Flask, jsonify, request

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
