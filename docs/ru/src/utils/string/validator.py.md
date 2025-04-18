# Модуль валидации строк

## Обзор

Модуль `validator.py` предназначен для валидации строк на соответствие определенным критериям и форматам. Он предоставляет класс `ProductFieldsValidator` с набором статических методов для проверки различных типов данных, таких как цена, вес, артикул и URL. Валидация может включать проверку наличия определенных символов, длины строки, соответствия регулярным выражениям и другие проверки.

## Подробнее

Модуль содержит класс `ProductFieldsValidator`, который предоставляет статические методы для валидации различных типов данных, используемых в продуктовых полях. Эти методы используются для проверки корректности данных перед их использованием или сохранением.
Данный модуль предназначен для проверки корректности введенных данных. Он определяет набор статических методов, каждый из которых отвечает за валидацию определенного типа данных (цена, вес, артикул, URL).

## Классы

### `ProductFieldsValidator`

**Описание**: Валидатор полей продукта. Предоставляет статические методы для проверки корректности различных полей продукта, таких как цена, вес, артикул (SKU) и URL.

**Принцип работы**:
Класс `ProductFieldsValidator` содержит статические методы, каждый из которых выполняет определенную проверку входной строки на соответствие заданным критериям. Методы возвращают `True`, если строка прошла валидацию, и `None`, если строка не прошла валидацию или была пустой.

**Методы**:

- `validate_price(price: str) -> bool`: Валидирует строку, представляющую цену продукта.
- `validate_weight(weight: str) -> bool`: Валидирует строку, представляющую вес продукта.
- `validate_sku(sku: str) -> bool`: Валидирует строку, представляющую артикул продукта (SKU).
- `validate_url(url: str) -> bool`: Валидирует строку, представляющую URL.
- `isint(s: str) -> bool`: Проверяет, является ли строка целым числом.

## Функции

### `validate_price`

```python
    @staticmethod
    def validate_price(price: str) -> bool:
        """
        Валидация цены
        """
```

**Назначение**: Валидация строки, представляющей цену продукта.

**Параметры**:

- `price` (str): Строка, содержащая цену продукта.

**Возвращает**:

- `bool`: `True`, если строка прошла валидацию, и `None`, если строка не прошла валидацию или была пустой.

**Как работает функция**:

1.  **Проверка на пустоту**: Если строка `price` пустая, функция возвращает `None`.
2.  **Очистка строки**: Из строки удаляются все символы, не являющиеся цифрами или разделителями, с помощью регулярного выражения `Ptrn.clear_price`.
3.  **Замена разделителя**: Заменяет запятую на точку, чтобы привести строку к формату, который можно преобразовать в число с плавающей точкой.
4.  **Преобразование в число**: Пытается преобразовать строку в число с плавающей точкой с помощью `float(price)`.
5.  **Обработка исключений**: Если преобразование не удалось, функция возвращает `None`.
6.  **Возврат результата**: Если преобразование удалось, функция возвращает `True`.

**Примеры**:

```python
ProductFieldsValidator.validate_price("100")   # Возвращает True
ProductFieldsValidator.validate_price("100,50") # Возвращает True
ProductFieldsValidator.validate_price("abc")   # Возвращает None
ProductFieldsValidator.validate_price("")      # Возвращает None
```

### `validate_weight`

```python
    @staticmethod
    def validate_weight(weight: str) -> bool:
        """
        Валидация веса
        """
```

**Назначение**: Валидация строки, представляющей вес продукта.

**Параметры**:

- `weight` (str): Строка, содержащая вес продукта.

**Возвращает**:

- `bool`: `True`, если строка прошла валидацию, и `None`, если строка не прошла валидацию или была пустой.

**Как работает функция**:

1.  **Проверка на пустоту**: Если строка `weight` пустая, функция возвращает `None`.
2.  **Очистка строки**: Из строки удаляются все символы, не являющиеся цифрами или разделителями, с помощью регулярного выражения `Ptrn.clear_number`.
3.  **Замена разделителя**: Заменяет запятую на точку, чтобы привести строку к формату, который можно преобразовать в число с плавающей точкой.
4.  **Преобразование в число**: Пытается преобразовать строку в число с плавающей точкой с помощью `float(weight)`.
5.  **Обработка исключений**: Если преобразование не удалось, функция возвращает `None`.
6.  **Возврат результата**: Если преобразование удалось, функция возвращает `True`.

**Примеры**:

```python
ProductFieldsValidator.validate_weight("100")   # Возвращает True
ProductFieldsValidator.validate_weight("100,50") # Возвращает True
ProductFieldsValidator.validate_weight("abc")   # Возвращает None
ProductFieldsValidator.validate_weight("")      # Возвращает None
```

### `validate_sku`

```python
    @staticmethod
    def validate_sku(sku: str) -> bool:
        """
        Валидация артикула
        """
```

**Назначение**: Валидация строки, представляющей артикул продукта (SKU).

**Параметры**:

- `sku` (str): Строка, содержащая артикул продукта.

**Возвращает**:

- `bool`: `True`, если строка прошла валидацию, и `None`, если строка не прошла валидацию или была пустой.

**Как работает функция**:

1.  **Проверка на пустоту**: Если строка `sku` пустая, функция возвращает `None`.
2.  **Очистка строки**: Из строки удаляются специальные символы с помощью `StringFormatter.remove_special_characters(sku)`.
3.  **Удаление переносов строк**: Из строки удаляются переносы строк с помощью `StringFormatter.remove_line_breaks(sku)`.
4.  **Удаление пробелов**: Удаляются начальные и конечные пробелы с помощью `sku.strip()`.
5.  **Проверка длины**: Если длина строки меньше 3 символов, функция возвращает `None`.
6.  **Возврат результата**: Если все проверки пройдены, функция возвращает `True`.

**Примеры**:

```python
ProductFieldsValidator.validate_sku("ABC")    # Возвращает True
ProductFieldsValidator.validate_sku("AB")     # Возвращает None
ProductFieldsValidator.validate_sku("")      # Возвращает None
ProductFieldsValidator.validate_sku("!@#ABC") # Возвращает True (после очистки специальных символов)
```

### `validate_url`

```python
    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Валидация URL
        """
```

**Назначение**: Валидация строки, представляющей URL.

**Параметры**:

- `url` (str): Строка, содержащая URL.

**Возвращает**:

- `bool`: `True`, если строка прошла валидацию, и `None`, если строка не прошла валидацию или была пустой.

**Как работает функция**:

1.  **Проверка на пустоту**: Если строка `url` пустая, функция возвращает `None`.
2.  **Удаление пробелов**: Удаляются начальные и конечные пробелы с помощью `url.strip()`.
3.  **Добавление протокола**: Если URL не начинается с `http`, добавляется `http://` в начало строки.
4.  **Разбор URL**: URL разбирается с помощью `urlparse(url)`.
5.  **Проверка наличия домена и схемы**: Если у разобранного URL отсутствуют домен (`netloc`) или схема (`scheme`), функция возвращает `None`.
6.  **Возврат результата**: Если все проверки пройдены, функция возвращает `True`.

**Примеры**:

```python
ProductFieldsValidator.validate_url("example.com")       # Возвращает True
ProductFieldsValidator.validate_url("http://example.com")  # Возвращает True
ProductFieldsValidator.validate_url("ftp://example.com")   # Возвращает True
ProductFieldsValidator.validate_url("")                   # Возвращает None
```

### `isint`

```python
    @staticmethod
    def isint(s: str) -> bool:
        """
        [Function's description]
        Parameters : 
            @param s : str  :  [description]
        Returns : 
            @return bool  :  [description]
        """
        try:
            s = int(s)
            return True
        except Exception as ex:
            return
```

**Назначение**: Проверка, является ли строка целым числом.

**Параметры**:

- `s` (str): Строка для проверки.

**Возвращает**:

- `bool`: `True`, если строка является целым числом, и `None` в противном случае.

**Как работает функция**:

1.  **Попытка преобразования**: Функция пытается преобразовать входную строку `s` в целое число с использованием `int(s)`.
2.  **Обработка исключений**: Если преобразование успешно, функция возвращает `True`. Если во время преобразования возникает исключение (например, `ValueError`), функция возвращает `None`.

**Примеры**:

```python
ProductFieldsValidator.isint("123")  # Возвращает True
ProductFieldsValidator.isint("abc")  # Возвращает None