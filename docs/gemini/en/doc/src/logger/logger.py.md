# Модуль логгера

## Обзор

Модуль `src.logger.logger` предоставляет классы и функции для ведения логов в проекте `hypotez`. Он реализует различные типы логгирования: 

- **Логгирование в консоль:**  вывод сообщений в консоль с использованием цветов для различного уровня серьезности сообщений (информация, ошибки, предупреждения и т.д.).
- **Логгирование в файлы:** создание отдельных файлов логов для информационных, отладочных, ошибочных сообщений и JSON-формата логов.
- **Логгирование в JSON:** сохранение логов в формате JSON для облегчения анализа и обработки.

## Подробности

### **Структура файлов**

-   **`src/logger/logger.py`**:  Основной файл модуля, содержащий классы `Logger`, `JsonFormatter` и  `SingletonMeta`.

### **Основные компоненты**

#### Класс `SingletonMeta`

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

**Описание**:  Реализует паттерн "Одиночка" (Singleton) для класса `Logger`.  Гарантирует, что существует только один экземпляр класса `Logger` в приложении.

####  Класс `JsonFormatter`

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

**Описание**:  Определяет пользовательский форматтер для логгирования в формате JSON.

#### Класс `Logger`

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
            message = f"{log_symbol} {text_color}{bg_color}{message} {ex or ''} {colorama.Style.RESET_ALL}"
        else:
            message = f"{log_symbol} {message} {ex or ''}"
        return message

    def _ex_full_info(self, ex):
        """Returns full exception information along with the previous function, file, and line details."""
        frame_info = inspect.stack()[3]
        file_name = frame_info.filename
        function_name = frame_info.function
        line_number = frame_info.lineno

        return f"\nFile: {file_name}, \n | \n  -Function: {function_name}, \n   | \n    --Line: {line_number}\n{ex if ex else ''}"

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

    def exception(self, message, ex=None, exc_info=True, text_color: str = "cyan", bg_color: "light_gray"):
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

**Описание**:  Главный класс, отвечающий за ведение логов. 
-  Реализует паттерн "Одиночка" (Singleton) через метакласс `SingletonMeta`.
-  Создает отдельные экземпляры логгеров для консоли, файлов (информационных, отладочных, ошибочных) и JSON-логов.
-  Определяет методы для записи различных типов сообщений (info, success, warning, debug, exception, error, critical). 
-  В методах используется `_format_message` для форматирования сообщений с цветами и добавления символов, обозначающих уровень серьезности сообщения. 
-  `_ex_full_info` позволяет получить подробную информацию об исключении, включая имя файла, функцию и номер строки, где произошло исключение.

### **Пример использования**

```python
# Initialize logger with file paths
# logger = Logger(info_log_path='info.log', debug_log_path='debug.log', errors_log_path='errors.log', json_log_path='log.json')
logger: Logger = Logger()

# Log some messages
logger.info("Информационное сообщение")
logger.success("Успешное выполнение")
logger.warning("Предупреждение", ex="Ошибка:  нет такой папки")
logger.debug("Отладочное сообщение")
logger.exception("Ошибка с описанием исключения", ex="Ошибка:  неверный формат файла", exc_info=True)
logger.error("Ошибка", ex="Ошибка:  неверные данные", exc_info=True)
logger.critical("Критическая ошибка", ex="Ошибка:  не удалось подключиться к базе данных")

# ... Other parts of the code
```

## Как это работает?

Модуль `src.logger.logger` использует стандартный модуль Python `logging`.  Он  расширяет функциональность стандартного логгирования, предоставляя: 

1.  **Пользовательский форматтер `JsonFormatter`:** для записи логов в формате JSON.
2.  **Класс `Logger`:**  создает экземпляры логгеров для различных каналов (консоль, файлы, JSON) и предоставляет удобные методы для записи сообщений разных уровней. 

## Параметры

-   **`info_log_path` (Optional[str])**:  Путь к файлу для информационных логов.  По умолчанию - "info.log" в директории `log_files_path`.
-   **`debug_log_path` (Optional[str])**:  Путь к файлу для отладочных логов.  По умолчанию - "debug.log" в директории `log_files_path`.
-   **`errors_log_path` (Optional[str])**:  Путь к файлу для ошибок.  По умолчанию - "errors.log" в директории `log_files_path`.
-   **`json_log_path` (Optional[str])**:  Путь к файлу для JSON-логов.  По умолчанию - `timestamp.json`  в директории `log_files_path`.

## Примеры

```python
from src.logger import logger

# Информационное сообщение
logger.info("Загрузка данных из файла")

# Успешное выполнение операции
logger.success("Данные загружены успешно")

# Предупреждение
logger.warning("Неверный формат файла", ex="Ошибка:  неверный формат файла")

# Отладочная информация
logger.debug("Проверка значения переменной x:", x)

# Ошибка
logger.error("Не удалось подключиться к базе данных", ex="Ошибка:  не удалось подключиться к базе данных")

# Критическая ошибка
logger.critical("Серьезная ошибка", ex="Ошибка:  не удалось выполнить критически важные операции")
```