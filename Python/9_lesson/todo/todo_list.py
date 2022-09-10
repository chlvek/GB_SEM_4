import logging
from typing import List

from .utils import gen_id
from .todo_item import ToDoItem


class ToDoList:
    def __init__(self, *items: ToDoItem) -> None:
        self.items = {}
        for item in items:
            self.add_item(item)

    def add_item(self, item: ToDoItem) -> str:
        new_id = self._make_id()
        item.id = new_id
        self.items[new_id] = item
        return new_id

    def get(self, item_id: str):
        return self.items.get(item_id)

    def remove(self, item_id: str):
        if self.get(item_id):
            del self.items[item_id]
        else:
            logging.error(f'no such item: {item_id}')

    def get_overdue(self) -> List[ToDoItem]:
        return list(filter(lambda x: x.is_overdue and not x.is_complete, self.items.values()))

    def get_incomplete(self) -> List[ToDoItem]:
        return list(filter(lambda x: not x.is_complete, self.items.values()))

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def _make_id(self) -> str:
        new_id = gen_id(7)
        while new_id in self.items.keys():
            new_id = gen_id(7)
        return new_id

    def __iter__(self):
        return iter(self.items.values())