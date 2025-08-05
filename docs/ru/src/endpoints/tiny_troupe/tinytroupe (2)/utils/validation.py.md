# Модуль для валидации данных
## \file hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/utils/validation.py

Модуль содержит функции для проверки корректности и очистки данных, включая проверку допустимых полей в словарях и санитарную обработку строк.

## Обзор

Этот модуль предоставляет набор функций для валидации и очистки данных. Основная цель модуля - обеспечение безопасности и корректности обрабатываемых данных. Он включает в себя функции для проверки допустимых полей в словарях и для санитарной обработки строк с целью удаления недопустимых символов и ограничения длины.

## Подробней

Модуль содержит функции для проверки допустимых полей в словарях, а также для очистки и нормализации строк. Это необходимо для предотвращения ошибок и уязвимостей, связанных с некорректными или вредоносными данными.

## Функции

### `check_valid_fields`

**Назначение**: Проверяет, все ли поля в предоставленном словаре допустимы в соответствии со списком допустимых полей.

```python
def check_valid_fields(obj: dict, valid_fields: list) -> None:
    """
    Checks whether the fields in the specified dict are valid, according to the list of valid fields. If not, raises a ValueError.
    """
    ...
```

**Параметры**:
- `obj` (dict): Словарь, поля которого необходимо проверить.
- `valid_fields` (list): Список допустимых полей.

**Возвращает**:
- `None`: Функция ничего не возвращает. В случае обнаружения недопустимого поля выбрасывается исключение `ValueError`.

**Вызывает исключения**:
- `ValueError`: Если обнаружено недопустимое поле в словаре `obj`.

**Как работает функция**:
- Функция итерируется по ключам словаря `obj`.
- Для каждого ключа проверяется, присутствует ли он в списке допустимых полей `valid_fields`.
- Если ключ не найден в списке допустимых полей, функция возбуждает исключение `ValueError` с сообщением об ошибке, содержащим недопустимый ключ и список допустимых ключей.

**Примеры**:
```python
# Пример 1: Все поля допустимы
valid_fields = ['name', 'age']
obj = {'name': 'John', 'age': 30}
check_valid_fields(obj, valid_fields)  # Функция не выбрасывает исключение

# Пример 2: Есть недопустимое поле
valid_fields = ['name', 'age']
obj = {'name': 'John', 'age': 30, 'city': 'New York'}
# check_valid_fields(obj, valid_fields)  # Функция выбрасывает ValueError: Invalid key city in dictionary. Valid keys are: ['name', 'age']
```

### `sanitize_raw_string`

**Назначение**: Очищает строку, удаляя недопустимые символы и обрезая ее до максимальной длины, разрешенной в Python.

```python
def sanitize_raw_string(value: str) -> str:
    """
    Sanitizes the specified string by: 
      - removing any invalid characters.
      - ensuring it is not longer than the maximum Python string length.
    
    This is for an abundance of caution with security, to avoid any potential issues with the string.
    """
    ...
```

**Параметры**:
- `value` (str): Строка, которую необходимо очистить.

**Возвращает**:
- `str`: Очищенная строка, обрезанная до `sys.maxsize`.

**Как работает функция**:
- Кодирует строку в формат UTF-8, игнорируя недопустимые символы, и декодирует обратно.
- Нормализует строку, используя форму NFC (Normalization Form Canonical Composition).
- Обрезает строку до максимальной длины, разрешенной в Python (`sys.maxsize`).

**Примеры**:
```python
# Пример 1: Очистка строки с недопустимыми символами
raw_string = "тест\x00строки"
sanitized_string = sanitize_raw_string(raw_string)
print(sanitized_string)  # Вывод: тестстроки

# Пример 2: Обрезание длинной строки
long_string = "A" * (sys.maxsize + 100)
sanitized_string = sanitize_raw_string(long_string)
print(len(sanitized_string))  # Вывод: sys.maxsize
```

### `sanitize_dict`

**Назначение**: Очищает словарь, применяя санитарную обработку ко всем строковым значениям.

```python
def sanitize_dict(value: dict) -> dict:
    """
    Sanitizes the specified dictionary by:
      - removing any invalid characters.
      - ensuring that the dictionary is not too deeply nested.
    """
    ...
```

**Параметры**:
- `value` (dict): Словарь, который необходимо очистить.

**Возвращает**:
- `dict`: Очищенный словарь, где все строковые значения прошли санитарную обработку.

**Как работает функция**:
- Функция итерируется по элементам словаря.
- Для каждого значения проверяется, является ли оно строкой.
- Если значение является строкой, вызывается функция `sanitize_raw_string` для его очистки.

**Примеры**:
```python
# Пример 1: Очистка словаря со строковыми значениями
raw_dict = {'name': "John\x00", 'age': 30, 'city': "New York"}
sanitized_dict = sanitize_dict(raw_dict)
print(sanitized_dict)  # Вывод: {'name': 'John', 'age': 30, 'city': 'New York'}

# Пример 2: Очистка словаря с различными типами данных
raw_dict = {'name': "Alice", 'age': 25, 'address': {'street': "Main\x00 St"}}
sanitized_dict = sanitize_dict(raw_dict)
print(sanitized_dict)  # Вывод: {'name': 'Alice', 'age': 25, 'address': {'street': 'Main\x00 St'}}