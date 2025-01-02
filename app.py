from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import unicodedata

# Create the Flask app
app = Flask(__name__)

# Function to normalize text
def normalize_text(text):
    return unicodedata.normalize('NFKC', text)

# Function to scrape the definition of a word
def scrape_definition(word, page=1, per_page=5):
    try:
        # Define the URL with the page parameter
        url = f"https://www.jfdictionary.com/search.php?terms={word}&p={page}"
        
        # Add the user-agent header
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Make the request with the headers
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'  # Ensure proper encoding
        
        # Parse the response
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract all definitions (update the selector as needed)
        definitions = soup.find_all('div', class_='details')  # Updated selector
        if definitions:
            definitions = [normalize_text(definition.get_text(strip=True)) for definition in definitions]
            # Check if there are more results
            has_more = len(definitions) >= per_page
            return definitions, len(definitions), has_more  # Return definitions, total count, and has_more flag
        return ["Definition not found."], 0, False
    except Exception as e:
        return [f"Error: {str(e)}"], 0, False

# Root route
@app.route('/')
def home():
    return render_template('index.html')  # Serve the index.html file

# Search route
@app.route('/search', methods=['GET'])
def search():
    # Get the word and page from the query parameters
    word = request.args.get('word')
    page = request.args.get('page', default=1, type=int)
    per_page = 5  # Number of definitions per page
    
    # If no word is provided, return an error
    if not word:
        return jsonify({"error": "Please provide a word."}), 400
    
    # Scrape the definitions for the given page
    definitions, total_definitions, has_more = scrape_definition(word, page, per_page)
    
    # Create the response JSON
    response_data = {
        "word": word,
        "definitions": definitions,
        "page": page,
        "total_definitions": total_definitions,
        "has_more": has_more  # Indicates if there are more results
    }
    
    # Print the raw JSON response for debugging
    import json
    print("Raw JSON Response:", json.dumps(response_data, ensure_ascii=False))
    
    # Return the result as JSON with ensure_ascii=False
    return jsonify(response_data), 200, {'Content-Type': 'application/json; charset=utf-8'}

# Suggestions route
@app.route('/suggest', methods=['GET'])
def suggest():
    # Get the partial word from the query parameters
    partial_word = request.args.get('q')
    
    # If no partial word is provided, return an empty list
    if not partial_word:
        return jsonify([])
    
    # Define the URL for fetching suggestions
    url = f"https://www.jfdictionary.com/suggest.php?q={partial_word}"
    
    # Add the user-agent header
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Make the request with the headers
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'  # Ensure proper encoding
    
    # Parse the response (assuming the website returns a JSON array of suggestions)
    suggestions = response.json()
    
    # Return the suggestions as JSON
    return jsonify(suggestions)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)