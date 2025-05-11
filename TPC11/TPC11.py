import json
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://revista.spmi.pt/index.php/rpmi/issue/archive'
articles = {}

def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def iterate_archive_pages(base_link, total_pages=6):
    for page_num in range(1, total_pages + 1):
        page_url = f"{base_link}/{page_num}" if page_num > 1 else base_link
        extract_issues_from_archive(page_url)

def extract_issues_from_archive(archive_url):
    soup = fetch_html(archive_url)
    issue_list = soup.find('ul', class_="issues_archive")

    for issue_item in issue_list.find_all('li'):
        issue_link = issue_item.a['href']
        extract_issue_data(issue_link)

def extract_issue_data(issue_url):
    soup = fetch_html(issue_url)
    page_content = soup.find('div', class_="page page_issue")

    issue_title = page_content.h1.text.strip()
    print(f"A processar: {issue_title}")

    issue_date = page_content.find('span', class_="value").text.strip()
    section_container = page_content.find('div', class_="sections")

    article_blocks = section_container.find_all('div', class_="obj_article_summary")
    artigos = [extract_article_data(article.h3.a['href']) for article in article_blocks]

    articles[issue_title] = {
        "URL": issue_url,
        "data_publicacao": issue_date,
        "artigos": artigos
    }

def extract_article_data(article_url):
    soup = fetch_html(article_url)
    article_data = {
        "URL": article_url
    }

    article_section = soup.find('article', class_="obj_article_details")
    article_data['titulo'] = article_section.h1.text.strip()

    main_entry = article_section.find('div', class_="main_entry")

    # Autores
    autores = [nome.text.strip() for nome in main_entry.find_all('span', class_="name")]
    article_data['autores'] = autores

    # DOI
    doi_section = main_entry.find('section', class_="item doi")
    article_data['DOI'] = doi_section.a['href'] if doi_section else None

    # Keywords
    keywords_section = main_entry.find('section', class_="item keywords")
    if keywords_section:
        raw_keywords = keywords_section.span.text.strip().split(',')
        keywords = [k.strip() for k in raw_keywords if k.strip() and k.strip() != "."]
        article_data['keywords'] = keywords if keywords else []

    # Abstract
    abstract_section = main_entry.find('section', class_="item abstract")
    if abstract_section:
        abstract = [p.text.strip() for p in abstract_section.find_all('p')]
        article_data['abstract'] = abstract

    return article_data

if __name__ == '__main__':
    iterate_archive_pages(BASE_URL)

    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=4, ensure_ascii=False)