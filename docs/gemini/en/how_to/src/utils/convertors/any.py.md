**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the `any2dict` Function
=========================================================================================

Description
-------------------------
The `any2dict` function converts any data type into a dictionary recursively. This includes various data types like sets, lists, integers, floats, strings, booleans, and even custom classes, if they have a `__dict__` attribute.

Execution Steps
-------------------------
1. **Type Check**: The function checks the type of the input data.
2. **Object Conversion**: If the input is an object, the function iterates through its `__dict__` attribute or the dictionary itself.
3. **Recursive Conversion**:  The `any2dict` function recursively calls itself on each key and value, ensuring all nested data is also converted to a dictionary.
4. **Basic Type Handling**: For basic data types like integers, floats, strings, booleans, and None, the function returns the data as is.
5. **Unsupported Types**: For unsupported data types, the function returns `False`.

Usage Example
-------------------------

```python
    # Example 1: Converting a dictionary with nested data
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
    # Output: {'name': 'John', 'age': 30, 'address': {'city': 'New York', 'street': 'Main St', 'numbers': [1, 2, 3]}, 'phones': ['123-456-7890', '987-654-3210'], 'skills': ['python', 'java', 'c++']}

    # Example 2: Converting a list with mixed data types
    data2 = [1, 2, "three", {"key": "value"}]
    print(any2dict(data2))
    # Output: [1, 2, 'three', {'key': 'value'}]

    # Example 3: Converting a simple integer
    data3 = 123
    print(any2dict(data3))
    # Output: 123

    # Example 4: Converting a custom class with a `__dict__` attribute
    class MyClass:
        def __init__(self, x):
            self.x = x

    data6 = MyClass(10)
    print(any2dict(data6))
    # Output: {'x': 10}
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".