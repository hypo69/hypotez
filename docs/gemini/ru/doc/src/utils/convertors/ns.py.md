# Модуль для конвертации SimpleNamespace в различные форматы
## Обзор

Модуль `ns.py` предоставляет набор функций для конвертации объектов `SimpleNamespace` в различные форматы данных, такие как `dict`, `JSON`, `CSV`, `XML` и `XLS`. Он предназначен для упрощения процесса преобразования данных между различными представлениями, что может быть полезно при работе с конфигурационными файлами, обменом данными между системами и другими задачами.

## Подробнее

Модуль содержит функции для преобразования объектов `SimpleNamespace` в словари, JSON, CSV, XML и XLS форматы. Это облегчает взаимодействие с данными, представленными в различных форматах, и обеспечивает гибкость при работе с ними. Он включает функции для рекурсивной обработки вложенных структур данных, преобразования в XML и сохранения в файлы CSV и XLS.

## Функции

### `ns2dict`

**Назначение**: Рекурсивно преобразует объект с парами ключ-значение в словарь. Обрабатывает пустые ключи, заменяя их пустой строкой.

**Параметры**:
- `obj` (Any): Объект для преобразования. Может быть `SimpleNamespace`, `dict` или любым объектом с аналогичной структурой.

**Возвращает**:
- `Dict[str, Any]`: Преобразованный словарь с обработанными вложенными структурами.

**Внутренние функции**:

#### `convert`

**Назначение**: Рекурсивно обрабатывает значения для обработки вложенных структур и пустых ключей.

**Параметры**:
- `value` (Any): Значение для обработки.

**Возвращает**:
- `Any`: Преобразованное значение.

**Как работает функция `ns2dict`**:
- Функция `ns2dict` принимает объект `obj` в качестве аргумента и вызывает внутреннюю функцию `convert` для его преобразования в словарь.
- Внутренняя функция `convert` проверяет тип значения:
    - Если значение имеет атрибут `__dict__` (например, `SimpleNamespace` или пользовательский объект), оно преобразуется в словарь, где ключи становятся строками (пустые ключи заменяются на `""`), а значения рекурсивно обрабатываются функцией `convert`.
    - Если значение является объектом, подобным словарю (имеет метод `items()`), оно также преобразуется в словарь с рекурсивной обработкой значений.
    - Если значение является списком, каждый элемент списка рекурсивно обрабатывается функцией `convert`.
    - В противном случае значение возвращается без изменений.
- Функция `ns2dict` возвращает полученный словарь.

**Примеры**:

```python
from types import SimpleNamespace

# Пример 1: Преобразование SimpleNamespace в словарь
ns_obj = SimpleNamespace(name="John", age=30, address=SimpleNamespace(city="New York", zip="10001"))
result = ns2dict(ns_obj)
print(result)
# Expected Output: {'name': 'John', 'age': 30, 'address': {'city': 'New York', 'zip': '10001'}}

# Пример 2: Преобразование словаря в словарь (с рекурсией)
dict_obj = {"name": "Jane", "age": 25, "address": {"city": "Los Angeles", "zip": "90001"}}
result = ns2dict(dict_obj)
print(result)
# Expected Output: {'name': 'Jane', 'age': 25, 'address': {'city': 'Los Angeles', 'zip': '90001'}}

# Пример 3: Преобразование списка с вложенными структурами
list_obj = [SimpleNamespace(item="A", value=1), {"item": "B", "value": 2}]
result = ns2dict(list_obj)
print(result)
# Expected Output: [{'item': 'A', 'value': 1}, {'item': 'B', 'value': 2}]
```

### `ns2csv`

**Назначение**: Преобразует объект `SimpleNamespace` в формат CSV.

**Параметры**:
- `ns_obj` (SimpleNamespace): Объект `SimpleNamespace` для преобразования.
- `csv_file_path` (str | Path): Путь для сохранения CSV-файла.

**Возвращает**:
- `bool`: `True`, если успешно, `False` в противном случае.

**Как работает функция `ns2csv`**:

1.  Функция `ns2csv` принимает объект `ns_obj` типа `SimpleNamespace` и путь к файлу `csv_file_path` в качестве аргументов.
2.  Преобразует `ns_obj` в словарь с помощью функции `ns2dict`.
3.  Создает список, содержащий полученный словарь.
4.  Сохраняет данные в CSV-файл, используя функцию `save_csv_file` из модуля `src.utils.csv`.
5.  В случае успеха возвращает `True`. Если во время выполнения возникнет исключение, логирует ошибку с использованием `logger.error` и возвращает `False`.

**Примеры**:

```python
from types import SimpleNamespace
from pathlib import Path
import tempfile
import os

# Создаем временный файл для записи CSV
with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmpfile:
    temp_csv_path = tmpfile.name

    # Пример 1: Преобразование SimpleNamespace в CSV
    ns_obj = SimpleNamespace(name="John", age=30, city="New York")
    result = ns2csv(ns_obj, temp_csv_path)
    print(f"CSV creation successful: {result}")

    # Очищаем временный файл после использования
    os.remove(temp_csv_path)
```

### `ns2xml`

**Назначение**: Преобразует объект `SimpleNamespace` в формат XML.

**Параметры**:
- `ns_obj` (SimpleNamespace): Объект `SimpleNamespace` для преобразования.
- `root_tag` (str): Корневой тег для XML. По умолчанию `"root"`.

**Возвращает**:
- `str`: Результирующая XML-строка.

**Как работает функция `ns2xml`**:

1.  Функция `ns2xml` принимает объект `ns_obj` типа `SimpleNamespace` и корневой тег `root_tag` в качестве аргументов.
2.  Преобразует `ns_obj` в словарь с помощью функции `ns2dict`.
3.  Преобразует словарь в XML-строку, используя функцию `xml2dict` из модуля `src.utils.convertors`.
4.  Возвращает полученную XML-строку. Если во время выполнения возникнет исключение, логирует ошибку с использованием `logger.error`.

**Примеры**:

```python
from types import SimpleNamespace

# Пример 1: Преобразование SimpleNamespace в XML
ns_obj = SimpleNamespace(name="John", age=30, city="New York")
result = ns2xml(ns_obj)
print(result)
# Expected Output: <xml string>

# Пример 2: Преобразование SimpleNamespace в XML с пользовательским корневым тегом
ns_obj = SimpleNamespace(name="Jane", age=25, city="Los Angeles")
result = ns2xml(ns_obj, root_tag="person")
print(result)
# Expected Output: <xml string with root tag "person">
```

### `ns2xls`

**Назначение**: Преобразует объект `SimpleNamespace` в формат XLS.

**Параметры**:
- `data` (SimpleNamespace): Объект `SimpleNamespace` для преобразования.
- `xls_file_path` (str | Path): Путь для сохранения XLS-файла.

**Возвращает**:
- `bool`: `True`, если успешно, `False` в противном случае.

**Как работает функция `ns2xls`**:

1.  Функция `ns2xls` принимает объект `data` типа `SimpleNamespace` и путь к файлу `xls_file_path` в качестве аргументов.
2.  Сохраняет данные в XLS-файл, используя функцию `save_xls_file` из модуля `src.utils.xls`.
3.  Возвращает результат выполнения функции `save_xls_file`.

**Примеры**:

```python
from types import SimpleNamespace
from pathlib import Path
import tempfile
import os

# Создаем временный файл для записи XLS
with tempfile.NamedTemporaryFile(delete=False, suffix=".xls") as tmpfile:
    temp_xls_path = tmpfile.name

    # Пример 1: Преобразование SimpleNamespace в XLS
    ns_obj = SimpleNamespace(name="John", age=30, city="New York")
    result = ns2xls(ns_obj, temp_xls_path)
    print(f"XLS creation successful: {result}")

    # Очищаем временный файл после использования
    os.remove(temp_xls_path)