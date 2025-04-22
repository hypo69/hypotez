# Документация модуля `src.logger`

## Обзор

Модуль `src.logger` предоставляет гибкую систему логирования, поддерживающую логирование в консоль, файлы и JSON. Он использует паттерн проектирования Singleton, чтобы гарантировать использование только одного экземпляра логгера во всем приложении. Логгер поддерживает различные уровни логирования (например, `INFO`, `ERROR`, `DEBUG`) и включает цветной вывод для консольных логов. Вы также можете настроить форматы вывода логов и управлять логированием в разные файлы.

## Подробнее

Этот модуль предназначен для упрощения процесса логирования в приложении `hypotez`. Он обеспечивает централизованный механизм для записи сообщений различных уровней важности, что позволяет разработчикам отслеживать состояние приложения, выявлять и устранять ошибки. Использование паттерна Singleton гарантирует, что все компоненты приложения используют один и тот же экземпляр логгера, что упрощает управление и настройку логирования.

## Содержание

1.  [Классы](#классы)
    *   [SingletonMeta](#singletonmeta)
    *   [JsonFormatter](#jsonformatter)
    *   [Logger](#logger)
2.  [Функции](#функции)
    *   [`__init__`](#__init__)
    *   [`_configure_logger`](#_configure_logger)
    *   [`initialize_loggers`](#initialize_loggers)
    *   [`log`](#log)
    *   [`info`](#info)
    *   [`success`](#success)
    *   [`warning`](#warning)
    *   [`debug`](#debug)
    *   [`error`](#error)
    *   [`critical`](#critical)
3.  [Параметры для логгера](#параметры-для-логгера)
4.  [Конфигурация логирования в файлы](#конфигурация-логирования-в-файлы-config)
5.  [Примеры использования](#примеры-использования)

## Классы

### `SingletonMeta`

**Описание**: Метакласс, реализующий паттерн проектирования Singleton для логгера.

**Принцип работы**:

Гарантирует, что у класса будет только один экземпляр. При попытке создать новый экземпляр класса возвращается уже существующий. Это достигается за счет хранения экземпляра класса в приватном атрибуте `_instances`.

### `JsonFormatter`

**Описание**: Пользовательский форматтер, который выводит логи в формате JSON.

### `Logger`

**Описание**: Основной класс логгера, который поддерживает логирование в консоль, файлы и JSON.

**Атрибуты**:

*   `console_logger` (`logging.Logger`): Логгер для вывода в консоль.
*   `file_info_logger` (`logging.Logger`): Логгер для записи информационных сообщений в файл.
*   `file_debug_logger` (`logging.Logger`): Логгер для записи отладочных сообщений в файл.
*   `file_error_logger` (`logging.Logger`): Логгер для записи сообщений об ошибках в файл.
*   `file_json_logger` (`logging.Logger`): Логгер для записи сообщений в формате JSON в файл.

## Функции

### `__init__`

**Описание**: Инициализирует экземпляр логгера с заполнителями для различных типов логгеров (консольного, файлового и JSON).

### `_configure_logger`

```python
def _configure_logger(name: str, log_path: str, level: Optional[int] = logging.DEBUG, formatter: Optional[logging.Formatter] = None, mode: Optional[str] = 'a') -> logging.Logger:
    """Configures and returns a logger instance.
    
    Parameters:
    - `name`: Name of the logger.
    - `log_path`: Path to the log file.
    - `level`: Logging level, e.g., `logging.DEBUG`. Default is `logging.DEBUG`.
    - `formatter`: Custom formatter (optional).
    - `mode`: File mode, e.g., `'a'` for append (default).
    
    Returns: Configured `logging.Logger` instance.
    """
```

**Назначение**: Настраивает и возвращает экземпляр логгера.

**Параметры**:

*   `name` (`str`): Имя логгера.
*   `log_path` (`str`): Путь к файлу журнала.
*   `level` (`Optional[int]`, optional): Уровень логирования, например, `logging.DEBUG`. По умолчанию `logging.DEBUG`.
*   `formatter` (`Optional[logging.Formatter]`, optional): Пользовательский форматтер (необязательно).
*   `mode` (`Optional[str]`, optional): Режим файла, например, `'a'` для добавления (по умолчанию).

**Возвращает**:

*   `logging.Logger`: Настроенный экземпляр `logging.Logger`.

**Как работает функция**:

Функция `_configure_logger` создает и настраивает экземпляр логгера с заданным именем, путем к файлу журнала, уровнем логирования, форматтером и режимом файла. Она создает обработчик файла (`FileHandler`) для записи логов в указанный файл, устанавливает уровень логирования и форматтер для обработчика, а затем добавляет обработчик к логгеру.

### `initialize_loggers`

```python
def initialize_loggers(info_log_path: Optional[str] = '', debug_log_path: Optional[str] = '', errors_log_path: Optional[str] = '', json_log_path: Optional[str] = '')
    """Initializes the loggers for console and file logging (info, debug, error, and JSON).
    
    Parameters:
    - `info_log_path`: Path for info log file (optional).
    - `debug_log_path`: Path for debug log file (optional).
    - `errors_log_path`: Path for error log file (optional).
    - `json_log_path`: Path for JSON log file (optional).
    """
```

**Назначение**: Инициализирует логгеры для консольного и файлового логирования (информационного, отладочного, ошибок и JSON).

**Параметры**:

*   `info_log_path` (`Optional[str]`, optional): Путь к файлу информационных логов (необязательно).
*   `debug_log_path` (`Optional[str]`, optional): Путь к файлу отладочных логов (необязательно).
*   `errors_log_path` (`Optional[str]`, optional): Путь к файлу логов ошибок (необязательно).
*   `json_log_path` (`Optional[str]`, optional): Путь к файлу JSON-логов (необязательно).

**Как работает функция**:

Функция `initialize_loggers` настраивает различные логгеры для записи сообщений в файлы и консоль. Она вызывает функцию `_configure_logger` для создания и настройки каждого логгера, указывая путь к файлу журнала, уровень логирования и форматтер.

### `log`

```python
def log(level, message, ex=None, exc_info=False, color=None)
    """Logs a message at the specified level (e.g., `INFO`, `DEBUG`, `ERROR`) with optional exception and color formatting.
    
    Parameters:
    - `level`: Logging level (e.g., `logging.INFO`, `logging.DEBUG`).
    - `message`: The log message.
    - `ex`: Optional exception to log.
    - `exc_info`: Whether to include exception information (default is `False`).
    - `color`: Tuple with text and background colors for console output (optional).
    """
```

**Назначение**: Регистрирует сообщение на указанном уровне (например, `INFO`, `DEBUG`, `ERROR`) с необязательным исключением и цветовым форматированием.

**Параметры**:

*   `level` (`int`): Уровень логирования (например, `logging.INFO`, `logging.DEBUG`).
*   `message` (`str`): Сообщение журнала.
*   `ex` (`Optional[Exception]`, optional): Необязательное исключение для регистрации.
*   `exc_info` (`bool`, optional): Следует ли включать информацию об исключении (по умолчанию `False`).
*   `color` (`Optional[tuple]`, optional): Кортеж с цветами текста и фона для вывода в консоль (необязательно).

**Как работает функция**:

Функция `log` регистрирует сообщение на указанном уровне логирования. Она выводит сообщение в консоль с использованием цветного форматирования, если указан параметр `color`, и записывает сообщение в соответствующие файлы журналов в зависимости от уровня логирования. Если указано исключение `ex`, оно также будет зарегистрировано вместе с сообщением.

### `info`

```python
def info(message, ex=None, exc_info=False, colors: Optional[tuple] = None)
    """Logs an info message.
    
    Parameters:
    - `message`: The info message to log.
    - `ex`: Optional exception to log.
    - `exc_info`: Whether to include exception info (default is `False`).
    - `colors`: Tuple of color values for the message (optional).
    """
```

**Назначение**: Регистрирует информационное сообщение.

**Параметры**:

*   `message` (`str`): Информационное сообщение для регистрации.
*   `ex` (`Optional[Exception]`, optional): Необязательное исключение для регистрации.
*   `exc_info` (`bool`, optional): Следует ли включать информацию об исключении (по умолчанию `False`).
*   `colors` (`Optional[tuple]`, optional): Кортеж значений цвета для сообщения (необязательно).

**Как работает функция**:

Функция `info` вызывает функцию `log` с уровнем логирования `logging.INFO` для регистрации информационного сообщения.

### `success`

```python
def success(message, ex=None, exc_info=False, colors: Optional[tuple] = None)
    """Logs a success message.
    
    Parameters:
    - Same as `info`.
    """
```

**Назначение**: Регистрирует сообщение об успехе.

**Параметры**:

*   Аналогичны параметрам функции `info`.

**Как работает функция**:

Функция `success` вызывает функцию `log` с уровнем логирования `logging.INFO` для регистрации сообщения об успехе.

### `warning`

```python
def warning(message, ex=None, exc_info=False, colors: Optional[tuple] = None)
    """Logs a warning message.
    
    Parameters:
    - Same as `info`.
    """
```

**Назначение**: Регистрирует предупреждающее сообщение.

**Параметры**:

*   Аналогичны параметрам функции `info`.

**Как работает функция**:

Функция `warning` вызывает функцию `log` с уровнем логирования `logging.WARNING` для регистрации предупреждающего сообщения.

### `debug`

```python
def debug(message, ex=None, exc_info=True, colors: Optional[tuple] = None)
    """Logs a debug message.
    
    Parameters:
    - Same as `info`.
    """
```

**Назначение**: Регистрирует отладочное сообщение.

**Параметры**:

*   Аналогичны параметрам функции `info`.

**Как работает функция**:

Функция `debug` вызывает функцию `log` с уровнем логирования `logging.DEBUG` для регистрации отладочного сообщения.

### `error`

```python
def error(message, ex=None, exc_info=True, colors: Optional[tuple] = None)
    """Logs an error message.
    
    Parameters:
    - Same as `info`.
    """
```

**Назначение**: Регистрирует сообщение об ошибке.

**Параметры**:

*   Аналогичны параметрам функции `info`.

**Как работает функция**:

Функция `error` вызывает функцию `log` с уровнем логирования `logging.ERROR` для регистрации сообщения об ошибке.

### `critical`

```python
def critical(message, ex=None, exc_info=True, colors: Optional[tuple] = None)
    """Logs a critical message.
    
    Parameters:
    - Same as `info`.
    """
```

**Назначение**: Регистрирует критическое сообщение.

**Параметры**:

*   Аналогичны параметрам функции `info`.

**Как работает функция**:

Функция `critical` вызывает функцию `log` с уровнем логирования `logging.CRITICAL` для регистрации критического сообщения.

## Параметры для логгера

Класс `Logger` принимает несколько необязательных параметров для настройки поведения логирования.

*   **Уровень**: Управляет серьезностью регистрируемых логов. Общие уровни включают:
    *   `logging.DEBUG`: Подробная информация, полезная для диагностики проблем.
    *   `logging.INFO`: Общая информация, такая как успешные операции.
    *   `logging.WARNING`: Предупреждения, которые не обязательно требуют немедленных действий.
    *   `logging.ERROR`: Сообщения об ошибках.
    *   `logging.CRITICAL`: Критические ошибки, требующие немедленного внимания.
*   **Форматтер**: Определяет, как форматируются сообщения журнала. По умолчанию сообщения форматируются как `'%(asctime)s - %(levelname)s - %(message)s'`. Вы можете предоставить пользовательский форматтер для различных форматов, таких как JSON.
*   **Цвет**: Цвета для сообщений журнала в консоли. Цвета указываются в виде кортежа с двумя элементами:
    *   **Цвет текста**: Указывает цвет текста (например, `colorama.Fore.RED`).
    *   **Цвет фона**: Указывает цвет фона (например, `colorama.Back.WHITE`).

Цвет можно настроить для разных уровней логирования (например, зеленый для информации, красный для ошибок и т. д.).

## Конфигурация логирования в файлы (`config`)

Чтобы регистрировать сообщения в файл, вы можете указать пути к файлам в конфигурации.

```python
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
```

Пути к файлам, указанные в `config`, используются для записи логов в соответствующие файлы для каждого уровня логирования.

## Примеры использования

#### 1. Инициализация логгера:

```python
logger: Logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)
```

#### 2. Регистрация сообщений на разных уровнях:

```python
logger.info('Это информационное сообщение')
logger.success('Это сообщение об успехе')
logger.warning('Это предупреждающее сообщение')
logger.debug('Это отладочное сообщение')
logger.error('Это сообщение об ошибке')
logger.critical('Это критическое сообщение')
```

#### 3. Настройка цветов:

```python
logger.info('Это сообщение будет зеленым', colors=(colorama.Fore.GREEN, colorama.Back.BLACK))
logger.error('У этого сообщения будет красный фон', colors=(colorama.Fore.WHITE, colorama.Back.RED))
```

Этот модуль предоставляет комплексную и гибкую систему логирования для Python-приложений. Вы можете настроить логирование в консоль и файлы с различными форматами и цветами, управлять уровнями логирования и корректно обрабатывать исключения. Конфигурация для логирования в файлы хранится в словаре `config`, что обеспечивает простую настройку.