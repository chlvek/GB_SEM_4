# Условие задачи: На столе лежит 2021 конфета. Играют два игрока делая ход друг после друга.
# Первый ход определяется жеребьёвкой. За один ход можно забрать не более чем 28 конфет.
# Все конфеты оппонента достаются сделавшему последний ход.
# Сколько конфет нужно взять первому игроку, чтобы забрать все конфеты у своего конкурента?

import random


def input_second_player():
    while True:
        inp = input('Are you going to play with another player(1) or with bot(2)?: ')
        if not inp.isdigit():
            print("You must enter a digit, idiot!")
            continue
        bot_or_player = int(inp)
        if bot_or_player not in (1, 2):
            print("Enter a digit, 1 for human or 2 for bot")
            continue
        break
    return bot_or_player != 1


def input_number_of_candies(current_number_of_candies: int) -> int:
    while True:
        input_candies = input("Enter the number of candies: ")
        if not input_candies.isdigit():
            print("You must enter a digit, idiot!")
            continue
        input_candies = int(input_candies)
        if input_candies > 28 or input_candies <= 0 :
            print("Enter a digit within 1 and 28")
            continue
        if input_candies > current_number_of_candies:
            print("There are not enough candies for u to take..")
            continue
        break
    return input_candies


def player_turn(number_of_candies_left: int, is_bot: bool = False):
    if is_bot:
        return random.randint(1, 28 if number_of_candies_left >= 28 else number_of_candies_left)
    else:
        turn_candies = input_number_of_candies(number_of_candies_left)
        return turn_candies


if __name__ == "__main__":
    number_of_candies = 2021
    player1_candies = 0
    player2_candies = 0
    second_player_is_bot = input_second_player()

    player1_turn = random.randint(1,100) < 50

    while number_of_candies > 0:
        current_player = 1 if player1_turn else 2
        print(f'Player {current_player} turn! ({number_of_candies} candies left)')
        bot_flag = second_player_is_bot if not player1_turn else False
        candies = player_turn(number_of_candies, bot_flag)
        print(f'Player {current_player} took: {candies} candies')
        number_of_candies -= candies

        if player1_turn:
            player1_candies = candies + player2_candies
            player2_candies = 0
        else:
            player2_candies = candies + player1_candies
            player1_candies = 0

        print('=' * 100)
        print(f'Candies left: {number_of_candies}')
        print(f'Player 1 candies: {player1_candies}')
        print(f'Player 2 candies: {player2_candies}')
        print('=' * 100)

        player1_turn = not player1_turn

    print("GAME OVER!!!")

    winner = 1 if player1_candies > 0 else 2

    print(f"Player {winner} wins!")
