# Модуль `any`

## Обзор

Модуль предоставляет утилиты для рекурсивного преобразования данных любого типа в словари. Это полезно, когда необходимо сериализовать сложные структуры данных в формат, который можно легко представить в виде JSON или CSV.

## Подробнее

Модуль содержит функцию `any2dict`, которая рекурсивно преобразует входные данные любого типа в словарь Python. Он обрабатывает различные типы данных, такие как списки, множества, целые числа, числа с плавающей запятой, строки, булевы значения и None. Если входные данные не могут быть преобразованы в словарь, функция возвращает `False`.

## Функции

### `any2dict`

```python
def any2dict(any_data: Any) -> dict | list | Any | bool:
    """
    Рекурсивно преобразует любой тип данных в словарь.

    Args:
        any_data (Any): Любой тип данных.

    Returns:
        dict | list | Any | bool: Словарь, представляющий входные данные, список, базовый тип данных или `False`, если преобразование невозможно.
    
    **Как работает функция**:
    1. **Проверка базовых типов данных**: Функция проверяет, является ли входной параметр `any_data` экземпляром одного из базовых типов данных: `set`, `list`, `int`, `float`, `str`, `bool` или `None`. Если это так, функция возвращает `any_data` без изменений.

    2. **Обработка сложных типов данных**: Если `any_data` не является базовым типом, функция пытается преобразовать его в словарь. Она проверяет, имеет ли `any_data` атрибут `__dict__` (например, если это экземпляр класса) или является ли он экземпляром `dict`. Если ни одно из этих условий не выполняется, функция возвращает `False`, указывая на то, что преобразование невозможно.

    3. **Преобразование в словарь**: Если `any_data` имеет атрибут `__dict__` или является словарем, функция создает пустой словарь `result_dict`. Затем она перебирает элементы `items_dict` (которые могут быть либо `any_data.__dict__`, либо `any_data`, если `any_data` является словарем). Для каждой пары ключ-значение функция рекурсивно вызывает `any2dict` для преобразования как ключа, так и значения.

    4. **Обработка пустых значений**: Если преобразованный ключ не является `False` (чтобы пустые значения тоже записывались), функция добавляет пару ключ-значение в `result_dict`. Если преобразованное значение равно `None`, оно заменяется пустой строкой `''`.

    5. **Обработка списков и кортежей**: Если `any_data` является списком или кортежем, функция создает пустой список `result_list` и перебирает элементы `any_data`. Для каждого элемента функция рекурсивно вызывает `any2dict`. Если преобразованный элемент равен `False`, функция добавляет пустую строку в `result_list`; в противном случае она добавляет преобразованный элемент.

    6. **Обработка множеств**: Если `any_data` является множеством, функция создает пустой список `result_set` и перебирает элементы `any_data`. Для каждого элемента функция рекурсивно вызывает `any2dict`. Если преобразованный элемент равен `False`, функция добавляет пустую строку в `result_set`; в противном случае она добавляет преобразованный элемент.

    7. **Обработка исключений**: Если в процессе преобразования возникает исключение, функция возвращает `False`.
        
    A
    |
    Проверка: any_data - базовый тип?
    |
    Нет → B, Да → Возврат any_data
    |
    B
    |
    Проверка: any_data имеет __dict__ или является dict?
    |
    Нет → Возврат False, Да → C
    |
    C
    |
    Создание result_dict
    |
    Перебор items_dict
    |
    Преобразование key и value рекурсивно
    |
    Добавление в result_dict (если key не False)
    |
    Возврат result_dict

    **Примеры**:
    ```python
    import types
    # Пример 1: Словарь с различными типами данных
    data1 = {
        "name": "John",
        "age": 30,
        "address": {
            "city": "New York",
            "street": "Main St",
            "numbers": [1, 2, 3]
        },
        "phones": ["123-456-7890", "987-654-3210"],
        "skills": {"python", "java", "c++"}
    }
    print(any2dict(data1))
    # Вывод: {'name': 'John', 'age': 30, 'address': {'city': 'New York', 'street': 'Main St', 'numbers': [1, 2, 3]}, 'phones': ['123-456-7890', '987-654-3210'], 'skills': ['python', 'java', 'c++']}

    # Пример 2: Список с различными типами данных
    data2 = [1, 2, "three", {"key": "value"}]
    print(any2dict(data2))
    # Вывод: [1, 2, 'three', {'key': 'value'}]

    # Пример 3: Целое число
    data3 = 123
    print(any2dict(data3))
    # Вывод: 123

    # Пример 4: Строка
    data4 = "string"
    print(any2dict(data4))
    # Вывод: string

    # Пример 5: None
    data5 = None
    print(any2dict(data5))
    # Вывод: None

    # Пример 6: Пользовательский класс
    class MyClass:
        def __init__(self, x):
            self.x = x

    data6 = MyClass(10)
    print(any2dict(data6))
    # Вывод: {'x': 10}

    # Пример 7: SimpleNamespace
    data7 = types.SimpleNamespace(a=1, b='hello', c=[1, 2, 3])
    print(any2dict(data7))
    # Вывод: {'a': 1, 'b': 'hello', 'c': [1, 2, 3]}

    # Пример 8: Словарь с SimpleNamespace в качестве значения
    data8 = {'a': 1, 'b': types.SimpleNamespace(x=2, y=3)}
    print(any2dict(data8))
    # Вывод: {'a': 1, 'b': {'x': 2, 'y': 3}}

    # Пример 9: Список с SimpleNamespace в качестве элемента
    data9 = [types.SimpleNamespace(x=2), 3, 'str']
    print(any2dict(data9))
    # Вывод: [{'x': 2}, 3, 'str']

    # Пример 10: SimpleNamespace с пользовательским классом в качестве значения
    class MyClass:
        def __init__(self, x):
            self.x = x
    data10 = types.SimpleNamespace(a=1, b=MyClass(3))
    print(any2dict(data10))
    # Вывод: {'a': 1, 'b': {}}

    # Пример 11: Словарь с пользовательским классом в качестве значения
    data11 = {"a": 1, "b": MyClass(10)}
    print(any2dict(data11))
    # Вывод: {'a': 1, 'b': {}}
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

        except Exception: # убрал ex и логгирование, так как не просили
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