# Модуль для работы с JSON и SimpleNamespace

## Обзор

Модуль `jjson` предоставляет функции для загрузки и сохранения данных в формате JSON, а также для преобразования данных в объекты `SimpleNamespace`. Он включает в себя функции для чтения JSON из файлов, строк и объектов, а также для записи данных в файлы. Модуль также поддерживает объединение JSON-данных и преобразование строк с escape-последовательностями Unicode.

## Более подробно

Модуль `jjson` предоставляет удобные инструменты для работы с данными в формате JSON. Он облегчает чтение, запись и преобразование данных, а также предоставляет возможности для обработки ошибок и логирования. Этот модуль используется для работы с файлами конфигурации, обмена данными между компонентами системы и хранения структурированной информации.

## Классы

### `Config`

**Описание**: Класс для хранения констант, используемых при работе с файлами.

**Атрибуты**:
- `MODE_WRITE` (str): Режим записи файла ("w").
- `MODE_APPEND_START` (str): Режим добавления в начало файла ("a+").
- `MODE_APPEND_END` (str): Режим добавления в конец файла ("+a").

```python
@dataclass
class Config:
    MODE_WRITE:str = "w"
    MODE_APPEND_START:str = "a+"
    MODE_APPEND_END:str = "+a"
```

## Функции

### `_convert_to_dict`

**Назначение**: Преобразует объекты `SimpleNamespace` и списки в словари.

**Параметры**:
- `value` (Any): Значение, которое нужно преобразовать.

**Возвращает**:
- Any: Преобразованное значение в виде словаря или списка.

**Как работает функция**:
- Функция рекурсивно преобразует объекты `SimpleNamespace` и списки в словари, чтобы обеспечить совместимость с JSON.

**Примеры**:
```python
from types import SimpleNamespace
data = SimpleNamespace(name="John", age=30)
result = _convert_to_dict(data)
print(result)  # {'name': 'John', 'age': 30}
```
```python
data = [SimpleNamespace(name="John"), SimpleNamespace(name="Jane")]
result = _convert_to_dict(data)
print(result)  # [{'name': 'John'}, {'name': 'Jane'}]
```
```python
data = {'name': SimpleNamespace(first="John", last="Doe")}
result = _convert_to_dict(data)
print(result) # {'name': {'first': 'John', 'last': 'Doe'}}
```

### `_read_existing_data`

**Назначение**: Читает существующие JSON-данные из файла.

**Параметры**:
- `path` (Path): Путь к файлу.
- `exc_info` (bool): Флаг, определяющий, нужно ли логировать информацию об исключении. По умолчанию `True`.

**Возвращает**:
- dict: Словарь с данными из файла или пустой словарь в случае ошибки.

**Как работает функция**:
- Функция пытается прочитать JSON-данные из файла, используя указанный путь. В случае ошибки декодирования JSON или других исключений, функция логирует ошибку и возвращает пустой словарь.

**Примеры**:
```python
from pathlib import Path
file_path = Path("data.json")
file_path.write_text('{"name": "John", "age": 30}')
result = _read_existing_data(file_path)
print(result)  # {'name': 'John', 'age': 30}
```
```python
from pathlib import Path
file_path = Path("nonexistent.json")
result = _read_existing_data(file_path)
print(result)  # {}
```

### `_merge_data`

**Назначение**: Объединяет новые данные с существующими данными в зависимости от режима.

**Параметры**:
- `data` (Dict): Новые данные для объединения.
- `existing_data` (Dict): Существующие данные.
- `mode` (str): Режим объединения (Config.MODE_APPEND_START, Config.MODE_APPEND_END).

**Возвращает**:
- Dict: Объединенные данные.

**Как работает функция**:
- Функция объединяет новые данные с существующими данными в зависимости от указанного режима. Если режим `Config.MODE_APPEND_START`, новые данные добавляются в начало существующих данных. Если режим `Config.MODE_APPEND_END`, новые данные добавляются в конец существующих данных.

**Примеры**:
```python
data = {"new": "value"}
existing_data = {"old": "value"}
mode = Config.MODE_APPEND_START
result = _merge_data(data, existing_data, mode)
print(result)  # {'old': 'value', 'new': 'value'}
```
```python
data = {"new": "value"}
existing_data = {"old": "value"}
mode = Config.MODE_APPEND_END
result = _merge_data(data, existing_data, mode)
print(result)  # {'new': 'value', 'old': 'value'}
```

### `j_dumps`

**Назначение**: Записывает JSON-данные в файл или возвращает JSON-данные в виде словаря.

**Параметры**:
- `data` (Union[Dict, SimpleNamespace, List[Dict], List[SimpleNamespace]]): JSON-совместимые данные или объекты `SimpleNamespace` для записи.
- `file_path` (Optional[Path], optional): Путь к выходному файлу. Если `None`, возвращает JSON в виде словаря. По умолчанию `None`.
- `ensure_ascii` (bool, optional): Если `True`, экранирует не-ASCII символы в выводе. По умолчанию `True`.
- `mode` (str, optional): Режим открытия файла ('w', 'a+', '+a'). По умолчанию 'w'.
- `exc_info` (bool, optional): Если `True`, логирует исключения с трассировкой. По умолчанию `True`.

**Возвращает**:
- Optional[Dict]: JSON-данные в виде словаря в случае успеха или `None`, если произошла ошибка.

**Вызывает**:
- ValueError: Если указан неподдерживаемый режим файла.

**Как работает функция**:
- Функция преобразует входные данные в словарь, объединяет их с существующими данными (если указан путь к файлу и режим добавления), а затем записывает данные в файл в формате JSON. Если `file_path` не указан, функция возвращает JSON-данные в виде словаря.

**Примеры**:
```python
from pathlib import Path
data = {"name": "John", "age": 30}
file_path = Path("data.json")
result = j_dumps(data, file_path)
print(result)  # {'name': 'John', 'age': 30}
```
```python
data = {"name": "John", "age": 30}
result = j_dumps(data)
print(result)  # {'name': 'John', 'age': 30}
```

### `_decode_strings`

**Назначение**: Рекурсивно декодирует строки в структуре данных.

**Параметры**:
- `data` (Any): Данные для декодирования.

**Возвращает**:
- Any: Декодированные данные.

**Как работает функция**:
- Функция рекурсивно проходит по структуре данных и декодирует все строки, используя кодировку `unicode_escape`.

**Примеры**:
```python
data = {"name": "John\\u0020Doe", "age": 30}
result = _decode_strings(data)
print(result)  # {'name': 'John Doe', 'age': 30}
```
```python
data = ["John\\u0020Doe", 30]
result = _decode_strings(data)
print(result)  # ['John Doe', 30]
```

### `_string_to_dict`

**Назначение**: Удаляет markdown-кавычки и преобразует JSON-строку в словарь.

**Параметры**:
- `json_string` (str): JSON-строка.

**Возвращает**:
- dict: Словарь, полученный из JSON-строки, или пустой словарь в случае ошибки.

**Как работает функция**:
- Функция удаляет markdown-кавычки (если они есть) из JSON-строки и преобразует строку в словарь. В случае ошибки парсинга JSON, функция логирует ошибку и возвращает пустой словарь.

**Примеры**:
```python
json_string = "```json\n{\"name\": \"John\", \"age\": 30}\n```"
result = _string_to_dict(json_string)
print(result)  # {'name': 'John', 'age': 30}
```
```python
json_string = "{\"name\": \"John\", \"age\": 30}"
result = _string_to_dict(json_string)
print(result)  # {'name': 'John', 'age': 30}
```
```python
json_string = "```\n{\"name\": \"John\", \"age\": 30}\n```"
result = _string_to_dict(json_string)
print(result)  # {'name': 'John', 'age': 30}
```

### `j_loads`

**Назначение**: Загружает JSON или CSV-данные из файла, каталога, строки или объекта.

**Параметры**:
- `jjson` (Union[dict, SimpleNamespace, str, Path, list]): Путь к файлу/каталогу, JSON-строка или JSON-объект.
- `ordered` (bool, optional): Использовать `OrderedDict` для сохранения порядка элементов. По умолчанию `True`.

**Возвращает**:
- Union[dict, list]: Обработанные данные (словарь или список словарей).

**Вызывает**:
- FileNotFoundError: Если указанный файл не найден.
- json.JSONDecodeError: Если JSON-данные не могут быть распарсены.

**Как работает функция**:
- Функция загружает JSON-данные из файла, каталога, строки или объекта. Если указан путь к каталогу, функция загружает все JSON-файлы из этого каталога. Если указана JSON-строка, функция преобразует строку в словарь.

**Примеры**:
```python
from pathlib import Path
file_path = Path("data.json")
file_path.write_text('{"name": "John", "age": 30}')
result = j_loads(file_path)
print(result)  # {'name': 'John', 'age': 30}
```
```python
json_string = "{\"name\": \"John\", \"age\": 30}"
result = j_loads(json_string)
print(result)  # {'name': 'John', 'age': 30}
```

### `j_loads_ns`

**Назначение**: Загружает JSON/CSV-данные и преобразует их в `SimpleNamespace`.

**Параметры**:
- `jjson` (Union[Path, SimpleNamespace, Dict, str]): Путь, объект `SimpleNamespace`, словарь или строка с JSON/CSV-данными.
- `ordered` (bool, optional): Использовать `OrderedDict` для сохранения порядка элементов. По умолчанию `True`.

**Возвращает**:
- Union[SimpleNamespace, List[SimpleNamespace], Dict]: Данные, преобразованные в `SimpleNamespace` или список `SimpleNamespace`.

**Как работает функция**:
- Функция загружает JSON/CSV-данные с использованием `j_loads` и преобразует их в объекты `SimpleNamespace`. Если данные представлены в виде списка, функция преобразует каждый элемент списка в `SimpleNamespace`.

**Примеры**:
```python
from pathlib import Path
file_path = Path("data.json")
file_path.write_text('{"name": "John", "age": 30}')
result = j_loads_ns(file_path)
print(result)  # namespace(name='John', age=30)
```
```python
json_string = "{\"name\": \"John\", \"age\": 30}"
result = j_loads_ns(json_string)
print(result)  # namespace(name='John', age=30)
```
```python
from types import SimpleNamespace
jjson = SimpleNamespace(name="John", age=30)
result = j_loads_ns(jjson)
print(result)  # namespace(name='John', age=30)