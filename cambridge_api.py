from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import codecs

app = Flask(__name__)

def extract_ipa(word):
    url = f"https://dictionary.cambridge.org/dictionary/english/{word}"
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0"
    })
    soup = BeautifulSoup(response.content, "html.parser")
    
    ipa_element = soup.find("span", class_="ipa")
    if ipa_element:
        return ipa_element.text
    return None

@app.route("/")
def home():
    return "Cambridge IPA API is running! Try /ipa?word=your_word"

@app.route("/ipa")
def get_ipa():
    word = request.args.get("word")
    ipa = extract_ipa(word)
    if ipa:
        return jsonify({
            "ipa": codecs.decode(repr(ipa), 'unicode_escape'),
            "word": word
        })
    else:
        return jsonify({
            "ipa": "Not found",
            "word": word
        })

if __name__ == "__main__":
    app.run(debug=True)
