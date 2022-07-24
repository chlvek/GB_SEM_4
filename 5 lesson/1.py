# 1 - Напишите программу, удаляющую из текста все слова, содержащие ""абв"".
# 'абвгдейка - это передача' = >" - это передача"


def delete_words_with_substring(strochka: str) -> str:
    words = strochka.split()
    new_words = []
    for word in words:
        if word.find("абв") == -1:
            new_words.append(word)
    return " ".join(new_words)


if __name__ == '__main__':
    stroka = input("")
    print(delete_words_with_substring(stroka))

