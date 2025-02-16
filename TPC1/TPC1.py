#TPC1

#  Create a function that

#  1. given a string “s”, reverse it.
def reverse(s):
    return s[::-1]


#  2. given a string “s”, returns how many “a” and “A” characters are present in it.
def count_a(s):
    return s.count("a") + s.count("A")


# 3. given a string “s”, returns the number of vowels there are present in it.
def count_vowels(s):
    count=0
    for i in s.lower():
        if i in "aáàâãeéèêiíìîoóòôõuúùû":
            count += 1
    return count


# 4. given a string “s”, convert it into lowercase.
def lower(s):
    return s.lower()


# 5. given a string “s”,  convert it into uppercase.
def upper(s):
    return s.upper()


#  6. Verifica se uma string é capicua
def capicua(s):
    s = s.lower()
    return s == s[::-1]


# 7. Verifica se duas strings estão balanceadas 
# (Duas strings, s1 e s2, estão balanceadas se todos os caracteres de s1 estão presentes em s2.)
def balance(s1, s2):
    for i in s1.lower():
        if i not in s2.lower():
            return False
    return True


#  8. Calcula o número de ocorrências de s1 em s2
def ocorrencias(s1, s2):
    return s2.lower().count(s1.lower())


#9. Verifica se s1 é anagrama de s2. 
# ○ "listen" e "silent": Deve imprimir True
# ○ "hello", "world": Deve imprimir False
def anagrama(s1, s2):
    return sorted(s1.lower()) == sorted(s2.lower())


# 10. Dado um dicionário, calcular a tabela das classes de anagramas.
def anagram_classes(list):
    anagram = {}

    for i in list:
        word = "".join(sorted(i))
        if word not in anagram:
            anagram[word] = [i]
        else:
            anagram[word].append(i)

    return anagram

def table_anagrams(classes):
    print(f"{'Letters':<20}{'Classes'}")
    print("-" * 50)
    
    for k, v in sorted(classes.items()):
        anagrams = ", ".join(sorted(v))
        print(f"{k:<20}{anagrams}")


# ---------- Testes ---------
def tests():

    print(f'Ex.1 \n Reverse of hello: {reverse("hello")} \n')

    print(f'Ex.2 \n There are {count_a("biomedicaAaA")} "a" and "A" in "biomedicaAaA" \n')

    print(f'Ex. 3 \n Number of vowels in "biomédicA": {count_vowels("biomédicA")} \n')

    print(f'Ex. 4 \n Original text: BIOMEDICA \n Lowercase text: {lower("BIOMEDICA")} \n')

    print(f'Ex. 5 \n Original text: biomedica \n Uppercase text: {upper("biomedica")} \n')

    print(f'Ex. 6 \n Is palindrome? \n hello: {capicua("hello")}')
    print(f' ana: {capicua("ana")}')

    print(f'\n Ex. 7 \n Are balanced? \n "clara" and "carla": {balance("clara", "carla")}.')
    print(f' "joana" and "jarro": {balance("joana", "jarro")}.')

    print(f'\n Ex. 8 \n Letter "a" appears {ocorrencias("a", "biomedica")} time(s) in "biomedica".')
    print(f' Sequence "na" appears {ocorrencias("na", "banana")} time(s) in "banana". \n')


    print(f'Ex. 9 \n Are anagrams? \n "LiSten" e "silent": {anagrama("LiSten", "silent")}.')
    print(f' "hello" e "world": {anagrama("hello", "world")}. \n')


    list = ["listen", "silent", "enlist", "amor", "roma", "ramo", "hello", "world"]
    classes = anagram_classes(list)
    print('Ex. 10')
    table_anagrams(classes)


# ---------- Menu - ---------
def show_menu():
    print("\n#TPC1 Menu")
    options = [
        "Exit",
        "Reverse a string",
        "Count 'a' and 'A' in a string",
        "Count vowels in a string",
        "Convert to lowercase",
        "Convert to uppercase",
        "Check if it's a palindrome",
        "Check if two strings are balanced",
        "Count occurrences of a substring",
        "Check if two strings are anagrams",
        "Calculate anagram table",
        "Show pre-made tests",
    ]
    for i, option in enumerate(options, 1):
        print(f"{i-1}. {option}")


def menu():
    while True:
        show_menu()
        choice = input("Enter your choice (0 to exit): ")

        if choice == '1':
            s = input("Enter a string to reverse: ")
            print(f'Reversed string: {reverse(s)}')
        elif choice == '2':
            s = input("Enter a string to count 'a' and 'A': ")
            print(f'Count of "a" and "A": {count_a(s)}')
        elif choice == '3':
            s = input("Enter a string to count vowels: ")
            print(f'Vowel count: {count_vowels(s)}')
        elif choice == '4':
            s = input("Enter a string to convert to lowercase: ")
            print(f'Lowercase: {lower(s)}')
        elif choice == '5':
            s = input("Enter a string to convert to uppercase: ")
            print(f'Uppercase: {upper(s)}')
        elif choice == '6':
            s = input("Enter a string to check if it's a palindrome: ")
            print(f'Is palindrome: {capicua(s)}')
        elif choice == '7':
            s1 = input("Enter the first string to check balance: ")
            s2 = input("Enter the second string to check balance: ")
            print(f'Are balanced: {balance(s1, s2)}')
        elif choice == '8':
            s1 = input("Enter the substring to count: ")
            s2 = input("Enter the string to count occurrences in: ")
            print(f'Occurrences: {ocorrencias(s1, s2)}')
        elif choice == '9':
            s1 = input("Enter the first string to check anagram: ")
            s2 = input("Enter the second string to check anagram: ")
            print(f'Are anagrams: {anagrama(s1, s2)}')
        elif choice == '10':
            list = input("Type a list of words (comma-separated): ").split(',')
            list = [word.strip() for word in list]

            classes = anagram_classes(list)
            table_anagrams(classes)
        elif choice == '11':
            tests()
        elif choice == '0':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please try again.")

menu()