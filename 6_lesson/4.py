# 4- Определить, позицию второго вхождения строки в списке либо сообщить, что её нет.

def find_string(string_1, string_2):
    count = 0
    for i, word in enumerate(string_1):
        if word == string_2:
            count += 1
        if count == 2:
            return i
    return -1            # если нет второго вхождения

if __name__ == "__main__":
    strings = input().split(" ")
    string_to_find = input()
    print(find_string(strings, string_to_find))