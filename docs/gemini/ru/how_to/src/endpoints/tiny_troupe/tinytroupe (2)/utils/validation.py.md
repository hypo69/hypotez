### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предоставляет набор функций для валидации и очистки данных, предназначенных для обработки в приложении Tiny Troupe. Он включает в себя проверку допустимости полей в словаре и очистку строк и словарей от потенциально опасных или нежелательных символов.

Шаги выполнения
-------------------------
1. **`check_valid_fields(obj: dict, valid_fields: list)`**:
   - Функция проверяет, все ли ключи в словаре `obj` содержатся в списке допустимых ключей `valid_fields`.
   - Если какой-либо ключ из `obj` отсутствует в `valid_fields`, функция вызывает исключение `ValueError` с сообщением об ошибке, указывающим недопустимый ключ и список допустимых ключей.

2. **`sanitize_raw_string(value: str)`**:
   - Функция очищает входную строку `value`, удаляя недопустимые символы и обрезая строку до максимальной длины, поддерживаемой Python.
   - Сначала строка кодируется в UTF-8 с игнорированием ошибок, а затем декодируется обратно в UTF-8 для удаления недопустимых символов.
   - Затем строка нормализуется в формате NFC для обеспечения консистентности Unicode.
   - В конце строка обрезается до `sys.maxsize`, чтобы избежать переполнения.

3. **`sanitize_dict(value: dict)`**:
   - Функция очищает словарь `value`, применяя функцию `sanitize_raw_string` ко всем строковым значениям в словаре.
   - Проходит по всем элементам словаря и, если значение является строкой, вызывает `sanitize_raw_string` для его очистки.
   - Возвращает очищенный словарь.

Пример использования
-------------------------

```python
import json
import sys
import unicodedata

from tinytroupe.utils import logger

################################################################################
# Validation
################################################################################
def check_valid_fields(obj: dict, valid_fields: list) -> None:
    """
    Checks whether the fields in the specified dict are valid, according to the list of valid fields. If not, raises a ValueError.
    """
    for key in obj:
        if key not in valid_fields:
            raise ValueError(f"Invalid key {key} in dictionary. Valid keys are: {valid_fields}")

def sanitize_raw_string(value: str) -> str:
    """
    Sanitizes the specified string by: 
      - removing any invalid characters.
      - ensuring it is not longer than the maximum Python string length.
    
    This is for an abundance of caution with security, to avoid any potential issues with the string.
    """

    # remove any invalid characters by making sure it is a valid UTF-8 string
    value = value.encode("utf-8", "ignore").decode("utf-8")

    value = unicodedata.normalize("NFC", value)


    # ensure it is not longer than the maximum Python string length
    return value[:sys.maxsize]

def sanitize_dict(value: dict) -> dict:
    """
    Sanitizes the specified dictionary by:
      - removing any invalid characters.
      - ensuring that the dictionary is not too deeply nested.
    """

    # sanitize the string representation of the dictionary
    for k, v in value.items():
        if isinstance(v, str):
            value[k] = sanitize_raw_string(v)

    # ensure that the dictionary is not too deeply nested
    return value

# Пример использования функций

# Пример 1: Проверка допустимых полей
data = {"name": "John", "age": 30, "city": "New York"}
valid_keys = ["name", "age"]

try:
    check_valid_fields(data, valid_keys)
except ValueError as e:
    print(f"Ошибка валидации: {e}")  # Выведет ошибку, так как "city" нет в списке допустимых ключей

# Пример 2: Очистка строки
raw_string = "Пример строки с недопустимыми символами: \x00, \uFFFF"
sanitized_string = sanitize_raw_string(raw_string)
print(f"Очищенная строка: {sanitized_string}")

# Пример 3: Очистка словаря
dirty_dict = {"name": "Alice", "description": "Описание с <скриптом> и символами \x00"}
clean_dict = sanitize_dict(dirty_dict)
print(f"Очищенный словарь: {clean_dict}")