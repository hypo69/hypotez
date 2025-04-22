# Модуль `any`

## Обзор

Модуль `any` содержит утилиты для преобразования данных различных типов в словари. В частности, он включает функцию `any2dict`, которая рекурсивно преобразует любой тип данных в словарь.

## Подробнее

Модуль предоставляет функцию `any2dict`, которая может быть полезна для преобразования сложных объектов в формат, удобный для сериализации (например, JSON) или для обработки данных, когда структура данных заранее неизвестна.

## Функции

### `any2dict`

```python
def any2dict(any_data: Any) -> dict | list | Any | bool:
    """
    Рекурсивно преобразует любой тип данных в словарь.

    Args:
        any_data: Любой тип данных.

    Returns:
        Словарь, представляющий входные данные, список или исходные данные, если преобразование возможно, иначе `False`.

    Как работает функция:
    - Функция проверяет тип входных данных `any_data`.
    - Если `any_data` является экземпляром класса, у которого есть атрибут `__dict__` (например, пользовательский класс),
      функция преобразует этот атрибут в словарь.
    - Если `any_data` является словарем, функция рекурсивно преобразует его ключи и значения.
    - Если `any_data` является списком, кортежем или множеством, функция рекурсивно преобразует каждый элемент.
    - Если `any_data` является базовым типом данных (int, float, str, bool, None), функция возвращает его без изменений.
    - Если тип данных не поддерживается, функция возвращает `False`.
    - В случае возникновения исключения во время преобразования, функция возвращает `False`.
    - Если рекурсивное преобразование ключа возвращает `False`, то ключ не включается в результирующий словарь.
    - Пустые значения преобразуются в пустые строки.

    Примеры:
    ```python
    data1 = {
        "name": "John",
        "age": 30,
        "address": {
            "city": "New York",
            "street": "Main St",
            "numbers":[1,2,3]
        },
        "phones": ["123-456-7890", "987-654-3210"],
        "skills": {"python", "java", "c++"}
    }
    print(any2dict(data1))
    # Вывод: {'name': 'John', 'age': 30, 'address': {'city': 'New York', 'street': 'Main St', 'numbers': [1, 2, 3]}, 'phones': ['123-456-7890', '987-654-3210'], 'skills': ['python', 'java', 'c++']}

    data2 = [1, 2, "three", {"key": "value"}]
    print(any2dict(data2))
    # Вывод: [1, 2, 'three', {'key': 'value'}]

    data3 = 123
    print(any2dict(data3))
    # Вывод: 123

    data4 = "string"
    print(any2dict(data4))
    # Вывод: string

    data5 = None
    print(any2dict(data5))
    # Вывод: None

    class MyClass:
        def __init__(self, x):
            self.x = x

    data6 = MyClass(10)
    print(any2dict(data6))
    # Вывод: {}

    import types
    # Тестируем SimpleNamespace
    data7 = types.SimpleNamespace(a=1, b='hello', c=[1,2,3])
    print(any2dict(data7))
    # Вывод: {'a': 1, 'b': 'hello', 'c': [1, 2, 3]}

    data8 = {'a':1, 'b': types.SimpleNamespace(x=2, y=3)}
    print(any2dict(data8))
    # Вывод: {'a': 1, 'b': {'x': 2, 'y': 3}}

    data9 = [types.SimpleNamespace(x=2), 3, 'str']
    print(any2dict(data9))
    # Вывод: [{'x': 2}, 3, 'str']

    data10 = types.SimpleNamespace(a=1, b=MyClass(3))
    print(any2dict(data10))
    # Вывод: {'a': 1, 'b': ''}
    
    data11 = {"a":1, "b": MyClass(10)}
    print(any2dict(data11))
    # Вывод: {'a': 1, 'b': ''}
    ```
    """
    if not isinstance(any_data, (set, list, int, float, str, bool, type(None))):
        result_dict = {}

        items_dict = None
        if hasattr(any_data, '__dict__'):
             items_dict = any_data.__dict__
        elif isinstance(any_data, dict):
             items_dict = any_data
        
        if not items_dict:
             return False
        try:
            for key, value in items_dict.items():
                converted_key = any2dict(key)
                converted_value = any2dict(value)
                if converted_key: # чтобы пустые значения тоже писало, надо проверять на то, что не False
                    result_dict[converted_key] = converted_value or ''

            return result_dict

        except Exception:
            return False

    elif isinstance(any_data, (list, tuple)):
        result_list = []
        for item in any_data:
            converted_item = any2dict(item)
            if converted_item is False:
                result_list.append('') # Пустая строка
            else:
                result_list.append(converted_item)
        return result_list

    elif isinstance(any_data, set):
        result_set = []
        for item in any_data:
            converted_item = any2dict(item)
            if converted_item is False:
                result_set.append('')
            else:
                result_set.append(converted_item)
        return result_set

    elif isinstance(any_data, (int, float, str, bool, type(None))):
        return any_data  # Базовые типы данных возвращаем как есть
    else:
      return False  # Неподдерживаемый тип данных.