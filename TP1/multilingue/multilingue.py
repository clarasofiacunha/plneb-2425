import re, json
from bs4 import BeautifulSoup

categorias = {
    r"n",
    r"n pl",
    r"n m",
    r"n m pl", 
    r"n f",
    r"n f pl",
    r"n m, f",
    r"n m/f",
    r"adj",
    r"v tr",
    r"v tr/intr",
    r"v intr"
}

remis = {
    r'sin. compl.',
    r'sin.',
    r'den. com.',
    r"sigla",
    r"veg."
}

langs = {
    r"oc",
    r"eu",
    r"gl",
    r"es",
    r"en",
    r"fr",
    r"pt",
    r"pt \[PT\]",
    r"pt \[BR\]",
    r"nl",
    r"ar"
}

codigos = {
    r"sbl",
    r"nc",
    r"CAS"
}

campos = {
    r"CONCEPTES GENERALS",
    r"EPIDEMIOLOGIA",
    r"ETIOPATOGÈNIA",
    r"DIAGNÒSTIC",
    r"CLÍNICA",
    r"PREVENCIÓ",
    r"TRACTAMENT",
    r"PRINCIPIS ACTIUS",
    r"ENTORN SOCIAL"
}

# NOTA

markers = "@#§★∞☣₿$"

with open('multilingue.xml', 'r', encoding='utf-8') as file:
    content = file.read()

soup = BeautifulSoup(content, features="xml")
pages = ""

for page in soup.find_all('page'):
    page_number = int(page['number'])
    
    if page_number % 2 == 0:
        left = 500
    else:
        left = 440
    
    if 30 <= page_number <= 182:
        left_column = ''
        right_column = ''

        for text in page.find_all('text'):
            if int(text['left']) < left:
                left_column += str(text) + '\n'
            else:
                right_column += str(text) + '\n'

        page = left_column + right_column
        pages += (page) #153 pages

pages = re.sub(r'<text font="6".*/text>\n', r'', pages) #sub dos page numbers
pages = re.sub(r'<.*font="14".*/text>\n', r'', pages) #sub do cabeçalho
pages = re.sub(r'<.*font="15".*/text>\n', r'', pages) #sub do cabeçalho
pages = re.sub(r'<.*font="36".*/text>\n', r'', pages) #sub das letras a bold no inicio dessa letra
pages = re.sub(r'<.*font="38".*/text>\n', r'', pages) #sub da letra na pag esquerda de cada letra
pages = re.sub(r'<.*?>', r'', pages) #rebentar com as tags

new_pages = ''
for line in pages.split('\n'):
    line = line.strip()
    if line in categorias:
        new_pages += '##' + line + '\n' # marcar as categorias com ##
    else:
        new_pages += line + '\n'

pages = new_pages

codigos_pattern = rf"^({'|'.join(codigos)})\n(?=[^{markers}])" # ^(sbl|CAS|nc)\n(?=[^#@§★∞☣])
pages = re.sub(codigos_pattern, r'§\1\n', pages, flags=re.MULTILINE) #marcar os codigos com §

traducao_pattern = rf"^({'|'.join(langs)})\n(?=[^{markers}])" # (^(en|eu|fr|gl|oc|ar|pt|pt \[BR\]|nl|es|pt \[PT\])\n)[^#@§★∞☣]
pages = re.sub(traducao_pattern, r'★\1\n', pages, flags=re.MULTILINE) #marcar as traducoes com ★

remis_pattern = rf"^({'|'.join(remis)})\n(?=[^{markers}])" # (^(veg.|den. com.|sin. compl.|sin.|sigla)\n)[^#@§★∞☣]
pages = re.sub(remis_pattern, r'∞\1\n', pages, flags=re.MULTILINE) # marcar os remis com ∞

campos_pattern = rf"^({'|'.join(campos)})\.(?=[^{markers}])" # (^(CONCEPTES GENERALS|EPIDEMIOLOGIA|ETIOPATOGÈNIA|DIAGNÒSTIC|CLÍNICA|PREVENCIÓ|TRACTAMENT|PRINCIPIS ACTIUS|ENTORN SOCIAL)\n)[^#@§★∞☣]
pages = re.sub(campos_pattern, r'☣\1\.', pages, flags=re.MULTILINE) #marcar os campos com ☣

nota_pattern = r"^(Nota:.*)"
pages = re.sub(nota_pattern, r'₿\1', pages, flags=re.MULTILINE) #marcar as notas com ₿

concept_pattern = r"(^[1-9]\d*(\n+.*){1,2}\n##.+?)"
pages = re.sub(rf"{concept_pattern}", r"@\1", pages, flags= re.MULTILINE)


dict = {}

glossario = pages.split('@')
glossario = glossario[1:]

for concept in glossario:

    title_pattern = r"^\d+((\n.*){1,2})\n##(.*)"
    title = re.search(title_pattern, concept, flags=re.MULTILINE)
    if title:
        title = title.group(1).replace('\n', ' ').strip()
        dict[title] = {}
    
    categoria_pattern = r"^\d+(\n.*){1,2}\n##(.*)"
    categoria = re.search(categoria_pattern, concept, flags=re.MULTILINE)
    if categoria:
        dict[title]["categoria"] = categoria.group(2).strip().replace('\n', ' ')

    gloss_trad = {}
    traducoes_pattern = rf"★((.*\n)*?)(@|§|∞|☣|₿|$)" # ★(.*\n)*?(@|§|∞|☣|₿|$)
    traduc = re.findall(traducoes_pattern, concept, flags=re.MULTILINE)
    if traduc:
        for tr in traduc:
            traducoes = tr[0]
            traducoes_list = re.split(r"★", traducoes.strip())
            for traducao in traducoes_list:
                traducao_split = traducao.split(";")
                if len(traducao_split) == 1:
                    if len(traducao.split('##')) > 1:
                        cat = traducao.split('##')[1].replace("\n", " ").strip()
                    else:  
                        cat = ''
                    
                    lang = traducao.split('##')[0].split('\n')[0].strip()
                    
                    trads = ''
                    
                    for trad in traducao.split('##')[0].split('\n')[1:]:
                        trads += trad.strip()
                    
                    gloss_trad[lang] = {
                        "tradução" : trads,
                        "categoria": cat
                        }
                else:
                    lang = traducao.split('##')[0].split('\n')[0].strip()
                    mult_trads = {}
                    for i, same_lang_trad in enumerate(traducao_split):
                        if len(same_lang_trad.split('##')) > 1:
                            cat = same_lang_trad.split('##')[1].replace("\n", " ").strip()
                        else:  
                            cat = ''
                        
                        if i == 0:
                            trads = ''
                            for trad in same_lang_trad.split('##')[0].split('\n')[1:]:
                                trads += trad.strip()
                        else:
                            trads = ''
                            for trad in same_lang_trad.split('##')[0].split('\n'):
                                trads += trad.strip()
                        
                        mult_trads[i+1] = {
                            "tradução" : trads,
                            "categoria": cat
                        }
                    gloss_trad[lang] = mult_trads

    dict[title]["traducoes"] = gloss_trad

    gloss_remis = {}
    remi_pattern = rf"∞((.*\n)*?)(@|§|★|☣|₿|$)" # ∞((.*\n)*?)(@|§|★|☣|₿|$)
    remiss = re.findall(remi_pattern, concept, flags=re.MULTILINE)
    if remiss:
        for remis in remiss:
            remis = remis[0]
            remis_list = re.split(r"∞", remis.strip())
            for remi in remis_list:
                remi_split = remi.split(";")
                if len(remi_split) == 1:
                    remi_code = remi.split('\n')[0]
                    if len(remi.split('##')) > 1:
                        cat = remi.split('##')[1].replace("\n", " ").strip()
                    else:  
                        cat = ''
                
                    remi_text = ''
                    for remi_text_line in remi.split('##')[0].split('\n')[1:]:
                        remi_text += remi_text_line.strip().replace('\n', ' ')
                        
                    gloss_remis[remi_code] = {
                        "texto" : remi_text,
                        "categoria": cat
                        }
                    
                else:
                    remi_code = remi.split('##')[0].split('\n')[0].strip()
                    mult_remi = {}
                    for i, same_remi in enumerate(remi_split):
                        if len(same_remi.split('##')) > 1:
                            cat = same_remi.split('##')[1].replace("\n", " ").strip()
                        else:
                            cat = ''
                            
                        if i == 0:
                            remi_text = ''
                            for remi_text_line in same_remi.split('##')[0].split('\n')[1:]:
                                remi_text += remi_text_line.strip().replace('\n', ' ')
                        else:   
                            remi_text = ''
                            for remi_text_line in same_remi.split('##')[0].split('\n'):
                                remi_text += remi_text_line.strip().replace('\n', ' ')
                        
                        mult_remi[i+1] = {
                            "texto" : remi_text,
                            "categoria": cat
                        }
                    gloss_remis[remi_code] = mult_remi                
    dict[title]["remis"] = gloss_remis

    gloss_codigos = {}
    codigos_pattern = rf"§((.*\n)*?)(?={'|'.join(markers)})" # §((.*\n)*?)(?=@|#|§|★|∞|☣|₿|$)
    codigos = re.findall(codigos_pattern, concept, flags=re.MULTILINE)
    if codigos:
        #print(codigos)
        for codigo in codigos:
            codigo = codigo[0]
            codigo_code = codigo.split('\n')[0].strip()
            codigo_text = ''
            for codigo_text_line in codigo.split('\n')[1:]:
                codigo_text += codigo_text_line.strip().replace('\n', ' ')
            gloss_codigos[codigo_code] = codigo_text
    
    dict[title]["codigos"] = gloss_codigos
    
    campos_pattern = rf"☣.*\.((.*\n)*?)(?={'|'.join(markers)})" # ☣.*\.((.*\n)*?)(?=@|#|§|★|∞|☣|₿|$)
    campos = re.search(campos_pattern, concept, flags=re.MULTILINE)
    if campos:
        dict[title]['descricao'] = campos.group(1).strip().replace('\n', ' ')
        
    nota_pattern = rf"₿Nota:((.*\n)*?)(?={'|'.join(markers)})" # ₿Nota:((.*\n)*?)(?=@|#|§|★|∞|☣|₿|$)
    notas = re.search(nota_pattern, concept, flags=re.MULTILINE)
    if notas:
        notas = notas.group(1).strip()
        notas_list = re.split(r"^\d+\.", notas, flags=re.MULTILINE)
        if len(notas_list) > 1:
            notas = [nota.strip().replace('\n', ' ') for nota in notas_list[1:]]
        else:
            notas = notas.replace('\n', ' ')
        dict[title]['Notas'] = notas

with open('multilingue.json', 'w', encoding='utf-8') as json_file:
    json.dump(dict, json_file, ensure_ascii=False, indent=4)