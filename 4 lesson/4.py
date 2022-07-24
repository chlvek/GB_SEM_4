# В текстовом файле удалить все слова, которые содержат хотя бы одну цифру.
# В файле содержится:
# Мама сшила м0не штаны и7з бере9зовой кор45ы 893. -> Мама сшила штаны.




def find_words_with_digits(strochka: str) -> str:
    strochka = strochka.split()
    temp_str = ' '
    digits_str = "0,1,2,3,4,5,6,7,8,9"

    for word in strochka:
        for letter in word:
            if letter in digits_str and word not in temp_str:
                temp_str += word
            temp_str += " "

    return temp_str


def delete_words_with_digits(strochka, temp_str: str) -> list:
    strochka = strochka.split()
    temp_str = temp_str.split()
    for word_i in strochka:
        for word_j in temp_str:
            if word_j in strochka:
                strochka.remove(word_j)
    return strochka


if __name__ == '__main__':
    with open('4.txt', 'w', encoding='utf-8') as file:
        file.write("Мама сшила м0не штаны и7з бере9зовой кор45ы 893.")

    with open('4.txt', encoding='utf-8') as file:
        stroka = file.read()

    print('Initial string: ', stroka)
    temp_str = find_words_with_digits(stroka)
    print('Words with digits:', find_words_with_digits(stroka).split())
    result_list = delete_words_with_digits(stroka,temp_str)
    result_string = " ".join(result_list)
    print('String without words with digits:', result_string)

    with open('4.txt', 'w', encoding='utf-8') as file:
        file.write(result_string)