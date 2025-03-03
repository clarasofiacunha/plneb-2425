# TPC3 

## Descrição

Este código Python foi desenvolvido para processar um ficheiro de texto contendo conceitos médicos, limpar e formatar as informações, e gerar uma página HTML contendo uma lista desses conceitos com as respetivas descrições.


## Resolução

### 1. Leitura do Ficheiro

O primeiro passo foi abrir e ler o conteúdo de um ficheiro de texto com as informações a serem apresentadas no dicionário.

```python
file = open("dicionario_medico.txt", encoding="utf-8")
texto = file.read()
```

### 2. Limpeza

Após uma análise do texto, foram encontrados caracteres \f indesejados. Além disso, a designação de cada conceito normalmente é precedida por \n\n, o que facilita a sua diferenciação. No entanto, foi observado que, além das quebras de linha duplas (\n\n), algumas descrições contêm uma quebra de página (\f).

Assim, é necessário tratar o conteúdo das descrições para garantir a separação entre os diferentes tipos de informações. Para isso, foi utilizada a seguinte expressão regular:


```python
texto = re.sub(r'\f(?=[a-zà-öø-ÿ])|\n\f(?=[A-Z])', '', texto)
```

1. `\f(?=[a-zà-öø-ÿ])`: Se o caractere de quebra de página (\f) for seguido por uma letra minúscula, é removido. Isto permite remover quebras de página desnecessárias no meio de descrições ou entre conceitos.

2. `\n\f(?=[A-Z])`: Se houver uma quebra de linha (\n) seguida de uma quebra de página (\f) e logo depois uma letra maiúscula, a quebra de página é removida. Isto acontece quando há quebras de página entre o nome de um conceito e a respetiva descrição.


O próximo passo foi garantir que as descrições dos conceitos fossem formatadas corretamente, sem quebras de linha extras:

```python
def limpa_descricao(descricao):
    descricao = descricao.strip()
    descricao = re.sub(r"\n", " ", descricao)
    return descricao
```


### 3. Marcação dos Conceitos
Para identificar e organizar os conceitos dentro do texto, foi utilizada uma técnica de marcação, onde cada ocorrência de um conceito e sua descrição é associada ao símbolo `@`:

```python
texto = re.sub(r"\n\n", "\n\n@", texto)
```

Esta expressão insere o símbolo `@` após cada par de quebras de linha consecutivas, indicando a separação entre conceitos.


### 4. Extração de Conceitos

Com o texto devidamente formatado, foi possível utilizar expressões regulares para extrair os pares de conceito e descrição. A expressão regular utilizada para isso foi:

```python
conceitos_raw = re.findall(r"@(.*)\n([^@]*)", texto)
```

- `@(.*)`: Captura qualquer texto que venha após o símbolo @ (a designação do conceito), até ao final da linha.

- `\n([^@]*)`: Captura a descrição do conceito, que está na linha seguinte à designação, até encontrar o próximo símbolo @.


A partir disso, o código gera uma lista de tuplos, onde cada tupla contém a designação e a descrição do conceito:

```python
conceitos = [(designacao, limpa_descricao(descricao)) for designacao, descricao in conceitos_raw]
```

### 5. Gerar a página HTML

Após a extração e limpeza, o código cria uma página HTML simples que organiza os conceitos e as suas descrições de forma estruturada.
