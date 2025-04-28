import json

with open('popular/populares.json', 'r', encoding='utf-8') as f:
    populares_data = json.load(f)
    
with open('multilingue/multilingue.json', 'r', encoding='utf-8') as f:
    multilingue_data = json.load(f)
    
with open('neologismos/neologismos.json', 'r', encoding='utf-8') as f:
    neologismos_data = json.load(f)
    
final_data = multilingue_data.copy()

for key, value in populares_data.items():
    if key in final_data:
        if 'descricao' in final_data[key]:
            final_data[key]['descricao'] = [final_data[key]['descricao'], value['descricao']]
        else:
            final_data[key]['descricao'] = value['descricao']
    else:
        final_data[key] = value
        
for key, value in neologismos_data.items():
    if key in final_data:
        if 'descricao' in value:
            if 'descricao' in final_data[key]:
                final_data[key]['descricao'] = [final_data[key]['descricao'], value['descricao']]
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
                    final_data[key]['traducoes']['es'] = [final_data[key]['traducoes']['es'], traducoes['es']]
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
            if 'remis' not in final_data[key]:
                final_data[key]['remis'] = {}
            if 'sigla' in final_data[key]['remis']:
                final_data[key]['remis']['sigla'] = [final_data[key]['sigla'], value['sigla']]
            else:
                final_data[key]['remis'] = {'sigla' : value['sigla']}
        if 'enciclopedia' in value:
            final_data[key]['enciclopedia'] = value['enciclopedia']
        if 'exemplo' in value:
                final_data[key]['exemplo'] = value['exemplo']
    else:
        final_data[key] = value
        
with open('final.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=4)