import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.chlo.min-saude.pt/index.php/component/seoglossary/1-glossario?start=0"

def get_html(url):
    # Add headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        # Add a random delay to avoid being detected as a bot
        #time.sleep(random.uniform(1, 3))
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        print(f"Fetched HTML content from {url} - Status: {response.status_code}")
        return response.text
        
    except requests.RequestException as e:
        print(f"Failed to fetch HTML content from {url}: {e}")
        return None

def get_pages():
    url = BASE_URL
    html_content = get_html(url)
    soup = BeautifulSoup(html_content, "html.parser")
    
    pages = []
    pages.append(url)
    
    next_page = soup.find("li", class_="pagination-next").a
    
    while next_page:  
        new_url = "https://www.chlo.min-saude.pt/" + next_page["href"]
        pages.append(new_url)
        html_content = get_html(new_url)
        soup = BeautifulSoup(html_content, "html.parser")
        next_page = soup.find("li", class_="pagination-next").a

    return pages

def get_glossary_data(url):
    html_content = get_html(url)
    soup = BeautifulSoup(html_content, "html.parser")
    
    glossary_items = soup.find("table", class_="glossaryclear table").tbody.find_all("tr")
    
    data = {}
    
    for tr in glossary_items:
        
        tds = tr.find_all("td")
        
        term, definition = tds[0].text.strip(), tds[1].text.strip()
        
        split = definition.split('Sinónimos -')
        
        description = [split[0].strip()]
        
        data[term.lower()] = {'descricao': description, 'remis': {'sin.': split[1].strip()} if len(split) > 1 else {}}

    return data

def scrape_glossary():
    pages = get_pages()
    all_data = {}

    for page in pages:
        data = get_glossary_data(page)
        all_data.update(data)

    return all_data

if __name__ == "__main__":
    data = scrape_glossary()
    with open("min_saude.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)