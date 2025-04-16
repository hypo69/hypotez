# Модуль для работы с JSON (jjson.py)

## Обзор

Этот модуль предоставляет набор утилит для работы с данными в формате JSON, включая загрузку данных из файлов, строк и объектов, а также сохранение данных в файлы. Он включает функции для преобразования данных в различные структуры данных, такие как словари и SimpleNamespace, а также для исправления ошибок в JSON-строках.

## Подробней

Модуль предназначен для упрощения работы с данными в формате JSON в проекте `hypotez`. Он предоставляет удобные функции для загрузки, сохранения и преобразования данных, а также для обработки ошибок, которые могут возникнуть при работе с JSON.

## Функции

### `_convert_to_dict`

**Назначение**: Преобразует объекты `SimpleNamespace` и списки в словари.

```python
def _convert_to_dict(value: Any) -> Any:
    """Convert SimpleNamespace and lists to dict."""
    ...
```

**Параметры**:

-   `value` (Any): Значение, которое необходимо преобразовать.

**Возвращает**:

-   `Any`: Преобразованное значение (словарь, список или исходное значение, если преобразование не требуется).

**Как работает функция**:

1.  Проверяет тип входного значения.
2.  Если значение является объектом `SimpleNamespace`, преобразует его в словарь, рекурсивно применяя `_convert_to_dict` к каждому значению атрибута.
3.  Если значение является словарем, рекурсивно применяет `_convert_to_dict` к каждому значению.
4.  Если значение является списком, рекурсивно применяет `_convert_to_dict` к каждому элементу списка.
5.  В противном случае возвращает исходное значение без изменений.

### `_read_existing_data`

**Назначение**: Читает существующие данные JSON из файла.

```python
def _read_existing_data(path: Path, exc_info: bool = True) -> dict:
    """Read existing JSON data from a file."""
    ...
```

**Параметры**:

-   `path` (Path): Путь к файлу JSON.
-   `exc_info` (bool): Включать ли информацию об исключении в логи. По умолчанию `True`.

**Возвращает**:

-   `dict`: Словарь, содержащий данные JSON из файла, или пустой словарь в случае ошибки.

**Как работает функция**:

1.  Пытается прочитать содержимое файла, используя `path.read_text(encoding="utf-8")`.
2.  Пытается преобразовать содержимое файла в словарь, используя `json.loads`.
3.  В случае ошибки при чтении или разборе JSON логирует ошибку с использованием `logger.error` и возвращает пустой словарь.

### `_merge_data`

**Назначение**: Объединяет новые данные с существующими данными на основе указанного режима.

```python
def _merge_data(
    data: Dict, existing_data: Dict, mode: str
) -> Dict:
    """Merge new data with existing data based on mode."""
    ...
```

**Параметры**:

-   `data` (Dict): Новые данные для объединения.
-   `existing_data` (Dict): Существующие данные.
-   `mode` (str): Режим объединения (`Config.MODE_APPEND_START` или `Config.MODE_APPEND_END`).

**Возвращает**:

-   `Dict`: Объединенные данные (словарь или список).

**Как работает функция**:

1.  В зависимости от значения `mode` выполняет объединение данных:
    -   `Config.MODE_APPEND_START`: Добавляет новые данные в начало существующих данных (если это списки) или обновляет существующие данные новыми (если это словари).
    -   `Config.MODE_APPEND_END`: Добавляет новые данные в конец существующих данных (если это списки) или обновляет новые данные существующими (если это словари).
2.  Если `mode` не соответствует ни одному из поддерживаемых значений, возвращает исходные данные (`data`).
3.  Логирует информацию об ошибке, используя `logger.error`.

### `j_dumps`

**Назначение**: Преобразует данные JSON в строку и записывает их в файл или возвращает данные JSON в виде словаря.

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

**Параметры**:

-   `data` (Union[Dict, SimpleNamespace, List[Dict], List[SimpleNamespace]]): Данные, совместимые с JSON, или объекты `SimpleNamespace` для сохранения.
-   `file_path` (Optional[Path]): Путь к файлу для сохранения. Если `None`, возвращает данные JSON в виде словаря. По умолчанию `None`.
-   `ensure_ascii` (bool): Если `True`, экранирует символы, не входящие в ASCII. По умолчанию `False`.
-   `mode` (str): Режим открытия файла (`'w'`, `'a+'`, `'+a'`). По умолчанию `'w'`.
-   `exc_info` (bool): Если `True`, логирует исключения с информацией об отслеживании. По умолчанию `True`.

**Возвращает**:

-   `Optional[Dict]`: Данные JSON в виде словаря при успехе или `None` при возникновении ошибки.

**Вызывает исключения**:

-   `ValueError`: Если режим файла не поддерживается.

**Как работает функция**:

1.  Преобразует входные данные в словарь, используя функцию `_convert_to_dict`.
2.  В зависимости от режима (`mode`) выполняет объединение данных с существующими данными в файле (если файл существует и указан режим добавления).
3.  Открывает файл для записи (если указан `file_path`) и записывает данные JSON в файл с указанными параметрами (`ensure_ascii`, `indent`).
4.  Если `file_path` не указан, возвращает данные JSON в виде словаря.
5.  Обрабатывает исключения, логирует ошибки и возвращает `None` в случае ошибки.

### `_decode_strings`

**Назначение**: Рекурсивно декодирует строки в структуре данных.

```python
def _decode_strings(data: Any) -> Any:
    """Recursively decode strings in a data structure."""
    ...
```

**Параметры**:

-   `data` (Any): Данные для декодирования.

**Возвращает**:

-   `Any`: Декодированные данные.

**Как работает функция**:

1.  Если входные данные - строка, пытается декодировать её, используя `codecs.decode(data, 'unicode_escape')`.
2.  Если входные данные - список, рекурсивно вызывает `_decode_strings` для каждого элемента списка.
3.  Если входные данные - словарь, рекурсивно вызывает `_decode_strings` для каждого ключа и значения в словаре.
4.  В противном случае возвращает исходные данные без изменений.

### `_string_to_dict`

**Назначение**: Удаляет Markdown-кавычки и преобразует JSON-строку в словарь.

```python
def _string_to_dict(json_string: str) -> dict:
    """Remove markdown quotes and parse JSON string."""
    ...
```

**Параметры**:

-   `json_string` (str): JSON-строка для преобразования.

**Возвращает**:

-   `dict`: Словарь, полученный из JSON-строки, или пустой словарь в случае ошибки.

**Как работает функция**:

1.  Удаляет Markdown-кавычки (```` ``` ````) из начала и конца строки.
2.  Пытается преобразовать строку в словарь, используя `json.loads`.
3.  В случае ошибки разбора JSON логирует ошибку и возвращает пустой словарь.

### `j_loads`

**Назначение**: Загружает данные JSON или CSV из файла, директории, строки или объекта.

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

**Параметры**:

-   `jjson` (Union[dict, SimpleNamespace, str, Path, list]): Путь к файлу/директории, JSON-строка или JSON-объект.
-   `ordered` (bool): Использовать ли `OrderedDict` для сохранения порядка элементов. По умолчанию `True`.

**Возвращает**:

-   `Union[dict, list]`: Обработанные данные (словарь или список словарей).

**Вызывает исключения**:

-   `FileNotFoundError`: Если указанный файл не найден.
-   `json.JSONDecodeError`: Если данные JSON не могут быть разобраны.

**Как работает функция**:

1.  Обрабатывает различные типы входных данных:
    -   `SimpleNamespace`: Преобразует в словарь.
    -   `Path`: Если это файл, читает содержимое как JSON и преобразует в словарь. Если это директория, рекурсивно обрабатывает все JSON-файлы в директории.
    -   `str`: Преобразует JSON-строку в словарь, используя `_string_to_dict`.
    -   `list`: Рекурсивно декодирует строки в списке.
    -   `dict`: Рекурсивно декодирует строки в словаре.
2.  Обрабатывает исключения, возникающие при работе с файлами и разборе JSON, и возвращает пустой словарь в случае ошибки.

### `j_loads_ns`

**Назначение**: Загружает данные JSON/CSV и преобразует их в `SimpleNamespace`.

```python
def j_loads_ns(
    jjson: Union[Path, SimpleNamespace, Dict, str], ordered: bool = True
) -> Union[SimpleNamespace, List[SimpleNamespace], Dict]:
    """Load JSON/CSV data and convert to SimpleNamespace."""
    ...
```

**Параметры**:

-   `jjson` (Union[Path, SimpleNamespace, Dict, str]): Путь к файлу, объекту `SimpleNamespace`, словарю или JSON-строке.
-   `ordered` (bool): Использовать ли `OrderedDict` для сохранения порядка элементов. По умолчанию `True`.

**Возвращает**:

-   `Union[SimpleNamespace, List[SimpleNamespace], Dict]`: Обработанные данные в виде объекта `SimpleNamespace` или списка объектов `SimpleNamespace`.

**Как работает функция**:

1.  Загружает данные, используя функцию `j_loads`.
2.  Если загрузка прошла успешно, преобразует данные в объект `SimpleNamespace` или список объектов `SimpleNamespace`.
3.  Возвращает `SimpleNamespace` или список `SimpleNamespace`
4.  Использует функцию `dict2ns` для преобразования словаря в `SimpleNamespace`.

## Переменные модуля

-   `Config`: Внутренний класс, определяющий константы для режимов записи.
    -   `MODE_WRITE` (str): Режим записи файла (w).
    -   `MODE_APPEND_START` (str): Режим добавления в начало файла (a+).
    -   `MODE_APPEND_END` (str): Режим добавления в конец файла (+a).

## Пример использования

### Чтение JSON из файла

```python
from src.utils.jjson import j_loads

data = j_loads('config.json')
if data:
    print(data['key'])
```

### Преобразование JSON в SimpleNamespace

```python
from src.utils.jjson import j_loads_ns

config = j_loads_ns('config.json')
if config:
    print(config.key)
```

## Взаимосвязь с другими частями проекта

-   Этот модуль зависит от модуля `src.logger.logger` для логирования ошибок и от модуля `src.utils.convertors.dict` для преобразования в `SimpleNamespace`.
-   Модуль используется другими частями проекта для загрузки и сохранения конфигурационных файлов и других данных в формате JSON.