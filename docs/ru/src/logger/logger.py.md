# Модуль логгера

## Обзор

Модуль `src.logger.logger` предоставляет класс `Logger` для реализации паттерна Singleton с возможностью ведения логов в консоль, файлы и JSON. Он позволяет записывать сообщения различных уровней (INFO, DEBUG, ERROR, CRITICAL) с возможностью настройки цветов текста и фона.

## Подробнее

Этот модуль предназначен для централизованного управления логированием в проекте `hypotez`. Он использует библиотеку `logging` и `colorama` для форматирования и вывода логов. Класс `Logger` реализован как Singleton, что гарантирует наличие только одного экземпляра логгера во всем приложении. Логи могут быть направлены в консоль, в отдельные файлы для информации, отладки и ошибок, а также в JSON-файл для структурированного хранения.

## Классы

### `SingletonMeta`

**Описание**: Метакласс для реализации паттерна Singleton.

**Принцип работы**:
Метакласс `SingletonMeta` гарантирует, что класс, к которому он применяется, будет иметь только один экземпляр. Это достигается за счет хранения экземпляров в словаре `_instances` и использования блокировки `_lock` для предотвращения одновременного создания нескольких экземпляров в многопоточной среде.

### `JsonFormatter`

**Описание**: Пользовательский форматтер для логирования в формате JSON.

**Принцип работы**:
Класс `JsonFormatter` наследует `logging.Formatter` и переопределяет метод `format`, чтобы преобразовывать записи лога в формат JSON. Он включает время записи, уровень логирования, сообщение и информацию об исключении (если она есть).

**Методы**:

- `format(record)`: Форматирует запись лога в JSON.
    - **Параметры**:
        - `record` (logging.LogRecord): Запись лога.
    - **Возвращает**:
        - `str`: JSON-представление записи лога.

### `Logger`

**Описание**: Класс Logger, реализующий паттерн Singleton с логированием в консоль, файлы и JSON.

**Принцип работы**:
Класс `Logger` использует паттерн Singleton для обеспечения единственного экземпляра логгера в приложении. Он настраивает несколько логгеров для вывода в консоль и файлы (info, debug, errors, json). Поддерживает форматирование сообщений с использованием цветов и символов.

**Атрибуты**:

- `log_files_path` (Path): Путь к папке с файлами логов.
- `info_log_path` (Path): Путь к файлу информационных логов.
- `debug_log_path` (Path): Путь к файлу отладочных логов.
- `errors_log_path` (Path): Путь к файлу логов ошибок.
- `json_log_path` (Path): Путь к файлу JSON-логов.
- `logger_console`: (logging.Logger): Логгер для консоли.
- `logger_file_info`: (logging.Logger): Логгер для информационных сообщений.
- `logger_file_debug`: (logging.Logger): Логгер для отладочных сообщений.
- `logger_file_errors`: (logging.Logger): Логгер для сообщений об ошибках.
- `logger_file_json`: (logging.Logger): Логгер для JSON-форматированных сообщений.

**Методы**:

- `__init__(info_log_path: Optional[str] = None, debug_log_path: Optional[str] = None, errors_log_path: Optional[str] = None, json_log_path: Optional[str] = None)`: Инициализирует экземпляр логгера.
    - **Параметры**:
        - `info_log_path` (Optional[str], optional): Путь к файлу информационных логов. По умолчанию `None`.
        - `debug_log_path` (Optional[str], optional): Путь к файлу отладочных логов. По умолчанию `None`.
        - `errors_log_path` (Optional[str], optional): Путь к файлу логов ошибок. По умолчанию `None`.
        - `json_log_path` (Optional[str], optional): Путь к файлу JSON-логов. По умолчанию `None`.
    - **Как работает функция**:
        1. Загружает конфигурацию из файла `config.json`.
        2. Определяет пути к файлам логов на основе конфигурации и текущего времени.
        3. Создает директории для логов, если они не существуют.
        4. Создает файлы логов, если они не существуют.
        5. Настраивает логгеры для консоли и файлов с соответствующими уровнями логирования и форматтерами.

```
        A: Загрузка конфигурации и определение путей
        |
        B: Создание директорий и файлов логов
        |
        C: Настройка логгеров для консоли и файлов
```

- `_format_message(message, ex=None, color: Optional[Tuple[str, str]] = None, level=None)`: Возвращает отформатированное сообщение с информацией об исключении и цветом.
    - **Параметры**:
        - `message` (str): Сообщение для логирования.
        - `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
        - `color` (Optional[Tuple[str, str]], optional): Кортеж цветов текста и фона. По умолчанию `None`.
        - `level` (int, optional): Уровень логирования. По умолчанию `None`.
    - **Возвращает**:
        - `str`: Отформатированное сообщение.
    - **Как работает функция**:
        1. Определяет символ лога на основе уровня логирования.
        2. Если указан цвет, применяет его к сообщению.
        3. Форматирует сообщение с символом лога, цветом (если есть) и информацией об исключении (если есть).

```
        A: Определение символа лога
        |
        B: Применение цвета (если указан)
        |
        C: Форматирование сообщения
```

- `_ex_full_info(ex)`: Возвращает полную информацию об исключении, включая имя файла, имя функции и номер строки.
    - **Параметры**:
        - `ex` (Exception): Объект исключения.
    - **Возвращает**:
        - `str`: Полная информация об исключении.
    - **Как работает функция**:
        1. Получает информацию о кадре стека вызовов.
        2. Извлекает имя файла, имя функции и номер строки из информации о кадре.
        3. Форматирует информацию об исключении, включая имя файла, имя функции и номер строки.

```
        A: Получение информации о кадре стека вызовов
        |
        B: Извлечение имени файла, имени функции и номера строки
        |
        C: Форматирование информации об исключении
```

- `log(level, message, ex=None, exc_info=False, color: Optional[Tuple[str, str]] = None)`: Общий метод для логирования сообщений на указанном уровне с указанным цветом.
    - **Параметры**:
        - `level` (int): Уровень логирования.
        - `message` (str): Сообщение для логирования.
        - `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
        - `exc_info` (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. По умолчанию `False`.
        - `color` (Optional[Tuple[str, str]], optional): Кортеж цветов текста и фона. По умолчанию `None`.
    - **Как работает функция**:
        1. Форматирует сообщение с использованием метода `_format_message`.
        2. Логирует сообщение с указанным уровнем и информацией об исключении (если указано).

```
        A: Форматирование сообщения
        |
        B: Логирование сообщения
```

- `info(message, ex=None, exc_info=False, text_color: str = "green", bg_color: str = "")`: Логирует информационное сообщение с необязательными цветами текста и фона.
    - **Параметры**:
        - `message` (str): Сообщение для логирования.
        - `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
        - `exc_info` (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. По умолчанию `False`.
        - `text_color` (str, optional): Цвет текста. По умолчанию `"green"`.
        - `bg_color` (str, optional): Цвет фона. По умолчанию `""`.
    - **Как работает функция**:
        1. Определяет цвет на основе параметров `text_color` и `bg_color`.
        2. Вызывает метод `log` с уровнем `logging.INFO` и определенным цветом.

```
        A: Определение цвета
        |
        B: Вызов метода log
```

- `success(message, ex=None, exc_info=False, text_color: str = "yellow", bg_color: str = "")`: Логирует сообщение об успехе с необязательными цветами текста и фона.
    - **Параметры**:
        - `message` (str): Сообщение для логирования.
        - `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
        - `exc_info` (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. По умолчанию `False`.
        - `text_color` (str, optional): Цвет текста. По умолчанию `"yellow"`.
        - `bg_color` (str, optional): Цвет фона. По умолчанию `""`.
    - **Как работает функция**:
        1. Определяет цвет на основе параметров `text_color` и `bg_color`.
        2. Вызывает метод `log` с уровнем `logging.INFO` и определенным цветом.

```
        A: Определение цвета
        |
        B: Вызов метода log
```

- `warning(message, ex=None, exc_info=False, text_color: str = "light_red", bg_color: str = "")`: Логирует предупреждающее сообщение с необязательными цветами текста и фона.
    - **Параметры**:
        - `message` (str): Сообщение для логирования.
        - `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
        - `exc_info` (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. По умолчанию `False`.
        - `text_color` (str, optional): Цвет текста. По умолчанию `"light_red"`.
        - `bg_color` (str, optional): Цвет фона. По умолчанию `""`.
    - **Как работает функция**:
        1. Определяет цвет на основе параметров `text_color` и `bg_color`.
        2. Вызывает метод `log` с уровнем `logging.WARNING` и определенным цветом.

```
        A: Определение цвета
        |
        B: Вызов метода log
```

- `debug(message, ex=None, exc_info=True, text_color: str = "cyan", bg_color: str = "")`: Логирует отладочное сообщение с необязательными цветами текста и фона.
    - **Параметры**:
        - `message` (str): Сообщение для логирования.
        - `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
        - `exc_info` (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. По умолчанию `True`.
        - `text_color` (str, optional): Цвет текста. По умолчанию `"cyan"`.
        - `bg_color` (str, optional): Цвет фона. По умолчанию `""`.
    - **Как работает функция**:
        1. Определяет цвет на основе параметров `text_color` и `bg_color`.
        2. Вызывает метод `log` с уровнем `logging.DEBUG` и определенным цветом.

```
        A: Определение цвета
        |
        B: Вызов метода log
```

- `exception(message, ex=None, exc_info=True, text_color: str = "cyan", bg_color: str = "light_gray")`: Логирует сообщение об исключении с необязательными цветами текста и фона.
    - **Параметры**:
        - `message` (str): Сообщение для логирования.
        - `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
        - `exc_info` (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. По умолчанию `True`.
        - `text_color` (str, optional): Цвет текста. По умолчанию `"cyan"`.
        - `bg_color` (str, optional): Цвет фона. По умолчанию `"light_gray"`.
    - **Как работает функция**:
        1. Определяет цвет на основе параметров `text_color` и `bg_color`.
        2. Вызывает метод `log` с уровнем `logging.ERROR` и определенным цветом.

```
        A: Определение цвета
        |
        B: Вызов метода log
```

- `error(message, ex=None, exc_info=True, text_color: str = "red", bg_color: str = "")`: Логирует сообщение об ошибке с необязательными цветами текста и фона.
    - **Параметры**:
        - `message` (str): Сообщение для логирования.
        - `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
        - `exc_info` (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. По умолчанию `True`.
        - `text_color` (str, optional): Цвет текста. По умолчанию `"red"`.
        - `bg_color` (str, optional): Цвет фона. По умолчанию `""`.
    - **Как работает функция**:
        1. Определяет цвет на основе параметров `text_color` и `bg_color`.
        2. Вызывает метод `log` с уровнем `logging.ERROR` и определенным цветом.

```
        A: Определение цвета
        |
        B: Вызов метода log
```

- `critical(message, ex=None, exc_info=True, text_color: str = "red", bg_color: str = "white")`: Логирует критическое сообщение с необязательными цветами текста и фона.
    - **Параметры**:
        - `message` (str): Сообщение для логирования.
        - `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
        - `exc_info` (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. По умолчанию `True`.
        - `text_color` (str, optional): Цвет текста. По умолчанию `"red"`.
        - `bg_color` (str, optional): Цвет фона. По умолчанию `"white"`.
    - **Как работает функция**:
        1. Определяет цвет на основе параметров `text_color` и `bg_color`.
        2. Вызывает метод `log` с уровнем `logging.CRITICAL` и определенным цветом.

```
        A: Определение цвета
        |
        B: Вызов метода log
```

## Функции

### `log`

```python
def log(self, level, message, ex=None, exc_info=False, color: Optional[Tuple[str, str]] = None):
    """
    Общий метод для логирования сообщений на указанном уровне с указанным цветом.
    Args:
        level:
        message:
        ex:
        exc_info:
        color:
    """
    ...
```

**Назначение**: Общий метод для логирования сообщений на указанном уровне с указанным цветом.

**Параметры**:

- `level` (int): Уровень логирования.
- `message` (str): Сообщение для логирования.
- `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
- `exc_info` (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. По умолчанию `False`.
- `color` (Optional[Tuple[str, str]], optional): Кортеж цветов текста и фона. По умолчанию `None`.

**Как работает функция**:

1.  Форматирует сообщение с использованием метода `_format_message`.
2.  Логирует сообщение с указанным уровнем и информацией об исключении (если указано).

```
     A
     ↓
     B
```

Где:

-   `A`: Форматирование сообщения с использованием `_format_message`.
-   `B`: Логирование сообщения с использованием `self.logger_console.log`.

**Примеры**:

```python
logger.log(logging.INFO, "Сообщение", color=("green", ""))
logger.log(logging.ERROR, "Ошибка", ex=ValueError("Неверное значение"), exc_info=True, color=("red", "white"))
```

### `info`

```python
def info(self, message, ex=None, exc_info=False, text_color: str = "green", bg_color: str = ""):
    """
    Логирует информационное сообщение с необязательными цветами текста и фона.
    Args:
        message:
        ex:
        exc_info:
        text_color:
        bg_color:
    """
    ...
```

**Назначение**: Логирует информационное сообщение с необязательными цветами текста и фона.

**Параметры**:

- `message` (str): Сообщение для логирования.
- `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
- `exc_info` (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. По умолчанию `False`.
- `text_color` (str, optional): Цвет текста. По умолчанию `"green"`.
- `bg_color` (str, optional): Цвет фона. По умолчанию `""`.

**Как работает функция**:

1.  Определяет цвет на основе параметров `text_color` и `bg_color`.
2.  Вызывает метод `log` с уровнем `logging.INFO` и определенным цветом.

```
     A
     ↓
     B
```

Где:

-   `A`: Определение цвета на основе `text_color` и `bg_color`.
-   `B`: Вызов метода `log` с уровнем `logging.INFO`.

**Примеры**:

```python
logger.info("Информационное сообщение")
logger.info("Информация", text_color="blue")
```

### `success`

```python
def success(self, message, ex=None, exc_info=False, text_color: str = "yellow", bg_color: str = ""):
    """
    Logs a success message with optional text and background colors.
    Args:
        message:
        ex:
        exc_info:
        text_color:
        bg_color:
    """
    ...
```

**Назначение**: Логирует сообщение об успехе с необязательными цветами текста и фона.

**Параметры**:

- `message` (str): Сообщение для логирования.
- `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
- `exc_info` (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. По умолчанию `False`.
- `text_color` (str, optional): Цвет текста. По умолчанию `"yellow"`.
- `bg_color` (str, optional): Цвет фона. По умолчанию `""`.

**Как работает функция**:

1.  Определяет цвет на основе параметров `text_color` и `bg_color`.
2.  Вызывает метод `log` с уровнем `logging.INFO` и определенным цветом.

```
     A
     ↓
     B
```

Где:

-   `A`: Определение цвета на основе `text_color` и `bg_color`.
-   `B`: Вызов метода `log` с уровнем `logging.INFO`.

**Примеры**:

```python
logger.success("Операция выполнена успешно")
logger.success("Успех!", text_color="green")
```

### `warning`

```python
def warning(self, message, ex=None, exc_info=False, text_color: str = "light_red", bg_color: str = ""):
    """
    Logs a warning message with optional text and background colors.
    Args:
        message:
        ex:
        exc_info:
        text_color:
        bg_color:
    """
    ...
```

**Назначение**: Логирует предупреждающее сообщение с необязательными цветами текста и фона.

**Параметры**:

- `message` (str): Сообщение для логирования.
- `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
- `exc_info` (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. По умолчанию `False`.
- `text_color` (str, optional): Цвет текста. По умолчанию `"light_red"`.
- `bg_color` (str, optional): Цвет фона. По умолчанию `""`.

**Как работает функция**:

1.  Определяет цвет на основе параметров `text_color` и `bg_color`.
2.  Вызывает метод `log` с уровнем `logging.WARNING` и определенным цветом.

```
     A
     ↓
     B
```

Где:

-   `A`: Определение цвета на основе `text_color` и `bg_color`.
-   `B`: Вызов метода `log` с уровнем `logging.WARNING`.

**Примеры**:

```python
logger.warning("Предупреждение!")
logger.warning("Внимание!", text_color="yellow")
```

### `debug`

```python
def debug(self, message, ex=None, exc_info=True, text_color: str = "cyan", bg_color: str = ""):
    """
    Logs a debug message with optional text and background colors.
    Args:
        message:
        ex:
        exc_info:
        text_color:
        bg_color:
    """
    ...
```

**Назначение**: Логирует отладочное сообщение с необязательными цветами текста и фона.

**Параметры**:

- `message` (str): Сообщение для логирования.
- `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
- `exc_info` (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. По умолчанию `True`.
- `text_color` (str, optional): Цвет текста. По умолчанию `"cyan"`.
- `bg_color` (str, optional): Цвет фона. По умолчанию `""`.

**Как работает функция**:

1.  Определяет цвет на основе параметров `text_color` и `bg_color`.
2.  Вызывает метод `log` с уровнем `logging.DEBUG` и определенным цветом.

```
     A
     ↓
     B
```

Где:

-   `A`: Определение цвета на основе `text_color` и `bg_color`.
-   `B`: Вызов метода `log` с уровнем `logging.DEBUG`.

**Примеры**:

```python
logger.debug("Отладочное сообщение")
logger.debug("Отладка", text_color="blue", exc_info=False)
```

### `exception`

```python
def exception(self, message, ex=None, exc_info=True, text_color: str = "cyan", bg_color: str = "light_gray"):
    """
    Logs an exception message with optional text and background colors.
    Args:
        message:
        ex:
        exc_info:
        text_color:
        bg_color:
    """
    ...
```

**Назначение**: Логирует сообщение об исключении с необязательными цветами текста и фона.

**Параметры**:

- `message` (str): Сообщение для логирования.
- `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
- `exc_info` (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. По умолчанию `True`.
- `text_color` (str, optional): Цвет текста. По умолчанию `"cyan"`.
- `bg_color` (str, optional): Цвет фона. По умолчанию `"light_gray"`.

**Как работает функция**:

1.  Определяет цвет на основе параметров `text_color` и `bg_color`.
2.  Вызывает метод `log` с уровнем `logging.ERROR` и определенным цветом.

```
     A
     ↓
     B
```

Где:

-   `A`: Определение цвета на основе `text_color` и `bg_color`.
-   `B`: Вызов метода `log` с уровнем `logging.ERROR`.

**Примеры**:

```python
try:
    raise ValueError("Ошибка значения")
except ValueError as ex:
    logger.exception("Произошло исключение", ex=ex)
```

### `error`

```python
def error(self, message, ex=None, exc_info=True, text_color: str = "red", bg_color: str = ""):
    """
    Logs an error message with optional text and background colors.
    Args:
        message:
        ex:
        exc_info:
        text_color:
        bg_color:
    """
    ...
```

**Назначение**: Логирует сообщение об ошибке с необязательными цветами текста и фона.

**Параметры**:

- `message` (str): Сообщение для логирования.
- `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
- `exc_info` (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. По умолчанию `True`.
- `text_color` (str, optional): Цвет текста. По умолчанию `"red"`.
- `bg_color` (str, optional): Цвет фона. По умолчанию `""`.

**Как работает функция**:

1.  Определяет цвет на основе параметров `text_color` и `bg_color`.
2.  Вызывает метод `log` с уровнем `logging.ERROR` и определенным цветом.

```
     A
     ↓
     B
```

Где:

-   `A`: Определение цвета на основе `text_color` и `bg_color`.
-   `B`: Вызов метода `log` с уровнем `logging.ERROR`.

**Примеры**:

```python
logger.error("Произошла ошибка")
logger.error("Ошибка ввода", ex=IOError("Нет доступа к файлу"))
```

### `critical`

```python
def critical(self, message, ex=None, exc_info=True, text_color: str = "red", bg_color: str = "white"):
    """
    Logs a critical message with optional text and background colors.
    Args:
        message:
        ex:
        exc_info:
        text_color:
        bg_color:
    """
    ...
```

**Назначение**: Логирует критическое сообщение с необязательными цветами текста и фона.

**Параметры**:

- `message` (str): Сообщение для логирования.
- `ex` (Optional[Exception], optional): Объект исключения. По умолчанию `None`.
- `exc_info` (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключении. По умолчанию `True`.
- `text_color` (str, optional): Цвет текста. По умолчанию `"red"`.
- `bg_color` (str, optional): Цвет фона. По умолчанию `"white"`.

**Как работает функция**:

1.  Определяет цвет на основе параметров `text_color` и `bg_color`.
2.  Вызывает метод `log` с уровнем `logging.CRITICAL` и определенным цветом.

```
     A
     ↓
     B
```

Где:

-   `A`: Определение цвета на основе `text_color` и `bg_color`.
-   `B`: Вызов метода `log` с уровнем `logging.CRITICAL`.

**Примеры**:

```python
logger.critical("Критическая ошибка!")
logger.critical("Система будет остановлена", text_color="yellow", bg_color="black")