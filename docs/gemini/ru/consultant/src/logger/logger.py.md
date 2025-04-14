### **Анализ кода модуля `src.logger.logger`**

2. **Качество кода**:
   - **Соответствие стандартам**: 7/10
   - **Плюсы**:
     - Реализован паттерн Singleton для класса Logger.
     - Используется модуль `colorama` для раскрашивания консольного вывода.
     - Присутствует возможность логирования в файлы различных уровней (info, debug, errors) и в JSON-формате.
     - Наличие кастомного форматтера `JsonFormatter` для логирования в JSON.
   - **Минусы**:
     - В коде есть строки, превышающие 79 символов, что нарушает PEP8.
     - Отсутствуют аннотации типов для некоторых переменных и возвращаемых значений функций.
     - Некоторые docstring написаны на английском языке. Необходимо перевести на русский.
     - Не все функции имеют docstring.
     - В некоторых местах используется старый стиль форматирования строк.
     - Не используется `j_loads` для чтения `config.json`.
     - Не все переменные аннотированы.
     - `Union` в коде не используется, поэтому заменять нечего.

3. **Рекомендации по улучшению**:
   - Добавить docstring для всех классов и методов, включая описание аргументов и возвращаемых значений.
   - Перевести существующие docstring на русский язык и привести к единому стилю оформления.
   - Устранить строки, превышающие 79 символов в длину, чтобы соответствовать PEP8.
   - Добавить аннотации типов для всех переменных и возвращаемых значений функций.
   - Использовать `j_loads` для чтения `config.json`.
   - Использовать f-строки для форматирования строк, где это уместно.

4. **Оптимизированный код**:

```python
# -*- coding: utf-8 -*-

"""
Модуль логгера
================

Модуль предоставляет класс :class:`Logger`, который реализует паттерн Singleton
и обеспечивает логирование в консоль, файлы и JSON-формате.
"""

import logging
import colorama
import datetime
import json
import inspect
import threading
from pathlib import Path
from typing import Optional, Tuple
from types import SimpleNamespace

import header
from header import __root__


TEXT_COLORS = {
    'black': colorama.Fore.BLACK,
    'red': colorama.Fore.RED,
    'green': colorama.Fore.GREEN,
    'yellow': colorama.Fore.YELLOW,
    'blue': colorama.Fore.BLUE,
    'magenta': colorama.Fore.MAGENTA,
    'cyan': colorama.Fore.CYAN,
    'white': colorama.Fore.WHITE,
    'light_gray': colorama.Fore.LIGHTBLACK_EX,
    'light_red': colorama.Fore.LIGHTRED_EX,
    'light_green': colorama.Fore.LIGHTGREEN_EX,
    'light_yellow': colorama.Fore.LIGHTYELLOW_EX,
    'light_blue': colorama.Fore.LIGHTBLUE_EX,
    'light_magenta': colorama.Fore.LIGHTMAGENTA_EX,
    'light_cyan': colorama.Fore.LIGHTCYAN_EX,
}

# Словарь для цветов фона
BG_COLORS = {
    'black': colorama.Back.BLACK,
    'red': colorama.Back.RED,
    'green': colorama.Back.GREEN,
    'yellow': colorama.Back.YELLOW,
    'blue': colorama.Back.BLUE,
    'magenta': colorama.Back.MAGENTA,
    'cyan': colorama.Back.CYAN,
    'white': colorama.Back.WHITE,
    'light_gray': colorama.Back.LIGHTBLACK_EX,
    'light_red': colorama.Back.LIGHTRED_EX,
    'light_green': colorama.Back.LIGHTGREEN_EX,
    'light_yellow': colorama.Back.LIGHTYELLOW_EX,
    'light_blue': colorama.Back.LIGHTBLUE_EX,
    'light_magenta': colorama.Back.LIGHTMAGENTA_EX,
    'light_cyan': colorama.Back.LIGHTCYAN_EX,
}

LOG_SYMBOLS = {
    logging.INFO: 'ℹ️',  # Information
    logging.WARNING: '⚠️',  # Warning
    logging.ERROR: '❌',  # Error
    logging.CRITICAL: '🔥',  # Critical
    logging.DEBUG: '🐛',  # Debug
    'EXCEPTION': '🚨',  # Exception
    'SUCCESS': '✅'  # Success
}


class SingletonMeta(type):
    """Metaclass for Singleton pattern implementation."""

    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class JsonFormatter(logging.Formatter):
    """Custom formatter for logging in JSON format."""

    def format(self, record: logging.LogRecord) -> str:
        """
        Форматирует запись лога в формате JSON.

        Args:
            record (logging.LogRecord): Запись лога.

        Returns:
            str: JSON-представление записи лога.
        """
        log_entry = {
            'asctime': self.formatTime(record, self.datefmt),
            'levelname': record.levelname,
            'message': record.getMessage().replace('"', '\''),
            'exc_info': self.formatException(record.exc_info)
            if record.exc_info
            else None,
        }
        _json: str = json.dumps(log_entry, ensure_ascii=False)
        return _json


class Logger(metaclass=SingletonMeta):
    """
    Logger class implementing Singleton pattern with console, file, and JSON logging.
    """

    log_files_path: Path
    info_log_path: Path
    debug_log_path: Path
    errors_log_path: Path
    json_log_path: Path

    def __init__(
        self,
        info_log_path: Optional[str] = None,
        debug_log_path: Optional[str] = None,
        errors_log_path: Optional[str] = None,
        json_log_path: Optional[str] = None,
    ) -> None:
        """
        Инициализирует экземпляр Logger.

        Args:
            info_log_path (Optional[str], optional): Путь к файлу информационных логов. Defaults to None.
            debug_log_path (Optional[str], optional): Путь к файлу дебаг логов. Defaults to None.
            errors_log_path (Optional[str], optional): Путь к файлу логов ошибок. Defaults to None.
            json_log_path (Optional[str], optional): Путь к файлу JSON логов. Defaults to None.
        """
        # Define file paths
        from src.utils.file_utils import j_loads

        config = SimpleNamespace(**j_loads(Path(__root__ / 'src' / 'config.json')))
        timestamp: str = datetime.datetime.now().strftime('%d%m%y%H%M')
        base_path: Path = Path(config.path['log'])
        self.log_files_path: Path = base_path / timestamp

        self.info_log_path = self.log_files_path / (info_log_path or 'info.log')
        self.debug_log_path = self.log_files_path / (debug_log_path or 'debug.log')
        self.errors_log_path = self.log_files_path / (errors_log_path or 'errors.log')
        self.json_log_path = base_path / (json_log_path or f'{timestamp}.json')

        # Ensure directories exist
        self.log_files_path.mkdir(parents=True, exist_ok=True)

        # Ensure log files exist
        self.info_log_path.touch(exist_ok=True)
        self.debug_log_path.touch(exist_ok=True)
        self.errors_log_path.touch(exist_ok=True)
        self.json_log_path.touch(exist_ok=True)

        # Console logger
        self.logger_console: logging.Logger = logging.getLogger(name='logger_console')
        self.logger_console.setLevel(logging.DEBUG)

        # Info file logger
        self.logger_file_info: logging.Logger = logging.getLogger(name='logger_file_info')
        self.logger_file_info.setLevel(logging.INFO)
        info_handler: logging.FileHandler = logging.FileHandler(self.info_log_path)
        info_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        self.logger_file_info.addHandler(info_handler)

        # Debug file logger
        self.logger_file_debug: logging.Logger = logging.getLogger(name='logger_file_debug')
        self.logger_file_debug.setLevel(logging.DEBUG)
        debug_handler: logging.FileHandler = logging.FileHandler(self.debug_log_path)
        debug_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        self.logger_file_debug.addHandler(debug_handler)

        # Errors file logger
        self.logger_file_errors: logging.Logger = logging.getLogger(name='logger_file_errors')
        self.logger_file_errors.setLevel(logging.ERROR)
        errors_handler: logging.FileHandler = logging.FileHandler(self.errors_log_path)
        errors_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        self.logger_file_errors.addHandler(errors_handler)

        # JSON file logger
        self.logger_file_json: logging.Logger = logging.getLogger(name='logger_json')
        self.logger_file_json.setLevel(logging.DEBUG)
        json_handler: logging.FileHandler = logging.FileHandler(self.json_log_path)
        json_handler.setFormatter(JsonFormatter())  # Используем наш кастомный форматтер
        self.logger_file_json.addHandler(json_handler)

        # Удаляем все обработчики, которые выводят в консоль
        for handler in self.logger_file_json.handlers:
            if isinstance(handler, logging.StreamHandler):
                self.logger_file_json.removeHandler(handler)

    def _format_message(
        self,
        message: str,
        ex: Optional[Exception] = None,
        color: Optional[Tuple[str, str]] = None,
        level: Optional[int] = None,
    ) -> str:
        """
        Возвращает отформатированное сообщение с опциональным цветом и информацией об исключении.

        Args:
            message (str): Сообщение для логирования.
            ex (Optional[Exception], optional): Объект исключения. Defaults to None.
            color (Optional[Tuple[str, str]], optional): Кортеж цветов текста и фона. Defaults to None.
            level (Optional[int], optional): Уровень логирования. Defaults to None.

        Returns:
            str: Отформатированное сообщение.
        """
        log_symbol: str = LOG_SYMBOLS.get(level, '')  # Get log symbol based on level
        if color:
            text_color, bg_color = color
            text_color: str = TEXT_COLORS.get(text_color, colorama.Fore.RESET)
            bg_color: str = BG_COLORS.get(bg_color, colorama.Back.RESET)
            message = f'{log_symbol} {text_color}{bg_color}{message} {ex or ""}{colorama.Style.RESET_ALL}'
        else:
            message = f'{log_symbol} {message} {ex or ""}'
        return message

    def _ex_full_info(self, ex: Exception) -> str:
        """
        Возвращает полную информацию об исключении вместе с деталями о предыдущей функции, файле и строке.

        Args:
            ex (Exception): Объект исключения.

        Returns:
            str: Полная информация об исключении.
        """
        frame_info = inspect.stack()[3]
        file_name: str = frame_info.filename
        function_name: str = frame_info.function
        line_number: int = frame_info.lineno

        return f'\nFile: {file_name}, \n |\n  -Function: {function_name}, \n   |\n    --Line: {line_number}\n{ex if ex else ""}'

    def log(
        self,
        level: int,
        message: str,
        ex: Optional[Exception] = None,
        exc_info: bool = False,
        color: Optional[Tuple[str, str]] = None,
    ) -> None:
        """
        Общий метод для логирования сообщений на указанном уровне с опциональным цветом.

        Args:
            level (int): Уровень логирования.
            message (str): Сообщение для логирования.
            ex (Optional[Exception], optional): Объект исключения. Defaults to None.
            exc_info (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. Defaults to False.
            color (Optional[Tuple[str, str]], optional): Кортеж цветов текста и фона. Defaults to None.
        """
        formatted_message: str = self._format_message(message, ex, color, level=level)

        if self.logger_console:
            if exc_info and ex:
                self.logger_console.exception(formatted_message)
            else:
                self.logger_console.log(level, formatted_message, exc_info=exc_info)

    def info(
        self,
        message: str,
        ex: Optional[Exception] = None,
        exc_info: bool = False,
        text_color: str = 'green',
        bg_color: str = '',
    ) -> None:
        """
        Логирует информационное сообщение с опциональными цветами текста и фона.

        Args:
            message (str): Сообщение для логирования.
            ex (Optional[Exception], optional): Объект исключения. Defaults to None.
            exc_info (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. Defaults to False.
            text_color (str, optional): Цвет текста. Defaults to "green".
            bg_color (str, optional): Цвет фона. Defaults to "".
        """
        color: Tuple[str, str] = (text_color, bg_color)
        self.log(logging.INFO, message, ex, exc_info, color)

    def success(
        self,
        message: str,
        ex: Optional[Exception] = None,
        exc_info: bool = False,
        text_color: str = 'yellow',
        bg_color: str = '',
    ) -> None:
        """
        Логирует сообщение об успехе с опциональными цветами текста и фона.

        Args:
            message (str): Сообщение для логирования.
            ex (Optional[Exception], optional): Объект исключения. Defaults to None.
            exc_info (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. Defaults to False.
            text_color (str, optional): Цвет текста. Defaults to "yellow".
            bg_color (str, optional): Цвет фона. Defaults to "".
        """
        color: Tuple[str, str] = (text_color, bg_color)
        self.log(logging.INFO, message, ex, exc_info, color)

    def warning(
        self,
        message: str,
        ex: Optional[Exception] = None,
        exc_info: bool = False,
        text_color: str = 'light_red',
        bg_color: str = '',
    ) -> None:
        """
        Логирует предупреждение с опциональными цветами текста и фона.

        Args:
            message (str): Сообщение для логирования.
            ex (Optional[Exception], optional): Объект исключения. Defaults to None.
            exc_info (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. Defaults to False.
            text_color (str, optional): Цвет текста. Defaults to "light_red".
            bg_color (str, optional): Цвет фона. Defaults to "".
        """
        color: Tuple[str, str] = (text_color, bg_color)
        self.log(logging.WARNING, message, ex, exc_info, color)

    def debug(
        self,
        message: str,
        ex: Optional[Exception] = None,
        exc_info: bool = True,
        text_color: str = 'cyan',
        bg_color: str = '',
    ) -> None:
        """
        Логирует отладочное сообщение с опциональными цветами текста и фона.

        Args:
            message (str): Сообщение для логирования.
            ex (Optional[Exception], optional): Объект исключения. Defaults to None.
            exc_info (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. Defaults to True.
            text_color (str, optional): Цвет текста. Defaults to "cyan".
            bg_color (str, optional): Цвет фона. Defaults to "".
        """
        color: Tuple[str, str] = (text_color, bg_color)
        self.log(logging.DEBUG, message, ex, exc_info, color)

    def exception(
        self,
        message: str,
        ex: Optional[Exception] = None,
        exc_info: bool = True,
        text_color: str = 'cyan',
        bg_color: str = 'light_gray',
    ) -> None:
        """
        Логирует сообщение об исключении с опциональными цветами текста и фона.

        Args:
            message (str): Сообщение для логирования.
            ex (Optional[Exception], optional): Объект исключения. Defaults to None.
            exc_info (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. Defaults to True.
            text_color (str, optional): Цвет текста. Defaults to "cyan".
            bg_color (str, optional): Цвет фона. Defaults to "light_gray".
        """
        color: Tuple[str, str] = (text_color, bg_color)
        self.log(logging.ERROR, message, ex, exc_info, color)  # Log as error

    def error(
        self,
        message: str,
        ex: Optional[Exception] = None,
        exc_info: bool = True,
        text_color: str = 'red',
        bg_color: str = '',
    ) -> None:
        """
        Логирует сообщение об ошибке с опциональными цветами текста и фона.

        Args:
            message (str): Сообщение для логирования.
            ex (Optional[Exception], optional): Объект исключения. Defaults to None.
            exc_info (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. Defaults to True.
            text_color (str, optional): Цвет текста. Defaults to "red".
            bg_color (str, optional): Цвет фона. Defaults to "".
        """
        color: Tuple[str, str] = (text_color, bg_color)
        self.log(logging.ERROR, message, ex, exc_info, color)

    def critical(
        self,
        message: str,
        ex: Optional[Exception] = None,
        exc_info: bool = True,
        text_color: str = 'red',
        bg_color: str = 'white',
    ) -> None:
        """
        Логирует критическое сообщение с опциональными цветами текста и фона.

        Args:
            message (str): Сообщение для логирования.
            ex (Optional[Exception], optional): Объект исключения. Defaults to None.
            exc_info (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. Defaults to True.
            text_color (str, optional): Цвет текста. Defaults to "red".
            bg_color (str, optional): Цвет фона. Defaults to "white".
        """
        color: Tuple[str, str] = (text_color, bg_color)
        self.log(logging.CRITICAL, message, ex, exc_info, color)


# Initialize logger with file paths
# logger = Logger(info_log_path='info.log', debug_log_path='debug.log', errors_log_path='errors.log', json_log_path='log.json')
logger: Logger = Logger()