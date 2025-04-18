# Документация для модуля `src.logger`

## Обзор

Модуль `src.logger` предоставляет гибкую систему логирования, поддерживающую логирование в консоль, файлы и в формате JSON. Он использует шаблон проектирования Singleton, чтобы обеспечить использование единственного экземпляра логгера во всем приложении. Логгер поддерживает различные уровни логирования (например, `INFO`, `ERROR`, `DEBUG`) и включает цветное отображение для вывода в консоль. Также доступны настройки форматов вывода и управление логированием в различные файлы.

## Подробнее

Этот модуль предназначен для централизованного и гибкого управления логированием в проекте. Он предоставляет возможность настройки различных приемников для логов (консоль, файлы в разных форматах) и уровней детализации, что позволяет адаптировать процесс логирования под конкретные нужды проекта. Использование паттерна Singleton гарантирует, что все компоненты проекта будут использовать один и тот же экземпляр логгера, что упрощает управление и обеспечивает консистентность логирования.

## Содержание

- [Классы](#классы)
    - [SingletonMeta](#singletonmeta)
    - [JsonFormatter](#jsonformatter)
    - [Logger](#logger)
- [Функции](#функции)
    - [`_configure_logger`](#_configure_logger)
    - [`initialize_loggers`](#initialize_loggers)
    - [`log`](#log)
- [Параметры логгера](#параметры-логгера)
- [Конфигурация для логирования в файл (`config`)](#конфигурация-для-логирования-в-файл-config)
- [Примеры использования](#примеры-использования)
    - [1. Инициализация логгера](#1-инициализация-логгера)
    - [2. Логирование сообщений](#2-логирование-сообщений)
    - [3. Настройка цветов](#3-настройка-цветов)

## Классы

### `SingletonMeta`

**Описание**: Метакласс, реализующий шаблон Singleton для логгера.

**Принцип работы**:
Метакласс SingletonMeta гарантирует, что у класса логгера будет только один экземпляр. При попытке создать новый экземпляр класса, метакласс возвращает уже существующий экземпляр. Это достигается за счет хранения экземпляра класса в атрибуте `_instances` метакласса.

### `JsonFormatter`

**Описание**: Кастомный форматтер для вывода логов в формате JSON.

**Принцип работы**:
Этот класс форматирует логи в формат JSON. Он наследуется от `logging.Formatter` и переопределяет метод `format`, чтобы преобразовывать запись лога в JSON-строку. Это позволяет сохранять логи в структурированном формате, удобном для дальнейшей обработки и анализа.

### `Logger`

**Описание**: Основной класс логгера, поддерживающий логирование в консоль, файлы и в формате JSON.

**Принцип работы**:
Класс `Logger` реализует всю логику логирования. Он позволяет настраивать различные обработчики (handlers) для вывода логов в консоль и файлы. Поддерживаются разные уровни логирования и форматы вывода, включая JSON. Класс использует методы `_configure_logger` и `initialize_loggers` для настройки логгеров и обработчиков. Метод `log` является основным методом для записи логов.

**Методы**:

- `__init__`:
    ```python
    def __init__(self):
        """
        Инициализирует экземпляр класса Logger с плейсхолдерами для различных типов логгеров (консоль, файлы и JSON).
        """
    ```
    - **Назначение**: Инициализирует экземпляр класса `Logger` с плейсхолдерами для различных типов логгеров (консоль, файлы и JSON).
    - **Параметры**: Отсутствуют.
    - **Возвращает**: Ничего.
    - **Как работает функция**:
        В конструкторе класса `Logger` инициализируются плейсхолдеры для логгеров: `console_logger`, `info_logger`, `debug_logger`, `error_logger` и `json_logger`. Эти плейсхолдеры будут содержать настроенные экземпляры логгеров после вызова метода `initialize_loggers`.

- `_configure_logger`:
    ```python
    def _configure_logger(name: str, log_path: str, level: Optional[int] = logging.DEBUG, formatter: Optional[logging.Formatter] = None, mode: Optional[str] = 'a') -> logging.Logger:
        """
        Настраивает и возвращает экземпляр логгера.

        Args:
            name (str): Имя логгера.
            log_path (str): Путь к файлу логов.
            level (Optional[int], optional): Уровень логирования, например, `logging.DEBUG`. Значение по умолчанию — `logging.DEBUG`.
            formatter (Optional[logging.Formatter], optional): Кастомный форматтер (опционально).
            mode (Optional[str], optional): Режим работы с файлом, например, `'a'` для добавления (значение по умолчанию).

        Returns:
            logging.Logger: Настроенный экземпляр `logging.Logger`.
        """
    ```
    - **Назначение**: Настраивает и возвращает экземпляр логгера.
    - **Параметры**:
        - `name` (str): Имя логгера.
        - `log_path` (str): Путь к файлу логов.
        - `level` (Optional[int], optional): Уровень логирования, например, `logging.DEBUG`. Значение по умолчанию — `logging.DEBUG`.
        - `formatter` (Optional[logging.Formatter], optional): Кастомный форматтер (опционально).
        - `mode` (Optional[str], optional): Режим работы с файлом, например, `'a'` для добавления (значение по умолчанию).
    - **Возвращает**: Настроенный экземпляр `logging.Logger`.
    - **Как работает функция**:
        Функция `_configure_logger` создает и настраивает экземпляр логгера. Она создает объект `logging.Logger` с указанным именем, устанавливает уровень логирования и добавляет обработчик (handler) для записи логов в файл. Если указан форматтер, он применяется к обработчику. Функция возвращает настроенный экземпляр логгера.

- `initialize_loggers`:
    ```python
    def initialize_loggers(info_log_path: Optional[str] = '', debug_log_path: Optional[str] = '', errors_log_path: Optional[str] = '', json_log_path: Optional[str] = ''):
        """
        Инициализирует логгеры для логирования в консоль и файлы (информация, отладка, ошибки и JSON).

        Args:
            info_log_path (Optional[str], optional): Путь к файлу логов информации (опционально).
            debug_log_path (Optional[str], optional): Путь к файлу логов отладки (опционально).
            errors_log_path (Optional[str], optional): Путь к файлу логов ошибок (опционально).
            json_log_path (Optional[str], optional): Путь к файлу логов в формате JSON (опционально).
        """
    ```
    - **Назначение**: Инициализирует логгеры для логирования в консоль и файлы (информация, отладка, ошибки и JSON).
    - **Параметры**:
        - `info_log_path` (Optional[str], optional): Путь к файлу логов информации (опционально).
        - `debug_log_path` (Optional[str], optional): Путь к файлу логов отладки (опционально).
        - `errors_log_path` (Optional[str], optional): Путь к файлу логов ошибок (опционально).
        - `json_log_path` (Optional[str], optional): Путь к файлу логов в формате JSON (опционально).
    - **Возвращает**: Ничего.
    - **Как работает функция**:
        Функция `initialize_loggers` настраивает логгеры для различных типов логов: информационные, отладочные, ошибки и JSON. Она вызывает метод `_configure_logger` для каждого типа логов, передавая соответствующие параметры. Если указан путь к файлу логов, создается файловый логгер. Также настраивается логгер для вывода в консоль. Все настроенные логгеры сохраняются в атрибутах класса (`info_logger`, `debug_logger`, `error_logger`, `json_logger` и `console_logger`).

- `log`:
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
    ```
    - **Назначение**: Логирует сообщение на указанном уровне (например, `INFO`, `DEBUG`, `ERROR`) с возможным исключением и цветовым форматированием.
    - **Параметры**:
        - `level`: Уровень логирования (например, `logging.INFO`, `logging.DEBUG`).
        - `message`: Логируемое сообщение.
        - `ex`: Исключение для логирования (опционально).
        - `exc_info`: Включать информацию об исключении (значение по умолчанию — `False`).
        - `color`: Кортеж цветов текста и фона для консольного вывода (опционально).
    - **Возвращает**: Ничего.
    - **Как работает функция**:
        Функция `log` является основной функцией для записи логов. Она принимает уровень логирования, сообщение и опциональные параметры для исключения и цветового форматирования. В зависимости от уровня логирования, сообщение записывается в соответствующие логгеры (консоль, файлы). Если указано исключение, оно также записывается в лог.

- Другие методы:
    - `info`: Логирует информационное сообщение.
    - `success`: Логирует сообщение об успешной операции.
    - `warning`: Логирует предупреждение.
    - `debug`: Логирует сообщение для отладки.
    - `error`: Логирует сообщение об ошибке.
    - `critical`: Логирует критическое сообщение.
    - **Назначение**: Эти методы являются обертками для метода `log` и позволяют записывать сообщения с соответствующим уровнем логирования. Они принимают сообщение и опциональные параметры для исключения и цветового форматирования.
    - **Параметры**:
        - `message`: Логируемое сообщение.
        - `ex`: Исключение для логирования (опционально).
        - `exc_info`: Включать информацию об исключении (значение по умолчанию — `False`).
        - `color`: Кортеж цветов текста и фона для консольного вывода (опционально).
    - **Возвращает**: Ничего.
    - **Как работают функции**:
       Эти методы упрощают запись логов с определенным уровнем логирования. Они вызывают метод `log` с соответствующим уровнем логирования и передают сообщение и опциональные параметры.

## Функции

### `_configure_logger`

```python
def _configure_logger(name: str, log_path: str, level: Optional[int] = logging.DEBUG, formatter: Optional[logging.Formatter] = None, mode: Optional[str] = 'a') -> logging.Logger:
    """
    Настраивает и возвращает экземпляр логгера.

    Args:
        name (str): Имя логгера.
        log_path (str): Путь к файлу логов.
        level (Optional[int], optional): Уровень логирования, например, `logging.DEBUG`. Значение по умолчанию — `logging.DEBUG`.
        formatter (Optional[logging.Formatter], optional): Кастомный форматтер (опционально).
        mode (Optional[str], optional): Режим работы с файлом, например, `'a'` для добавления (значение по умолчанию).

    Returns:
        logging.Logger: Настроенный экземпляр `logging.Logger`.
    """
```

**Назначение**: Настраивает и возвращает экземпляр логгера.

**Параметры**:

- `name` (str): Имя логгера.
- `log_path` (str): Путь к файлу логов.
- `level` (Optional[int], optional): Уровень логирования, например, `logging.DEBUG`. Значение по умолчанию — `logging.DEBUG`.
- `formatter` (Optional[logging.Formatter], optional): Кастомный форматтер (опционально).
- `mode` (Optional[str], optional): Режим работы с файлом, например, `'a'` для добавления (значение по умолчанию).

**Возвращает**:

- `logging.Logger`: Настроенный экземпляр `logging.Logger`.

**Как работает функция**:
Функция создает и настраивает экземпляр логгера. Она создает объект `logging.Logger` с указанным именем, устанавливает уровень логирования и добавляет обработчик (handler) для записи логов в файл. Если указан форматтер, он применяется к обработчику. Функция возвращает настроенный экземпляр логгера.

### `initialize_loggers`

```python
def initialize_loggers(info_log_path: Optional[str] = '', debug_log_path: Optional[str] = '', errors_log_path: Optional[str] = '', json_log_path: Optional[str] = ''):
    """
    Инициализирует логгеры для логирования в консоль и файлы (информация, отладка, ошибки и JSON).

    Args:
        info_log_path (Optional[str], optional): Путь к файлу логов информации (опционально).
        debug_log_path (Optional[str], optional): Путь к файлу логов отладки (опционально).
        errors_log_path (Optional[str], optional): Путь к файлу логов ошибок (опционально).
        json_log_path (Optional[str], optional): Путь к файлу логов в формате JSON (опционально).
    """
```

**Назначение**: Инициализирует логгеры для логирования в консоль и файлы (информация, отладка, ошибки и JSON).

**Параметры**:

- `info_log_path` (Optional[str], optional): Путь к файлу логов информации (опционально).
- `debug_log_path` (Optional[str], optional): Путь к файлу логов отладки (опционально).
- `errors_log_path` (Optional[str], optional): Путь к файлу логов ошибок (опционально).
- `json_log_path` (Optional[str], optional): Путь к файлу логов в формате JSON (опционально).

**Возвращает**: Ничего.

**Как работает функция**:
Функция настраивает логгеры для различных типов логов: информационные, отладочные, ошибки и JSON. Она вызывает метод `_configure_logger` для каждого типа логов, передавая соответствующие параметры. Если указан путь к файлу логов, создается файловый логгер. Также настраивается логгер для вывода в консоль. Все настроенные логгеры сохраняются в атрибутах класса (`info_logger`, `debug_logger`, `error_logger`, `json_logger` и `console_logger`).

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
```

**Назначение**: Логирует сообщение на указанном уровне (например, `INFO`, `DEBUG`, `ERROR`) с возможным исключением и цветовым форматированием.

**Параметры**:

- `level`: Уровень логирования (например, `logging.INFO`, `logging.DEBUG`).
- `message`: Логируемое сообщение.
- `ex`: Исключение для логирования (опционально).
- `exc_info`: Включать информацию об исключении (значение по умолчанию — `False`).
- `color`: Кортеж цветов текста и фона для консольного вывода (опционально).

**Возвращает**: Ничего.

**Как работает функция**:
Функция является основной функцией для записи логов. Она принимает уровень логирования, сообщение и опциональные параметры для исключения и цветового форматирования. В зависимости от уровня логирования, сообщение записывается в соответствующие логгеры (консоль, файлы). Если указано исключение, оно также записывается в лог.

## Параметры логгера

Класс `Logger` принимает несколько опциональных параметров для настройки поведения логирования.

- **Уровень**: Контролирует, какие сообщения будут записаны. Основные уровни:
  - `logging.DEBUG`: Подробная информация для диагностики.
  - `logging.INFO`: Общая информация, например, успешные операции.
  - `logging.WARNING`: Предупреждения, не требующие немедленного действия.
  - `logging.ERROR`: Сообщения об ошибках.
  - `logging.CRITICAL`: Критические ошибки, требующие немедленного внимания.

- **Форматтер**: Определяет формат сообщений. По умолчанию используется `'%(asctime)s - %(levelname)s - %(message)s'`. Можно задать кастомный форматтер, например для JSON.

- **Цвета**: Задают цвет текста и фона в консоли. Цвета указываются кортежем:
  - **Цвет текста**: Например, `colorama.Fore.RED`.
  - **Цвет фона**: Например, `colorama.Back.WHITE`.

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

#### 2. Логирование сообщений:

```python
logger.info('Это информационное сообщение')
logger.success('Это сообщение об успешной операции')
logger.warning('Это предупреждение')
logger.debug('Это сообщение для отладки')
logger.error('Это сообщение об ошибке')
logger.critical('Это критическое сообщение')
```

#### 3. Настройка цветов:

```python
logger.info('Это сообщение будет зеленым', colors=(colorama.Fore.GREEN, colorama.Back.BLACK))
logger.error('Это сообщение с красным фоном', colors=(colorama.Fore.WHITE, colorama.Back.RED))
```