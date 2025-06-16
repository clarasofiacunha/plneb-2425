import json
from gensim.models import Word2Vec
from gensim.utils import tokenize
from gensim.models import KeyedVectors

trad_dict = {
    "CONCEPTES GENERALS": "conceitos gerais",
    "EPIDEMIOLOGIA": "epidemiologia",
    "ETIOPATOGÈNIA": "etiopatogenia",
    "DIAGNÒSTIC": "diagnóstico",
    "CLÍNICA": "clínica",
    "PREVENCIÓ": "prevenção",
    "TRACTAMENT": "tratamento",
    "PRINCIPIS ACTIUS": "princípios ativos",
    "ENTORN SOCIAL": "contexto social"
}

with open('final.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for key, value in data.items():
    if 'campo' in value:
        value['campo'] = trad_dict[value['campo']]

with open('final_translated.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# Campos possíveis e suas descrições
campos_descricoes = {
    "conceitos gerais": "conceitos gerais medicina básica fundamentos anatomia fisiologia patologia geral conhecimento médico essencial estrutura corpo humano",
    "epidemiologia": "epidemiologia prevalência incidência distribuição população estatística doença saúde pública mortalidade morbidade fatores risco estudo populacional",
    "etiopatogenia": "etiopatogenia causa origem fisiopatologia mecanismo patogênese desenvolvimento doença etiologia fatores causais processo patológico",
    "diagnóstico": "diagnóstico exame teste avaliação identificação detecção análise laboratorial imagem clínica differential diagnóstico diferencial",
    "clínica": "clínica sintomas sinais manifestação apresentação quadro clínico exame físico anamnese história clínica observação paciente",
    "prevenção": "prevenção profilaxia vacina imunização proteção medidas preventivas saúde pública controle infecção higiene cuidados preventivos",
    "tratamento": "tratamento terapia medicamento fármaco cura intervenção médica cirurgia procedimento reabilitação cuidados médicos terapêutico",
    "princípios ativos": "princípios ativos substância ativa componente farmacológico droga medicamento composto químico farmacologia molecular",
    "contexto social": "contexto social impacto sociedade ambiente comunitário saúde pública política saúde determinantes sociais qualidade vida"
}

corpus = []

for campo, desc in campos_descricoes.items():
    corpus.append(list(tokenize(campo, lower=True)))
    corpus.append(list(tokenize(desc, lower=True)))

for key, value in data.items():
    corpus.append(list(tokenize(key, lower=True)))
    if 'descricao' in value:
        descriptions = '. '.join(value['descricao'])
        corpus.append(list(tokenize(descriptions, lower=True)))

model = Word2Vec(corpus, vector_size=300, window=10, min_count=1, workers=4, sg=1, epochs=100)

def find_most_similar_field(key, value):
    best_field = None
    best_similarity = -1

    term_descriptions = '. '.join(value['descricao'])
    term_tokens = list(tokenize(key, lower=True)) + list(tokenize(term_descriptions, lower=True))
    term_vector = model.wv[term_tokens]

    for field, description in campos_descricoes.items():
        field_tokens = list(tokenize(field, lower=True)) + list(tokenize(description, lower=True))
        field_vector = model.wv[field_tokens]

        if term_vector.size > 0 and field_vector.size > 0:
            similarity = model.wv.n_similarity(term_tokens, field_tokens)
            if similarity > best_similarity:
                best_similarity = similarity
                best_field = field

    return best_field if best_field else "conceitos gerais"

for key, value in data.items():
    if 'campo' not in value or not value['campo']:
        predicted_field = find_most_similar_field(key, value)
        value['campo'] = predicted_field

with open('final_with_predicted_fields.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
