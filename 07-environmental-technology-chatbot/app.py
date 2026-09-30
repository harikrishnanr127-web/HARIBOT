import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from google import genai
from google.genai import types

from chatbot_config import CHATBOT_TITLE, SYSTEM_PROMPT, WELCOME_MESSAGE

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

MAX_MESSAGE_CHARS = 2000
MAX_HISTORY_TURNS = 20

app = Flask(__name__)
client = genai.Client(api_key=API_KEY) if API_KEY else None


@app.route("/")
def index():
    return render_template("index.html", title=CHATBOT_TITLE, welcome=WELCOME_MESSAGE)


@app.route("/chat", methods=["POST"])
def chat():
    if client is None:
        return jsonify(error="GEMINI_API_KEY is missing. Add it to your .env file."), 500

    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    history = data.get("history", [])

    if not message:
        return jsonify(error="Please type a question first."), 400
    if len(message) > MAX_MESSAGE_CHARS:
        return jsonify(error=f"Keep your question under {MAX_MESSAGE_CHARS} characters."), 400

    contents = []
    if isinstance(history, list):
        for turn in history[-MAX_HISTORY_TURNS:]:
            role = turn.get("role") if isinstance(turn, dict) else None
            text = str(turn.get("text", ""))[:MAX_MESSAGE_CHARS] if role else ""
            if role in ("user", "model") and text:
                contents.append(
                    types.Content(role=role, parts=[types.Part.from_text(text=text)])
                )
    contents.append(types.Content(role="user", parts=[types.Part.from_text(text=message)]))

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.4,
                max_output_tokens=1024,
            ),
        )
        reply = (response.text or "").strip()
        if not reply:
            reply = "I couldn't produce an answer for that. Try rephrasing your question."
        return jsonify(reply=reply)
    except Exception as exc:  # noqa: BLE001
        app.logger.exception("Gemini request failed: %s", exc)
        return jsonify(error="The assistant is unavailable right now. Please try again."), 502


if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("PORT", 5000)))
