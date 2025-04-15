# Документация для модуля `src.logger`

## Обзор

Модуль `src.logger` предоставляет гибкую систему логирования, поддерживающую логирование в консоль, файлы и JSON. Он использует шаблон проектирования Singleton, чтобы гарантировать, что в приложении используется только один экземпляр логгера. Логгер поддерживает различные уровни логирования (например, `INFO`, `ERROR`, `DEBUG`) и включает цветной вывод для консольных логов. Вы также можете настроить форматы вывода логов и управлять логированием в разные файлы.

## Содержание

- [Классы](#классы)
    - [SingletonMeta](#singletonmeta)
    - [JsonFormatter](#jsonformatter)
    - [Logger](#logger)
- [Функции](#функции)
    - [`__init__`](#__init__)
    - [`_configure_logger`](#_configure_logger)
    - [`initialize_loggers`](#initialize_loggers)
    - [`log`](#log)
    - [`info`](#info)
    - [`success`](#success)
    - [`warning`](#warning)
    - [`debug`](#debug)
    - [`error`](#error)
    - [`critical`](#critical)
- [Параметры для Logger](#параметры-для-logger)
- [Конфигурация файлового логирования (`config`)](#конфигурация-файлового-логирования-config)
- [Примеры использования](#примеры-использования)

## Подробнее

### Классы

#### `SingletonMeta`

**Описание**: Метакласс, реализующий шаблон проектирования Singleton для логгера.

#### `JsonFormatter`

**Описание**: Пользовательский форматтер, который выводит логи в формате JSON.

#### `Logger`

**Описание**: Основной класс логгера, который поддерживает логирование в консоль, файлы и JSON.

**Методы**:

- [`__init__`](#__init__)
- [`_configure_logger`](#_configure_logger)
- [`initialize_loggers`](#initialize_loggers)
- [`log`](#log)
- [`info`](#info)
- [`success`](#success)
- [`warning`](#warning)
- [`debug`](#debug)
- [`error`](#error)
- [`critical`](#critical)

### Функции

#### `__init__`

**Назначение**: Инициализирует экземпляр логгера с заполнителями для различных типов логгеров (консоль, файл и JSON).

#### `_configure_logger`

```python
def _configure_logger(name: str, log_path: str, level: Optional[int] = logging.DEBUG, formatter: Optional[logging.Formatter] = None, mode: Optional[str] = 'a') -> logging.Logger
```

**Назначение**: Настраивает и возвращает экземпляр логгера.

**Параметры**:

- `name` (str): Имя логгера.
- `log_path` (str): Путь к файлу логов.
- `level` (Optional[int], optional): Уровень логирования, например `logging.DEBUG`. По умолчанию `logging.DEBUG`.
- `formatter` (Optional[logging.Formatter], optional): Пользовательский форматтер (необязательно).
- `mode` (Optional[str], optional): Режим файла, например `'a'` для добавления (по умолчанию).

**Возвращает**:

- `logging.Logger`: Настроенный экземпляр `logging.Logger`.

**Как работает функция**:
Функция `_configure_logger` создает и настраивает экземпляр логгера. Она принимает имя логгера, путь к файлу логов, уровень логирования, форматтер и режим файла. Функция создает файловый обработчик (FileHandler), устанавливает форматтер, добавляет обработчик к логгеру и устанавливает уровень логирования. В результате возвращается настроенный экземпляр логгера.

**Пример**:
```python
import logging
from src.logger.logger import Logger

logger = Logger()
log = logger._configure_logger(name='my_logger', log_path='logs/debug.log', level=logging.DEBUG)
logger.debug("debug message")
```

#### `initialize_loggers`

```python
def initialize_loggers(info_log_path: Optional[str] = '', debug_log_path: Optional[str] = '', errors_log_path: Optional[str] = '', json_log_path: Optional[str] = '')
```

**Назначение**: Инициализирует логгеры для консольного и файлового логирования (info, debug, error и JSON).

**Параметры**:

- `info_log_path` (Optional[str], optional): Путь к файлу info логов (необязательно).
- `debug_log_path` (Optional[str], optional): Путь к файлу debug логов (необязательно).
- `errors_log_path` (Optional[str], optional): Путь к файлу error логов (необязательно).
- `json_log_path` (Optional[str], optional): Путь к файлу JSON логов (необязательно).

**Как работает функция**:
Функция `initialize_loggers` инициализирует логгеры для различных уровней (info, debug, error, json). Она использует пути к файлам, переданные в качестве аргументов, для настройки файловых логгеров. Консольный логгер также настраивается. Эта функция гарантирует, что логи будут записываться как в консоль, так и в соответствующие файлы, в зависимости от конфигурации.

**Пример**:

```python
from src.logger.logger import Logger

logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)
```

#### `log`

```python
def log(level, message, ex=None, exc_info=False, color=None)
```

**Назначение**: Регистрирует сообщение на указанном уровне (например, `INFO`, `DEBUG`, `ERROR`) с необязательным исключением и цветовым форматированием.

**Параметры**:

- `level`: Уровень логирования (например, `logging.INFO`, `logging.DEBUG`).
- `message`: Сообщение лога.
- `ex`: Необязательное исключение для логирования.
- `exc_info`: Включать ли информацию об исключении (по умолчанию `False`).
- `color`: Кортеж с цветами текста и фона для вывода в консоль (необязательно).

**Как работает функция**:
Функция `log` является основной функцией для записи логов. Она принимает уровень логирования, сообщение и необязательные параметры, такие как исключение и цвет. Она обрабатывает логирование как в консоль, так и в файлы, используя настроенные логгеры. Если указано исключение, оно также будет зарегистрировано.

**Пример**:
```python
import logging
from src.logger.logger import Logger

logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)
logger.log(logging.INFO, 'This is an info message')
```

#### `info`

```python
def info(message, ex=None, exc_info=False, colors: Optional[tuple] = None)
```

**Назначение**: Регистрирует информационное сообщение.

**Параметры**:

- `message`: Информационное сообщение для логирования.
- `ex`: Необязательное исключение для логирования.
- `exc_info`: Включать ли информацию об исключении (по умолчанию `False`).
- `colors`: Кортеж цветовых значений для сообщения (необязательно).

**Как работает функция**:
Функция `info` вызывает функцию `log` с уровнем логирования `logging.INFO`. Она принимает сообщение, исключение и цвета. Она использует функцию `log` для фактической записи сообщения.

**Пример**:
```python
import logging
from src.logger.logger import Logger

logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)
logger.info('This is an info message')
```

#### `success`

```python
def success(message, ex=None, exc_info=False, colors: Optional[tuple] = None)
```

**Назначение**: Регистрирует сообщение об успехе.

**Параметры**:

- `message`: Сообщение об успехе для логирования.
- `ex`: Необязательное исключение для логирования.
- `exc_info`: Включать ли информацию об исключении (по умолчанию `False`).
- `colors`: Кортеж цветовых значений для сообщения (необязательно).

**Как работает функция**:
Функция `success` вызывает функцию `log` с уровнем логирования `logging.INFO`. Она принимает сообщение, исключение и цвета. Она использует функцию `log` для фактической записи сообщения.

**Пример**:

```python
import logging
from src.logger.logger import Logger

logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)
logger.success('This is a success message')
```

#### `warning`

```python
def warning(message, ex=None, exc_info=False, colors: Optional[tuple] = None)
```

**Назначение**: Регистрирует сообщение предупреждения.

**Параметры**:

- `message`: Сообщение предупреждения для логирования.
- `ex`: Необязательное исключение для логирования.
- `exc_info`: Включать ли информацию об исключении (по умолчанию `False`).
- `colors`: Кортеж цветовых значений для сообщения (необязательно).

**Как работает функция**:
Функция `warning` вызывает функцию `log` с уровнем логирования `logging.WARNING`. Она принимает сообщение, исключение и цвета. Она использует функцию `log` для фактической записи сообщения.

**Пример**:
```python
import logging
from src.logger.logger import Logger

logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)
logger.warning('This is a warning message')
```

#### `debug`

```python
def debug(message, ex=None, exc_info=True, colors: Optional[tuple] = None)
```

**Назначение**: Регистрирует сообщение отладки.

**Параметры**:

- `message`: Сообщение отладки для логирования.
- `ex`: Необязательное исключение для логирования.
- `exc_info`: Включать ли информацию об исключении (по умолчанию `True`).
- `colors`: Кортеж цветовых значений для сообщения (необязательно).

**Как работает функция**:
Функция `debug` вызывает функцию `log` с уровнем логирования `logging.DEBUG`. Она принимает сообщение, исключение и цвета. Она использует функцию `log` для фактической записи сообщения.

**Пример**:
```python
import logging
from src.logger.logger import Logger

logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)
logger.debug('This is a debug message')
```

#### `error`

```python
def error(message, ex=None, exc_info=True, colors: Optional[tuple] = None)
```

**Назначение**: Регистрирует сообщение об ошибке.

**Параметры**:

- `message`: Сообщение об ошибке для логирования.
- `ex`: Необязательное исключение для логирования.
- `exc_info`: Включать ли информацию об исключении (по умолчанию `True`).
- `colors`: Кортеж цветовых значений для сообщения (необязательно).

**Как работает функция**:
Функция `error` вызывает функцию `log` с уровнем логирования `logging.ERROR`. Она принимает сообщение, исключение и цвета. Она использует функцию `log` для фактической записи сообщения.

**Пример**:
```python
import logging
from src.logger.logger import Logger

logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)
logger.error('This is an error message')
```

#### `critical`

```python
def critical(message, ex=None, exc_info=True, colors: Optional[tuple] = None)
```

**Назначение**: Регистрирует критическое сообщение.

**Параметры**:

- `message`: Критическое сообщение для логирования.
- `ex`: Необязательное исключение для логирования.
- `exc_info`: Включать ли информацию об исключении (по умолчанию `True`).
- `colors`: Кортеж цветовых значений для сообщения (необязательно).

**Как работает функция**:
Функция `critical` вызывает функцию `log` с уровнем логирования `logging.CRITICAL`. Она принимает сообщение, исключение и цвета. Она использует функцию `log` для фактической записи сообщения.

**Пример**:
```python
import logging
from src.logger.logger import Logger

logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)
logger.critical('This is a critical message')
```

### Параметры для Logger

Класс `Logger` принимает несколько необязательных параметров для настройки поведения логирования.

- **Level**: Управляет серьезностью захватываемых логов. Общие уровни включают:
  - `logging.DEBUG`: Подробная информация, полезная для диагностики проблем.
  - `logging.INFO`: Общая информация, например, об успешных операциях.
  - `logging.WARNING`: Предупреждения, которые не обязательно требуют немедленных действий.
  - `logging.ERROR`: Сообщения об ошибках.
  - `logging.CRITICAL`: Критические ошибки, которые требуют немедленного внимания.

- **Formatter**: Определяет, как форматируются сообщения лога. По умолчанию сообщения форматируются как `'%(asctime)s - %(levelname)s - %(message)s'`. Вы можете предоставить пользовательский форматтер для разных форматов, например JSON.

- **Color**: Цвета для сообщений лога в консоли. Цвета указываются в виде кортежа с двумя элементами:
  - **Text color**: Указывает цвет текста (например, `colorama.Fore.RED`).
  - **Background color**: Указывает цвет фона (например, `colorama.Back.WHITE`).

Цвет можно настроить для разных уровней логов (например, зеленый для info, красный для errors и т. д.).

### Конфигурация файлового логирования (`config`)

Чтобы записывать сообщения в файл, вы можете указать пути к файлам в конфигурации.

```python
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
```

Пути к файлам, указанные в `config`, используются для записи логов в соответствующие файлы для каждого уровня лога.

### Примеры использования

#### 1. Инициализация Logger:

```python
from src.logger.logger import Logger

logger: Logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)
```

#### 2. Логирование сообщений на разных уровнях:

```python
import logging
from src.logger.logger import Logger

logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)
logger.info('This is an info message')
logger.success('This is a success message')
logger.warning('This is a warning message')
logger.debug('This is a debug message')
logger.error('This is an error message')
logger.critical('This is a critical message')
```

#### 3. Настройка цветов:

```python
import logging
import colorama
from src.logger.logger import Logger

logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)
logger.info('This message will be green', colors=(colorama.Fore.GREEN, colorama.Back.BLACK))
logger.error('This message will have a red background', colors=(colorama.Fore.WHITE, colorama.Back.RED))
```

Этот модуль предоставляет комплексную и гибкую систему логирования для Python-приложений. Вы можете настроить консольное и файловое логирование с различными форматами и цветами, управлять уровнями логирования и корректно обрабатывать исключения. Конфигурация для файлового логирования хранится в словаре `config`, что обеспечивает простую настройку.