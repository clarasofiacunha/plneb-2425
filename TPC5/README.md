# TPC5  

## Descrição

Este trabalho foi desenvolvido com base na atividade realizada em aula, tendo como objetivo aprimorar a funcionalidade de visualização da descrição de cada conceito médico, permitindo o acesso à respetiva página da descrição.

## Resolução

Foi criada a rota `/conceitos/<designacao>` para permitir a visualização da descrição de um conceito específico a partir da sua designação. Esta rota utiliza a função `api_designacao(designacao)`, que recebe o parâmetro `designacao` para recuperar a descrição correspondente ao conceito na base de dados. As variáveis `designacao` e `descricao` são então passadas para um novo template HTML (`designacao.html`). Este template foi desenvolvido para exibir a designação e a descrição do conceito correspondente.

Para facilitar o acesso direto às descrições dos conceitos clicando nestes, foi inserido um elemento `<a>` no template da lista de conceitos, que associa a designação de cada conceito ao url da sua descrição.