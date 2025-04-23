# Модуль для работы с JSON и SimpleNamespace

## Обзор

Модуль `src.utils.jjson` предоставляет набор функций для работы с данными в формате JSON, включая загрузку, выгрузку, преобразование и обработку ошибок. Он также поддерживает преобразование данных в объекты `SimpleNamespace` для удобного доступа к данным через атрибуты.

## Подробнее

Этот модуль предназначен для упрощения работы с JSON-данными в проекте `hypotez`. Он предоставляет функции для чтения данных из файлов, строк и объектов, а также для записи данных в файлы. Модуль также включает функции для обработки ошибок и преобразования данных между различными форматами.

## Классы

### `Config`

**Описание**: Класс `Config` определяет константы, используемые для указания режимов записи файлов.

**Атрибуты**:
- `MODE_WRITE` (str): Режим записи "w".
- `MODE_APPEND_START` (str): Режим дозаписи в начало файла "a+".
- `MODE_APPEND_END` (str): Режим дозаписи в конец файла "+a".

**Принцип работы**:

Класс `Config` используется для хранения констант, определяющих режимы записи в файл. Это позволяет избежать использования строковых литералов в коде и упрощает изменение режимов записи в одном месте.

## Функции

### `_convert_to_dict`

**Назначение**: Преобразует объекты `SimpleNamespace` и списки в словари.

**Параметры**:
- `value` (Any): Значение для преобразования. Может быть объектом `SimpleNamespace`, словарем, списком или любым другим типом данных.

**Возвращает**:
- `Any`: Преобразованное значение в виде словаря, списка или исходного значения, если преобразование не требуется.

**Как работает функция**:
Функция рекурсивно проходит по входному значению и преобразует объекты `SimpleNamespace` в словари, а также обрабатывает списки и словари, преобразуя их элементы.

**Примеры**:

```python
from types import SimpleNamespace
data = SimpleNamespace(name="John", age=30)
result = _convert_to_dict(data)
print(result)  # Вывод: {'name': 'John', 'age': 30}

data = [SimpleNamespace(name="John", age=30), {"city": "New York"}]
result = _convert_to_dict(data)
print(result)  # Вывод: [{'name': 'John', 'age': 30}, {'city': 'New York'}]
```

### `_read_existing_data`

**Назначение**: Читает существующие JSON-данные из файла.

**Параметры**:
- `path` (Path): Путь к файлу.
- `exc_info` (bool, optional): Если `True`, логирует исключения с трассировкой. По умолчанию `True`.

**Возвращает**:
- `dict`: Словарь с данными из JSON-файла. Возвращает пустой словарь `{}` в случае ошибки.

**Как работает функция**:
Функция пытается прочитать JSON-данные из файла, указанного в параметре `path`. Если файл не найден или содержит невалидные JSON-данные, функция логирует ошибку и возвращает пустой словарь.

**Примеры**:

```python
from pathlib import Path
file_path = Path("data.json")
file_path.write_text('{"name": "John", "age": 30}')
data = _read_existing_data(file_path)
print(data)  # Вывод: {'name': 'John', 'age': 30}
file_path.unlink() # удаляем тестовый файл

file_path = Path("non_existent_file.json")
data = _read_existing_data(file_path)
print(data)  # Вывод: {}
```

### `_merge_data`

**Назначение**: Объединяет новые данные с существующими данными в зависимости от режима.

**Параметры**:
- `data` (Dict): Новые данные для объединения.
- `existing_data` (Dict): Существующие данные.
- `mode` (str): Режим объединения (Config.MODE_APPEND_START, Config.MODE_APPEND_END).

**Возвращает**:
- `Dict`: Объединенные данные в виде словаря. Возвращает пустой словарь `{}` в случае ошибки.

**Как работает функция**:

Функция объединяет новые данные с существующими в зависимости от указанного режима. Если режим `Config.MODE_APPEND_START`, новые данные добавляются в начало существующих (если это списки) или обновляют существующие (если это словари). Если режим `Config.MODE_APPEND_END`, новые данные добавляются в конец существующих (если это списки) или обновляют существующие (если это словари).

**Примеры**:

```python
data = {"city": "New York"}
existing_data = {"name": "John", "age": 30}
mode = Config.MODE_APPEND_START
result = _merge_data(data, existing_data, mode)
print(result)  # Вывод: {'name': 'John', 'age': 30, 'city': 'New York'}

data = [1, 2, 3]
existing_data = [4, 5, 6]
mode = Config.MODE_APPEND_END
result = _merge_data(data, existing_data, mode)
print(result)  # Вывод: [4, 5, 6, 1, 2, 3]
```

### `j_dumps`

**Назначение**: Выгружает JSON-данные в файл или возвращает JSON-данные в виде словаря.

**Параметры**:
- `data` (Union[Dict, SimpleNamespace, List[Dict], List[SimpleNamespace]]): JSON-совместимые данные или объекты SimpleNamespace для выгрузки.
- `file_path` (Optional[Path], optional): Путь к выходному файлу. Если `None`, возвращает JSON в виде словаря. По умолчанию `None`.
- `ensure_ascii` (bool, optional): Если `True`, экранирует не-ASCII символы в выводе. По умолчанию `False`.
- `mode` (str, optional): Режим открытия файла ('w', 'a+', '+a'). По умолчанию 'w'.
- `exc_info` (bool, optional): Если `True`, логирует исключения с трассировкой. По умолчанию `True`.

**Возвращает**:
- `Optional[Dict]`: JSON-данные в виде словаря в случае успеха или `None`, если произошла ошибка.

**Вызывает исключения**:
- `ValueError`: Если режим файла не поддерживается.

**Как работает функция**:

Функция `j_dumps` принимает JSON-совместимые данные и записывает их в файл, если указан `file_path`. Если `file_path` не указан, функция возвращает JSON-данные в виде словаря. Функция поддерживает различные режимы записи (запись, добавление в начало, добавление в конец) и обрабатывает исключения, логируя их при необходимости.

**Примеры**:

```python
from pathlib import Path
data = {"name": "John", "age": 30}
file_path = Path("data.json")
result = j_dumps(data, file_path=file_path)
print(result)  # Вывод: {'name': 'John', 'age': 30}
print(file_path.read_text()) # {"name": "John", "age": 30}
file_path.unlink() # удаляем тестовый файл

result = j_dumps(data)
print(result)  # Вывод: {'name': 'John', 'age': 30}
```

### `_decode_strings`

**Назначение**: Рекурсивно декодирует строки в структуре данных.

**Параметры**:
- `data` (Any): Данные для декодирования.

**Возвращает**:
- `Any`: Декодированные данные.

**Как работает функция**:
Функция рекурсивно проходит по входным данным и пытается декодировать строки с использованием кодека `unicode_escape`. Если декодирование не удается, возвращает исходную строку.

**Примеры**:

```python
data = {"name": "John\\u0020Doe", "age": 30}
result = _decode_strings(data)
print(result)  # Вывод: {'name': 'John Doe', 'age': 30}

data = ["string\\u00201", "string 2"]
result = _decode_strings(data)
print(result)  # Вывод: ['string 1', 'string 2']
```

### `_string_to_dict`

**Назначение**: Удаляет markdown-кавычки и парсит JSON-строку.

**Параметры**:
- `json_string` (str): JSON-строка для парсинга.

**Возвращает**:
- `dict`: Словарь, полученный из JSON-строки. Возвращает пустой словарь `{}` в случае ошибки парсинга.

**Как работает функция**:
Функция удаляет markdown-кавычки (если они есть) из JSON-строки и пытается распарсить её с помощью `json.loads`. В случае ошибки парсинга логирует ошибку и возвращает пустой словарь.

**Примеры**:

```python
json_string = "```json\n{\"name\": \"John\", \"age\": 30}\n```"
result = _string_to_dict(json_string)
print(result)  # Вывод: {'name': 'John', 'age': 30}

json_string = "{\"name\": \"John\", \"age\": 30}"
result = _string_to_dict(json_string)
print(result)  # Вывод: {'name': 'John', 'age': 30}

json_string = "invalid json"
result = _string_to_dict(json_string)
print(result)  # Вывод: {}
```

### `j_loads`

**Назначение**: Загружает JSON или CSV-данные из файла, каталога, строки или объекта.

**Параметры**:
- `jjson` (Union[dict, SimpleNamespace, str, Path, list]): Путь к файлу/каталогу, JSON-строка или JSON-объект.
- `ordered` (bool, optional): Использовать OrderedDict для сохранения порядка элементов. По умолчанию `True`.

**Возвращает**:
- `Union[dict, list]`: Обработанные данные (словарь или список словарей).

**Вызывает исключения**:
- `FileNotFoundError`: Если указанный файл не найден.
- `json.JSONDecodeError`: Если JSON-данные не могут быть распарсены.

**Как работает функция**:

Функция `j_loads` принимает различные типы входных данных (путь к файлу, JSON-строку, объект) и пытается загрузить и распарсить JSON-данные. Если входные данные являются путем к каталогу, функция рекурсивно загружает все JSON-файлы в этом каталоге. Функция также обрабатывает ошибки, логируя их при необходимости.

**Примеры**:

```python
from pathlib import Path
file_path = Path("data.json")
file_path.write_text('{"name": "John", "age": 30}')
data = j_loads(file_path)
print(data)  # Вывод: {'name': 'John', 'age': 30}
file_path.unlink() # удаляем тестовый файл

json_string = "{\"name\": \"John\", \"age\": 30}"
data = j_loads(json_string)
print(data)  # Вывод: {'name': 'John', 'age': 30}
```

### `j_loads_ns`

**Назначение**: Загружает JSON/CSV-данные и преобразует в SimpleNamespace.

**Параметры**:
- `jjson` (Union[Path, SimpleNamespace, Dict, str]): Путь, SimpleNamespace, Dict или строка с JSON-данными.
- `ordered` (bool, optional): Использовать ли OrderedDict для сохранения порядка элементов. По умолчанию `True`.

**Возвращает**:
- `Union[SimpleNamespace, List[SimpleNamespace], Dict]`: Данные в виде SimpleNamespace или списка SimpleNamespace.

**Как работает функция**:

Функция `j_loads_ns` использует функцию `j_loads` для загрузки данных из различных источников, а затем преобразует полученные данные в объекты `SimpleNamespace` для удобного доступа к атрибутам.

**Примеры**:

```python
from pathlib import Path
file_path = Path("data.json")
file_path.write_text('{"name": "John", "age": 30}')
data = j_loads_ns(file_path)
print(data.name)  # Вывод: John
file_path.unlink() # удаляем тестовый файл

json_string = "{\"name\": \"John\", \"age\": 30}"
data = j_loads_ns(json_string)
print(data.age)  # Вывод: 30