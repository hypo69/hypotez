# Модуль `src.logger.exceptions`

## Обзор

Модуль определяет пользовательские исключения, используемые в приложении. Он содержит классы исключений для обработки ошибок, связанных с операциями с файлами, полями товаров, подключениями к базам данных KeePass и ошибками веб-служб PrestaShop.

## Подробнее

Модуль содержит несколько пользовательских классов исключений для обработки ошибок, связанных с различными компонентами приложения, включая файловые операции, поля товара, подключения к базам данных KeePass и ошибки веб-служб PrestaShop.

## Классы

### `CustomException`

**Описание**: Базовый класс для всех пользовательских исключений в приложении. Он обрабатывает логирование исключений и предоставляет механизм для работы с исходным исключением, если оно существует.

**Атрибуты**:

-   `original_exception` (Optional[Exception]): Исходное исключение, вызвавшее данное пользовательское исключение, если оно есть.
-   `exc_info` (bool): Флаг, указывающий, следует ли логировать информацию об исключении.

**Методы**:

-   `__init__(self, message: str, e: Optional[Exception] = None, exc_info: bool = True)`: Инициализирует `CustomException` сообщением и необязательным исходным исключением.
-   `handle_exception(self)`: Обрабатывает исключение, логируя ошибку и исходное исключение, если оно доступно.

#### `__init__`

```python
def __init__(self, message: str, e: Optional[Exception] = None, exc_info: bool = True):
    """Инициализирует CustomException с сообщением и необязательным исходным исключением.

    Args:
        message (str): Сообщение об ошибке.
        e (Optional[Exception], optional): Исходное исключение, вызвавшее данное исключение. По умолчанию `None`.
        exc_info (bool, optional): Флаг, указывающий, следует ли логировать информацию об исключении. По умолчанию `True`.
    """
    super().__init__(message)
    self.original_exception = e
    self.exc_info = exc_info
    self.handle_exception()
```

#### `handle_exception`

```python
def handle_exception(self):
    """Обрабатывает исключение, логируя ошибку и исходное исключение, если оно доступно.
    """
    logger.error(f"Exception occurred: {self}")
    if self.original_exception:
        logger.debug(f"Original exception: {self.original_exception}")
    # Add recovery logic, retries, or other handling as necessary.
```

### `FileNotFoundError`

**Описание**: Исключение, возникающее, когда файл не найден.

**Наследует**:
- `CustomException`
- `IOError`

### `ProductFieldException`

**Описание**: Исключение, возникающее при ошибках, связанных с полями товара.

**Наследует**:
- `CustomException`

### `KeePassException`

**Описание**: Исключение, возникающее при проблемах с подключением к базе данных KeePass.

**Наследует**:
- `CredentialsError`
- `BinaryError`
- `HeaderChecksumError`
- `PayloadChecksumError`
- `UnableToSendToRecycleBin`

### `DefaultSettingsException`

**Описание**: Исключение, возникающее при проблемах с настройками по умолчанию.

**Наследует**:
- `CustomException`

### `WebDriverException`

**Описание**: Исключение, возникающее при проблемах, связанных с WebDriver.

**Наследует**:
- `WDriverException` (из `selenium.common.exceptions`)

### `ExecuteLocatorException`

**Описание**: Исключение, возникающее при ошибках, связанных с исполнителями локаторов.

**Наследует**:
- `CustomException`

### `PrestaShopException`

**Описание**: Общее исключение для ошибок веб-службы PrestaShop.

**Атрибуты**:

-   `msg` (str): Пользовательское сообщение об ошибке.
-   `error_code` (Optional[int]): Код ошибки, возвращенный PrestaShop.
-   `ps_error_msg` (str): Сообщение об ошибке от PrestaShop.
-   `ps_error_code` (Optional[int]): Код ошибки PrestaShop.

**Методы**:

-   `__init__(self, msg: str, error_code: Optional[int] = None, ps_error_msg: str = '', ps_error_code: Optional[int] = None)`: Инициализирует `PrestaShopException` предоставленным сообщением и деталями ошибки.
-   `__str__(self)`: Возвращает строковое представление исключения.

#### `__init__`

```python
def __init__(self, msg: str, error_code: Optional[int] = None,
             ps_error_msg: str = '', ps_error_code: Optional[int] = None):
    """Инициализирует PrestaShopException предоставленным сообщением и деталями ошибки.

    Args:
        msg (str): Пользовательское сообщение об ошибке.
        error_code (Optional[int], optional): Код ошибки, возвращенный PrestaShop. По умолчанию `None`.
        ps_error_msg (str, optional): Сообщение об ошибке от PrestaShop. По умолчанию ''.
        ps_error_code (Optional[int], optional): Код ошибки PrestaShop. По умолчанию `None`.
    """
    self.msg = msg
    self.error_code = error_code
    self.ps_error_msg = ps_error_msg
    self.ps_error_code = ps_error_code
```

#### `__str__`

```python
def __str__(self):
    """Возвращает строковое представление исключения.
    """
    return repr(self.ps_error_msg or self.msg)
```

### `PrestaShopAuthenticationError`

**Описание**: Исключение, возникающее при ошибках аутентификации PrestaShop (Unauthorized).

**Наследует**:
- `PrestaShopException`