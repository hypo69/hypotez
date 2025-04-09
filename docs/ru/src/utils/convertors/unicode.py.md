# Модуль для декодирования Unicode escape-последовательностей
=========================================================

Модуль содержит функцию :func:`decode_unicode_escape`, которая используется для преобразования строк, списков или словарей, содержащих Unicode escape-последовательности, в читаемый формат.

Пример использования
----------------------

```python
input_dict = {
    'product_name': r'\u05de\u05e7"\u05d8 \u05d9\u05e6\u05e8\u05df\nH510M K V2',
    'category': r'\u05e2\u05e8\u05db\u05ea \u05e9\u05d1\u05d1\u05d9\u05dd',
    'price': 123.45
}

input_list = [r'\u05e2\u05e8\u05db\u05ea \u05e9\u05d1\u05d1\u05d9\u05dd', r'H510M K V2']

input_string = r'\u05de\u05e7"\u05d8 \u05d9\u05e6\u05e8\u05df\nH510M K V2'

# Применяем функцию
decoded_dict = decode_unicode_escape(input_dict)
decoded_list = decode_unicode_escape(input_list)
decoded_string = decode_unicode_escape(input_string)

print(decoded_dict)
print(decoded_list)
print(decoded_string)
```

## Оглавление

- [Обзор](#обзор)
- [Подробнее](#подробнее)
- [Функции](#функции)
    - [`decode_unicode_escape`](#decode_unicode_escape)

## Обзор

Модуль предоставляет функцию для декодирования Unicode escape-последовательностей в строках, списках и словарях. Это полезно, когда необходимо преобразовать данные, содержащие Unicode символы, представленные в виде escape-последовательностей, в читаемый вид.

## Подробнее

Функция `decode_unicode_escape` рекурсивно обрабатывает входные данные, будь то словарь, список или строка. Если входные данные являются строкой, она пытается декодировать escape-последовательности. Если это словарь или список, функция рекурсивно применяется к каждому элементу или значению.

## Функции

### `decode_unicode_escape`

```python
def decode_unicode_escape(input_data: Dict[str, Any] | list | str) -> Dict[str, Any] | list | str:
    """Функция декодирует значения в словаре, списке или строке, содержащие юникодные escape-последовательности, в читаемый текст.

    Args:
        input_data (dict | list | str): Входные данные - словарь, список или строка, которые могут содержать юникодные escape-последовательности.

    Returns:
        dict | list | str: Преобразованные данные. В случае строки применяется декодирование escape-последовательностей. В случае словаря или списка рекурсивно обрабатываются все значения.

    Пример использования:
    .. code-block:: python
        input_dict = {
            'product_name': r'\u05de\u05e7"\u05d8 \u05d9\u05e6\u05e8\u05df\nH510M K V2',
            'category': r'\u05e2\u05e8\u05db\u05ea \u05e9\u05d1\u05d1\u05d9\u05dd',
            'price': 123.45
        }

        input_list = [r'\u05e2\u05e8\u05db\u05ea \u05e9\u05d1\u05d1\u05d9\u05dd', r'H510M K V2']

        input_string = r'\u05de\u05e7"\u05d8 \u05d9\u05e6\u05e8\u05df\nH510M K V2'

        # Применяем функцию
        decoded_dict = decode_unicode_escape(input_dict)
        decoded_list = decode_unicode_escape(input_list)
        decoded_string = decode_unicode_escape(input_string)

        print(decoded_dict)
        print(decoded_list)
        print(decoded_string)

    """
```

**Назначение**: Декодирует Unicode escape-последовательности в строках, списках и словарях.

**Параметры**:
- `input_data` (Dict[str, Any] | list | str): Входные данные, которые могут быть словарем, списком или строкой, содержащей Unicode escape-последовательности.

**Возвращает**:
- `Dict[str, Any] | list | str`: Преобразованные данные с декодированными Unicode escape-последовательностями.

**Как работает функция**:
1. **Проверка типа входных данных**: Определяется, является ли `input_data` словарем, списком или строкой.
2. **Обработка словаря**: Если `input_data` является словарем, функция рекурсивно вызывает саму себя для каждого значения в словаре.
3. **Обработка списка**: Если `input_data` является списком, функция рекурсивно вызывает саму себя для каждого элемента в списке.
4. **Обработка строки**: Если `input_data` является строкой, функция пытается декодировать Unicode escape-последовательности.
    - Сначала строка кодируется в формат UTF-8 и затем декодируется с использованием `unicode_escape`.
    - Затем происходит поиск всех последовательностей `\\uXXXX` (где XXXX - шестнадцатеричное число) и их преобразование в соответствующие Unicode символы.
5. **Обработка других типов данных**: Если тип входных данных не является словарем, списком или строкой, функция возвращает данные без изменений.

```
    Входные данные (input_data)
    │
    ├───Словарь?───Да
    │   │
    │   └───Рекурсивно обработать значения словаря
    │
    ├───Список?───Да
    │   │
    │   └───Рекурсивно обработать элементы списка
    │
    ├───Строка?───Да
    │   │
    │   └───Декодировать Unicode escape-последовательности
    │       │
    │       ├───Кодировать в UTF-8 и декодировать как unicode_escape
    │       │
    │       └───Найти и преобразовать все \\uXXXX последовательности
    │
    └───Другой тип данных
        │
        └───Вернуть без изменений
```

**Примеры**:

```python
input_dict = {
    'product_name': r'\u05de\u05e7"\u05d8 \u05d9\u05e6\u05e8\u05df\nH510M K V2',
    'category': r'\u05e2\u05e8\u05db\u05ea \u05e9\u05d1\u05d1\u05d9\u05dd',
    'price': 123.45
}

input_list = [r'\u05e2\u05e8\u05db\u05ea \u05e9\u05d1\u05d1\u05d9\u05dd', r'H510M K V2']

input_string = r'\u05de\u05e7"\u05d8 \u05d9\u05e6\u05e8\u05df\nH510M K V2'

# Применяем функцию
decoded_dict = decode_unicode_escape(input_dict)
decoded_list = decode_unicode_escape(input_list)
decoded_string = decode_unicode_escape(input_string)

print(decoded_dict)
print(decoded_list)
print(decoded_string)