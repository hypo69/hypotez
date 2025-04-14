# Модуль для работы с CSV и JSON файлами
=================================================

Модуль содержит функции для сохранения, чтения и конвертации данных между форматами CSV и JSON.
Он включает функции для записи данных в CSV файлы, чтения CSV файлов в виде списка словарей, конвертации CSV в JSON,
а также для чтения CSV файлов с использованием библиотеки `pandas`.

## Обзор

Модуль предоставляет набор утилит для работы с CSV и JSON файлами. Он упрощает операции чтения и записи данных, а также обеспечивает возможность конвертации между этими двумя форматами.

## Подробней

Этот модуль разработан для облегчения обработки данных, хранящихся в формате CSV и JSON. Он предоставляет функции для сохранения данных в CSV файлы, чтения данных из CSV файлов в виде списка словарей, преобразования CSV файлов в JSON формат и чтения CSV файлов с использованием библиотеки `pandas`.
Модуль использует библиотеку `csv` для работы с CSV файлами, библиотеку `json` для работы с JSON файлами, библиотеку `pathlib` для работы с путями к файлам, библиотеку `typing` для аннотации типов и библиотеку `pandas` для чтения CSV файлов в виде DataFrame.
Расположение файла в проекте: `hypotez/src/utils/csv.py`.

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
```

**Назначение**: Сохраняет список словарей в CSV файл.

**Параметры**:
- `data` (List[Dict[str, str]]): Список словарей для сохранения. Каждый словарь представляет строку в CSV файле, где ключи словаря становятся заголовками столбцов.
- `file_path` (Union[str, Path]): Путь к CSV файлу, в который будут сохранены данные. Может быть строкой или объектом `Path`.
- `mode` (str): Режим открытия файла. `'a'` - для добавления данных в конец файла, `'w'` - для перезаписи файла. По умолчанию `'a'`.
- `exc_info` (bool): Флаг, указывающий, нужно ли включать информацию об исключении в логи. По умолчанию `True`.

**Возвращает**:
- `bool`: `True`, если сохранение прошло успешно, `False` в противном случае.

**Вызывает исключения**:
- `TypeError`: Если входные данные не являются списком словарей.
- `ValueError`: Если входной список данных пуст.

**Как работает функция**:
1. **Проверка входных данных**:
   - Проверяется, что входные данные (`data`) являются списком. Если нет, вызывается исключение `TypeError`.
   - Проверяется, что список данных не пуст. Если пуст, вызывается исключение `ValueError`.
2. **Подготовка к записи**:
   - Преобразует `file_path` в объект `Path`.
   - Создает родительские директории для файла, если они не существуют. Параметр `exist_ok=True` предотвращает возникновение ошибки, если директория уже существует.
3. **Запись данных в файл**:
   - Открывает файл в указанном режиме (`mode`) с кодировкой `utf-8`.
   - Создает объект `csv.DictWriter` для записи словарей в CSV файл.
   - Если файл открыт в режиме записи (`'w'`) или файл не существует, записывает заголовки столбцов из ключей первого словаря в списке.
   - Записывает все словари из списка `data` в CSV файл.
4. **Обработка исключений**:
   - Если в процессе записи возникает исключение, оно логируется с помощью `logger.error` и возвращается `False`.

**ASCII flowchart**:

```
A [Проверка типа данных]
|
B [Проверка на пустоту]
|
C [Преобразование file_path в Path]
|
D [Создание родительских директорий]
|
E [Открытие файла]
|
F [Создание csv.DictWriter]
|
G [Запись заголовка (если необходимо)]
|
H [Запись данных]
|
I [Успешное завершение]
```

**Примеры**:

```python
from pathlib import Path
import os
from src.logger.logger import logger

# Пример 1: Сохранение данных в новый CSV файл
data1 = [{'name': 'John', 'age': '30'}, {'name': 'Alice', 'age': '25'}]
file_path1 = 'example1.csv'
result1 = save_csv_file(data1, file_path1, mode='w')
print(f'Результат сохранения в новый файл: {result1}')

# Пример 2: Добавление данных в существующий CSV файл
data2 = [{'name': 'Bob', 'age': '40'}]
file_path2 = 'example1.csv'  # Используем тот же файл, что и в примере 1
result2 = save_csv_file(data2, file_path2, mode='a')
print(f'Результат добавления в существующий файл: {result2}')

# Пример 3: Обработка ошибки при некорректных данных
data3 = "неправильный формат данных"
file_path3 = 'example3.csv'
try:
    result3 = save_csv_file(data3, file_path3, mode='w')
    print(f'Результат сохранения с неправильными данными: {result3}')
except TypeError as ex:
    logger.error("Ошибка типа данных:", ex, exc_info = True)
```

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
```

**Назначение**: Читает содержимое CSV файла и возвращает его в виде списка словарей.

**Параметры**:
- `file_path` (Union[str, Path]): Путь к CSV файлу. Может быть строкой или объектом `Path`.
- `exc_info` (bool): Флаг, указывающий, нужно ли включать информацию об исключении в логи. По умолчанию `True`.

**Возвращает**:
- `List[Dict[str, str]] | None`: Список словарей, где каждый словарь представляет строку из CSV файла. Заголовки столбцов используются в качестве ключей словаря. Возвращает `None`, если произошла ошибка при чтении файла.

**Вызывает исключения**:
- `FileNotFoundError`: Если файл не найден.

**Как работает функция**:
1. **Открытие файла**:
   - Открывает файл по указанному пути (`file_path`) в режиме чтения (`'r'`) с кодировкой `utf-8`.
2. **Чтение данных**:
   - Создает объект `csv.DictReader` для чтения CSV файла как списка словарей.
   - Преобразует и возвращает содержимое файла в виде списка словарей.
3. **Обработка исключений**:
   - Если файл не найден, логируется ошибка `FileNotFoundError` и возвращается `None`.
   - Если в процессе чтения возникает другое исключение, оно логируется с помощью `logger.error` и возвращается `None`.

**ASCII flowchart**:

```
A [Открытие файла]
|
B [Создание csv.DictReader]
|
C [Чтение данных]
|
D [Успешное завершение]
```

**Примеры**:

```python
from pathlib import Path
import os
from src.logger.logger import logger

# Пример 1: Чтение существующего CSV файла
file_path1 = 'example1.csv'  # Файл, созданный в примере save_csv_file
result1 = read_csv_file(file_path1)
print(f'Результат чтения существующего файла: {result1}')

# Пример 2: Обработка ошибки при отсутствии файла
file_path2 = 'non_existent.csv'
result2 = read_csv_file(file_path2)
print(f'Результат чтения несуществующего файла: {result2}')

# Пример 3: Чтение CSV файла с абсолютным путем
current_dir = Path.cwd()
file_path3 = current_dir / 'example1.csv'
result3 = read_csv_file(file_path3)
print(f'Результат чтения файла с абсолютным путем: {result3}')
```

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
```

**Назначение**: Преобразует CSV файл в JSON формат и сохраняет его в указанный файл.

**Параметры**:
- `csv_file_path` (Union[str, Path]): Путь к CSV файлу, который нужно преобразовать. Может быть строкой или объектом `Path`.
- `json_file_path` (Union[str, Path]): Путь к файлу, в который будет сохранен JSON. Может быть строкой или объектом `Path`.
- `exc_info` (bool): Флаг, указывающий, нужно ли включать информацию об исключении в логи. По умолчанию `True`.

**Возвращает**:
- `bool`: `True`, если преобразование и сохранение прошли успешно, `False` в противном случае.

**Как работает функция**:
1. **Чтение CSV файла**:
   - Вызывает функцию `read_csv_file` для чтения содержимого CSV файла в виде списка словарей.
   - Если чтение не удалось (возвращается `None`), функция возвращает `False`.
2. **Запись JSON файла**:
   - Открывает файл по указанному пути (`json_file_path`) в режиме записи (`'w'`) с кодировкой `utf-8`.
   - Использует `json.dump` для записи списка словарей в файл в формате JSON с отступами (`indent=4`) для удобочитаемости.
3. **Обработка исключений**:
   - Если в процессе чтения или записи возникает исключение, оно логируется с помощью `logger.error` и возвращается `False`.

**ASCII flowchart**:

```
A [Чтение CSV файла (read_csv_file)]
|
B [Проверка успешности чтения]
|
C [Открытие JSON файла]
|
D [Запись JSON данных]
|
E [Успешное завершение]
```

**Примеры**:

```python
from pathlib import Path
import os
from src.logger.logger import logger

# Пример 1: Преобразование CSV в JSON
csv_file_path1 = 'example1.csv'  # Файл, созданный в примере save_csv_file
json_file_path1 = 'example1.json'
result1 = read_csv_as_json(csv_file_path1, json_file_path1)
print(f'Результат преобразования CSV в JSON: {result1}')

# Пример 2: Обработка ошибки при отсутствии CSV файла
csv_file_path2 = 'non_existent.csv'
json_file_path2 = 'non_existent.json'
result2 = read_csv_as_json(csv_file_path2, json_file_path2)
print(f'Результат преобразования несуществующего CSV в JSON: {result2}')
```

### `read_csv_as_dict`

```python
def read_csv_as_dict(csv_file: Union[str, Path]) -> dict | None:
    """    Convert CSV content to a dictionary.

    Args:
        csv_file (Union[str, Path]): Path to the CSV file.

    Returns:
        dict | None: Dictionary representation of CSV content, or None if failed.
    """
```

**Назначение**: Преобразует содержимое CSV файла в словарь, где ключ `"data"` содержит список словарей, представляющих строки CSV файла.

**Параметры**:
- `csv_file` (Union[str, Path]): Путь к CSV файлу. Может быть строкой или объектом `Path`.

**Возвращает**:
- `dict | None`: Словарь, содержащий ключ `"data"` и список словарей в качестве значения. Возвращает `None`, если произошла ошибка при чтении файла.

**Как работает функция**:
1. **Открытие файла**:
   - Открывает файл по указанному пути (`csv_file`) в режиме чтения (`'r'`) с кодировкой `utf-8`.
2. **Чтение данных**:
   - Создает объект `csv.DictReader` для чтения CSV файла как списка словарей.
   - Преобразует содержимое файла в словарь, где ключ `"data"` содержит список словарей, представляющих строки CSV файла.
3. **Обработка исключений**:
   - Если в процессе чтения возникает исключение, оно логируется с помощью `logger.error` и возвращается `None`.

**ASCII flowchart**:

```
A [Открытие файла]
|
B [Создание csv.DictReader]
|
C [Чтение данных]
|
D [Формирование словаря]
|
E [Успешное завершение]
```

**Примеры**:

```python
from pathlib import Path
import os
from src.logger.logger import logger

# Пример 1: Чтение CSV файла и преобразование в словарь
csv_file_path1 = 'example1.csv'  # Файл, созданный в примере save_csv_file
result1 = read_csv_as_dict(csv_file_path1)
print(f'Результат преобразования CSV в словарь: {result1}')

# Пример 2: Обработка ошибки при отсутствии CSV файла
csv_file_path2 = 'non_existent.csv'
result2 = read_csv_as_dict(csv_file_path2)
print(f'Результат преобразования несуществующего CSV в словарь: {result2}')
```

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
```

**Назначение**: Загружает данные из CSV файла в виде списка словарей, используя библиотеку `pandas`.

**Параметры**:
- `file_path` (Union[str, Path]): Путь к CSV файлу. Может быть строкой или объектом `Path`.

**Возвращает**:
- `List[dict]`: Список словарей, где каждый словарь представляет строку из CSV файла. Заголовки столбцов используются в качестве ключей словаря. Возвращает пустой список, если произошла ошибка при чтении файла.

**Вызывает исключения**:
- `FileNotFoundError`: Если файл не найден.

**Как работает функция**:
1. **Чтение CSV файла с помощью pandas**:
   - Использует `pd.read_csv` для чтения CSV файла в DataFrame.
2. **Преобразование в список словарей**:
   - Преобразует DataFrame в список словарей с помощью `df.to_dict(orient='records')`.
3. **Обработка исключений**:
   - Если файл не найден, логируется ошибка `FileNotFoundError` и возвращается пустой список.
   - Если в процессе чтения возникает другое исключение, оно логируется с помощью `logger.error` и возвращается пустой список.

**ASCII flowchart**:

```
A [Чтение CSV файла (pandas)]
|
B [Преобразование в список словарей]
|
C [Успешное завершение]
```

**Примеры**:

```python
from pathlib import Path
import os
from src.logger.logger import logger

# Пример 1: Чтение CSV файла с использованием pandas
csv_file_path1 = 'example1.csv'  # Файл, созданный в примере save_csv_file
result1 = read_csv_as_ns(csv_file_path1)
print(f'Результат чтения CSV с pandas: {result1}')

# Пример 2: Обработка ошибки при отсутствии CSV файла
csv_file_path2 = 'non_existent.csv'
result2 = read_csv_as_ns(csv_file_path2)
print(f'Результат чтения несуществующего CSV с pandas: {result2}')