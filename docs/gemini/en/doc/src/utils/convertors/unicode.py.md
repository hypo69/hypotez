# Модуль для работы с юникодными escape-последовательностями

## Обзор

Модуль предоставляет функцию `decode_unicode_escape`, которая декодирует юникодные escape-последовательности в текстовые данные. 

## Детали

Функция `decode_unicode_escape` предназначена для преобразования строк, словарей и списков, которые могут содержать юникодные escape-последовательности, в читаемый текст. 

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

**Описание**: Функция `decode_unicode_escape` принимает в качестве аргумента словарь, список или строку. Она проверяет тип входных данных. Если это словарь, то рекурсивно обрабатывает все значения в нем. Если это список, то рекурсивно обрабатывает каждый элемент списка. Если это строка, то функция декодирует ее, используя методы `encode` и `decode` для преобразования юникодных escape-последовательностей в читаемый текст. В случае, если входные данные не относятся к поддерживаемым типам, функция возвращает их без изменений.

**Как работает**: Функция `decode_unicode_escape` работает следующим образом:

1. **Проверяет тип входных данных**: Проверяет, является ли входные данные словарем, списком или строкой.
2. **Рекурсивная обработка**: Если входные данные представляют собой словарь, то рекурсивно вызывается функция `decode_unicode_escape` для обработки значений словаря. Аналогично, если это список, то рекурсивно вызывается функция для обработки элементов списка.
3. **Декодирование строки**: Если входные данные представляют собой строку, то функция сначала пытается декодировать ее с помощью метода `encode` с кодировкой `utf-8` и `decode` с кодировкой `unicode_escape`. Если это приводит к ошибке, то функция возвращает исходную строку.
4. **Преобразование escape-последовательностей**: Затем функция находит все escape-последовательности вида `\\uXXXX` в строке. 
5. **Возвращает результат**: После преобразования escape-последовательностей функция возвращает преобразованную строку.

**Примеры**: 

**Пример 1**:

```python
>>> input_data = {'key1': r'\u041f\u0440\u0438\u0432\u0435\u0442', 'key2': 123}
>>> decode_unicode_escape(input_data)
{'key1': 'Привет', 'key2': 123}
```

**Пример 2**:

```python
>>> input_data = ['\u041f\u0440\u0438\u0432\u0435\u0442', 'World']
>>> decode_unicode_escape(input_data)
['Привет', 'World']
```

**Пример 3**:

```python
>>> input_data = r'\u041f\u0440\u0438\u0432\u0435\u0442'
>>> decode_unicode_escape(input_data)
'Привет'
```

**Пример 4**:

```python
>>> input_data = 123
>>> decode_unicode_escape(input_data)
123