# TPC9

## Descrição
O presente trabalho tem como objetivo treinar um modelo **Word2Vec** utilizando textos extraídos das obras 
*Harry Potter e a Pedra Filosofal* e *Harry Potter e a Câmara Secreta*. Através desta abordagem, pretende-se explorar as relações semânticas entre as palavras presentes nas obras, avaliando a capacidade do modelo em captar regularidades linguísticas e proximidades semânticas.

## Implementação

### Pré-processamento dos dados

Os textos são carregados linha a linha, sendo cada uma tokenizada com a função `gensim.utils.tokenize`. Durante o processo, as palavras são convertidas para minúsculas e a pontuação é removida, garantindo um vocabulário limpo para o treino do modelo.

```python
sentences = []

with open("Harry_Potter_e_A_Pedra_Filosofal.txt", encoding = "utf-8") as f:
    for line in f:
        tokens = list(gensim.utils.tokenize(line, lower=True))
        sentences.append(tokens)
```

### Treino do modelo Word2Vec

O modelo foi treinado com os seguintes hiperparâmetros:  

  - `vector_size=300` - Dimensão dos vetores de palavras.

  - `window=5` - Tamanho da janela de contexto.

  - `min_count=1`- Considera todas as palavras, mesmo as que aparecem apenas uma vez. 

  - `epochs=20` - Número de épocas de treino.

  - `workers=3` - Número de núcleos de CPU utilizados. 


### Exploração dos Resultados

- **Vetores de Palavras**

    É possível extrair diretamente os vetores associados a palavras específicas, por exemplo:

    ```python
    model.wv['harry']
    ```

- **Similaridade**

    A função `most_similar` permite identificar palavras semanticamente próximas:

    ```python
    model_wv.wv.most_similar('harry')
    ```

    Também é possível calcular o grau de similaridade entre pares de palavras com a função `similarity`:

    ```python
    model.wv.similarity("bruxaria", "magia")
    ```
    
- **Intruso**

    Com `doesnt_match`, o modelo identifica a palavra que não pertence a um determinado grupo:

    ```python
    model_wv.wv.doesnt_match(["varinha", "capa", "harry"])
    ```


### Análise e Visualização

O modelo treinado foi exportado para um ficheiro de texto, permitindo sua reutilização sem necessidade de novo treino:

```python
model.wv.save_word2vec_format('model_harry.txt', binary = False)
```

- **PCA**

Utilizou-se o **PCA** para representar visualmente os vetores, possibilitando a visualização bidimensional da relação semântica entre palavras. 


- **TensorFlow Embedding Projector**

Foi ainda realizada uma visualização interativa em 3D através da plataforma **TensorFlow Embedding Projector**. Para isso, o modelo foi convertido utilizando, no terminal, o script abaixo:

```python
python -m gensim.scripts.word2vec2tensor -i models/model_harry.txt -o model_harry
```
Os ficheiros `model_harry_tensor.tsv` e `model_harry_metadata.tsv` foram carregados na plataforma, permitindo uma exploração mais imersiva dos embeddings aprendidos.