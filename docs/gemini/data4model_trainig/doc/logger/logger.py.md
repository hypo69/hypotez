### Анализ кода модуля `src/logger/logger.py`

## Обзор

Модуль предоставляет класс `Logger`, реализующий паттерн Singleton, для логирования сообщений в консоль, файлы и в формате JSON. Поддерживает различные уровни логирования, цветовое выделение в консоли и обработку исключений.

## Подробнее

Модуль предоставляет централизованный механизм логирования для всего проекта. Он использует стандартную библиотеку `logging`, а также добавляет кастомные возможности, такие как цветовое выделение в консоли и форматирование логов в JSON. Реализация паттерна Singleton гарантирует, что в приложении будет только один экземпляр логгера.

## Классы

### `SingletonMeta`

```python
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
```

**Описание**:
Метакласс для реализации паттерна Singleton. Гарантирует, что у класса будет только один экземпляр.

**Атрибуты**:

*   `_instances` (dict): Словарь для хранения экземпляров классов-синглтонов.
*   `_lock` (threading.Lock): Блокировка для обеспечения безопасности при многопоточном создании экземпляра.

**Методы**:

*   `__call__(cls, *args, **kwargs)`:  Переопределяет оператор вызова класса. Если экземпляр класса еще не создан, он создается с использованием блокировки для защиты от одновременного создания в разных потоках.

### `JsonFormatter`

```python
class JsonFormatter(logging.Formatter):
    """Custom formatter for logging in JSON format."""

    def format(self, record):
        """Format the log record as JSON."""
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
```

**Описание**:
Пользовательский форматтер для логирования в формате JSON.

**Наследует**:
- `logging.Formatter`

**Методы**:

*   `format(self, record)`:  Форматирует запись лога в виде JSON-строки. Заменяет двойные кавычки на одинарные в сообщении, чтобы избежать проблем при сериализации в JSON.

### `Logger`

```python
class Logger(metaclass=SingletonMeta):
    """Logger class implementing Singleton pattern with console, file, and JSON logging."""

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
    ):
        """Initialize the Logger instance."""
        # Define file paths
        config = SimpleNamespace(
            **json.loads(Path(__root__ / "src" / "config.json").read_text(encoding="UTF-8"))
        )
        timestamp = datetime.datetime.now().strftime("%d%m%y%H%M")
        base_path: Path = Path(config.path["log"])
        self.log_files_path: Path = base_path / timestamp

        self.info_log_path = self.log_files_path / (info_log_path or "info.log")
        self.debug_log_path = self.log_files_path / (debug_log_path or "debug.log")
        self.errors_log_path = self.log_files_path / (errors_log_path or "errors.log")
        self.json_log_path = base_path / (json_log_path or f"{timestamp}.json")

        # Ensure directories exist
        self.log_files_path.mkdir(parents=True, exist_ok=True)

        # Ensure log files exist
        self.info_log_path.touch(exist_ok=True)
        self.debug_log_path.touch(exist_ok=True)
        self.errors_log_path.touch(exist_ok=True)
        self.json_log_path.touch(exist_ok=True)

        # Console logger
        self.logger_console = logging.getLogger(name="logger_console")
        self.logger_console.setLevel(logging.DEBUG)

        # Info file logger
        self.logger_file_info = logging.getLogger(name="logger_file_info")
        self.logger_file_info.setLevel(logging.INFO)
        info_handler = logging.FileHandler(self.info_log_path)
        info_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        self.logger_file_info.addHandler(info_handler)

        # Debug file logger
        self.logger_file_debug = logging.getLogger(name="logger_file_debug")
        self.logger_file_debug.setLevel(logging.DEBUG)
        debug_handler = logging.FileHandler(self.debug_log_path)
        debug_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        self.logger_file_debug.addHandler(debug_handler)

        # Errors file logger
        self.logger_file_errors = logging.getLogger(name="logger_file_errors")
        self.logger_file_errors.setLevel(logging.ERROR)
        errors_handler = logging.FileHandler(self.errors_log_path)
        errors_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        self.logger_file_errors.addHandler(errors_handler)

        # JSON file logger
        self.logger_file_json = logging.getLogger(name="logger_json")
        self.logger_file_json.setLevel(logging.DEBUG)
        json_handler = logging.FileHandler(self.json_log_path)
        json_handler.setFormatter(JsonFormatter())  # Используем наш кастомный форматтер
        self.logger_file_json.addHandler(json_handler)

        # Удаляем все обработчики, которые выводят в консоль
        for handler in self.logger_file_json.handlers:
            if isinstance(handler, logging.StreamHandler):
                self.logger_file_json.removeHandler(handler)

    def _format_message(self, message, ex=None, color: Optional[Tuple[str, str]] = None, level=None):
        """Returns formatted message with optional color and exception information."""
        log_symbol = LOG_SYMBOLS.get(level, "")  # Get log symbol based on level
        if color:
            text_color, bg_color = color
            text_color = TEXT_COLORS.get(text_color, colorama.Fore.RESET)
            bg_color = BG_COLORS.get(bg_color, colorama.Back.RESET)
            message = f"{log_symbol} {text_color}{bg_color}{message} {ex or ''}{colorama.Style.RESET_ALL}"
        else:
            message = f"{log_symbol} {message} {ex or ''}"
        return message

    def _ex_full_info(self, ex):
        """Returns full exception information along with the previous function, file, and line details."""
        frame_info = inspect.stack()[3]
        file_name = frame_info.filename
        function_name = frame_info.function
        line_number = frame_info.lineno

        return f"\nFile: {file_name}, \n |\n  -Function: {function_name}, \n   |\n    --Line: {line_number}\n{ex if ex else ''}"

    def log(self, level, message, ex=None, exc_info=False, color: Optional[Tuple[str, str]] = None):
        """General method to log messages at specified level with optional color."""
        formatted_message = self._format_message(message, ex, color, level=level)

        if self.logger_console:
            #self.logger_console.log(level, formatted_message, exc_info=exc_info) # Old code
            if exc_info and ex:
                self.logger_console.exception(formatted_message)
            else:
                self.logger_console.log(level, formatted_message, exc_info=exc_info)

    def info(self, message, ex=None, exc_info=False, text_color: str = "green", bg_color: str = ""):
        """Logs an info message with optional text and background colors."""
        color = (text_color, bg_color)
        self.log(logging.INFO, message, ex, exc_info, color)

    def success(self, message, ex=None, exc_info=False, text_color: str = "yellow", bg_color: str = ""):
        """Logs a success message with optional text and background colors."""
        color = (text_color, bg_color)
        self.log(logging.INFO, message, ex, exc_info, color)

    def warning(self, message, ex=None, exc_info=False, text_color: str = "light_red", bg_color: str = ""):
        """Logs a warning message with optional text and background colors."""
        color = (text_color, bg_color)
        self.log(logging.WARNING, message, ex, exc_info, color)

    def debug(self, message, ex=None, exc_info=True, text_color: str = "cyan", bg_color: str = ""):
        """Logs a debug message with optional text and background colors."""
        color = (text_color, bg_color)
        self.log(logging.DEBUG, message, ex, exc_info, color)

    def exception(self, message, ex=None, exc_info=True, text_color: str = "cyan", bg_color: str = "light_gray"):
        """Logs an exception message with optional text and background colors."""
        color = (text_color, bg_color)
        self.log(logging.ERROR, message, ex, exc_info, color) #Log as error

    def error(self, message, ex=None, exc_info=True, text_color: str = "red", bg_color: str = ""):
        """Logs an error message with optional text and background colors."""
        color = (text_color, bg_color)
        self.log(logging.ERROR, message, ex, exc_info, color)

    def critical(self, message, ex=None, exc_info=True, text_color: str = "red", bg_color: str = "white"):
        """Logs a critical message with optional text and background colors."""
        color = (text_color, bg_color)
        self.log(logging.CRITICAL, message, ex, exc_info, color)
```

**Описание**:
Класс `Logger` реализует паттерн Singleton и предоставляет методы для логирования сообщений в консоль, файлы и JSON-файл. Поддерживает различные уровни логирования и цветовое выделение в консоли.

**Наследует**:
- Нет

**Атрибуты**:

*   `log_files_path` (Path): Путь к директории, где хранятся файлы логов.
*   `info_log_path` (Path): Путь к файлу для логирования информационных сообщений.
*   `debug_log_path` (Path): Путь к файлу для логирования отладочных сообщений.
*   `errors_log_path` (Path): Путь к файлу для логирования сообщений об ошибках.
*   `json_log_path` (Path): Путь к файлу для логирования сообщений в формате JSON.
*   `logger_console` (logging.Logger): Объект логгера для вывода в консоль.
*   `logger_file_info` (logging.Logger): Объект логгера для записи информационных сообщений в файл.
*   `logger_file_debug` (logging.Logger): Объект логгера для записи отладочных сообщений в файл.
*   `logger_file_errors` (logging.Logger): Объект логгера для записи сообщений об ошибках в файл.
*   `logger_file_json` (logging.Logger): Объект логгера для записи сообщений в формате JSON в файл.

**Методы**:

*   `__init__(self, info_log_path: Optional[str] = None, debug_log_path: Optional[str] = None, errors_log_path: Optional[str] = None, json_log_path: Optional[str] = None)`:  Инициализирует экземпляр класса `Logger`, настраивает пути к файлам логов и создает объекты логгеров для консоли и файлов.
*   `_format_message(self, message, ex=None, color: Optional[Tuple[str, str]] = None, level=None)`:  Форматирует сообщение лога с учетом уровня, цвета и информации об исключении.
*   `_ex_full_info(self, ex)`: Извлекает полную информацию об исключении, включая имя файла, имя функции и номер строки, где произошло исключение.
*   `log(self, level, message, ex=None, exc_info=False, color: Optional[Tuple[str, str]] = None)`:  Основной метод для логирования сообщений на указанном уровне.
*   `info(self, message, ex=None, exc_info=False, text_color: str = "green", bg_color: str = "")`:  Логирует информационное сообщение.
*   `success(self, message, ex=None, exc_info=False, text_color: str = "yellow", bg_color: str = "")`:  Логирует сообщение об успехе.
*   `warning(self, message, ex=None, exc_info=False, text_color: str = "light_red", bg_color: str = "")`:  Логирует предупреждение.
*   `debug(self, message, ex=None, exc_info=True, text_color: str = "cyan", bg_color: str = "")`:  Логирует отладочное сообщение.
*   `exception(self, message, ex=None, exc_info=True, text_color: str = "cyan", bg_color: str = "light_gray")`:  Логирует сообщение об исключении.
*   `error(self, message, ex=None, exc_info=True, text_color: str = "red", bg_color: str = "")`:  Логирует сообщение об ошибке.
*   `critical(self, message, ex=None, exc_info=True, text_color: str = "red", bg_color: str = "white")`:  Логирует критическую ошибку.

## Переменные

### `TEXT_COLORS`

```python
TEXT_COLORS = {
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
```

Словарь, содержащий соответствия между названиями цветов текста и значениями из модуля `colorama`.

### `BG_COLORS`

```python
BG_COLORS = {
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
```

Словарь, содержащий соответствия между названиями цветов фона и значениями из модуля `colorama`.

### `LOG_SYMBOLS`

```python
LOG_SYMBOLS = {
    logging.INFO: "ℹ️",  # Information
    logging.WARNING: "⚠️",  # Warning
    logging.ERROR: "❌",  # Error
    logging.CRITICAL: "🔥",  # Critical
    logging.DEBUG: "🐛",  # Debug
    "EXCEPTION": "🚨",  # Exception
    "SUCCESS": "✅" # Success
}
```

Словарь, содержащий соответствия между уровнями логирования и символами для их отображения.

### `logger`

```python
logger: Logger = Logger()
```

Экземпляр класса `Logger`, используемый для логирования сообщений.

## Запуск

Этот модуль предназначен для использования в других частях проекта `hypotez`. Для логирования сообщений необходимо импортировать объект `logger` из модуля `src.logger.logger` и использовать его методы (`info`, `debug`, `warning`, `error`, `critical`, `exception`).
```python
from src.logger.logger import logger

logger.info("This is an information message")
logger.error("This is an error message", ex, exc_info=True)