import requests
from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Fetch country data from REST Countries API
def get_countries():
    try:
        response = requests.get("https://restcountries.com/v3.1/all?fields=name,capital")
        data = response.json()
        # Sort countries alphabetically by name
        countries = []
        for country in data:
            name = country.get('name', {}).get('common', 'Unknown')
            capital_list = country.get('capital', ['No Capital'])
            capital = capital_list[0] if capital_list else 'No Capital'
            countries.append({'name': name, 'capital': capital})
        
        return sorted(countries, key=lambda x: x['name'])
    except Exception as e:
        print(f"Error fetching countries: {e}")
        return [{'name': 'Error', 'capital': 'Could not load data'}]

@app.route('/')
def index():
    countries = get_countries()
    return render_template('index.html', countries=countries)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    # Ensure templates and static directories exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    app.run(debug=True, port=5001)
