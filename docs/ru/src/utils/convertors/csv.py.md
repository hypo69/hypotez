# Модуль `src.utils.convertors.csv`

## Обзор

Модуль предоставляет утилиты для конвертации данных между форматами CSV и JSON.
Он включает функции для преобразования CSV данных в словари и объекты SimpleNamespace, а также для сохранения CSV-файлов и чтения CSV-файлов.

## Подробней

Модуль содержит функции, которые позволяют преобразовывать данные из формата CSV в JSON и наоборот. Он предоставляет удобные инструменты для работы с данными, представленными в формате CSV, и их преобразования в другие структуры данных, такие как словари и объекты SimpleNamespace. Модуль использует библиотеку `csv` для чтения и записи CSV-файлов, а также библиотеку `json` для работы с данными в формате JSON.

## Функции

### `csv2dict`

```python
def csv2dict(csv_file: str | Path, *args, **kwargs) -> dict | None:
    """
    Конвертирует CSV данные в словарь.

    Args:
        csv_file (str | Path): Путь к CSV-файлу для чтения.

    Returns:
        dict | None: Словарь, содержащий данные из CSV, преобразованные в формат JSON, или `None`, если преобразование не удалось.

    Raises:
        Exception: Если не удается прочитать CSV.
    """
    ...
```

**Назначение**: Преобразует данные из CSV файла в словарь.
**Параметры**:
- `csv_file` (str | Path): Путь к CSV файлу, который нужно преобразовать.
- `*args`:  Произвольные позиционные аргументы, передаваемые в функцию `read_csv_as_dict`.
- `**kwargs`: Произвольные именованные аргументы, передаваемые в функцию `read_csv_as_dict`.

**Возвращает**:
- `dict | None`:  Словарь, содержащий данные из CSV файла. Возвращает `None` в случае ошибки.

**Вызывает исключения**:
- `Exception`: Если не удается прочитать CSV файл.

**Как работает функция**:
- Функция вызывает функцию `read_csv_as_dict` из модуля `src.utils.csv`, передавая ей путь к CSV файлу и дополнительные аргументы.
- Функция `read_csv_as_dict` читает CSV файл и преобразует его содержимое в словарь.
- Функция возвращает полученный словарь.

**Примеры**:

```python
from pathlib import Path
csv_file_path = Path('data.csv')
data = csv2dict(csv_file_path)
if data:
    print(data)
```

### `csv2ns`

```python
def csv2ns(csv_file: str | Path, *args, **kwargs) -> SimpleNamespace | None:
    """
    Конвертирует CSV данные в объекты SimpleNamespace.

    Args:
        csv_file (str | Path): Путь к CSV-файлу для чтения.

    Returns:
        SimpleNamespace | None: Объект SimpleNamespace, содержащий данные из CSV, или `None`, если преобразование не удалось.

    Raises:
        Exception: Если не удается прочитать CSV.
    """
    ...
```

**Назначение**: Преобразует данные из CSV файла в объект `SimpleNamespace`.

**Параметры**:
- `csv_file` (str | Path): Путь к CSV файлу, который нужно преобразовать.
- `*args`:  Произвольные позиционные аргументы, передаваемые в функцию `read_csv_as_ns`.
- `**kwargs**: Произвольные именованные аргументы, передаваемые в функцию `read_csv_as_ns`.

**Возвращает**:
- `SimpleNamespace | None`:  Объект `SimpleNamespace`, содержащий данные из CSV файла. Возвращает `None` в случае ошибки.

**Вызывает исключения**:
- `Exception`: Если не удается прочитать CSV файл.

**Как работает функция**:
- Функция вызывает функцию `read_csv_as_ns` из модуля `src.utils.csv`, передавая ей путь к CSV файлу и дополнительные аргументы.
- Функция `read_csv_as_ns` читает CSV файл и преобразует его содержимое в объект `SimpleNamespace`.
- Функция возвращает полученный объект `SimpleNamespace`.

**Примеры**:

```python
from pathlib import Path
csv_file_path = Path('data.csv')
data = csv2ns(csv_file_path)
if data:
    print(data)
```

### `csv_to_json`

```python
def csv_to_json(
    csv_file_path: str | Path,
    json_file_path: str | Path,
    exc_info: bool = True
) -> List[Dict[str, str]] | None:
    """ Конвертирует CSV файл в формат JSON и сохраняет его в JSON файл.

    Args:
        csv_file_path (str | Path): Путь к CSV файлу для чтения.
        json_file_path (str | Path): Путь к JSON файлу для сохранения.
        exc_info (bool, optional): Если True, включает информацию об отслеживании в лог. По умолчанию True.

    Returns:
        List[Dict[str, str]] | None: Данные JSON в виде списка словарей или None, если преобразование не удалось.

    Example:
        >>> json_data = csv_to_json('dialogue_log.csv', 'dialogue_log.json')
        >>> print(json_data)
        [{'role': 'user', 'content': 'Hello'}, {'role': 'assistant', 'content': 'Hi there!'}]
    """
    ...
```

**Назначение**: Преобразует CSV файл в формат JSON и сохраняет его в JSON файл.

**Параметры**:
- `csv_file_path` (str | Path): Путь к CSV файлу, который нужно преобразовать.
- `json_file_path` (str | Path): Путь к JSON файлу, в который будет сохранен результат.
- `exc_info` (bool, optional): Флаг, определяющий, нужно ли включать информацию об исключении в лог. По умолчанию `True`.

**Возвращает**:
- `List[Dict[str, str]] | None`: Список словарей, представляющий данные в формате JSON. Возвращает `None` в случае ошибки.

**Вызывает исключения**:
- Отсутствуют явные указания на вызываемые исключения, но в случае ошибки функция логирует информацию об ошибке с помощью `logger.error`.

**Как работает функция**:
1. Функция пытается прочитать данные из CSV файла с использованием функции `read_csv_file` из модуля `src.utils.csv`.
2. Если данные успешно прочитаны, функция открывает JSON файл для записи и сохраняет в него данные в формате JSON с отступом 4.
3. В случае возникновения исключения в процессе чтения или записи файла, функция логирует информацию об ошибке с использованием `logger.error` и возвращает `None`.

**Примеры**:

```python
from pathlib import Path
csv_file = Path('data.csv')
json_file = Path('data.json')
json_data = csv_to_json(csv_file, json_file)
if json_data:
    print(json_data)