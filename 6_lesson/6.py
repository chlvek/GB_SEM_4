# 6-Сформировать список из  N членов последовательности. Для N = 5: 1, -3, 9, -27, 81 и т.д.

def input_list_length():
    while True:
        length_lst = input("Type the list length (it should be within 100 elements): ")
        if length_lst.isdigit():
            length_lst = int(length_lst)
            if length_lst <= 0 or length_lst > 100:
                continue
            else:
                return length_lst
        continue


if __name__ == "__main__":
    N = input_list_length()
    lst = [(-3)**i for i in range(N)]
    print(lst)