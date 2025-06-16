from flask import Flask, render_template, request, redirect, url_for
import json
import unicodedata
import re

app = Flask(__name__)

def load_data():
    with open('final_final.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data

def normalize(text):
    if not text:
        return text
    normalized = unicodedata.normalize('NFD', text)
    normalized = ''.join([c for c in normalized if not unicodedata.combining(c)])
    normalized = re.sub(r'[^\w]', '', normalized).strip()
    return normalized.upper()

def extract_translation(lang_data):
    if isinstance(lang_data, dict):
        if 'tradução' in lang_data:
            return {
                'texto': lang_data['tradução'],
                'categoria': lang_data.get('categoria', '')
            }
        elif '1' in lang_data:
            translations = []
            i = 1
            while str(i) in lang_data:
                if 'tradução' in lang_data[str(i)]:
                    translations.append(lang_data[str(i)]['tradução'])
                i += 1
            return {
                'texto': '; '.join(translations) if translations else '',
                'categoria': lang_data.get('1', {}).get('categoria', '')
            }
    return {'texto': lang_data, 'categoria': ''}

def extract_remis_list(remis_dict, key):
    result = []
    if not remis_dict or key not in remis_dict:
        return result
    entry = remis_dict[key]
    if isinstance(entry, dict):
        if 'texto' in entry:
            result.append({'texto': entry.get('texto', ''), 'categoria': entry.get('categoria', '')})
        else:
            for _, item in sorted(entry.items()):
                if isinstance(item, dict):
                    result.append({'texto': item.get('texto', ''), 'categoria': item.get('categoria', '')})
    return result

def process_translation(translation_text, category):
    if not translation_text:
        return None
    translations = [t.strip() for t in translation_text.split(';') if t.strip()]
    categories = [c.strip() for c in category.split(';')] if category else [''] * len(translations)
    if len(translations) == 1:
        return {"tradução": translations[0], "categoria": categories[0] if categories else ''}
    else:
        result = {}
        for i, trans in enumerate(translations, 1):
            cat = categories[i-1] if i-1 < len(categories) else ''
            result[str(i)] = {"tradução": trans, "categoria": cat}
        return result

def highlight_term(text, search_term, exact_match=False):
    if not search_term or not text:
        return text
    
    if exact_match:
        pattern = r'\b(' + re.escape(search_term) + r')\b'
        return re.sub(pattern, r'<b>\1</b>', text, flags=re.IGNORECASE)
    else:
        # Simple case-insensitive replacement
        pattern = re.escape(search_term)
        return re.sub(f'({pattern})', r'<b>\1</b>', text, flags=re.IGNORECASE)

@app.route('/')
def index():
    data = load_data()
    sorted_keys = sorted(data.keys(), key=lambda x: normalize(x))
    sorted_data = {k: data[k] for k in sorted_keys}

    letter = request.args.get('letter', '').upper()
    trad_lang = request.args.get('trad_lang', '').strip()
    search_term = request.args.get('search_term', '').strip()
    campo = request.args.get('campo', '').strip()
    cluster = request.args.get('cluster', '').strip()  # novo filtro

    if search_term:
        return search()

    # Aplicar filtro por letra
    if letter:
        filtered_items = [(k, v) for k, v in sorted_data.items() if normalize(k[0]) == letter or (normalize(k[0]) == '' and normalize(k[1]) == letter)]
    else:
        filtered_items = list(sorted_data.items())

    if trad_lang:
        filtered_items = [(k, v) for k, v in filtered_items if v.get('traducoes', {}).get(trad_lang)]

    if campo:
        filtered_items = [(k, v) for k, v in filtered_items if v.get('campo', '').lower() == campo.lower()]

    if cluster:
        filtered_items = [(k, v) for k, v in filtered_items if v.get('cluster', '').lower() == cluster.lower()]

    filtered_items.sort(key=lambda item: normalize(item[0]))
    filtered_data = dict(filtered_items)

    letters = sorted({normalize(k[0]) for k in data.keys() if k and k[0].isalpha()})

    idiomas = set()
    campos = set()
    clusters = set()
    for v in data.values():
        if 'traducoes' in v:
            idiomas.update(v['traducoes'].keys())
        if 'campo' in v and v['campo']:
            campos.add(v['campo'])
        if 'cluster' in v and v['cluster']:
            clusters.add(v['cluster'])
    idiomas = sorted(idiomas)
    campos = sorted(campos)
    clusters = sorted(clusters)

    return render_template(
        'index.html',
        data=filtered_data,
        search_term='',
        letters=letters,
        selected_letter=letter,
        idiomas=idiomas,
        trad_lang=trad_lang,
        campos=campos,
        selected_campo=campo,
        clusters=clusters,
        selected_cluster=cluster
    )

@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('search_term', '').strip()
    search_in_term = request.args.get('search_in_term')
    search_in_desc = request.args.get('search_in_desc')
    exact_match = request.args.get('exact_match')
    trad_lang = request.args.get('trad_lang', '').strip()
    letter = request.args.get('letter', '').upper()
    cluster = request.args.get('cluster', '').strip()

    if not search_in_term and not search_in_desc:
        search_in_term = 'on'
        search_in_desc = 'on'

    if not search_term:
        return index()

    data = load_data()
    results = {}

    pattern = r'\b' + re.escape(search_term) + r'\b'

    for term, entry in data.items():
        term_match = False
        desc_match = False

        if search_in_term:
            if exact_match:
                if re.search(pattern, term, re.IGNORECASE):
                    term_match = True
            else:
                term_match = search_term.lower() in term.lower()

        if search_in_desc and 'descricao' in entry:
            for desc_item in entry['descricao']:
                if type(desc_item) is str:
                    if exact_match:
                        if re.search(pattern, desc_item, re.IGNORECASE):
                            desc_match = True
                            break
                    else:
                        if search_term.lower() in desc_item.lower():
                            desc_match = True
                            break

        if term_match or desc_match:
            highlighted_entry = entry.copy()
            
            highlighted_term = highlight_term(term, search_term, exact_match == 'on')
            
            if 'descricao' in highlighted_entry:
                highlighted_desc = []
                for desc in highlighted_entry['descricao']:
                    if isinstance(desc, str):
                        highlighted_desc.append(highlight_term(desc, search_term, exact_match == 'on'))
                    else:
                        highlighted_desc.append(desc)
                highlighted_entry['descricao'] = highlighted_desc
            
            results[term] = highlighted_entry
            results[term]['_highlighted_term'] = highlighted_term

    # Filtro por letra
    if letter:
        results = {k: v for k, v in results.items() if normalize(k[0]) == letter}

    # Filtro por idioma
    if trad_lang:
        results = {k: v for k, v in results.items() if v.get('traducoes', {}).get(trad_lang)}

    # Filtro por cluster
    if cluster:
        results = {k: v for k, v in results.items() if v.get('cluster', '').lower() == cluster.lower()}

    letters = sorted({normalize(k[0]) for k in data.keys() if k and k[0].isalpha()})
    idiomas = set()
    clusters = set()
    for v in data.values():
        if 'traducoes' in v:
            idiomas.update(v['traducoes'].keys())
        if 'cluster' in v and v['cluster']:
            clusters.add(v['cluster'])
    idiomas = sorted(idiomas)
    clusters = sorted(clusters)

    return render_template('index.html', data=results, search_term=search_term, exact_match=exact_match,
                          search_in_term=search_in_term, search_in_desc=search_in_desc,
                          letters=letters, selected_letter=letter,
                          idiomas=idiomas, trad_lang=trad_lang,
                          clusters=clusters, selected_cluster=cluster,
                          highlight_search=True)

def find_similar_terms(target_term, target_entry, data, max_terms=5):
    if not target_term or not target_entry:
        return []
    
    similarities = {}
    target_words = set(re.findall(r'\b\w+\b', target_term.lower()))
    
    # Get target cluster and campo
    target_cluster = target_entry.get('cluster', '').lower()
    target_campo = target_entry.get('campo', '').lower()
    
    # Get target description words
    target_desc_words = set()
    if 'descricao' in target_entry:
        for desc in target_entry['descricao']:
            if isinstance(desc, str):
                target_desc_words.update(set(re.findall(r'\b\w+\b', desc.lower())))
    
    for term, entry in data.items():
        if term == target_term:
            continue
            
        score = 0
        
        # Cluster match
        if entry.get('cluster', '').lower() == target_cluster and target_cluster:
            score += 3
            
        # Campo match
        if entry.get('campo', '').lower() == target_campo and target_campo:
            score += 2
            
        # Term word matches
        term_words = set(re.findall(r'\b\w+\b', term.lower()))
        word_overlap = target_words.intersection(term_words)
        score += len(word_overlap) * 2
        
        # Description matches
        if 'descricao' in entry:
            entry_desc_words = set()
            for desc in entry['descricao']:
                if isinstance(desc, str):
                    entry_desc_words.update(set(re.findall(r'\b\w+\b', desc.lower())))
            
            desc_overlap = target_desc_words.intersection(entry_desc_words)
            score += min(len(desc_overlap) / 3, 3)  # Cap description score
        
        if score > 0:
            similarities[term] = score
    
    # Sort by score (descending) and return top max_terms
    sorted_terms = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
    return [(term, data[term]) for term, _ in sorted_terms[:max_terms]]

@app.route('/entry/<term>')
def entry_detail(term):
    data = load_data()
    letter = request.args.get('letter', '')
    if term in data:
        # Find similar terms
        similar_terms = find_similar_terms(term, data[term], data)
        return render_template('entry_detail.html', term=term, entry=data[term], letter=letter, similar_terms=similar_terms)
    return render_template('index.html', data={}, search_term='', error=f"Termo '{term}' não encontrado")

@app.route('/edit/<term>', methods=['GET'])
def edit_entry_form(term):
    data = load_data()
    if term not in data:
        return render_template('index.html', data={}, search_term='', error=f"Termo '{term}' não encontrado")
    entry = data[term]

    sinonimos_list = extract_remis_list(entry.get('remis', {}), 'sin. compl.')
    antonimos_list = extract_remis_list(entry.get('remis', {}), 'ant')
    siglas_list = extract_remis_list(entry.get('remis', {}), 'sigla')

    traducoes = entry.get('traducoes', {})
    traducao_en_data = extract_translation(traducoes.get('en', ''))
    traducao_es_data = extract_translation(traducoes.get('es', ''))
    traducao_fr_data = extract_translation(traducoes.get('fr', ''))
    traducao_de_data = extract_translation(traducoes.get('de', ''))
    traducao_oc_data = extract_translation(traducoes.get('oc', ''))
    traducao_eu_data = extract_translation(traducoes.get('eu', ''))
    traducao_gl_data = extract_translation(traducoes.get('gl', ''))
    traducao_nl_data = extract_translation(traducoes.get('nl', ''))
    traducao_ar_data = extract_translation(traducoes.get('ar', ''))
    traducao_pt_br_data = extract_translation(traducoes.get('pt [BR]', ''))
    traducao_pt_pt_data = extract_translation(traducoes.get('pt [PT]', ''))

    codigos = entry.get('codigos', {})

    # Obter todos os clusters disponíveis
    clusters = set()
    for v in data.values():
        if 'cluster' in v and v['cluster']:
            clusters.add(v['cluster'])
    clusters_list = sorted(clusters)

    return render_template('add_entry.html',
        is_edit=True,
        original_term=term,
        term=term,
        campo=entry.get('campo', ''),
        cluster=entry.get('cluster', ''),
        clusters_list=clusters_list,
        categoria=entry.get('categoria', ''),
        descricao=entry.get('descricao', ['']),
        traducao_en=traducao_en_data['texto'],
        categoria_traducao_en=traducao_en_data['categoria'],
        traducao_es=traducao_es_data['texto'],
        categoria_traducao_es=traducao_es_data['categoria'],
        traducao_fr=traducao_fr_data['texto'],
        categoria_traducao_fr=traducao_fr_data['categoria'],
        traducao_de=traducao_de_data['texto'],
        categoria_traducao_de=traducao_de_data['categoria'],
        traducao_oc=traducao_oc_data['texto'],
        categoria_traducao_oc=traducao_oc_data['categoria'],
        traducao_eu=traducao_eu_data['texto'],
        categoria_traducao_eu=traducao_eu_data['categoria'],
        traducao_gl=traducao_gl_data['texto'],
        categoria_traducao_gl=traducao_gl_data['categoria'],
        traducao_nl=traducao_nl_data['texto'],
        categoria_traducao_nl=traducao_nl_data['categoria'],
        traducao_ar=traducao_ar_data['texto'],
        categoria_traducao_ar=traducao_ar_data['categoria'],
        traducao_pt_br=traducao_pt_br_data['texto'],
        categoria_traducao_pt_br=traducao_pt_br_data['categoria'],
        traducao_pt_pt=traducao_pt_pt_data['texto'],
        categoria_traducao_pt_pt=traducao_pt_pt_data['categoria'],
        sinonimos_list=sinonimos_list,
        antonimos_list=antonimos_list,
        codigo_cas=codigos.get('CAS', ''),
        codigo_sbl=codigos.get('sbl', ''),
        codigo_icd=codigos.get('ICD', ''),
        codigo_outro=codigos.get('outro', ''),
        siglas_list=siglas_list,
        exemplo=entry.get('exemplo', ''),
        enciclopedia=entry.get('enciclopedia', ''),
        sigla=entry.get('sigla', ''),
        notas=entry.get('Notas', '')
    )

@app.route('/add', methods=['GET'])
def add_entry_form():
    data = load_data()
    clusters = set()
    for v in data.values():
        if 'cluster' in v and v['cluster']:
            clusters.add(v['cluster'])
    clusters_list = sorted(clusters)
    
    return render_template('add_entry.html', is_edit=False, descricao=[''], clusters_list=clusters_list)

@app.route('/add', methods=['POST'])
def add_entry_submit():
    term = request.form.get('term', '').strip()
    original_term = request.form.get('original_term', '').strip()
    is_edit = original_term != ''
    campo = request.form.get('campo', '').strip()
    cluster = request.form.get('cluster', '').strip()
    categoria = request.form.get('categoria', '').strip()
    descricao = request.form.getlist('descricao[]')
    descricao = [d.strip() for d in descricao if d.strip()]

    def get_translation_field(lang):
        traducoes = request.form.getlist(f'traducao_{lang}[]')
        categorias = request.form.getlist(f'categoria_traducao_{lang}[]')
        pairs = [(t.strip(), c.strip()) for t, c in zip(traducoes, categorias) if t.strip()]
        if not pairs:
            return '', ''
        trads = ';'.join([t for t, _ in pairs])
        cats = ';'.join([c for _, c in pairs])
        return trads, cats

    traducao_en, categoria_traducao_en = get_translation_field('en')
    traducao_es, categoria_traducao_es = get_translation_field('es')
    traducao_fr, categoria_traducao_fr = get_translation_field('fr')
    traducao_de, categoria_traducao_de = get_translation_field('de')
    traducao_oc, categoria_traducao_oc = get_translation_field('oc')
    traducao_eu, categoria_traducao_eu = get_translation_field('eu')
    traducao_gl, categoria_traducao_gl = get_translation_field('gl')
    traducao_nl, categoria_traducao_nl = get_translation_field('nl')
    traducao_ar, categoria_traducao_ar = get_translation_field('ar')
    traducao_pt_br, categoria_traducao_pt_br = get_translation_field('pt_br')
    traducao_pt_pt, categoria_traducao_pt_pt = get_translation_field('pt_pt')

    # Get remission fields
    sinonimos_texto = request.form.getlist('sinonimos_texto[]')
    sinonimos_categoria = request.form.getlist('sinonimos_categoria[]')
    antonimos_texto = request.form.getlist('antonimos_texto[]')
    antonimos_categoria = request.form.getlist('antonimos_categoria[]')
    
    # Get code fields
    codigo_cas = request.form.get('codigo_cas', '').strip()
    codigo_sbl = request.form.get('codigo_sbl', '').strip()
    codigo_icd = request.form.get('codigo_icd', '').strip()
    codigo_outro = request.form.get('codigo_outro', '').strip()
    
    # Get siglas fields
    siglas_texto = request.form.getlist('siglas_texto[]')
    siglas_categoria = request.form.getlist('siglas_categoria[]')
    
    # Get example fields
    exemplo = request.form.get('exemplo', '').strip()
    enciclopedia = request.form.get('enciclopedia', '').strip()
    sigla = request.form.get('sigla', '').strip()
    
    # Get notes
    notas = request.form.get('notas', '').strip()
    
    if not term:
        return render_template('add_entry.html', error="O termo é obrigatório.", is_edit=is_edit, original_term=original_term, descricao=descricao)
    
    if not descricao:
        sinonimos_list = []
        for t, c in zip(sinonimos_texto, sinonimos_categoria):
            if t.strip():
                sinonimos_list.append({'texto': t, 'categoria': c})
        
        antonimos_list = []
        for t, c in zip(antonimos_texto, antonimos_categoria):
            if t.strip():
                antonimos_list.append({'texto': t, 'categoria': c})
                
        return render_template('add_entry.html', 
                              error="A descrição é obrigatória.", 
                              is_edit=is_edit,
                              original_term=original_term,
                              term=term,
                              campo=campo,
                              cluster=cluster,
                              categoria=categoria,
                              descricao=descricao,
                              traducao_en=traducao_en,
                              categoria_traducao_en=categoria_traducao_en,
                              traducao_es=traducao_es,
                              categoria_traducao_es=categoria_traducao_es,
                              traducao_fr=traducao_fr,
                              categoria_traducao_fr=categoria_traducao_fr,
                              traducao_de=traducao_de,
                              categoria_traducao_de=categoria_traducao_de['categoria'],
                              traducao_oc=traducao_oc,
                              categoria_traducao_oc=categoria_traducao_oc,
                              traducao_eu=traducao_eu,
                              categoria_traducao_eu=categoria_traducao_eu,
                              traducao_gl=traducao_gl,
                              categoria_traducao_gl=categoria_traducao_gl,
                              traducao_nl=traducao_nl,
                              categoria_traducao_nl=categoria_traducao_nl,
                              traducao_ar=traducao_ar,
                              categoria_traducao_ar=categoria_traducao_ar['categoria'],
                              traducao_pt_br=traducao_pt_br,
                              categoria_traducao_pt_br=categoria_traducao_pt_br['categoria'],
                              traducao_pt_pt=traducao_pt_pt,
                              categoria_traducao_pt_pt=categoria_traducao_pt_pt['categoria'],
                              sinonimos_list=sinonimos_list,
                              antonimos_list=antonimos_list,
                              codigo_cas=codigo_cas,
                              codigo_sbl=codigo_sbl,
                              codigo_icd=codigo_icd,
                              codigo_outro=codigo_outro,
                              exemplo=exemplo,
                              enciclopedia=enciclopedia,
                              sigla=sigla,
                              notas=notas)
    
    data = load_data()
    
    # Check if the term already exists
    term_exists = term in data
    is_duplicate_term = term_exists and (not is_edit or (is_edit and term != original_term))
    
    if is_duplicate_term:
        sinonimos_list = []
        for t, c in zip(sinonimos_texto, sinonimos_categoria):
            if t.strip():
                sinonimos_list.append({'texto': t, 'categoria': c})
        
        antonimos_list = []
        for t, c in zip(antonimos_texto, antonimos_categoria):
            if t.strip():
                antonimos_list.append({'texto': t, 'categoria': c})
                
        error_message = f"O termo '{term}' já existe no dicionário. Não é possível adicionar ou editar para um termo duplicado."
        
        return render_template('add_entry.html', 
                              error=error_message, 
                              is_edit=is_edit,
                              original_term=original_term,
                              term=term,
                              campo=campo,
                              cluster=cluster,
                              categoria=categoria, 
                              descricao=descricao,
                              traducao_en=traducao_en,
                              categoria_traducao_en=categoria_traducao_en,
                              traducao_es=traducao_es,
                              categoria_traducao_es=categoria_traducao_es,
                              traducao_fr=traducao_fr,
                              categoria_traducao_fr=categoria_traducao_fr,
                              traducao_de=traducao_de,
                              categoria_traducao_de=categoria_traducao_de,
                              traducao_oc=traducao_oc,
                              categoria_traducao_oc=categoria_traducao_oc,
                              traducao_eu=traducao_eu,
                              categoria_traducao_eu=categoria_traducao_eu,
                              traducao_gl=traducao_gl,
                              categoria_traducao_gl=categoria_traducao_gl,
                              traducao_nl=traducao_nl,
                              categoria_traducao_nl=categoria_traducao_nl,
                              traducao_ar=traducao_ar,
                              categoria_traducao_ar=categoria_traducao_ar,
                              traducao_pt_br=traducao_pt_br,
                              categoria_traducao_pt_br=categoria_traducao_pt_br,
                              traducao_pt_pt=traducao_pt_pt,
                              categoria_traducao_pt_pt=categoria_traducao_pt_pt,
                              sinonimos_list=sinonimos_list,
                              antonimos_list=antonimos_list,
                              codigo_cas=codigo_cas,
                              codigo_sbl=codigo_sbl,
                              codigo_icd=codigo_icd,
                              codigo_outro=codigo_outro,
                              exemplo=exemplo,
                              enciclopedia=enciclopedia,
                              sigla=sigla,
                              notas=notas)
    
    # Create new entry with all fields
    new_entry = {
        "categoria": categoria,
        "descricao": descricao
    }
    
    if campo:
        new_entry["campo"] = campo
    
    if cluster:
        new_entry["cluster"] = cluster
    
    # Build traducoes object from individual fields
    traducoes = {}
    
    if traducao_en:
        traducoes["en"] = process_translation(traducao_en, categoria_traducao_en)
    if traducao_es:
        traducoes["es"] = process_translation(traducao_es, categoria_traducao_es)
    if traducao_fr:
        traducoes["fr"] = process_translation(traducao_fr, categoria_traducao_fr)
    if traducao_de:
        traducoes["de"] = process_translation(traducao_de, categoria_traducao_de)
    if traducao_oc:
        traducoes["oc"] = process_translation(traducao_oc, categoria_traducao_oc)
    if traducao_eu:
        traducoes["eu"] = process_translation(traducao_eu, categoria_traducao_eu)
    if traducao_gl:
        traducoes["gl"] = process_translation(traducao_gl, categoria_traducao_gl)
    if traducao_nl:
        traducoes["nl"] = process_translation(traducao_nl, categoria_traducao_nl)
    if traducao_ar:
        traducoes["ar"] = process_translation(traducao_ar, categoria_traducao_ar)
    if traducao_pt_br:
        traducoes["pt [BR]"] = process_translation(traducao_pt_br, categoria_traducao_pt_br)
    if traducao_pt_pt:
        traducoes["pt [PT]"] = process_translation(traducao_pt_pt, categoria_traducao_pt_pt)
    
    if traducoes:
        new_entry["traducoes"] = traducoes
    
    # Build remis object from individual fields
    remis = {}
    # SINONIMOS
    sinonimos_validos = [
        (t.strip(), c.strip()) for t, c in zip(sinonimos_texto, sinonimos_categoria) if t.strip()
    ]
    if sinonimos_validos:
        if len(sinonimos_validos) == 1:
            t, c = sinonimos_validos[0]
            remis["sin. compl."] = {
                "texto": t,
                "categoria": c
            }
        else:
            sin_dict = {}
            for idx, (t, c) in enumerate(sinonimos_validos, 1):
                sin_dict[str(idx)] = {
                    "texto": t,
                    "categoria": c
                }
            remis["sin. compl."] = sin_dict
    
    # ANTONIMOS
    antonimos_validos = [
        (t.strip(), c.strip()) for t, c in zip(antonimos_texto, antonimos_categoria) if t.strip()
    ]
    if antonimos_validos:
        if len(antonimos_validos) == 1:
            t, c = antonimos_validos[0]
            remis["ant"] = {
                "texto": t,
                "categoria": c
            }
        else:
            ant_dict = {}
            for idx, (t, c) in enumerate(antonimos_validos, 1):
                ant_dict[str(idx)] = {
                    "texto": t,
                    "categoria": c
                }
            remis["ant"] = ant_dict
    
    # SIGLAS
    siglas_validas = [
        (t.strip(), c.strip()) for t, c in zip(siglas_texto, siglas_categoria) if t.strip()
    ]
    if siglas_validas:
        if len(siglas_validas) == 1:
            t, c = siglas_validas[0]
            remis["sigla"] = {
                "texto": t,
                "categoria": c
            }
        else:
            sig_dict = {}
            for idx, (t, c) in enumerate(siglas_validas, 1):
                sig_dict[str(idx)] = {
                    "texto": t,
                    "categoria": c
                }
            remis["sigla"] = sig_dict
    
    if remis:
        new_entry["remis"] = remis
    
    codigos = {}
    if codigo_cas:
        codigos["CAS"] = codigo_cas
    if codigo_sbl:
        codigos["sbl"] = codigo_sbl
    if codigo_icd:
        codigos["ICD"] = codigo_icd
    if codigo_outro:
        codigos["outro"] = codigo_outro
    
    if codigos:
        new_entry["codigos"] = codigos
    
    if exemplo:
        new_entry["exemplo"] = exemplo
    if enciclopedia:
        new_entry["enciclopedia"] = enciclopedia
    if sigla:
        new_entry["sigla"] = sigla
    
    if notas:
        new_entry["Notas"] = notas
    
    # For edit mode, handle term rename
    if is_edit:
        if original_term != term:
            if original_term in data:
                data.pop(original_term)
    
    data[term] = new_entry
    
    with open('final_final.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    return redirect(url_for('entry_detail', term=term))

@app.route('/delete/<term>', methods=['POST'])
def delete_entry(term):
    data = load_data()
    if term in data:
        del data[term]
        with open('final_final.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return redirect(url_for('index'))
    return render_template('index.html', data=data, search_term='', error=f"Termo '{term}' não encontrado")

if __name__ == '__main__':
    app.run(debug=True)