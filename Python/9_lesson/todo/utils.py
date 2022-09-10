from string import ascii_letters
from random import randint
from typing import List

from .todo_item import ToDoItem


def gen_id(length: int):
    return ''.join(ascii_letters[randint(0, len(ascii_letters + ' ') - 2)] for _ in range(length))


def make_random_item():
    name = gen_id(7)
    desc = gen_id(15)
    item = ToDoItem(name, desc)
    if randint(0, 100) > 50:
        item.mark_complete()
    return item


def make_random_items(x: int) -> List[ToDoItem]:
    return [make_random_item() for _ in range(x)]


def get_item_complete_mark_emoji(item: ToDoItem):
    if item.is_complete:
        complete_mark = '✅'
    elif item.is_overdue:
        complete_mark = '🟥'
    else:
        complete_mark = '⬜️'
    return complete_mark