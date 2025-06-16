import re, json

with open('neologismos.txt', 'r', encoding='utf-8') as file:
    content = file.read()

pattern = r'3\.2(.*?)3\.3'
match = re.search(pattern, content, re.DOTALL)

if match:
    glossario_raw = match.group(1)[14:].strip()
    glossario_raw = re.sub(r'\n', ' ', glossario_raw)
else:
    glossario_raw = ""

# remover nomes de publicações depois de exemplos”
glossario_raw = re.sub(r'” [^(]+', '” ', glossario_raw)

glossario = re.split(r'”.?\s*\(', glossario_raw)

dict = {}

def parse_entry(entry):
    title_pattern = r'(.+) \w\.'
    title = re.search(title_pattern, entry).group(1).strip()
    
    gender_pattern = r'.+ \w\.(\w)\.'
    gender = re.search(gender_pattern, entry).group(1)

    eng_trans = re.search(r'(.*)\[ing\]', entry)
    esp_trans = re.search(r';(.*)\[esp\]', entry, flags=re.DOTALL)
    
    definition_pattern = r'\]\n([\s\S]*?\.)'
    definition = re.search(definition_pattern, entry)

    definition = definition.group(1) if definition else ""

    sigla = re.search(r"Sigla: (.*)\n", definition)
    if sigla:
        sigla = sigla.group(1).strip()
        definition = re.sub(r"Sigla: (.*)\n", "", definition)

    encicl = re.search(r"Inf. encicl.: (.*?\.)", entry, flags=re.DOTALL)
    if encicl:
        encicl = encicl.group(1).replace("\n", " ").strip()

    usage_pattern = r'“([^”]*)'
    usage = re.search(usage_pattern, entry, flags=re.DOTALL)
    
    content = {
        'traducoes': {'en': {'tradução': eng_trans.group(1).replace("\n", " ").strip() if eng_trans else "", 'categoria': ''},
            'es': {'tradução': esp_trans.group(1).replace("\n", " ").strip() if esp_trans else "", 'categoria': ''}
            },
        'categoria' : "n " + gender,
        'descricao': [definition.replace("\n", " ").strip()],
        'exemplo': usage.group(1).replace("\n", " ").strip() if usage else ""
    }

    if sigla:
        content['sigla'] = sigla
    if encicl:
        content['enciclopedia'] = encicl
  
    return title, content

for conceito in glossario[:-1]: #remover ultima entrada pq é só (19, 12, ...)
    title, content = parse_entry(conceito)
    dict[title] = content

with open('neologismos.json', 'w', encoding='utf-8') as json_file:
    json.dump(dict, json_file, ensure_ascii=False, indent=4)