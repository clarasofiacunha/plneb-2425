# TPC2 - Expressões Regulares

## Descrição

Este ficheiro contém a resolução do TPC2, que implementa diversas funções que utilizam expressões regulares em Python.


## Resolução

#### Ex. 1 
#### Alínea 1.1 - hello_start(lines)
Verifica se a palavra "hello" aparece no início da linha utilizando *re.match*. Se a correspondência for encontrada, a função imprime True; caso contrário, imprime False.

Exemplo:
    
     line1 = "hello world"
     line2 = "goodbye world"

     hello_start(line1)  
     # Saída: True

     hello_start(line2)
     # Saída: False
    
---

#### Alínea 1.2 - have_hello(lines)
Verifica se a palavra "hello" aparece em qualquer parte da linha utilizando *re.search*. Se a palavra "hello" for encontrada em qualquer lugar da linha, a função imprime True; caso contrário, imprime False.

Exemplo:

     line1 = "hello world"
     line2 = "goodbye world"

     have_hello(line1)
     # Saída: True

     have_hello(line1)
     # Saída: False
    
---

#### Alínea 1.3 - all_hello(line)
Encontra todas as ocorrências da palavra "hello", utilizando *re.findall*, ignorando maiúsculas e minúsculas através de *flags=re.IGNORECASE*.

Exemplo:
    
     line = "Hello there! Uh, hi, hello, it's me... Heyyy, hello? HELLO!"

     all_hello (line)  
     # Saída: ['Hello', 'hello', 'hello', 'HELLO']
    
---

#### Alínea 1.4 - sub(line)
Substitui todas as ocorrências da palavra "hello" por "YEP", através de *re.sub* e ignorando maiúsculas e minúsculas com *flags=re.IGNORECASE*.

Exemplo:
    
     line = "Hello there! Uh, hi, hello, it's me... Heyyy, hello? HELLO!"

     sub(line)  
     # Saída: *YEP* there! Uh, hi, *YEP*, it's me... Heyyy, *YEP*? *YEP*!
    
---

#### Alínea 1.5 - comma(line)
Divide a linha em partes usando a vírgula (,) como delimitador, através de *re.split*.

Exemplo:
    
     line = "bananas, laranjas, maçãs, uvas, melancias, cerejas, kiwis, etc."

     comma(line) 
     # Saída: ['bananas', ' laranjas', ' maçãs', ' uvas', ' melancias', ' cerejas', ' kiwis', ' etc.']
    
---

#### Ex. 2 - palavra_magica(frase)
A função usa *re.search* para procurar a expressão "por favor" no final da frase ($ indica o final da linha), seguida de um sinal de pontuação válido (ponto, ponto de interrogação ou ponto de exclamação) e ignorando maiúsculas/minúsculas (re.IGNORECASE). Se a correspondência for encontrada, a função retorna True, caso contrário, retorna False.

Exemplo:
    
     palavra_magica("Posso ir à casa de banho, por favor?")
     # Saída: True

     palavra_magica("Preciso de um favor.")
     # Saída: False

---

#### Ex. 3 - narcissismo(linha)
A função usa *re.findall* para procurar todas as ocorrências da palavra "eu" isolada (\b garante que se escontra a palavra inteira, e não parte de outra palavra). A função retorna o número de ocorrências encontradas usando len().

Exemplo:
    
     narcissismo("Eu não sei se eu quero continuar a ser eu. Por outro lado, eu ser eu é uma parte importante de quem EU sou.")
     # Saída: 6

---

#### Ex. 4 - troca_de_curso(linha, novo_curso)
A função usa *re.sub* para substituir a palavra "LEI" (novamente, o \b garante que "LEI" seja uma palavra isolada). O parâmetro novo_curso é usado para substituir "LEI" na linha.

**Exemplo**
    
     troca_de_curso("LEI é o melhor curso! Adoro LEI! Gostar de LEI devia ser uma lei.", "BIOM")
     # Saída: BIOM é o melhor curso! Adoro BIOM! Gostar de BIOM devia ser uma lei.

---

#### Ex. 5 - soma_string(linha)
A função usa *re.split* para dividir a string com base na vírgula.
Cada elemento dessa lista é convertido para inteiro com int(x) e somado usando sum().

**Exemplo**
    
     soma_string("4,-6,2,3,8,-3,0,2,-5,1")
     # Saída: 6

---

#### Ex. 6 - pronomes(frase)
Encontra todos os pronomes pessoais presentes na frase, considerando variações de maiúsculas/minúsculas, através da expressão regular *r"[et]u|el[ea]s?|[nv]ós"*. O *re.findall* retorna todas as ocorrências desses pronomes na frase, independentemente de maiúsculas ou minúsculas, devido ao re.IGNORECASE.

**Exemplo**
    
     pronomes("Eu vi o João, tu falaste com ele. Ela estava lá também, nós decidimos ajudar, e eles e elas ficaram contentes.") 
     # Saída: ['Eu', 'tu', 'ele', 'Ela', 'nós', 'eles', 'elas']

---

#### Ex. 7 - variavel_valida(string)
Verifica se uma string é um nome válido de variável, que começa com uma letra e pode conter letras, números ou underscores.
A expressão regular r"[A-Za-z]\w*$" garante que o nome da variável comece com uma letra ([A-Za-z]), só contenha letras, números ou underscores após o primeiro caractere (\w*). O *re.match* tenta casar essa expressão regular no início da string, retornando True ou False.

**Exemplo**
    
     variavel_valida("variavel1")
     # Saída: True

     variavel_valida("_variavel") 
     # Saída: False

---

#### Ex. 8 - inteiros(string)
Encontra todos os números inteiros na string, incluindo os negativos. -? permite capturar números negativos e \d+ captura um ou mais dígitos. O re.findall retorna todas as ocorrências de números inteiros na string.

**Exemplo**

     inteiros("12, -34, 56, -78")
     # Saída: ['12', '-34', '56', '-78']

---

#### Ex. 9 - underscores(string)
Substitui todos os espaços em branco (inclusive múltiplos espaços) por underscores atarvés do *re.sub*. A expressão regular r"\s+" captura um ou mais espaços em branco (\s corresponde a qualquer caractere de espaço).

**Exemplo**
    
     underscores("Eu  gosto  de  programar.")
     # Saída: Eu_gosto_de_programar.

---

#### Ex. 10 - codigos_postais(lista)
Divide códigos postais válidos em pares de partes, separando-os pelo hífen, utilizando *re.split*.

**Exemplo**
    
     lista = [
        "4700-000",
        "1234-567",
        "8541-543",
        "4123-974",
        "9481-025"
        ]
        
     # Saída: [('4700', '000'), ('1234', '567'), ('8541', '543'), ('4123', '974'), ('9481', '025')]
