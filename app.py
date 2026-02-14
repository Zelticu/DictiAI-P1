from flask import Flask, request, jsonify
from spellchecker import SpellChecker

app = Flask(__name__)
spell = SpellChecker()

@app.route('/check', methods=['POST'])
def check_text():
    data = request.get_json()
    text = data.get("text", "")

    lines = text.split("\n")
    errors = []

    for i, line in enumerate(lines):
        words = line.split()

        for word in words:
            clean_word = ''.join(filter(str.isalpha, word))

            if clean_word and clean_word.lower() not in spell:
                errors.append({
                    "line": i + 1,
                    "type": "Spelling",
                    "word": clean_word
                })

    return jsonify({"errors": errors})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
