# Модуль `src.utils.convertors.csv`

## Обзор

Модуль предоставляет утилиты для конвертации данных между форматами CSV и JSON. Он включает функции для преобразования CSV в словарь или объект SimpleNamespace, а также для конвертации CSV в JSON с сохранением в файл.

## Подробней

Модуль содержит функции для работы с данными в формате CSV и JSON. Он предоставляет функциональность для преобразования CSV-файлов в различные структуры данных Python, такие как словари и объекты SimpleNamespace, а также для конвертации CSV в JSON с сохранением результата в файл. Модуль использует стандартные библиотеки `json` и `csv`, а также модуль `logger` из проекта `hypotez` для логирования ошибок.

## Функции

### `csv2dict`

**Назначение**: Преобразует данные из CSV-файла в словарь.

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
- `csv_file` (str | Path): Путь к CSV-файлу, который необходимо прочитать.
- `*args`: Произвольные позиционные аргументы, передаваемые в функцию `read_csv_as_dict`.
- `**kwargs`: Произвольные именованные аргументы, передаваемые в функцию `read_csv_as_dict`.

**Возвращает**:
- `dict | None`: Словарь, содержащий данные из CSV-файла, преобразованные в формат JSON. Возвращает `None`, если преобразование не удалось.

**Вызывает исключения**:
- `Exception`: Возникает, если не удается прочитать CSV-файл.

**Как работает функция**:
Функция вызывает функцию `read_csv_as_dict` для чтения данных из указанного CSV-файла и преобразования их в словарь. Возвращает полученный словарь или `None` в случае ошибки.

**Примеры**:

```python
from pathlib import Path
# Пример использования функции
csv_file_path = Path('data.csv')
data = csv2dict(csv_file_path)
if data:
    print(data)
```

### `csv2ns`

**Назначение**: Преобразует данные из CSV-файла в объекты SimpleNamespace.

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
- `csv_file` (str | Path): Путь к CSV-файлу, который необходимо прочитать.
- `*args`: Произвольные позиционные аргументы, передаваемые в функцию `read_csv_as_ns`.
- `**kwargs`: Произвольные именованные аргументы, передаваемые в функцию `read_csv_as_ns`.

**Возвращает**:
- `SimpleNamespace | None`: Объект SimpleNamespace, содержащий данные из CSV-файла. Возвращает `None`, если преобразование не удалось.

**Вызывает исключения**:
- `Exception`: Возникает, если не удается прочитать CSV-файл.

**Как работает функция**:
Функция вызывает функцию `read_csv_as_ns` для чтения данных из указанного CSV-файла и преобразования их в объекты SimpleNamespace. Возвращает полученный объект или `None` в случае ошибки.

**Примеры**:

```python
from pathlib import Path
# Пример использования функции
csv_file_path = Path('data.csv')
data = csv2ns(csv_file_path)
if data:
    print(data)
```

### `csv_to_json`

**Назначение**: Преобразует CSV-файл в JSON-формат и сохраняет его в JSON-файл.

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
- `csv_file_path` (str | Path): Путь к CSV-файлу, который необходимо прочитать.
- `json_file_path` (str | Path): Путь к JSON-файлу, в который нужно сохранить преобразованные данные.
- `exc_info` (bool, optional): Если `True`, включает информацию об отслеживании в лог. По умолчанию `True`.

**Возвращает**:
- `List[Dict[str, str]] | None`: JSON-данные в виде списка словарей. Возвращает `None`, если преобразование не удалось.

**Как работает функция**:
1. Функция вызывает `read_csv_file` для чтения данных из CSV-файла.
2. Если данные успешно прочитаны, функция открывает JSON-файл для записи.
3. Преобразует данные в JSON-формат с отступом 4 для читаемости и сохраняет их в файл.
4. Возвращает преобразованные JSON-данные.
5. В случае возникновения ошибки, функция логирует ошибку с использованием `logger.error` и возвращает `None`.

**Примеры**:

```python
from pathlib import Path
# Пример использования функции
csv_file_path = Path('data.csv')
json_file_path = Path('data.json')
json_data = csv_to_json(csv_file_path, json_file_path)
if json_data:
    print(json_data)
```