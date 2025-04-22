# Модуль `any2dict`

## Обзор

Модуль `any2dict` предоставляет утилиты для рекурсивного преобразования данных любого типа в словарь Python. Это может быть полезно при работе с данными, структура которых заранее неизвестна, или когда требуется унифицированное представление данных для дальнейшей обработки или сериализации.

## Подробнее

Модуль содержит функцию `any2dict`, которая рекурсивно обходит входные данные и преобразует их в словарь. Поддерживаются следующие типы данных:

- `dict` (словари)
- `list` (списки)
- `tuple` (кортежи)
- `set` (множества)
- `int` (целые числа)
- `float` (числа с плавающей точкой)
- `str` (строки)
- `bool` (булевы значения)
- `None` (значение `None`)
- Объекты классов, у которых есть атрибут `__dict__`

Если тип данных не поддерживается или происходит ошибка во время преобразования, функция возвращает `False`.

## Функции

### `any2dict`

```python
def any2dict(any_data) -> dict | list | str | int | float | bool | None | False:
    """Рекурсивно преобразует любой тип данных в словарь.

    Args:
        any_data: Любой тип данных.

    Returns:
        dict | list | str | int | float | bool | None | False: Словарь, представляющий входные данные, или `False`, если преобразование невозможно.

    Как работает функция:
    - Проверяет, является ли входной тип данных одним из базовых типов (set, list, int, float, str, bool, None).
    - Если входные данные не являются базовым типом, пытается получить словарь из атрибута __dict__ объекта или напрямую, если это словарь.
    - Если словарь получен, рекурсивно преобразует ключи и значения словаря.
    - Если входные данные являются списком, кортежем или множеством, рекурсивно преобразует каждый элемент.
    - Возвращает преобразованные данные или False в случае ошибки или неподдерживаемого типа данных.
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
                if converted_key:  # чтобы пустые значения тоже писало, надо проверять на то, что не False
                    result_dict[converted_key] = converted_value or ''

            return result_dict

        except Exception:
            return False

    elif isinstance(any_data, (list, tuple)):
        result_list = []
        for item in any_data:
            converted_item = any2dict(item)
            if converted_item is False:
                result_list.append('')  # Пустая строка
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

    """
    ### Внутренние функции
    Внутри функции `any2dict` нет внутренних функций.
    """

    """
    Примеры:

    Пример 1: Преобразование словаря
    ```python
    data = {"name": "John", "age": 30}
    result = any2dict(data)
    print(result)  # Вывод: {'name': 'John', 'age': 30}
    ```

    Пример 2: Преобразование списка
    ```python
    data = [1, 2, "three"]
    result = any2dict(data)
    print(result)  # Вывод: [1, 2, 'three']
    ```

    Пример 3: Преобразование объекта класса
    ```python
    class MyClass:
        def __init__(self, x):
            self.x = x

    data = MyClass(10)
    result = any2dict(data)
    print(result)  # Вывод: {'x': 10}
    ```

    Пример 4: Преобразование `SimpleNamespace`
    ```python
    import types
    data = types.SimpleNamespace(a=1, b='hello', c=[1,2,3])
    print(any2dict(data))
    # Вывод: {'a': 1, 'b': 'hello', 'c': [1, 2, 3]}
    ```

    Пример 5: Преобразование вложенных структур данных
    ```python
    import types
    class MyClass:
        def __init__(self, x):
            self.x = x

    data = {"a":1, "b": MyClass(10)}
    print(any2dict(data))
    # Вывод: {'a': 1, 'b': ''}
    ```
    """