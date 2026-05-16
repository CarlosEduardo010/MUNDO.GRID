import requests
from jinja2 import Environment, FileSystemLoader
import os

def get_countries():
    print("Obteniendo datos de países...")
    try:
        response = requests.get("https://restcountries.com/v3.1/all?fields=name,capital")
        data = response.json()
        countries = []
        for country in data:
            name = country.get('name', {}).get('common', 'Unknown')
            capital_list = country.get('capital', ['No Capital'])
            capital = capital_list[0] if capital_list else 'No Capital'
            countries.append({'name': name, 'capital': capital})
        
        return sorted(countries, key=lambda x: x['name'])
    except Exception as e:
        print(f"Error: {e}")
        return []

def export():
    countries = get_countries()
    if not countries:
        print("No se pudieron obtener los países. Abortando exportación.")
        return

    # Set up Jinja2
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')

    # Render template with static paths relative for GitHub Pages
    # We pass None for url_for to trigger the fallback in our template
    html_content = template.render(countries=countries, url_for=None)

    # Save to index.html at root
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("¡Éxito! index.html ha sido generado y está listo para GitHub Pages.")

if __name__ == '__main__':
    export()
