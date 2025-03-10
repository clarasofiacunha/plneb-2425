# TPC4: Criação de Página HTML

Este projeto teve como objetivo a criação de uma página HTML com um tema livre. Optei por desenvolver uma página dedicada às minhas viagens, onde compartilho minhas experiências em diversos destinos europeus.

A página está organizada em quatro seções principais:

- **Apresentação**: Breve introdução pessoal acompanhada de algumas fotos tiradas durante as minhas viagens.

- **Destinos visitados**: Lista interativa com links para as páginas sobre cada destino, além de um mapa interativo da Europa.

- **Destinos favoritos**: Destaque para os meus cinco destinos favoritos até agora.

- **Contacto**:  Espaço para que outros viajantes possam compartilhar as suas aventuras comigo.


## Estrutura

- `TPC4.html` - Página principal.

- `destination.html` - Página de detalhes para cada destino, onde faço uma introdução à cidade e depois falo brevemente da minha experiência seguida de algumas fotos que tirei.

- `style.css` - Personalização da página de modo a torná-la esteticamente mais agradável.


##
O `TPC4.html` é composto pelos seguintes elementos principais:

1. **Cabeçalho (\<header>)**: Contém a navegação da página, incluindo um botão para a página inicial e links para as seções "Destinations" e "Contact".

2. **Seção de Introdução (\<div class="welcome">)**: Esta seção contém uma breve apresentação pessoal e inclui um slider de imagens destacando alguns dos destinos visitados. 

3. **Seção de Destinos (\<section id="destinations">)**: Contém uma lista de destinos organizados numericamente, cada um com um link para a sua respetiva página. Além disso, tem um mapa interativo da Europa, onde os destinos são marcados numericamente.

4. **Seção de Destinos Favoritos (\<section id="top-destinations">)**: Lista os meus cinco destinos favoritos, permitindo acesso rápido a essas páginas.

5. **Seção de Contacto (\<section id="contact">)**: Inclui uma breve mensagem incentivando os visitantes a entrarem em contato para partilharem as suas viagens. Há um link para o meu perfil no Instagram, acompanhado por um ícone da rede social.


##
O `destination.html` é composto pelos seguintes elementos principais:

1. **Cabeçalho (\<header>)**: Igual ao do `TPC4.html`.

2. **Corpo (`<main>`)**: Esta seção mostra uma imagem principal do destino e inclui uma sobreposição com o nome do país, nome do destino e uma breve descrição. Mais abaixo, contém uma breve descrição da minha experiência pessoal no destino e apresenta uma galeria de imagens rolável com setas.

3. **Script Dinâmico**: Contém um objeto `destinos` que armazena informações de diferentes locais. O destino é definido dinamicamente e preenche os elementos HTML:
  - **Título da página**
  - **Nome do país e destino**
  - **Imagem principal**
  - **Descrição e detalhes**
  - **Galeria de imagens**

    Este modelo permite adicionar facilmente novos destinos apenas preenchendo o objeto `destinos`.