# 3- Найти расстояние между двумя точками пространства(числа вводятся через пробел)

from math import sqrt

if __name__ == "__main__":
    x_a, x_b = map(float, input("Enter x coordinates: ").split())
    y_a, y_b = map(float, input("Enter y coordinates: ").split())
    distance = sqrt((x_b - x_a) ** 2 + (y_b - y_a) ** 2)
    print("Distance is: ", round(distance, 3))