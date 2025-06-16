import json

with open('popular/populares.json', 'r', encoding='utf-8') as f:
    populares_data = json.load(f)
    
with open('multilingue/multilingue.json', 'r', encoding='utf-8') as f:
    multilingue_data = json.load(f)
    
with open('neologismos/neologismos.json', 'r', encoding='utf-8') as f:
    neologismos_data = json.load(f)

with open('min_saude/min_saude.json', 'r', encoding='utf-8') as f:
    min_saude_data = json.load(f)

old_keys = []
new_tuples = []
for key, value in multilingue_data.items():
    traducao = None
    pt = None
    if 'pt [PT]' in value["traducoes"]:
        traducao = value["traducoes"]['pt [PT]']
        pt = 'pt [PT]'
    elif 'pt' in value["traducoes"]:
        traducao = value["traducoes"]['pt']
        pt = 'pt'
    elif 'pt [BR]' in value["traducoes"]:
        traducao = value["traducoes"]['pt [BR]']
        pt = 'pt [BR]'

    new_key = None
    new_category = None
    if traducao:
        if 'tradução' in traducao:
            new_key = traducao['tradução'] if traducao['tradução'] != '' else None
            new_category = traducao['categoria']
        elif '1' in traducao:
            new_key = traducao['1']['tradução'] if traducao['1']['tradução'] != '' else None
            new_category = traducao['1']['categoria']

    if new_key:
        new_value = value.copy()
        del new_value['traducoes'][pt]
        new_value['traducoes']['ca'] = {'tradução': key, 'categoria': value['categoria']}
        new_value['categoria'] = new_category
        new_value['descricao'] = [value['descricao']]

        new_tuples.append((new_key, new_value))
        old_keys.append(key)

    if not new_key:
        old_keys.append(key)

for key in old_keys:
    if key in multilingue_data:
        del multilingue_data[key]

for new_key, new_value in new_tuples:
    multilingue_data[new_key] = new_value
    
    multilingue_data[new_key]['enciclopedia'] = ''
    multilingue_data[new_key]['exemplo'] = ''

final_data = multilingue_data.copy()

for key, value in populares_data.items():
    if key in final_data:
        final_data[key]['categoria'] = ''
        final_data[key]['traducoes'] = {}
        final_data[key]['codigos'] = {}
        final_data[key]['Notas'] = ''
        final_data[key]['enciclopedia'] = ''
        final_data[key]['exemplo'] = ''
        final_data[key]['remis'] = {}
        
        if 'descricao' in final_data[key]:
            final_data[key]['descricao'] += value['descricao']
        else:
            final_data[key]['descricao'] = value['descricao']
    else:
        final_data[key] = {
            'descricao': value['descricao'],
            'remis': {},
            'categoria': '',
            'traducoes': {},
            'codigos': {},
            'Notas': '',
            'enciclopedia': '',
            'exemplo': ''
        }
        
for key, value in neologismos_data.items():
    if key in final_data:
        final_data[key]['categoria'] = ''
        final_data[key]['traducoes'] = {}
        final_data[key]['codigos'] = {}
        final_data[key]['Notas'] = ''
        final_data[key]['enciclopedia'] = ''
        final_data[key]['exemplo'] = ''
        final_data[key]['remis'] = {}
        
        if 'descricao' in value:
            if 'descricao' in final_data[key]:
                final_data[key]['descricao'] += value['descricao']
            else:
                final_data[key]['descricao'] = value['descricao']
        if 'traducoes' in value:
            if 'traducoes' in final_data[key]:
                traducoes = value['traducoes']
                if 'en' in final_data[key]['traducoes']:
                    final_data[key]['traducoes']['en'] = [final_data[key]['traducoes']['en'], traducoes['en']]
                else:
                    final_data[key]['traducoes']['en'] = traducoes['en']
                if 'es' in final_data[key]['traducoes']:
                    final_data[key]['traducoes']['es'][f"{len(final_data[key]['traducoes']['es']) + 1}"] = [final_data[key]['traducoes']['es'], traducoes['es']]
                else:
                    final_data[key]['traducoes']['es'] = traducoes['es']
            else:
                traducoes = value['traducoes']
                final_data[key]['traducoes'] = traducoes
        if 'categoria' in value:
            if 'categoria' in final_data[key]:
                final_data[key]['categoria'] = [final_data[key]['categoria'], value['categoria']]
            else:
                final_data[key]['categoria'] = value['categoria']
                
        if 'sigla' in value:               
            if 'sigla' in final_data[key]['remis']:  
                if len(final_data[key]['remis']['sigla']) > 1:
                    final_data[key]['remis']['sigla'][f"{len(final_data[key]['remis']['sigla']) + 1}"] = {'texto': value['sigla'], 'categoria': ''}
                else:
                    final_data[key]['remis']['sigla']['1'] = {'texto': final_data[key]['remis']['sigla']['texto'], 'categoria': final_data[key]['remis']['sigla']['categoria']}
                    final_data[key]['remis']['sigla']['2'] = {'texto': value['sigla'], 'categoria': ''}
                    del final_data[key]['remis']['sigla']['texto']
                    del final_data[key]['remis']['sigla']['categoria']  
            else:
                final_data[key]['remis']['sigla'] = {'texto': value['sigla'], 'categoria': ''}
        
        if 'enciclopedia' in value:
            final_data[key]['enciclopedia'] = value['enciclopedia']
        if 'exemplo' in value:
                final_data[key]['exemplo'] = value['exemplo']
    else:
        if 'sigla' in value:
            final_data[key] = {
                'descricao': value['descricao'],
                'remis': {'sigla': {'texto': value['sigla'], 'categoria': ''}},
                'categoria': value.get('categoria', ''),
                'traducoes': value.get('traducoes', {}),
                'codigos': {},
                'Notas': '',
                'enciclopedia': value.get('enciclopedia', ''),
                'exemplo': value.get('exemplo', '')
            }
        else:
            final_data[key] = {
                'descricao': value['descricao'],
                'remis': {},
                'categoria': value.get('categoria', ''),
                'traducoes': value.get('traducoes', {}),
                'codigos': {},
                'Notas': '',
                'enciclopedia': value.get('enciclopedia', ''),
                'exemplo': value.get('exemplo', '')
            }

for key, value in min_saude_data.items():
    if key in final_data:
        final_data[key]['categoria'] = ''
        final_data[key]['traducoes'] = {}
        final_data[key]['codigos'] = {}
        final_data[key]['Notas'] = ''
        final_data[key]['enciclopedia'] = ''
        final_data[key]['exemplo'] = ''
        
        if 'descricao' in final_data[key]:
            final_data[key]['descricao'] += value['descricao']
        else:
            final_data[key]['descricao'] = value['descricao']
        if 'sin.' in final_data[key]['remis']:
            if 'sin.' in  value['remis']:
                if len(final_data[key]['remis']['sin.']) > 1:
                    final_data[key]['remis']['sin.'][f"{len(final_data[key]['remis']['sin.']) + 1}"] = {'texto': value['remis']['sin.'], 'categoria': ''}
                else:
                    final_data[key]['remis']['sin.']['1'] = {'texto': final_data[key]['remis']['sin.']['texto'], 'categoria': final_data[key]['remis']['sin.']['categoria']}
                    final_data[key]['remis']['sin.']['2'] = {'texto': value['remis']['sin.'], 'categoria': ''}
                    del final_data[key]['remis']['sin.']['texto']
                    del final_data[key]['remis']['sin.']['categoria']
        else:
            if 'sin.' in  value['remis']:
                final_data[key]['remis'] = {'sin.': value['remis']['sin.']}
    else:
        if 'sin.' in value['remis']:
            final_data[key] = {'descricao': value['descricao'], 'remis': {'sin.': {'texto': value['remis']['sin.'], 'categoria': ''}},
                            'categoria': '', 'traducoes': {}, 'codigos': {}, 'Notas': '', 'enciclopedia': '', 'exemplo': ''}
        else:
            final_data[key] = {'descricao': value['descricao'], 'remis': {},
                            'categoria': '', 'traducoes': {}, 'codigos': {}, 'Notas': '', 'enciclopedia': '', 'exemplo': ''}

print(f"Total entries in final data: {len(final_data)}")

with open('final.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=4)