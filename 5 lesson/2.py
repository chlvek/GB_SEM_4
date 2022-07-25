# Условие задачи: На столе лежит 2021 конфета. Играют два игрока делая ход друг после друга.
# Первый ход определяется жеребьёвкой. За один ход можно забрать не более чем 28 конфет.
# Все конфеты оппонента достаются сделавшему последний ход.
# Сколько конфет нужно взять первому игроку, чтобы забрать все конфеты у своего конкурента?

import random

def input_number_of_candies(current_number_of_candies: int) -> int:
    while True:
        number_of_candies = input("Your turn! Enter the number of candies: ")
        if not number_of_candies.isdigit():
            print("You must enter a digit, idiot!")
            continue
        number_of_candies = int(number_of_candies)
        if number_of_candies > 28 or number_of_candies <= 0 :
            print("Enter a digit within 1 and 28")
            continue
        if number_of_candies > current_number_of_candies:
            print("There are not enough candies for u to take..")
            continue
        break
    return number_of_candies


def player_turn(number_of_candies: int, is_bot: bool = False):
    if is_bot:
        pass
    else:
        turn_candies = input_number_of_candies(number_of_candies)
        return turn_candies


if __name__ == "__main__":
    number_of_candies = 2021
    player1_candies = 0
    player2_candies = 0

    player1_turn = random.randint(1,100) < 50

    while number_of_candies > 0:
        if player1_turn:
            candies = player_turn(number_of_candies)
            player1_candies = candies + player2_candies
            player2_candies = 0
        else:
            candies = player_turn(number_of_candies)
            player2_candies = candies + player1_candies
            player1_candies = 0


    print("game is over")

    winner = "player1" if player1_candies > 0 else "player2"

    print(f"{winner} wins!")