import re

file = open("dicionario_medico.txt", encoding="utf-8")
texto = file.read()

#limpeza
texto = re.sub(r'\f(?=[a-zÀ-ÖØ-öø-ÿ])|\n\f(?=[A-ZÀ-ÖØ-Ý])', '', texto)


def limpa_descricao(descricao):
    descricao = descricao.strip()
    descricao = re.sub(r"\n", " ", descricao)
    return descricao


#marcar
texto = re.sub(r"\n\n", "\n\n@", texto)


#extrair conceitos
conceitos_raw = re.findall(r"@(.*)\n([^@]*)", texto)

conceitos = [(designacao, limpa_descricao(descricao)) for designacao, descricao in conceitos_raw]


#gerar HTML
def gera_html(conceitos):
    html_header = """
        <!DOCTYPE html>
            <head>
            </head>
            <body>
            <h3>Dicionário de Conceitos Médicos</h3>
            <p>Este dicionário foi desenvolvido para a aula de PLNEB 2024/2025</p>"""
    html_conceitos = ""
    for designacao, descricao in conceitos:
        html_conceitos += f"""
                    <div>
                    <p><b>{designacao}</b></p>
                    <p>{descricao}</p>
                    </div>
                    <hr/>
                """
    html_footer = """
                </body>
            </html>"""
    
    return html_header + html_conceitos + html_footer

html = gera_html(conceitos)
f_out = open("output.html", "w")
f_out.write(html)

f_out.close()
file.close() # temos sempre de fechar
