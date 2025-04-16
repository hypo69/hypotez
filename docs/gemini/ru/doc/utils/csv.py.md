# Модуль для работы с CSV и JSON файлами (src.utils.csv)

## Обзор

Этот модуль предоставляет набор функций для работы с CSV и JSON файлами, включая сохранение данных в CSV, чтение CSV файлов в различные структуры данных (список словарей, JSON, словарь) и преобразование CSV в JSON формат. Он также использует модуль `src.logger.logger` для логирования ошибок и событий.

## Подробней

Модуль предназначен для упрощения операций чтения и записи данных в форматах CSV и JSON. Он предоставляет удобные функции для преобразования данных между этими форматами и обеспечивает надежную обработку ошибок с использованием логирования. Функции модуля позволяют легко интегрировать работу с CSV и JSON файлами в другие части проекта `hypotez`.

## Функции

### `save_csv_file`

**Назначение**: Сохраняет список словарей в CSV файл.

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

**Параметры**:

-   `data` (List[Dict[str, str]]): Список словарей для сохранения.
-   `file_path` (Union[str, Path]): Путь к CSV файлу.
-   `mode` (str): Режим открытия файла (`'a'` - добавление, `'w'` - перезапись). По умолчанию `'a'`.
-   `exc_info` (bool): Включать ли информацию об исключении в логи.

**Возвращает**:

-   `bool`: `True`, если сохранение прошло успешно, `False` - в противном случае.

**Вызывает исключения**:

-   `TypeError`: Если входные данные не являются списком словарей.
-   `ValueError`: Если входные данные пусты.

**Как работает функция**:

1.  Проверяет тип входных данных (`data`). Если это не список, вызывает `TypeError`.
2.  Проверяет, не пуст ли список `data`. Если пуст, вызывает `ValueError`.
3.  Преобразует `file_path` в объект `Path`.
4.  Создает родительские директории для файла, если они не существуют.
5.  Открывает файл для записи (добавления или перезаписи) с указанной кодировкой.
6.  Создает объект `csv.DictWriter` для записи данных в формате словаря.
7.  Если файл только что создан или открыт в режиме перезаписи (`'w'`), записывает заголовок (названия ключей словаря).
8.  Записывает все словари из списка `data` в CSV файл.
9.  Возвращает `True` в случае успеха, `False` в случае ошибки.
10. Логирует информацию об ошибке при помощи `logger.error`.

### `read_csv_file`

**Назначение**: Читает содержимое CSV файла в виде списка словарей.

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

**Параметры**:

-   `file_path` (Union[str, Path]): Путь к CSV файлу.
-   `exc_info` (bool): Включать ли информацию об исключении в логи.

**Возвращает**:

-   `List[Dict[str, str]] | None`: Список словарей, представляющих содержимое CSV файла, или `None` в случае ошибки.

**Вызывает исключения**:

-   `FileNotFoundError`: Если файл не найден.

**Как работает функция**:

1.  Преобразует `file_path` в объект `Path`.
2.  Открывает CSV файл для чтения с указанием кодировки.
3.  Создает объект `csv.DictReader` для чтения данных в формате словаря.
4.  Преобразует содержимое файла в список словарей и возвращает его.
5.  В случае ошибки логирует ее и возвращает `None`.

### `read_csv_as_json`

**Назначение**: Конвертирует CSV файл в JSON формат и сохраняет его в файл.

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

**Параметры**:

-   `csv_file_path` (Union[str, Path]): Путь к CSV файлу.
-   `json_file_path` (Union[str, Path]): Путь для сохранения JSON файла.
-   `exc_info` (bool): Включать ли информацию об исключении в логи.

**Возвращает**:

-   `bool`: `True`, если преобразование прошло успешно, `False` - в противном случае.

**Как работает функция**:

1.  Читает содержимое CSV файла в виде списка словарей, используя функцию `read_csv_file`.
2.  Если чтение CSV файла прошло успешно, открывает JSON файл для записи с указанием кодировки.
3.  Записывает данные в JSON файл с отступами для улучшения читаемости.
4.  Возвращает `True` в случае успеха, `False` в случае ошибки.
5.  Логирует информацию об ошибке при помощи `logger.error`.

### `read_csv_as_dict`

**Назначение**: Преобразует содержимое CSV файла в словарь.

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

**Параметры**:

-   `csv_file` (Union[str, Path]): Путь к CSV файлу.

**Возвращает**:

-   `dict | None`: Словарь, представляющий содержимое CSV файла, или `None` в случае ошибки.

**Как работает функция**:

1.  Преобразует `csv_file` в объект `Path`.
2.  Открывает CSV файл для чтения с указанием кодировки.
3.  Создает объект `csv.DictReader` для чтения данных в формате словаря.
4.  Создает словарь, содержащий список словарей из CSV файла под ключом `"data"` и возвращает его.
5.  Логирует информацию об ошибке при помощи `logger.error`.

### `read_csv_as_ns`

**Назначение**: Загружает данные из CSV файла в список словарей, используя библиотеку Pandas.

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

**Параметры**:

-   `file_path` (Union[str, Path]): Путь к CSV файлу.

**Возвращает**:

-   `List[dict]`: Список словарей, представляющих содержимое CSV файла.

**Вызывает исключения**:

-   `FileNotFoundError`: Если файл не найден.

**Как работает функция**:

1.  Использует библиотеку `pandas` для чтения CSV файла (`pd.read_csv`).
2.  Преобразует содержимое DataFrame в список словарей с помощью `df.to_dict(orient='records')`.
3.  В случае ошибки логирует ее и возвращает пустой список.

## Зависимости

-   `csv`: Для работы с CSV файлами.
-   `json`: Для работы с JSON файлами.
-   `pathlib.Path`: Для работы с путями к файлам.
-   `typing.List`, `typing.Dict`, `typing.Union`: Для аннотации типов.
-   `pandas`: Для чтения CSV в DataFrame.
-   `src.logger.logger`: Для логирования информации об ошибках.

## Пример использования

```python
from src.utils.csv import save_csv_file, read_csv_file

# Пример данных
data = [
    {'name': 'John', 'age': '30', 'city': 'New York'},
    {'name': 'Jane', 'age': '25', 'city': 'London'}
]

# Сохранение в CSV
save_csv_file(data, 'output.csv', mode='w')

# Чтение из CSV
read_data = read_csv_file('output.csv')
print(read_data)
```

## Связь с другими частями проекта

Модуль `src.utils.csv` используется в других частях проекта `hypotez` для работы с данными в форматах CSV и JSON. Он обеспечивает простой и надежный способ чтения и записи данных, а также интеграцию с системой логирования проекта. Модуль может использоваться для импорта данных из внешних источников, экспорта результатов работы алгоритмов и хранения конфигурационной информации.