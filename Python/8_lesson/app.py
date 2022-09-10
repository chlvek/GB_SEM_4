from cli import Cli, Command, CommandsNode, StopCli
from todo import ToDoList, ToDoItem, todo_to_dict
from typing import Optional
import json
from validators import DateValidator, JsonFilePathValidator
from interactive_input import ask, ask_once, confirm, choice
from validators import DateValidator
import os

__version__ = '0.1'


class ItemEditor:
    def __init__(self, item: ToDoItem, date_validator: DateValidator) -> None:
        self.item = item
        self.date_validator = date_validator
        self.to_delete = False
        self.cli = Cli(f'Editor: {item}', f'{item.name}> ', [
            Command('name', 'Change item name', self.change_name),
            Command('desc', 'Change item description', self.change_description),
            CommandsNode('due', 'Change item due date', [
                Command('set', 'Set new due date', self.change_due_date),
                Command('clear', 'Clear due date', self.clear_due_date),
            ]),
            Command('done', 'Mark item complete', self.mark_complete),
            Command('undone', 'Mark item incomplete', self.mark_incomplete),
            Command('show', 'Show item', self.show),
            Command('del', 'Delete item', self.delete),
            Command('back', 'Back to main menu', lambda: None, stops_cli=True),
        ], False)

    def run(self):
        self.cli.run()

    def show(self):
        print(self.item)

    def change_name(self):
        new_name = ask_once('New name', self.item.name)
        if new_name:
            self.item.name = new_name
            print(f'Updated name to: {new_name}')

    def change_description(self):
        new_description = ask_once('New description', self.item.description)
        if new_description:
            self.item.description = new_description
            print(f'Updated description to: {new_description}')

    def change_due_date(self):
        new_due_date = ask_once('New due date (dd.mm.yyyy)', self.item.due_date, self.date_validator)
        if new_due_date:
            self.item.due_date = new_due_date
            print(f'Updated due date to: {new_due_date}')

    def clear_due_date(self):
        self.item.due_date = None

    def mark_complete(self):
        self.item.mark_complete()
        print('Marked item complete.')

    def mark_incomplete(self):
        self.item.mark_incomplete()
        print('Marked item incomplete.')

    def delete(self):
        sure = confirm('Are you sure you want to delete item?', False)
        if sure:
            self.to_delete = True
            raise StopCli()



class ToDoCliApp:
    def __init__(self):
        self.cli = Cli(
            title='ToDo app', 
            prompt=f'todo {__version__}> ', 
            commands=[
                Command('add', 'Add new todo item', self.add_item),
                CommandsNode('show', 'Show todo items', [
                    Command('all', 'Show all todo items', self.show_todos),
                    Command('overdue', 'Show overdue todo items', self.show_overdue),
                    Command('incomplete', 'Show incomplete todo items', self.show_incomplete),
                ]),
                CommandsNode('data', 'Import/Export options', [
                    Command('import', 'Import todo items from json', self.import_data),
                    Command('export', 'Export todo items to json', self.export_data),
                ]),
                Command('edit', 'Edit item', self.edit),
            ],
        )
        self.todo_list = ToDoList()
        self.date_validator = DateValidator('%d.%m.%Y')

    def run(self):
        self.cli.run()

    def show_todos(self):
        if self.todo_list.is_empty():
            print('Nothing to show')
            return
        for item in self.todo_list:
            print(item)

    def show_overdue(self):
        to_show = self.todo_list.get_overdue()
        if not to_show:
            print('Nothing to show')
            return
        for item in to_show:
            print(item)

    def show_incomplete(self):
        to_show = self.todo_list.get_incomplete()
        if not to_show:
            print('Nothing to show')
            return
        for item in to_show:
            print(item)

    def add_item(self):
        name = ask('Name')
        description = ask('Description')
        due_date = ask('Due Date (dd.mm.yyyy)', None, self.date_validator)
        new_item = ToDoItem(name, description, due_date)
        self.todo_list.add_item(new_item)

    def import_data(self) -> None:
        try:
            self._import()
        except Exception as e:
            print(f'Import failed: {e}')

    def export_data(self):
        try:
            self._export()
        except Exception as e:
            print(f'Export failed: {e}')

    def edit(self):
        items_opts = [str(item) for item in self.todo_list]
        index = choice('Pick item id', items_opts)
        item = self.todo_list.get(index)
        editor = ItemEditor(item, self.date_validator)
        editor.run()
        if editor.to_delete:
            self.todo_list.remove(index)
            print('Deleted item')

    def _import(self):
        file_path = ask_once('Path to the data file', validator=JsonFilePathValidator())
        if not file_path:
            return
        with open(file_path, 'r') as f:
            data = json.load(f)
        for item_data in data.values():
            name = item_data['name']
            description = item_data['description']
            vr = self.date_validator(item_data['due date'])
            due_date = vr.value if vr.is_ok else None
            complete = item_data['complete']

            new_item = ToDoItem(name, description, due_date)
            new_item.complete = complete
            self.todo_list.add_item(new_item)
        print(f'Imported data from: {file_path}')

    def _export(self):
        file_path = ask('Path to the output file')
        if not file_path:
            return
        file_path = os.path.abspath(file_path)
        if not file_path.endswith('.json'):
            file_path += '.json'
        if os.path.exists(file_path):
            sure = confirm(f'Are you sure you want to overwrite existing {file_path}?', False)
            if not sure:
                print('Export stopped.')
                return
        data = todo_to_dict(self.todo_list)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f'Exported data to: {file_path}')