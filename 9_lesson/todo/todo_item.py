from datetime import date
from typing import Optional


class ToDoItem:
    def __init__(self, name: str, description: str, due_date: Optional[date] = None):
        self.id = None
        self.complete = False
        self.name = name
        self.description = description
        self.due_date = due_date

    @property
    def due_date_str(self) -> Optional[str]:
        if self.due_date is None:
            return 'no due date'
        due = self.due_date.strftime('%d.%m.%Y')
        overdue = ' (overdue)' if self.is_overdue and not self.complete else ''
        return f'{due}{overdue}'

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
        due = self.due_date_str
        return f'{completness} {{{due}}} {name}{description}'
