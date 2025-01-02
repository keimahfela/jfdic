from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

# Create the Flask app
app = Flask(__name__)

# Function to scrape the definition of a word
def scrape_definition(word):
    try:
        # Define the URL
        url = f"https://www.jfdictionary.com/search.php?terms={word}"
        
        # Add the user-agent header to mimic a browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Make the request with the headers
        response = requests.get(url, headers=headers)
        
        # Parse the response
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the definition (update the selector as needed)
        definition = soup.find('div', class_='definition')  # Update this selector
        if definition:
            return definition.get_text(strip=True)
        return "Definition not found."
    except Exception as e:
        return f"Error: {str(e)}"

# Root route
@app.route('/')
def home():
    return "Welcome to the Dictionary App!"

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
    
    # Return the result as JSON
    return jsonify({"word": word, "definition": definition})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)