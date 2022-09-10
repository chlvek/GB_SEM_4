# 1- Определить, присутствует ли в заданном списке строк, некоторое число
from functools import reduce


def input_digit():
    sign = 1
    while True:
        digit = input("Enter a desired number: ")
        if digit.startswith("-"):
            sign = -1
            digit = digit[1:]
        if not digit.isdigit():
            continue
        digit = sign*int(digit)
        return digit


if __name__ == "__main__":
    strings = input().split(" ")
    desires_number = str(input_digit())
    print(reduce(lambda x,y: x or y, [s == desires_number for s in strings], False))