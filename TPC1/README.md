# TPC1 - Manipulação de Strings

## Descrição

Este ficheiro contém a resolução do TPC1, que implementa diversas funções para manipulação de strings em Python. Além disso, o código inclui um menu interativo para testar as funcionalidades.


## Resolução

O código está organizado nas seguintes secções:

- Definição das funções principais (exercícios)
- Função tests() para testar as funcionalidades com valores pré definidos
- Função menu() que permite interagir com as opções de forma dinâmica

#### Ex. 1 - reverse(s)
Inverte a ordem dos caracteres da string (s) fornecida utilizando *slicing*.

Exemplo:
    
     reverse("hello")  
     # Saída: "olleh"
    
---

#### Ex. 2 - count_a(s)
Conta quantas vezes as letras "a" e "A" aparecem na string (s) através do método *count*. 

Exemplo:
    
     count_a("Andreia")  
     # Saída: 2

---

#### Ex. 3 - count_vowels(s)
Conta o número de vogais na string (s), considerando acentos, maiúsculas e minúsculas. É inicializado um contador, que é incrementado sempre que um caractere é uma vogal. Por fim, o contador é retornado.

Exemplo:
    
     count_vowels("biomédicA")  
     # Saída: 5

---

#### Ex. 4 - lower(s)
Converte todos os caracteres da string (s) para minúsculas através do método *lower*. 

**Exemplo**
    
     lower("BIOMEDICA")  
     # Saída: "biomedica"

---

#### Ex. 5 - upper(s)
Converte todos os caracteres da string (s) para maiúsculas através do método *upper*. 

**Exemplo**
    
     upper("biomedica")  
     # Saída: "BIOMEDICA"

---

#### Ex. 6 - capicua(s)
Verifica se uma string (s) é capicua (lê-se igual de trás para frente), considerando maiúsculas e minúsculas. Se a versão invertida da string for igual é string original, a função retorna True; coso contrário, retorna False.

**Exemplo**
    
     capicua("ana")  
     # Saída: True

     capicua("python")  
     # Saída: False

---

#### Ex. 7 - balance(s1, s2)
Verifica se todos os caracteres de 's1' estão presentes em 's2', considerando maiúsculas e minúsculas. A string s1 é percorrida e verifica-se se cada um dos seus caracteres está presente em s1. Se todos os caracteres de s1 estiverem presentes em s2 a função retorna True; caso contrário, retorna False.

**Exemplo**
    
     balance("clara", "carla")  
     # Saída: True

     balance("joana", "jarro")
     # Saída: False

---

#### Ex. 8 - ocorrencias(s1, s2)
Conta quantas vezes uma string 's1' aparece dentro de uma string 's2', através do método *count*, considerando maiúsculas e minúsculas. 

**Exemplo**

     ocorrencias("na", "banana")
     # Saída: 2

---

#### Ex. 9 - anagrama(s1, s2)
Verifica se 's1' e 's2' são anagramas (possuem as mesmas letras), considerando maiúsculas e minúsculas. Os caracteres de ambas as strings são ordenados através do método *sorted* e comparados. Se forem iguais, a função retorna True; caso contrário, retorna False.

**Exemplo**
    
     anagrama("listen", "silent")  
     # Saída: True

     anagrama("hello", "world")
     # Saída: False

---

#### Ex. 10 - anagram_classes(list) e table_anagrams(classes)
A função *anagram_classes(list)* agrupa palavras que são anagramas dentro de um dicionário. Ela recebe uma lista de palavras, percorre cada palavra e ordena as letras, tranformando-a numa chave para identificar anagramas.
Se essa chave ainda não existir no dicionário, cria uma nova chave e adiciona a palavra na lista.
Se a chave já existir, adiciona a palavra à lista correspondente.

A função *table_anagrams(classes)* recebe um dicionário de anagramas e imprime-os de forma organizada numa tabela.

**Exemplo**
    
     palavras = ["listen", "silent", "enlist", "amor", "roma", "ramo"]
     table_anagram(palavras)

     # Saída: {"eilnst": ["listen", "silent", "enlist"],
                   "amor": ["amor", "roma", "ramo"]}

---

     classes = {"eilnst": ["listen", "silent", "enlist"],
                   "amor": ["amor", "roma", "ramo"]}
     table_anagrams(classes)

     # Saída: 
     Letters             Classes
     -----------------------------------------------
     amor                amor, ramo, roma
     dlorw               world
     ehllo               hello
     eilnst              enlist, listen, silent


#### Extra - tests()
A função *tests()* executa uma série de testes, com exemplos pré-definidos, para as diferentes funções desenvolvidas.

#### Extra - menu()

O código inclui um **menu interativo** que permite ao utilizador escolher qual operação deseja executar. O menu apresenta as opções, recebe a entrada do utilizador e exibe os resultados de forma intuitiva. O menu tem ainda uma opção que permite ao utilizador visulalizar os testes pré-feitos da função *tests()*.