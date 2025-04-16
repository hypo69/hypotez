### Анализ кода модуля `hypotez/src/utils/jjson.py`

## Обзор

Этот модуль предоставляет утилиты для работы с данными в формате JSON, включая функции для загрузки JSON из различных источников, сохранения данных в JSON-файл и преобразования данных в объекты `SimpleNamespace`.

## Подробнее

Модуль предоставляет набор функций для упрощения работы с JSON-данными, такими как чтение JSON из файлов, директорий, строк или объектов, а также преобразование этих данных в различные структуры, включая словари и объекты `SimpleNamespace`. Также модуль предоставляет функции для сохранения данных в JSON-файлы с возможностью добавления.

## Классы

### `Config`

```python
class Config:
    MODE_WRITE:str = "w"
    MODE_APPEND_START:str = "a+"
    MODE_APPEND_END:str = "+a"
```

**Описание**:
Класс `Config` содержит константы, определяющие режимы записи в файл.

**Атрибуты**:
- `MODE_WRITE` (str): Режим записи (перезапись) - `"w"`.
- `MODE_APPEND_START` (str): Режим добавления в начало файла - `"a+"`.
- `MODE_APPEND_END` (str): Режим добавления в конец файла - `"+a"`.

**Методы**:
- Нет

## Функции

### `_convert_to_dict`

```python
def _convert_to_dict(value: Any) -> Any:
    """Convert SimpleNamespace and lists to dict."""
    ...
```

**Назначение**:
Преобразует объекты `SimpleNamespace` и списки в словари.

**Параметры**:
- `value` (Any): Значение для преобразования.

**Возвращает**:
- Any: Преобразованное значение.

**Как работает функция**:
1. Проверяет тип входного значения.
2. Если значение является `SimpleNamespace`, преобразует его в словарь, рекурсивно применяя `_convert_to_dict` к каждому значению атрибута.
3. Если значение является словарем, рекурсивно применяет `_convert_to_dict` к каждому значению в словаре.
4. Если значение является списком, рекурсивно применяет `_convert_to_dict` к каждому элементу списка.
5. Если значение не является ни одним из вышеперечисленных типов, возвращает его без изменений.

### `_read_existing_data`

```python
def _read_existing_data(path: Path, exc_info: bool = True) -> dict:
    """Read existing JSON data from a file."""
    ...
```

**Назначение**:
Читает существующие данные JSON из файла.

**Параметры**:
- `path` (Path): Путь к файлу.
- `exc_info` (bool, optional): Если `True`, логирует информацию об исключении. По умолчанию `True`.

**Возвращает**:
- `dict`: Словарь, содержащий данные JSON, или пустой словарь, если не удалось прочитать файл.

**Как работает функция**:
1. Пытается прочитать содержимое файла как JSON.
2. В случае ошибки декодирования JSON, логирует ошибку и возвращает пустой словарь.
3. В случае любой другой ошибки при чтении файла, логирует ошибку и возвращает пустой словарь.

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
- `data` (Dict): Новые данные для объединения.
- `existing_data` (Dict): Существующие данные.
- `mode` (str): Режим объединения (Config.MODE_APPEND_START, Config.MODE_APPEND_END).

**Возвращает**:
- `Dict`: Объединенные данные.

**Как работает функция**:
1.  В зависимости от режима `mode`:
    -   `Config.MODE_APPEND_START`: Добавляет новые данные в начало существующих (если это списки) или обновляет существующие данные новыми (если это словари).
    -   `Config.MODE_APPEND_END`: Добавляет новые данные в конец существующих (если это списки) или обновляет новые данные существующими (если это словари).
    -   Если режим не поддерживается, возвращает новые данные.
2. В случае возникновения ошибок логирует информацию об ошибке.

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
- `data` (Union[Dict, SimpleNamespace, List[Dict], List[SimpleNamespace]]): Данные, совместимые с JSON, или объекты SimpleNamespace для сохранения.
- `file_path` (Optional[Path], optional): Путь к выходному файлу. Если None, возвращает JSON в виде словаря. По умолчанию None.
- `ensure_ascii` (bool, optional): Если True, экранирует не-ASCII символы в выводе. По умолчанию False.
- `mode` (str, optional): Режим открытия файла ('w', 'a+', '+a'). По умолчанию 'w'.
- `exc_info` (bool, optional): Если True, логирует исключения с трассировкой. По умолчанию True.

**Возвращает**:
- `Optional[Dict]`: JSON-данные в виде словаря в случае успеха, или None в случае ошибки.

**Вызывает исключения**:
- `ValueError`: Если режим файла не поддерживается.

**Как работает функция**:
1.  Определяет путь к файлу на основе `file_path`.
2.  Преобразует входные данные в словарь с помощью `_convert_to_dict`.
3.  Если `mode` - один из режимов добавления, читает существующие данные из файла и объединяет их с новыми данными.
4.  Сохраняет данные в файл в формате JSON.
5.  Возвращает данные в виде словаря.

### `_decode_strings`

```python
def _decode_strings(data: Any) -> Any:
    """Recursively decode strings in a data structure."""
    ...
```

**Назначение**:
Рекурсивно декодирует строки в структуре данных.

**Параметры**:
- `data` (Any): Структура данных для декодирования.

**Возвращает**:
- Any: Структура данных с декодированными строками.

**Как работает функция**:
1. Проверяет тип входного значения.
2. Если значение является строкой, пытается декодировать ее с использованием `codecs.decode(data, 'unicode_escape')`.
3. Если значение является списком, рекурсивно применяет `_decode_strings` к каждому элементу списка.
4. Если значение является словарем, рекурсивно применяет `_decode_strings` к каждому ключу и значению в словаре.
5. Если значение не является ни одним из вышеперечисленных типов, возвращает его без изменений.

### `_string_to_dict`

```python
def _string_to_dict(json_string: str) -> dict:
    """Remove markdown quotes and parse JSON string."""
    ...
```

**Назначение**:
Удаляет Markdown-кавычки и преобразует JSON-строку в словарь.

**Параметры**:
- `json_string` (str): JSON-строка для преобразования.

**Возвращает**:
- `dict`: Словарь, полученный из JSON-строки.

**Как работает функция**:
1. Проверяет, начинается и заканчивается ли строка с Markdown-кавычек ("\`\`\`" или "\`\`\`json").
2. Если да, удаляет кавычки и "json" (если есть) из строки.
3. Пытается преобразовать строку в словарь с помощью `json.loads`.
4. В случае ошибки преобразования логирует ошибку и возвращает пустой словарь.

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
- `jjson` (Union[dict, SimpleNamespace, str, Path, list]): Путь к файлу/директории, JSON-строка или JSON-объект.
- `ordered` (bool, optional): Использовать ли OrderedDict для сохранения порядка элементов. По умолчанию True.

**Возвращает**:
- `dict | list`: Обработанные данные (словарь или список словарей).

**Вызывает исключения**:
- `FileNotFoundError`: Если указанный файл не найден.
- `json.JSONDecodeError`: Если не удалось разобрать JSON-данные.

**Как работает функция**:
1. Обрабатывает входные данные в зависимости от их типа:
    - Если это `SimpleNamespace`, преобразует его в словарь.
    - Если это `Path`:
        - Если это директория, рекурсивно загружает все JSON-файлы в директории.
        - Если это файл, загружает JSON из файла.
    - Если это строка, преобразует строку в словарь с помощью `_string_to_dict`.
    - Если это список, декодирует строки в списке с помощью `_decode_strings`.
    - Если это словарь, декодирует строки в словаре с помощью `_decode_strings`.
2. Возвращает обработанные данные.

### `j_loads_ns`

```python
def j_loads_ns(
    jjson: Union[Path, SimpleNamespace, Dict, str], ordered: bool = True
) -> Union[SimpleNamespace, List[SimpleNamespace], Dict]:
    """Load JSON/CSV data and convert to SimpleNamespace."""
    ...
```

**Назначение**:
Загружает данные JSON/CSV и преобразует их в SimpleNamespace.

**Параметры**:
- `jjson` (Union[Path, SimpleNamespace, Dict, str]): Путь к файлу/директории, JSON-строка или JSON-объект.
- `ordered` (bool, optional): Использовать ли OrderedDict для сохранения порядка элементов. По умолчанию True.

**Возвращает**:
- `Union[SimpleNamespace, List[SimpleNamespace], Dict]`: Обработанные данные в виде SimpleNamespace или списка SimpleNamespace.

**Как работает функция**:
1. Загружает данные с помощью `j_loads`.
2. Если загрузка успешна, преобразует данные в `SimpleNamespace` (или список `SimpleNamespace`, если загружен список).

## Переменные

### `Config`

```python
class Config:
    MODE_WRITE:str = "w"
    MODE_APPEND_START:str = "a+"
    MODE_APPEND_END:str = "+a"
```

Содержит режимы записи JSON-файла.

## Запуск

Для использования этого модуля необходимо:

1.  Установить необходимые библиотеки:

```bash
pip install json_repair
```

2.  Импортировать нужные функции из модуля `src.utils.jjson`.

```python
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from pathlib import Path
from types import SimpleNamespace

# Загрузка из файла
data = j_loads(Path("config.json"))

# Загрузка и преобразование в SimpleNamespace
ns = j_loads_ns("config.json")

# Сохранение в файл
data = {"key": "value"}
j_dumps(data, Path("output.json"))