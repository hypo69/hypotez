## Как использовать блок кода `validation.py`
=========================================================================================

Описание
-------------------------
Этот блок кода содержит функции для валидации и санитации данных. Он предоставляет функции для проверки наличия допустимых ключей в словаре, а также для очистки строк и словарей от потенциально опасных символов и для предотвращения слишком глубокой вложенности словарей.

Шаги выполнения
-------------------------
1. **Проверка допустимых полей**: Функция `check_valid_fields(obj: dict, valid_fields: list) -> None` проверяет, содержатся ли ключи словаря `obj` в списке допустимых ключей `valid_fields`. Если в словаре присутствуют недопустимые ключи, то функция выдает исключение `ValueError`.

2. **Санитация строки**: Функция `sanitize_raw_string(value: str) -> str`  чистит  строку `value` от недопустимых символов, делая ее строкой UTF-8,  нормализует ее, а затем обрезает до максимальной допустимой длины строки в Python. Это помогает предотвратить проблемы безопасности, связанные с использованием строки.

3. **Санитация словаря**: Функция `sanitize_dict(value: dict) -> dict` очищает словарь `value`. Она проходит по всем строковым значениям в словаре и очищает их с помощью функции `sanitize_raw_string`.  Затем функция возвращает словарь с очищенными значениями.

Пример использования
-------------------------

```python
from tinytroupe.utils import validation

# Пример использования функции `check_valid_fields`
data = {"name": "John", "age": 30, "city": "New York"}
valid_fields = ["name", "age"]

try:
    validation.check_valid_fields(data, valid_fields)
except ValueError as e:
    print(f"Ошибка валидации: {e}")

# Пример использования функции `sanitize_raw_string`
raw_string = "This string has invalid characters: <&>"
sanitized_string = validation.sanitize_raw_string(raw_string)
print(f"Исходная строка: {raw_string}")
print(f"Очищенная строка: {sanitized_string}")

# Пример использования функции `sanitize_dict`
data = {"name": "John <&>", "age": 30, "city": "New York"}
sanitized_data = validation.sanitize_dict(data)
print(f"Исходный словарь: {data}")
print(f"Очищенный словарь: {sanitized_data}")
```