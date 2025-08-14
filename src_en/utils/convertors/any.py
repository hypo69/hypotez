
# # \file /src/utils/convertors/any.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

""".. module:: src.utils.convertors.any 
	:platform: Windows, Unix
	:synopsis: CSV and JSON conversion utilities"""
from typing import Any
import header
from src.logger import logger

def any2dict(any_data):
    """Recursively converts any type of data into a dictionary.

    Args:
      Any_Data: Any type of data.

    Returns:
      A dictionary representing input data, or false, if a conversion is impossible."""
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
                if converted_key: # In order for empty values to write too, it must be checked for the fact that not false
                    result_dict[converted_key] = converted_value or ''

            return result_dict

        except Exception: # removed ex and logging, as they did not ask
            return False

    elif isinstance(any_data, (list, tuple)):
        result_list = []
        for item in any_data:
            converted_item = any2dict(item)
            if converted_item is False:
                result_list.append('') # Empty line
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
        return any_data  # Basic types of data return as is
    else:
      return False  # Unsupported data type.

if __name__ == '__main__':
    import types
    # Examples of use
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
    # Conclusion: [1, 2, 'Three', {'Key': 'value'}]

    data3 = 123
    print(any2dict(data3))
    # Conclusion: 123

    data4 = "string"
    print(any2dict(data4))
    # Conclusion: String

    data5 = None
    print(any2dict(data5))
    # Conclusion: None

    class MyClass:
        def __init__(self, x):
            self.x = x

    data6 = MyClass(10)
    print(any2dict(data6))
    # Conclusion: {}

    # We test Simplenamespace
    data7 = types.SimpleNamespace(a=1, b='hello', c=[1,2,3])
    print(any2dict(data7))
    # Conclusion: {'a': 1, 'b': 'HELLO', 'C': [1, 2, 3]}}

    data8 = {'a':1, 'b': types.SimpleNamespace(x=2, y=3)}
    print(any2dict(data8))
    # Conclusion: {'a': 1, 'b': {'x': 2, 'y': 3}}

    data9 = [types.SimpleNamespace(x=2), 3, 'str']
    print(any2dict(data9))
    # Conclusion: [{'x': 2}, 3, 'str']

    data10 = types.SimpleNamespace(a=1, b=MyClass(3))
    print(any2dict(data10))
    # Conclusion: {'a': 1, 'b': ''}
    
    data11 = {"a":1, "b": MyClass(10)}
    print(any2dict(data11))
    # Conclusion: {'a': 1, 'b': ''}