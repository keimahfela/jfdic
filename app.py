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
def scrape_definition(word):
    try:
        # Define the URL
        url = f"https://www.jfdictionary.com/search.php?terms={word}"
        
        # Add the user-agent header
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Make the request with the headers
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'  # Ensure proper encoding
        
        # Parse the response
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the definition using the correct selector
        definition = soup.find('div', class_='details')  # Updated selector
        if definition:
            return normalize_text(definition.get_text(strip=True))
        return "Definition not found."
    except Exception as e:
        return f"Error: {str(e)}"

# Root route
@app.route('/')
def home():
    return render_template('index.html')  # Serve the index.html file

# Search route
@app.route('/search', methods=['GET'])
def search():
    # Get the word from the query parameters
    word = request.args.get('word')
    
    # If no word is provided, return an error
    if not word:
        return jsonify({"error": "Please provide a word."}), 400
    
    # Scrape the definition
    definition = scrape_definition(word)
    
    # Create the response JSON
    response_data = {"word": word, "definition": definition}
    
    # Print the raw JSON response for debugging
    import json
    print("Raw JSON Response:", json.dumps(response_data, ensure_ascii=False))
    
    # Return the result as JSON with ensure_ascii=False
    return jsonify(response_data), 200, {'Content-Type': 'application/json; charset=utf-8'}

# Run the app
if __name__ == '__main__':
    app.run(debug=True)