### Descrição
Neste trabalho, o objetivo foi expandir o script desenvolvido nas aulas de forma a recolher os detalhes sobre as doenças presente no site Atlas da Saúde.

### Resolução 
Para atingir o objetivo de recolher os detalhes das doenças, foram desenvolvidas várias funções. Cada uma delas tem uma responsabilidade específica no processo de scraping da página. Abaixo estão as descrições detalhadas de cada função:

- `extrair_data(div_conteudo)`: Extrai a data de publicação da doença.

- `extrair_conteudo(div_conteudo)`: Recolhe a descrição detalhada da doença, incluindo parágrafos, listas, subtítulos e links. O conteúdo extraído inclui:
   
   - **Parágrafos e texto corrido**: São extraídos e armazenados na lista associada à chave "Descrição".
   - **Subtítulos**: Caso existam, são identificados por `<h2>` e adicionados como novos títulos na estrutura de dados.
   - **Listas**: As listas de sintomas, tratamentos, etc., são extraídas de `<ul>` e armazenadas como listas dentro da estrutura.
   - **Links**: Caso haja links internos (como artigos ou seções relacionadas), são extraídos e armazenados sob o título correspondente.

- `extrair_fonte(div_conteudo)`: Obtém a fonte da informação (se existir).

- `extrair_site(div_conteudo)`: Extrai o site externo relacionado (caso exista).

- `extrair_nota(div_conteudo)`: Retira alguma nota adicional que esteja presente na página.

- `obter_info_doenca(url)`: Junta toda a informação de uma doença a partir da sua página específica. Esta faz uma requisição HTTP para obter o conteúdo da página, processa a resposta usando BeautifulSoup, e chama as funções de extração (extrair_data, extrair_conteudo, etc.) para juntar todos os dados relevantes. O resultado é retornado como um dicionário com a URL e todas as informações extraídas.

- `obter_doencas_por_letra(letra)`: Percorre a lista de doenças que começam por uma letra específica e recolhe os dados de cada uma.

- `obter_todas_as_doencas()`: Percorre todas as letras de A a Z e junta os dados de todas as doenças encontradas.