# Модуль `src.utils.convertors.csv`

## Обзор

Модуль предоставляет утилиты для конвертации данных между форматами CSV и JSON. Он включает функции для преобразования CSV в словарь (`csv2dict`), в объекты SimpleNamespace (`csv2ns`) и в JSON (`csv_to_json`). Модуль использует другие утилиты для чтения и сохранения CSV файлов, а также логирует ошибки с помощью модуля `src.logger.logger`.

## Подробней

Модуль предназначен для упрощения работы с данными, хранящимися в формате CSV, путем их преобразования в более удобные структуры данных, такие как словари, объекты SimpleNamespace или JSON. Это позволяет легко манипулировать данными и использовать их в различных приложениях и сервисах.

## Функции

### `csv2dict`

**Назначение**: Преобразует данные из CSV файла в словарь.

```python
def csv2dict(csv_file: str | Path, *args, **kwargs) -> dict | None:
    """
    Convert CSV data to a dictionary.

    Args:
        csv_file (str | Path): Path to the CSV file to read.

    Returns:
        dict | None: Dictionary containing the data from CSV converted to JSON format, or `None` if conversion failed.

    Raises:
        Exception: If unable to read CSV.
    """
    ...
```

**Параметры**:

-   `csv_file` (str | Path): Путь к CSV файлу, который требуется прочитать.
-   `*args`: Произвольные позиционные аргументы, передаваемые в функцию `read_csv_as_dict`.
-   `**kwargs`: Произвольные именованные аргументы, передаваемые в функцию `read_csv_as_dict`.

**Возвращает**:

-   `dict | None`: Словарь, содержащий данные из CSV файла, преобразованные в формат JSON. Возвращает `None`, если преобразование не удалось.

**Вызывает исключения**:

-   `Exception`: Если не удается прочитать CSV файл.

**Как работает функция**:

Функция `csv2dict` принимает путь к CSV файлу и использует функцию `read_csv_as_dict` для чтения данных из файла и преобразования их в словарь.  Если чтение и преобразование прошли успешно, функция возвращает полученный словарь. В случае ошибки возвращается `None`.

**Примеры**:

```python
from pathlib import Path

# Пример использования функции
csv_file = Path("data.csv")
data = csv2dict(csv_file)
if data:
    print(data)
```

### `csv2ns`

**Назначение**: Преобразует данные из CSV файла в объекты `SimpleNamespace`.

```python
def csv2ns(csv_file: str | Path, *args, **kwargs) -> SimpleNamespace | None:
    """
    Convert CSV data to SimpleNamespace objects.

    Args:
        csv_file (str | Path): Path to the CSV file to read.

    Returns:
        SimpleNamespace | None: SimpleNamespace object containing the data from CSV, or `None` if conversion failed.

    Raises:
        Exception: If unable to read CSV.
    """
    ...
```

**Параметры**:

-   `csv_file` (str | Path): Путь к CSV файлу, который требуется прочитать.
-   `*args`: Произвольные позиционные аргументы, передаваемые в функцию `read_csv_as_ns`.
-   `**kwargs`: Произвольные именованные аргументы, передаваемые в функцию `read_csv_as_ns`.

**Возвращает**:

-   `SimpleNamespace | None`: Объект `SimpleNamespace`, содержащий данные из CSV файла. Возвращает `None`, если преобразование не удалось.

**Вызывает исключения**:

-   `Exception`: Если не удается прочитать CSV файл.

**Как работает функция**:

Функция `csv2ns` принимает путь к CSV файлу и использует функцию `read_csv_as_ns` для чтения данных из файла и преобразования их в объекты `SimpleNamespace`. Если чтение и преобразование прошли успешно, функция возвращает полученный объект `SimpleNamespace`. В случае ошибки возвращается `None`.

**Примеры**:

```python
from pathlib import Path

# Пример использования функции
csv_file = Path("data.csv")
data = csv2ns(csv_file)
if data:
    print(data)
```

### `csv_to_json`

**Назначение**: Преобразует CSV файл в JSON формат и сохраняет его в JSON файл.

```python
def csv_to_json(
    csv_file_path: str | Path,
    json_file_path: str | Path,
    exc_info: bool = True
) -> List[Dict[str, str]] | None:
    """ Convert a CSV file to JSON format and save it to a JSON file.

    Args:
        csv_file_path (str | Path): The path to the CSV file to read.
        json_file_path (str | Path): The path to the JSON file to save.
        exc_info (bool, optional): If True, includes traceback information in the log. Defaults to True.

    Returns:
        List[Dict[str, str]] | None: The JSON data as a list of dictionaries, or None if conversion failed.

    Example:
        >>> json_data = csv_to_json('dialogue_log.csv', 'dialogue_log.json')
        >>> print(json_data)
        [{'role': 'user', 'content': 'Hello'}, {'role': 'assistant', 'content': 'Hi there!'}]
    """
    ...
```

**Параметры**:

-   `csv_file_path` (str | Path): Путь к CSV файлу, который требуется прочитать.
-   `json_file_path` (str | Path): Путь к JSON файлу, в который требуется сохранить преобразованные данные.
-   `exc_info` (bool, optional): Если установлено в `True`, включает информацию об отслеживании в журнал. По умолчанию `True`.

**Возвращает**:

-   `List[Dict[str, str]] | None`: JSON данные в виде списка словарей. Возвращает `None`, если преобразование не удалось.

**Как работает функция**:

1.  Функция `csv_to_json` принимает пути к CSV и JSON файлам.
2.  Вызывает функцию `read_csv_file` для чтения данных из CSV файла. Параметр `exc_info` определяет, включать ли отладочную информацию в логи в случае возникновения ошибки.
3.  Если данные успешно прочитаны из CSV файла, функция открывает JSON файл для записи с кодировкой UTF-8.
4.  Записывает данные в JSON файл с отступом 4 для удобочитаемости.
5.  Возвращает преобразованные JSON данные.
6.  В случае возникновения ошибки при чтении CSV или записи JSON, функция логирует ошибку с помощью `logger.error` и возвращает `None`.

**Примеры**:

```python
from pathlib import Path

# Пример использования функции
csv_file = Path("data.csv")
json_file = Path("data.json")
json_data = csv_to_json(csv_file, json_file)
if json_data:
    print(json_data)