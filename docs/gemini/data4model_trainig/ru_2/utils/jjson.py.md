### Анализ кода `hypotez/src/utils/jjson.py.md`

## Обзор

Модуль предоставляет утилиты для работы с данными в формате JSON, включая функции для загрузки, сохранения и преобразования данных.

## Подробнее

Этот модуль содержит набор функций, упрощающих чтение и запись JSON-файлов, а также преобразование данных между различными форматами (например, из `SimpleNamespace` в `dict` и обратно). Модуль также включает функции для исправления JSON-строк и декодирования строк.

## Классы

### `Config`

```python
class Config:
    MODE_WRITE:str = "w"
    MODE_APPEND_START:str = "a+"
    MODE_APPEND_END:str = "+a"
```

**Описание**:
Класс, содержащий константы для определения режима записи файла.

**Атрибуты**:

*   `MODE_WRITE` (str): Режим записи файла (перезапись).
*   `MODE_APPEND_START` (str): Режим добавления в начало файла.
*   `MODE_APPEND_END` (str): Режим добавления в конец файла.

## Функции

### `_convert_to_dict`

```python
def _convert_to_dict(value: Any) -> Any:
    """Convert SimpleNamespace and lists to dict."""
    ...
```

**Назначение**:
Рекурсивно преобразует объекты `SimpleNamespace` и списки в словари.

**Параметры**:

*   `value` (Any): Значение для преобразования.

**Возвращает**:

*   `Any`: Преобразованное значение (словарь, список или исходное значение, если оно не требует преобразования).

**Как работает функция**:

1.  Проверяет, является ли входное значение экземпляром `SimpleNamespace`. Если да, преобразует его в словарь, рекурсивно применяя `_convert_to_dict` к каждому значению.
2.  Проверяет, является ли входное значение словарем. Если да, рекурсивно применяет `_convert_to_dict` к каждому значению в словаре.
3.  Проверяет, является ли входное значение списком. Если да, рекурсивно применяет `_convert_to_dict` к каждому элементу списка.
4.  Если входное значение не является ни `SimpleNamespace`, ни словарем, ни списком, возвращает его без изменений.

### `_read_existing_data`

```python
def _read_existing_data(path: Path, exc_info: bool = True) -> dict:
    """Read existing JSON data from a file."""
    ...
```

**Назначение**:
Читает существующие данные JSON из файла.

**Параметры**:

*   `path` (Path): Путь к файлу.
*   `exc_info` (bool, optional): Включать ли информацию об исключении в логи. Defaults to `True`.

**Возвращает**:

*   `dict`: Словарь, содержащий данные JSON, или пустой словарь, если произошла ошибка.

**Как работает функция**:

1.  Пытается прочитать содержимое файла как текст в кодировке UTF-8.
2.  Пытается преобразовать прочитанный текст в JSON-объект.
3.  В случае успеха возвращает полученный словарь.
4.  В случае ошибки `json.JSONDecodeError` логирует ошибку и возвращает пустой словарь.
5.  В случае любой другой ошибки логирует ошибку и возвращает пустой словарь.

### `_merge_data`

```python
def _merge_data(
    data: Dict, existing_data: Dict, mode: str
) -> Dict:
    """Merge new data with existing data based on mode."""
    ...
```

**Назначение**:
Объединяет новые данные с существующими данными в зависимости от режима.

**Параметры**:

*   `data` (Dict): Новые данные для добавления.
*   `existing_data` (Dict): Существующие данные.
*   `mode` (str): Режим добавления (должен быть одним из `Config.MODE_WRITE`, `Config.MODE_APPEND_START`, `Config.MODE_APPEND_END`).

**Возвращает**:

*   `Dict`: Объединенные данные (словарь).

**Как работает функция**:

1.  В зависимости от значения параметра `mode`:

    *   Если `mode` равен `Config.MODE_APPEND_START`:

        *    Если `data` и `existing_data` - списки, то к `data` добавляется `existing_data`.
        *   Если `data` и `existing_data` - словари, то `data` обновляет `existing_data`.
        *   Возвращает `existing_data`.
    *   Если `mode` равен `Config.MODE_APPEND_END`:

        *   Если `data` и `existing_data` - списки, то к `existing_data` добавляется `data`.
        *   Если `data` и `existing_data` - словари, то `existing_data` обновляет `data`.
        *   Возвращает `data`.
    *   В противном случае возвращает `data`.
2.  В случае ошибки логирует её.

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

**Назначение**:
Сохраняет JSON-данные в файл или возвращает JSON-данные в виде словаря.

**Параметры**:

*   `data` (Union[Dict, SimpleNamespace, List[Dict], List[SimpleNamespace]]): Данные, совместимые с JSON, или объекты `SimpleNamespace` для сохранения.
*   `file_path` (Optional[Path], optional): Путь к выходному файлу. Если `None`, возвращает JSON в виде словаря. Defaults to `None`.
*   `ensure_ascii` (bool, optional): Если `True`, экранирует символы, не входящие в ASCII, в выводе. Defaults to `False`.
*   `mode` (str, optional): Режим открытия файла ('w', 'a+', '+a'). Defaults to `Config.MODE_WRITE`.
*   `exc_info` (bool, optional): Если `True`, логирует исключения с трассировкой. Defaults to `True`.

**Возвращает**:

*   `Optional[Dict]`: Данные JSON в виде словаря в случае успеха или `None` в случае ошибки.

**Вызывает исключения**:

*   `ValueError`: Если указан неподдерживаемый режим файла.

**Как работает функция**:

1.  Преобразует входные данные в словарь с помощью функции `_convert_to_dict`.
2.  Проверяет режим записи.
3.  Если указан путь к файлу:

    *   Создает родительские директории для файла, если они не существуют.
    *   Открывает файл для записи и записывает данные в формате JSON с отступами.
    *   Логирует исключения, если возникают ошибки при записи в файл.
    *   Возвращает данные в виде словаря.
4.  Если путь к файлу не указан, возвращает данные в виде словаря.

### `_decode_strings`

```python
def _decode_strings(data: Any) -> Any:
    """Recursively decode strings in a data structure."""
    ...
```

**Назначение**:
Рекурсивно декодирует строки в структуре данных.

**Параметры**:

*   `data` (Any): Структура данных для декодирования.

**Возвращает**:

*   `Any`: Декодированная структура данных.

**Как работает функция**:

1.  Проверяет, является ли входное значение строкой. Если да, пытается декодировать её с использованием `codecs.decode(data, 'unicode_escape')`.
2.  Если значение является списком, рекурсивно применяет функцию к каждому элементу списка.
3.  Если значение является словарем, рекурсивно применяет функцию к каждому ключу и значению в словаре.
4.  В противном случае возвращает входное значение без изменений.

### `_string_to_dict`

```python
def _string_to_dict(json_string: str) -> dict:
    """Remove markdown quotes and parse JSON string."""
    ...
```

**Назначение**:
Удаляет Markdown-кавычки и преобразует JSON-строку в словарь.

**Параметры**:

*   `json_string` (str): JSON-строка.

**Возвращает**:

*   `dict`: Словарь, полученный из JSON-строки.

**Как работает функция**:

1.  Удаляет обрамляющие Markdown-кавычки (```` и ```json) из входной строки.
2.  Пытается преобразовать строку в словарь с помощью `json.loads`.
3.  В случае ошибки преобразования логирует ошибку и возвращает пустой словарь.

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

**Назначение**:
Загружает данные JSON или CSV из файла, директории, строки или объекта.

**Параметры**:

*   `jjson` (Union[dict, SimpleNamespace, str, Path, list]): Путь к файлу/директории, JSON-строка или JSON-объект.
*   `ordered` (bool, optional): Использовать ли `OrderedDict` для сохранения порядка элементов. Defaults to `True`.

**Возвращает**:

*   `dict | list`: Обработанные данные (словарь или список словарей).

**Вызывает исключения**:

*   `FileNotFoundError`: Если указанный файл не найден.
*   `json.JSONDecodeError`: Если не удается распарсить JSON-данные.

**Как работает функция**:

1.  Преобразует входные данные в словарь или список словарей, в зависимости от типа входных данных.
2.  Если входные данные являются объектом `SimpleNamespace`, преобразует его в словарь.
3.  Если входные данные являются объектом `Path`:

    *   Если `Path` указывает на директорию, рекурсивно загружает JSON-файлы из этой директории.
    *   Если `Path` указывает на файл, считывает его содержимое и преобразует его в JSON.
4.  Если входные данные являются строкой, преобразует строку в словарь с помощью `_string_to_dict`.
5.  Рекурсивно декодирует строки в данных с помощью функции `_decode_strings`.
6.  Обрабатывает исключения, логируя ошибки и возвращая пустой словарь в случае неудачи.

### `j_loads_ns`

```python
def j_loads_ns(
    jjson: Union[Path, SimpleNamespace, Dict, str], ordered: bool = True
) -> Union[SimpleNamespace, List[SimpleNamespace], Dict]:
    """Load JSON/CSV data and convert to SimpleNamespace."""
    data = j_loads(jjson, ordered=ordered)
    if data:
        if isinstance(data, list):
            return [dict2ns(item) for item in data]
        return dict2ns(data)
    return {}
```

**Назначение**:
Загружает данные JSON/CSV и преобразует их в `SimpleNamespace`.

**Параметры**:

*   `jjson` (Union[Path, SimpleNamespace, Dict, str]): Путь к файлу/директории, JSON-строка или JSON-объект.
*   `ordered` (bool, optional): Использовать ли `OrderedDict` для сохранения порядка элементов. Defaults to `True`.

**Возвращает**:

*   `Union[SimpleNamespace, List[SimpleNamespace], Dict]`: Обработанные данные в виде `SimpleNamespace`, списка `SimpleNamespace` или словаря.

**Как работает функция**:

1.  Загружает данные с помощью функции `j_loads`.
2.  Если загрузка прошла успешно, преобразует полученные данные в объекты `SimpleNamespace` с помощью функции `dict2ns`.
3.  Возвращает преобразованные данные.
4.  В случае ошибки возвращает пустой словарь.

## Константы

*   `Config.MODE_WRITE` (str): Режим записи файла (перезапись).
*   `Config.MODE_APPEND_START` (str): Режим добавления в начало файла.
*   `Config.MODE_APPEND_END` (str): Режим добавления в конец файла.

## Примеры использования

```python
from src.utils.jjson import j_loads, j_dumps, j_loads_ns
from pathlib import Path

# Пример загрузки JSON из файла
data = j_loads(Path('config.json'))

# Пример сохранения JSON в файл
data_to_save = {'key': 'value'}
j_dumps(data_to_save, Path('output.json'))

# Пример загрузки JSON из строки и преобразования в SimpleNamespace
data_ns = j_loads_ns('{"key": "value"}')
```

## Зависимости

*   `json`: Стандартный модуль Python для работы с JSON-данными.
*   `os`: Стандартный модуль Python для работы с операционной системой.
*   `re`: Для работы с регулярными выражениями.
*   `codecs`: Модуль для кодирования и декодирования данных.
*   `datetime`: Для работы с датой и временем.
*   `pathlib.Path`: Для работы с путями к файлам.
*   `typing.Any, typing.Dict, typing.List, typing.Optional, typing.Union`: Для аннотаций типов.
*   `types.SimpleNamespace`: Для создания объектов с атрибутами на основе словаря.
*    `src.logger.logger`: Для логирования.
*   `json_repair`: Для исправления JSON-строк
*   `collections.OrderedDict`: Для сохранения порядка в словаре
*   `hypotez.src.utils.convertors.dict.dict2ns`: Для преобразования словарей в SimpleNamespace.

## Взаимосвязи с другими частями проекта

Модуль `jjson.py` предоставляет основные утилиты для работы с JSON-данными и используется во многих частях проекта `hypotez`, где необходимо чтение, запись или преобразование JSON-файлов и структур данных.