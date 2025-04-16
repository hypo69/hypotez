# Модуль exceptions

## Обзор

Модуль `exceptions` определяет пользовательские исключения, используемые в приложении. Эти исключения предназначены для обработки ошибок, связанных с различными компонентами приложения, такими как файловые операции, поля продуктов, соединения с базами данных KeePass и ошибки PrestaShop WebService.

## Подробнее

Модуль содержит несколько классов пользовательских исключений для обработки ошибок, связанных с различными компонентами приложения, включая файловые операции, поля продуктов, соединения с базами данных KeePass и ошибки PrestaShop WebService.

## Классы

### `CustomException`

**Описание**: Базовый класс пользовательских исключений.

**Наследует**: `Exception`

**Атрибуты**:

- `original_exception` (Optional[Exception]): Исходное исключение, вызвавшее это пользовательское исключение, если есть.
- `exc_info` (bool): Флаг, указывающий, следует ли регистрировать информацию об исключении.

**Методы**:

- `__init__(self, message: str, e: Optional[Exception] = None, exc_info: bool = True)`: Инициализирует `CustomException` сообщением и необязательным исходным исключением.
- `handle_exception(self)`: Обрабатывает исключение, регистрируя ошибку и исходное исключение, если оно доступно.

**Принцип работы**:

`CustomException` является базовым классом для всех пользовательских исключений в приложении. Он обеспечивает механизм регистрации исключений и обработки исходного исключения, если оно существует. При инициализации класса вызывается метод `handle_exception`, который регистрирует сообщение об ошибке и, при наличии, информацию об исходном исключении.

### `FileNotFoundError`

**Описание**: Исключение, вызываемое, когда файл не найден.

**Наследует**: `CustomException`, `IOError`

### `ProductFieldException`

**Описание**: Исключение, вызываемое для ошибок, связанных с полями продукта.

**Наследует**: `CustomException`

### `KeePassException`

**Описание**: Исключение, вызываемое для ошибок, связанных с соединением с базой данных KeePass.

**Наследует**: `CredentialsError`, `BinaryError`, `HeaderChecksumError`, `PayloadChecksumError`, `UnableToSendToRecycleBin`

### `DefaultSettingsException`

**Описание**: Исключение, вызываемое для проблем с настройками по умолчанию.

**Наследует**: `CustomException`

### `WebDriverException`

**Описание**: Исключение, вызываемое для проблем, связанных с WebDriver.

**Наследует**: `WDriverException`

### `ExecuteLocatorException`

**Описание**: Исключение, вызываемое для ошибок, связанных с исполнителями локаторов.

**Наследует**: `CustomException`

### `PrestaShopException`

**Описание**: Общее исключение для ошибок PrestaShop WebService.

**Наследует**: `Exception`

**Атрибуты**:

- `msg` (str): Пользовательское сообщение об ошибке.
- `error_code` (Optional[int]): Код ошибки, возвращенный PrestaShop.
- `ps_error_msg` (str): Сообщение об ошибке от PrestaShop.
- `ps_error_code` (Optional[int]): Код ошибки PrestaShop.

**Методы**:

- `__init__(self, msg: str, error_code: Optional[int] = None, ps_error_msg: str = '', ps_error_code: Optional[int] = None)`: Инициализирует `PrestaShopException` предоставленным сообщением и деталями ошибки.
- `__str__(self)`: Возвращает строковое представление исключения.

**Принцип работы**:

`PrestaShopException` используется для обработки ошибок, возникающих при взаимодействии с PrestaShop WebService. Класс позволяет хранить пользовательское сообщение об ошибке, код ошибки и сообщение об ошибке от PrestaShop. Метод `__str__` возвращает строковое представление исключения, используя сообщение об ошибке от PrestaShop, если оно доступно, или пользовательское сообщение об ошибке.

### `PrestaShopAuthenticationError`

**Описание**: Исключение, вызываемое для ошибок аутентификации PrestaShop (Unauthorized).

**Наследует**: `PrestaShopException`

## Методы класса

### `CustomException.__init__`

```python
def __init__(self, message: str, e: Optional[Exception] = None, exc_info: bool = True) -> None:
    """Инициализирует CustomException с сообщением и необязательным исходным исключением.

    Args:
        message (str): Сообщение об ошибке.
        e (Optional[Exception], optional): Исходное исключение, вызвавшее это исключение. По умолчанию None.
        exc_info (bool, optional): Флаг, указывающий, следует ли регистрировать информацию об исключении. По умолчанию True.

    Raises:
        Exception: Если возникает ошибка во время инициализации.
    """
    ...
```

### `CustomException.handle_exception`

```python
def handle_exception(self) -> None:
    """Обрабатывает исключение, регистрируя ошибку и исходное исключение, если оно доступно.

    Args:
        self (CustomException): Экземпляр класса CustomException.

    Raises:
        Exception: Если возникает ошибка во время обработки исключения.
    """
    ...
```

### `PrestaShopException.__init__`

```python
def __init__(self, msg: str, error_code: Optional[int] = None, ps_error_msg: str = '', ps_error_code: Optional[int] = None) -> None:
    """Инициализирует PrestaShopException предоставленным сообщением и деталями ошибки.

    Args:
        msg (str): Пользовательское сообщение об ошибке.
        error_code (Optional[int], optional): Код ошибки, возвращенный PrestaShop. По умолчанию None.
        ps_error_msg (str, optional): Сообщение об ошибке от PrestaShop. По умолчанию ''.
        ps_error_code (Optional[int], optional): Код ошибки PrestaShop. По умолчанию None.

    Raises:
        Exception: Если возникает ошибка во время инициализации.
    """
    ...
```

### `PrestaShopException.__str__`

```python
def __str__(self) -> str:
    """Возвращает строковое представление исключения.

    Returns:
        str: Строковое представление исключения.
    """
    ...
```

## Примеры

```python
from src.logger.exceptions import CustomException, FileNotFoundError, PrestaShopException

try:
    raise FileNotFoundError('Файл не найден: example.txt')
except FileNotFoundError as ex:
    print(f'Произошла ошибка: {ex}')

try:
    raise CustomException('Произошла пользовательская ошибка')
except CustomException as ex:
    print(f'Произошла ошибка: {ex}')

try:
    raise PrestaShopException('Ошибка PrestaShop', ps_error_msg='Неверный формат данных')
except PrestaShopException as ex:
    print(f'Произошла ошибка: {ex}')