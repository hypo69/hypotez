# Модуль для декодирования Unicode escape-последовательностей
==============================================================

Модуль содержит функцию `decode_unicode_escape`, которая используется для преобразования строк, списков или словарей, содержащих Unicode escape-последовательности, в читаемый вид.

Пример использования
----------------------

```python
input_dict = {
    'product_name': r'\u05de\u05e7\"\u05d8 \u05d9\u05e6\u05e8\u05df\nH510M K V2',
    'category': r'\u05e2\u05e8\u05db\u05ea \u05e9\u05d1\u05d1\u05d9\u05dd',
    'price': 123.45
}

input_list = [r'\u05e2\u05e8\u05db\u05ea \u05e9\u05d1\u05d1\u05d9\u05dd', r'H510M K V2']

input_string = r'\u05de\u05e7\"\u05d8 \u05d9\u05e6\u05e8\u05df\nH510M K V2'

# Применяем функцию
decoded_dict = decode_unicode_escape(input_dict)
decoded_list = decode_unicode_escape(input_list)
decoded_string = decode_unicode_escape(input_string)

print(decoded_dict)
print(decoded_list)
print(decoded_string)
```

## Оглавление
1. [Обзор](#обзор)
2. [Подробнее](#подробнее)
3. [Функции](#функции)
   - [`decode_unicode_escape`](#decode_unicode_escape)

## Обзор

Модуль предоставляет функциональность для обработки данных, содержащих Unicode escape-последовательности. Он может быть использован для очистки и форматирования текстовых данных, полученных из различных источников, таких как JSON-файлы или веб-страницы.

## Подробнее

Этот модуль содержит функцию `decode_unicode_escape`, которая рекурсивно обрабатывает словари и списки, а также преобразует строки, заменяя Unicode escape-последовательности на соответствующие символы. Функция использует регулярные выражения для поиска и замены escape-последовательностей.

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
            'product_name': r'\u05de\u05e7\"\u05d8 \u05d9\u05e6\u05e8\u05df\nH510M K V2',
            'category': r'\u05e2\u05e8\u05db\u05ea \u05e9\u05d1\u05d1\u05d9\u05dd',
            'price': 123.45
        }

        input_list = [r'\u05e2\u05e8\u05db\u05ea \u05e9\u05d1\u05d1\u05d9\u05dd', r'H510M K V2']

        input_string = r'\u05de\u05e7\"\u05d8 \u05d9\u05e6\u05e8\u05df\nH510M K V2'

        # Применяем функцию
        decoded_dict = decode_unicode_escape(input_dict)
        decoded_list = decode_unicode_escape(input_list)
        decoded_string = decode_unicode_escape(input_string)

        print(decoded_dict)
        print(decoded_list)
        print(decoded_string)

    """
```

**Назначение**: Декодирует значения в словаре, списке или строке, содержащие Unicode escape-последовательности, в читаемый текст.

**Параметры**:
- `input_data` (Dict[str, Any] | list | str): Входные данные, которые могут быть словарем, списком или строкой, содержащей Unicode escape-последовательности.

**Возвращает**:
- `Dict[str, Any] | list | str`: Преобразованные данные. В случае строки применяется декодирование escape-последовательностей. В случае словаря или списка рекурсивно обрабатываются все значения. Если тип данных не поддерживается, функция вернет данные без изменений.

**Как работает функция**:
1. **Проверка типа данных**: Функция проверяет тип входных данных (`input_data`).
2. **Обработка словаря**: Если входные данные - словарь, функция рекурсивно вызывает саму себя для каждого значения в словаре и возвращает новый словарь с декодированными значениями.
3. **Обработка списка**: Если входные данные - список, функция рекурсивно вызывает саму себя для каждого элемента в списке и возвращает новый список с декодированными элементами.
4. **Обработка строки**: Если входные данные - строка, функция пытается декодировать строку, используя кодировку `utf-8` и метод `unicode_escape`. Если происходит ошибка декодирования, строка возвращается без изменений.
5. **Дополнительная обработка для `\\\\uXXXX`**: Код преобразует все найденные последовательности `\\\\uXXXX`, используя регулярное выражение `r'\\\\u[0-9a-fA-F]{4}'`.
6. **Обработка других типов данных**: Если входные данные не являются словарем, списком или строкой, функция возвращает их без изменений.

**Примеры**:
```python
input_dict = {
    'product_name': r'\u05de\u05e7\"\u05d8 \u05d9\u05e6\u05e8\u05df\nH510M K V2',
    'category': r'\u05e2\u05e8\u05db\u05ea \u05e9\u05d1\u05d1\u05d9\u05dd',
    'price': 123.45
}
decoded_dict = decode_unicode_escape(input_dict)
print(decoded_dict)
# {'product_name': 'מק"ט יצרן\nH510M K V2', 'category': 'ערכת שבבים', 'price': 123.45}
```

```python
input_list = [r'\u05e2\u05e8\u05db\u05ea \u05e9\u05d1\u05d1\u05d9\u05dd', r'H510M K V2']
decoded_list = decode_unicode_escape(input_list)
print(decoded_list)
# ['ערכת שבבים', 'H510M K V2']
```

```python
input_string = r'\u05de\u05e7\"\u05d8 \u05d9\u05e6\u05e8\u05df\nH510M K V2'
decoded_string = decode_unicode_escape(input_string)
print(decoded_string)
# מק"ט יצרן
# H510M K V2