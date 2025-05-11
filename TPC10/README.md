# TPC10
## Descrição
O presente trabalho tem como objetivo a extração de dados provenientes da [*Revista Portuguesa de Medicina Interna (PRMI)*](https://revista.spmi.pt/index.php/rpmi/issue/archive) e o respetivo armazenamento num ficheiro JSON estruturado.

## Implementação

**Funções**

1. `fetch_html(url)`: Realiza o download do conteúdo HTML de uma página e converte para um objeto BeautifulSoup.

2. `iterate_archive_pages(base_link, total_pages=6)`: Itera pelas página do ficheiro de edições (por padrão, as primeiras 6), monta as URLs de cada página e chama `extract_issues_from_archive` para processar cada uma.

3. `extract_issues_from_archive`: Extrai os links de cada edição.

4. `extract_issue_data`: Para cada edição extrai:

    - Título da edição
    - Data de publicação
    - Lista de artigos

    Armazena os dados num dicionário chamado `articles`.

5. `extract_article_data`: Extrai os dados de cada artigo:

    - Título do artigo
    - Lista de autores
    - DOI
    - Palavras-chave
    - Resumo
    - URL do artigo

---

**Saída**

O ficheiro JSON final contém toda a estrutura de dados recolhida. 

Estrutura:

```json
{
    "Título da Revista": {
        "URL": "link para a edição da revista",
        "data_publicacao": "data no formato YYYY-MM-DD",
        "artigos": [
            {
                "URL": "link do artigo",
                "titulo": "Título do Artigo",
                "autores": ["Nome do Autor 1", "Nome do Autor 2"],
                "doi": "https://doi.org/...",
                "keywords": ["palavra-chave 1", "palavra-chave 2"],
                "abstract": ["parágrafo 1 do resumo", "parágrafo 2", "..."]
            },
            {
                "titulo": "Outro Artigo",
                ...
            }
        ]
    },
    "Outra Edição da Revista": {
        ...
    }
}
```