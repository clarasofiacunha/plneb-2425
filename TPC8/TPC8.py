import json
import requests
from bs4 import BeautifulSoup


URL_BASE = "https://www.atlasdasaude.pt"

def extrair_data(div_conteudo):
    div_data = div_conteudo.find('div', class_="field-name-post-date")
    if div_data:
        return div_data.div.div.text
    return None

def extrair_conteudo(div_conteudo):
    div_info = div_conteudo.find('div', class_="field-name-body")
    if not div_info:
        return None

    info = {"Descrição": []}
    titulo = "Descrição"
    elemento = div_info.find("div", class_="field-item even")

    for item in elemento:
        if item.name in ['p', 'div']:
            info[titulo].append(item.text.replace(" ", " "))

        elif item.name == 'h2':
            titulo = item.text.replace(" ", "").title()
            info[titulo] = []

        elif item.name == 'ul':
            info[titulo].append([i.text for i in item.find_all('li')])

        elif item.name == 'h3':
            link = {item.text.replace(" ", ""): item.a["href"]}
            if len(info[titulo]) == 0:
                info[titulo].append(link)
            else:
                info[titulo][0] = info[titulo][0] | link

    return info

def extrair_fonte(div_conteudo):
    div_fonte = div_conteudo.find('div', class_="field-name-field-fonte")
    if div_fonte:
        return div_fonte.find('div', class_="field-item even").text
    return None

def extrair_site(div_conteudo):
    div_site = div_conteudo.find('div', class_="field-name-field-site")
    if div_site:
        return div_site.find('div', class_="field-item even").text
    return None

def extrair_nota(div_conteudo):
    div_nota = div_conteudo.find("div", class_="field-name-field-nota")
    if div_nota:
        return div_nota.find("div", class_="field-item even").text
    return None

def obter_info_doenca(url):
    link_completo = URL_BASE + url
    resposta = requests.get(link_completo)
    sopa = BeautifulSoup(resposta.text, 'html.parser')

    div_conteudo = sopa.find('div', class_="node-doencas")
    informacao = {}

    data = extrair_data(div_conteudo)
    if data:
        informacao["Data"] = data

    conteudo = extrair_conteudo(div_conteudo)
    if conteudo:
        informacao["Informação"] = conteudo

    fonte = extrair_fonte(div_conteudo)
    if fonte:
        informacao["Fonte"] = fonte

    site = extrair_site(div_conteudo)
    if site:
        informacao["Site"] = site

    nota = extrair_nota(div_conteudo)
    if nota:
        informacao["Nota"] = nota

    return {"URL": link_completo, "Conteúdo": informacao}

def obter_doencas_por_letra(letra):
    url = f"{URL_BASE}/doencasAaZ/{letra}"
    resposta = requests.get(url)
    sopa = BeautifulSoup(resposta.text, 'html.parser')

    doencas = {}
    for elemento in sopa.find_all('div', class_="views-row"):
        nome = elemento.div.h3.a.text.strip()
        url_doenca = elemento.div.h3.a['href']
        info = obter_info_doenca(url_doenca)

        resumo_div = elemento.find("div", class_="views-field-body")
        resumo = resumo_div.div.text.strip().replace(" ", " ")
        info["Resumo"] = resumo

        doencas[nome] = info

    return doencas

def obter_todas_as_doencas():
    todas = {}
    for codigo in range(ord("a"), ord("z") + 1):
        letra = chr(codigo)
        print(f"A obter doenças com a letra: {letra}")
        todas.update(obter_doencas_por_letra(letra))
    return todas

if __name__ == "__main__":
    todas_as_doencas = obter_todas_as_doencas()
    with open("doencas.json", "w", encoding="utf-8") as ficheiro:
        json.dump(todas_as_doencas, ficheiro, indent=4, ensure_ascii=False)