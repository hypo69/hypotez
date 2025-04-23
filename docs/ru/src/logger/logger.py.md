# Модуль логгера

## Обзор

Модуль предоставляет функциональность для логирования сообщений различных уровней (INFO, DEBUG, WARNING, ERROR, CRITICAL) в консоль и файлы. Реализован с использованием паттерна Singleton, что гарантирует существование только одного экземпляра логгера в приложении. Поддерживает форматирование сообщений с использованием цветов, а также запись в формате JSON.

## Подробней

Модуль предназначен для централизованного логирования событий в приложении. Он позволяет записывать сообщения в файлы различных уровней (информационные, отладочные, ошибки и критические) и в консоль с возможностью цветового выделения. Использование паттерна Singleton обеспечивает единую точку доступа к логгеру из любой части приложения.

## Содержание

1.  [Классы](#классы)
    *   [SingletonMeta](#singletonmeta)
    *   [JsonFormatter](#jsonformatter)
    *   [Logger](#logger)
2.  [Переменные](#переменные)
    *   [TEXT_COLORS](#text_colors)
    *   [BG_COLORS](#bg_colors)
    *   [LOG_SYMBOLS](#log_symbols)

## Переменные

### `TEXT_COLORS`

Словарь, содержащий ANSI escape-коды для различных цветов текста, используемых при форматировании сообщений логгера.

### `BG_COLORS`

Словарь, содержащий ANSI escape-коды для различных цветов фона, используемых при форматировании сообщений логгера.

### `LOG_SYMBOLS`

Словарь, содержащий символы, соответствующие различным уровням логирования (INFO, WARNING, ERROR, CRITICAL, DEBUG, EXCEPTION, SUCCESS).

## Классы

### `SingletonMeta`

**Описание**: Метакласс, реализующий паттерн Singleton.

**Принцип работы**:
Гарантирует, что у класса будет только один экземпляр. При первом вызове класса создается его экземпляр, который сохраняется в словаре `_instances`. При последующих вызовах возвращается сохраненный экземпляр. Для обеспечения потокобезопасности используется блокировка `_lock`.

### `JsonFormatter`

**Описание**: Пользовательский форматтер для логирования в формате JSON.

**Наследует**:
`logging.Formatter`

**Методы**:

*   `format(self, record)`: Форматирует запись лога в JSON.

### `Logger`

**Описание**: Класс логгера, реализующий паттерн Singleton и поддерживающий логирование в консоль, файлы и JSON.

**Наследует**:
Реализует паттерн Singleton через метакласс `SingletonMeta`.

**Атрибуты**:

*   `log_files_path` (Path): Путь к директории с файлами логов.
*   `info_log_path` (Path): Путь к файлу с информационными логами.
*   `debug_log_path` (Path): Путь к файлу с отладочными логами.
*   `errors_log_path` (Path): Путь к файлу с логами ошибок.
*   `json_log_path` (Path): Путь к файлу с логами в формате JSON.
*   `logger_console` (logging.Logger): Объект логгера для вывода в консоль.
*   `logger_file_info` (logging.Logger): Объект логгера для записи информационных сообщений в файл.
*   `logger_file_debug` (logging.Logger): Объект логгера для записи отладочных сообщений в файл.
*   `logger_file_errors` (logging.Logger): Объект логгера для записи сообщений об ошибках в файл.
*   `logger_file_json` (logging.Logger): Объект логгера для записи сообщений в формате JSON в файл.

**Методы**:

*   `__init__(self, info_log_path: Optional[str] = None, debug_log_path: Optional[str] = None, errors_log_path: Optional[str] = None, json_log_path: Optional[str] = None)`: Инициализирует экземпляр логгера.
*   `_format_message(self, message, ex=None, color: Optional[Tuple[str, str]] = None, level=None)`: Форматирует сообщение с учетом уровня логирования, цвета и информации об исключении.
*   `_ex_full_info(self, ex)`: Возвращает полную информацию об исключении, включая имя файла, функцию и номер строки, где произошло исключение.
*   `log(self, level, message, ex=None, exc_info=False, color: Optional[Tuple[str, str]] = None)`: Общий метод для логирования сообщений на указанном уровне с возможностью указания цвета.
*   `info(self, message, ex=None, exc_info=False, text_color: str = "green", bg_color: str = "")`: Логирует информационное сообщение с возможностью указания цвета текста и фона.
*   `success(self, message, ex=None, exc_info=False, text_color: str = "yellow", bg_color: str = "")`: Логирует сообщение об успехе с возможностью указания цвета текста и фона.
*   `warning(self, message, ex=None, exc_info=False, text_color: str = "light_red", bg_color: str = "")`: Логирует предупреждающее сообщение с возможностью указания цвета текста и фона.
*   `debug(self, message, ex=None, exc_info=True, text_color: str = "cyan", bg_color: str = "")`: Логирует отладочное сообщение с возможностью указания цвета текста и фона.
*   `exception(self, message, ex=None, exc_info=True, text_color: str = "cyan", bg_color: str = "light_gray")`: Логирует сообщение об исключении с возможностью указания цвета текста и фона.
*   `error(self, message, ex=None, exc_info=True, text_color: str = "red", bg_color: str = "")`: Логирует сообщение об ошибке с возможностью указания цвета текста и фона.
*   `critical(self, message, ex=None, exc_info=True, text_color: str = "red", bg_color: str = "white")`: Логирует критическое сообщение с возможностью указания цвета текста и фона.

### `__init__(self, info_log_path: Optional[str] = None, debug_log_path: Optional[str] = None, errors_log_path: Optional[str] = None, json_log_path: Optional[str] = None)`

**Назначение**: Инициализирует экземпляр логгера, настраивает пути к файлам логов и обработчики логирования.

**Параметры**:

*   `info_log_path` (Optional[str], optional): Путь к файлу для информационных логов. По умолчанию `None`.
*   `debug_log_path` (Optional[str], optional): Путь к файлу для отладочных логов. По умолчанию `None`.
*   `errors_log_path` (Optional[str], optional): Путь к файлу для логов ошибок. По умолчанию `None`.
*   `json_log_path` (Optional[str], optional): Путь к файлу для логов в формате JSON. По умолчанию `None`.

**Как работает функция**:

1.  Определяет пути к файлам логов на основе переданных параметров и конфигурационного файла `config.json`.
2.  Создает необходимые директории для хранения файлов логов, если они не существуют.
3.  Создает файлы логов, если они не существуют.
4.  Инициализирует объекты логгеров для консоли и файлов, устанавливает уровни логирования и форматтеры.
5.  Добавляет обработчики логирования для записи сообщений в файлы.
6.  Удаляет все обработчики, которые выводят в консоль для `logger_file_json`.

### `_format_message(self, message, ex:Optional[Exception] = None, color: Optional[Tuple[str, str]] = None, level=None)`

**Назначение**: Форматирует сообщение для логирования, добавляя символ уровня логирования, цвет и информацию об исключении (если оно есть).

**Параметры**:

*   `message` (str): Сообщение для логирования.
*   `ex` (Exception, optional): Объект исключения. По умолчанию `None`.
*   `color` (Optional[Tuple[str, str]], optional): Кортеж, содержащий цвет текста и фона. По умолчанию `None`.
*   `level` (int, optional): Уровень логирования. По умолчанию `None`.

**Возвращает**:

*   str: Форматированное сообщение для логирования.

**Как работает функция**:

1.  Определяет символ уровня логирования из словаря `LOG_SYMBOLS`.
2.  Если указан цвет, применяет ANSI escape-коды для установки цвета текста и фона.
3.  Формирует сообщение, добавляя символ уровня логирования, цвет (если указан) и информацию об исключении (если оно есть).

### `_ex_full_info(self, ex)`

**Назначение**: Возвращает полную информацию об исключении, включая имя файла, функцию и номер строки, где произошло исключение.

**Параметры**:

*   `ex` (Exception): Объект исключения.

**Возвращает**:

*   str: Полная информация об исключении.

**Как работает функция**:

1.  Извлекает информацию о кадре стека вызовов, где произошло исключение.
2.  Формирует строку, содержащую имя файла, имя функции и номер строки.
3.  Возвращает строку с полной информацией об исключении.

### `log(self, level, message, ex:Optional[Exception] = None, exc_info=False, color: Optional[Tuple[str, str]] = None)`

**Назначение**: Общий метод для логирования сообщений на указанном уровне с возможностью указания цвета и информации об исключении.

**Параметры**:

*   `level` (int): Уровень логирования (например, `logging.INFO`, `logging.ERROR`).
*   `message` (str): Сообщение для логирования.
*   `ex` (Exception, optional): Объект исключения. По умолчанию `None`.
*   `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `False`.
*   `color` (Optional[Tuple[str, str]], optional): Кортеж, содержащий цвет текста и фона. По умолчанию `None`.

**Как работает функция**:

1.  Форматирует сообщение с помощью метода `_format_message`.
2.  Логирует сообщение в консоль и файлы с использованием соответствующих объектов логгеров.

### `info(self, message, ex:Optional[Exception] = None, exc_info=False, text_color: str = "green", bg_color: str = "")`

**Назначение**: Логирует информационное сообщение с возможностью указания цвета текста и фона.

**Параметры**:

*   `message` (str): Сообщение для логирования.
*   `ex` (Exception, optional): Объект исключения. По умолчанию `None`.
*   `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `False`.
*   `text_color` (str, optional): Цвет текста. По умолчанию "green".
*   `bg_color` (str, optional): Цвет фона. По умолчанию "".

**Как работает функция**:

1.  Вызывает метод `log` с уровнем `logging.INFO` и указанными цветами.

### `success(self, message, ex:Optional[Exception] = None, exc_info=False, text_color: str = "yellow", bg_color: str = "")`

**Назначение**: Логирует сообщение об успехе с возможностью указания цвета текста и фона.

**Параметры**:

*   `message` (str): Сообщение для логирования.
*   `ex` (Exception, optional): Объект исключения. По умолчанию `None`.
*   `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `False`.
*   `text_color` (str, optional): Цвет текста. По умолчанию "yellow".
*   `bg_color` (str, optional): Цвет фона. По умолчанию "".

**Как работает функция**:

1.  Вызывает метод `log` с уровнем `logging.INFO` и указанными цветами.

### `warning(self, message, ex:Optional[Exception] = None, exc_info=False, text_color: str = "light_red", bg_color: str = "")`

**Назначение**: Логирует предупреждающее сообщение с возможностью указания цвета текста и фона.

**Параметры**:

*   `message` (str): Сообщение для логирования.
*   `ex` (Exception, optional): Объект исключения. По умолчанию `None`.
*   `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `False`.
*   `text_color` (str, optional): Цвет текста. По умолчанию "light_red".
*   `bg_color` (str, optional): Цвет фона. По умолчанию "".

**Как работает функция**:

1.  Вызывает метод `log` с уровнем `logging.WARNING` и указанными цветами.

### `debug(self, message, ex:Optional[Exception] = None, exc_info=True, text_color: str = "cyan", bg_color: str = "")`

**Назначение**: Логирует отладочное сообщение с возможностью указания цвета текста и фона.

**Параметры**:

*   `message` (str): Сообщение для логирования.
*   `ex` (Exception, optional): Объект исключения. По умолчанию `None`.
*   `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `True`.
*   `text_color` (str, optional): Цвет текста. По умолчанию "cyan".
*   `bg_color` (str, optional): Цвет фона. По умолчанию "".

**Как работает функция**:

1.  Вызывает метод `log` с уровнем `logging.DEBUG` и указанными цветами.

### `exception(self, message, ex:Optional[Exception] = None, exc_info=True, text_color: str = "cyan", bg_color: str = "light_gray")`

**Назначение**: Логирует сообщение об исключении с возможностью указания цвета текста и фона.

**Параметры**:

*   `message` (str): Сообщение для логирования.
*   `ex` (Exception, optional): Объект исключения. По умолчанию `None`.
*   `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `True`.
*   `text_color` (str, optional): Цвет текста. По умолчанию "cyan".
*   `bg_color` (str, optional): Цвет фона. По умолчанию "light_gray".

**Как работает функция**:

1.  Вызывает метод `log` с уровнем `logging.ERROR` и указанными цветами.

### `error(self, message, ex:Optional[Exception] = None, exc_info=True, text_color: str = "red", bg_color: str = "")`

**Назначение**: Логирует сообщение об ошибке с возможностью указания цвета текста и фона.

**Параметры**:

*   `message` (str): Сообщение для логирования.
*   `ex` (Exception, optional): Объект исключения. По умолчанию `None`.
*   `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `True`.
*   `text_color` (str, optional): Цвет текста. По умолчанию "red".
*   `bg_color` (str, optional): Цвет фона. По умолчанию "".

**Как работает функция**:

1.  Вызывает метод `log` с уровнем `logging.ERROR` и указанными цветами.

### `critical(self, message, ex:Optional[Exception] = None, exc_info=True, text_color: str = "red", bg_color: str = "white")`

**Назначение**: Логирует критическое сообщение с возможностью указания цвета текста и фона.

**Параметры**:

*   `message` (str): Сообщение для логирования.
*   `ex` (Exception, optional): Объект исключения. По умолчанию `None`.
*   `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `True`.
*   `text_color` (str, optional): Цвет текста. По умолчанию "red".
*   `bg_color` (str, optional): Цвет фона. По умолчанию "white".

**Как работает функция**:

1.  Вызывает метод `log` с уровнем `logging.CRITICAL` и указанными цветами.

**Примеры**:

Пример использования логгера:

```python
from src.logger import logger

try:
    result = 1 / 0
except Exception as ex:
    logger.error('Произошла ошибка при делении на ноль', ex, exc_info=True)
```
```python
from src.logger import logger

logger.info('Приложение запущено')
```

```python
from src.logger import logger

logger.warning('Недостаточно памяти')
```

```python
from src.logger import logger

logger.debug('Значение переменной x: %s', x)
```

```python
from src.logger import logger

logger.success('Операция успешно завершена')