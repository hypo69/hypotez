# Модуль пользовательских исключений для проекта Hypotez

## Обзор

Этот модуль определяет пользовательские исключения, используемые в приложении Hypotez. Он содержит иерархию исключений, начинающуюся с базового класса `CustomException`, который обеспечивает логирование исключений.  Определены специализированные исключения для обработки ошибок, связанных с различными компонентами приложения, такими как файловые операции, поля продуктов, соединения с базами данных KeePass и ошибки веб-сервисов PrestaShop.

## Подробней

Модуль предоставляет набор пользовательских исключений для более структурированной и удобной обработки ошибок в проекте Hypotez. Базовый класс `CustomException` обеспечивает автоматическое логирование исключений, а специализированные классы позволяют обрабатывать ошибки, специфичные для различных частей приложения. Использование пользовательских исключений улучшает читаемость и поддерживаемость кода, а также упрощает отладку.

## Классы

### `CustomException`

**Описание**: Базовый класс для всех пользовательских исключений в приложении.

```python
class CustomException(Exception):
    """Base custom exception class.
    
    This is the base class for all custom exceptions in the application. It handles logging of the exception
    and provides a mechanism for dealing with the original exception if it exists.
    
    Attributes:
    ----------
    original_exception : Optional[Exception]
        The original exception that caused this custom exception, if any.
    exc_info : bool
        A flag to indicate if exception information should be logged.
    """
    ...
```

**Наследует**:

-   `Exception` (базовый класс для всех исключений в Python).

**Атрибуты**:

-   `original_exception` (Optional[Exception]): Исходное исключение, вызвавшее данное пользовательское исключение (если есть).
-   `exc_info` (bool): Флаг, указывающий, следует ли логировать информацию об исключении.

**Методы**:

-   `__init__(self, message: str, e: Optional[Exception] = None, exc_info: bool = True)`: Инициализирует объект `CustomException` с сообщением и опциональным исходным исключением.
-   `handle_exception(self)`: Обрабатывает исключение, логируя ошибку и исходное исключение (если доступно).

#### `__init__`

**Назначение**: Инициализирует объект `CustomException` с сообщением и опциональным исходным исключением.

```python
def __init__(self, message: str, e: Optional[Exception] = None, exc_info: bool = True):
    """Initializes the CustomException with a message and an optional original exception."""
    ...
```

**Параметры**:

-   `message` (str): Сообщение об ошибке.
-   `e` (Optional[Exception]): Исходное исключение (если есть). По умолчанию `None`.
-   `exc_info` (bool): Флаг, указывающий, следует ли логировать информацию об исключении. По умолчанию `True`.

**Как работает функция**:

1.  Вызывает конструктор базового класса `Exception`.
2.  Сохраняет исходное исключение в атрибуте `original_exception`.
3.  Сохраняет значение флага `exc_info` в соответствующем атрибуте.
4.  Вызывает метод `handle_exception` для обработки исключения.

#### `handle_exception`

**Назначение**: Обрабатывает исключение, логируя ошибку и исходное исключение (если доступно).

```python
def handle_exception(self):
    """Handles the exception by logging the error and original exception, if available."""
    ...
```

**Параметры**:

-   Нет.

**Как работает функция**:

1.  Логирует сообщение об ошибке с использованием `logger.error`.
2.  Если доступно исходное исключение (`self.original_exception`), логирует информацию об исходном исключении с использованием `logger.debug`.

### `FileNotFoundError`

**Описание**: Исключение, вызываемое, когда файл не найден.

```python
class FileNotFoundError(CustomException, IOError):
    """Exception raised when a file is not found."""
    pass
```

**Наследует**:

-   `CustomException`
-   `IOError` (базовый класс для исключений, связанных с операциями ввода-вывода).

### `ProductFieldException`

**Описание**: Исключение, вызываемое при ошибках, связанных с полями продукта.

```python
class ProductFieldException(CustomException):
    """Exception raised for errors related to product fields."""
    pass
```

**Наследует**:

-   `CustomException`

### `KeePassException`

**Описание**: Исключение, вызываемое при проблемах с подключением к базе данных KeePass.

```python
class KeePassException(CredentialsError, BinaryError, HeaderChecksumError, PayloadChecksumError, UnableToSendToRecycleBin):
    """Exception raised for connection issues with KeePass database."""
    pass
```

**Наследует**:

-   `CredentialsError`, `BinaryError`, `HeaderChecksumError`, `PayloadChecksumError`, `UnableToSendToRecycleBin` (исключения из библиотеки `pykeepass`).

### `DefaultSettingsException`

**Описание**: Исключение, вызываемое при проблемах с настройками по умолчанию.

```python
class DefaultSettingsException(CustomException):
    """Exception raised for issues with default settings."""
    pass
```

**Наследует**:

-   `CustomException`

### `WebDriverException`

**Описание**: Исключение, вызываемое при проблемах, связанных с WebDriver.

```python
class WebDriverException(WDriverException):
    """Exception raised for WebDriver related issues."""
    pass
```

**Наследует**:

-   `WDriverException` (исключение из библиотеки `selenium`).

### `ExecuteLocatorException`

**Описание**: Исключение, вызываемое при ошибках, связанных с исполнителями локаторов.

```python
class ExecuteLocatorException(CustomException):
    """Exception raised for errors related to locator executors."""
    pass
```

**Наследует**:

-   `CustomException`

### `PrestaShopException`

**Описание**: Базовое исключение для ошибок веб-сервисов PrestaShop.

```python
class PrestaShopException(Exception):
    """Generic exception for PrestaShop WebService errors.
    
    This class is used for handling errors that occur when interacting with the PrestaShop WebService.
    
    Attributes:
    ----------
    msg : str
        A custom error message.
    error_code : Optional[int]
        The error code returned by PrestaShop.
    ps_error_msg : str
        The error message from PrestaShop.
    ps_error_code : Optional[int]
        The PrestaShop error code.
    """
    ...
```

**Наследует**:

-   `Exception` (базовый класс для всех исключений в Python).

**Атрибуты**:

-   `msg` (str): Пользовательское сообщение об ошибке.
-   `error_code` (Optional[int]): Код ошибки, возвращенный PrestaShop (если есть).
-   `ps_error_msg` (str): Сообщение об ошибке, возвращенное PrestaShop.
-   `ps_error_code` (Optional[int]): Код ошибки PrestaShop (если есть).

**Методы**:

-   `__init__(self, msg: str, error_code: Optional[int] = None,  ps_error_msg: str = '', ps_error_code: Optional[int] = None)`: Инициализирует объект `PrestaShopException` с сообщением и деталями ошибки.
-   `__str__(self)`: Возвращает строковое представление исключения.

#### `__init__`

**Назначение**: Инициализирует объект `PrestaShopException` с сообщением и деталями ошибки.

```python
def __init__(self, msg: str, error_code: Optional[int] = None, 
             ps_error_msg: str = '', ps_error_code: Optional[int] = None):
    """Initializes the PrestaShopException with the provided message and error details."""
    ...
```

**Параметры**:

-   `msg` (str): Пользовательское сообщение об ошибке.
-   `error_code` (Optional[int]): Код ошибки, возвращенный PrestaShop (если есть). По умолчанию `None`.
-   `ps_error_msg` (str): Сообщение об ошибке, возвращенное PrestaShop. По умолчанию `''`.
-   `ps_error_code` (Optional[int]): Код ошибки PrestaShop (если есть). По умолчанию `None`.

**Как работает функция**:

1.  Сохраняет предоставленные значения в соответствующих атрибутах объекта.

#### `__str__`

**Назначение**: Возвращает строковое представление исключения.

```python
def __str__(self):
    """Returns the string representation of the exception."""
    ...
```

**Параметры**:

-   Нет.

**Возвращает**:

-   `str`: Строковое представление исключения, содержащее сообщение об ошибке из PrestaShop (если есть) или пользовательское сообщение.

**Как работает функция**:

1.  Возвращает строковое представление исключения, используя сообщение об ошибке из PrestaShop (`self.ps_error_msg`) если оно доступно, или пользовательское сообщение (`self.msg`) в противном случае.

### `PrestaShopAuthenticationError`

**Описание**: Исключение, вызываемое при ошибках аутентификации PrestaShop (Unauthorized).

```python
class PrestaShopAuthenticationError(PrestaShopException):
    """Exception raised for PrestaShop authentication errors (Unauthorized)."""
    pass
```

**Наследует**:

-   `PrestaShopException`

## Переменные модуля

В данном модуле отсутствуют переменные, за исключением констант, используемых для определения путей или настроек по умолчанию (если бы они были).

## Пример использования

```python
from src.logger.exceptions import FileNotFoundError, CustomException

try:
    with open('nonexistent_file.txt', 'r') as f:
        content = f.read()
except FileNotFoundError as ex:
    #  Используем 'ex' вместо 'e' в блоках обработки исключений.
    print(f"File not found: {ex}")
except Exception as ex:
    logger.error("Произошла непредвиденная ошибка", ex, exc_info=True)
```

## Взаимосвязь с другими частями проекта

Этот модуль предназначен для использования в других частях проекта `hypotez`, где требуется обрабатывать исключительные ситуации.  Все пользовательские исключения логируются с использованием модуля `src.logger.logger`.