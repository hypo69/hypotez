### **Анализ кода модуля `any.py`**

## \\file /src/utils/convertors/any.py

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код достаточно хорошо структурирован и выполняет поставленную задачу.
    - Присутствуют примеры использования, что облегчает понимание функциональности.
    - Используются аннотации типов.
- **Минусы**:
    - Отсутствует подробное описание модуля в начале файла.
    - Обработка исключений в функции `any2dict` не логирует ошибку.
    - Не все переменные аннотированы типами.
    - Присутствуют устаревшие элементы, такие как `header`.
    - Не хватает документации для параметров функций.
    - Примеры использования не следуют принятому стилю с `>>>`.

**Рекомендации по улучшению:**

1.  **Добавить описание модуля в начале файла**:

    ```python
    """
    Модуль для рекурсивного преобразования различных типов данных в словарь.
    ========================================================================

    Модуль содержит функцию :func:`any2dict`, которая рекурсивно преобразует любой тип данных в словарь,
    поддерживая вложенные структуры данных, такие как списки, кортежи, множества и пользовательские классы.

    Пример использования
    ----------------------

    >>> data = {"name": "John", "age": 30}
    >>> result = any2dict(data)
    >>> print(result)
    {'name': 'John', 'age': 30}
    """
    ```

2.  **Добавить логирование ошибок**:
    - В блоке `except Exception` функции `any2dict` добавить логирование ошибки с использованием `logger.error`.
    - Переименовать переменную исключения с `Exception` на `ex`.

    ```python
    from src.logger import logger

    try:
        for key, value in items_dict.items():
            converted_key = any2dict(key)
            converted_value = any2dict(value)
            if converted_key:  # чтобы пустые значения тоже писало, надо проверять на то, что не False
                result_dict[converted_key] = converted_value or ''

        return result_dict

    except Exception as ex:
        logger.error('Ошибка при преобразовании данных в словарь', ex, exc_info=True)
        return False
    ```

3.  **Добавить документацию для параметров функций**:

    ```python
    from typing import Any

    def any2dict(any_data: Any) -> dict | list | str | int | float | bool | None | False:
        """
        Рекурсивно преобразует любой тип данных в словарь.

        Args:
            any_data (Any): Данные любого типа для преобразования.

        Returns:
            dict | list | str | int | float | bool | None | False:  Словарь, представляющий входные данные,
            или False, если преобразование невозможно.
        """
    ```

4.  **Удалить устаревший импорт `header`**:

    ```python
    # REMOVE import header
    ```

5.  **Исправить примеры использования в `if __name__ == '__main__'`**:
    - Привести примеры использования к общепринятому виду с использованием `>>>`.
    - Добавить аннотации типов для переменных.

    ```python
    if __name__ == '__main__':
        import types

        # Примеры использования
        data1: dict = {
            'name': 'John',
            'age': 30,
            'address': {
                'city': 'New York',
                'street': 'Main St',
                'numbers': [1, 2, 3]
            },
            'phones': ['123-456-7890', '987-654-3210'],
            'skills': {'python', 'java', 'c++'}
        }

        print(any2dict(data1))
        # Вывод: {'name': 'John', 'age': 30, 'address': {'city': 'New York', 'street': 'Main St', 'numbers': [1, 2, 3]}, 'phones': ['123-456-7890', '987-654-3210'], 'skills': ['python', 'java', 'c++']}

        data2: list = [1, 2, 'three', {'key': 'value'}]
        print(any2dict(data2))
        # Вывод: [1, 2, 'three', {'key': 'value'}]

        data3: int = 123
        print(any2dict(data3))
        # Вывод: 123

        data4: str = 'string'
        print(any2dict(data4))
        # Вывод: string

        data5: None = None
        print(any2dict(data5))
        # Вывод: None

        class MyClass:
            def __init__(self, x: int):
                self.x: int = x

        data6: MyClass = MyClass(10)
        print(any2dict(data6))
        # Вывод: {}

        # Тестируем SimpleNamespace
        data7: types.SimpleNamespace = types.SimpleNamespace(a=1, b='hello', c=[1, 2, 3])
        print(any2dict(data7))
        # Вывод: {'a': 1, 'b': 'hello', 'c': [1, 2, 3]}

        data8: dict = {'a': 1, 'b': types.SimpleNamespace(x=2, y=3)}
        print(any2dict(data8))
        # Вывод: {'a': 1, 'b': {'x': 2, 'y': 3}}

        data9: list = [types.SimpleNamespace(x=2), 3, 'str']
        print(any2dict(data9))
        # Вывод: [{'x': 2}, 3, 'str']

        data10: types.SimpleNamespace = types.SimpleNamespace(a=1, b=MyClass(3))
        print(any2dict(data10))
        # Вывод: {'a': 1, 'b': ''}

        data11: dict = {'a': 1, 'b': MyClass(10)}
        print(any2dict(data11))
        # Вывод: {'a': 1, 'b': ''}
    ```

**Оптимизированный код:**

```python
## \\file /src/utils/convertors/any.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для рекурсивного преобразования различных типов данных в словарь.
========================================================================

Модуль содержит функцию :func:`any2dict`, которая рекурсивно преобразует любой тип данных в словарь,
поддерживая вложенные структуры данных, такие как списки, кортежи, множества и пользовательские классы.

Пример использования
----------------------

>>> data = {"name": "John", "age": 30}
>>> result = any2dict(data)
>>> print(result)
{'name': 'John', 'age': 30}
"""
from typing import Any, Optional, Union
import types
# REMOVE import header
from src.logger import logger


def any2dict(any_data: Any) -> dict | list | str | int | float | bool | None | False:
    """
    Рекурсивно преобразует любой тип данных в словарь.

    Args:
        any_data (Any): Данные любого типа для преобразования.

    Returns:
        dict | list | str | int | float | bool | None | False:  Словарь, представляющий входные данные,
        или False, если преобразование невозможно.
    """
    if not isinstance(any_data, (set, list, int, float, str, bool, type(None))):
        result_dict: dict = {}

        items_dict: Optional[dict] = None
        if hasattr(any_data, '__dict__'):
            items_dict = any_data.__dict__
        elif isinstance(any_data, dict):
            items_dict = any_data

        if not items_dict:
            return False
        try:
            for key, value in items_dict.items():
                converted_key: Any = any2dict(key)
                converted_value: Any = any2dict(value)
                if converted_key:  # чтобы пустые значения тоже писало, надо проверять на то, что не False
                    result_dict[converted_key] = converted_value or ''

            return result_dict

        except Exception as ex:
            logger.error('Ошибка при преобразовании данных в словарь', ex, exc_info=True)
            return False

    elif isinstance(any_data, (list, tuple)):
        result_list: list = []
        for item in any_data:
            converted_item: Any = any2dict(item)
            if converted_item is False:
                result_list.append('')  # Пустая строка
            else:
                result_list.append(converted_item)
        return result_list

    elif isinstance(any_data, set):
        result_set: list = []
        for item in any_data:
            converted_item: Any = any2dict(item)
            if converted_item is False:
                result_set.append('')
            else:
                result_set.append(converted_item)
        return result_set

    elif isinstance(any_data, (int, float, str, bool, type(None))):
        return any_data  # Базовые типы данных возвращаем как есть
    else:
        return False  # Неподдерживаемый тип данных.


if __name__ == '__main__':

    # Примеры использования
    data1: dict = {
        'name': 'John',
        'age': 30,
        'address': {
            'city': 'New York',
            'street': 'Main St',
            'numbers': [1, 2, 3]
        },
        'phones': ['123-456-7890', '987-654-3210'],
        'skills': {'python', 'java', 'c++'}
    }

    print(any2dict(data1))
    # Вывод: {'name': 'John', 'age': 30, 'address': {'city': 'New York', 'street': 'Main St', 'numbers': [1, 2, 3]}, 'phones': ['123-456-7890', '987-654-3210'], 'skills': ['python', 'java', 'c++']}

    data2: list = [1, 2, 'three', {'key': 'value'}]
    print(any2dict(data2))
    # Вывод: [1, 2, 'three', {'key': 'value'}]

    data3: int = 123
    print(any2dict(data3))
    # Вывод: 123

    data4: str = 'string'
    print(any2dict(data4))
    # Вывод: string

    data5: None = None
    print(any2dict(data5))
    # Вывод: None

    class MyClass:
        def __init__(self, x: int):
            self.x: int = x

    data6: 'MyClass' = MyClass(10)
    print(any2dict(data6))
    # Вывод: {}

    # Тестируем SimpleNamespace
    data7: types.SimpleNamespace = types.SimpleNamespace(a=1, b='hello', c=[1, 2, 3])
    print(any2dict(data7))
    # Вывод: {'a': 1, 'b': 'hello', 'c': [1, 2, 3]}

    data8: dict = {'a': 1, 'b': types.SimpleNamespace(x=2, y=3)}
    print(any2dict(data8))
    # Вывод: {'a': 1, 'b': {'x': 2, 'y': 3}}

    data9: list = [types.SimpleNamespace(x=2), 3, 'str']
    print(any2dict(data9))
    # Вывод: [{'x': 2}, 3, 'str']

    data10: types.SimpleNamespace = types.SimpleNamespace(a=1, b=MyClass(3))
    print(any2dict(data10))
    # Вывод: {'a': 1, 'b': ''}

    data11: dict = {'a': 1, 'b': MyClass(10)}
    print(any2dict(data11))
    # Вывод: {'a': 1, 'b': ''}