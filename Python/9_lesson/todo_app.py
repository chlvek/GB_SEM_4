from bot_app import BotApp

from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from todo import ToDoList
from handlers import ToDoHandler, Start, Show, Help, QueryHandler, TextHandler, CancelInput


class ToDoApp(BotApp):
    def __init__(self, token: str, todo: ToDoList) -> None:
        super().__init__(token)
        self.todo = todo
        self.help_handler = Help
        self.add_command('start', None, Start, help_exclude=True)
        self.add_command('show', 'Показать список дел', Show)
        self.add_command('help', 'Показать эту справку', self.help_handler)
        query_handler = QueryHandler(todo)
        self.add_command('cancel', None, CancelInput, help_exclude=True, query_handler=query_handler)
        self.dispatcher.add_handler(CallbackQueryHandler(query_handler))
        self.dispatcher.add_handler(MessageHandler(Filters.all, TextHandler(self.todo, query_handler=query_handler)))

    def add_command(self, command: str, description: str, handler: ToDoHandler, help_exclude: bool = False, **kwargs) -> None:
        if not help_exclude:
            self.help_handler.add_command_help(command, description)
        self.dispatcher.add_handler(CommandHandler(command, handler(self.todo, **kwargs)))
