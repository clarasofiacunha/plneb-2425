import re
import json

with open('populares.xml', 'r', encoding='utf-8') as file:
    content = file.read()

start_pattern = r"<text[^>]*><b>A</b></text>"
start_match = re.search(start_pattern, content)
content = content[start_match.start():] if start_match else ""

tags = [
    r"</?fontspec.*?>", 
    r"</?page.*?>", 
    r"</?text.*?>", 
    r"<i>", 
    r"</i>"
    ]

content = re.sub(r"<.*>[A-Z]<.*>", "", content) # letras

for tag in tags:
    content = re.sub(tag, "", content)

terms = re.findall(r"<b>(.*?)</b>", content)
terms = [termo.strip() for termo in terms]

# remoções
processed_content = re.sub(r"<b>.*?</b>", "", content) # termos
processed_content= re.sub(r"\n+", " ", processed_content) # paragrafos
processed_content = re.sub(r"\s+,", "", processed_content) # espaços
processed_content = re.sub(r"\s{2,}", " ", processed_content) # múltiplos espaços

#marcar
processed_content = re.sub(r"\(pop\)", "@@", processed_content) 

design = re.findall(r"(?:@(?:\s|,|X)|^)(.*?)@", processed_content)
design = [desc.strip() for desc in design]

# Construir dicionário
glossario_dict = dict(zip(terms, design))

for termo, descricao in zip(terms, design):
    if termo in glossario_dict:
        if isinstance(glossario_dict[termo], list):
            if descricao not in glossario_dict[termo]:
                glossario_dict[termo].append(descricao)
        else:
            if descricao != glossario_dict[termo]:
                glossario_dict[termo] = [glossario_dict[termo], descricao]
    else:
        glossario_dict[termo] = descricao

for termo, descricao in glossario_dict.items():
    glossario_dict[termo] = {'descricao': descricao}

# Salvar em JSON
with open("populares.json", "w", encoding="utf-8") as output:
    json.dump(glossario_dict, output, ensure_ascii=False, indent=4)
