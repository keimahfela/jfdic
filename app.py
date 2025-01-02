from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

# Create the Flask app instance
app = Flask(__name__)

def scrape_definition(word):
    url = f"https://www.jfdictionary.com/search.php?terms={word}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    definition = soup.find('div', class_='definition')  # Update this selector
    if definition:
        return definition.get_text(strip=True)
    return "Definition not found."

@app.route('/search', methods=['GET'])
def search():
    word = request.args.get('word')
    if not word:
        return jsonify({"error": "Please provide a word."}), 400
    definition = scrape_definition(word)
    return jsonify({"word": word, "definition": definition})

# Ensure the app object is accessible
if __name__ == '__main__':
    app.run(debug=True)