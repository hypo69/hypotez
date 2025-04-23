# Модуль исключений для AliExpress API

## Обзор

Этот модуль содержит пользовательские исключения, используемые для обработки ошибок, связанных с API AliExpress. Все исключения наследуются от базового класса `AliexpressException`.

## Подробней

Модуль предназначен для обеспечения единообразного подхода к обработке ошибок при взаимодействии с API AliExpress. Он включает в себя исключения для различных сценариев, таких как неверные аргументы, отсутствие идентификатора товара, сбои запросов к API и неверные ответы. Использование этих исключений помогает улучшить читаемость кода и упростить отладку.

## Классы

### `AliexpressException`

**Описание**: Базовый класс для всех исключений, связанных с API AliExpress.

**Наследует**: `Exception`

**Атрибуты**:

-   `reason` (str): Причина возникновения исключения.

**Методы**:

-   `__init__(self, reason: str)`:
    *   **Назначение**: Инициализирует объект исключения с указанием причины.
    *   **Параметры**:
        *   `reason` (str): Причина возникновения исключения.
    *   **Возвращает**: `None`

-   `__str__(self) -> str`:
    *   **Назначение**: Возвращает строковое представление исключения, содержащее причину ошибки.
    *   **Параметры**: `None`
    *   **Возвращает**: `str`: Строковое представление исключения.

### `InvalidArgumentException`

**Описание**: Исключение, которое выбрасывается, когда аргументы, переданные в API, некорректны.

**Наследует**: `AliexpressException`

**Методы**: Отсутствуют

### `ProductIdNotFoundException`

**Описание**: Исключение, которое выбрасывается, когда идентификатор товара не найден.

**Наследует**: `AliexpressException`

**Методы**: Отсутствуют

### `ApiRequestException`

**Описание**: Исключение, которое выбрасывается, когда запрос к API AliExpress завершается неудачей.

**Наследует**: `AliexpressException`

**Методы**: Отсутствуют

### `ApiRequestResponseException`

**Описание**: Исключение, которое выбрасывается, когда ответ от API AliExpress недействителен.

**Наследует**: `AliexpressException`

**Методы**: Отсутствуют

### `ProductsNotFoudException`

**Описание**: Исключение, которое выбрасывается, когда товары не найдены.

**Наследует**: `AliexpressException`

**Методы**: Отсутствуют

### `CategoriesNotFoudException`

**Описание**: Исключение, которое выбрасывается, когда категории не найдены.

**Наследует**: `AliexpressException`

**Методы**: Отсутствуют

### `InvalidTrackingIdException`

**Описание**: Исключение, которое выбрасывается, когда идентификатор отслеживания отсутствует или недействителен.

**Наследует**: `AliexpressException`

**Методы**: Отсутствуют

## Методы класса

### `AliexpressException.__init__`

```python
def __init__(self, reason: str):
    """ Инициализирует объект исключения AliexpressException.

    Args:
        reason (str): Причина возникновения исключения.

    Returns:
        None

    """
```

### `AliexpressException.__str__`

```python
def __str__(self) -> str:
    """ Возвращает строковое представление исключения.

    Returns:
        str: Строковое представление исключения, содержащее причину ошибки.

    """
```

## Примеры

```python
from src.suppliers.aliexpress.api.errors.exceptions import ProductIdNotFoundException

try:
    product_id = "12345"
    # Попытка получить информацию о товаре с указанным ID
    # Если товар не найден, выбрасывается исключение ProductIdNotFoundException
    raise ProductIdNotFoundException(f"Товар с ID {product_id} не найден.")
except ProductIdNotFoundException as ex:
    print(f"Произошла ошибка: {ex}")  # Вывод: Произошла ошибка: Товар с ID 12345 не найден.
```
```python
from src.suppliers.aliexpress.api.errors.exceptions import InvalidArgumentException

try:
    # Попытка выполнить операцию с неверными аргументами
    raise InvalidArgumentException("Неверный тип аргумента.")
except InvalidArgumentException as ex:
    print(f"Произошла ошибка: {ex}")  # Вывод: Произошла ошибка: Неверный тип аргумента.
```
```python
from src.suppliers.aliexpress.api.errors.exceptions import ApiRequestException

try:
    # Имитация ошибки при запросе к API
    raise ApiRequestException("Ошибка при запросе к API AliExpress.")
except ApiRequestException as ex:
    print(f"Произошла ошибка: {ex}")  # Вывод: Произошла ошибка: Ошибка при запросе к API AliExpress.