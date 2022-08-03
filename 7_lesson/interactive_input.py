import sys


MIN_INT = - sys.maxsize - 1
MAX_INT = sys.maxsize


def input_digit(prompt, start=MIN_INT, end=MIN_INT) -> int:
    while True:
        digit = input(prompt)
        if not digit.isdigit():
            print('Input must be a digit!')
            continue
        digit = int(digit)
        if digit < start:
            print(f'Input must be greater or equal to {start}')
            continue
        if digit > end:
            print(f'Input must be less or equal to {end}')
            continue
        return digit


def input_phone():
    while True:
        phone = input('Input phone (format: "XXX-XXXXXXX"): ')
        if '-' not in phone:
            print('Please enter a valid phone number')
            continue
        phone_parts = phone.split('-')
        if len(phone_parts) != 2:
            print('Please enter a valid phone number')
            continue
        p1, p2 = phone_parts
        if not all(c.isdigit() for c in p1) or not all(c.isdigit() for c in p2) or len(p1) != 3 or len(p2) != 7:
            print('Please enter a valid phone number')
            continue
        return f'+880 {phone}'


def yn_dialog(prompt: str) -> bool:
    sure = ('y', 'ye', 'yes', 'yeah')
    not_sure = ('n', 'no', 'nope')
    while True:
        yn = input(prompt)
        if yn.lower() in sure:
            return True
        if yn.lower() in not_sure:
            return False
        print('Type "y" or "n"')
        
        