# Модуль для определения пользовательских исключений

## Обзор

Этот модуль определяет пользовательские исключения, используемые в приложении. Он содержит классы исключений для обработки ошибок, связанных с различными компонентами приложения, включая файловые операции, поля продуктов, соединения с базой данных KeePass и ошибки веб-службы PrestaShop.

## Подробней

Модуль содержит несколько пользовательских классов исключений для обработки ошибок, связанных с различными компонентами приложения, включая файловые операции, поля продуктов, соединения с базой данных KeePass и ошибки веб-службы PrestaShop.

## Классы

### `CustomException`

**Описание**: Базовый класс пользовательских исключений.

**Принцип работы**:
Этот класс является базовым для всех пользовательских исключений в приложении. Он обрабатывает логирование исключения и предоставляет механизм для работы с исходным исключением, если оно существует.

**Атрибуты**:

- `original_exception` (Optional[Exception]): Исходное исключение, вызвавшее это пользовательское исключение, если таковое имеется.
- `exc_info` (bool): Флаг, указывающий, следует ли логировать информацию об исключении.

**Методы**:

- `__init__(self, message: str, e: Optional[Exception] = None, exc_info: bool = True)`: Инициализирует `CustomException` сообщением и необязательным исходным исключением.
- `handle_exception(self)`: Обрабатывает исключение, логируя ошибку и исходное исключение, если оно доступно. Добавляет логику восстановления, повторные попытки или другую обработку по мере необходимости.

### `FileNotFoundError`

**Описание**: Исключение, возникающее, когда файл не найден.

**Наследует**:
- `CustomException`: Наследует базовый класс пользовательских исключений.
- `IOError`: Наследует класс исключений ввода-вывода.

### `ProductFieldException`

**Описание**: Исключение, возникающее при ошибках, связанных с полями продукта.

**Наследует**:
- `CustomException`: Наследует базовый класс пользовательских исключений.

### `KeePassException`

**Описание**: Исключение, возникающее при проблемах соединения с базой данных KeePass.

**Наследует**:
- `CredentialsError`
- `BinaryError`
- `HeaderChecksumError`
- `PayloadChecksumError`
- `UnableToSendToRecycleBin`

### `DefaultSettingsException`

**Описание**: Исключение, возникающее при проблемах с настройками по умолчанию.

**Наследует**:
- `CustomException`: Наследует базовый класс пользовательских исключений.

### `WebDriverException`

**Описание**: Исключение, возникающее при проблемах, связанных с WebDriver.

**Наследует**:
- `WDriverException`: Наследует класс исключений WebDriver из `selenium`.

### `ExecuteLocatorException`

**Описание**: Исключение, возникающее при ошибках, связанных с исполнителями локаторов.

**Наследует**:
- `CustomException`: Наследует базовый класс пользовательских исключений.

### `PrestaShopException`

**Описание**: Общее исключение для ошибок веб-службы PrestaShop.

**Принцип работы**:
Этот класс используется для обработки ошибок, возникающих при взаимодействии с веб-службой PrestaShop.

**Атрибуты**:

- `msg` (str): Пользовательское сообщение об ошибке.
- `error_code` (Optional[int]): Код ошибки, возвращенный PrestaShop.
- `ps_error_msg` (str): Сообщение об ошибке от PrestaShop.
- `ps_error_code` (Optional[int]): Код ошибки PrestaShop.

**Методы**:

- `__init__(self, msg: str, error_code: Optional[int] = None, ps_error_msg: str = '', ps_error_code: Optional[int] = None)`: Инициализирует `PrestaShopException` предоставленным сообщением и деталями ошибки.
- `__str__(self)`: Возвращает строковое представление исключения.

### `PrestaShopAuthenticationError`

**Описание**: Исключение, возникающее при ошибках аутентификации PrestaShop (Unauthorized).

**Наследует**:
- `PrestaShopException`: Наследует класс исключений PrestaShop.

## Функции

### `CustomException.__init__`

```python
def __init__(self, message: str, e: Optional[Exception] = None, exc_info: bool = True):
    """Initializes the CustomException with a message and an optional original exception."""
    super().__init__(message)
    self.original_exception = e
    self.exc_info = exc_info
    self.handle_exception()
```

**Назначение**: Инициализирует объект `CustomException`.

**Параметры**:

- `message` (str): Сообщение об ошибке.
- `e` (Optional[Exception], optional): Исходное исключение, вызвавшее текущее исключение. По умолчанию `None`.
- `exc_info` (bool): Флаг, определяющий, нужно ли выводить информацию об исключении в лог. По умолчанию `True`.

**Возвращает**:
- None

**Как работает функция**:
1. Вызывается конструктор базового класса `Exception` с переданным сообщением об ошибке.
2. Сохраняется исходное исключение `e` в атрибуте `original_exception`.
3. Сохраняется значение флага `exc_info` в соответствующем атрибуте.
4. Вызывается метод `handle_exception` для обработки исключения.

```
Инициализация CustomException
│
├── message: str, e: Optional[Exception], exc_info: bool
│
│   Вызов конструктора базового класса Exception
│   │
│   ├── super().__init__(message)
│   │
│   Сохранение original_exception
│   │
│   ├── self.original_exception = e
│   │
│   Сохранение exc_info
│   │
│   ├── self.exc_info = exc_info
│   │
│   Вызов handle_exception
│   │
│   └── self.handle_exception()
│
Конец
```

**Примеры**:

```python
from src.logger.exceptions import CustomException

try:
    raise ValueError("Пример ошибки")
except ValueError as ex:
    raise CustomException("Произошла ошибка", ex)
```

### `CustomException.handle_exception`

```python
def handle_exception(self):
    """Handles the exception by logging the error and original exception, if available."""
    logger.error(f"Exception occurred: {self}")
    if self.original_exception:
        logger.debug(f"Original exception: {self.original_exception}")
    # Add recovery logic, retries, or other handling as necessary.
```

**Назначение**: Обрабатывает исключение, выполняя логирование ошибки и исходного исключения, если оно предоставлено.

**Параметры**:
- None

**Возвращает**:
- None

**Как работает функция**:
1. Выполняется логирование сообщения об ошибке с использованием `logger.error`.
2. Проверяется, существует ли исходное исключение `original_exception`.
3. Если исходное исключение существует, выполняется его логирование с использованием `logger.debug`.

```
handle_exception
│
├── Логирование сообщения об ошибке
│   │
│   └── logger.error(f"Exception occurred: {self}")
│
├── Проверка наличия original_exception
│   │
│   └── if self.original_exception:
│       │
│       └── Логирование original_exception
│           │
│           └── logger.debug(f"Original exception: {self.original_exception}")
│
Конец
```

**Примеры**:

```python
from src.logger.exceptions import CustomException
from src.logger import logger

try:
    raise ValueError("Пример ошибки")
except ValueError as ex:
    try:
        raise CustomException("Произошла ошибка", ex)
    except CustomException as cust_ex:
        logger.error(f"Custom Exception handled: {cust_ex}")
```

### `PrestaShopException.__init__`

```python
def __init__(self, msg: str, error_code: Optional[int] = None, 
             ps_error_msg: str = '', ps_error_code: Optional[int] = None):
    """Initializes the PrestaShopException with the provided message and error details."""
    self.msg = msg
    self.error_code = error_code
    self.ps_error_msg = ps_error_msg
    self.ps_error_code = ps_error_code
```

**Назначение**: Инициализирует объект `PrestaShopException`.

**Параметры**:

- `msg` (str): Сообщение об ошибке.
- `error_code` (Optional[int], optional): Код ошибки. По умолчанию `None`.
- `ps_error_msg` (str, optional): Сообщение об ошибке от PrestaShop. По умолчанию пустая строка.
- `ps_error_code` (Optional[int], optional): Код ошибки от PrestaShop. По умолчанию `None`.

**Возвращает**:
- None

**Как работает функция**:
1. Сохраняет сообщение об ошибке `msg` в атрибуте `self.msg`.
2. Сохраняет код ошибки `error_code` в атрибуте `self.error_code`.
3. Сохраняет сообщение об ошибке от PrestaShop `ps_error_msg` в атрибуте `self.ps_error_msg`.
4. Сохраняет код ошибки от PrestaShop `ps_error_code` в атрибуте `self.ps_error_code`.

```
Инициализация PrestaShopException
│
├── msg: str, error_code: Optional[int], ps_error_msg: str, ps_error_code: Optional[int]
│
│   Сохранение msg
│   │
│   ├── self.msg = msg
│   │
│   Сохранение error_code
│   │
│   ├── self.error_code = error_code
│   │
│   Сохранение ps_error_msg
│   │
│   ├── self.ps_error_msg = ps_error_msg
│   │
│   Сохранение ps_error_code
│   │
│   └── self.ps_error_code = ps_error_code
│
Конец
```

**Примеры**:

```python
from src.logger.exceptions import PrestaShopException

try:
    raise PrestaShopException("Ошибка при работе с PrestaShop", ps_error_msg="Неверный формат данных")
except PrestaShopException as ex:
    print(ex)
```

### `PrestaShopException.__str__`

```python
def __str__(self):
    """Returns the string representation of the exception."""
    return repr(self.ps_error_msg or self.msg)
```

**Назначение**: Возвращает строковое представление исключения.

**Параметры**:
- None

**Возвращает**:
- str: Строковое представление исключения.

**Как работает функция**:
1. Возвращает строковое представление атрибута `ps_error_msg`, если он не пустой, иначе возвращает строковое представление атрибута `msg`.

```
__str__
│
├── Проверка ps_error_msg на пустоту
│   │
│   └── if self.ps_error_msg:
│       │
│       └── Возврат repr(self.ps_error_msg)
│   │
│   └── else:
│       │
│       └── Возврат repr(self.msg)
│
Конец
```

**Примеры**:

```python
from src.logger.exceptions import PrestaShopException

try:
    raise PrestaShopException("Ошибка при работе с PrestaShop", ps_error_msg="Неверный формат данных")
except PrestaShopException as ex:
    print(ex)