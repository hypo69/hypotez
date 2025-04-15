# Модуль для работы с JSON и SimpleNamespace
=================================================

Модуль содержит функции для загрузки (`j_loads`, `j_loads_ns`) и сохранения (`j_dumps`) данных в формате JSON, а также для преобразования между словарями и объектами `SimpleNamespace`.

## Обзор

Модуль предоставляет удобные инструменты для работы с JSON-данными, включая чтение из файлов, строк и объектов, а также запись в файлы. Он также поддерживает преобразование данных в объекты `SimpleNamespace` для более удобного доступа к атрибутам.

## Подробнее

Этот модуль облегчает работу с конфигурационными файлами, данными, полученными из API, и другими источниками JSON-данных. Он предоставляет функции для автоматического преобразования данных в нужный формат и обработки ошибок, таких как некорректный JSON или отсутствие файлов.

## Классы

### `Config`

**Описание**: Класс, содержащий константы для режимов записи файлов.

**Атрибуты**:
- `MODE_WRITE` (str): Режим записи "w".
- `MODE_APPEND_START` (str): Режим добавления в начало файла "a+".
- `MODE_APPEND_END` (str): Режим добавления в конец файла "+a".

## Функции

### `_convert_to_dict`

```python
def _convert_to_dict(value: Any) -> Any:
    """Convert SimpleNamespace and lists to dict."""
    ...
```

**Назначение**: Преобразует объекты `SimpleNamespace` и списки в словари.

**Параметры**:
- `value` (Any): Значение, которое нужно преобразовать.

**Возвращает**:
- `Any`: Преобразованное значение в виде словаря, списка или исходного значения, если преобразование не требуется.

**Как работает функция**:
- Если `value` является экземпляром `SimpleNamespace`, функция рекурсивно преобразует его атрибуты в словарь.
- Если `value` является словарем, функция рекурсивно преобразует его значения.
- Если `value` является списком, функция рекурсивно преобразует каждый элемент списка.
- В противном случае функция возвращает `value` без изменений.

**Примеры**:
```python
from types import SimpleNamespace
ns = SimpleNamespace(a=1, b=SimpleNamespace(c=2))
result = _convert_to_dict(ns)
print(result)  # Вывод: {'a': 1, 'b': {'c': 2}}

data = [SimpleNamespace(x=3), {'y': 4}]
result = _convert_to_dict(data)
print(result)  # Вывод: [{'x': 3}, {'y': 4}]
```

### `_read_existing_data`

```python
def _read_existing_data(path: Path, exc_info: bool = True) -> dict:
    """Read existing JSON data from a file."""
    ...
```

**Назначение**: Считывает существующие JSON-данные из файла.

**Параметры**:
- `path` (Path): Путь к файлу.
- `exc_info` (bool, optional): Если `True`, логирует исключения с трассировкой. По умолчанию `True`.

**Возвращает**:
- `dict`: Словарь с данными из файла или пустой словарь, если произошла ошибка.

**Вызывает исключения**:
- `json.JSONDecodeError`: Если не удается распарсить JSON.
- `Exception`: При других ошибках чтения файла.

**Как работает функция**:
- Пытается прочитать содержимое файла по указанному пути и распарсить его как JSON.
- Если возникает ошибка `json.JSONDecodeError`, логирует ошибку и возвращает пустой словарь.
- Если возникает любая другая ошибка, логирует ошибку и возвращает пустой словарь.

**Примеры**:
```python
from pathlib import Path
# Пример: файл существует и содержит корректный JSON
file_path = Path('config.json')
file_path.write_text('{"key": "value"}')
data = _read_existing_data(file_path)
print(data)  # Вывод: {'key': 'value'}

# Пример: файл не существует
file_path = Path('nonexistent.json')
data = _read_existing_data(file_path)
print(data)  # Вывод: {}
```

### `_merge_data`

```python
def _merge_data(
    data: Dict, existing_data: Dict, mode: str
) -> Dict:
    """Merge new data with existing data based on mode."""
    ...
```

**Назначение**: Объединяет новые данные с существующими данными в зависимости от режима.

**Параметры**:
- `data` (Dict): Новые данные для объединения.
- `existing_data` (Dict): Существующие данные.
- `mode` (str): Режим объединения (`Config.MODE_APPEND_START` или `Config.MODE_APPEND_END`).

**Возвращает**:
- `Dict`: Объединенные данные.

**Как работает функция**:
- Если `mode` равен `Config.MODE_APPEND_START`:
  - Если `data` и `existing_data` являются списками, возвращает конкатенацию `data` и `existing_data`.
  - Если `data` и `existing_data` являются словарями, обновляет `existing_data` данными из `data` и возвращает `existing_data`.
- Если `mode` равен `Config.MODE_APPEND_END`:
  - Если `data` и `existing_data` являются списками, возвращает конкатенацию `existing_data` и `data`.
  - Если `data` и `existing_data` являются словарями, обновляет `data` данными из `existing_data` и возвращает `data`.
- В противном случае возвращает `data`.
- В случае возникновения исключения, логирует ошибку и возвращает пустой словарь.

**Примеры**:
```python
data = {'new': 'value'}
existing_data = {'old': 'value'}
mode = Config.MODE_APPEND_START
result = _merge_data(data, existing_data, mode)
print(result)  # Вывод: {'old': 'value', 'new': 'value'}

data = [1, 2]
existing_data = [3, 4]
mode = Config.MODE_APPEND_END
result = _merge_data(data, existing_data, mode)
print(result)  # Вывод: [3, 4, 1, 2]
```

### `j_dumps`

```python
def j_dumps(
    data: Union[Dict, SimpleNamespace, List[Dict], List[SimpleNamespace]],
    file_path: Optional[Path] = None,
    ensure_ascii: bool = False,
    mode: str = Config.MODE_WRITE,
    exc_info: bool = True,
) -> Optional[Dict]:
    """
    Dump JSON data to a file or return the JSON data as a dictionary.

    Args:
        data (Dict | SimpleNamespace | List[Dict] | List[SimpleNamespace]): JSON-compatible data or SimpleNamespace objects to dump.
        file_path (Optional[Path], optional): Path to the output file. If None, returns JSON as a dictionary. Defaults to None.
        ensure_ascii (bool, optional): If True, escapes non-ASCII characters in output. Defaults to True.
        mode (str, optional): File open mode ('w', 'a+', '+a'). Defaults to 'w'.
        exc_info (bool, optional): If True, logs exceptions with traceback. Defaults to True.

    Returns:
        Optional[Dict]: JSON data as a dictionary if successful, or nothing if an error occurs.

    Raises:
        ValueError: If the file mode is unsupported.
    """
    ...
```

**Назначение**: Записывает JSON-данные в файл или возвращает JSON-данные в виде словаря.

**Параметры**:
- `data` (Dict | SimpleNamespace | List[Dict] | List[SimpleNamespace]): JSON-совместимые данные или объекты `SimpleNamespace` для записи.
- `file_path` (Optional[Path], optional): Путь к выходному файлу. Если `None`, возвращает JSON в виде словаря. По умолчанию `None`.
- `ensure_ascii` (bool, optional): Если `True`, экранирует символы, не входящие в ASCII, в выходных данных. По умолчанию `False`.
- `mode` (str, optional): Режим открытия файла (`'w'`, `'a+'`, `'+a'`). По умолчанию `'w'`.
- `exc_info` (bool, optional): Если `True`, логирует исключения с трассировкой. По умолчанию `True`.

**Возвращает**:
- `Optional[Dict]`: JSON-данные в виде словаря при успехе или `None` при ошибке.

**Как работает функция**:
1. Преобразует входные данные в словарь, если они представлены в виде строки, `SimpleNamespace` или списка.
2. Определяет режим записи файла. Если указанный режим не поддерживается, устанавливает режим `'w'` по умолчанию.
3. Если указан путь к файлу и режим предполагает добавление данных (`'a+'` или `'+a'`), считывает существующие данные из файла.
4. Объединяет новые данные с существующими данными, если это необходимо.
5. Записывает данные в файл в формате JSON с использованием указанного режима и параметров.
6. В случае возникновения исключения логирует ошибку и возвращает `None`.

**Примеры**:

```python
from pathlib import Path
from types import SimpleNamespace

# Пример 1: Запись данных в файл
data = {'key': 'value'}
file_path = Path('output.json')
result = j_dumps(data, file_path=file_path)
print(result)  # Вывод: {'key': 'value'}

# Пример 2: Возврат данных в виде словаря
data = SimpleNamespace(key='value')
result = j_dumps(data)
print(result)  # Вывод: {'key': 'value'}

# Пример 3: Добавление данных в начало файла
file_path = Path('append.json')
file_path.write_text('{"old_key": "old_value"}')
data = {'new_key': 'new_value'}
result = j_dumps(data, file_path=file_path, mode='a+')
print(result) # Вывод: {'old_key': 'old_value', 'new_key': 'new_value'}

# Пример 4: Некорректный JSON
data = "{'key': 'value'}"
result = j_dumps(data)
print(result) # Вывод: None
```

### `_decode_strings`

```python
def _decode_strings(data: Any) -> Any:
    """Recursively decode strings in a data structure."""
    ...
```

**Назначение**: Рекурсивно декодирует строки в структуре данных.

**Параметры**:
- `data` (Any): Структура данных для декодирования.

**Возвращает**:
- `Any`: Декодированная структура данных.

**Как работает функция**:
- Если `data` является строкой, пытается декодировать ее с помощью `codecs.decode(data, 'unicode_escape')`. Если декодирование не удается, возвращает исходную строку.
- Если `data` является списком, рекурсивно декодирует каждый элемент списка.
- Если `data` является словарем, рекурсивно декодирует каждый ключ и значение словаря.
- В противном случае возвращает `data` без изменений.

**Примеры**:
```python
# Пример 1: Декодирование строки
data = '\\u041f\\u0440\\u0438\\u0432\\u0435\\u0442'
result = _decode_strings(data)
print(result)  # Вывод: Привет

# Пример 2: Декодирование списка строк
data = ['\\u041f\\u0440\\u0438\\u0432\\u0435\\u0442', '\\u041c\\u0438\\u0440']
result = _decode_strings(data)
print(result)  # Вывод: ['Привет', 'Мир']

# Пример 3: Декодирование словаря
data = {'key': '\\u0417\\u043d\\u0430\\u0447\\u0435\\u043d\\u0438\\u0435'}
result = _decode_strings(data)
print(result)  # Вывод: {'key': 'Значение'}
```

### `_string_to_dict`

```python
def _string_to_dict(json_string: str) -> dict:
    """Remove markdown quotes and parse JSON string."""
    ...
```

**Назначение**: Удаляет markdown-кавычки и разбирает JSON-строку.

**Параметры**:
- `json_string` (str): JSON-строка для разбора.

**Возвращает**:
- `dict`: Словарь, полученный из JSON-строки.

**Как работает функция**:
- Если `json_string` начинается с "```" или "```json" и заканчивается на "```" или "```\n", удаляет эти markdown-кавычки.
- Пытается разобрать строку как JSON.
- Если возникает ошибка `json.JSONDecodeError`, логирует ошибку и возвращает пустой словарь.

**Примеры**:
```python
# Пример 1: JSON-строка с markdown-кавычками
json_string = "```json\n{\"key\": \"value\"}\n```"
result = _string_to_dict(json_string)
print(result)  # Вывод: {'key': 'value'}

# Пример 2: JSON-строка без markdown-кавычек
json_string = "{\"key\": \"value\"}"
result = _string_to_dict(json_string)
print(result)  # Вывод: {'key': 'value'}

# Пример 3: Некорректная JSON-строка
json_string = "{\"key\": \"value\""
result = _string_to_dict(json_string)
print(result)  # Вывод: {}
```

### `j_loads`

```python
def j_loads(
    jjson: Union[dict, SimpleNamespace, str, Path, list], ordered: bool = True
) -> Union[dict, list]:
    """
    Load JSON or CSV data from a file, directory, string, or object.

    Args:
        jjson (dict | SimpleNamespace | str | Path | list): Path to file/directory, JSON string, or JSON object.
        ordered (bool, optional): Use OrderedDict to preserve element order. Defaults to True.

    Returns:
        dict | list: Processed data (dictionary or list of dictionaries).

    Raises:
        FileNotFoundError: If the specified file is not found.
        json.JSONDecodeError: If the JSON data cannot be parsed.
    """
    ...
```

**Назначение**: Загружает JSON-данные из файла, каталога, строки или объекта.

**Параметры**:
- `jjson` (dict | SimpleNamespace | str | Path | list): Путь к файлу/каталогу, JSON-строка или JSON-объект.
- `ordered` (bool, optional): Использовать `OrderedDict` для сохранения порядка элементов. По умолчанию `True`.

**Возвращает**:
- `dict | list`: Обработанные данные (словарь или список словарей).

**Как работает функция**:
1. Если `jjson` является экземпляром `SimpleNamespace`, преобразует его в словарь.
2. Если `jjson` является объектом `Path`:
   - Если это каталог, рекурсивно загружает все JSON-файлы в каталоге.
   - Если это файл, считывает и разбирает JSON-данные из файла.
3. Если `jjson` является строкой, разбирает ее как JSON-строку.
4. Если `jjson` является списком, рекурсивно декодирует строки в списке.
5. Если `jjson` является словарем, рекурсивно декодирует строки в словаре.
6. Обрабатывает исключения, такие как `FileNotFoundError` и `json.JSONDecodeError`, логирует ошибки и возвращает пустой словарь.

**Примеры**:

```python
from pathlib import Path
from types import SimpleNamespace

# Пример 1: Загрузка из файла
file_path = Path('data.json')
file_path.write_text('{"key": "value"}')
data = j_loads(file_path)
print(data)  # Вывод: {'key': 'value'}

# Пример 2: Загрузка из строки
json_string = '{"key": "value"}'
data = j_loads(json_string)
print(data)  # Вывод: {'key': 'value'}

# Пример 3: Загрузка из SimpleNamespace
ns = SimpleNamespace(key='value')
data = j_loads(ns)
print(data)  # Вывод: {'key': 'value'}

# Пример 4: Загрузка из списка
data = ['\\u041f\\u0440\\u0438\\u0432\\u0435\\u0442']
result = j_loads(data)
print(result)  # Вывод: ['Привет']

# Пример 5: Несуществующий файл
file_path = Path('nonexistent.json')
data = j_loads(file_path)
print(data)  # Вывод: {}
```

### `j_loads_ns`

```python
def j_loads_ns(
    jjson: Union[Path, SimpleNamespace, Dict, str], ordered: bool = True
) -> Union[SimpleNamespace, List[SimpleNamespace], Dict]:
    """Load JSON/CSV data and convert to SimpleNamespace."""
    ...
```

**Назначение**: Загружает JSON-данные и преобразует их в объекты `SimpleNamespace`.

**Параметры**:
- `jjson` (Path | SimpleNamespace | Dict | str): Путь к файлу, объект `SimpleNamespace`, словарь или JSON-строка.
- `ordered` (bool, optional): Использовать `OrderedDict` для сохранения порядка элементов. По умолчанию `True`.

**Возвращает**:
- `SimpleNamespace | List[SimpleNamespace] | Dict`: Обработанные данные в виде объекта `SimpleNamespace`, списка объектов `SimpleNamespace` или словаря.

**Как работает функция**:
1. Загружает JSON-данные с помощью функции `j_loads`.
2. Если данные загружены успешно:
   - Если данные являются списком, преобразует каждый элемент списка в объект `SimpleNamespace`.
   - Если данные являются словарем, преобразует словарь в объект `SimpleNamespace`.
3. Возвращает преобразованные данные.
4. В случае ошибки возвращает пустой словарь.

**Примеры**:
```python
from pathlib import Path
from types import SimpleNamespace

# Пример 1: Загрузка из файла и преобразование в SimpleNamespace
file_path = Path('data.json')
file_path.write_text('{"key": "value"}')
data = j_loads_ns(file_path)
print(data)  # Вывод: namespace(key='value')

# Пример 2: Загрузка из строки и преобразование в SimpleNamespace
json_string = '{"key": "value"}'
data = j_loads_ns(json_string)
print(data)  # Вывод: namespace(key='value')

# Пример 3: Загрузка из списка и преобразование в список SimpleNamespace
json_string = '[{"key1": "value1"}, {"key2": "value2"}]'
file_path = Path('data.json')
file_path.write_text(json_string)
data = j_loads_ns(file_path)
print(data)

# Пример 4: Загрузка из словаря
data = {"key": "value"}
result = j_loads_ns(data)
print(result)