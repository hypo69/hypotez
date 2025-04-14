# Модуль `csv`

## Обзор

Модуль `csv` предоставляет утилиты для конвертации данных между форматами CSV и JSON. Он включает функции для чтения CSV-файлов и преобразования их в словари (`dict`) или объекты `SimpleNamespace`, а также функцию для сохранения данных из CSV-файла в формате JSON.

## Подробнее

Этот модуль предназначен для упрощения обработки данных, хранящихся в формате CSV, и их преобразования в другие форматы, такие как JSON, которые могут быть более удобными для использования в различных приложениях. Модуль использует стандартные библиотеки `json` и `csv`, а также модуль `logger` для логирования ошибок.
Расположение файла в проекте: `/src/utils/convertors/csv.py`

## Функции

### `csv2dict`

```python
def csv2dict(csv_file: str | Path, *args, **kwargs) -> dict | None:
    """
    Конвертирует данные из CSV-файла в словарь.

    Args:
        csv_file (str | Path): Путь к CSV-файлу, который необходимо прочитать.
        *args: Произвольные позиционные аргументы, передаваемые в функцию `read_csv_as_dict`.
        **kwargs: Произвольные именованные аргументы, передаваемые в функцию `read_csv_as_dict`.

    Returns:
        dict | None: Словарь, содержащий данные из CSV-файла, преобразованные в формат JSON, или `None`, если преобразование не удалось.

    Raises:
        Exception: Если не удается прочитать CSV-файл.

    """
```

**Как работает функция**:

1.  Функция `csv2dict` принимает путь к CSV-файлу (`csv_file`) в качестве аргумента.
2.  Вызывает функцию `read_csv_as_dict` с переданным путем к файлу и дополнительными аргументами (`*args`, `**kwargs`).
3.  Возвращает результат, полученный от функции `read_csv_as_dict`, который представляет собой словарь с данными из CSV-файла или `None` в случае ошибки.

```
    Начало
    ↓
    → Вызов read_csv_as_dict(csv_file, *args, **kwargs)
    ↓
    Возврат результата
    ↓
    Конец
```

**Примеры**:

```python
from pathlib import Path
from src.utils.convertors.csv import csv2dict

# Пример 1: Чтение CSV-файла и преобразование его в словарь
csv_file_path = Path('example.csv')  # Допустим, что такой файл существует
data = csv2dict(csv_file_path)
if data:
    print(data)
else:
    print("Не удалось преобразовать CSV в словарь.")

# Пример 2: Чтение CSV-файла с дополнительными аргументами
csv_file_path = 'example.csv'
data = csv2dict(csv_file_path, delimiter=';')  # Указание разделителя
if data:
    print(data)
else:
    print("Не удалось преобразовать CSV в словарь.")
```

### `csv2ns`

```python
def csv2ns(csv_file: str | Path, *args, **kwargs) -> SimpleNamespace | None:
    """
    Конвертирует данные из CSV-файла в объекты SimpleNamespace.

    Args:
        csv_file (str | Path): Путь к CSV-файлу, который необходимо прочитать.
        *args: Произвольные позиционные аргументы, передаваемые в функцию `read_csv_as_ns`.
        **kwargs: Произвольные именованные аргументы, передаваемые в функцию `read_csv_as_ns`.

    Returns:
        SimpleNamespace | None: Объект SimpleNamespace, содержащий данные из CSV-файла, или `None`, если преобразование не удалось.

    Raises:
        Exception: Если не удается прочитать CSV-файл.
    """
```

**Как работает функция**:

1.  Функция `csv2ns` принимает путь к CSV-файлу (`csv_file`) в качестве аргумента.
2.  Вызывает функцию `read_csv_as_ns` с переданным путем к файлу и дополнительными аргументами (`*args`, `**kwargs`).
3.  Возвращает результат, полученный от функции `read_csv_as_ns`, который представляет собой объект `SimpleNamespace` с данными из CSV-файла или `None` в случае ошибки.

```
    Начало
    ↓
    → Вызов read_csv_as_ns(csv_file, *args, **kwargs)
    ↓
    Возврат результата
    ↓
    Конец
```

**Примеры**:

```python
from pathlib import Path
from src.utils.convertors.csv import csv2ns

# Пример 1: Чтение CSV-файла и преобразование его в SimpleNamespace
csv_file_path = Path('example.csv')  # Допустим, что такой файл существует
data = csv2ns(csv_file_path)
if data:
    print(data)
else:
    print("Не удалось преобразовать CSV в SimpleNamespace.")

# Пример 2: Чтение CSV-файла с дополнительными аргументами
csv_file_path = 'example.csv'
data = csv2ns(csv_file_path, delimiter=';')  # Указание разделителя
if data:
    print(data)
else:
    print("Не удалось преобразовать CSV в SimpleNamespace.")
```

### `csv_to_json`

```python
def csv_to_json(
    csv_file_path: str | Path,
    json_file_path: str | Path,
    exc_info: bool = True
) -> List[Dict[str, str]] | None:
    """ Конвертирует CSV-файл в формат JSON и сохраняет его в JSON-файл.

    Args:
        csv_file_path (str | Path): Путь к CSV-файлу для чтения.
        json_file_path (str | Path): Путь к JSON-файлу для сохранения.
        exc_info (bool, optional): Если True, включает информацию трассировки в журнал. По умолчанию True.

    Returns:
        List[Dict[str, str]] | None: Данные JSON в виде списка словарей или None, если преобразование не удалось.

    Example:
        >>> json_data = csv_to_json('dialogue_log.csv', 'dialogue_log.json')
        >>> print(json_data)
        [{'role': 'user', 'content': 'Hello'}, {'role': 'assistant', 'content': 'Hi there!'}]
    """
```

**Как работает функция**:

1.  Функция `csv_to_json` принимает пути к CSV-файлу (`csv_file_path`) и JSON-файлу (`json_file_path`) в качестве аргументов. Также принимает необязательный аргумент `exc_info`, который определяет, следует ли включать информацию трассировки в журнал в случае ошибки (по умолчанию `True`).
2.  Вызывает функцию `read_csv_file` для чтения данных из CSV-файла.
3.  Если данные успешно прочитаны (не `None`), открывает JSON-файл для записи (`'w'`) с кодировкой UTF-8.
4.  Использует функцию `json.dump` для записи данных в JSON-файл с отступом 4 для удобочитаемости.
5.  Возвращает прочитанные данные в формате списка словарей.
6.  В случае возникновения исключения (например, если не удается прочитать CSV-файл или записать JSON-файл), логирует ошибку с использованием `logger.error` и возвращает `None`.

```
    Начало
    ↓
    → Вызов read_csv_file(csv_file_path, exc_info=exc_info)
    ↓
    Данные прочитаны?
    ├─── Да → Открытие JSON-файла для записи
    │       ↓
    │       → Запись данных в JSON-файл с использованием json.dump
    │       ↓
    │       → Возврат данных
    └─── Нет → Логирование ошибки и возврат None
    ↓
    Конец
```

**Примеры**:

```python
from pathlib import Path
from src.utils.convertors.csv import csv_to_json

# Пример 1: Преобразование CSV-файла в JSON
csv_file = Path('input.csv') # Создаем объект Path
json_file = Path('output.json')# Создаем объект Path

json_data = csv_to_json(csv_file, json_file)

if json_data:
    print("CSV успешно преобразован в JSON.")
    # print(json_data)  # Вывод данных JSON (опционально)
else:
    print("Не удалось преобразовать CSV в JSON.")

# Создаем example.csv для тестов
#import csv
#data = [{'name': 'user', 'surname': 'test_user'}, {'name': 'user2', 'surname': 'test_user2'}]
#with open('input.csv', 'w') as f:
#   writer = csv.DictWriter(f, fieldnames=data[0].keys())
#    writer.writeheader()
#    writer.writerows(data)
```
```python
from pathlib import Path
from src.utils.convertors.csv import csv_to_json

# Пример 2: Обработка ошибки при преобразовании
csv_file = Path('non_existent.csv')
json_file = Path('output.json')

json_data = csv_to_json(csv_file, json_file)

if json_data:
    print("CSV успешно преобразован в JSON.")
else:
    print("Не удалось преобразовать CSV в JSON.")
```
```python
from pathlib import Path
from src.utils.convertors.csv import csv_to_json

# Пример 3: Отключение логирования трассировки
csv_file = Path('input.csv')
json_file = Path('output.json')

json_data = csv_to_json(csv_file, json_file, exc_info=False)

if json_data:
    print("CSV успешно преобразован в JSON.")
else:
    print("Не удалось преобразовать CSV в JSON.")