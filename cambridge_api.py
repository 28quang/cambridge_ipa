from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return 'Cambridge IPA API is running! Try /ipa?word=your_word'

@app.route('/ipa')
def get_ipa():
    word = request.args.get('word')
    if not word:
        return jsonify({'error': 'Missing word parameter'}), 400

    url = f"https://dictionary.cambridge.org/dictionary/english/{word}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch from Cambridge Dictionary'}), 500

    soup = BeautifulSoup(response.text, 'html.parser')
    ipa = soup.find('span', class_='ipa')

    if ipa:
        return jsonify({'word': word, 'ipa': ipa.text})
    else:
        return jsonify({'word': word, 'ipa': None})
