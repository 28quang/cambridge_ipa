from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
@app.route("/")
def home():
    return jsonify({"message": "Cambridge IPA API is running!"})


def get_ipa_cambridge(word):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    url = f"https://dictionary.cambridge.org/dictionary/english/{word}"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    uk_ipa = soup.select_one('.uk .pron.dpron .ipa')
    us_ipa = soup.select_one('.us .pron.dpron .ipa')

    return {
        "UK": uk_ipa.text.strip() if uk_ipa else None,
        "US": us_ipa.text.strip() if us_ipa else None
    }

@app.route("/ipa")
def ipa():
    word = request.args.get("word", "")
    if not word:
        return jsonify({"error": "Missing 'word' parameter"}), 400
    ipa_data = get_ipa_cambridge(word)
    return jsonify(ipa_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
