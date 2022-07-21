# В текстовом файле удалить все слова, которые содержат хотя бы одну цифру.
# В файле содержится:
# Мама сшила м0не штаны и7з бере9зовой кор45ы 893. -> Мама сшила штаны.


file = open('4.txt', 'r', encoding='utf-8')
stroka = " "
for line in file.read():
    stroka = line
file.close()





def find_words_with_digits(strochka: str) -> str:
    strochka = strochka.split()
    temp_str = ' '
    digits_str = "0, 1, 2, 3, 4, 5, 6, 7, 8, 9"

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
    print('Initial string: ', stroka)
    temp_str = find_words_with_digits(stroka)
    print('Words with digits:', find_words_with_digits(stroka).split())
    result_string = delete_words_with_digits(stroka,temp_str)
    print('String without words with digits:', " ".join(result_string))


