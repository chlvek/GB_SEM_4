from typing import Any, Iterable, Optional, Callable
from utils import MISSING
from validators import NullValidator, YnValidator, IntValidator


def input_default(prompt: str, default: Any = MISSING, default_hint: str = MISSING) -> Any:
    '''Prompt a user for input with default value.'''
    if default_hint is MISSING:
        default_hint = f' [{default}]' if default is not MISSING else ''
    else:
        default_hint = f' [{default_hint}]'
    prompt = f'{prompt}{default_hint}: '
    value = input(prompt)
    if not value and default is not MISSING:
        return default
    return value


def ask_once(prompt: str, default: Any = MISSING, validator: Optional[Callable] = MISSING, default_hint: str = MISSING) -> Any:
    '''Prompt user for input.'''
    if validator is MISSING:
        validator = NullValidator()
    
    value = input_default(prompt, default, default_hint)
    validator_result = validator(value, default)
    if not validator_result.is_ok:
        print(validator_result.message)
        return MISSING
    else:
        # print(f'Caught: {validator_result.value} {type(validator_result.value)}')
        return validator_result.value


def ask(prompt: str, default: Any = MISSING, validator: Optional[Callable] = MISSING, default_hint: str = MISSING) -> Any:
    '''
    Prompt user for input.
    
    Runs in cycle until input hasn't
    passed validator.
    '''
    while True:
        value = ask_once(prompt, default, validator, default_hint)
        if value is MISSING:
            continue
        return value


def confirm(prompt: str, default: Optional[bool] = MISSING) -> bool:
    '''Prompt a user for confirmation.'''
    default_hint = MISSING
    if default is not MISSING:
        default = bool(default)
        default_hint = 'yes' if default else 'no'
    return ask(prompt, default, YnValidator(('y', 'yes'), ('n', 'no')), default_hint)


def choice(prompt: str, options: Iterable[str], default: int = MISSING) -> int:
    '''
    Prompt a user to choose from given options.
    
    :param prompt: Prompt message
    :param options: Options
    :param default: Index of the default option in options
    '''
    option_validator = IntValidator(0, len(options) - 1)
    vr = option_validator(default)
    default = vr.value if vr.is_ok else MISSING
    choice_prompt = '\n'.join(f'[{i}]: {option}' for i, option in enumerate(options))
    choice_prompt += f'\n    {prompt}'
    choice = ask(choice_prompt, default, option_validator)
    return choice