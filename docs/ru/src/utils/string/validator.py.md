# Модуль `src.utils.string.validator`

## Обзор

Модуль предоставляет класс `ProductFieldsValidator`, предназначенный для валидации различных строковых полей, таких как цена, вес, артикул и URL. Валидация включает проверку наличия данных, соответствие формату и другим критериям.

## Подробней

Этот модуль содержит инструменты для проверки соответствия строковых значений определенным критериям. Он может быть использован для проверки цен, веса, артикулов (SKU) и URL-адресов, чтобы убедиться, что они соответствуют ожидаемым форматам и требованиям.

## Классы

### `ProductFieldsValidator`

**Описание**: Класс, содержащий статические методы для валидации различных полей товара.

**Атрибуты**:
- Отсутствуют, так как класс содержит только статические методы.

**Методы**:
- `validate_price(price: str) -> bool`: Валидирует цену товара.
- `validate_weight(weight: str) -> bool`: Валидирует вес товара.
- `validate_sku(sku: str) -> bool`: Валидирует артикул товара.
- `validate_url(url: str) -> bool`: Валидирует URL товара.
- `isint(s: str) -> bool`: Проверяет, является ли строка целым числом.

## Методы класса

### `validate_price`

```python
@staticmethod
def validate_price(price: str) -> bool:
    """
    Выполняет валидацию цены товара.

    Args:
        price (str): Строка, представляющая цену товара.

    Returns:
        bool: `True`, если цена прошла валидацию, иначе `False`.

    
    - Если строка `price` пустая, функция ничего не возвращает (возвращает None).
    - Удаляет все символы, не являющиеся цифрами или запятой/точкой, используя регулярное выражение `Ptrn.clear_price`.
    - Заменяет запятую на точку для приведения к стандартному формату десятичного числа.
    - Пытается преобразовать строку в число с плавающей точкой. Если преобразование успешно, возвращает `True`, иначе `False`.

    Примеры:
        >>> ProductFieldsValidator.validate_price("100,00")
        True
        >>> ProductFieldsValidator.validate_price("100.00")
        True
        >>> ProductFieldsValidator.validate_price("abc")
        False
        >>> ProductFieldsValidator.validate_price("")
        
    """
    ...
```

### `validate_weight`

```python
@staticmethod
def validate_weight(weight: str) -> bool:
    """
    Выполняет валидацию веса товара.

    Args:
        weight (str): Строка, представляющая вес товара.

    Returns:
        bool: `True`, если вес прошел валидацию, иначе `False`.

    
    - Если строка `weight` пустая, функция ничего не возвращает (возвращает None).
    - Удаляет все символы, не являющиеся цифрами или запятой/точкой, используя регулярное выражение `Ptrn.clear_number`.
    - Заменяет запятую на точку для приведения к стандартному формату десятичного числа.
    - Пытается преобразовать строку в число с плавающей точкой. Если преобразование успешно, возвращает `True`, иначе `False`.

    Примеры:
        >>> ProductFieldsValidator.validate_weight("1.5")
        True
        >>> ProductFieldsValidator.validate_weight("abc")
        False
        >>> ProductFieldsValidator.validate_weight("")
        
    """
    ...
```

### `validate_sku`

```python
@staticmethod
def validate_sku(sku: str) -> bool:
    """
    Выполняет валидацию артикула (SKU) товара.

    Args:
        sku (str): Строка, представляющая артикул товара.

    Returns:
        bool: `True`, если артикул прошел валидацию, иначе `False`.

    
    - Если строка `sku` пустая, функция ничего не возвращает (возвращает None).
    - Удаляет специальные символы из строки, используя `StringFormatter.remove_special_characters`.
    - Удаляет символы переноса строки из строки, используя `StringFormatter.remove_line_breaks`.
    - Удаляет пробелы в начале и конце строки.
    - Проверяет длину строки: если она меньше 3 символов, возвращает `False`, иначе `True`.

    Примеры:
        >>> ProductFieldsValidator.validate_sku("ABC-123")
        True
        >>> ProductFieldsValidator.validate_sku("AB")
        False
        >>> ProductFieldsValidator.validate_sku("")
        
    """
    ...
```

### `validate_url`

```python
@staticmethod
def validate_url(url: str) -> bool:
    """
    Выполняет валидацию URL.

    Args:
        url (str): Строка, представляющая URL.

    Returns:
        bool: `True`, если URL прошел валидацию, иначе `False`.

    
    - Если строка `url` пустая, функция ничего не возвращает (возвращает None).
    - Удаляет пробелы в начале и конце строки.
    - Если URL не начинается с "http", добавляет "http://".
    - Пытается разобрать URL, используя `urlparse`.
    - Проверяет, что URL имеет схему и сетевое расположение (netloc). Если оба условия выполняются, возвращает `True`, иначе `False`.

    Примеры:
        >>> ProductFieldsValidator.validate_url("example.com")
        True
        >>> ProductFieldsValidator.validate_url("http://example.com")
        True
        >>> ProductFieldsValidator.validate_url("invalid url")
        False
        >>> ProductFieldsValidator.validate_url("")
        
    """
    ...
```

### `isint`

```python
@staticmethod
def isint(s: str) -> bool:
    """
    Проверяет, является ли строка целым числом.

    Args:
        s (str): Строка для проверки.

    Returns:
        bool: `True`, если строка является целым числом, иначе `None`.

    
    - Пытается преобразовать строку в целое число, используя `int()`.
    - Если преобразование успешно, возвращает `True`.
    - Если возникает исключение `Exception` во время преобразования, возвращает `None`.

    Примеры:
        >>> ProductFieldsValidator.isint("123")
        True
        >>> ProductFieldsValidator.isint("abc")
        
    """
    ...