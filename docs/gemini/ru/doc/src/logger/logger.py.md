# Модуль `src.logger.logger`

## Обзор

Модуль предназначен для реализации гибкой системы логирования в проекте `hypotez`. Он предоставляет класс `Logger`, который реализует паттерн Singleton, обеспечивая единую точку доступа к экземпляру логгера. Поддерживается логирование в консоль, файлы (info, debug, errors) и в формате JSON. Модуль использует библиотеку `colorama` для добавления цветов в вывод консоли, что облегчает восприятие сообщений разного уровня важности.

## Подробней

Модуль содержит классы:
- `SingletonMeta`: метакласс для реализации паттерна Singleton.
- `JsonFormatter`: класс для форматирования логов в JSON формат.
- `Logger`: класс, реализующий Singleton паттерн и предоставляющий методы для логирования сообщений разного уровня (info, debug, warning, error, critical) с поддержкой цветов и записи в разные файлы.

В модуле определены константы, такие как `TEXT_COLORS`, `BG_COLORS` и `LOG_SYMBOLS`, которые используются для настройки внешнего вида логов.

## Классы

### `SingletonMeta`

**Описание**: Метакласс, реализующий паттерн Singleton. Гарантирует, что у класса будет только один экземпляр.

**Атрибуты**:
- `_instances` (dict): Словарь для хранения экземпляров классов.
- `_lock` (threading.Lock): Блокировка для обеспечения потокобезопасности при создании экземпляра.

**Методы**:
- `__call__(cls, *args, **kwargs)`: Обеспечивает создание только одного экземпляра класса.

### `JsonFormatter`

**Описание**: Класс для форматирования записей лога в формат JSON.

**Методы**:
- `format(self, record)`: Форматирует запись лога в JSON.

### `Logger`

**Описание**: Класс, реализующий Singleton паттерн для логирования в консоль, файлы и JSON.

**Атрибуты**:
- `log_files_path` (Path): Путь к директории с файлами логов.
- `info_log_path` (Path): Путь к файлу информационных логов.
- `debug_log_path` (Path): Путь к файлу отладочных логов.
- `errors_log_path` (Path): Путь к файлу логов ошибок.
- `json_log_path` (Path): Путь к файлу JSON логов.
- `logger_console` (logging.Logger): Логгер для вывода в консоль.
- `logger_file_info` (logging.Logger): Логгер для записи информационных сообщений в файл.
- `logger_file_debug` (logging.Logger): Логгер для записи отладочных сообщений в файл.
- `logger_file_errors` (logging.Logger): Логгер для записи сообщений об ошибках в файл.
- `logger_file_json` (logging.Logger): Логгер для записи сообщений в JSON файл.

**Методы**:
- `__init__(self, info_log_path: Optional[str] = None, debug_log_path: Optional[str] = None, errors_log_path: Optional[str] = None, json_log_path: Optional[str] = None)`: Инициализирует экземпляр логгера, настраивает пути к файлам логов и создает необходимые логгеры.
- `_format_message(self, message, ex=None, color: Optional[Tuple[str, str]] = None, level=None)`: Форматирует сообщение лога с учетом уровня важности, цвета и информации об исключении.
- `_ex_full_info(self, ex)`: Возвращает полную информацию об исключении, включая имя файла, функцию и номер строки, где произошло исключение.
- `log(self, level, message, ex=None, exc_info=False, color: Optional[Tuple[str, str]] = None)`: Общий метод для записи сообщений в лог с указанным уровнем важности и цветом.
- `info(self, message, ex=None, exc_info=False, text_color: str = "green", bg_color: str = "")`: Записывает информационное сообщение в лог.
- `success(self, message, ex=None, exc_info=False, text_color: str = "yellow", bg_color: str = "")`: Записывает сообщение об успехе в лог.
- `warning(self, message, ex=None, exc_info=False, text_color: str = "light_red", bg_color: str = "")`: Записывает предупреждение в лог.
- `debug(self, message, ex=None, exc_info=True, text_color: str = "cyan", bg_color: str = "")`: Записывает отладочное сообщение в лог.
- `exception(self, message, ex=None, exc_info=True, text_color: str = "cyan", bg_color: str = "light_gray")`: Записывает сообщение об исключении в лог.
- `error(self, message, ex=None, exc_info=True, text_color: str = "red", bg_color: str = "")`: Записывает сообщение об ошибке в лог.
- `critical(self, message, ex=None, exc_info=True, text_color: str = "red", bg_color: str = "white")`: Записывает критическое сообщение в лог.

## Методы класса

### `__init__`

```python
def __init__(
    self,
    info_log_path: Optional[str] = None,
    debug_log_path: Optional[str] = None,
    errors_log_path: Optional[str] = None,
    json_log_path: Optional[str] = None,
):
    """Инициализирует экземпляр логгера."""
    ...
```

**Назначение**: Инициализирует объект `Logger`.

**Параметры**:
- `info_log_path` (Optional[str], optional): Имя файла для информационных логов. По умолчанию `info.log`.
- `debug_log_path` (Optional[str], optional): Имя файла для отладочных логов. По умолчанию `debug.log`.
- `errors_log_path` (Optional[str], optional): Имя файла для логов ошибок. По умолчанию `errors.log`.
- `json_log_path` (Optional[str], optional): Имя файла для JSON логов. По умолчанию формируется на основе текущей даты и времени.

**Как работает функция**:
- Определяет пути к файлам логов на основе переданных параметров и конфигурационного файла `config.json`.
- Создает директории для хранения логов, если они не существуют.
- Создает файлы логов, если они не существуют.
- Инициализирует логгеры для консоли и файлов, устанавливает уровни логирования и форматтеры.
- Удаляет обработчики, выводящие в консоль, для JSON-логгера.

**Примеры**:
```python
from src.logger.logger import Logger
# Инициализация логгера с параметрами по умолчанию
logger = Logger()

# Инициализация логгера с указанием имен файлов
logger = Logger(info_log_path='my_info.log', debug_log_path='my_debug.log', errors_log_path='my_errors.log', json_log_path='my_log.json')
```

### `_format_message`

```python
def _format_message(self, message, ex=None, color: Optional[Tuple[str, str]] = None, level=None):
    """Возвращает отформатированное сообщение с опциональным цветом и информацией об исключении."""
    ...
```

**Назначение**: Форматирует сообщение для логирования, добавляя символы, цвета и информацию об исключении.

**Параметры**:
- `message` (str): Текст сообщения.
- `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
- `color` (Optional[Tuple[str, str]], optional): Кортеж, содержащий цвет текста и фона. По умолчанию `None`.
- `level` (int, optional): Уровень логирования. По умолчанию `None`.

**Возвращает**:
- `str`: Отформатированное сообщение.

**Как работает функция**:
- Получает символ лога на основе уровня логирования.
- Применяет цвета к сообщению, если они указаны.
- Добавляет информацию об исключении к сообщению.

**Примеры**:
```python
from src.logger.logger import Logger
logger = Logger()
formatted_message = logger._format_message('Test message', level=logging.INFO)
print(formatted_message)
```

### `_ex_full_info`

```python
def _ex_full_info(self, ex):
    """Возвращает полную информацию об исключении вместе с деталями о предыдущей функции, файле и строке."""
    ...
```

**Назначение**: Извлекает и форматирует полную информацию об исключении, включая имя файла, имя функции и номер строки, где произошло исключение.

**Параметры**:
- `ex` (Exception): Объект исключения.

**Возвращает**:
- `str`: Строка с полной информацией об исключении.

**Как работает функция**:
- Получает информацию о кадре стека вызовов.
- Извлекает имя файла, имя функции и номер строки.
- Форматирует информацию об исключении в строку.

**Примеры**:
```python
from src.logger.logger import Logger
logger = Logger()
try:
    raise ValueError('Test exception')
except ValueError as ex:
    full_info = logger._ex_full_info(ex)
    print(full_info)
```

### `log`

```python
def log(self, level, message, ex=None, exc_info=False, color: Optional[Tuple[str, str]] = None):
    """Общий метод для записи сообщений в лог с указанным уровнем важности и опциональным цветом."""
    ...
```

**Назначение**: Записывает сообщение в лог с указанным уровнем важности, информацией об исключении и цветом.

**Параметры**:
- `level` (int): Уровень логирования (например, `logging.INFO`, `logging.ERROR`).
- `message` (str): Текст сообщения.
- `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
- `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `False`.
- `color` (Optional[Tuple[str, str]], optional): Кортеж, содержащий цвет текста и фона. По умолчанию `None`.

**Как работает функция**:
- Форматирует сообщение с помощью метода `_format_message`.
- Записывает сообщение в консоль и в файл(ы) в зависимости от уровня логирования.

**Примеры**:
```python
from src.logger.logger import Logger
import logging
logger = Logger()
logger.log(logging.INFO, 'Test message')
```

### `info`

```python
def info(self, message, ex=None, exc_info=False, text_color: str = "green", bg_color: str = ""):
    """Записывает информационное сообщение в лог с опциональным цветом текста и фона."""
    ...
```

**Назначение**: Записывает информационное сообщение в лог с возможностью указания цвета текста и фона.

**Параметры**:
- `message` (str): Текст сообщения.
- `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
- `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `False`.
- `text_color` (str, optional): Цвет текста. По умолчанию `"green"`.
- `bg_color` (str, optional): Цвет фона. По умолчанию `""`.

**Как работает функция**:
- Вызывает метод `log` с уровнем `logging.INFO` и переданными параметрами.

**Примеры**:
```python
from src.logger.logger import Logger
logger = Logger()
logger.info('Test info message')
```

### `success`

```python
def success(self, message, ex=None, exc_info=False, text_color: str = "yellow", bg_color: str = ""):
    """Записывает сообщение об успехе в лог с опциональным цветом текста и фона."""
    ...
```

**Назначение**: Записывает сообщение об успешном выполнении операции в лог.

**Параметры**:
- `message` (str): Текст сообщения.
- `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
- `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `False`.
- `text_color` (str, optional): Цвет текста. По умолчанию `"yellow"`.
- `bg_color` (str, optional): Цвет фона. По умолчанию `""`.

**Как работает функция**:
- Вызывает метод `log` с уровнем `logging.INFO` и переданными параметрами.

**Примеры**:
```python
from src.logger.logger import Logger
logger = Logger()
logger.success('Operation completed successfully')
```

### `warning`

```python
def warning(self, message, ex=None, exc_info=False, text_color: str = "light_red", bg_color: str = ""):
    """Записывает предупреждение в лог с опциональным цветом текста и фона."""
    ...
```

**Назначение**: Записывает предупреждение в лог с возможностью указания цвета текста и фона.

**Параметры**:
- `message` (str): Текст сообщения.
- `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
- `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `False`.
- `text_color` (str, optional): Цвет текста. По умолчанию `"light_red"`.
- `bg_color` (str, optional): Цвет фона. По умолчанию `""`.

**Как работает функция**:
- Вызывает метод `log` с уровнем `logging.WARNING` и переданными параметрами.

**Примеры**:
```python
from src.logger.logger import Logger
logger = Logger()
logger.warning('This is a warning message')
```

### `debug`

```python
def debug(self, message, ex=None, exc_info=True, text_color: str = "cyan", bg_color: str = ""):
    """Записывает отладочное сообщение в лог с опциональным цветом текста и фона."""
    ...
```

**Назначение**: Записывает отладочное сообщение в лог с возможностью указания цвета текста и фона.

**Параметры**:
- `message` (str): Текст сообщения.
- `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
- `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `True`.
- `text_color` (str, optional): Цвет текста. По умолчанию `"cyan"`.
- `bg_color` (str, optional): Цвет фона. По умолчанию `""`.

**Как работает функция**:
- Вызывает метод `log` с уровнем `logging.DEBUG` и переданными параметрами.

**Примеры**:
```python
from src.logger.logger import Logger
logger = Logger()
logger.debug('This is a debug message')
```

### `exception`

```python
def exception(self, message, ex=None, exc_info=True, text_color: str = "cyan", bg_color: str = "light_gray"):
    """Записывает сообщение об исключении в лог с опциональным цветом текста и фона."""
    ...
```

**Назначение**: Записывает сообщение об исключении в лог, используя уровень `logging.ERROR`.

**Параметры**:
- `message` (str): Текст сообщения.
- `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
- `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `True`.
- `text_color` (str, optional): Цвет текста. По умолчанию `"cyan"`.
- `bg_color` (str, optional): Цвет фона. По умолчанию `"light_gray"`.

**Как работает функция**:
- Вызывает метод `log` с уровнем `logging.ERROR` и переданными параметрами.

**Примеры**:
```python
from src.logger.logger import Logger
logger = Logger()
try:
    raise ValueError('Test exception')
except ValueError as ex:
    logger.exception('An exception occurred', ex=ex)
```

### `error`

```python
def error(self, message, ex=None, exc_info=True, text_color: str = "red", bg_color: str = ""):
    """Записывает сообщение об ошибке в лог с опциональным цветом текста и фона."""
    ...
```

**Назначение**: Записывает сообщение об ошибке в лог с возможностью указания цвета текста и фона.

**Параметры**:
- `message` (str): Текст сообщения.
- `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
- `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `True`.
- `text_color` (str, optional): Цвет текста. По умолчанию `"red"`.
- `bg_color` (str, optional): Цвет фона. По умолчанию `""`.

**Как работает функция**:
- Вызывает метод `log` с уровнем `logging.ERROR` и переданными параметрами.

**Примеры**:
```python
from src.logger.logger import Logger
logger = Logger()
logger.error('This is an error message')
```

### `critical`

```python
def critical(self, message, ex=None, exc_info=True, text_color: str = "red", bg_color: str = "white"):
    """Записывает критическое сообщение в лог с опциональным цветом текста и фона."""
    ...
```

**Назначение**: Записывает критическое сообщение в лог с возможностью указания цвета текста и фона.

**Параметры**:
- `message` (str): Текст сообщения.
- `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
- `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `True`.
- `text_color` (str, optional): Цвет текста. По умолчанию `"red"`.
- `bg_color` (str, optional): Цвет фона. По умолчанию `"white"`.

**Как работает функция**:
- Вызывает метод `log` с уровнем `logging.CRITICAL` и переданными параметрами.

**Примеры**:
```python
from src.logger.logger import Logger
logger = Logger()
logger.critical('This is a critical message')
```

## Параметры класса

- `info_log_path` (str): Путь к файлу, в который будут записываться информационные сообщения.
- `debug_log_path` (str): Путь к файлу, в который будут записываться отладочные сообщения.
- `errors_log_path` (str): Путь к файлу, в который будут записываться сообщения об ошибках.
- `json_log_path` (str): Путь к файлу, в который будут записываться логи в формате JSON.

## Примеры

```python
from src.logger.logger import Logger
import logging

# Получение экземпляра логгера
logger = Logger()

# Запись информационного сообщения
logger.info('Application started')

# Запись отладочного сообщения
logger.debug('Variable x = 5')

# Запись сообщения об ошибке с исключением
try:
    result = 1 / 0
except Exception as ex:
    logger.error('Division by zero', ex=ex, exc_info=True)

# Запись критического сообщения
logger.critical('Application is shutting down')