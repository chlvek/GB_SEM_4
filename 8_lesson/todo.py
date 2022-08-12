from datetime import date
from typing import Optional, List


class ToDoItem:
    def __init__(self, name: str, description: str, due_date: Optional[date] = None):
        self.complete = False
        self.name = name
        self.description = description
        self.due_date = due_date

    @property
    def due_date_str(self) -> Optional[str]:
        if self.due_date is None:
            return None
        return self.due_date.strftime('%d.%m.%Y')

    @property
    def is_complete(self):
        return self.complete

    @property
    def is_overdue(self):
        if not self.due_date:
            return False
        return self.due_date < date.today()

    def mark_complete(self):
        self.complete = True

    def mark_incomplete(self):
        self.complete = False

    def __str__(self) -> str:
        name = self.name
        description = f' - {self.description}' if self.description else ''
        completness = '[X]' if self.is_complete else '[ ]'
        due = 'no due date' if not self.due_date else self.due_date.strftime('%d.%m.%Y')
        overdue = ' (overdue)' if self.is_overdue and not self.complete else ''
        return f'{completness} {{{due}{overdue}}} {name}{description}'


class ToDoList:
    def __init__(self, *items: ToDoItem) -> None:
        self.items = {}
        for item in items:
            self.add_item(item)

    def add_item(self, item: ToDoItem) -> None:
        if not self.items:
            new_id = 0
        else:
            last_id = tuple(self.items.keys())[-1]
            new_id = last_id + 1
        self.items[new_id] = item

    def get(self, index: int):
        return self.items.get(index)

    def remove(self, index: int):
        if self.get(index):
            del self.items[index]
        else:
            print(f'no such index: {index}')

    def get_overdue(self) -> List[ToDoItem]:
        return list(filter(lambda x: x.is_overdue and not x.is_complete, self.items.values()))

    def get_incomplete(self) -> List[ToDoItem]:
        return list(filter(lambda x: not x.is_complete, self.items.values()))

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def __iter__(self):
        return iter(self.items.values())


def item_to_dict(item: ToDoItem):
    return {
        'name': item.name,
        'description': item.description,
        'due date': item.due_date_str,
        'complete': item.complete,
    }


def todo_to_dict(todo: ToDoList):
    return {str(item_id): item_to_dict(item) for item_id, item in todo.items.items()}
