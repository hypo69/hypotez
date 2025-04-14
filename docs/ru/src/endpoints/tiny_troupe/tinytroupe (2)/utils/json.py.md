# Модуль для работы с JSON и регистрацией классов
=================================================

Модуль предоставляет класс `JsonSerializableRegistry`, который обеспечивает JSON сериализацию, десериализацию и регистрацию подклассов.
Также содержит функции для слияния словарей и удаления дубликатов из списков.

## Обзор

Этот модуль предназначен для облегчения работы с JSON-сериализацией и десериализацией объектов, а также для регистрации подклассов. Он предоставляет класс `JsonSerializableRegistry`, который можно использовать в качестве базового класса для классов, требующих JSON-сериализации. Также, модуль содержит функции для слияния словарей (`merge_dicts`) и удаления дубликатов из списков (`remove_duplicates`), что может быть полезно при работе с данными.

## Подробнее

Модуль содержит класс `JsonSerializableRegistry`, который позволяет классам автоматически регистрировать свои подклассы и обеспечивает методы для преобразования объектов в JSON и обратно. Это полезно для сохранения и восстановления состояния объектов, а также для передачи данных между различными частями приложения или между приложениями.

Функция `merge_dicts` позволяет объединять два словаря, обрабатывая различные типы данных и разрешая конфликты при совпадении ключей. Функция `remove_duplicates` удаляет дубликаты из списка, сохраняя порядок элементов.

## Классы

### `JsonSerializableRegistry`

**Описание**: Предоставляет методы для JSON сериализации, десериализации и регистрации подклассов.

**Наследует**: Нет

**Атрибуты**:
- `class_mapping` (dict): Словарь, хранящий соответствие между именами классов и самими классами.
- `serializable_attributes` (list): Список атрибутов, которые должны быть сериализованы в JSON.
- `suppress_attributes_from_serialization` (list): Список атрибутов, которые не должны быть сериализованы в JSON.
- `custom_serialization_initializers` (dict): Словарь, содержащий пользовательские функции инициализации для атрибутов при десериализации.
- `serializable_attributes_renaming` (dict): Словарь, содержащий переименования атрибутов при сериализации и десериализации.

**Методы**:
- `to_json`: Преобразует объект в JSON-представление.
- `from_json`: Создает экземпляр класса из JSON-представления.
- `__init_subclass__`: Автоматически регистрирует подклассы.
- `_post_deserialization_init`: Вызывает метод `_post_init` после десериализации.
- `_programmatic_name_to_json_name`: Преобразует имя атрибута в имя для JSON.
- `_json_name_to_programmatic_name`: Преобразует имя атрибута из JSON в имя атрибута класса.

**Принцип работы**:

Класс `JsonSerializableRegistry` предоставляет функциональность для автоматической сериализации и десериализации объектов в JSON. Он использует атрибут `class_mapping` для хранения соответствия между именами классов и самими классами, что позволяет восстанавливать объекты из JSON-представления. Методы `to_json` и `from_json` выполняют преобразование объектов в JSON и обратно, соответственно. Метод `__init_subclass__` автоматически регистрирует подклассы при их создании.

### Методы класса

#### `to_json`

```python
def to_json(self, include: list = None, suppress: list = None, file_path: str = None,
            serialization_type_field_name = "json_serializable_class_name") -> dict:
    """
    Возвращает JSON представление объекта.

    Args:
        include (list, optional): Атрибуты для включения в сериализацию. Переопределяет поведение по умолчанию.
        suppress (list, optional): Атрибуты для исключения из сериализации. Переопределяет поведение по умолчанию.
        file_path (str, optional): Путь к файлу, куда будет записан JSON.
        serialization_type_field_name (str, optional): Имя поля, содержащего имя класса при сериализации. По умолчанию "json_serializable_class_name".

    Returns:
        dict: JSON представление объекта.
    """
```

**Назначение**: Преобразует объект в JSON-представление.

**Параметры**:
- `include` (list, optional): Список атрибутов, которые необходимо включить в JSON-представление. Если указан, то только эти атрибуты будут включены. По умолчанию `None`.
- `suppress` (list, optional): Список атрибутов, которые необходимо исключить из JSON-представления. Если указан, то указанные атрибуты будут исключены. По умолчанию `None`.
- `file_path` (str, optional): Путь к файлу, в который необходимо записать JSON-представление. Если указан, то JSON будет записан в файл. По умолчанию `None`.
- `serialization_type_field_name` (str, optional): Имя поля, которое будет содержать имя класса при сериализации. По умолчанию `"json_serializable_class_name"`.

**Возвращает**:
- `dict`: JSON-представление объекта в виде словаря.

**Как работает функция**:
- Собирает все сериализуемые атрибуты из иерархии классов.
- Переопределяет атрибуты с параметрами метода, если они предоставлены.
- Создает словарь, содержащий имя класса и значения атрибутов.
- Рекурсивно вызывает `to_json` для атрибутов, являющихся экземплярами `JsonSerializableRegistry`, списками или словарями.
- Записывает JSON в файл, если указан `file_path`.

**Примеры**:

```python
class MyClass(JsonSerializableRegistry):
    serializable_attributes = ['attr1', 'attr2']

    def __init__(self, attr1, attr2, attr3):
        self.attr1 = attr1
        self.attr2 = attr2
        self.attr3 = attr3

obj = MyClass('value1', 'value2', 'value3')
json_data = obj.to_json()
print(json_data)
# {'json_serializable_class_name': 'MyClass', 'attr1': 'value1', 'attr2': 'value2'}

json_data_with_include = obj.to_json(include=['attr1'])
print(json_data_with_include)
# {'json_serializable_class_name': 'MyClass', 'attr1': 'value1'}

json_data_with_suppress = obj.to_json(suppress=['attr2'])
print(json_data_with_suppress)
# {'json_serializable_class_name': 'MyClass', 'attr1': 'value1'}
```

#### `from_json`

```python
@classmethod
def from_json(cls, json_dict_or_path, suppress: list = None, 
              serialization_type_field_name = "json_serializable_class_name", 
              post_init_params: dict = None):
    """
    Загружает JSON представление объекта и создает экземпляр класса.

    Args:
        json_dict_or_path (dict or str): JSON словарь, представляющий объект, или путь к файлу, содержащему JSON.
        suppress (list, optional): Атрибуты для исключения из загрузки.
        serialization_type_field_name (str, optional): Имя поля, содержащего имя класса при сериализации. По умолчанию "json_serializable_class_name".
        post_init_params (dict, optional): Параметры для передачи в метод `_post_deserialization_init`.

    Returns:
        An instance of the class populated with the data from json_dict_or_path.
    """
```

**Назначение**: Создает экземпляр класса из JSON-представления.

**Параметры**:
- `json_dict_or_path` (dict | str): JSON-словарь, представляющий объект, или путь к файлу, содержащему JSON.
- `suppress` (list, optional): Список атрибутов, которые следует исключить при десериализации. По умолчанию `None`.
- `serialization_type_field_name` (str, optional): Имя поля, содержащего имя класса при сериализации. По умолчанию `"json_serializable_class_name"`.
- `post_init_params` (dict, optional): Параметры, которые будут переданы в метод `_post_deserialization_init`, если он существует. По умолчанию `None`.

**Возвращает**:
- Экземпляр класса, заполненный данными из `json_dict_or_path`.

**Как работает функция**:
- Загружает JSON из файла или использует предоставленный словарь.
- Определяет класс, который необходимо создать, на основе имени класса, указанного в JSON.
- Создает экземпляр класса без вызова `__init__`.
- Присваивает значения атрибутам экземпляра на основе данных из JSON.
- Рекурсивно вызывает `from_json` для атрибутов, являющихся экземплярами `JsonSerializableRegistry`, списками или словарями.
- Вызывает метод `_post_deserialization_init`, если он существует.

**Примеры**:

```python
class MyClass(JsonSerializableRegistry):
    serializable_attributes = ['attr1', 'attr2']

    def __init__(self, attr1, attr2, attr3):
        self.attr1 = attr1
        self.attr2 = attr2
        self.attr3 = attr3

    def _post_deserialization_init(self, param1=None):
        self.attr4 = param1

json_data = {'json_serializable_class_name': 'MyClass', 'attr1': 'value1', 'attr2': 'value2'}
obj = MyClass.from_json(json_data, post_init_params={'param1': 'value4'})
print(obj.attr1)  # value1
print(obj.attr2)  # value2
print(hasattr(obj, 'attr3'))  # False
print(obj.attr4)  # value4
```

#### `__init_subclass__`

```python
def __init_subclass__(cls, **kwargs):
    """
    Регистрирует подкласс.

    Args:
        **kwargs: Дополнительные аргументы.
    """
```

**Назначение**: Автоматически регистрирует подклассы при их создании.

**Параметры**:
- `**kwargs`: Дополнительные аргументы.

**Как работает функция**:
- Регистрирует подкласс в `JsonSerializableRegistry.class_mapping`.
- Автоматически расширяет `serializable_attributes`, `suppress_attributes_from_serialization` и `custom_serialization_initializers` из родительских классов.

**Примеры**:

```python
class MyClass(JsonSerializableRegistry):
    serializable_attributes = ['attr1']

class MySubClass(MyClass):
    serializable_attributes = ['attr2']

print(MyClass.serializable_attributes) # ['attr1']
print(MySubClass.serializable_attributes) # ['attr1', 'attr2']
print(JsonSerializableRegistry.class_mapping['MySubClass']) # <class '__main__.MySubClass'>
```

#### `_post_deserialization_init`

```python
def _post_deserialization_init(self, **kwargs):
    """
    Вызывает метод `_post_init` после десериализации.

    Args:
        **kwargs: Дополнительные аргументы.
    """
```

**Назначение**: Вызывает метод `_post_init` после десериализации, если он существует.

**Параметры**:
- `**kwargs`: Дополнительные аргументы.

**Как работает функция**:
- Если у экземпляра класса есть метод `_post_init`, он вызывается с переданными аргументами.

**Примеры**:

```python
class MyClass(JsonSerializableRegistry):
    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2

    def _post_init(self, param1=None):
        self.attr3 = param1

json_data = {'json_serializable_class_name': 'MyClass', 'attr1': 'value1', 'attr2': 'value2'}
obj = MyClass.from_json(json_data)
obj._post_deserialization_init(param1='value3')
print(obj.attr3) # value3
```

#### `_programmatic_name_to_json_name`

```python
@classmethod
def _programmatic_name_to_json_name(cls, name):
    """
    Преобразует программное имя в JSON имя, преобразуя его в snake case.
    """
```

**Назначение**: Преобразует имя атрибута в имя для JSON.

**Параметры**:
- `name` (str): Имя атрибута.

**Возвращает**:
- `str`: Имя атрибута для JSON.

**Как работает функция**:
- Если у класса есть атрибут `serializable_attributes_renaming`, используется он для переименования.
- В противном случае возвращается исходное имя.

**Примеры**:

```python
class MyClass(JsonSerializableRegistry):
    serializable_attributes_renaming = {'attr1': 'attr_1'}

print(MyClass._programmatic_name_to_json_name('attr1')) # attr_1
print(MyClass._programmatic_name_to_json_name('attr2')) # attr2
```

#### `_json_name_to_programmatic_name`

```python
@classmethod
def _json_name_to_programmatic_name(cls, name):
    """
    Преобразует JSON имя в программное имя.
    """
```

**Назначение**: Преобразует имя атрибута из JSON в имя атрибута класса.

**Параметры**:
- `name` (str): Имя атрибута в JSON.

**Возвращает**:
- `str`: Имя атрибута класса.

**Как работает функция**:
- Если у класса есть атрибут `serializable_attributes_renaming`, используется он для переименования.
- В противном случае возвращается исходное имя.

**Примеры**:

```python
class MyClass(JsonSerializableRegistry):
    serializable_attributes_renaming = {'attr1': 'attr_1'}

print(MyClass._json_name_to_programmatic_name('attr_1')) # attr1
print(MyClass._json_name_to_programmatic_name('attr2')) # attr2
```

## Функции

### `post_init`

```python
def post_init(cls):
    """
    Декоратор для принудительного вызова метода постобработки инициализации в классе, если он есть.
    Метод должен называться `_post_init`.
    """
```

**Назначение**: Декоратор для принудительного вызова метода постобработки инициализации в классе, если он есть.

**Параметры**:
- `cls` (class): Класс, к которому применяется декоратор.

**Как работает функция**:
- Заменяет оригинальный метод `__init__` класса на новый, который вызывает оригинальный метод `__init__`, а затем метод `_post_init`, если он существует.

**Примеры**:

```python
@post_init
class MyClass:
    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2

    def _post_init(self):
        self.attr3 = self.attr1 + self.attr2

obj = MyClass('value1', 'value2')
print(obj.attr3) # value1value2
```

### `merge_dicts`

```python
def merge_dicts(current, additions, overwrite=False, error_on_conflict=True):
    """
    Объединяет два словаря и возвращает новый словарь. Работает следующим образом:
    - Если ключ существует в словаре `additions`, но отсутствует в словаре `current`, он добавляется.
    - Если ключ отображается на `None` в словаре `current`, он заменяется значением из словаря `additions`.
    - Если ключ существует в обоих словарях и значения являются словарями, функция вызывается рекурсивно.
    - Если ключ существует в обоих словарях и значения являются списками, списки объединяются, и дубликаты удаляются.
    - Если значения имеют разные типы, возникает исключение.
    - Если значения имеют одинаковый тип, но не являются списками или словарями, значение из словаря `additions` перезаписывает значение в словаре `current` в зависимости от параметра `overwrite`.

    Parameters:
    - current (dict): Исходный словарь.
    - additions (dict): Словарь со значениями для добавления.
    - overwrite (bool): Следует ли перезаписывать значения, если они имеют один и тот же тип, но не являются списками или словарями.
    - error_on_conflict (bool): Следует ли вызывать ошибку, если есть конфликт и `overwrite` установлено в `False`.

    Returns:
    - dict: Новый словарь с объединенными значениями.
    """
```

**Назначение**: Объединяет два словаря и возвращает новый словарь.

**Параметры**:
- `current` (dict): Исходный словарь.
- `additions` (dict): Словарь с значениями для добавления.
- `overwrite` (bool): Определяет, следует ли перезаписывать значения, если они имеют один и тот же тип, но не являются списками или словарями. По умолчанию `False`.
- `error_on_conflict` (bool): Определяет, следует ли вызывать ошибку, если есть конфликт и `overwrite` установлено в `False`. По умолчанию `True`.

**Возвращает**:
- `dict`: Новый словарь с объединенными значениями.

**Как работает функция**:
- Создает копию исходного словаря.
- Итерируется по ключам в словаре `additions`.
- Если ключ уже существует в `current`, происходит слияние в зависимости от типов значений.
- Если ключ не существует в `current`, он добавляется из `additions`.

**Примеры**:

```python
dict1 = {'a': 1, 'b': {'c': 2}}
dict2 = {'b': {'d': 3}, 'e': 4}
merged_dict = merge_dicts(dict1, dict2)
print(merged_dict) # {'a': 1, 'b': {'c': 2, 'd': 3}, 'e': 4}

dict1 = {'a': [1, 2], 'b': 3}
dict2 = {'a': [2, 3], 'c': 4}
merged_dict = merge_dicts(dict1, dict2)
print(merged_dict) # {'a': [1, 2, 3], 'b': 3, 'c': 4}

dict1 = {'a': 1}
dict2 = {'a': 2}
merged_dict = merge_dicts(dict1, dict2, overwrite=True)
print(merged_dict) # {'a': 2}
```

### `remove_duplicates`

```python
def remove_duplicates(lst):
    """
    Удаляет дубликаты из списка, сохраняя порядок.
    Обрабатывает нехешируемые элементы, используя list comprehension.

    Parameters:
    - lst (list): Список для удаления дубликатов.

    Returns:
    - list: Новый список без дубликатов.
    """
```

**Назначение**: Удаляет дубликаты из списка, сохраняя порядок элементов.

**Параметры**:
- `lst` (list): Список, из которого необходимо удалить дубликаты.

**Возвращает**:
- `list`: Новый список без дубликатов, сохраняющий порядок элементов исходного списка.

**Как работает функция**:
- Итерируется по списку.
- Для каждого элемента проверяет, был ли он уже встречен.
- Если элемент не был встречен, он добавляется в новый список и в список встреченных элементов.
- Если элемент является словарем, он преобразуется во frozenset для возможности хеширования.

**Примеры**:

```python
my_list = [1, 2, 2, 3, 4, 4, 5]
unique_list = remove_duplicates(my_list)
print(unique_list) # [1, 2, 3, 4, 5]

my_list = [{'a': 1}, {'a': 2}, {'a': 1}]
unique_list = remove_duplicates(my_list)
print(unique_list) # [{'a': 1}, {'a': 2}]