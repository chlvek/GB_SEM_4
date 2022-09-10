from telegram.ext import Updater

class BotApp:
    def __init__(self, token: str):
        self.token = token
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher

    def run(self):
        self.updater.start_polling()