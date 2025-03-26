# TPC7

## Descrição
O presente trabalho consiste na implementação de uma tabela no script que tem vindo a ser desenvolvido ao longo das aulas. A tabela deve ser composta pelo par `designação: descrição` de cada conceito do dicionário médico. Além disso, é necessário ativar a funcionalidade de pesquisa utilizando expressões regulares.

## Resolução
**1. Criação da tabela** 

No template `tabela.html`, a tabela é gerada através de um ciclo *for*. Para cada conceito no dicionário médico (`db.items()`), o script cria uma linha (`<tr>`) com duas células (`<td>`): a primeira célula contém a designação e a segunda contém a descrição.

Ao clicar na designação ou na descrição, o utilizador é redirecionado para a página do conceito correspondente:

```html
<a href="/conceitos/{{ designacao }}" class="text-decoration-none text-reset">
```

<br>

**2. Rota para a tabela** 

Foi definida a rota `@app.get("/conceitos/tabela")` para renderizar o template `tabela.html`, passando o dicionário (db) como argumento para ser utilizado na criação da tabela:

```python
@app.get("/conceitos/tabela")
def conceitos_tabela():
    return render_template("tabela.html", db=db)
```

<br>


**3. Pesquisa com regex**

No ficheiro `conceitos.js` foi ativada a funcionalidade de pesquisa por meio de expressões regulares:

```javascript
$(document).ready(function() {
    $('#tabela_conceitos').DataTable({
        search: {
            regex: true
        }
    });
});
```


<br>


**4. Adição ao menu de navegação** 

Para facilitar o acesso à tabela, foi adicionado um link no menu de navegação:

```html
    <a class="nav-link" href="/conceitos/tabela">Tabela</a>
```

<br>

**5. Estilo da tabela**

A tabela foi estilizada com o uso de classes do Bootstrap. A classe `class="table"` aplica um estilo padrão, enquanto a classe `class="table-dark"` é usada para aplicar um fundo escuro ao cabeçalho da tabela.
Além disso, para garantir que os links não tenham o sublinhado tradicional e que a cor do texto siga a cor padrão do design da página, foi aplicada a classe text-decoration-none text-reset nos links: `class="text-decoration-none text-reset"`. 