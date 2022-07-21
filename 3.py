# 3- Задайте натуральное число N. Напишите программу, которая составит список простых множителей числа N.
# Пример: при N = 12 -> [2, 3]

def input_number():
    while True:
        number = input("Enter a number: ")
        if number.isdigit():
            number = int(number)
            if number > 1:
                return number
        else:
            continue


def simple_factors_list(number) -> list:
    lst = []
    divider = 2
    while number > 1: # 6
        if number % divider == 0: # t
            number //= divider
            if divider not in lst: # 6
                lst.append(divider) # 3
            else:
                continue
        else:
            divider += 1

    return lst


if __name__ == '__main__':
    number = input_number()
    print(simple_factors_list(number))