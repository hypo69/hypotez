# Модуль validator

## Обзор

Модуль `validator` предоставляет класс `ProductFieldsValidator` с набором статических методов для валидации различных полей товара, таких как цена, вес, артикул (SKU) и URL. Валидация включает проверку формата, наличия символов и соответствия определенным критериям. Модуль использует регулярные выражения и другие вспомогательные функции для выполнения проверок.

## Подробнее

Модуль предназначен для обеспечения корректности данных, вводимых в систему, и предотвращения ошибок, связанных с некорректным форматом данных. Расположение файла в проекте указывает на то, что он является частью подсистемы обработки и валидации данных, используемой для работы с товарами.

## Классы

### `ProductFieldsValidator`

**Описание**: Класс `ProductFieldsValidator` предоставляет статические методы для валидации различных полей, связанных с товарами.

**Атрибуты**:
- Отсутствуют, так как класс содержит только статические методы.

**Методы**:
- `validate_price(price: str) -> bool`: Валидирует цену товара.
- `validate_weight(weight: str) -> bool`: Валидирует вес товара.
- `validate_sku(sku: str) -> bool`: Валидирует артикул товара.
- `validate_url(url: str) -> bool`: Валидирует URL.
- `isint(s: str) -> bool`: Проверяет, является ли строка целым числом.

## Методы класса

### `validate_price(price: str) -> bool`

```python
@staticmethod
def validate_price(price: str) -> bool:
    """
    Валидирует цену товара.

    Args:
        price (str): Цена товара в виде строки.

    Returns:
        bool: `True`, если цена валидна, иначе `None`.
    """
    ...
```

**Назначение**: Метод `validate_price` выполняет валидацию входной строки `price`, представляющей цену товара.

**Параметры**:
- `price` (str): Строка, содержащая цену товара.

**Возвращает**:
- `bool`: Возвращает `True`, если цена прошла валидацию, иначе `None`.

**Как работает функция**:
1. Если строка `price` пустая, функция немедленно возвращает `None`.
2. Очищает строку `price` от лишних символов с помощью регулярного выражения `Ptrn.clear_price`.
3. Заменяет запятые на точки для соответствия формату чисел с плавающей точкой.
4. Пытается преобразовать очищенную строку в число с плавающей точкой. Если преобразование успешно, возвращает `True`. Если происходит исключение, возвращает `None`.

**Примеры**:
```python
ProductFieldsValidator.validate_price("100,00")  # True
ProductFieldsValidator.validate_price("100.00")  # True
ProductFieldsValidator.validate_price("abc")     # None
ProductFieldsValidator.validate_price("")        # None
```

### `validate_weight(weight: str) -> bool`

```python
@staticmethod
def validate_weight(weight: str) -> bool:
    """
    Валидирует вес товара.

    Args:
        weight (str): Вес товара в виде строки.

    Returns:
        bool: `True`, если вес валиден, иначе `None`.
    """
    ...
```

**Назначение**: Метод `validate_weight` выполняет валидацию входной строки `weight`, представляющей вес товара.

**Параметры**:
- `weight` (str): Строка, содержащая вес товара.

**Возвращает**:
- `bool`: Возвращает `True`, если вес прошел валидацию, иначе `None`.

**Как работает функция**:
1. Если строка `weight` пустая, функция немедленно возвращает `None`.
2. Очищает строку `weight` от лишних символов с помощью регулярного выражения `Ptrn.clear_number`.
3. Заменяет запятые на точки для соответствия формату чисел с плавающей точкой.
4. Пытается преобразовать очищенную строку в число с плавающей точкой. Если преобразование успешно, возвращает `True`. Если происходит исключение, возвращает `None`.

**Примеры**:
```python
ProductFieldsValidator.validate_weight("1.5")   # True
ProductFieldsValidator.validate_weight("1,5")   # True
ProductFieldsValidator.validate_weight("abc")   # None
ProductFieldsValidator.validate_weight("")      # None
```

### `validate_sku(sku: str) -> bool`

```python
@staticmethod
def validate_sku(sku: str) -> bool:
    """
    Валидирует артикул товара.

    Args:
        sku (str): Артикул товара в виде строки.

    Returns:
        bool: `True`, если артикул валиден, иначе `None`.
    """
    ...
```

**Назначение**: Метод `validate_sku` выполняет валидацию входной строки `sku`, представляющей артикул товара.

**Параметры**:
- `sku` (str): Строка, содержащая артикул товара.

**Возвращает**:
- `bool`: Возвращает `True`, если артикул прошел валидацию, иначе `None`.

**Как работает функция**:
1. Если строка `sku` пустая, функция немедленно возвращает `None`.
2. Удаляет специальные символы из строки `sku` с помощью `StringFormatter.remove_special_characters`.
3. Удаляет переносы строк из строки `sku` с помощью `StringFormatter.remove_line_breaks`.
4. Удаляет начальные и конечные пробелы из строки `sku`.
5. Проверяет длину строки `sku`. Если длина меньше 3 символов, возвращает `None`.
6. Если все проверки пройдены, возвращает `True`.

**Примеры**:
```python
ProductFieldsValidator.validate_sku("ABC-123")  # True
ProductFieldsValidator.validate_sku("AB")       # None
ProductFieldsValidator.validate_sku("")        # None
```

### `validate_url(url: str) -> bool`

```python
@staticmethod
def validate_url(url: str) -> bool:
    """
    Валидирует URL.

    Args:
        url (str): URL в виде строки.

    Returns:
        bool: `True`, если URL валиден, иначе `None`.
    """
    ...
```

**Назначение**: Метод `validate_url` выполняет валидацию входной строки `url`, представляющей URL.

**Параметры**:
- `url` (str): Строка, содержащая URL.

**Возвращает**:
- `bool`: Возвращает `True`, если URL прошел валидацию, иначе `None`.

**Как работает функция**:
1. Если строка `url` пустая, функция немедленно возвращает `None`.
2. Удаляет начальные и конечные пробелы из строки `url`.
3. Если строка `url` не начинается с "http", добавляет "http://" в начало строки.
4. Пытается распарсить строку `url` с помощью `urlparse`.
5. Проверяет, что у распарсенного URL присутствуют атрибуты `netloc` (доменное имя) и `scheme` (схема протокола). Если они отсутствуют, возвращает `None`.
6. Если все проверки пройдены, возвращает `True`.

**Примеры**:
```python
ProductFieldsValidator.validate_url("example.com")       # True
ProductFieldsValidator.validate_url("http://example.com")  # True
ProductFieldsValidator.validate_url("example")           # None
ProductFieldsValidator.validate_url("")                # None
```

### `isint(s: str) -> bool`

```python
@staticmethod
def isint(s: str) -> bool:
    """
    Проверяет, является ли строка целым числом.

    Args:
        s (str): Строка для проверки.

    Returns:
        bool: `True`, если строка является целым числом, иначе `None`.
    """
    ...
```

**Назначение**: Метод `isint` проверяет, может ли входная строка `s` быть преобразована в целое число.

**Параметры**:
- `s` (str): Строка, которую необходимо проверить.

**Возвращает**:
- `bool`: Возвращает `True`, если строка может быть преобразована в целое число, иначе `None`.

**Как работает функция**:
1. Пытается преобразовать строку `s` в целое число с помощью `int(s)`.
2. Если преобразование успешно, возвращает `True`. Если происходит исключение, возвращает `None`.

**Примеры**:
```python
ProductFieldsValidator.isint("123")   # True
ProductFieldsValidator.isint("abc")   # None
ProductFieldsValidator.isint("")      # None