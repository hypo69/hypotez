# Модуль для преобразования SimpleNamespace в различные форматы
=================================================================

Модуль `src.utils.convertors.ns` предоставляет функции для преобразования объектов `SimpleNamespace` в различные форматы данных, такие как словари, JSON, CSV, XML и XLS. Это упрощает экспорт данных из объектов `SimpleNamespace` в форматы, подходящие для различных целей, например, для сохранения в файлы или передачи по сети.

## Обзор

Модуль содержит набор функций для преобразования объектов `SimpleNamespace` в различные форматы. Он включает в себя функции для преобразования в словари, JSON, CSV, XML и XLS.

## Подробней

Этот модуль предназначен для работы с объектами `SimpleNamespace` и преобразования их в другие форматы данных. Он предоставляет удобные функции для экспорта данных из объектов `SimpleNamespace` в различные форматы, что полезно для сохранения данных в файлы или передачи их по сети.

## Функции

### `ns2dict`

```python
def ns2dict(obj: Any) -> Dict[str, Any]:
    """
    Recursively convert an object with key-value pairs to a dictionary.
    Handles empty keys by substituting them with an empty string.

    Args:
        obj (Any): The object to convert. Can be SimpleNamespace, dict, or any object
                   with a similar structure.

    Returns:
        Dict[str, Any]: Converted dictionary with nested structures handled.
    """
```

**Назначение**: Рекурсивно преобразует объект с парами ключ-значение в словарь. Обрабатывает пустые ключи, заменяя их пустой строкой.

**Параметры**:
- `obj` (Any): Объект для преобразования. Может быть `SimpleNamespace`, `dict` или любым объектом с аналогичной структурой.

**Возвращает**:
- `Dict[str, Any]`: Преобразованный словарь с обработанными вложенными структурами.

**Как работает функция**:

1. Функция `ns2dict` принимает объект `obj` в качестве аргумента.
2. Внутри функции определена внутренняя функция `convert`, которая рекурсивно обрабатывает значения объекта.
3. Если у значения есть атрибут `__dict__` (например, `SimpleNamespace` или пользовательские объекты), функция преобразует его в словарь, рекурсивно обрабатывая каждое значение.
4. Если значение является объектом, подобным словарю (имеет метод `items()`), функция преобразует его в словарь, рекурсивно обрабатывая каждое значение.
5. Если значение является списком или другим итерируемым объектом, функция рекурсивно обрабатывает каждый элемент списка.
6. В противном случае функция возвращает значение без изменений.
7. Функция `ns2dict` возвращает результат вызова функции `convert` с объектом `obj`.

```
    A (obj)
    |
    B (convert)
    |
    C (hasattr(value, '__dict__'))? -- Yes --> D (vars(value).items()) --> рекурсивный вызов convert для каждого значения
    |                                  No  --> E (hasattr(value, 'items'))? -- Yes --> F (value.items()) --> рекурсивный вызов convert для каждого значения
    |                                                             No  --> G (isinstance(value, list))? -- Yes --> H (convert для каждого элемента списка)
    |                                                                                               No  --> I (return value)
    |
    J (return)
```

**Примеры**:

```python
from types import SimpleNamespace

# Пример 1: Преобразование SimpleNamespace в словарь
ns_obj = SimpleNamespace(name='John', age=30, address=SimpleNamespace(city='New York', zip='10001'))
result = ns2dict(ns_obj)
print(result)  # {'name': 'John', 'age': 30, 'address': {'city': 'New York', 'zip': '10001'}}

# Пример 2: Преобразование словаря в словарь
dict_obj = {'name': 'John', 'age': 30, 'address': {'city': 'New York', 'zip': '10001'}}
result = ns2dict(dict_obj)
print(result)  # {'name': 'John', 'age': 30, 'address': {'city': 'New York', 'zip': '10001'}}

# Пример 3: Преобразование списка в список
list_obj = ['John', 30, {'city': 'New York', 'zip': '10001'}]
result = ns2dict(list_obj)
print(result)  # ['John', 30, {'city': 'New York', 'zip': '10001'}]
```

#### Внутренние функции

##### `convert`

```python
def convert(value: Any) -> Any:
    """
    Recursively process values to handle nested structures and empty keys.

    Args:
        value (Any): Value to process.

    Returns:
        Any: Converted value.
    """
```

**Назначение**: Рекурсивно обрабатывает значения для работы с вложенными структурами и пустыми ключами.

**Параметры**:
- `value` (Any): Значение для обработки.

**Возвращает**:
- `Any`: Преобразованное значение.

### `ns2csv`

```python
def ns2csv(ns_obj: SimpleNamespace, csv_file_path: str | Path) -> bool:
    """
    Convert SimpleNamespace object to CSV format.

    Args:
        ns_obj (SimpleNamespace): The SimpleNamespace object to convert.
        csv_file_path (str | Path): Path to save the CSV file.

    Returns:
        bool: True if successful, False otherwise.
    """
```

**Назначение**: Преобразует объект `SimpleNamespace` в формат CSV.

**Параметры**:
- `ns_obj` (SimpleNamespace): Объект `SimpleNamespace` для преобразования.
- `csv_file_path` (str | Path): Путь для сохранения CSV-файла.

**Возвращает**:
- `bool`: `True`, если преобразование прошло успешно, `False` в противном случае.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при преобразовании.

**Как работает функция**:

1. Функция `ns2csv` принимает объект `SimpleNamespace` `ns_obj` и путь к CSV-файлу `csv_file_path` в качестве аргументов.
2. Преобразует `ns_obj` в словарь с помощью функции `ns2dict`.
3. Сохраняет словарь в CSV-файл по указанному пути с помощью функции `save_csv_file`.
4. Если во время выполнения возникает исключение, оно перехватывается, и в лог записывается сообщение об ошибке.
5. Функция возвращает `True`, если преобразование прошло успешно, и `False` в противном случае.

```
    A (ns_obj, csv_file_path)
    |
    B (data = [ns2dict(ns_obj)])
    |
    C (save_csv_file(data, csv_file_path))
    |
    D (return True)
    |
    E (Exception)
    |
    F (logger.error(f"ns2csv failed", ex, True))
    |
    G (return False)
```

**Примеры**:

```python
from types import SimpleNamespace
from pathlib import Path

# Пример 1: Преобразование SimpleNamespace в CSV-файл
ns_obj = SimpleNamespace(name='John', age=30, city='New York')
csv_file_path = 'data.csv'
result = ns2csv(ns_obj, csv_file_path)
print(result)  # True

# Пример 2: Преобразование SimpleNamespace в CSV-файл с указанием пути Path
ns_obj = SimpleNamespace(name='John', age=30, city='New York')
csv_file_path = Path('data.csv')
result = ns2csv(ns_obj, csv_file_path)
print(result)  # True
```

### `ns2xml`

```python
def ns2xml(ns_obj: SimpleNamespace, root_tag: str = "root") -> str:
    """
    Convert SimpleNamespace object to XML format.

    Args:
        ns_obj (SimpleNamespace): The SimpleNamespace object to convert.
        root_tag (str): The root element tag for the XML.

    Returns:
        str: The resulting XML string.
    """
```

**Назначение**: Преобразует объект `SimpleNamespace` в формат XML.

**Параметры**:
- `ns_obj` (SimpleNamespace): Объект `SimpleNamespace` для преобразования.
- `root_tag` (str): Корневой тег для XML. По умолчанию "root".

**Возвращает**:
- `str`: Результирующая XML-строка.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при преобразовании.

**Как работает функция**:

1. Функция `ns2xml` принимает объект `SimpleNamespace` `ns_obj` и корневой тег `root_tag` в качестве аргументов.
2. Преобразует `ns_obj` в словарь с помощью функции `ns2dict`.
3. Преобразует словарь в XML-строку с помощью функции `xml2dict`.
4. Если во время выполнения возникает исключение, оно перехватывается, и в лог записывается сообщение об ошибке.
5. Функция возвращает результирующую XML-строку.

```
    A (ns_obj, root_tag)
    |
    B (data = ns2dict(ns_obj))
    |
    C (return xml2dict(data))
    |
    D (Exception)
    |
    E (logger.error(f"ns2xml failed", ex, True))
```

**Примеры**:

```python
from types import SimpleNamespace

# Пример 1: Преобразование SimpleNamespace в XML-строку
ns_obj = SimpleNamespace(name='John', age=30, city='New York')
result = ns2xml(ns_obj)
print(result)  # <root><name>John</name><age>30</age><city>New York</city></root>

# Пример 2: Преобразование SimpleNamespace в XML-строку с указанием корневого тега
ns_obj = SimpleNamespace(name='John', age=30, city='New York')
result = ns2xml(ns_obj, root_tag='person')
print(result)  # <person><name>John</name><age>30</age><city>New York</city></person>
```

### `ns2xls`

```python
def ns2xls(data: SimpleNamespace, xls_file_path: str | Path) -> bool:
    """
    Convert SimpleNamespace object to XLS format.

    Args:
        ns_obj (SimpleNamespace): The SimpleNamespace object to convert.
        xls_file_path (str | Path): Path to save the XLS file.

    Returns:
        bool: True if successful, False otherwise.
    """
```

**Назначение**: Преобразует объект `SimpleNamespace` в формат XLS.

**Параметры**:
- `data` (SimpleNamespace): Объект `SimpleNamespace` для преобразования.
- `xls_file_path` (str | Path): Путь для сохранения XLS-файла.

**Возвращает**:
- `bool`: `True`, если преобразование прошло успешно, `False` в противном случае.

**Как работает функция**:

1. Функция `ns2xls` принимает объект `SimpleNamespace` `data` и путь к XLS-файлу `xls_file_path` в качестве аргументов.
2. Сохраняет `data` в XLS-файл по указанному пути с помощью функции `save_xls_file`.
3. Функция возвращает результат вызова функции `save_xls_file`.

```
    A (data, xls_file_path)
    |
    B (return save_xls_file(data,xls_file_path))
```

**Примеры**:

```python
from types import SimpleNamespace
from pathlib import Path

# Пример 1: Преобразование SimpleNamespace в XLS-файл
ns_obj = SimpleNamespace(name='John', age=30, city='New York')
xls_file_path = 'data.xls'
result = ns2xls(ns_obj, xls_file_path)
print(result)  # True

# Пример 2: Преобразование SimpleNamespace в XLS-файл с указанием пути Path
ns_obj = SimpleNamespace(name='John', age=30, city='New York')
xls_file_path = Path('data.xls')
result = ns2xls(ns_obj, xls_file_path)
print(result)  # True