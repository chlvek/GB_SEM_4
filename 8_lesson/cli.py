from typing import Any, List, Optional, Tuple, Callable, Union


class StopCli(Exception):
    pass


class Command:
    def __init__(self, name: str, help: str, callback: Callable, stops_cli: bool = False) -> None:
        self.name = name
        self.help = help
        self.callback = callback
        self.stops_cli = stops_cli

    def get_help(self, indent=''):
        return f'{indent}{self.name} - {self.help}'

    def __call__(self):
        self.callback()


class CommandsNode:
    def __init__(self, name: str, help: str, commands: List[Command]) -> None:
        self.name = name
        self.help = help
        self.commands = {cmd.name: cmd for cmd in commands}

    def get(self, command: str, default: Any = None) -> Optional[Command]:
        return self.commands.get(command, default)

    def add_command(self, command: Command):
        self.commands[command.name] = command

    def get_help(self, indent='') -> str:
        hlp = ''
        for cmd in self.commands.values():
            new_line = f'{indent}{cmd.name} - {cmd.help}\n'
            hlp += new_line
            if isinstance(cmd, CommandsNode):
                hlp += cmd.get_help(indent + '  ')
        return hlp

    def __iter__(self):
        return iter(self.commands.values())


class Cli:
    def __init__(self, title: str, prompt: str, commands: list, add_exit: bool = True, add_help: bool = True) -> None:
        self.title = title
        self.prompt = prompt
        self.root = self.setup_root(commands, add_exit, add_help)

    def run(self) -> None:
        while True:
            try:
                words = self.input_command()
                cmd = self.get_command(words)
                if not cmd:
                    continue
                r = cmd()
                if cmd.stops_cli:
                    return r
            except StopCli:
                return
            except Exception as exc:
                print(f'Cli app {self.title} crushed with error: {exc}')

    def input_command(self) -> List[str]:
        '''Prompt a user to input a command.'''
        cmd = input(self.prompt)
        words = cmd.split(' ')
        return words

    def get_command(self, words: List[str]) -> Optional[Command]:
        current = self.root
        for word in words:
            current = current.get(word, {})
            if isinstance(current, Command):
                return current
        if not isinstance(current, Command):
            print('Invalid command! type "help" to see available commands.')
            return None
        return current

    def setup_root(self, commands: list, add_exit: bool = True, add_help: bool = True) -> dict:
        additional_commands = []
        if add_exit:
            additional_commands.append(Command('exit', 'Exit programm', self.exit))
            additional_commands.append(Command('quit', 'Exit programm', self.exit))
        if add_help:
            additional_commands.append(Command('help', 'Show help', self.print_help))
        root = {}
        for command in (*commands, *additional_commands):
            root[command.name] = command
        return root

    def exit(self):
        print('Bye!')
        exit(0)

    def print_help(self) -> None:
        hlp = f'{self.title}\n'
        indent = '  '
        for cmd in self.root.values():
            new_line = f'{indent}{cmd.name} - {cmd.help}'
            hlp += new_line
            if isinstance(cmd, CommandsNode):
                hlp += ' (Must be chained with): \n'
                hlp += cmd.get_help(indent + '  ')
            else:
                hlp += '\n'
        print(hlp)