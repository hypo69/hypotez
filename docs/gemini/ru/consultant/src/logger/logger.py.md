### **Анализ кода модуля `src.logger.logger`**

**Качество кода**:

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Реализация паттерна Singleton для класса Logger.
  - Использование модуля `colorama` для раскраски вывода в консоль.
  - Возможность логирования в файлы разных уровней (info, debug, errors, json).
  - Кастомизированный форматтер `JsonFormatter` для логирования в JSON.
- **Минусы**:
  - Отсутствие docstring для некоторых методов (например, `_ex_full_info`).
  - Использование устаревшего форматирования строк (следует заменить на f-строки).
  - Смешивание логики форматирования сообщений и логирования в методах (`log`, `info`, `error` и т.д.).
  - Жестко заданные пути к файлам конфигурации и логов. Желательно использовать переменные окружения или параметры конфигурации.
  - Не все переменные аннотированы типами.

**Рекомендации по улучшению**:

1.  **Добавить docstring для всех методов и классов**. Это улучшит понимание кода и облегчит его использование.

2.  **Использовать f-строки для форматирования строк**. Это сделает код более читаемым и современным.

3.  **Разделить логику форматирования и логирования**. Создать отдельные методы для форматирования сообщений и для их записи в лог.

4.  **Использовать переменные окружения или параметры конфигурации для путей к файлам**. Это позволит легко менять пути к логам и файлам конфигурации без изменения кода.

5.  **Добавить обработку исключений при чтении файла конфигурации**. Это позволит избежать падения приложения при отсутствии или повреждении файла конфигурации.

6.  **Аннотировать все переменные типами**.

7.  **Удалить неиспользуемые импорты и переменные.**

8.  **В `logger_file_json` почему-то удаляются все обработчики, которые выводят в консоль. Необходимо это исправить.**

9.  **В блоках except используй `ex` вместо `e`**

**Оптимизированный код**:

```python
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль логгера
=================

Модуль предоставляет класс `Logger`, реализующий паттерн Singleton для логирования в консоль, файлы и JSON.
"""

import logging
import colorama
import datetime
import json
import inspect
import threading
import os
from pathlib import Path
from typing import Optional, Tuple
from types import SimpleNamespace

import header
from header import __root__


TEXT_COLORS: dict[str, str] = {
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
BG_COLORS: dict[str, str] = {
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

LOG_SYMBOLS: dict[int | str, str] = {
    logging.INFO: 'ℹ️',  # Information
    logging.WARNING: '⚠️',  # Warning
    logging.ERROR: '❌',  # Error
    logging.CRITICAL: '🔥',  # Critical
    logging.DEBUG: '🐛',  # Debug
    'EXCEPTION': '🚨',  # Exception
    'SUCCESS': '✅',  # Success
}


class SingletonMeta(type):
    """Metaclass for Singleton pattern implementation."""

    _instances: dict = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class JsonFormatter(logging.Formatter):
    """Custom formatter for logging in JSON format."""

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record as JSON."""
        log_entry: dict = {
            'asctime': self.formatTime(record, self.datefmt),
            'levelname': record.levelname,
            'message': record.getMessage().replace('"', "'"),
            'exc_info': self.formatException(record.exc_info) if record.exc_info else None,
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
            info_log_path (Optional[str], optional): Путь к файлу информационного лога. По умолчанию 'info.log'.
            debug_log_path (Optional[str], optional): Путь к файлу дебаг лога. По умолчанию 'debug.log'.
            errors_log_path (Optional[str], optional): Путь к файлу лога ошибок. По умолчанию 'errors.log'.
            json_log_path (Optional[str], optional): Путь к файлу JSON лога. По умолчанию 'log.json'.
        """
        # Define file paths
        try:
            config = SimpleNamespace(
                **json.loads(Path(__root__ / 'src' / 'config.json').read_text(encoding='UTF-8'))
            )
        except Exception as ex:
            # Обработка исключения при чтении файла конфигурации
            print(f'Ошибка при чтении файла конфигурации: {ex}')
            config = SimpleNamespace()  # Создаем пустой объект SimpleNamespace, чтобы избежать ошибок

        timestamp: str = datetime.datetime.now().strftime('%d%m%y%H%M')
        base_path: Path = Path(config.path['log']) if hasattr(config, 'path') and 'log' in config.path else Path('./logs')
        self.log_files_path: Path = base_path / timestamp

        self.info_log_path: Path = self.log_files_path / (info_log_path or 'info.log')
        self.debug_log_path: Path = self.log_files_path / (debug_log_path or 'debug.log')
        self.errors_log_path: Path = self.log_files_path / (errors_log_path or 'errors.log')
        self.json_log_path: Path = base_path / (json_log_path or f'{timestamp}.json')

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
        # for handler in self.logger_file_json.handlers:
        #     if isinstance(handler, logging.StreamHandler):
        #         self.logger_file_json.removeHandler(handler)

    def _format_message(self, message: str, ex: Optional[Exception] = None, color: Optional[Tuple[str, str]] = None, level: Optional[int | str] = None) -> str:
        """
        Форматирует сообщение лога с учетом уровня, цвета и исключения.

        Args:
            message (str): Текст сообщения.
            ex (Optional[Exception], optional): Исключение. По умолчанию None.
            color (Optional[Tuple[str, str]], optional): Кортеж цветов текста и фона. По умолчанию None.
            level (Optional[int], optional): Уровень логирования. По умолчанию None.

        Returns:
            str: Отформатированное сообщение.
        """
        log_symbol: str = LOG_SYMBOLS.get(level, '')  # Get log symbol based on level
        if color:
            text_color, bg_color = color
            text_color: str = TEXT_COLORS.get(text_color, colorama.Fore.RESET)
            bg_color: str = BG_COLORS.get(bg_color, colorama.Back.RESET)
            message: str = f'{log_symbol} {text_color}{bg_color}{message} {ex or ""}{colorama.Style.RESET_ALL}'
        else:
            message: str = f'{log_symbol} {message} {ex or ""}'
        return message

    def _ex_full_info(self, ex: Exception) -> str:
        """
        Возвращает полную информацию об исключении, включая имя файла, функции и номер строки, где произошло исключение.

        Args:
            ex (Exception): Объект исключения.

        Returns:
            str: Полная информация об исключении.
        """
        frame_info: inspect.FrameInfo = inspect.stack()[3]
        file_name: str = frame_info.filename
        function_name: str = frame_info.function
        line_number: int = frame_info.lineno

        return f'\nFile: {file_name}, \n |\n  -Function: {function_name}, \n   |\n    --Line: {line_number}\n{ex if ex else ""}'

    def log(self, level: int, message: str, ex: Optional[Exception] = None, exc_info: bool = False, color: Optional[Tuple[str, str]] = None) -> None:
        """
        Общий метод для логирования сообщений на указанном уровне.

        Args:
            level (int): Уровень логирования (например, logging.INFO, logging.ERROR).
            message (str): Сообщение для логирования.
            ex (Optional[Exception], optional): Объект исключения. По умолчанию None.
            exc_info (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию False.
            color (Optional[Tuple[str, str]], optional): Кортеж цветов текста и фона. По умолчанию None.
        """
        formatted_message: str = self._format_message(message, ex, color, level=level)

        if self.logger_console:
            if exc_info and ex:
                self.logger_console.exception(formatted_message)
            else:
                self.logger_console.log(level, formatted_message, exc_info=exc_info)

    def info(self, message: str, ex: Optional[Exception] = None, exc_info: bool = False, text_color: str = 'green', bg_color: str = '') -> None:
        """
        Логирует информационное сообщение.

        Args:
            message (str): Сообщение для логирования.
            ex (Optional[Exception], optional): Объект исключения. По умолчанию None.
            exc_info (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию False.
            text_color (str, optional): Цвет текста. По умолчанию 'green'.
            bg_color (str, optional): Цвет фона. По умолчанию ''.
        """
        color: Tuple[str, str] = (text_color, bg_color)
        self.log(logging.INFO, message, ex, exc_info, color)

    def success(self, message: str, ex: Optional[Exception] = None, exc_info: bool = False, text_color: str = 'yellow', bg_color: str = '') -> None:
        """
        Логирует сообщение об успехе.

        Args:
            message (str): Сообщение для логирования.
            ex (Optional[Exception], optional): Объект исключения. По умолчанию None.
            exc_info (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию False.
            text_color (str, optional): Цвет текста. По умолчанию 'yellow'.
            bg_color (str, optional): Цвет фона. По умолчанию ''.
        """
        color: Tuple[str, str] = (text_color, bg_color)
        self.log(logging.INFO, message, ex, exc_info, color)

    def warning(self, message: str, ex: Optional[Exception] = None, exc_info: bool = False, text_color: str = 'light_red', bg_color: str = '') -> None:
        """
        Логирует сообщение предупреждения.

        Args:
            message (str): Сообщение для логирования.
            ex (Optional[Exception], optional): Объект исключения. По умолчанию None.
            exc_info (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию False.
            text_color (str, optional): Цвет текста. По умолчанию 'light_red'.
            bg_color (str, optional): Цвет фона. По умолчанию ''.
        """
        color: Tuple[str, str] = (text_color, bg_color)
        self.log(logging.WARNING, message, ex, exc_info, color)

    def debug(self, message: str, ex: Optional[Exception] = None, exc_info: bool = True, text_color: str = 'cyan', bg_color: str = '') -> None:
        """
        Логирует отладочное сообщение.

        Args:
            message (str): Сообщение для логирования.
            ex (Optional[Exception], optional): Объект исключения. По умолчанию None.
            exc_info (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию True.
            text_color (str, optional): Цвет текста. По умолчанию 'cyan'.
            bg_color (str, optional): Цвет фона. По умолчанию ''.
        """
        color: Tuple[str, str] = (text_color, bg_color)
        self.log(logging.DEBUG, message, ex, exc_info, color)

    def exception(self, message: str, ex: Optional[Exception] = None, exc_info: bool = True, text_color: str = 'cyan', bg_color: str = 'light_gray') -> None:
        """
        Логирует сообщение об исключении.

        Args:
            message (str): Сообщение для логирования.
            ex (Optional[Exception], optional): Объект исключения. По умолчанию None.
            exc_info (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию True.
            text_color (str, optional): Цвет текста. По умолчанию 'cyan'.
            bg_color (str, optional): Цвет фона. По умолчанию 'light_gray'.
        """
        color: Tuple[str, str] = (text_color, bg_color)
        self.log(logging.ERROR, message, ex, exc_info, color)  # Log as error

    def error(self, message: str, ex: Optional[Exception] = None, exc_info: bool = True, text_color: str = 'red', bg_color: str = '') -> None:
        """
        Логирует сообщение об ошибке.

        Args:
            message (str): Сообщение для логирования.
            ex (Optional[Exception], optional): Объект исключения. По умолчанию None.
            exc_info (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию True.
            text_color (str, optional): Цвет текста. По умолчанию 'red'.
            bg_color (str, optional): Цвет фона. По умолчанию ''.
        """
        color: Tuple[str, str] = (text_color, bg_color)
        self.log(logging.ERROR, message, ex, exc_info, color)

    def critical(self, message: str, ex: Optional[Exception] = None, exc_info: bool = True, text_color: str = 'red', bg_color: str = 'white') -> None:
        """
        Логирует критическое сообщение.

        Args:
            message (str): Сообщение для логирования.
            ex (Optional[Exception], optional): Объект исключения. По умолчанию None.
            exc_info (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию True.
            text_color (str, optional): Цвет текста. По умолчанию 'red'.
            bg_color (str, optional): Цвет фона. По умолчанию 'white'.
        """
        color: Tuple[str, str] = (text_color, bg_color)
        self.log(logging.CRITICAL, message, ex, exc_info, color)


# Initialize logger with file paths
logger: Logger = Logger()