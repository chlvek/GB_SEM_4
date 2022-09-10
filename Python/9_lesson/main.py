import logging

import art

from todo import ToDoList
from todo.utils import make_random_items
from todo_app import ToDoApp
from utils import get_token


def main():
    logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.INFO)
    title = art.text2art('TODO APP', font='cybermedum')
    logging.info(f'Starting:\n{title}')

    token = get_token()
    todo = ToDoList(*make_random_items(1))
    app = ToDoApp(token, todo)
    app.run()


if __name__ == '__main__':
    main()
