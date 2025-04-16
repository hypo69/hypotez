# Модуль логирования (logger.py)

## Обзор

Этот модуль предоставляет класс `Logger`, реализующий паттерн Singleton, для организации логирования в консоль, файлы и в формате JSON.  Он позволяет настраивать пути к файлам логов, уровни логирования и цвета для консольного вывода. Модуль также включает поддержку логирования информации об исключениях, а также форматирование сообщений.

## Подробней

Модуль предназначен для централизованного управления логированием в проекте `hypotez`.  Он обеспечивает гибкую настройку логирования, позволяя разработчикам легко записывать информацию о работе программы в различные источники (консоль, файлы) с разным уровнем детализации. Использование паттерна Singleton гарантирует, что в приложении будет только один экземпляр класса `Logger`, что упрощает управление и координацию логирования.

## Классы

### `SingletonMeta`

**Описание**: Метакласс для реализации паттерна Singleton.

```python
class SingletonMeta(type):
    """Metaclass for Singleton pattern implementation."""
    ...
```

**Атрибуты**:

-   `_instances` (dict): Словарь, хранящий экземпляры классов-синглтонов.
-   `_lock` (threading.Lock): Блокировка для обеспечения потокобезопасности при создании экземпляров.

**Методы**:

-   `__call__(cls, *args, **kwargs)`: Метод, вызываемый при создании экземпляра класса.

#### `__call__`

**Назначение**: Обеспечивает создание только одного экземпляра класса.

```python
def __call__(cls, *args, **kwargs):
    ...
```

**Параметры**:

-   `cls` (type): Класс, для которого создается экземпляр.
-   `*args`: Позиционные аргументы, передаваемые в конструктор класса.
-   `**kwargs`: Именованные аргументы, передаваемые в конструктор класса.

**Как работает функция**:

1.  Проверяет, существует ли уже экземпляр класса в словаре `_instances`.
2.  Если экземпляр не существует, создает его, используя блокировку для обеспечения потокобезопасности.
3.  Возвращает существующий экземпляр класса.

### `JsonFormatter`

**Описание**: Пользовательский форматтер для логирования в формате JSON.

```python
class JsonFormatter(logging.Formatter):
    """Custom formatter for logging in JSON format."""
    ...
```

**Наследует**:

-   `logging.Formatter` (базовый класс для форматтеров логов в Python).

**Методы**:

-   `format(self, record)`: Форматирует запись лога в JSON.

#### `format`

**Назначение**: Форматирует запись лога в JSON.

```python
def format(self, record):
    """Format the log record as JSON."""
    ...
```

**Параметры**:

-   `record` (logging.LogRecord): Запись лога, которую необходимо отформатировать.

**Возвращает**:

-   `str`: Отформатированная строка в формате JSON.

**Как работает функция**:

1.  Создает словарь `log_entry`, содержащий информацию о времени, уровне логирования, сообщении и информации об исключении (если есть).
2.  Преобразует словарь в строку JSON с использованием `json.dumps`, обеспечивая поддержку Unicode и заменяя двойные кавычки на одинарные в сообщении.
3.  Возвращает отформатированную строку JSON.

### `Logger`

**Описание**: Класс для логирования, реализующий паттерн Singleton и поддерживающий логирование в консоль, файлы и в формате JSON.

```python
class Logger(metaclass=SingletonMeta):
    """Logger class implementing Singleton pattern with console, file, and JSON logging."""
    ...
```

**Наследует**:

-   `SingletonMeta` (для реализации паттерна Singleton).

**Атрибуты**:

-   `log_files_path` (Path): Путь к директории, где хранятся файлы логов.
-   `info_log_path` (Path): Путь к файлу для записи информационных сообщений.
-   `debug_log_path` (Path): Путь к файлу для записи отладочных сообщений.
-   `errors_log_path` (Path): Путь к файлу для записи сообщений об ошибках.
-   `json_log_path` (Path): Путь к файлу для записи логов в формате JSON.
-   `logger_console` (logging.Logger): Объект логгера для вывода в консоль.
-   `logger_file_info` (logging.Logger): Объект логгера для записи информационных сообщений в файл.
-   `logger_file_debug` (logging.Logger): Объект логгера для записи отладочных сообщений в файл.
-   `logger_file_errors` (logging.Logger): Объект логгера для записи сообщений об ошибках в файл.
-   `logger_file_json` (logging.Logger): Объект логгера для записи логов в формате JSON в файл.

**Методы**:

-   `__init__(self, info_log_path: Optional[str] = None, debug_log_path: Optional[str] = None, errors_log_path: Optional[str] = None, json_log_path: Optional[str] = None)`: Инициализирует объект `Logger` и настраивает обработчики для логирования в консоль и файлы.
-   `_format_message(self, message, ex=None, color: Optional[Tuple[str, str]] = None, level=None)`: Форматирует сообщение лога с учетом уровня логирования, цвета и информации об исключении.
-   `_ex_full_info(self, ex)`: Возвращает подробную информацию об исключении, включая имя файла, имя функции и номер строки, где произошло исключение.
-   `log(self, level, message, ex=None, exc_info=False, color: Optional[Tuple[str, str]] = None)`: Общий метод для логирования сообщений на указанном уровне с опциональной информацией об исключении и цвете.
-   `info(self, message, ex=None, exc_info=False, text_color: str = "green", bg_color: str = "")`: Логирует информационное сообщение.
-   `success(self, message, ex=None, exc_info=False, text_color: str = "yellow", bg_color: str = "")`: Логирует сообщение об успехе.
-   `warning(self, message, ex=None, exc_info=False, text_color: str = "light_red", bg_color: str = "")`: Логирует сообщение с предупреждением.
-   `debug(self, message, ex=None, exc_info=True, text_color: str = "cyan", bg_color: str = "")`: Логирует отладочное сообщение.
-   `exception(self, message, ex=None, exc_info=True, text_color: str = "cyan", bg_color: str = "light_gray")`: Логирует сообщение об исключении.
-   `error(self, message, ex=None, exc_info=True, text_color: str = "red", bg_color: str = "")`: Логирует сообщение об ошибке.
-   `critical(self, message, ex=None, exc_info=True, text_color: str = "red", bg_color: str = "white")`: Логирует критическое сообщение.

#### `__init__`

**Назначение**: Инициализирует объект `Logger` и настраивает обработчики для логирования в консоль и файлы.

```python
def __init__(
    self,
    info_log_path: Optional[str] = None,
    debug_log_path: Optional[str] = None,
    errors_log_path: Optional[str] = None,
    json_log_path: Optional[str] = None,
):
    """Initialize the Logger instance."""
    ...
```

**Параметры**:

-   `info_log_path` (Optional[str]): Путь к файлу для записи информационных сообщений. По умолчанию `"info.log"`.
-   `debug_log_path` (Optional[str]): Путь к файлу для записи отладочных сообщений. По умолчанию `"debug.log"`.
-   `errors_log_path` (Optional[str]): Путь к файлу для записи сообщений об ошибках. По умолчанию `"errors.log"`.
-   `json_log_path` (Optional[str]): Путь к файлу для записи логов в формате JSON. По умолчанию `"{timestamp}.json"`.

**Как работает функция**:

1.  Определяет пути к файлам логов, используя параметры конструктора и конфигурацию из файла `config.json`.
2.  Создает директории для хранения файлов логов, если они не существуют.
3.  Создает файлы логов, если они не существуют.
4.  Создает объекты логгеров для консоли, файлов (информационных, отладочных, ошибок) и JSON-формата.
5.  Настраивает форматтеры для каждого обработчика логов.
6.  Добавляет обработчики к соответствующим логгерам.

#### `_format_message`

**Назначение**: Форматирует сообщение лога с учетом уровня логирования, цвета и информации об исключении.

```python
def _format_message(self, message, ex=None, color: Optional[Tuple[str, str]] = None, level=None):
    """Returns formatted message with optional color and exception information."""
    ...
```

**Параметры**:

-   `message` (str): Сообщение лога.
-   `ex` (Optional[Exception]): Информация об исключении (если есть). По умолчанию `None`.
-   `color` (Optional[Tuple[str, str]]): Кортеж, содержащий цвет текста и фона (если есть). По умолчанию `None`.
-   `level` (int): Уровень логирования. По умолчанию `None`.

**Возвращает**:

-   `str`: Отформатированное сообщение лога.

**Как работает функция**:

1.  Получает символ лога на основе уровня логирования из словаря `LOG_SYMBOLS`.
2.  Если указаны цвета текста и фона, применяет их к сообщению с использованием `colorama`.
3.  Добавляет к сообщению информацию об исключении (если есть).
4.  Возвращает отформатированное сообщение.

#### `_ex_full_info`

**Назначение**: Возвращает подробную информацию об исключении, включая имя файла, имя функции и номер строки, где произошло исключение.

```python
def _ex_full_info(self, ex):
    """Returns full exception information along with the previous function, file, and line details."""
    ...
```

**Параметры**:

-   `ex` (Exception): Исключение, информацию о котором необходимо получить.

**Возвращает**:

-   `str`: Подробная информация об исключении.

**Как работает функция**:

1.  Использует `inspect.stack()` для получения информации о стеке вызовов.
2.  Извлекает имя файла, имя функции и номер строки из информации о стеке вызовов.
3.  Форматирует информацию об исключении и возвращает ее в виде строки.

#### `log`

**Назначение**: Общий метод для логирования сообщений на указанном уровне с опциональной информацией об исключении и цвете.

```python
def log(self, level, message, ex=None, exc_info=False, color: Optional[Tuple[str, str]] = None):
    """General method to log messages at specified level with optional color."""
    ...
```

**Параметры**:

-   `level` (int): Уровень логирования (например, `logging.INFO`, `logging.ERROR`).
-   `message` (str): Сообщение лога.
-   `ex` (Optional[Exception]): Информация об исключении (если есть). По умолчанию `None`.
-   `exc_info` (bool): Флаг, указывающий, следует ли добавлять информацию об исключении в лог. По умолчанию `False`.
-   `color` (Optional[Tuple[str, str]]): Кортеж, содержащий цвет текста и фона (если есть). По умолчанию `None`.

**Как работает функция**:

1.  Форматирует сообщение лога с использованием метода `_format_message`.
2.  Логирует отформатированное сообщение в консоль с использованием метода `logger_console.log` или `logger_console.exception` (если `exc_info` равно `True` и `ex` не равно `None`).

#### `info`, `success`, `warning`, `debug`, `exception`, `error`, `critical`

**Назначение**: Методы для логирования сообщений с различными уровнями важности и опциональными цветами.

```python
def info(self, message, ex=None, exc_info=False, text_color: str = "green", bg_color: str = ""):
    ...
def success(self, message, ex=None, exc_info=False, text_color: str = "yellow", bg_color: str = ""):
    ...
def warning(self, message, ex=None, exc_info=False, text_color: str = "light_red", bg_color: str = ""):
    ...
def debug(self, message, ex=None, exc_info=True, text_color: str = "cyan", bg_color: str = ""):
    ...
def exception(self, message, ex=None, exc_info=True, text_color: str = "cyan", bg_color: str = "light_gray"):
    ...
def error(self, message, ex=None, exc_info=True, text_color: str = "red", bg_color: str = ""):
    ...
def critical(self, message, ex=None, exc_info=True, text_color: str = "red", bg_color: str = "white"):
    ...
```

**Параметры**:

-   `message` (str): Сообщение лога.
-   `ex` (Optional[Exception]): Информация об исключении (если есть). По умолчанию `None`.
-   `exc_info` (bool): Флаг, указывающий, следует ли добавлять информацию об исключении в лог. По умолчанию `False` (для `info` и `success`) или `True` (для остальных методов).
-   `text_color` (str): Цвет текста. По умолчанию завист от уровня логирования.
-   `bg_color` (str): Цвет фона. По умолчанию пустая строка.

**Как работают функции**:

1.  Каждый метод вызывает метод `log` с соответствующим уровнем логирования и заданными цветами.

## Переменные модуля

-   `TEXT_COLORS` (dict): Словарь, содержащий соответствия между названиями цветов текста и их значениями из библиотеки `colorama`.
-   `BG_COLORS` (dict): Словарь, содержащий соответствия между названиями цветов фона и их значениями из библиотеки `colorama`.
-   `LOG_SYMBOLS` (dict): Словарь, содержащий соответствия между уровнями логирования и символами Unicode, используемыми для их обозначения.
-    `logger: Logger = Logger()`: Инициализация логгера с указанием путей к файлам логирования и их форматов.

## Пример использования

```python
from src.logger.logger import logger

logger.info("Information message")
logger.warning("Warning message", text_color="yellow")
logger.error("Error message", ex=Exception("Some error"))
```

## Взаимосвязи с другими частями проекта

Этот модуль используется во всех частях проекта `hypotez`, где требуется логирование. Он предоставляет централизованный и удобный интерфейс для записи информации о работе приложения, что упрощает отладку и мониторинг.