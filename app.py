from flask import Flask, request, jsonify
import hunspell

app = Flask(__name__)

# Load dictionary (we’ll add files next)
h = hunspell.HunSpell('en_US.dic', 'en_US.aff')

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

            if clean_word and not h.spell(clean_word):
                errors.append({
                    "line": i + 1,
                    "type": "Spelling",
                    "word": clean_word
                })

    return jsonify({"errors": errors})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
