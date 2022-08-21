import logging
from typing import Tuple

from telegram import InlineKeyboardMarkup 
from telegram import InlineKeyboardButton 
from telegram import Update 
from telegram import ReplyKeyboardMarkup 
from telegram import ReplyKeyboardRemove
from telegram import KeyboardButton
from telegram.ext import ConversationHandler
from telegram.ext import CommandHandler 
from telegram.ext import CallbackQueryHandler
from telegram.ext import MessageHandler 
from telegram.ext import CallbackContext 
from telegram.ext import Filters

from todo import ToDoItem, ToDoList
from todo.utils import get_item_complete_mark_emoji
from utils import WithContext
from validators import DateValidator, YnValidator


class EmptyHandlerCallback:
    def __call__(self, update: Update, context: CallbackContext) -> None:
        return None


EMPTY_HANDLER = MessageHandler(Filters.all, EmptyHandlerCallback())


class ToDoHandler(WithContext):
    def __init__(self, todo: ToDoList) -> None:
        self.todo = todo

    def __call__(self, update: Update, context: CallbackContext) -> None:
        self.set_context(update, context)
        return self.handle()

    def handle(self):
        raise NotImplementedError()


class query:
    def __init__(self, item: ToDoItem = None): 
        self.item = item

    def edit(self):
        return f'edit-{self.item.id}'

    def edit_name(self):
        return f'edit_name-{self.item.id}'

    def edit_description(self):
        return f'edit_description-{self.item.id}'
    
    def edit_due(self):
        return f'edit_due-{self.item.id}'

    def switch(self):
        return f'switch-{self.item.id}'

    def remove(self):
        return f'remove-{self.item.id}'

    def show_todo(self):
        return f'show_todo-'

    def add(self):
        return f'add-'


class Help(ToDoHandler):

    helps = {}

    def __init__(self, todo: ToDoList) -> None:
        super().__init__(todo)
        self.help = {}
    
    @classmethod
    def add_command_help(cls, command: str, help_message: str) -> None:
        cls.helps[f'/{command}'] = help_message
    
    def handle(self):
        txt = ''
        for cmd, hlp in self.helps.items():
            txt += f'{cmd}: {hlp}\n'
        self.send_message(txt)


class Start(ToDoHandler):
    '''A start command handler.'''

    def handle(self):
        self.send_message(f'Привет в TODO App!\n\nОтправь (или нажми) /help чтобы увидеть доступные команды.')


class Show(ToDoHandler):
    '''A show command handler.'''

    def handle(self):
        self.run()

    def run(self):
        self.send_message(*self.get_message_data())

    def get_message_data(self) -> Tuple[str, InlineKeyboardMarkup]:
        return '📋 TODO: 📋', self.todo_inline_markup()

    def todo_inline_markup(self):
        keyboard = []

        for item in self.todo:
            item_markup = self.item_to_inline_markup(item)
            keyboard.append(item_markup)
        
        keyboard.append([InlineKeyboardButton('+➕+', callback_data=query().add())])
        markup = InlineKeyboardMarkup(keyboard)
        return markup

    def item_to_inline_markup(self, item: ToDoItem):
        complete_mark = get_item_complete_mark_emoji(item)
        text = f'{complete_mark} {item.name}'
        return [
            InlineKeyboardButton(text, callback_data=query(item).edit()),
        ]


class Edit(ToDoHandler):
    '''An edit callback query handler.'''

    def handle(self):
        return 'set_name'

    def run(self, item_id: str) -> None:
        item = self.todo.get(item_id)
        text, markup = self.get_item_editor(item)
        self.send_message(text, reply_markup=markup)
        return 'set_name'

    @staticmethod
    def get_item_editor(item: ToDoItem) -> Tuple[str, InlineKeyboardMarkup]:
        mark = get_item_complete_mark_emoji(item)
        mark_text = 'Выполнить' if not item.is_complete else 'Снять галочку'
        text = f'{item.name} ({item.due_date_str})\n\n{item.description}'
        markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton('🖊 Имя', callback_data=query(item).edit_name()), 
                InlineKeyboardButton('🖊 Описание', callback_data=query(item).edit_description()),
            ],
            [
                InlineKeyboardButton('🖊 Дата', callback_data=query(item).edit_due()), 
                InlineKeyboardButton('⬅️ Вернуться к списку', callback_data=query().show_todo()),
            ],
            [
                InlineKeyboardButton(f'{mark} {mark_text}', callback_data=query(item).switch()), 
                InlineKeyboardButton('❌ Удалить', callback_data=query(item).remove()),
            ],
        ])
        return text, markup


class QueryHandler(ToDoHandler):
    '''A callback query handler.'''

    _context_item_id = None
    _wait = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._actions = {
            'edit': (self.edit, None),
            'edit_name': (self.edit_name, self.set_name),
            'edit_description': (self.edit_description, self.set_description),
            'edit_due': (self.edit_due, self.set_due),
            'switch': (self.switch, None),
            'remove': (self.remove, self.do_remove),
            'show_todo': (self.show_todo, None),
            'add': (self.add, None),
        }

    def handle(self):
        query = self.update.callback_query.data
        self.update.callback_query.answer()
        action_id, item_id = query.split('-')
        logging.info(f'Got query: "{query}". Action id: {action_id}, Item id: {item_id}')
        action = self._actions.get(action_id)
        if not action:
            logging.error(f'Got unknown action id: "{action_id}"')
            return
        self._context_item_id = item_id
        prompt, self._wait = action
        prompt(item_id)

    def handle_text(self):
        if self._wait:
            if self._wait():
                self.drop_context()
        else:
            logging.info('handle text with no _wait')

    def edit(self, item_id: str):
        if not self.check_id(item_id):
            return
        Edit(self.todo).set_context(self.update, self.context).run(item_id)

    def edit_name(self, item_id: str):
        if not self.check_id(item_id):
            return
        self.send_message('Введи новое имя задачи (/cancel чтобы отменить ввод)')

    def set_name(self):
        new_name = self.update.message.text
        logging.info(f'Got new name for {self._context_item_id}: {new_name}')
        if not new_name:
            self.send_message('Имя задачи не должно быть пустым')
            return False
        item = self.todo.get(self._context_item_id)
        item.name = new_name
        self.send_message(f'Имя задачи успешно изменено на: "{new_name}"')
        self.edit(self._context_item_id)
        return True
    
    def edit_description(self, item_id: str):
        if not self.check_id(item_id):
            return
        self.send_message('Введи новое описание задачи (/cancel чтобы отменить ввод)')

    def set_description(self):
        new_description = self.update.message.text
        logging.info(f'Got new description for {self._context_item_id}: {new_description}')
        item = self.todo.get(self._context_item_id)
        item.description = new_description
        self.send_message(f'Описание задачи успешно изменено на: "{new_description}"')
        self.edit(self._context_item_id)
        return True
    
    def edit_due(self, item_id: str):
        if not self.check_id(item_id):
            return
        self.send_message('Введи новую дату в формате дд.мм.гггг (/cancel чтобы отменить ввод)')

    def set_due(self):
        new_due_date = self.update.message.text
        logging.info(f'Got new due date for {self._context_item_id}: {new_due_date}')
        validated = DateValidator('%d.%m.%Y')(new_due_date)
        if validated.is_ok:
            item = self.todo.get(self._context_item_id)
            item.due_date = validated.value
            self.send_message(f'Дедлайн задачи выставлен на {new_due_date}')
            self.edit(self._context_item_id)
            return True
        else:
            logging.error(f'Invalid due date: {new_due_date}')
            self.send_message(f'Ошибка: {validated.message}')
            return False
    
    def switch(self, item_id: str):
        if not self.check_id(item_id):
            return
        
        item = self.todo.get(item_id)
        item.complete = not item.complete
        text, keyboard = Edit.get_item_editor(item)
        self.update.callback_query.edit_message_text(
            text, reply_markup=keyboard,
        )
        return True
    
    def remove(self, item_id: str):
        if not self.check_id(item_id):
            return
        self.send_message(
            'Ты уверен что хочешь удалить задачу? (/cancel чтобы отменить ввод)', 
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton('Да'), KeyboardButton('Нет')]],
                one_time_keyboard=True,
            ),
        )

    def do_remove(self):
        input_text = self.update.message.text
        validated = YnValidator(('да',), ('нет',))(input_text)
        if validated.is_ok:
            if validated.value:
                self.todo.remove(self._context_item_id)
                message = 'Задача удалена'
            else:
                message = 'Удаление отменено'
            self.send_message(message, reply_markup=ReplyKeyboardRemove())
            self.show_todo(None)
            return True
        else:
            self.send_message(f'Ошибка: {validated.message}')
            return False
    
    def show_todo(self, item_id: str):
        Show(self.todo).set_context(self.update, self.context).run()
    
    def add(self, item_id: str):
        self.todo.add_item(ToDoItem('Новая задача', ''))
        text, keyboard = Show(self.todo).get_message_data()
        self.update.callback_query.edit_message_text(
            text, reply_markup=keyboard,
        )
        return True

    def drop_context(self):
        self._context_item_id = None
        self._wait = None

    def check_id(self, item_id: str) -> bool:
        item = self.todo.get(item_id)
        if not item:
            self.send_message('Неизвестная задача. Актуальные задачи можно помтотреть с помощью команды /show')
            return False
        return True

class TextHandler(ToDoHandler):

    def __init__(self, *args, query_handler, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.query_handler = query_handler
    
    def handle(self):
        self.query_handler.set_context(self.update, self.context)
        self.query_handler.handle_text()


class CancelInput(ToDoHandler):

    def __init__(self, *args, query_handler, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.query_handler = query_handler
    
    def handle(self):
        self.send_message('Ввод отменён. Вернуться у списку дел: /show')
        self.query_handler.drop_context()