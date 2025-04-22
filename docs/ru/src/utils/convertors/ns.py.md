# Модуль `ns`

## Обзор

Модуль `ns` предоставляет функции для конвертации объектов `SimpleNamespace` в различные форматы: словарь (`dict`), JSON, CSV, XML и XLS.

## Подробнее

Модуль содержит функции для преобразования объектов `SimpleNamespace` в различные форматы данных, что позволяет удобно экспортировать и использовать данные в разных приложениях и системах. Он использует вспомогательные функции из других модулей, таких как `xml2dict` (для XML), `save_csv_file` (для CSV) и `save_xls_file` (для XLS).

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

**Назначение**: Рекурсивно преобразует объект с парами "ключ-значение" в словарь. Обрабатывает пустые ключи, заменяя их пустой строкой.

**Параметры**:
- `obj` (Any): Объект для преобразования. Может быть `SimpleNamespace`, `dict` или любым другим объектом с аналогичной структурой.

**Возвращает**:
- `Dict[str, Any]`: Преобразованный словарь с обработанными вложенными структурами.

**Как работает функция**:
Функция `ns2dict` принимает объект `obj` и рекурсивно преобразует его в словарь. Если обнаруживается объект с атрибутом `__dict__` (например, `SimpleNamespace` или пользовательский объект) или объект, подобный словарю (с методом `items()`), он преобразуется в словарь, где ключи и значения обрабатываются рекурсивно. Пустые ключи заменяются пустой строкой.

**Внутренние функции**:

#### `convert`

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

**Как работает функция**:
Внутренняя функция `convert` рекурсивно обрабатывает значения, проверяя их тип и структуру. Если значение имеет атрибут `__dict__` (например, `SimpleNamespace`) или метод `items()` (как у словаря), оно преобразуется в словарь с рекурсивной обработкой ключей и значений. Если значение является списком, каждый элемент списка также обрабатывается рекурсивно.

**Примеры**:

```python
from types import SimpleNamespace

# Пример 1: Преобразование SimpleNamespace в словарь
ns_obj = SimpleNamespace(name="Alice", age=30, address=SimpleNamespace(city="New York", zip="10001"))
result = ns2dict(ns_obj)
print(result)  # Вывод: {'name': 'Alice', 'age': 30, 'address': {'city': 'New York', 'zip': '10001'}}

# Пример 2: Преобразование словаря с вложенными структурами
dict_obj = {"name": "Bob", "age": 25, "contact": {"email": "bob@example.com", "phone": "123-456-7890"}}
result = ns2dict(dict_obj)
print(result)  # Вывод: {'name': 'Bob', 'age': 25, 'contact': {'email': 'bob@example.com', 'phone': '123-456-7890'}}
```

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
- `bool`: `True`, если преобразование выполнено успешно, `False` в противном случае.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при преобразовании в CSV.

**Как работает функция**:
Функция `ns2csv` преобразует объект `SimpleNamespace` в CSV-формат, используя функцию `save_csv_file` из модуля `src.utils.csv`. Сначала объект `SimpleNamespace` преобразуется в словарь с помощью `ns2dict`, затем этот словарь передается в `save_csv_file` для сохранения в CSV-файл. В случае ошибки, информация об ошибке логируется с использованием `logger.error`.

**Примеры**:

```python
from types import SimpleNamespace
from pathlib import Path

# Пример: Преобразование SimpleNamespace в CSV
ns_obj = SimpleNamespace(name="Alice", age=30, city="New York")
csv_file_path = "output.csv"
result = ns2csv(ns_obj, csv_file_path)
print(result)  # Вывод: True (если успешно)
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
- `Exception`: Если возникает ошибка при преобразовании в XML.

**Как работает функция**:
Функция `ns2xml` преобразует объект `SimpleNamespace` в XML-формат. Сначала объект `SimpleNamespace` преобразуется в словарь с помощью `ns2dict`, затем этот словарь передается в функцию `xml2dict` из модуля `src.utils.convertors` для преобразования в XML. В случае ошибки, информация об ошибке логируется с использованием `logger.error`.

**Примеры**:

```python
from types import SimpleNamespace

# Пример: Преобразование SimpleNamespace в XML
ns_obj = SimpleNamespace(name="Alice", age=30, city="New York")
xml_string = ns2xml(ns_obj, root_tag="data")
print(xml_string)  # Вывод: XML-строка
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
- `bool`: `True`, если преобразование выполнено успешно, `False` в противном случае.

**Как работает функция**:
Функция `ns2xls` преобразует объект `SimpleNamespace` в XLS-формат, используя функцию `save_xls_file` из модуля `src.utils.xls`. Эта функция принимает объект `SimpleNamespace` и путь для сохранения XLS-файла.  В случае ошибки, информация об ошибке логируется с использованием `logger.error`.

**Примеры**:

```python
from types import SimpleNamespace
from pathlib import Path

# Пример: Преобразование SimpleNamespace в XLS
ns_obj = SimpleNamespace(name="Alice", age=30, city="New York")
xls_file_path = "output.xls"
result = ns2xls(ns_obj, xls_file_path)
print(result)  # Вывод: True (если успешно)