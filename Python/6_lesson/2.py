# 2- Найти сумму чисел списка стоящих на нечетной позиции

import random as ra

def input_list_length():
    while True:
        length_lst = input("Type the list length (it should be within 10 elements): ")
        if length_lst.isdigit():
            length_lst = int(length_lst)
            if length_lst <= 0 or length_lst > 10:
                continue
            else:
                return length_lst
        continue


if __name__ == "__main__":
    length_lst = input_list_length()
    lst = [ra.randint(0, 89) for i in range(length_lst)]
    print(lst)
    print(sum([x for i, x in enumerate(lst) if i % 2!=0]))

