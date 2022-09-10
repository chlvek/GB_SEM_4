# 5- Найти произведение пар чисел в списке. Парой считаем первый и последний элемент, второй и предпоследний и т.д.

import random


def input_list_length():
    while True:    # only digits within 1-10 will be suitable and program will proceed
        length_lst = input("Type the list length (it should be within 10 elements): ")
        if length_lst.isdigit():
            length_lst = int(length_lst)
            if length_lst <= 0 or length_lst > 10:
                continue
            else:
                return length_lst
        continue


def multiply_to_middle(lst):
    middle_index = int(len(lst) / 2)
    result = [lst[i] * lst[len(lst) - i - 1] for i in range(middle_index)]

    if len(lst) % 2 != 0:
      result.append(lst[middle_index])

    return result


if __name__ == "__main__":
    length_lst = input_list_length()
    lst = [random.randint(1, 30) for i in range(length_lst)]
    print(lst)
    result = multiply_to_middle(lst)
    print('result: ', result)
