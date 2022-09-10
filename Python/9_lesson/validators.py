import sys
import os
from typing import Tuple, Any
from datetime import datetime
from utils import MISSING

class ValidatorResult:
    def __init__(self, value: Any, is_ok: bool = True, message: str = 'Error'):
        self.is_ok = bool(is_ok)
        self.value = value
        self.message = str(message)

    @classmethod
    def valid(cls, value: Any) -> 'ValidatorResult':
        return ValidatorResult(value)

    @classmethod
    def invalid(cls, message: str = 'Error') -> 'ValidatorResult':
        return ValidatorResult(None, False, message)


class NullValidator:
    def __call__(self, value: Any, default: Any = MISSING) -> ValidatorResult:
        return ValidatorResult.valid(value)


class YnValidator:
    def __init__(
        self, 
        yes: Tuple[str] = ('y', 'ye', 'yes', 'yeah'),
        no: Tuple[str] = ('n', 'no', 'nope'),
    ):
        self.yes = yes
        self.no = no

    def __call__(self, value: Any, default: Any = MISSING) -> ValidatorResult:
        if value == default and default is not MISSING:
            return ValidatorResult.valid(default)
        try:
            value = str(value)
            if value.lower() in self.yes:
                return ValidatorResult.valid(True)
            elif value.lower() in self.no:
                return ValidatorResult.valid(False)
            else:
                return ValidatorResult.invalid(f'Type in {self.yes} or {self.no}')
        except Exception:
            return ValidatorResult.invalid('Expected str')


class IntValidator:

    MIN_INT = - sys.maxsize - 1
    MAX_INT = sys.maxsize

    def __init__(self, start: int = MIN_INT, end: int = MAX_INT) -> None:
        self.start = start
        self.end = end
    
    def __call__(self, value: Any, default: Any = MISSING) -> ValidatorResult:
        if value == default and default is not MISSING:
            return ValidatorResult.valid(default)
        try:
            value = int(value)
            if value < self.start:
                return ValidatorResult.invalid(f'Value must be greater than {self.start}')
            if value > self.end:
                return ValidatorResult.invalid(f'Value must be less than {self.end}')
            return ValidatorResult.valid(value)
        except (ValueError, TypeError):
            return ValidatorResult.invalid('Value is not a digit')


class DateValidator:
    def __init__(self, fmt: str):
        self.fmt = fmt
        self.last_value = None
    
    def __call__(self, value: Any, default: Any = MISSING) -> ValidatorResult:
        if value == default and default is not MISSING:
            return ValidatorResult.valid(default)
        try:
            dt = datetime.strptime(value, self.fmt).date()
            return ValidatorResult.valid(dt)
        except ValueError as e:
            return ValidatorResult.invalid(f'Error: {e}')
        except TypeError as e:
            return ValidatorResult.invalid(f'Value must be a date in format {self.fmt}')


class JsonFilePathValidator:
    def __call__(self, value: Any, default: Any = MISSING) -> ValidatorResult:
        file_path = str(value)
        if file_path == default and default is not MISSING:
            return ValidatorResult.valid(default)
        if not os.path.exists(file_path):
            return ValidatorResult.invalid(f'Path "{file_path}" does not exist.')

        file_path = os.path.abspath(value)

        if not os.path.isfile(file_path):
            return ValidatorResult.invalid(f'"{file_path}" is not a file')
        if not file_path.endswith('.json'):
            return ValidatorResult.invalid(f'"{file_path}" is not a json file')

        return ValidatorResult.valid(file_path)
