# Модуль для JSON-сериализации и десериализации с поддержкой регистрации подклассов

## Обзор

Модуль предоставляет класс `JsonSerializableRegistry`, который обеспечивает JSON-сериализацию, десериализацию и регистрацию подклассов. Это позволяет легко сохранять и загружать объекты, а также управлять иерархией классов.

## Подробнее

Данный модуль предназначен для упрощения работы с JSON-сериализацией и десериализацией в проекте `hypotez`. Он предоставляет механизм для автоматической регистрации подклассов и обработки различных типов данных, включая вложенные объекты и списки. Это особенно полезно при работе со сложными структурами данных, которые необходимо сохранять и загружать.

## Классы

### `JsonSerializableRegistry`

**Описание**: Базовый класс, предоставляющий функциональность JSON-сериализации, десериализации и регистрации подклассов.

**Наследует**:

- Не наследует другие классы.

**Атрибуты**:

- `class_mapping` (dict): Словарь, содержащий соответствие между именами классов и самими классами. Используется для регистрации подклассов.

**Методы**:

- `to_json(include: list = None, suppress: list = None, file_path: str = None, serialization_type_field_name: str = "json_serializable_class_name") -> dict`
- `from_json(json_dict_or_path, suppress: list = None, serialization_type_field_name: str = "json_serializable_class_name", post_init_params: dict = None)`
- `__init_subclass__(cls, **kwargs)`
- `_post_deserialization_init(self, **kwargs)`
- `_programmatic_name_to_json_name(cls, name)`
- `_json_name_to_programmatic_name(cls, name)`

**Принцип работы**:

Класс `JsonSerializableRegistry` предоставляет механизм для преобразования объектов в JSON-представление и обратно. Он использует атрибут `class_mapping` для регистрации подклассов, что позволяет корректно десериализовать объекты разных типов. Методы `to_json` и `from_json` отвечают за сериализацию и десериализацию соответственно. Метод `__init_subclass__` автоматически регистрирует подклассы при их создании.

## Методы класса

### `to_json`

```python
def to_json(self, include: list = None, suppress: list = None, file_path: str = None, serialization_type_field_name: str = "json_serializable_class_name") -> dict:
    """
    Возвращает JSON-представление объекта.

    Args:
        include (list, optional): Атрибуты для включения в сериализацию. Переопределяет поведение по умолчанию.
        suppress (list, optional): Атрибуты для исключения из сериализации. Переопределяет поведение по умолчанию.
        file_path (str, optional): Путь к файлу, куда будет записан JSON.
        serialization_type_field_name (str, optional): Имя поля, используемого для хранения имени класса при сериализации. По умолчанию "json_serializable_class_name".

    Returns:
        dict: Словарь, представляющий JSON-представление объекта.
    """
```

**Назначение**: Преобразует объект в JSON-представление.

**Параметры**:

- `include` (list, optional): Список атрибутов, которые должны быть включены в JSON-представление. Если указан, то только эти атрибуты будут сериализованы. По умолчанию `None`.
- `suppress` (list, optional): Список атрибутов, которые должны быть исключены из JSON-представления. По умолчанию `None`.
- `file_path` (str, optional): Путь к файлу, в который будет записано JSON-представление объекта. Если указан, JSON будет записан в файл. По умолчанию `None`.
- `serialization_type_field_name` (str, optional): Имя поля, которое будет использоваться для хранения имени класса при сериализации. По умолчанию `"json_serializable_class_name"`.

**Возвращает**:

- `dict`: Словарь, представляющий JSON-представление объекта.

**Как работает функция**:

Функция `to_json` выполняет следующие действия:

1.  Определяет список атрибутов для сериализации на основе иерархии классов, атрибутов `serializable_attributes` и `suppress_attributes_from_serialization`.
2.  Переопределяет список атрибутов, если указаны параметры `include` или `suppress`.
3.  Создает словарь `result`, содержащий имя класса объекта и значения его атрибутов.
4.  Для каждого атрибута проверяет, является ли его значение экземпляром `JsonSerializableRegistry`, списком или словарем.
    -   Если значение является экземпляром `JsonSerializableRegistry`, рекурсивно вызывает метод `to_json` для этого объекта.
    -   Если значение является списком, применяет метод `to_json` к каждому элементу списка, если элемент является экземпляром `JsonSerializableRegistry`.
    -   Если значение является словарем, применяет метод `to_json` к каждому значению словаря, если значение является экземпляром `JsonSerializableRegistry`.
    -   В противном случае, выполняет глубокое копирование значения.
5.  Если указан параметр `file_path`, записывает JSON-представление объекта в файл.
6.  Возвращает словарь `result`.

**Примеры**:

```python
class MyClass(JsonSerializableRegistry):
    serializable_attributes = ['attr1', 'attr2']

    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2

obj = MyClass('value1', 'value2')
json_data = obj.to_json()
print(json_data)
# {'json_serializable_class_name': 'MyClass', 'attr1': 'value1', 'attr2': 'value2'}

obj.to_json(file_path='data.json')  # Запись в файл data.json
```

### `from_json`

```python
@classmethod
def from_json(cls, json_dict_or_path, suppress: list = None,
              serialization_type_field_name: str = "json_serializable_class_name",
              post_init_params: dict = None):
    """
    Загружает JSON-представление объекта и создает экземпляр класса.

    Args:
        json_dict_or_path (dict or str): JSON-словарь, представляющий объект, или путь к файлу, содержащему JSON.
        suppress (list, optional): Атрибуты для исключения при загрузке.
        serialization_type_field_name (str, optional): Имя поля, используемого для хранения имени класса при сериализации. По умолчанию "json_serializable_class_name".
        post_init_params (dict, optional): Параметры для передачи в метод `_post_deserialization_init`.

    Returns:
        An instance of the class populated with the data from json_dict_or_path.
    """
```

**Назначение**: Создает экземпляр класса на основе JSON-представления.

**Параметры**:

- `json_dict_or_path` (dict или str): JSON-словарь, представляющий объект, или путь к файлу, содержащему JSON.
- `suppress` (list, optional): Список атрибутов, которые следует исключить при десериализации. По умолчанию `None`.
- `serialization_type_field_name` (str, optional): Имя поля, в котором хранится имя класса при сериализации. По умолчанию `"json_serializable_class_name"`.
- `post_init_params` (dict, optional): Словарь параметров, которые будут переданы в метод `_post_deserialization_init` после десериализации. По умолчанию `None`.

**Возвращает**:

- Экземпляр класса, заполненный данными из `json_dict_or_path`.

**Как работает функция**:

Функция `from_json` выполняет следующие действия:

1.  Определяет, является ли `json_dict_or_path` словарем или путем к файлу. Если это путь к файлу, загружает JSON из файла.
2.  Извлекает имя класса из JSON-словаря с использованием ключа `serialization_type_field_name`.
3.  Определяет целевой класс на основе имени класса из словаря `class_mapping`. Если класс не найден в `class_mapping`, использует текущий класс.
4.  Создает экземпляр целевого класса без вызова метода `__init__`.
5.  Определяет список атрибутов для десериализации на основе иерархии классов, атрибутов `serializable_attributes`, `custom_serialization_initializers` и `suppress_attributes_from_serialization`.
6.  Для каждого атрибута в JSON-словаре устанавливает значение атрибута в экземпляре класса.
    -   Если для атрибута определен пользовательский инициализатор в `custom_serialization_initializers`, использует его для установки значения атрибута.
    -   Если значение атрибута является словарем и содержит ключ `serialization_type_field_name`, рекурсивно вызывает метод `from_json` для десериализации вложенного объекта.
    -   Если значение атрибута является списком, рекурсивно вызывает метод `from_json` для каждого элемента списка, если элемент является словарем и содержит ключ `serialization_type_field_name`.
    -   В противном случае, выполняет глубокое копирование значения.
7.  Если у экземпляра класса есть метод `_post_deserialization_init`, вызывает его после десериализации, передавая параметры из `post_init_params`.
8.  Возвращает экземпляр класса.

**Примеры**:

```python
class MyClass(JsonSerializableRegistry):
    serializable_attributes = ['attr1', 'attr2']

    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2

json_data = {'json_serializable_class_name': 'MyClass', 'attr1': 'value1', 'attr2': 'value2'}
obj = MyClass.from_json(json_data)
print(obj.attr1, obj.attr2)
# value1 value2

# Загрузка из файла
obj = MyClass.from_json('data.json')
```

### `__init_subclass__`

```python
def __init_subclass__(cls, **kwargs):
    """
    Регистрирует подкласс и автоматически расширяет атрибуты сериализации и пользовательские инициализаторы из родительских классов.

    Args:
        cls (class): Подкласс для инициализации.
        **kwargs: Дополнительные параметры.
    """
```

**Назначение**: Автоматически регистрирует подклассы и расширяет атрибуты сериализации и пользовательские инициализаторы из родительских классов.

**Параметры**:

- `cls` (class): Подкласс для инициализации.
- `**kwargs`: Дополнительные параметры.

**Как работает функция**:

Функция `__init_subclass__` вызывается автоматически при создании нового подкласса `JsonSerializableRegistry`. Она выполняет следующие действия:

1.  Регистрирует подкласс в словаре `class_mapping`, используя имя класса в качестве ключа.
2.  Автоматически расширяет списки `serializable_attributes` и `suppress_attributes_from_serialization` из родительских классов.
3.  Обновляет словарь `custom_serialization_initializers` из родительских классов.

**Примеры**:

```python
class BaseClass(JsonSerializableRegistry):
    serializable_attributes = ['base_attr1']
    custom_serialization_initializers = {'base_attr1': lambda x: x + '_base'}

class MyClass(BaseClass):
    serializable_attributes = ['my_attr1']
    custom_serialization_initializers = {'my_attr1': lambda x: x + '_my'}

print(MyClass.serializable_attributes)
# ['base_attr1', 'my_attr1']
```

### `_post_deserialization_init`

```python
def _post_deserialization_init(self, **kwargs):
    """
    Вызывает метод `_post_init` после десериализации, если он существует.

    Args:
        **kwargs: Дополнительные параметры для передачи в метод `_post_init`.
    """
```

**Назначение**: Вызывает метод `_post_init` после десериализации, если он существует.

**Параметры**:

- `**kwargs`: Дополнительные параметры для передачи в метод `_post_init`.

**Как работает функция**:

Функция `_post_deserialization_init` проверяет, существует ли у экземпляра класса метод `_post_init`. Если метод существует, он вызывается с передачей дополнительных параметров `kwargs`.

**Примеры**:

```python
class MyClass(JsonSerializableRegistry):
    def _post_init(self, value):
        self.attr1 = value

    def __init__(self, attr1=None):
        self.attr1 = attr1

json_data = {'json_serializable_class_name': 'MyClass'}
obj = MyClass.from_json(json_data, post_init_params={'value': 'post_init_value'})
print(obj.attr1)
# None
```

### `_programmatic_name_to_json_name`

```python
@classmethod
def _programmatic_name_to_json_name(cls, name):
    """
    Преобразует имя атрибута в формат JSON (snake_case).

    Args:
        name (str): Имя атрибута.

    Returns:
        str: Имя атрибута в формате JSON (snake_case).
    """
```

**Назначение**: Преобразует имя атрибута в формат JSON (snake_case).

**Параметры**:

- `name` (str): Имя атрибута.

**Возвращает**:

- `str`: Имя атрибута в формате JSON (snake_case).

**Как работает функция**:

Функция `_programmatic_name_to_json_name` преобразует имя атрибута из формата, используемого в коде (например, `camelCase`), в формат, используемый в JSON (например, `snake_case`). Если у класса определен атрибут `serializable_attributes_renaming`, функция использует его для переименования атрибутов.

**Примеры**:

```python
class MyClass(JsonSerializableRegistry):
    serializable_attributes_renaming = {'myAttr': 'my_attr'}

print(MyClass._programmatic_name_to_json_name('myAttr'))
# my_attr
```

### `_json_name_to_programmatic_name`

```python
@classmethod
def _json_name_to_programmatic_name(cls, name):
    """
    Преобразует имя атрибута из формата JSON (snake_case) в формат, используемый в коде.

    Args:
        name (str): Имя атрибута в формате JSON (snake_case).

    Returns:
        str: Имя атрибута в формате, используемом в коде.
    """
```

**Назначение**: Преобразует имя атрибута из формата JSON (snake_case) в формат, используемый в коде.

**Параметры**:

- `name` (str): Имя атрибута в формате JSON (snake_case).

**Возвращает**:

- `str`: Имя атрибута в формате, используемом в коде.

**Как работает функция**:

Функция `_json_name_to_programmatic_name` преобразует имя атрибута из формата JSON (например, `snake_case`) в формат, используемый в коде (например, `camelCase`). Если у класса определен атрибут `serializable_attributes_renaming`, функция использует его для переименования атрибутов.

**Примеры**:

```python
class MyClass(JsonSerializableRegistry):
    serializable_attributes_renaming = {'myAttr': 'my_attr'}

print(MyClass._json_name_to_programmatic_name('my_attr'))
# myAttr
```

## Функции

### `post_init`

```python
def post_init(cls):
    """
    Декоратор для принудительного вызова метода `_post_init` в классе, если он есть.
    Метод должен называться `_post_init`.

    Args:
        cls (class): Класс для декорирования.

    Returns:
        class: Декорированный класс.
    """
```

**Назначение**: Декоратор для принудительного вызова метода `_post_init` в классе, если он есть.

**Параметры**:

- `cls` (class): Класс для декорирования.

**Возвращает**:

- `class`: Декорированный класс.

**Как работает функция**:

Функция `post_init` является декоратором, который заменяет метод `__init__` класса новым методом, который вызывает оригинальный метод `__init__` и, если существует метод `_post_init`, вызывает его после инициализации.

**Примеры**:

```python
@post_init
class MyClass:
    def __init__(self, value):
        self.value = value

    def _post_init(self):
        self.value = self.value + '_post_init'

obj = MyClass('initial_value')
print(obj.value)
# initial_value_post_init
```

### `merge_dicts`

```python
def merge_dicts(current, additions, overwrite=False, error_on_conflict=True):
    """
    Объединяет два словаря и возвращает новый словарь.

    Args:
        current (dict): Оригинальный словарь.
        additions (dict): Словарь со значениями для добавления.
        overwrite (bool, optional): Перезаписывать ли значения, если они одного типа, но не списки/словари. По умолчанию False.
        error_on_conflict (bool, optional): Вызывать ли ошибку, если есть конфликт и overwrite=False. По умолчанию True.

    Returns:
        dict: Новый словарь с объединенными значениями.
    """
```

**Назначение**: Объединяет два словаря и возвращает новый словарь.

**Параметры**:

- `current` (dict): Оригинальный словарь.
- `additions` (dict): Словарь со значениями для добавления.
- `overwrite` (bool, optional): Определяет, следует ли перезаписывать значения, если они имеют одинаковый тип, но не являются списками или словарями. По умолчанию `False`.
- `error_on_conflict` (bool, optional): Определяет, следует ли вызывать исключение, если возникает конфликт и `overwrite` установлено в `False`. По умолчанию `True`.

**Возвращает**:

- `dict`: Новый словарь с объединенными значениями.

**Как работает функция**:

Функция `merge_dicts` выполняет следующие действия:

1.  Создает копию словаря `current`, чтобы избежать его изменения.
2.  Перебирает ключи в словаре `additions`.
3.  Если ключ существует в словаре `merged`:
    -   Если значение в `merged` равно `None`, присваивает ему значение из `additions`.
    -   Если оба значения являются словарями, рекурсивно вызывает функцию `merge_dicts` для их объединения.
    -   Если оба значения являются списками, объединяет их и удаляет дубликаты.
    -   Если типы значений отличаются, вызывает исключение `TypeError`.
    -   Если типы значений одинаковы, но не являются списками или словарями, перезаписывает значение из `merged` значением из `additions`, если `overwrite` установлено в `True`. Если `overwrite` установлено в `False` и значения отличаются, вызывает исключение `ValueError`, если `error_on_conflict` установлено в `True`.
4.  Если ключ не существует в словаре `merged`, добавляет его из словаря `additions`.
5.  Возвращает новый словарь `merged`.

**Примеры**:

```python
dict1 = {'a': 1, 'b': {'c': 2}}
dict2 = {'b': {'d': 3}, 'e': 4}
merged_dict = merge_dicts(dict1, dict2)
print(merged_dict)
# {'a': 1, 'b': {'c': 2, 'd': 3}, 'e': 4}
```

### `remove_duplicates`

```python
def remove_duplicates(lst):
    """
    Удаляет дубликаты из списка, сохраняя порядок элементов.

    Args:
        lst (list): Список для удаления дубликатов.

    Returns:
        list: Новый список без дубликатов.
    """
```

**Назначение**: Удаляет дубликаты из списка, сохраняя порядок элементов.

**Параметры**:

- `lst` (list): Список для удаления дубликатов.

**Возвращает**:

- `list`: Новый список без дубликатов.

**Как работает функция**:

Функция `remove_duplicates` выполняет следующие действия:

1.  Создает пустой список `seen` для хранения уникальных элементов.
2.  Создает пустой список `result` для хранения результата.
3.  Перебирает элементы в списке `lst`.
4.  Если элемент является словарем, преобразует его в `frozenset` для возможности хеширования.
5.  Если элемент (или его `frozenset`-представление) отсутствует в списке `seen`, добавляет его в `seen` и добавляет элемент в список `result`.
6.  Возвращает новый список `result`.

**Примеры**:

```python
lst = [1, 2, 2, 3, 4, 4, 5]
unique_list = remove_duplicates(lst)
print(unique_list)
# [1, 2, 3, 4, 5]