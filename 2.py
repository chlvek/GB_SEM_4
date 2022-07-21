#2- Задайте последовательность чисел. Напишите программу, которая выведет список
# неповторяющихся элементов исходной последовательности. Посмотрели, что такое множество?
# Вот здесь его не используйте.

import random

lst = [random.randint(1, 50) for i in range(1, 11)]


def unique_el(initial_list:list) -> list:
    count = {}
    for i in initial_list:
        is_exist = count.get(i)
        if is_exist:
            count[i] += 1
        else:
            count[i] = 1

    return list(count.keys())


if __name__ == '__main__':
    print(lst)
    print(unique_el(lst))
