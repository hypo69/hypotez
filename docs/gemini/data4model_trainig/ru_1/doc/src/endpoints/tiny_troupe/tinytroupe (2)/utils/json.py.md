# Модуль для работы с JSON и классами
=================================================

Модуль предоставляет функциональность для сериализации и десериализации объектов в формат JSON, а также инструменты для работы с классами, такие как регистрация подклассов и слияние словарей.

## Обзор

Модуль содержит класс `JsonSerializableRegistry`, который обеспечивает JSON-сериализацию, десериализацию и регистрацию подклассов. Также в модуле реализованы функции для слияния словарей (`merge_dicts`) и удаления дубликатов из списков (`remove_duplicates`).

## Подробней

Данный код используется для облегчения работы с JSON-представлением объектов, особенно когда требуется сохранять и восстанавливать состояние объектов, а также для упрощения работы с классами.
Он позволяет автоматизировать процесс сериализации и десериализации объектов, а также предоставляет удобные инструменты для работы со словарями и списками.

## Классы

### `JsonSerializableRegistry`

**Описание**: Предоставляет JSON сериализацию, десериализацию и регистрацию подклассов.

**Наследует**:

**Атрибуты**:
- `class_mapping` (dict): Словарь, содержащий соответствия между именами классов и самими классами. Используется для регистрации подклассов.

**Методы**:
- `to_json()`: Возвращает JSON представление объекта.
- `from_json()`: Загружает JSON представление объекта и создает экземпляр класса.
- `__init_subclass__()`: Регистрирует подкласс при создании.
- `_post_deserialization_init()`: Вызывается после десериализации объекта.
- `_programmatic_name_to_json_name()`: Преобразует имя атрибута в JSON-совместимое имя.
- `_json_name_to_programmatic_name()`: Преобразует JSON-совместимое имя в имя атрибута.

**Принцип работы**:
Класс `JsonSerializableRegistry` предоставляет механизм для автоматической сериализации и десериализации объектов в JSON-формат. Он использует атрибут `class_mapping` для регистрации подклассов, что позволяет восстанавливать объекты из JSON-представления, даже если они являются экземплярами подклассов. Методы `to_json` и `from_json` выполняют сериализацию и десериализацию соответственно, а метод `__init_subclass__` автоматически регистрирует подклассы при их создании. Методы `_programmatic_name_to_json_name` и `_json_name_to_programmatic_name` используются для преобразования имен атрибутов в формат, совместимый с JSON.

### `JsonSerializableRegistry.to_json`

```python
def to_json(self, include: list = None, suppress: list = None, file_path: str = None,
                serialization_type_field_name = "json_serializable_class_name") -> dict:
    """
    Returns a JSON representation of the object.
        
    Args:
        include (list, optional): Attributes to include in the serialization. Will override the default behavior.
        suppress (list, optional): Attributes to suppress from the serialization. Will override the default behavior.
        file_path (str, optional): Path to a file where the JSON will be written.
    """
    ...
```

**Назначение**:
Преобразует объект в JSON-совместимый словарь.

**Параметры**:
- `include` (list, optional): Список атрибутов, которые необходимо включить в сериализацию. Если указан, переопределяет поведение по умолчанию.
- `suppress` (list, optional): Список атрибутов, которые необходимо исключить из сериализации. Если указан, переопределяет поведение по умолчанию.
- `file_path` (str, optional): Путь к файлу, в который будет записан JSON.
- `serialization_type_field_name` (str): Имя поля, в котором будет храниться имя класса для сериализации.

**Возвращает**:
- `dict`: JSON-представление объекта в виде словаря.

**Как работает функция**:
Функция `to_json` преобразует объект в JSON-совместимый словарь. Сначала она собирает все сериализуемые атрибуты из иерархии классов, используя атрибуты `serializable_attributes` и `suppress_attributes_from_serialization`. Затем она переопределяет эти атрибуты, если переданы параметры `include` и `suppress`. После этого функция создает словарь, содержащий имя класса объекта и значения его атрибутов. Если значение атрибута является экземпляром `JsonSerializableRegistry`, списком или словарем, функция рекурсивно вызывает `to_json` для этого значения. Наконец, если указан параметр `file_path`, функция записывает JSON-представление объекта в файл.

**Примеры**:

```python
class MyClass(JsonSerializableRegistry):
    serializable_attributes = ['name', 'value']

    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

obj = MyClass(name='example', value=123)
json_data = obj.to_json()
print(json_data)
# {'json_serializable_class_name': 'MyClass', 'name': 'example', 'value': 123}

obj.to_json(file_path='example.json')  # JSON записан в файл example.json
```

### `JsonSerializableRegistry.from_json`

```python
    @classmethod
    def from_json(cls, json_dict_or_path, suppress: list = None, 
                  serialization_type_field_name = "json_serializable_class_name", 
                  post_init_params: dict = None):
        """
        Loads a JSON representation of the object and creates an instance of the class.
        
        Args:
            json_dict_or_path (dict or str): The JSON dictionary representing the object or a file path to load the JSON from.
            suppress (list, optional): Attributes to suppress from being loaded.
            
        Returns:
            An instance of the class populated with the data from json_dict_or_path.
        """
        ...
```

**Назначение**:
Создает экземпляр класса из JSON-представления.

**Параметры**:
- `json_dict_or_path` (dict или str): JSON-словарь, представляющий объект, или путь к файлу, содержащему JSON.
- `suppress` (list, optional): Список атрибутов, которые необходимо исключить из загрузки.
- `serialization_type_field_name` (str): Имя поля, в котором хранится имя класса для сериализации.
- `post_init_params` (dict, optional): Параметры, передаваемые в метод `_post_deserialization_init` после десериализации.

**Возвращает**:
- Экземпляр класса, заполненный данными из `json_dict_or_path`.

**Как работает функция**:
Функция `from_json` создает экземпляр класса из JSON-представления. Сначала она загружает JSON из файла или словаря, в зависимости от типа параметра `json_dict_or_path`. Затем она определяет класс, который необходимо создать, используя имя класса, хранящееся в JSON-словаре. После этого функция создает экземпляр класса, не вызывая метод `__init__`. Далее функция присваивает значения атрибутам экземпляра, используя данные из JSON-словаря. Если значение атрибута является экземпляром `JsonSerializableRegistry`, списком или словарем, функция рекурсивно вызывает `from_json` для этого значения. Наконец, функция вызывает метод `_post_deserialization_init`, если он существует.

**Примеры**:

```python
class MyClass(JsonSerializableRegistry):
    serializable_attributes = ['name', 'value']

    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

json_data = {'json_serializable_class_name': 'MyClass', 'name': 'example', 'value': 123}
obj = MyClass.from_json(json_data)
print(obj.name, obj.value)
# example 123

obj = MyClass.from_json('example.json')  # Объект создан из файла example.json
```

### `JsonSerializableRegistry.__init_subclass__`

```python
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Register the subclass using its name as the key
        JsonSerializableRegistry.class_mapping[cls.__name__] = cls
        
        # Automatically extend serializable attributes and custom initializers from parent classes 
        if hasattr(cls, 'serializable_attributes') and isinstance(cls.serializable_attributes, list):
            for base in cls.__bases__:
                if hasattr(base, 'serializable_attributes') and isinstance(base.serializable_attributes, list):
                    cls.serializable_attributes = list(set(base.serializable_attributes + cls.serializable_attributes))
        
        if hasattr(cls, 'suppress_attributes_from_serialization') and isinstance(cls.suppress_attributes_from_serialization, list):
            for base in cls.__bases__:
                if hasattr(base, 'suppress_attributes_from_serialization') and isinstance(base.suppress_attributes_from_serialization, list):
                    cls.suppress_attributes_from_serialization = list(set(base.suppress_attributes_from_serialization + cls.suppress_attributes_from_serialization))
        
        if hasattr(cls, 'custom_serialization_initializers') and isinstance(cls.custom_serialization_initializers, dict):
            for base in cls.__bases__:
                if hasattr(base, 'custom_serialization_initializers') and isinstance(base.custom_serialization_initializers, dict):
                    base_initializers = base.custom_serialization_initializers.copy()
                    base_initializers.update(cls.custom_serialization_initializers)
                    cls.custom_serialization_initializers = base_initializers
```

**Назначение**:
Регистрирует подкласс при создании и автоматически расширяет атрибуты сериализации и инициализаторы из родительских классов.

**Параметры**:
- `cls` (class): Создаваемый подкласс.
- `**kwargs`: Дополнительные параметры, передаваемые в конструктор подкласса.

**Как работает функция**:
Функция `__init_subclass__` вызывается автоматически при создании подкласса `JsonSerializableRegistry`. Она регистрирует подкласс в словаре `class_mapping`, используя имя класса в качестве ключа. Кроме того, функция автоматически расширяет атрибуты `serializable_attributes`, `suppress_attributes_from_serialization` и `custom_serialization_initializers` из родительских классов, что позволяет подклассам наследовать и расширять поведение сериализации и десериализации.

**Примеры**:

```python
class MyBaseClass(JsonSerializableRegistry):
    serializable_attributes = ['base_attr']

class MySubClass(MyBaseClass):
    serializable_attributes = ['sub_attr']

print(MySubClass.serializable_attributes)
# ['base_attr', 'sub_attr']
```

### `JsonSerializableRegistry._post_deserialization_init`

```python
    def _post_deserialization_init(self, **kwargs):
        # if there's a _post_init method, call it after deserialization
        if hasattr(self, '_post_init'):
            self._post_init(**kwargs)
```

**Назначение**:
Вызывает метод `_post_init` после десериализации объекта, если он существует.

**Параметры**:
- `self` (object): Экземпляр класса.
- `**kwargs`: Дополнительные параметры, передаваемые в метод `_post_init`.

**Как работает функция**:
Функция `_post_deserialization_init` вызывается после десериализации объекта. Она проверяет, существует ли метод `_post_init` в классе, и если да, то вызывает его, передавая дополнительные параметры `kwargs`. Этот метод позволяет выполнять дополнительную инициализацию объекта после десериализации.

**Примеры**:

```python
class MyClass(JsonSerializableRegistry):
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

    def _post_init(self):
        self.name = self.name.upper()

json_data = {'json_serializable_class_name': 'MyClass', 'name': 'example', 'value': 123}
obj = MyClass.from_json(json_data)
print(obj.name)
# EXAMPLE
```

### `JsonSerializableRegistry._programmatic_name_to_json_name`

```python
    @classmethod
    def _programmatic_name_to_json_name(cls, name):
        """
        Converts a programmatic name to a JSON name by converting it to snake case.
        """
        if hasattr(cls, 'serializable_attributes_renaming') and isinstance(cls.serializable_attributes_renaming, dict):
            return cls.serializable_attributes_renaming.get(name, name)
        return name
```

**Назначение**:
Преобразует имя атрибута в JSON-совместимое имя.

**Параметры**:
- `cls` (class): Класс, для которого выполняется преобразование.
- `name` (str): Имя атрибута.

**Возвращает**:
- JSON-совместимое имя атрибута.

**Как работает функция**:
Функция `_programmatic_name_to_json_name` преобразует имя атрибута в JSON-совместимое имя. Она проверяет, существует ли атрибут `serializable_attributes_renaming` в классе, и если да, то использует его для переименования атрибута. В противном случае функция возвращает исходное имя атрибута.

**Примеры**:

```python
class MyClass(JsonSerializableRegistry):
    serializable_attributes_renaming = {'my_attribute': 'myAttribute'}

print(MyClass._programmatic_name_to_json_name('my_attribute'))
# myAttribute
print(MyClass._programmatic_name_to_json_name('other_attribute'))
# other_attribute
```

### `JsonSerializableRegistry._json_name_to_programmatic_name`

```python
    @classmethod
    def _json_name_to_programmatic_name(cls, name):
        """
        Converts a JSON name to a programmatic name.
        """
        if hasattr(cls, 'serializable_attributes_renaming') and isinstance(cls.serializable_attributes_renaming, dict):
            reverse_rename = {}
            for k, v in cls.serializable_attributes_renaming.items():
                if v in reverse_rename:
                    raise ValueError(f"Duplicate value '{v}' found in serializable_attributes_renaming.")
                reverse_rename[v] = k
            return reverse_rename.get(name, name)
        return name
```

**Назначение**:
Преобразует JSON-совместимое имя в имя атрибута.

**Параметры**:
- `cls` (class): Класс, для которого выполняется преобразование.
- `name` (str): JSON-совместимое имя.

**Возвращает**:
- Имя атрибута.

**Как работает функция**:
Функция `_json_name_to_programmatic_name` преобразует JSON-совместимое имя в имя атрибута. Она проверяет, существует ли атрибут `serializable_attributes_renaming` в классе, и если да, то использует его для переименования атрибута в обратном порядке. В противном случае функция возвращает исходное имя атрибута.

**Примеры**:

```python
class MyClass(JsonSerializableRegistry):
    serializable_attributes_renaming = {'my_attribute': 'myAttribute'}

print(MyClass._json_name_to_programmatic_name('myAttribute'))
# my_attribute
print(MyClass._json_name_to_programmatic_name('other_attribute'))
# other_attribute
```

## Функции

### `post_init`

```python
def post_init(cls):
    """
    Decorator to enforce a post-initialization method call in a class, if it has one.
    The method must be named `_post_init`.
    """
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        if hasattr(cls, '_post_init'):
            cls._post_init(self)

    cls.__init__ = new_init
    return cls
```

**Назначение**:
Декоратор для обеспечения вызова метода постобработки инициализации в классе, если он есть.

**Параметры**:
- `cls` (class): Класс, к которому применяется декоратор.

**Как работает функция**:
Декоратор `post_init` заменяет оригинальный метод `__init__` класса на новый метод `new_init`. Новый метод вызывает оригинальный метод `__init__`, а затем проверяет, существует ли метод `_post_init` в классе. Если метод `_post_init` существует, он вызывается с экземпляром класса в качестве аргумента. Это позволяет выполнять дополнительную инициализацию объекта после его создания.

**Примеры**:

```python
@post_init
class MyClass:
    def __init__(self, name: str):
        self.name = name

    def _post_init(self):
        self.name = self.name.upper()

obj = MyClass(name='example')
print(obj.name)
# EXAMPLE
```

### `merge_dicts`

```python
def merge_dicts(current, additions, overwrite=False, error_on_conflict=True):
    """
    Merges two dictionaries and returns a new dictionary. Works as follows:
    - If a key exists in the additions dictionary but not in the current dictionary, it is added.
    - If a key maps to None in the current dictionary, it is replaced by the value in the additions dictionary.
    - If a key exists in both dictionaries and the values are dictionaries, the function is called recursively.
    - If a key exists in both dictionaries and the values are lists, the lists are concatenated and duplicates are removed.
    - If the values are of different types, an exception is raised.
    - If the values are of the same type but not both lists/dictionaries, the value from the additions dictionary overwrites the value in the current dictionary based on the overwrite parameter.
    
    Parameters:
    - current (dict): The original dictionary.
    - additions (dict): The dictionary with values to add.
    - overwrite (bool): Whether to overwrite values if they are of the same type but not both lists/dictionaries.
    - error_on_conflict (bool): Whether to raise an error if there is a conflict and overwrite is False.
    
    Returns:
    - dict: A new dictionary with merged values.
    """
    ...
```

**Назначение**:
Объединяет два словаря и возвращает новый словарь.

**Параметры**:
- `current` (dict): Исходный словарь.
- `additions` (dict): Словарь, значения которого необходимо добавить.
- `overwrite` (bool): Определяет, следует ли перезаписывать значения, если они имеют одинаковый тип, но не являются списками или словарями.
- `error_on_conflict` (bool): Определяет, следует ли вызывать исключение, если возникает конфликт и `overwrite` имеет значение `False`.

**Возвращает**:
- Новый словарь с объединенными значениями.

**Как работает функция**:
Функция `merge_dicts` объединяет два словаря и возвращает новый словарь. Она работает следующим образом:
- Если ключ существует в словаре `additions`, но не существует в словаре `current`, он добавляется.
- Если ключ сопоставлен со значением `None` в словаре `current`, он заменяется значением из словаря `additions`.
- Если ключ существует в обоих словарях, и значения являются словарями, функция вызывается рекурсивно.
- Если ключ существует в обоих словарях, и значения являются списками, списки объединяются, и дубликаты удаляются.
- Если значения имеют разные типы, вызывается исключение `TypeError`.
- Если значения имеют одинаковый тип, но не являются списками или словарями, значение из словаря `additions` перезаписывает значение в словаре `current` в зависимости от параметра `overwrite`.

**Примеры**:

```python
dict1 = {'a': 1, 'b': {'c': 2}}
dict2 = {'b': {'d': 3}, 'e': 4}
merged_dict = merge_dicts(dict1, dict2)
print(merged_dict)
# {'a': 1, 'b': {'c': 2, 'd': 3}, 'e': 4}

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}
merged_dict = merge_dicts(dict1, dict2, overwrite=True)
print(merged_dict)
# {'a': 1, 'b': 3, 'c': 4}
```

### `remove_duplicates`

```python
def remove_duplicates(lst):
    """
    Removes duplicates from a list while preserving order.
    Handles unhashable elements by using a list comprehension.

    Parameters:
    - lst (list): The list to remove duplicates from.

    Returns:
    - list: A new list with duplicates removed.
    """
    ...
```

**Назначение**:
Удаляет дубликаты из списка, сохраняя порядок элементов.

**Параметры**:
- `lst` (list): Список, из которого необходимо удалить дубликаты.

**Возвращает**:
- Новый список с удаленными дубликатами.

**Как работает функция**:
Функция `remove_duplicates` удаляет дубликаты из списка, сохраняя порядок элементов. Она использует список `seen` для отслеживания уже встреченных элементов. Если элемент является словарем, он преобразуется во множество `frozenset` для хеширования. Затем функция добавляет элемент в список `result`, только если он еще не встречался.

**Примеры**:

```python
lst = [1, 2, 2, 3, 4, 4, 5]
unique_lst = remove_duplicates(lst)
print(unique_lst)
# [1, 2, 3, 4, 5]

lst = [1, {'a': 1}, 2, {'a': 1}, 3]
unique_lst = remove_duplicates(lst)
print(unique_lst)
# [1, {'a': 1}, 2, 3]