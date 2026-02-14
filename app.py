from flask import Flask, request, jsonify
import hunspell
import os
import re

app = Flask(__name__)

# Load Hunspell dictionary
h = hunspell.HunSpell("en_US.dic", "en_US.aff")


@app.route("/check", methods=["POST"])
def check_text():
    data = request.get_json()
    text = data.get("text", "")

    lines = text.split("\n")
    errors = []

    for i, line in enumerate(lines):
        # Extract words (letters only)
        words = re.findall(r"[A-Za-z']+", line)

        for word in words:
            # Ignore capitalized proper nouns (optional but smart)
            if word[0].isupper() and word.lower() not in h:
                continue

            if not h.spell(word):
                errors.append({
                    "line": i + 1,
                    "type": "Spelling",
                    "word": word
                })

    return jsonify({"errors": errors})


@app.route("/")
def home():
    return "Dicti backend running."


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
