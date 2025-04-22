# Модуль `src.logger.logger`

## Обзор

Модуль `src.logger.logger` предназначен для организации логирования в проекте. Он предоставляет класс `Logger`, реализующий паттерн Singleton, что гарантирует наличие только одного экземпляра логгера в системе. Логгер поддерживает вывод сообщений в консоль, запись в файлы (info, debug, errors) и в JSON-файл. Модуль использует библиотеку `colorama` для раскрашивания сообщений в консоли.

## Подробней

Модуль содержит классы и функции для настройки логирования, включая форматирование сообщений и обработку исключений. Он позволяет записывать логи в файлы различных уровней (INFO, DEBUG, ERROR) и предоставляет возможность настройки цветов для консольного вывода.

## Содержание

- [Классы](#Классы)
  - [SingletonMeta](#SingletonMeta)
  - [JsonFormatter](#JsonFormatter)
  - [Logger](#Logger)
- [Переменные](#Переменные)
- [Функции](#Функции)
  - [`_format_message`](#_format_message)
  - [`_ex_full_info`](#_ex_full_info)
  - [`log`](#log)
  - [`info`](#info)
  - [`success`](#success)
  - [`warning`](#warning)
  - [`debug`](#debug)
  - [`exception`](#exception)
  - [`error`](#error)
  - [`critical`](#critical)

## Переменные

### `TEXT_COLORS`

Словарь, содержащий ANSI escape-коды для различных цветов текста, используемых при логировании в консоль.

### `BG_COLORS`

Словарь, содержащий ANSI escape-коды для различных цветов фона, используемых при логировании в консоль.

### `LOG_SYMBOLS`

Словарь, содержащий символы, соответствующие различным уровням логирования, для визуального отображения в консоли.

## Классы

### `SingletonMeta`

**Описание**: Метакласс для реализации паттерна Singleton. Обеспечивает создание только одного экземпляра класса.

**Наследует**: `type`

**Методы**:

- `__call__(cls, *args, **kwargs)`: Обеспечивает создание только одного экземпляра класса. Если экземпляр класса уже существует, возвращает существующий экземпляр.

### `JsonFormatter`

**Описание**: Пользовательский форматтер для логирования в формате JSON.

**Наследует**: `logging.Formatter`

**Методы**:

- `format(self, record)`: Форматирует запись лога в JSON-формат. Включает время, уровень логирования, сообщение и информацию об исключении (если есть).

### `Logger`

**Описание**: Класс логгера, реализующий паттерн Singleton. Поддерживает логирование в консоль, файлы (info, debug, errors) и JSON-файл.

**Наследует**: Нет

**Атрибуты**:

- `log_files_path` (Path): Путь к директории, где хранятся файлы логов.
- `info_log_path` (Path): Путь к файлу для логирования информационных сообщений.
- `debug_log_path` (Path): Путь к файлу для логирования отладочных сообщений.
- `errors_log_path` (Path): Путь к файлу для логирования сообщений об ошибках.
- `json_log_path` (Path): Путь к файлу для логирования в формате JSON.
- `logger_console` (logging.Logger): Объект логгера для вывода в консоль.
- `logger_file_info` (logging.Logger): Объект логгера для записи информационных сообщений в файл.
- `logger_file_debug` (logging.Logger): Объект логгера для записи отладочных сообщений в файл.
- `logger_file_errors` (logging.Logger): Объект логгера для записи сообщений об ошибках в файл.
- `logger_file_json` (logging.Logger): Объект логгера для записи сообщений в формате JSON в файл.

**Методы**:

- `__init__(self, info_log_path: Optional[str] = None, debug_log_path: Optional[str] = None, errors_log_path: Optional[str] = None, json_log_path: Optional[str] = None)`:
    - **Назначение**: Инициализирует экземпляр класса `Logger`.
    - **Параметры**:
        - `info_log_path` (Optional[str], optional): Путь к файлу для информационных логов. По умолчанию `None`.
        - `debug_log_path` (Optional[str], optional): Путь к файлу для дебаг логов. По умолчанию `None`.
        - `errors_log_path` (Optional[str], optional): Путь к файлу для логов ошибок. По умолчанию `None`.
        - `json_log_path` (Optional[str], optional): Путь к файлу для JSON логов. По умолчанию `None`.
    - **Как работает функция**:
        - Функция определяет пути к файлам логов на основе переданных параметров или значений по умолчанию из конфигурационного файла.
        - Создает директории для хранения логов, если они не существуют.
        - Создает файлы логов, если они не существуют.
        - Инициализирует логгеры для консоли и файлов, устанавливает уровни логирования и форматтеры.
        - Удаляет все обработчики, которые выводят в консоль для JSON логгера.
    - **Примеры**:
      ```python
      from src.logger.logger import Logger
      logger = Logger(info_log_path='info.log', debug_log_path='debug.log', errors_log_path='errors.log', json_log_path='log.json')
      ```

## Функции

### `_format_message`

- **Назначение**: Форматирует сообщение лога с учетом уровня логирования, добавляет символ, цвет и информацию об исключении (если есть).
    - **Параметры**:
        - `message` (str): Сообщение для логирования.
        - `ex` (Exception, optional): Объект исключения. По умолчанию `None`.
        - `color` (Tuple[str, str], optional): Кортеж, содержащий цвет текста и фона. По умолчанию `None`.
        - `level` (int, optional): Уровень логирования. По умолчанию `None`.
    - **Возвращает**:
        - `str`: Отформатированное сообщение.
    - **Как работает функция**:
        - Функция извлекает символ лога на основе уровня логирования.
        - Если указан цвет, применяет ANSI escape-коды для раскрашивания сообщения.
        - Добавляет информацию об исключении (если есть) к сообщению.
        - Возвращает отформатированное сообщение.
    - **Примеры**:
      ```python
      from src.logger.logger import Logger
      logger = Logger()
      formatted_message = logger._format_message("Test message", ex=Exception("Test exception"), color=("red", "light_gray"), level=logging.ERROR)
      print(formatted_message)
      ```

### `_ex_full_info`

- **Назначение**: Получает полную информацию об исключении, включая имя файла, имя функции и номер строки, где произошло исключение.
    - **Параметры**:
        - `ex` (Exception): Объект исключения.
    - **Возвращает**:
        - `str`: Полная информация об исключении.
    - **Как работает функция**:
        - Функция использует модуль `inspect` для получения информации о стеке вызовов.
        - Извлекает имя файла, имя функции и номер строки из стека вызовов.
        - Форматирует информацию об исключении и возвращает ее в виде строки.
    - **Примеры**:
      ```python
      from src.logger.logger import Logger
      logger = Logger()
      try:
          raise ValueError("Test error")
      except ValueError as ex:
          full_info = logger._ex_full_info(ex)
          print(full_info)
      ```

### `log`

- **Назначение**: Общий метод для логирования сообщений на указанном уровне с возможностью указания цвета.
    - **Параметры**:
        - `level` (int): Уровень логирования.
        - `message` (str): Сообщение для логирования.
        - `ex` (Exception, optional): Объект исключения. По умолчанию `None`.
        - `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `False`.
        - `color` (Tuple[str, str], optional): Кортеж, содержащий цвет текста и фона. По умолчанию `None`.
    - **Как работает функция**:
        - Функция форматирует сообщение с помощью метода `_format_message`.
        - Выводит сообщение в консоль с использованием соответствующего метода логгера.
        - Если `exc_info` установлено в `True` и есть исключение, логирует сообщение как исключение.
    - **Примеры**:
      ```python
      from src.logger.logger import Logger
      logger = Logger()
      logger.log(logging.INFO, "Test message", ex=None, exc_info=False, color=("green", ""))
      ```

### `info`

- **Назначение**: Логирует информационное сообщение с возможностью указания цвета текста и фона.
    - **Параметры**:
        - `message` (str): Сообщение для логирования.
        - `ex` (Exception, optional): Объект исключения. По умолчанию `None`.
        - `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `False`.
        - `text_color` (str, optional): Цвет текста. По умолчанию `"green"`.
        - `bg_color` (str, optional): Цвет фона. По умолчанию `""`.
    - **Как работает функция**:
        - Функция вызывает метод `log` с уровнем логирования `logging.INFO` и указанными цветами.
    - **Примеры**:
      ```python
      from src.logger.logger import Logger
      logger = Logger()
      logger.info("Test info message", ex=None, exc_info=False, text_color="blue", bg_color="light_gray")
      ```

### `success`

- **Назначение**: Логирует сообщение об успехе с возможностью указания цвета текста и фона.
    - **Параметры**:
        - `message` (str): Сообщение для логирования.
        - `ex` (Exception, optional): Объект исключения. По умолчанию `None`.
        - `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `False`.
        - `text_color` (str, optional): Цвет текста. По умолчанию `"yellow"`.
        - `bg_color` (str, optional): Цвет фона. По умолчанию `""`.
    - **Как работает функция**:
        - Функция вызывает метод `log` с уровнем логирования `logging.INFO` и указанными цветами.
    - **Примеры**:
      ```python
      from src.logger.logger import Logger
      logger = Logger()
      logger.success("Test success message", ex=None, exc_info=False, text_color="green", bg_color="")
      ```

### `warning`

- **Назначение**: Логирует сообщение предупреждения с возможностью указания цвета текста и фона.
    - **Параметры**:
        - `message` (str): Сообщение для логирования.
        - `ex` (Exception, optional): Объект исключения. По умолчанию `None`.
        - `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `False`.
        - `text_color` (str, optional): Цвет текста. По умолчанию `"light_red"`.
        - `bg_color` (str, optional): Цвет фона. По умолчанию `""`.
    - **Как работает функция**:
        - Функция вызывает метод `log` с уровнем логирования `logging.WARNING` и указанными цветами.
    - **Примеры**:
      ```python
      from src.logger.logger import Logger
      logger = Logger()
      logger.warning("Test warning message", ex=None, exc_info=False, text_color="yellow", bg_color="")
      ```

### `debug`

- **Назначение**: Логирует отладочное сообщение с возможностью указания цвета текста и фона.
    - **Параметры**:
        - `message` (str): Сообщение для логирования.
        - `ex` (Exception, optional): Объект исключения. По умолчанию `None`.
        - `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `True`.
        - `text_color` (str, optional): Цвет текста. По умолчанию `"cyan"`.
        - `bg_color` (str, optional): Цвет фона. По умолчанию `""`.
    - **Как работает функция**:
        - Функция вызывает метод `log` с уровнем логирования `logging.DEBUG` и указанными цветами.
    - **Примеры**:
      ```python
      from src.logger.logger import Logger
      logger = Logger()
      logger.debug("Test debug message", ex=None, exc_info=True, text_color="magenta", bg_color="light_gray")
      ```

### `exception`

- **Назначение**: Логирует сообщение об исключении с возможностью указания цвета текста и фона.
    - **Параметры**:
        - `message` (str): Сообщение для логирования.
        - `ex` (Exception, optional): Объект исключения. По умолчанию `None`.
        - `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `True`.
        - `text_color` (str, optional): Цвет текста. По умолчанию `"cyan"`.
        - `bg_color` (str, optional): Цвет фона. По умолчанию `"light_gray"`.
    - **Как работает функция**:
        - Функция вызывает метод `log` с уровнем логирования `logging.ERROR` и указанными цветами. Логируется как ошибка.
    - **Примеры**:
      ```python
      from src.logger.logger import Logger
      logger = Logger()
      try:
          raise ValueError("Test error")
      except ValueError as ex:
          logger.exception("Test exception message", ex=ex, exc_info=True, text_color="red", bg_color="")
      ```

### `error`

- **Назначение**: Логирует сообщение об ошибке с возможностью указания цвета текста и фона.
    - **Параметры**:
        - `message` (str): Сообщение для логирования.
        - `ex` (Exception, optional): Объект исключения. По умолчанию `None`.
        - `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `True`.
        - `text_color` (str, optional): Цвет текста. По умолчанию `"red"`.
        - `bg_color` (str, optional): Цвет фона. По умолчанию `""`.
    - **Как работает функция**:
        - Функция вызывает метод `log` с уровнем логирования `logging.ERROR` и указанными цветами.
    - **Примеры**:
      ```python
      from src.logger.logger import Logger
      logger = Logger()
      logger.error("Test error message", ex=ValueError("Test error"), exc_info=True, text_color="yellow", bg_color="light_red")
      ```

### `critical`

- **Назначение**: Логирует критическое сообщение с возможностью указания цвета текста и фона.
    - **Параметры**:
        - `message` (str): Сообщение для логирования.
        - `ex` (Exception, optional): Объект исключения. По умолчанию `None`.
        - `exc_info` (bool, optional): Флаг, указывающий, нужно ли добавлять информацию об исключении в лог. По умолчанию `True`.
        - `text_color` (str, optional): Цвет текста. По умолчанию `"red"`.
        - `bg_color` (str, optional): Цвет фона. По умолчанию `"white"`.
    - **Как работает функция**:
        - Функция вызывает метод `log` с уровнем логирования `logging.CRITICAL` и указанными цветами.
    - **Примеры**:
      ```python
      from src.logger.logger import Logger
      logger = Logger()
      logger.critical("Test critical message", ex=None, exc_info=True, text_color="light_yellow", bg_color="bg_red")
      ```