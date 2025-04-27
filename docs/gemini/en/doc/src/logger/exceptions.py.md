# Модуль `src.logger.exceptions`

## Обзор

Этот модуль содержит определения пользовательских исключений, используемых в приложении `hypotez`. Он обеспечивает структурированный подход к обработке ошибок, связанных с различными компонентами приложения, включая операции с файлами, поля продуктов, подключение к базе данных KeePass и ошибки PrestaShop WebService.

## Подробности

Модуль `src.logger.exceptions` служит для централизованного управления исключениями, возникающими в разных частях приложения. Это позволяет повысить читаемость кода, организовать обработку ошибок и сделать код более устойчивым к ошибкам.

## Классы

### `CustomException`

**Описание**: Базовый класс для всех пользовательских исключений в приложении.

**Наследует**: `Exception`

**Атрибуты**:

- `original_exception` (Optional[Exception]): Исходное исключение, которое вызвало это пользовательское исключение, если таковое имеется.
- `exc_info` (bool): Флаг, указывающий, должна ли информация об исключении записываться в журнал.

**Методы**:

- `__init__(self, message: str, e: Optional[Exception] = None, exc_info: bool = True)`: Инициализирует `CustomException` с заданным сообщением и необязательным исходным исключением.
- `handle_exception(self)`: Обрабатывает исключение, записывая ошибку и исходное исключение (если доступно) в журнал.

### `FileNotFoundError`

**Описание**: Возникает, когда файл не найден.

**Наследует**: `CustomException`, `IOError`

### `ProductFieldException`

**Описание**: Возникает при ошибках, связанных с полями продукта.

**Наследует**: `CustomException`

### `KeePassException`

**Описание**: Возникает при проблемах с подключением к базе данных KeePass.

**Наследует**: `CredentialsError`, `BinaryError`, `HeaderChecksumError`, `PayloadChecksumError`, `UnableToSendToRecycleBin`

### `DefaultSettingsException`

**Описание**: Возникает при проблемах с настройками по умолчанию.

**Наследует**: `CustomException`

### `WebDriverException`

**Описание**: Возникает при проблемах, связанных с WebDriver.

**Наследует**: `WDriverException`

### `ExecuteLocatorException`

**Описание**: Возникает при ошибках, связанных с исполнителем локатора.

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

- `__init__(self, msg: str, error_code: Optional[int] = None, ps_error_msg: str = '', ps_error_code: Optional[int] = None)`: Инициализирует `PrestaShopException` с заданным сообщением и деталями ошибки.
- `__str__(self)`: Возвращает строковое представление исключения.

### `PrestaShopAuthenticationError`

**Описание**: Возникает при ошибках аутентификации PrestaShop (неавторизованный доступ).

**Наследует**: `PrestaShopException`

## Примеры

### `CustomException`

```python
from src.logger.exceptions import CustomException

try:
    # Some code that might raise an exception
    raise ValueError("This is a test error")
except ValueError as ex:
    custom_exception = CustomException("Error during processing", ex)
```

### `PrestaShopException`

```python
from src.logger.exceptions import PrestaShopException

try:
    # Code that interacts with PrestaShop WebService
    response =  # ... some API call
    if response.status_code != 200:
        raise PrestaShopException("Error during PrestaShop API call", error_code=response.status_code, ps_error_msg=response.text)
except PrestaShopException as ex:
    print(f"PrestaShop error: {ex}")
```

## Дополнительные сведения

- При возникновении исключения метод `handle_exception` класса `CustomException` записывает информацию об ошибке в журнал.
- Модуль использует модуль `logger` из `src.logger` для журналирования.
- Классы исключений предоставляют структурированный способ обработки ошибок, связанных с конкретными компонентами приложения.
- Модуль `src.logger.exceptions` помогает улучшить надежность и устойчивость приложения, обеспечивая централизованное управление исключениями.