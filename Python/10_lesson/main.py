import logging
import random
from enum import Enum, auto

from utils import get_token, WithContext
from bot_app import BotApp

from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters,
)


class BotState(Enum):
    picking_game = auto()
    starting_game = auto()
    playing = auto()
    unknown = auto()


BOT_STATE = BotState.unknown



class GameMenu(WithContext):

    def __init__(self, game):
        self.game = game
        self.callbacks = {
            '📚Правила': self.rules,
            '🎮Играть!': self.play,
            '◀️Назад': self.back,
        }
        self.buttons = [[KeyboardButton(name) for name in self.callbacks]]

    def get_callback(self, callback_id):
        return self.callbacks.get(callback_id, self.default)

    def rules(self):
        rules = self.game.rules
        self.send_message(rules)
        game_start(self.update, self.context)

    def play(self):
        if self.game.in_dev:
            self.send_message('Эта игра почти готова, и скоро в неё можно будет поиграть! А пока давай сыграем в что-нибудь другое?')
            game_start(self.update, self.context)  # tmp
        else:
            game_play(self.update, self.context)

    def back(self):
        game_pick(self.update, self.context)

    def default(self, update: Update, context: CallbackContext):
        self.send_message('Выбери пункт меню игру с помощью кнопок')
        game_start(update, context)


class Game(WithContext):

    in_dev = True
    name = None
    rules = None

    def __init__(self):
        self.menu = GameMenu(self)
        self.is_over = False
        self.player_turn = False
        self.player_win = False

    def send_status(self):
        status = self._get_status()
        turn_info = self._get_turn_info()
        self.send_messages(status, turn_info)

    def play_turn(self):
        if self.player_turn:
            self._play_player_turn()
            self._check_game_over()
            if self.is_over:
                return
            if not self.player_turn:
                self._play_bot_turn()
        else:
            self._play_bot_turn()

        self.send_status()
        self._check_game_over()

    def game_over(self):
        winner_text = f"{'Я' if not self.player_win else 'Ты'} выиграл!"
        self.send_messages('GAME OVER!!!', winner_text)

    def prepare(self):
        raise NotImplementedError()

    def _play_player_turn(self):
        raise NotImplementedError()

    def _play_bot_turn(self):
        raise NotImplementedError()

    def _check_game_over(self):
        raise NotImplementedError()

    def _get_status(self):
        raise NotImplementedError()

    def _get_turn_info(self):
        return 'Ты ходишь!' if self.player_turn else 'Я хожу!'


class CandiesGame(Game):

    in_dev = False
    name = 'Конфетки 🍬'
    rules = '\n'.join((
        'На столе лежит 100 конфет.',
        'Мы делаем ходы друг после друга.',
        'Первый ход определяется жеребьёвкой.',
        'За один ход можно забрать не более чем 28 конфет,',
        'при этом ходящий забирает все конфеты оппонента',
        'Тот, кто берет получил все конфеты - выиграл.',
    ))

    def __init__(self):
        super().__init__()
        self.number_of_candies = None
        self.player_candies = None
        self.bot_candies = None

    def prepare(self):
        self.is_over = False
        self.player_turn = random.randint(1,100) < 50

        self.number_of_candies = 100
        self.player_candies = 0
        self.bot_candies = 0

    def check_input(self, player_input):
        try:
            player_input = int(player_input)
            return 1 <= player_input <= min(28, self.number_of_candies)
        except Exception:
            return False

    def _play_player_turn(self):
        player_input = self.message

        if not self.check_input(player_input):
            self.send_message(f'Введи число от 1 до {min(28, self.number_of_candies)}!')
            return
        
        player_input = int(player_input)

        self.player_candies = self.bot_candies + player_input
        self.bot_candies = 0
        self.number_of_candies -= player_input
        self.player_turn = False

        self.send_message(f'Ты взял {player_input} конфет')

    def _play_bot_turn(self):
        k = random.randint(1, 28 if self.number_of_candies >= 28 else self.number_of_candies)

        self.bot_candies = self.player_candies + k
        self.player_candies = 0
        self.number_of_candies -= k
        self.player_turn = True

        self.send_message(f'Я взял {k} конфет')

    def _check_game_over(self):
        if self.number_of_candies == 0:
            self.is_over = True
            self.player_win = self.player_candies > 0

    def _get_status(self):
        return '\n'.join((
            f'Осталось конфет: {self.number_of_candies}',
            f'У меня конфет: {self.bot_candies}',
            f'У тебя конфет: {self.player_candies}',
        ))


class MacGame(Game):

    in_dev = True
    name = 'Быки и коровы 🐄🐂'
    rules = '\n'.join((
        'Я загадываю слово из определенного количества букв.',
        'Допустим, четырех. Твоя задача - угадать слово, называя',
        'слова из того же количества букв.',
        'Если буква из твоего слова есть в загаданном - это корова🐄.',
        'Если еще и позиция совпадает - это бык🐂.',
        'Пример:',
        'загаданное слово: чаты.',
        'Ты: тьма - 2 🐄🐄',
        'Ты: чума - 1 🐂, 1 🐄.',
    ))


class GamesManager:
    def __init__(self, *games: Game):
        self.games = {game.name: game for game in games}
        self.active_game = None

    def set_active(self, game_id: str):
        self.active_game = self.get(game_id)

    def get(self, game_id: str):
        return self.games.get(game_id)

    def __iter__(self):
        return iter(self.games.values())


GAMES = GamesManager(CandiesGame(), MacGame())


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='Привет! Я бот, который умеет играть в разные игры. Давай сыграем?',
    )
    game_pick(update, context)


def game_pick(update: Update, context: CallbackContext):
    global BOT_STATE
    buttons = [[KeyboardButton(game.name) for game in GAMES]]
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='Выбери игру',
        reply_markup=ReplyKeyboardMarkup(buttons),
    )
    BOT_STATE = BotState.picking_game


def game_pick_handle(update: Update, context: CallbackContext):
    global GAMES
    game_id = update.message.text
    game = GAMES.get(game_id)
    if not game:
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=f'Ой, я не знаю такой игры: {game_id}'
        )
        game_pick(update, context)
    GAMES.set_active(game_id)
    game_start(update, context)


def game_start(update: Update, context: CallbackContext):
    global BOT_STATE, GAMES
    buttons = GAMES.active_game.menu.buttons
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Начнём?",
        reply_markup=ReplyKeyboardMarkup(buttons),
    )
    BOT_STATE = BotState.starting_game


def game_start_handle(update: Update, context: CallbackContext):
    global GAMES, BOT_STATE
    callback = GAMES.active_game.menu.set_context(update, context).get_callback(update.message.text)
    callback()


def game_play(update: Update, context: CallbackContext):
    global GAMES, BOT_STATE
    BOT_STATE = BotState.playing
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Играем! (Отправь команду /start, чтобы вернуться в главное меню)',
        reply_markup=None,
    )
    game = GAMES.active_game
    game.set_context(update, context)
    game.prepare()
    game.play_turn()


def game_play_handle(update: Update, context: CallbackContext):
    game = GAMES.active_game
    game.set_context(update, context)
    game.play_turn()
    if game.is_over:
        game.game_over()
        game_pick(update, context)


STATE_TRANSITIONS = {
    BotState.picking_game: game_pick_handle,
    BotState.starting_game: game_start_handle,
    BotState.playing: game_play_handle,
}


def handle_message(update: Update, context: CallbackContext):
    try:
        handler = STATE_TRANSITIONS.get(BOT_STATE)
        handler(update, context)
    except Exception as e:
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=f'Что то сломалось... Попробуй заново запустить команду /start. Ошибка: {e}',
        )


def main():
    logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.INFO)
    token = get_token()
    app = BotApp(token)
    app.dispatcher.add_handler(CommandHandler('start', start))
    app.dispatcher.add_handler(MessageHandler(Filters.all, handle_message))
    app.run()


if __name__ == '__main__':
    main()