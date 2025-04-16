### Анализ кода `hypotez/src/utils/csv.py.md`

## Обзор

Модуль предоставляет набор утилит для работы с файлами CSV и JSON, включая функции для сохранения данных в CSV-файл, чтения данных из CSV-файла и конвертации CSV в JSON.

## Подробнее

Модуль содержит набор функций, упрощающих операции чтения и записи данных в формате CSV и JSON.  Он позволяет сохранять данные в CSV-файл из списка словарей, читать CSV-файл в виде списка словарей, преобразовывать CSV-файл в JSON-формат и читать CSV-файл, используя библиотеку Pandas. Также реализовано логирование ошибок при работе с файлами.

## Функции

### `save_csv_file`

```python
def save_csv_file(
    data: List[Dict[str, str]],
    file_path: Union[str, Path],
    mode: str = 'a',
    exc_info: bool = True,
) -> bool:
    """    Saves a list of dictionaries to a CSV file.

    Args:
        data (List[Dict[str, str]]): List of dictionaries to save.
        file_path (Union[str, Path]): Path to the CSV file.
        mode (str): File mode ('a' to append, 'w' to overwrite). Default is 'a'.
        exc_info (bool): Include traceback information in logs.

    Returns:
        bool: True if successful, otherwise False.

    Raises:
        TypeError: If input data is not a list of dictionaries.
        ValueError: If input data is empty.
    """
    ...
```

**Назначение**:
Сохраняет список словарей в CSV-файл.

**Параметры**:

*   `data` (List[Dict[str, str]]): Список словарей для сохранения.
*   `file_path` (Union[str, Path]): Путь к CSV-файлу.
*   `mode` (str): Режим открытия файла ('a' для добавления, 'w' для перезаписи). По умолчанию 'a'.
*   `exc_info` (bool): Включать ли информацию об исключении в логи.

**Возвращает**:

*   `bool`: `True`, если сохранение прошло успешно, иначе `False`.

**Вызывает исключения**:

*   `TypeError`: Если входные данные не являются списком словарей.
*   `ValueError`: Если входные данные пусты.

**Как работает функция**:

1.  Проверяет, является ли входной параметр `data` списком. Если нет, выбрасывает исключение `TypeError`.
2.  Проверяет, не является ли входной параметр `data` пустым. Если да, выбрасывает исключение `ValueError`.
3.  Преобразует `file_path` в объект `Path`.
4.  Создает родительские директории, если они не существуют.
5.  Открывает файл для записи.
6.  Создает объект `csv.DictWriter` для записи данных в формате CSV.
7.  Если файл открыт в режиме записи (`mode == 'w'`) или файл не существует, записывает заголовок CSV.
8.  Записывает данные в CSV-файл.
9.  Возвращает `True` в случае успеха.
10. В случае возникновения исключения логирует ошибку и возвращает `False`.

### `read_csv_file`

```python
def read_csv_file(file_path: Union[str, Path], exc_info: bool = True) -> List[Dict[str, str]] | None:
    """    Reads CSV content as a list of dictionaries.

    Args:
        file_path (Union[str, Path]): Path to the CSV file.
        exc_info (bool): Include traceback information in logs.

    Returns:
        List[Dict[str, str]] | None: List of dictionaries or None if failed.

    Raises:
        FileNotFoundError: If file not found.
    """
    ...
```

**Назначение**:
Читает содержимое CSV-файла и возвращает его в виде списка словарей.

**Параметры**:

*   `file_path` (Union[str, Path]): Путь к CSV-файлу.
*   `exc_info` (bool): Включать ли информацию об исключении в логи.

**Возвращает**:

*   `List[Dict[str, str]] | None`: Список словарей или `None`, если чтение не удалось.

**Вызывает исключения**:

*   `FileNotFoundError`: Если файл не найден.

**Как работает функция**:

1.  Открывает файл для чтения.
2.  Создает объект `csv.DictReader` для чтения данных в формате CSV.
3.  Преобразует данные в список словарей.
4.  Возвращает список словарей.
5.  В случае возникновения исключения `FileNotFoundError` логирует ошибку и возвращает `None`.
6.  В случае возникновения других исключений логирует ошибку и возвращает `None`.

### `read_csv_as_json`

```python
def read_csv_as_json(csv_file_path: Union[str, Path], json_file_path: Union[str, Path], exc_info: bool = True) -> bool:
    """    Convert a CSV file to JSON format and save it.

    Args:
        csv_file_path (Union[str, Path]): Path to the CSV file.
        json_file_path (Union[str, Path]): Path to save the JSON file.
        exc_info (bool): Include traceback information in logs.

    Returns:
        bool: True if conversion is successful, else False.
    """
    ...
```

**Назначение**:
Преобразует CSV-файл в JSON-формат и сохраняет результат в JSON-файл.

**Параметры**:

*   `csv_file_path` (Union[str, Path]): Путь к CSV-файлу.
*   `json_file_path` (Union[str, Path]): Путь к JSON-файлу для сохранения результата.
*   `exc_info` (bool): Включать ли информацию об исключении в логи.

**Возвращает**:

*   `bool`: `True`, если преобразование и сохранение прошли успешно, иначе `False`.

**Как работает функция**:

1.  Читает данные из CSV-файла с помощью функции `read_csv_file`.
2.  Если чтение не удалось, возвращает `False`.
3.  Открывает JSON-файл для записи.
4.  Записывает данные в JSON-файл с отступами для читаемости.
5.  Возвращает `True` в случае успеха.
6.  В случае возникновения исключения логирует ошибку и возвращает `False`.

### `read_csv_as_dict`

```python
def read_csv_as_dict(csv_file: Union[str, Path]) -> dict | None:
    """    Convert CSV content to a dictionary.

    Args:
        csv_file (Union[str, Path]): Path to the CSV file.

    Returns:
        dict | None: Dictionary representation of CSV content, or None if failed.
    """
    ...
```

**Назначение**:
Преобразует содержимое CSV-файла в словарь.

**Параметры**:

*   `csv_file` (Union[str, Path]): Путь к CSV-файлу.

**Возвращает**:

*   `dict | None`: Словарь, представляющий содержимое CSV-файла, или `None`, если чтение не удалось.

**Как работает функция**:

1.  Открывает CSV-файл для чтения.
2.  Создает объект `csv.DictReader` для чтения данных в формате CSV.
3.  Преобразует данные в словарь с ключом `"data"` и значением в виде списка строк CSV-файла.
4.  Возвращает словарь.
5.  В случае возникновения исключения логирует ошибку и возвращает `None`.

### `read_csv_as_ns`

```python
def read_csv_as_ns(file_path: Union[str, Path]) -> List[dict]:
    """!
    Load CSV data into a list of dictionaries using Pandas.

    Args:
        file_path (Union[str, Path]): Path to the CSV file.

    Returns:
        List[dict]: List of dictionaries representing the CSV content.

    Raises:
        FileNotFoundError: If file not found.
    """
    ...
```

**Назначение**:
Загружает данные из CSV-файла в список словарей с использованием библиотеки Pandas.

**Параметры**:

*   `file_path` (Union[str, Path]): Путь к CSV-файлу.

**Возвращает**:

*   `List[dict]`: Список словарей, представляющих содержимое CSV-файла.

**Вызывает исключения**:

*   `FileNotFoundError`: Если файл не найден.

**Как работает функция**:

1.  Использует `pd.read_csv` для чтения CSV-файла в объект DataFrame библиотеки Pandas.
2.  Преобразует DataFrame в список словарей с помощью метода `to_dict(orient='records')`.
3.  Возвращает список словарей.
4.  В случае возникновения исключения `FileNotFoundError` логирует ошибку и возвращает пустой список.
5.  В случае возникновения других исключений логирует ошибку и возвращает пустой список.

## Зависимости

*   `csv`: Стандартный модуль Python для работы с CSV-файлами.
*   `json`: Стандартный модуль Python для работы с JSON-данными.
*   `pathlib.Path`: Для работы с путями к файлам.
*   `typing.List, typing.Dict, typing.Union`: Для аннотаций типов.
*   `pandas`: Для работы с табличными данными.
*   `src.logger.logger`: Для логирования событий и ошибок.

## Взаимосвязи с другими частями проекта

*   Модуль `csv.py` предоставляет утилиты для работы с CSV-файлами, которые могут использоваться в различных частях проекта `hypotez` для чтения и записи данных в формате CSV.
*   Модуль использует `src.logger.logger` для логирования ошибок и информации о работе функций.
*   Функции для работы с JSON могут использоваться совместно с модулями, работающими с API или другими источниками JSON-данных.