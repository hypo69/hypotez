# Модуль для преобразования CSV данных (csv.py)

## Обзор

Этот модуль предоставляет утилиты для преобразования CSV данных в различные форматы: словари и объекты SimpleNamespace.

## Подробней

Модуль `src.utils.convertors.csv` предназначен для упрощения работы с CSV данными. Он предоставляет функции, которые позволяют преобразовывать CSV файлы в различные структуры данных, что облегчает их дальнейшую обработку и анализ. Модуль использует функции из `src.utils.csv` (такие как `read_csv_as_dict`, `read_csv_as_ns`, `save_csv_file`, `read_csv_file`) для выполнения основных операций.

## Функции

### `csv2dict`

**Назначение**: Преобразует CSV данные в словарь.

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

-   `csv_file` (str | Path): Путь к CSV файлу для чтения.
-   `*args`: Произвольные позиционные аргументы, передаваемые в функцию `read_csv_as_dict`.
-   `**kwargs`: Произвольные именованные аргументы, передаваемые в функцию `read_csv_as_dict`.

**Возвращает**:

-   `dict | None`: Словарь, содержащий данные из CSV, преобразованные в формат JSON, или `None`, если преобразование не удалось.

**Как работает функция**:

1.  Вызывает функцию `read_csv_as_dict` из модуля `src.utils.csv` для чтения данных из CSV файла в формате словаря.
2.  Возвращает результат, полученный от функции `read_csv_as_dict`.

### `csv2ns`

**Назначение**: Преобразует CSV данные в объекты SimpleNamespace.

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

-   `csv_file` (str | Path): Путь к CSV файлу для чтения.
-   `*args`: Произвольные позиционные аргументы, передаваемые в функцию `read_csv_as_ns`.
-   `**kwargs`: Произвольные именованные аргументы, передаваемые в функцию `read_csv_as_ns`.

**Возвращает**:

-   `SimpleNamespace | None`: Объект `SimpleNamespace`, содержащий данные из CSV, или `None`, если преобразование не удалось.

**Как работает функция**:

1.  Вызывает функцию `read_csv_as_ns` из модуля `src.utils.csv` для чтения данных из CSV файла и преобразования их в объекты `SimpleNamespace`.
2.  Возвращает результат, полученный от функции `read_csv_as_ns`.

### `csv_to_json`

**Назначение**: Преобразует CSV файл в формат JSON и сохраняет его в JSON файл.

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

-   `csv_file_path` (str | Path): Путь к CSV файлу для чтения.
-   `json_file_path` (str | Path): Путь к JSON файлу для сохранения.
-   `exc_info` (bool, optional): Если `True`, включает информацию об отслеживании в лог. По умолчанию `True`.

**Возвращает**:

-   `List[Dict[str, str]] | None`: Данные JSON в виде списка словарей или `None`, если преобразование не удалось.

**Как работает функция**:

1.  Вызывает функцию `read_csv_file` из модуля `src.utils.csv` для чтения данных из CSV файла в формате списка словарей.
2.  Если чтение CSV файла прошло успешно, открывает JSON файл для записи.
3.  Записывает данные в JSON файл с отступами для улучшения читаемости.
4.  Возвращает данные JSON в виде списка словарей.
5.  Логирует информацию об ошибке при помощи `logger.error`.

## Переменные модуля

В данном модуле отсутствуют переменные, за исключением констант, определенных внутри функций (если бы они были).

## Пример использования

**Чтение и опциональное сохранение в JSON:**

```python
from src.utils.convertors import csv

data = csv.read_xls_as_dict('input.xlsx', 'output.json', 'Sheet1')  # Чтение листа с именем 'Sheet1'
if data:
    print(data)  # Вывод: {'Sheet1': [{...}]}
```

**Сохранение из JSON данных:**

```python
from src.utils.convertors import csv

data_to_save = {'Sheet1': [{'column1': 'value1', 'column2': 'value2'}]}
success = csv.save_xls_file(data_to_save, 'output.xlsx')
if success:
    print("Successfully saved to output.xlsx")
```

## Взаимосвязь с другими частями проекта

-   Этот модуль зависит от модулей `src.utils.csv`, `src.utils.jjson`, `src.utils.xls` и `src.utils.convertors.dict` для выполнения конкретных преобразований.
-   Для логирования используется модуль `src.logger.logger`.
-   Модуль предназначен для использования в других частях проекта `hypotez`, где требуется преобразование данных CSV в другие форматы.