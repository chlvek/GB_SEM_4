import os

from telegram import Update
from telegram.ext import CallbackContext


class _Missing:
    def __bool__(self):
        return False

    def __copy__(self):
        return self

    def __deepcopy__(self, _):
        return self

    def __repr__(self):
        return f'<MISSING>'


MISSING = _Missing()


class WithContext:

    update = None
    context = None
    bot = None 
    chat_id = None

    def set_context(self, update: Update, context: CallbackContext) -> 'Self':
        self.update = update
        self.context = context
        self.bot = context.bot
        self.chat_id = update.effective_chat.id
        return self

    def send_message(self, text: str, reply_markup=None):
        self.bot.send_message(chat_id=self.chat_id, text=text, reply_markup=reply_markup)

    def send_messages(self, *messages: str):
        for text in messages:
            self.send_message(text)


def get_token():
    token_path = os.path.join(os.path.dirname(__file__), 'token.txt')
    with open(token_path, 'r') as f:
        token = f.read()
    token = token.strip()
    return token
