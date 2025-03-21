from flask import Flask, request, render_template
import json
import re

app = Flask(__name__)

db_file = open("conceitos_.json", encoding="utf-8")
db = json.load(db_file)
db_file.close()


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/conceitos")
def conceitos():
    designacoes = list(db.keys())
    return render_template("conceitos.html", designacoes=designacoes, title="Lista de Conceitos")

@app.get("/conceitos/<designacao>")
def conceito(designacao):
    referrer = request.referrer or "/"  # Fallback para home ou onde você quiser
    if designacao in db:
        return render_template("designacao.html", designacao=designacao, descricao=db[designacao], referrer=referrer)
    else:
        return render_template("designacao.html", designacao="Erro", descricao="Descrição não encontrada", referrer=referrer)


@app.route("/api/conceitos/<designacao>")
def api_conceito(designacao):
    return {"designacao":designacao, "descricao":db[designacao]}

@app.post("/conceitos")
def adicionar_conceito():
    descricao = request.form.get("descricao")
    designacao = request.form.get("designacao")

    db[designacao] = descricao
    f_out = open("conceitos_.json", "w", encoding="utf-8")
    json.dump(db, f_out, indent=4, ensure_ascii=False)
    f_out.close()

    designacoes = sorted(list(db.keys()))
    return render_template("conceitos.html", designacoes=designacoes, title="Lista de Conceitos")


@app.post("/api/conceitos")
def adicionar_conceito_api():
    #json
    data = request.get_json()

    #{"designacao": "vida", "descicao": "a vida é..."}
    db[data["designacao"]] = data["descricao"]
    f_out = open("conceitos_.json", "w", encoding="utf-8")
    json.dump(db, f_out, indent=4, ensure_ascii=False)
    f_out.close()
    #form data
    return data


@app.route('/pesquisar', methods=['GET', 'POST'])
def pesquisar():
    termo = request.form.get("termo", "").strip()
    match = request.form.get("match")
    resultados = []

    if termo:
        if match:
            texto = re.compile(rf'\b{termo}\b', re.IGNORECASE)
        else:
            texto = re.compile(rf'{termo}', re.IGNORECASE)

        for designacao, descricao in db.items():
            if texto.search(designacao) or texto.search(descricao):
                designacao = texto.sub(lambda m: f"<b>{m.group(0)}</b>", designacao)
                descricao = texto.sub(lambda m: f"<b>{m.group(0)}</b>", descricao)
                resultados.append(f"{designacao}: {descricao}")

    return render_template("pesquisar.html", title="Pesquisar", resultados=resultados, termo=termo, match=match)

app.run(host="localhost", port=4002, debug=True)