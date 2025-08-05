# Модуль json

## Обзор

Модуль `json` предоставляет классы и функции для сериализации и десериализации Python-объектов в формат JSON. 

## Подробней

В модуле определен класс `JsonSerializableRegistry`, который используется для удобной работы с сериализацией и десериализацией Python-объектов в формат JSON. 

Класс `JsonSerializableRegistry` предоставляет функции `to_json` и `from_json` для преобразования объектов в JSON и обратно. 

## Классы

### `JsonSerializableRegistry`

**Описание**: Mixin-класс, который предоставляет функциональность для сериализации, десериализации и регистрации подклассов. 

**Атрибуты**:
- `class_mapping (dict)`: Словарь, хранящий сопоставление имен классов с их соответствующими классами.

**Методы**:
- `to_json(self, include: list = None, suppress: list = None, file_path: str = None, serialization_type_field_name = "json_serializable_class_name") -> dict`: Возвращает JSON-представление объекта.
- `from_json(cls, json_dict_or_path, suppress: list = None, serialization_type_field_name = "json_serializable_class_name", post_init_params: dict = None)`: Загружает JSON-представление объекта и создает экземпляр класса.
- `__init_subclass__(cls, **kwargs)`: Регистрирует подкласс, используя его имя в качестве ключа.
- `_post_deserialization_init(self, **kwargs)`: Вызывается после десериализации, чтобы выполнить дополнительные действия инициализации.
- `_programmatic_name_to_json_name(cls, name)`: Преобразует программатическое имя в JSON-имя, преобразуя его в snake case.
- `_json_name_to_programmatic_name(cls, name)`: Преобразует JSON-имя в программатическое имя.

#### `to_json`

**Назначение**: Преобразует объект в JSON-представление.

**Параметры**:
- `include (list, optional)`: Список атрибутов для включения в сериализацию. Переопределяет стандартное поведение.
- `suppress (list, optional)`: Список атрибутов для исключения из сериализации. Переопределяет стандартное поведение.
- `file_path (str, optional)`: Путь к файлу, куда будет записан JSON.

**Возвращает**:
- `dict`: JSON-представление объекта.

**Пример**:

```python
from tinytroupe.utils.json import JsonSerializableRegistry

class MyObject(JsonSerializableRegistry):
    serializable_attributes = ["name", "age"]

    def __init__(self, name, age):
        self.name = name
        self.age = age

obj = MyObject("Alice", 30)
json_data = obj.to_json()
print(json_data)
```
#### `from_json`

**Назначение**: Загружает JSON-представление объекта и создает экземпляр класса.

**Параметры**:
- `json_dict_or_path (dict or str)`: JSON-словарь, представляющий объект, или путь к файлу для загрузки JSON.
- `suppress (list, optional)`: Список атрибутов, которые не будут загружаться.

**Возвращает**:
- `JsonSerializableRegistry`: Экземпляр класса, заполненный данными из `json_dict_or_path`.

**Пример**:

```python
from tinytroupe.utils.json import JsonSerializableRegistry

class MyObject(JsonSerializableRegistry):
    serializable_attributes = ["name", "age"]

    def __init__(self, name, age):
        self.name = name
        self.age = age

json_data = {"json_serializable_class_name": "MyObject", "name": "Alice", "age": 30}
obj = MyObject.from_json(json_data)
print(obj.name)
print(obj.age)
```

#### `__init_subclass__`

**Назначение**: Регистрирует подкласс в `class_mapping`.

**Параметры**:
- `cls (JsonSerializableRegistry)`: Класс, который регистрируется.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `None`.

#### `_post_deserialization_init`

**Назначение**: Выполняет дополнительные действия инициализации после десериализации.

**Параметры**:
- `self (JsonSerializableRegistry)`: Текущий экземпляр класса.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `None`.

#### `_programmatic_name_to_json_name`

**Назначение**: Преобразует программатическое имя в JSON-имя.

**Параметры**:
- `cls (JsonSerializableRegistry)`: Класс, для которого выполняется преобразование.
- `name (str)`: Программатическое имя.

**Возвращает**:
- `str`: JSON-имя.

#### `_json_name_to_programmatic_name`

**Назначение**: Преобразует JSON-имя в программатическое имя.

**Параметры**:
- `cls (JsonSerializableRegistry)`: Класс, для которого выполняется преобразование.
- `name (str)`: JSON-имя.

**Возвращает**:
- `str`: Программатическое имя.

## Функции

### `post_init(cls)`

**Назначение**: Декоратор, который обеспечивает вызов метода после инициализации в классе. 

**Параметры**:
- `cls (class)`: Класс, к которому применяется декоратор.

**Возвращает**:
- `class`: Измененный класс с вызовом метода после инициализации.

### `merge_dicts(current, additions, overwrite=False, error_on_conflict=True)`

**Назначение**: Объединяет два словаря и возвращает новый словарь. 

**Параметры**:
- `current (dict)`: Исходный словарь.
- `additions (dict)`: Словарь с значениями, которые нужно добавить.
- `overwrite (bool)`: Переопределять ли значения, если они имеют одинаковый тип, но не являются одновременно списками или словарями.
- `error_on_conflict (bool)`: Вызывать ли ошибку, если возникает конфликт и `overwrite` равно `False`.

**Возвращает**:
- `dict`: Новый словарь с объединенными значениями.

### `remove_duplicates(lst)`

**Назначение**: Удаляет дубликаты из списка, сохраняя порядок. 

**Параметры**:
- `lst (list)`: Список, из которого нужно удалить дубликаты.

**Возвращает**:
- `list`: Новый список без дубликатов.