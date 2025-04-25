# Модуль конвертации SimpleNamespace

## Обзор

Этот модуль предоставляет функции для преобразования объектов SimpleNamespace в различные форматы: словарь, JSON, CSV, XML и XLS.  

## Подробнее

Данный модуль используется для удобного преобразования данных, хранящихся в объектах SimpleNamespace, в различные форматы. Это позволяет легко экспортировать данные для дальнейшей обработки или сохранения в файлах.

## Функции

### `ns2dict`

**Назначение**: Преобразует объект SimpleNamespace в словарь.

**Параметры**:
- `obj (Any)`: Объект для преобразования. Может быть SimpleNamespace, словарь или любой объект с аналогичной структурой.

**Возвращает**:
- `Dict[str, Any]`: Преобразованный словарь с обработанными вложенными структурами.

**Как работает**:
- Функция рекурсивно обрабатывает объект, проверяя, имеет ли он атрибут `__dict__` (характерно для SimpleNamespace и пользовательских объектов). 
- Если атрибут присутствует, функция создает словарь, где ключи - имена атрибутов, а значения - результаты рекурсивного преобразования соответствующих атрибутов. 
- Если объект - словарь, функция создает новый словарь, где ключи и значения - результаты рекурсивного преобразования элементов исходного словаря.
- Если объект - список, функция создает новый список, где элементы - результаты рекурсивного преобразования элементов исходного списка.

**Пример**:
```python
from types import SimpleNamespace

ns_obj = SimpleNamespace(name="Alice", age=30, address={"city": "London", "street": "Baker Street"})

# Преобразуем объект в словарь
dict_obj = ns2dict(ns_obj)

print(dict_obj)
# Вывод:
# {'name': 'Alice', 'age': 30, 'address': {'city': 'London', 'street': 'Baker Street'}}
```

### `ns2csv`

**Назначение**: Преобразует объект SimpleNamespace в CSV-формат.

**Параметры**:
- `ns_obj (SimpleNamespace)`: Объект SimpleNamespace для преобразования.
- `csv_file_path (str | Path)`: Путь к файлу для сохранения CSV-файла.

**Возвращает**:
- `bool`: True, если преобразование прошло успешно, False в противном случае.

**Как работает**:
- Функция использует функцию `ns2dict` для преобразования объекта SimpleNamespace в словарь.
- Затем она использует функцию `save_csv_file` для сохранения данных в CSV-файл.

**Пример**:
```python
from types import SimpleNamespace
from pathlib import Path

ns_obj = SimpleNamespace(name="Alice", age=30, address={"city": "London", "street": "Baker Street"})

# Преобразуем объект в CSV-файл
csv_file_path = Path("my_data.csv")
success = ns2csv(ns_obj, csv_file_path)

print(f"CSV file saved: {success}")
```

### `ns2xml`

**Назначение**: Преобразует объект SimpleNamespace в XML-формат.

**Параметры**:
- `ns_obj (SimpleNamespace)`: Объект SimpleNamespace для преобразования.
- `root_tag (str)`: Тег корневого элемента для XML. По умолчанию "root".

**Возвращает**:
- `str`: Полученная XML-строка.

**Как работает**:
- Функция использует функцию `ns2dict` для преобразования объекта SimpleNamespace в словарь.
- Затем она использует функцию `xml2dict` для преобразования словаря в XML-строку.

**Пример**:
```python
from types import SimpleNamespace

ns_obj = SimpleNamespace(name="Alice", age=30, address={"city": "London", "street": "Baker Street"})

# Преобразуем объект в XML-строку
xml_string = ns2xml(ns_obj, root_tag="person")

print(xml_string)
# Вывод:
# <person><name>Alice</name><age>30</age><address><city>London</city><street>Baker Street</street></address></person>
```

### `ns2xls`

**Назначение**: Преобразует объект SimpleNamespace в XLS-формат.

**Параметры**:
- `ns_obj (SimpleNamespace)`: Объект SimpleNamespace для преобразования.
- `xls_file_path (str | Path)`: Путь к файлу для сохранения XLS-файла.

**Возвращает**:
- `bool`: True, если преобразование прошло успешно, False в противном случае.

**Как работает**:
- Функция использует функцию `save_xls_file` для сохранения данных в XLS-файл.

**Пример**:
```python
from types import SimpleNamespace
from pathlib import Path

ns_obj = SimpleNamespace(name="Alice", age=30, address={"city": "London", "street": "Baker Street"})

# Преобразуем объект в XLS-файл
xls_file_path = Path("my_data.xls")
success = ns2xls(ns_obj, xls_file_path)

print(f"XLS file saved: {success}")
```

## Примеры

### Преобразование SimpleNamespace в различные форматы:

```python
from types import SimpleNamespace
from pathlib import Path
from src.utils.convertors.ns import ns2dict, ns2csv, ns2xml, ns2xls

ns_obj = SimpleNamespace(name="Alice", age=30, address={"city": "London", "street": "Baker Street"})

# Преобразовать в словарь
dict_obj = ns2dict(ns_obj)
print(f"Словарь: {dict_obj}")

# Преобразовать в CSV-файл
csv_file_path = Path("my_data.csv")
success = ns2csv(ns_obj, csv_file_path)
print(f"CSV-файл сохранен: {success}")

# Преобразовать в XML-строку
xml_string = ns2xml(ns_obj, root_tag="person")
print(f"XML-строка: {xml_string}")

# Преобразовать в XLS-файл
xls_file_path = Path("my_data.xls")
success = ns2xls(ns_obj, xls_file_path)
print(f"XLS-файл сохранен: {success}")
```