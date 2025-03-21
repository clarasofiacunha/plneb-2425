# TPC6

## Descrição
Este trabalho foi desenvolvido com base na atividade realizada na aula, tendo como objetivo implementar a funcionalidade de pesquisa, criando uma nova página capaz de receber o input do utilizador e exibir todos os resultados (`conceito: designação`) que deem match, tanto na designação como na descrição. O match pode ser exato ou parcial (em meio de palavras), conforme a seleção do utilizador numa checkbox. Além disso, o termo inserido deve aparecer a negrito e os resultados devem ser clicávies, levando à página individual do conceito.

## Resolução
Foi implementada uma nova rota `/pesquisar`, para permitir a pesquisa de um termo no dicionário médico. A função associada, `pesquisar()`, verifica se a checkbox de "Correspondência Exata" está marcada. Se estiver ativada, apenas palavras completas são consideradas match, utilizando uma expressão regular que procura a palavra exata (`\b{termo}\b`). Caso contrário, o termo pode ser encontrado dentro de outras palavras (`{termo}`). A função percorre a base de dados, verificando a presença do termo na designação ou na descrição dos conceitos. Se houver correspondências, o comando `regex.sub()` é utilizado para substituir as ocorrências do termo por uma versão em negrito (`<b>termo</b>`) nos resultados.


Além disso, foi criada a página `pesquisar.html`, que possui:
- Um campo de input de texto e botão para pesquisa.

- Uma checkbox para ativar/desativar o modo de correspondência exata. Esta vem ativada por defeito.

- Uma caixa de resultados que correspondem ao texto introduzido, procurando tanto na designação como na descrição. Estes resultados são clicáveis, redirecionando para a página individual do conceito. Além disso, o termo inserido aparece sempre a negrito.
