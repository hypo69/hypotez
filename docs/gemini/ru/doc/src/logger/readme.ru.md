# Документация для модуля `src.logger`

## Обзор

Модуль `src.logger` предоставляет гибкую систему логирования для Python-приложений, поддерживающую логирование в консоль, файлы и в формате JSON. Он использует шаблон проектирования Singleton для обеспечения единственного экземпляра логгера во всем приложении. Логгер поддерживает различные уровни логирования (`INFO`, `ERROR`, `DEBUG`) и включает цветное отображение для вывода в консоль. Также доступны настройки форматов вывода и управление логированием в различные файлы.

## Содержание

1.  [Классы](#Классы)
    *   [SingletonMeta](#SingletonMeta)
    *   [JsonFormatter](#JsonFormatter)
    *   [Logger](#Logger)
2.  [Функции](#Функции)
    *   [\_\_init\_\_](#__init__)
    *   [\_configure\_logger](#_configure_logger)
    *   [initialize\_loggers](#initialize_loggers)
    *   [log](#log)
    *   [info](#info)
    *   [success](#success)
    *   [warning](#warning)
    *   [debug](#debug)
    *   [error](#error)
    *   [critical](#critical)
3.  [Параметры логгера](#Параметры-логгера)
4.  [Конфигурация для логирования в файл (`config`)](#Конфигурация-для-логирования-в-файл-config)
5.  [Примеры использования](#Примеры-использования)

## Подробнее

Модуль `src.logger` разработан для обеспечения централизованного и удобного способа логирования в Python-приложениях. Он позволяет разработчикам легко настраивать, куда и как будут записываться логи, а также предоставляет инструменты для форматирования и цветового выделения сообщений. Использование шаблона Singleton гарантирует, что во всем приложении будет использоваться один и тот же экземпляр логгера, что упрощает управление и согласованность логирования.

## Классы

### `SingletonMeta`

**Описание**: Метакласс, реализующий шаблон Singleton для логгера.

**Принцип работы**:
Метакласс `SingletonMeta` гарантирует, что при создании экземпляра класса, использующего этот метакласс, всегда будет возвращаться один и тот же экземпляр. Это достигается путем хранения экземпляра класса в приватном атрибуте `_instances`. Если экземпляр класса еще не создан, он создается и сохраняется в `_instances`. При последующих попытках создания экземпляра возвращается уже существующий экземпляр.

### `JsonFormatter`

**Описание**: Кастомный форматтер для вывода логов в формате JSON.

**Принцип работы**:
Класс `JsonFormatter` используется для форматирования логов в формате JSON. Он наследуется от `logging.Formatter` и переопределяет метод `format`, чтобы преобразовывать записи логов в JSON-строки. Это позволяет легко записывать структурированные данные логов, которые могут быть полезны для анализа и отладки.

### `Logger`

**Описание**: Основной класс логгера, поддерживающий логирование в консоль, файлы и в формате JSON.

**Принцип работы**:
Класс `Logger` предоставляет методы для логирования сообщений разных уровней (`INFO`, `DEBUG`, `ERROR` и т.д.) в консоль и файлы. Он использует стандартный модуль `logging` Python и расширяет его возможности за счет добавления поддержки цветового выделения в консоли и форматирования в JSON. Логгер инициализируется с плейсхолдерами для различных типов логгеров (консоль, файлы и JSON), которые настраиваются при вызове метода `initialize_loggers`.

**Методы**:

*   `__init__`: Инициализирует экземпляр класса Logger с плейсхолдерами для различных типов логгеров (консоль, файлы и JSON).
*   `_configure_logger(name: str, log_path: str, level: Optional[int] = logging.DEBUG, formatter: Optional[logging.Formatter] = None, mode: Optional[str] = 'a') -> logging.Logger`: Настраивает и возвращает экземпляр логгера.
*   `initialize_loggers(info_log_path: Optional[str] = '', debug_log_path: Optional[str] = '', errors_log_path: Optional[str] = '', json_log_path: Optional[str] = '')`: Инициализирует логгеры для логирования в консоль и файлы (информация, отладка, ошибки и JSON).
*   `log(level, message, ex=None, exc_info=False, color=None)`: Логирует сообщение на указанном уровне с возможным исключением и цветовым форматированием.
*   `info(message: str, colors: Optional[tuple] = None) -> None`: Логирует информационное сообщение.
*   `success(message: str, colors: Optional[tuple] = None) -> None`: Логирует сообщение об успешной операции.
*   `warning(message: str, colors: Optional[tuple] = None) -> None`: Логирует предупреждение.
*   `debug(message: str, colors: Optional[tuple] = None) -> None`: Логирует сообщение для отладки.
*   `error(message: str, ex: Optional[Exception] = None, exc_info: bool = True, colors: Optional[tuple] = None) -> None`: Логирует сообщение об ошибке.
*   `critical(message: str, colors: Optional[tuple] = None) -> None`: Логирует критическое сообщение.

## Функции

### `__init__`

**Назначение**: Инициализирует экземпляр класса Logger с плейсхолдерами для различных типов логгеров (консоль, файлы и JSON).

**Как работает функция**:
Функция `__init__` является конструктором класса `Logger`. Она инициализирует атрибуты экземпляра класса, такие как `console_logger`, `info_file_logger`, `debug_file_logger`, `errors_file_logger` и `json_file_logger`, присваивая им значение `None`. Это необходимо для последующей настройки логгеров с помощью метода `initialize_loggers`.

### `_configure_logger`

```python
def _configure_logger(name: str, log_path: str, level: Optional[int] = logging.DEBUG, formatter: Optional[logging.Formatter] = None, mode: Optional[str] = 'a') -> logging.Logger:
    """
    Настраивает и возвращает экземпляр логгера.

    Args:
        name (str): Имя логгера.
        log_path (str): Путь к файлу логов.
        level (Optional[int], optional): Уровень логирования, например, `logging.DEBUG`. По умолчанию `logging.DEBUG`.
        formatter (Optional[logging.Formatter], optional): Кастомный форматтер (опционально).
        mode (Optional[str], optional): Режим работы с файлом, например, `'a'` для добавления. По умолчанию `'a'`.

    Returns:
        logging.Logger: Настроенный экземпляр `logging.Logger`.
    """
    ...
```

**Назначение**: Настраивает и возвращает экземпляр логгера.

**Параметры**:

*   `name` (str): Имя логгера.
*   `log_path` (str): Путь к файлу логов.
*   `level` (Optional[int], optional): Уровень логирования, например, `logging.DEBUG`. Значение по умолчанию — `logging.DEBUG`.
*   `formatter` (Optional[logging.Formatter], optional): Кастомный форматтер (опционально).
*   `mode` (Optional[str], optional): Режим работы с файлом, например, `'a'` для добавления (значение по умолчанию).

**Возвращает**:

*   `logging.Logger`: Настроенный экземпляр `logging.Logger`.

**Как работает функция**:

1.  **Создание логгера**: Создается экземпляр логгера с указанным именем.
2.  **Настройка уровня логирования**: Устанавливается уровень логирования для логгера.
3.  **Создание обработчика**: Создается обработчик файла (`FileHandler`) для записи логов в указанный файл в заданном режиме.
4.  **Установка форматтера**: Устанавливается форматтер для обработчика. Если форматтер не указан, используется формат по умолчанию.
5.  **Добавление обработчика к логгеру**: Обработчик добавляется к логгеру.
6.  **Возврат логгера**: Возвращается настроенный экземпляр логгера.

**ASCII flowchart**:

```
Создание логгера --> Настройка уровня логирования --> Создание обработчика файла --> Установка форматтера --> Добавление обработчика к логгеру --> Возврат логгера
```

**Примеры**:

```python
import logging
from src.logger.logger import Logger

logger = Logger()
configured_logger = logger._configure_logger(name='my_logger', log_path='logs/my_log.log', level=logging.INFO)
```

### `initialize_loggers`

```python
def initialize_loggers(info_log_path: Optional[str] = '', debug_log_path: Optional[str] = '', errors_log_path: Optional[str] = '', json_log_path: Optional[str] = '') -> None:
    """
    Инициализирует логгеры для логирования в консоль и файлы (информация, отладка, ошибки и JSON).

    Args:
        info_log_path (Optional[str], optional): Путь к файлу логов информации (опционально). По умолчанию ''.
        debug_log_path (Optional[str], optional): Путь к файлу логов отладки (опционально). По умолчанию ''.
        errors_log_path (Optional[str], optional): Путь к файлу логов ошибок (опционально). По умолчанию ''.
        json_log_path (Optional[str], optional): Путь к файлу логов в формате JSON (опционально). По умолчанию ''.
    """
    ...
```

**Назначение**: Инициализирует логгеры для логирования в консоль и файлы (информация, отладка, ошибки и JSON).

**Параметры**:

*   `info_log_path` (Optional[str], optional): Путь к файлу логов информации (опционально). По умолчанию ''.
*   `debug_log_path` (Optional[str], optional): Путь к файлу логов отладки (опционально). По умолчанию ''.
*   `errors_log_path` (Optional[str], optional): Путь к файлу логов ошибок (опционально). По умолчанию ''.
*   `json_log_path` (Optional[str], optional): Путь к файлу логов в формате JSON (опционально). По умолчанию ''.

**Как работает функция**:

1.  **Настройка форматтера**: Создается форматтер для консольного логгера с цветовым оформлением.
2.  **Создание консольного логгера**: Создается консольный логгер и настраивается его уровень логирования и форматтер.
3.  **Инициализация файловых логгеров**: Для каждого из путей к файлам логов (информация, отладка, ошибки и JSON) вызывается функция `_configure_logger` для настройки соответствующего файлового логгера. Если путь не указан, логгер не создается.

**ASCII flowchart**:

```
Настройка форматтера --> Создание консольного логгера --> Инициализация файловых логгеров (info, debug, errors, json)
```

**Примеры**:

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

### `log`

```python
def log(level, message, ex=None, exc_info=False, color=None):
    """
    Логирует сообщение на указанном уровне (например, `INFO`, `DEBUG`, `ERROR`) с возможным исключением и цветовым форматированием.

    Args:
        level: Уровень логирования (например, `logging.INFO`, `logging.DEBUG`).
        message: Логируемое сообщение.
        ex: Исключение для логирования (опционально).
        exc_info: Включать информацию об исключении (значение по умолчанию — `False`).
        color: Кортеж цветов текста и фона для консольного вывода (опционально).
    """
    ...
```

**Назначение**: Логирует сообщение на указанном уровне (например, `INFO`, `DEBUG`, `ERROR`) с возможным исключением и цветовым форматированием.

**Параметры**:

*   `level`: Уровень логирования (например, `logging.INFO`, `logging.DEBUG`).
*   `message`: Логируемое сообщение.
*   `ex`: Исключение для логирования (опционально).
*   `exc_info`: Включать информацию об исключении (значение по умолчанию — `False`).
*   `color`: Кортеж цветов текста и фона для консольного вывода (опционально).

**Как работает функция**:

1.  **Цветовое оформление**: Если указан цвет, применяется цветовое оформление к консольному выводу.
2.  **Логирование в консоль**: Логируется сообщение в консоль с указанным уровнем. Если указано исключение, оно также логируется.
3.  **Логирование в файлы**: В зависимости от уровня логирования сообщение логируется в соответствующие файловые логгеры (информация, отладка, ошибки).

**ASCII flowchart**:

```
Цветовое оформление (если указано) --> Логирование в консоль --> Логирование в файловые логгеры (info, debug, errors)
```

**Примеры**:

```python
import logging
from src.logger.logger import Logger
import colorama

logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)

logger.log(logging.INFO, 'Это информационное сообщение')
logger.log(logging.ERROR, 'Это сообщение об ошибке', ex=Exception('Test error'), exc_info=True)
logger.log(logging.INFO, 'Это сообщение будет зеленым', color=(colorama.Fore.GREEN, colorama.Back.BLACK))
```

### `info`

```python
def info(message: str, colors: Optional[tuple] = None) -> None:
    """
    Логирует информационное сообщение.

    Args:
        message (str): Логируемое сообщение.
        colors (Optional[tuple], optional): Кортеж цветов текста и фона для консольного вывода (опционально). По умолчанию `None`.
    """
    ...
```

**Назначение**: Логирует информационное сообщение.

**Параметры**:

*   `message` (str): Логируемое сообщение.
*   `colors` (Optional[tuple], optional): Кортеж цветов текста и фона для консольного вывода (опционально). По умолчанию `None`.

**Как работает функция**:
Функция `info` вызывает метод `log` с уровнем логирования `logging.INFO` и переданным сообщением и цветами.

**ASCII flowchart**:

```
Вызов метода log(logging.INFO, message, color)
```

**Примеры**:

```python
from src.logger.logger import Logger
import colorama

logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)

logger.info('Это информационное сообщение')
logger.info('Это сообщение будет зеленым', colors=(colorama.Fore.GREEN, colorama.Back.BLACK))
```

### `success`

```python
def success(message: str, colors: Optional[tuple] = None) -> None:
    """
    Логирует сообщение об успешной операции.

    Args:
        message (str): Логируемое сообщение.
        colors (Optional[tuple], optional): Кортеж цветов текста и фона для консольного вывода (опционально). По умолчанию `None`.
    """
    ...
```

**Назначение**: Логирует сообщение об успешной операции.

**Параметры**:

*   `message` (str): Логируемое сообщение.
*   `colors` (Optional[tuple], optional): Кортеж цветов текста и фона для консольного вывода (опционально). По умолчанию `None`.

**Как работает функция**:
Функция `success` вызывает метод `log` с уровнем логирования `logging.INFO` и переданным сообщением и цветами.

**ASCII flowchart**:

```
Вызов метода log(logging.INFO, message, color)
```

**Примеры**:

```python
from src.logger.logger import Logger
import colorama

logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)

logger.success('Операция выполнена успешно')
logger.success('Операция выполнена успешно (зеленым цветом)', colors=(colorama.Fore.GREEN, colorama.Back.BLACK))
```

### `warning`

```python
def warning(message: str, colors: Optional[tuple] = None) -> None:
    """
    Логирует предупреждение.

    Args:
        message (str): Логируемое сообщение.
        colors (Optional[tuple], optional): Кортеж цветов текста и фона для консольного вывода (опционально). По умолчанию `None`.
    """
    ...
```

**Назначение**: Логирует предупреждение.

**Параметры**:

*   `message` (str): Логируемое сообщение.
*   `colors` (Optional[tuple], optional): Кортеж цветов текста и фона для консольного вывода (опционально). По умолчанию `None`.

**Как работает функция**:
Функция `warning` вызывает метод `log` с уровнем логирования `logging.WARNING` и переданным сообщением и цветами.

**ASCII flowchart**:

```
Вызов метода log(logging.WARNING, message, color)
```

**Примеры**:

```python
from src.logger.logger import Logger
import colorama

logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)

logger.warning('Это предупреждение')
logger.warning('Это предупреждение (желтым цветом)', colors=(colorama.Fore.YELLOW, colorama.Back.BLACK))
```

### `debug`

```python
def debug(message: str, colors: Optional[tuple] = None) -> None:
    """
    Логирует сообщение для отладки.

    Args:
        message (str): Логируемое сообщение.
        colors (Optional[tuple], optional): Кортеж цветов текста и фона для консольного вывода (опционально). По умолчанию `None`.
    """
    ...
```

**Назначение**: Логирует сообщение для отладки.

**Параметры**:

*   `message` (str): Логируемое сообщение.
*   `colors` (Optional[tuple], optional): Кортеж цветов текста и фона для консольного вывода (опционально). По умолчанию `None`.

**Как работает функция**:
Функция `debug` вызывает метод `log` с уровнем логирования `logging.DEBUG` и переданным сообщением и цветами.

**ASCII flowchart**:

```
Вызов метода log(logging.DEBUG, message, color)
```

**Примеры**:

```python
from src.logger.logger import Logger
import colorama

logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)

logger.debug('Это сообщение для отладки')
logger.debug('Это сообщение для отладки (синим цветом)', colors=(colorama.Fore.BLUE, colorama.Back.BLACK))
```

### `error`

```python
def error(message: str, ex: Optional[Exception] = None, exc_info: bool = True, colors: Optional[tuple] = None) -> None:
    """
    Логирует сообщение об ошибке.

    Args:
        message (str): Логируемое сообщение.
        ex (Optional[Exception], optional): Исключение для логирования (опционально). По умолчанию `None`.
        exc_info (bool, optional): Включать информацию об исключении (значение по умолчанию — `True`).
        colors (Optional[tuple], optional): Кортеж цветов текста и фона для консольного вывода (опционально). По умолчанию `None`.
    """
    ...
```

**Назначение**: Логирует сообщение об ошибке.

**Параметры**:

*   `message` (str): Логируемое сообщение.
*   `ex` (Optional[Exception], optional): Исключение для логирования (опционально). По умолчанию `None`.
*   `exc_info` (bool, optional): Включать информацию об исключении (значение по умолчанию — `True`).
*   `colors` (Optional[tuple], optional): Кортеж цветов текста и фона для консольного вывода (опционально). По умолчанию `None`.

**Как работает функция**:
Функция `error` вызывает метод `log` с уровнем логирования `logging.ERROR` и переданным сообщением, исключением, информацией об исключении и цветами.

**ASCII flowchart**:

```
Вызов метода log(logging.ERROR, message, ex, exc_info, color)
```

**Примеры**:

```python
from src.logger.logger import Logger
import colorama

logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)

logger.error('Это сообщение об ошибке')
logger.error('Это сообщение об ошибке (красным цветом)', colors=(colorama.Fore.RED, colorama.Back.BLACK))
logger.error('Произошла ошибка', ex=ValueError('Invalid value'))
```

### `critical`

```python
def critical(message: str, colors: Optional[tuple] = None) -> None:
    """
    Логирует критическое сообщение.

    Args:
        message (str): Логируемое сообщение.
        colors (Optional[tuple], optional): Кортеж цветов текста и фона для консольного вывода (опционально). По умолчанию `None`.
    """
    ...
```

**Назначение**: Логирует критическое сообщение.

**Параметры**:

*   `message` (str): Логируемое сообщение.
*   `colors` (Optional[tuple], optional): Кортеж цветов текста и фона для консольного вывода (опционально). По умолчанию `None`.

**Как работает функция**:
Функция `critical` вызывает метод `log` с уровнем логирования `logging.CRITICAL` и переданным сообщением и цветами.

**ASCII flowchart**:

```
Вызов метода log(logging.CRITICAL, message, color)
```

**Примеры**:

```python
from src.logger.logger import Logger
import colorama

logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)

logger.critical('Это критическое сообщение')
logger.critical('Это критическое сообщение (красным цветом)', colors=(colorama.Fore.RED, colorama.Back.BLACK))
```

## Параметры логгера

Класс `Logger` принимает несколько опциональных параметров для настройки поведения логирования.

*   **Уровень**: Контролирует, какие сообщения будут записаны. Основные уровни:
    *   `logging.DEBUG`: Подробная информация для диагностики.
    *   `logging.INFO`: Общая информация, например, успешные операции.
    *   `logging.WARNING`: Предупреждения, не требующие немедленного действия.
    *   `logging.ERROR`: Сообщения об ошибках.
    *   `logging.CRITICAL`: Критические ошибки, требующие немедленного внимания.

*   **Форматтер**: Определяет формат сообщений. По умолчанию используется `'%(asctime)s - %(levelname)s - %(message)s'`. Можно задать кастомный форматтер, например для JSON.

*   **Цвета**: Задают цвет текста и фона в консоли. Цвета указываются кортежем:
    *   **Цвет текста**: Например, `colorama.Fore.RED`.
    *   **Цвет фона**: Например, `colorama.Back.WHITE`.

## Конфигурация для логирования в файл (`config`)

Для записи сообщений в файл можно указать пути в конфигурации.

```python
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
```

## Примеры использования

### 1. Инициализация логгера:

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

### 2. Логирование сообщений:

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

logger.info('Это информационное сообщение')
logger.success('Это сообщение об успешной операции')
logger.warning('Это предупреждение')
logger.debug('Это сообщение для отладки')
logger.error('Это сообщение об ошибке')
logger.critical('Это критическое сообщение')
```

### 3. Настройка цветов:

```python
from src.logger.logger import Logger
import colorama

logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)

logger.info('Это сообщение будет зеленым', colors=(colorama.Fore.GREEN, colorama.Back.BLACK))
logger.error('Это сообщение с красным фоном', colors=(colorama.Fore.WHITE, colorama.Back.RED))
```

Модуль `src.logger` предоставляет полноценную систему логирования для Python-приложений. Вы можете настроить логирование в консоль и файлы с различными форматами и цветами, управлять уровнями логирования и обрабатывать исключения. Конфигурация логирования в файлы задается через словарь `config`, что позволяет легко изменять настройки.