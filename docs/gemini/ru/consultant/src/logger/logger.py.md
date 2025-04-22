### **Анализ кода модуля `src.logger.logger`**

2. **Качество кода**:
   - **Соответствие стандартам**: 8/10
   - **Плюсы**:
     - Реализован паттерн Singleton для класса Logger, что обеспечивает единственный экземпляр логгера во всей системе.
     - Поддержка различных уровней логирования (INFO, DEBUG, WARNING, ERROR, CRITICAL).
     - Возможность логирования в консоль, файлы и JSON формат.
     - Использование библиотеки `colorama` для раскрашивания сообщений в консоли.
     - Наличие кастомного форматтера `JsonFormatter` для логирования в JSON формате.
   - **Минусы**:
     - Отсутствуют аннотации типов для некоторых переменных и возвращаемых значений.
     - В некоторых местах используется `Optional[str] = None`, можно заменить на `str | None`.
     - Инициализация конфигурации через `SimpleNamespace` и `json.loads` выглядит несколько громоздко.
     - Не все методы имеют docstring.

3. **Рекомендации по улучшению**:
   - Добавить docstring для всех методов класса Logger, включая описание параметров и возвращаемых значений.
   - Использовать `str | None` вместо `Optional[str] = None` для аннотаций типов.
   - Улучшить читаемость инициализации конфигурации, возможно, вынести в отдельную функцию или использовать более удобный способ чтения конфигурационных файлов (например, `j_loads`).
   - Добавить обработку возможных исключений при чтении конфигурационного файла.
   - Добавить возможность перехвата и обработки исключений на уровне логирования, чтобы избежать дублирования кода в разных местах.
   - Изменить способ форматирования сообщений, чтобы упростить добавление новых цветов и стилей.
   - Добавить возможность настройки форматирования времени в JsonFormatter.
   - Добавить проверки на существование директорий и файлов перед их созданием.

4. **Оптимизированный код**:

```python
                # -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль логгера
==============

Модуль предоставляет класс :class:`Logger`, реализующий паттерн Singleton для логирования сообщений
различных уровней (INFO, DEBUG, WARNING, ERROR, CRITICAL) в консоль, файлы и JSON формат.
Использует библиотеку `colorama` для раскрашивания сообщений в консоли.

Пример использования
----------------------

>>> from src.logger import logger
>>> logger.info('Информационное сообщение')
>>> logger.error('Сообщение об ошибке', ex=Exception('Описание ошибки'), exc_info=True)

.. module:: src.logger.logger
"""

import logging
import colorama
import datetime
import json
import inspect
import threading
from pathlib import Path
from typing import Optional, Tuple, Dict
from types import SimpleNamespace

import header
from header import __root__

TEXT_COLORS: Dict[str, str] = {
    "black": colorama.Fore.BLACK,
    "red": colorama.Fore.RED,
    "green": colorama.Fore.GREEN,
    "yellow": colorama.Fore.YELLOW,
    "blue": colorama.Fore.BLUE,
    "magenta": colorama.Fore.MAGENTA,
    "cyan": colorama.Fore.CYAN,
    "white": colorama.Fore.WHITE,
    "light_gray": colorama.Fore.LIGHTBLACK_EX,
    "light_red": colorama.Fore.LIGHTRED_EX,
    "light_green": colorama.Fore.LIGHTGREEN_EX,
    "light_yellow": colorama.Fore.LIGHTYELLOW_EX,
    "light_blue": colorama.Fore.LIGHTBLUE_EX,
    "light_magenta": colorama.Fore.LIGHTMAGENTA_EX,
    "light_cyan": colorama.Fore.LIGHTCYAN_EX,
}

# Словарь для цветов фона
BG_COLORS: Dict[str, str] = {
    "black": colorama.Back.BLACK,
    "red": colorama.Back.RED,
    "green": colorama.Back.GREEN,
    "yellow": colorama.Back.YELLOW,
    "blue": colorama.Back.BLUE,
    "magenta": colorama.Back.MAGENTA,
    "cyan": colorama.Back.CYAN,
    "white": colorama.Back.WHITE,
    "light_gray": colorama.Back.LIGHTBLACK_EX,
    "light_red": colorama.Back.LIGHTRED_EX,
    "light_green": colorama.Back.LIGHTGREEN_EX,
    "light_yellow": colorama.Back.LIGHTYELLOW_EX,
    "light_blue": colorama.Back.LIGHTBLUE_EX,
    "light_magenta": colorama.Back.LIGHTMAGENTA_EX,
    "light_cyan": colorama.Back.LIGHTCYAN_EX,
}

LOG_SYMBOLS: Dict[int | str, str] = {
    logging.INFO: "ℹ️",  # Information
    logging.WARNING: "⚠️",  # Warning
    logging.ERROR: "❌",  # Error
    logging.CRITICAL: "🔥",  # Critical
    logging.DEBUG: "🐛",  # Debug
    "EXCEPTION": "🚨",  # Exception
    "SUCCESS": "✅"  # Success
}


class SingletonMeta(type):
    """Metaclass for Singleton pattern implementation."""

    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        """Выполняет создание единственного экземпляра класса."""
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class JsonFormatter(logging.Formatter):
    """Custom formatter for logging in JSON format."""

    def format(self, record: logging.LogRecord) -> str:
        """Форматирует запись лога как JSON."""
        log_entry = {
            "asctime": self.formatTime(record, self.datefmt),
            "levelname": record.levelname,
            "message": record.getMessage().replace('"', "'"),
            "exc_info": self.formatException(record.exc_info)
            if record.exc_info
            else None,
        }
        _json = json.dumps(log_entry, ensure_ascii=False)
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
        cls,
        info_log_path: str | None = None,
        debug_log_path: str | None = None,
        errors_log_path: str | None = None,
        json_log_path: str | None = None,
    ) -> None:
        """
        Инициализирует экземпляр Logger.

        Args:
            info_log_path (str | None): Путь к файлу для информационных логов.
            debug_log_path (str | None): Путь к файлу для отладочных логов.
            errors_log_path (str | None): Путь к файлу для логов ошибок.
            json_log_path (str | None): Путь к файлу для JSON логов.
        """
        # Функция извлекает значение из конфигурационного файла
        try:
            config = SimpleNamespace(
                **json.loads(Path(__root__ / "src" / "config.json").read_text(encoding="UTF-8"))
            )
        except Exception as ex:
            print(f'Ошибка при чтении файла конфигурации: {ex}')
            config = SimpleNamespace()
        timestamp = datetime.datetime.now().strftime("%d%m%y%H%M")
        base_path: Path = Path(config.path.get("log", "."))
        cls.log_files_path: Path = base_path / timestamp

        cls.info_log_path = cls.log_files_path / (info_log_path or "info.log")
        cls.debug_log_path = cls.log_files_path / (debug_log_path or "debug.log")
        cls.errors_log_path = cls.log_files_path / (errors_log_path or "errors.log")
        cls.json_log_path = base_path / (json_log_path or f"{timestamp}.json")

        # Функция создает директории, если они не существуют
        cls.log_files_path.mkdir(parents=True, exist_ok=True)

        # Функция создает файлы, если они не существуют
        cls.info_log_path.touch(exist_ok=True)
        cls.debug_log_path.touch(exist_ok=True)
        cls.errors_log_path.touch(exist_ok=True)
        cls.json_log_path.touch(exist_ok=True)

        # Console logger
        cls.logger_console = logging.getLogger(name="logger_console")
        cls.logger_console.setLevel(logging.DEBUG)

        # Info file logger
        cls.logger_file_info = logging.getLogger(name="logger_file_info")
        cls.logger_file_info.setLevel(logging.INFO)
        info_handler = logging.FileHandler(cls.info_log_path)
        info_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        cls.logger_file_info.addHandler(info_handler)

        # Debug file logger
        cls.logger_file_debug = logging.getLogger(name="logger_file_debug")
        cls.logger_file_debug.setLevel(logging.DEBUG)
        debug_handler = logging.FileHandler(cls.debug_log_path)
        debug_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        cls.logger_file_debug.addHandler(debug_handler)

        # Errors file logger
        cls.logger_file_errors = logging.getLogger(name="logger_file_errors")
        cls.logger_file_errors.setLevel(logging.ERROR)
        errors_handler = logging.FileHandler(cls.errors_log_path)
        errors_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        cls.logger_file_errors.addHandler(errors_handler)

        # JSON file logger
        cls.logger_file_json = logging.getLogger(name="logger_json")
        cls.logger_file_json.setLevel(logging.DEBUG)
        json_handler = logging.FileHandler(cls.json_log_path)
        json_handler.setFormatter(JsonFormatter())  # Используем наш кастомный форматтер
        cls.logger_file_json.addHandler(json_handler)

        # Функция удаляет все обработчики, которые выводят в консоль
        for handler in cls.logger_file_json.handlers:
            if isinstance(handler, logging.StreamHandler):
                cls.logger_file_json.removeHandler(handler)

    def _format_message(cls, message: str, ex: Exception | None = None, color: Tuple[str, str] | None = None, level: int | None = None) -> str:
        """
        Форматирует сообщение с опциональным цветом и информацией об исключении.

        Args:
            message (str): Сообщение для логирования.
            ex (Exception | None): Объект исключения (опционально).
            color (Tuple[str, str] | None): Кортеж с цветом текста и фона (опционально).
            level (int | None): Уровень логирования (опционально).

        Returns:
            str: Сформатированное сообщение.
        """
        log_symbol = LOG_SYMBOLS.get(level, "")  # Функция получает символ лога на основе уровня
        if color:
            text_color, bg_color = color
            text_color = TEXT_COLORS.get(text_color, colorama.Fore.RESET)
            bg_color = BG_COLORS.get(bg_color, colorama.Back.RESET)
            message = f"{log_symbol} {text_color}{bg_color}{message} {ex or ''}{colorama.Style.RESET_ALL}"
        else:
            message = f"{log_symbol} {message} {ex or ''}"
        return message

    def _ex_full_info(cls, ex: Exception) -> str:
        """
        Возвращает полную информацию об исключении, включая данные о функции, файле и номере строки.

        Args:
            ex (Exception): Объект исключения.

        Returns:
            str: Полная информация об исключении.
        """
        frame_info = inspect.stack()[3]
        file_name = frame_info.filename
        function_name = frame_info.function
        line_number = frame_info.lineno

        return f"\nFile: {file_name}, \n |\n  -Function: {function_name}, \n   |\n    --Line: {line_number}\n{ex if ex else ''}"

    def log(cls, level: int, message: str, ex: Exception | None = None, exc_info: bool = False, color: Tuple[str, str] | None = None) -> None:
        """
        Основной метод для логирования сообщений на указанном уровне с опциональным цветом.

        Args:
            level (int): Уровень логирования (например, logging.INFO, logging.ERROR).
            message (str): Сообщение для логирования.
            ex (Exception | None): Объект исключения (опционально).
            exc_info (bool): Флаг, указывающий, нужно ли включать информацию об исключении.
            color (Tuple[str, str] | None): Кортеж с цветом текста и фона (опционально).
        """
        formatted_message = cls._format_message(message, ex, color, level=level)

        if cls.logger_console:
            # cls.logger_console.log(level, formatted_message, exc_info=exc_info) # Old code
            if exc_info and ex:
                cls.logger_console.exception(formatted_message)
            else:
                cls.logger_console.log(level, formatted_message, exc_info=exc_info)

    def info(cls, message: str, ex: Exception | None = None, exc_info: bool = False, text_color: str = "green", bg_color: str = "") -> None:
        """
        Логирует информационное сообщение с опциональным цветом текста и фона.

        Args:
            message (str): Сообщение для логирования.
            ex (Exception | None): Объект исключения (опционально).
            exc_info (bool): Флаг, указывающий, нужно ли включать информацию об исключении.
            text_color (str): Цвет текста (опционально).
            bg_color (str): Цвет фона (опционально).
        """
        color = (text_color, bg_color)
        cls.log(logging.INFO, message, ex, exc_info, color)

    def success(cls, message: str, ex: Exception | None = None, exc_info: bool = False, text_color: str = "yellow", bg_color: str = "") -> None:
        """
        Логирует сообщение об успехе с опциональным цветом текста и фона.

        Args:
            message (str): Сообщение для логирования.
            ex (Exception | None): Объект исключения (опционально).
            exc_info (bool): Флаг, указывающий, нужно ли включать информацию об исключении.
            text_color (str): Цвет текста (опционально).
            bg_color (str): Цвет фона (опционально).
        """
        color = (text_color, bg_color)
        cls.log(logging.INFO, message, ex, exc_info, color)

    def warning(cls, message: str, ex: Exception | None = None, exc_info: bool = False, text_color: str = "light_red", bg_color: str = "") -> None:
        """
        Логирует предупреждающее сообщение с опциональным цветом текста и фона.

        Args:
            message (str): Сообщение для логирования.
            ex (Exception | None): Объект исключения (опционально).
            exc_info (bool): Флаг, указывающий, нужно ли включать информацию об исключении.
            text_color (str): Цвет текста (опционально).
            bg_color (str): Цвет фона (опционально).
        """
        color = (text_color, bg_color)
        cls.log(logging.WARNING, message, ex, exc_info, color)

    def debug(cls, message: str, ex: Exception | None = None, exc_info: bool = True, text_color: str = "cyan", bg_color: str = "") -> None:
        """
        Логирует отладочное сообщение с опциональным цветом текста и фона.

        Args:
            message (str): Сообщение для логирования.
            ex (Exception | None): Объект исключения (опционально).
            exc_info (bool): Флаг, указывающий, нужно ли включать информацию об исключении.
            text_color (str): Цвет текста (опционально).
            bg_color (str): Цвет фона (опционально).
        """
        color = (text_color, bg_color)
        cls.log(logging.DEBUG, message, ex, exc_info, color)

    def exception(cls, message: str, ex: Exception | None = None, exc_info: bool = True, text_color: str = "cyan", bg_color: str = "light_gray") -> None:
        """
        Логирует сообщение об исключении с опциональным цветом текста и фона.

        Args:
            message (str): Сообщение для логирования.
            ex (Exception | None): Объект исключения (опционально).
            exc_info (bool): Флаг, указывающий, нужно ли включать информацию об исключении.
            text_color (str): Цвет текста (опционально).
            bg_color (str): Цвет фона (опционально).
        """
        color = (text_color, bg_color)
        cls.log(logging.ERROR, message, ex, exc_info, color)  # Log as error

    def error(cls, message: str, ex: Exception | None = None, exc_info: bool = True, text_color: str = "red", bg_color: str = "") -> None:
        """
        Логирует сообщение об ошибке с опциональным цветом текста и фона.

        Args:
            message (str): Сообщение для логирования.
            ex (Exception | None): Объект исключения (опционально).
            exc_info (bool): Флаг, указывающий, нужно ли включать информацию об исключении.
            text_color (str): Цвет текста (опционально).
            bg_color (str): Цвет фона (опционально).
        """
        color = (text_color, bg_color)
        cls.log(logging.ERROR, message, ex, exc_info, color)

    def critical(cls, message: str, ex: Exception | None = None, exc_info: bool = True, text_color: str = "red", bg_color: str = "white") -> None:
        """
        Логирует критическое сообщение с опциональным цветом текста и фона.

        Args:
            message (str): Сообщение для логирования.
            ex (Exception | None): Объект исключения (опционально).
            exc_info (bool): Флаг, указывающий, нужно ли включать информацию об исключении.
            text_color (str): Цвет текста (опционально).
            bg_color (str): Цвет фона (опционально).
        """
        color = (text_color, bg_color)
        cls.log(logging.CRITICAL, message, ex, exc_info, color)


# Initialize logger with file paths
# logger = Logger(info_log_path='info.log', debug_log_path='debug.log', errors_log_path='errors.log', json_log_path='log.json')
logger: Logger = Logger()