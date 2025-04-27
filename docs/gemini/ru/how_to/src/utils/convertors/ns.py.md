## Как использовать модуль для преобразования SimpleNamespace

=========================================================================================

### Описание
-------------------------
Модуль `src.utils.convertors.ns` предоставляет набор функций для преобразования объекта `SimpleNamespace` в различные форматы, такие как `dict`, `JSON`, `CSV`, `XML` и `XLS`. 

### Шаги выполнения
-------------------------
1. **Импортируйте необходимые функции:**
    ```python
    from src.utils.convertors.ns import ns2dict, ns2json, ns2csv, ns2xml, ns2xls
    ```
2. **Создайте объект `SimpleNamespace`:**
    ```python
    from types import SimpleNamespace
    data = SimpleNamespace(name='John Doe', age=30, city='New York')
    ```
3. **Преобразуйте объект `SimpleNamespace` в нужный формат:**
    -  **В словарь:**
        ```python
        dict_data = ns2dict(data)
        ```
    - **В JSON:**
        ```python
        json_data = ns2json(data)
        ```
    - **В CSV:**
        ```python
        csv_file_path = 'data.csv' 
        result = ns2csv(data, csv_file_path)
        ```
    - **В XML:**
        ```python
        xml_data = ns2xml(data, root_tag='person')
        ```
    - **В XLS:**
        ```python
        xls_file_path = 'data.xls'
        result = ns2xls(data, xls_file_path)
        ```

### Пример использования
-------------------------

```python
from src.utils.convertors.ns import ns2dict, ns2json, ns2csv, ns2xml, ns2xls
from types import SimpleNamespace
from pathlib import Path

data = SimpleNamespace(name='John Doe', age=30, city='New York')

# Преобразование в словарь
dict_data = ns2dict(data)
print(f'Словарь: {dict_data}')

# Преобразование в JSON
json_data = ns2json(data)
print(f'JSON: {json_data}')

# Преобразование в CSV
csv_file_path = Path('data.csv') 
result = ns2csv(data, csv_file_path)
print(f'CSV файл: {result}')

# Преобразование в XML
xml_data = ns2xml(data, root_tag='person')
print(f'XML: {xml_data}')

# Преобразование в XLS
xls_file_path = Path('data.xls')
result = ns2xls(data, xls_file_path)
print(f'XLS файл: {result}')
```