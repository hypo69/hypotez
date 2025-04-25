# Модуль исключений

## Обзор

Модуль `src.logger.exceptions` определяет кастомные исключения, используемые в приложении. 

## Подробней

Этот модуль содержит несколько классов кастомных исключений для обработки ошибок, связанных с различными компонентами приложения, включая операции с файлами, полями товаров, подключением к базе данных KeePass и ошибками веб-сервиса PrestaShop.

## Классы

### `CustomException`

**Описание**: Базовый класс кастомных исключений.

**Наследует**: `Exception`

**Атрибуты**:

- `original_exception` (Optional[Exception]): Оригинальное исключение, которое вызвало это кастомное исключение, если такое есть.
- `exc_info` (bool): Флаг, указывающий, должна ли информация об исключении быть записана в лог.

**Методы**:

- `__init__(self, message: str, e: Optional[Exception] = None, exc_info: bool = True)`: Инициализирует `CustomException` с сообщением и необязательным оригинальным исключением.

- `handle_exception(self)`: Обрабатывает исключение, записывая ошибку и оригинальное исключение (если доступно) в лог.


### `FileNotFoundError`

**Описание**: Исключение, которое возникает, когда файл не найден.

**Наследует**: `CustomException`, `IOError`


### `ProductFieldException`

**Описание**: Исключение, которое возникает при ошибках, связанных с полями товаров.

**Наследует**: `CustomException`


### `KeePassException`

**Описание**: Исключение, которое возникает при проблемах с подключением к базе данных KeePass.

**Наследует**: `CredentialsError`, `BinaryError`, `HeaderChecksumError`, `PayloadChecksumError`, `UnableToSendToRecycleBin`


### `DefaultSettingsException`

**Описание**: Исключение, которое возникает при проблемах с настройками по умолчанию.

**Наследует**: `CustomException`


### `WebDriverException`

**Описание**: Исключение, которое возникает при проблемах, связанных с WebDriver.

**Наследует**: `WDriverException`


### `ExecuteLocatorException`

**Описание**: Исключение, которое возникает при ошибках, связанных с исполнителем локаторов.

**Наследует**: `CustomException`


### `PrestaShopException`

**Описание**: Общее исключение для ошибок веб-сервиса PrestaShop.

**Наследует**: `Exception`

**Атрибуты**:

- `msg` (str): Пользовательское сообщение об ошибке.
- `error_code` (Optional[int]): Код ошибки, возвращенный PrestaShop.
- `ps_error_msg` (str): Сообщение об ошибке от PrestaShop.
- `ps_error_code` (Optional[int]): Код ошибки PrestaShop.

**Методы**:

- `__init__(self, msg: str, error_code: Optional[int] = None, ps_error_msg: str = '', ps_error_code: Optional[int] = None)`: Инициализирует `PrestaShopException` с заданным сообщением и сведениями об ошибке.

- `__str__(self)`: Возвращает строковое представление исключения.


### `PrestaShopAuthenticationError`

**Описание**: Исключение, которое возникает при ошибках аутентификации PrestaShop (Unauthorized).

**Наследует**: `PrestaShopException`

**Примеры**:

```python
from src.logger.exceptions import PrestaShopAuthenticationError

# Пример вызова исключения:
raise PrestaShopAuthenticationError(
    msg="Ошибка аутентификации PrestaShop",
    ps_error_msg="Unauthorized",
    ps_error_code=401
)
```

## Внутренние функции

### `handle_exception`

**Назначение**: Обрабатывает исключение, записывая ошибку и оригинальное исключение (если доступно) в лог.

**Как работает**:

- Использует `logger` из модуля `src.logger` для записи ошибки в лог.
- Записывает оригинальное исключение в лог с помощью `logger.debug`, если оно доступно.
- Добавляет логику восстановления, повторов или другой обработки, если необходимо.

**Примеры**:

```python
from src.logger.exceptions import CustomException

# Пример обработки исключения:
try:
    # Some code that might raise an exception
    raise Exception("Test exception")
except Exception as ex:
    # Create a custom exception and handle it
    custom_exception = CustomException(message="Error occurred", e=ex)
    # ... further handling or recovery logic
```