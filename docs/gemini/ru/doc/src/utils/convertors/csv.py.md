# Модуль для преобразования CSV и JSON данных
=================================================

Модуль содержит функции для конвертации данных между форматами CSV и JSON. Он предоставляет функциональность для чтения данных из CSV файлов и преобразования их в словари или объекты SimpleNamespace, а также для сохранения данных в формате JSON.

## Обзор

Этот модуль предоставляет инструменты для работы с CSV и JSON файлами, позволяя преобразовывать данные между этими форматами. Он включает функции для чтения CSV файлов, преобразования их в словари или объекты `SimpleNamespace`, и сохранения данных в формате JSON.

## Подробней

Модуль предназначен для облегчения обмена данными между различными системами и приложениями, использующими CSV и JSON форматы. Он предоставляет удобные функции для чтения, преобразования и записи данных, что упрощает интеграцию и обработку данных. Расположение файла в структуре проекта `/src/utils/convertors/csv.py` указывает на то, что он является частью утилитного набора инструментов, предназначенных для преобразования данных.

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
- `csv_file` (str | Path): Путь к CSV файлу для чтения.

**Возвращает**:
- `dict | None`: Словарь, содержащий данные из CSV файла, преобразованные в формат JSON, или `None`, если преобразование не удалось.

**Вызывает исключения**:
- `Exception`: Возникает, если не удается прочитать CSV файл.

**Как работает функция**:
Функция `csv2dict` принимает путь к CSV файлу и использует функцию `read_csv_as_dict` для преобразования данных в словарь. Возвращает полученный словарь или `None` в случае ошибки.

**Примеры**:

```python
from pathlib import Path
csv_file_path = Path('data.csv')
data = csv2dict(csv_file_path)
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
- `csv_file` (str | Path): Путь к CSV файлу для чтения.

**Возвращает**:
- `SimpleNamespace | None`: Объект `SimpleNamespace`, содержащий данные из CSV файла, или `None`, если преобразование не удалось.

**Вызывает исключения**:
- `Exception`: Возникает, если не удается прочитать CSV файл.

**Как работает функция**:
Функция `csv2ns` принимает путь к CSV файлу и использует функцию `read_csv_as_ns` для преобразования данных в объекты `SimpleNamespace`. Возвращает полученный объект или `None` в случае ошибки.

**Примеры**:

```python
from pathlib import Path
csv_file_path = Path('data.csv')
data = csv2ns(csv_file_path)
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
- `csv_file_path` (str | Path): Путь к CSV файлу для чтения.
- `json_file_path` (str | Path): Путь к JSON файлу для сохранения.
- `exc_info` (bool, optional): Если `True`, включает информацию трассировки в лог. По умолчанию `True`.

**Возвращает**:
- `List[Dict[str, str]] | None`: JSON данные в виде списка словарей или `None`, если преобразование не удалось.

**Вызывает исключения**:
- Отсутствуют явные исключения, но функция логирует ошибки с использованием `logger.error`.

**Как работает функция**:
1. Функция `csv_to_json` принимает пути к CSV и JSON файлам.
2. Считывает данные из CSV файла с помощью функции `read_csv_file`.
3. Если данные успешно прочитаны, открывает JSON файл для записи и сохраняет данные в формате JSON с отступом 4.
4. В случае ошибки логирует сообщение об ошибке с использованием `logger.error` и возвращает `None`.

**Примеры**:

```python
from pathlib import Path
csv_file_path = Path('data.csv')
json_file_path = Path('data.json')
json_data = csv_to_json(csv_file_path, json_file_path)
if json_data:
    print(json_data)
```
```python
from pathlib import Path
from src.logger.logger import logger  # Убедитесь, что импортирован logger

def csv_to_json(
    csv_file_path: str | Path,
    json_file_path: str | Path,
    exc_info: bool = True
) -> List[Dict[str, str]] | None:
    """
    Преобразует CSV файл в JSON формат и сохраняет его в JSON файл.

    Args:
        csv_file_path (str | Path): Путь к CSV файлу для чтения.
        json_file_path (str | Path): Путь к JSON файлу для сохранения.
        exc_info (bool, optional): Если True, включает информацию трассировки в лог. По умолчанию True.

    Returns:
        List[Dict[str, str]] | None: JSON данные в виде списка словарей или None, если преобразование не удалось.
    """
    try:
        data = read_csv_file(csv_file_path, exc_info=exc_info)  # Чтение данных из CSV файла
        if data is not None:
            try:
                with open(json_file_path, 'w', encoding='utf-8') as jsonfile:  # Открытие JSON файла для записи
                    json.dump(data, jsonfile, indent=4)  # Запись данных в JSON файл с отступами
                logger.info(f"Данные успешно записаны в файл: {json_file_path}")  # Логирование успешной записи
                return data
            except IOError as ex:  # Обработка ошибок ввода-вывода при записи в файл
                logger.error(f"Ошибка при записи в файл {json_file_path}: {ex}", exc_info=exc_info)
                return None
        else:
            logger.warning(f"Не удалось прочитать данные из CSV файла: {csv_file_path}")
            return None
    except Exception as ex:  # Обработка общих исключений при чтении и преобразовании CSV
        logger.error(f"Не удалось преобразовать CSV в JSON: {ex}", exc_info=exc_info)
        return None