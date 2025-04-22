# Модуль для работы с CSV и JSON файлами
## Обзор

Модуль `src.utils.csv` предоставляет набор утилит для работы с CSV и JSON файлами. Он включает функции для сохранения данных в CSV файлы, чтения данных из CSV файлов, преобразования CSV файлов в JSON формат и представления содержимого CSV файлов в виде словарей.

## Подробней

Модуль предназначен для упрощения операций чтения и записи данных в формате CSV, а также для преобразования данных между форматами CSV и JSON. Функции модуля обеспечивают гибкость при работе с данными, позволяя сохранять, читать и преобразовывать их в различные структуры данных.

## Классы

В данном модуле классы отсутствуют.

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
```

**Параметры**:
- `data` (List[Dict[str, str]]): Список словарей, которые необходимо сохранить в CSV файл. Каждый словарь представляет собой строку данных, где ключи словаря являются заголовками столбцов.
- `file_path` (Union[str, Path]): Путь к CSV файлу, в который будут сохранены данные. Может быть представлен строкой или объектом `Path`.
- `mode` (str, optional): Режим открытия файла. `'a'` - для добавления данных в конец файла (если файл существует) или создания нового файла (если файл не существует). `'w'` - для перезаписи файла (если файл существует) или создания нового файла (если файл не существует). По умолчанию `'a'`.
- `exc_info` (bool, optional): Определяет, нужно ли включать информацию об исключении (traceback) в логи. По умолчанию `True`.

**Возвращает**:
- `bool`: `True`, если запись в файл прошла успешно, `False` в случае ошибки.

**Вызывает исключения**:
- `TypeError`: Если входные данные `data` не являются списком словарей.
- `ValueError`: Если входной список данных `data` пуст.

**Как работает функция**:

1.  Функция проверяет, что входные данные являются списком словарей. Если это не так, вызывается исключение `TypeError`.
2.  Функция проверяет, что список данных не пуст. Если это так, вызывается исключение `ValueError`.
3.  Функция преобразует `file_path` в объект `Path`.
4.  Создается директория для файла, если она не существует. Параметр `parents=True` обеспечивает создание всех необходимых родительских директорий. Параметр `exist_ok=True` предотвращает возникновение ошибки, если директория уже существует.
5.  Открывается файл в указанном режиме (`mode`) с указанием кодировки `utf-8`.
6.  Создается объект `csv.DictWriter`, который используется для записи словарей в CSV файл. В качестве заголовков столбцов используются ключи первого словаря в списке `data`.
7.  Если файл открывается для записи (mode == 'w') или файл не существует, записывается строка заголовков.
8.  Записываются строки данных из списка `data` в CSV файл.
9.  В случае возникновения исключения в процессе записи, информация об ошибке логируется с использованием `logger.error`, и функция возвращает `False`.

**Примеры**:

```python
from pathlib import Path
from src.utils.csv import save_csv_file

# Пример 1: Сохранение данных в новый CSV файл
data = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
file_path = 'data.csv'
result = save_csv_file(data, file_path, mode='w')
print(f'Результат сохранения: {result}')  # Вывод: Результат сохранения: True

# Пример 2: Добавление данных в существующий CSV файл
data = [{'name': 'Charlie', 'age': '35'}]
file_path = 'data.csv'
result = save_csv_file(data, file_path, mode='a')
print(f'Результат добавления: {result}')  # Вывод: Результат добавления: True

# Пример 3: Обработка ошибки при неверном типе данных
try:
    data = 'not a list'
    file_path = 'data.csv'
    result = save_csv_file(data, file_path, mode='w')
except TypeError as ex:
    print(f'Ошибка типа данных: {ex}')  # Вывод: Ошибка типа данных: Input data must be a list of dictionaries.

# Пример 4: Обработка ошибки при пустом списке данных
try:
    data = []
    file_path = 'data.csv'
    result = save_csv_file(data, file_path, mode='w')
except ValueError as ex:
    print(f'Ошибка значения: {ex}')  # Вывод: Ошибка значения: Input data cannot be empty.
```

### `read_csv_file`

**Назначение**: Читает содержимое CSV файла и возвращает его в виде списка словарей.

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
```

**Параметры**:
- `file_path` (Union[str, Path]): Путь к CSV файлу, который необходимо прочитать. Может быть представлен строкой или объектом `Path`.
- `exc_info` (bool, optional): Определяет, нужно ли включать информацию об исключении (traceback) в логи. По умолчанию `True`.

**Возвращает**:
- `List[Dict[str, str]] | None`: Список словарей, представляющий содержимое CSV файла, где каждый словарь соответствует строке данных. Ключи словаря соответствуют заголовкам столбцов. Возвращает `None`, если чтение файла не удалось.

**Вызывает исключения**:
- `FileNotFoundError`: Если файл не найден.

**Как работает функция**:

1.  Функция пытается открыть CSV файл по указанному пути (`file_path`) в режиме чтения (`'r'`) с кодировкой `utf-8`.
2.  Создается объект `csv.DictReader`, который позволяет читать CSV файл как список словарей.
3.  Функция возвращает список словарей, полученный из CSV файла.
4.  Если файл не найден, возникает исключение `FileNotFoundError`, которое перехватывается. Информация об ошибке логируется с использованием `logger.error`, и функция возвращает `None`.
5.  В случае возникновения другого исключения в процессе чтения, информация об ошибке логируется с использованием `logger.error`, и функция возвращает `None`.

**Примеры**:

```python
from pathlib import Path
from src.utils.csv import read_csv_file

# Пример 1: Чтение существующего CSV файла
file_path = 'data.csv'
data = read_csv_file(file_path)
if data:
    print(f'Содержимое файла: {data}')
else:
    print('Не удалось прочитать файл.')

# Пример 2: Обработка ошибки при отсутствии файла
file_path = 'non_existent_data.csv'
data = read_csv_file(file_path)
if data is None:
    print('Файл не найден.')

# Пример 3: Обработка исключения при поврежденном CSV файле
# (Создайте файл 'bad_data.csv' с некорректным CSV содержимым для этого примера)
file_path = 'bad_data.csv'
data = read_csv_file(file_path)
if data is None:
    print('Не удалось прочитать файл из-за ошибки.')
```

### `read_csv_as_json`

**Назначение**: Преобразует CSV файл в JSON формат и сохраняет его в указанный файл.

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
```

**Параметры**:
- `csv_file_path` (Union[str, Path]): Путь к CSV файлу, который необходимо преобразовать. Может быть представлен строкой или объектом `Path`.
- `json_file_path` (Union[str, Path]): Путь к JSON файлу, в который будут сохранены преобразованные данные. Может быть представлен строкой или объектом `Path`.
- `exc_info` (bool, optional): Определяет, нужно ли включать информацию об исключении (traceback) в логи. По умолчанию `True`.

**Возвращает**:
- `bool`: `True`, если преобразование и сохранение прошли успешно, `False` в случае ошибки.

**Как работает функция**:

1.  Функция вызывает `read_csv_file` для чтения данных из CSV файла.
2.  Если `read_csv_file` возвращает `None` (т.е. не удалось прочитать CSV файл), функция возвращает `False`.
3.  Если данные успешно прочитаны, функция открывает JSON файл в режиме записи (`'w'`) с кодировкой `utf-8`.
4.  Данные записываются в JSON файл с использованием `json.dump` с отступом 4 для удобочитаемости.
5.  В случае возникновения исключения, информация об ошибке логируется с использованием `logger.error`, и функция возвращает `False`.

**Примеры**:

```python
from pathlib import Path
from src.utils.csv import read_csv_as_json, save_csv_file

# Создание тестового CSV файла
test_data = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
csv_file_path = 'test.csv'
save_csv_file(test_data, csv_file_path, mode='w')

# Пример 1: Преобразование CSV в JSON
csv_file_path = 'test.csv'
json_file_path = 'test.json'
result = read_csv_as_json(csv_file_path, json_file_path)
print(f'Результат преобразования CSV в JSON: {result}')

# Пример 2: Обработка ошибки при отсутствии CSV файла
csv_file_path = 'non_existent_test.csv'
json_file_path = 'non_existent_test.json'
result = read_csv_as_json(csv_file_path, json_file_path)
print(f'Результат преобразования CSV в JSON: {result}')
```

### `read_csv_as_dict`

**Назначение**: Преобразует содержимое CSV файла в словарь, где ключ `"data"` содержит список словарей, представляющих строки CSV файла.

```python
def read_csv_as_dict(csv_file: Union[str, Path]) -> dict | None:
    """    Convert CSV content to a dictionary.

    Args:
        csv_file (Union[str, Path]): Path to the CSV file.

    Returns:
        dict | None: Dictionary representation of CSV content, or None if failed.
    """
```

**Параметры**:
- `csv_file` (Union[str, Path]): Путь к CSV файлу, который необходимо прочитать. Может быть представлен строкой или объектом `Path`.

**Возвращает**:
- `dict | None`: Словарь, содержащий ключ `"data"` и список словарей, представляющих содержимое CSV файла. Возвращает `None`, если чтение не удалось.

**Как работает функция**:

1.  Функция открывает CSV файл по указанному пути (`csv_file`) в режиме чтения (`'r'`) с кодировкой `utf-8`.
2.  Создается объект `csv.DictReader`, который позволяет читать CSV файл как список словарей.
3.  Функция возвращает словарь, содержащий ключ `"data"` и список словарей, полученный из CSV файла.
4.  В случае возникновения исключения, информация об ошибке логируется с использованием `logger.error`, и функция возвращает `None`.

**Примеры**:

```python
from pathlib import Path
from src.utils.csv import read_csv_as_dict, save_csv_file

# Создание тестового CSV файла
test_data = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
csv_file_path = 'test.csv'
save_csv_file(test_data, csv_file_path, mode='w')

# Пример 1: Чтение CSV в словарь
csv_file_path = 'test.csv'
data = read_csv_as_dict(csv_file_path)
if data:
    print(f'Содержимое файла в виде словаря: {data}')
else:
    print('Не удалось прочитать файл.')

# Пример 2: Обработка ошибки при отсутствии CSV файла
csv_file_path = 'non_existent_test.csv'
data = read_csv_as_dict(csv_file_path)
if data is None:
    print('Файл не найден.')
```

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
```

**Параметры**:
- `file_path` (Union[str, Path]): Путь к CSV файлу, который необходимо прочитать. Может быть представлен строкой или объектом `Path`.

**Возвращает**:
- `List[dict]`: Список словарей, представляющий содержимое CSV файла.

**Вызывает исключения**:
- `FileNotFoundError`: Если файл не найден.

**Как работает функция**:

1.  Функция использует библиотеку Pandas для чтения CSV файла с использованием `pd.read_csv`.
2.  Затем она преобразует данные в список словарей, используя `df.to_dict(orient='records')`.
3.  В случае, если файл не найден, возникает исключение `FileNotFoundError`, информация об ошибке логируется с использованием `logger.error`, и функция возвращает пустой список.
4.  В случае возникновения другого исключения в процессе чтения или преобразования, информация об ошибке логируется с использованием `logger.error`, и функция возвращает пустой список.

**Примеры**:

```python
from pathlib import Path
from src.utils.csv import read_csv_as_ns, save_csv_file

# Создание тестового CSV файла
test_data = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
csv_file_path = 'test.csv'
save_csv_file(test_data, csv_file_path, mode='w')

# Пример 1: Чтение CSV в список словарей с использованием Pandas
csv_file_path = 'test.csv'
data = read_csv_as_ns(csv_file_path)
print(f'Содержимое файла в виде списка словарей: {data}')

# Пример 2: Обработка ошибки при отсутствии CSV файла
csv_file_path = 'non_existent_test.csv'
data = read_csv_as_ns(csv_file_path)
print(f'Результат при отсутствии файла: {data}')