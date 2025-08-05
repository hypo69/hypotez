# Модуль для работы с XLS-файлами

## Обзор

Модуль `src.utils.convertors.xls` предоставляет функции для чтения и записи данных в XLS-файлы. 

## Подробнее

Данный модуль предоставляет функции для работы с XLS-файлами:

- `xls2dict(xls_file: str | Path) -> dict | None`:  Читает XLS-файл и возвращает словарь данных.

## Функции

### `xls2dict`

**Назначение**: Функция считывает XLS-файл и возвращает словарь данных.

**Параметры**:

- `xls_file` (str | Path): Путь к XLS-файлу.

**Возвращает**:

- `dict | None`: Словарь с данными из XLS-файла или `None` в случае ошибки.

**Примеры**:

```python
from src.utils.convertors.xls import xls2dict

# Пример 1: Чтение файла с абсолютным путем
xls_file = '/path/to/your/file.xls'
data = xls2dict(xls_file)
print(data)

# Пример 2: Чтение файла с относительным путем
xls_file = 'data/file.xls'
data = xls2dict(xls_file)
print(data)
```

-------------------------------------------------------------------------------------
```markdown
# Модуль для работы с XLS-файлами

## Обзор

Модуль `src.utils.xls` предоставляет функции для работы с XLS-файлами. Он позволяет считывать данные из XLS-файлов и сохранять их в виде словаря.

## Подробнее

Данный модуль используется для обработки данных из XLS-файлов, предоставляя функциональность для чтения и записи.  Он используется в других частях проекта для преобразования данных из XLS-формата в удобный формат для дальнейшей обработки.

## Функции

### `read_xls_as_dict`

**Назначение**:  Функция считывает XLS-файл и возвращает словарь данных.

**Параметры**:

- `xls_file` (str | Path): Путь к XLS-файлу.

**Возвращает**:

- `dict | None`: Словарь с данными из XLS-файла или `None` в случае ошибки.

**Примеры**:

```python
from src.utils.xls import read_xls_as_dict

# Пример 1: Чтение файла с абсолютным путем
xls_file = '/path/to/your/file.xls'
data = read_xls_as_dict(xls_file)
print(data)

# Пример 2: Чтение файла с относительным путем
xls_file = 'data/file.xls'
data = read_xls_as_dict(xls_file)
print(data)
```

### `save_xls_file`

**Назначение**:  Функция сохраняет данные в XLS-файл.

**Параметры**:

- `data` (dict): Словарь с данными для сохранения.
- `file_path` (str | Path): Путь к XLS-файлу для сохранения.

**Возвращает**:

- `bool`: True, если сохранение прошло успешно, False - в случае ошибки.

**Примеры**:

```python
from src.utils.xls import save_xls_file

# Пример 1: Сохранение данных в новый файл
data = {'name': ['Иван', 'Петр'], 'age': [25, 30]}
file_path = 'data/new_file.xls'
result = save_xls_file(data, file_path)
print(f'Сохранение: {result}')

# Пример 2: Запись данных в существующий файл (перезапись)
data = {'name': ['Иван', 'Петр'], 'age': [25, 30]}
file_path = 'data/existing_file.xls'
result = save_xls_file(data, file_path)
print(f'Сохранение: {result}')
```

##  Примеры использования

```python
from src.utils.xls import read_xls_as_dict, save_xls_file

# Чтение данных из XLS-файла
data = read_xls_as_dict('data/my_data.xls')

# Обработка данных
# ...

# Сохранение обработанных данных в новый файл
save_xls_file(data, 'data/processed_data.xls')
```

-------------------------------------------------------------------------------------
```markdown
# Модуль для работы с XLS-файлами

## Обзор

Модуль `src.utils.convertors.xls` предоставляет функции для работы с XLS-файлами, в том числе для чтения и записи данных.

## Подробнее

Этот модуль используется для преобразования данных из XLS-формата в формат словаря. Он является частью проекта `hypotez` и интегрируется с другими модулями для обработки данных.

## Функции

### `xls2dict`

**Назначение**: Функция читает XLS-файл и возвращает словарь данных.

**Параметры**:

- `xls_file` (str | Path): Путь к XLS-файлу.

**Возвращает**:

- `dict | None`: Словарь с данными из XLS-файла или `None` в случае ошибки.

**Примеры**:

```python
from src.utils.convertors.xls import xls2dict

# Пример 1: Чтение файла с абсолютным путем
xls_file = '/path/to/your/file.xls'
data = xls2dict(xls_file)
print(data)

# Пример 2: Чтение файла с относительным путем
xls_file = 'data/file.xls'
data = xls2dict(xls_file)
print(data)
```

**Как работает функция**:

- Функция использует `read_xls_as_dict` для чтения данных из XLS-файла.
-  `read_xls_as_dict`  считывает содержимое файла, обрабатывает его и возвращает словарь, где ключи - это заголовки столбцов, а значения - соответствующие данные.

**Внутренние функции**:

- `read_xls_as_dict`:  Функция считывает XLS-файл и возвращает словарь данных. 

```python
def read_xls_as_dict(
    xls_file: str | Path,
) -> dict | None:
    """
    Читает XLS-файл и возвращает словарь данных.

    Args:
        xls_file (str | Path): Путь к XLS-файлу.

    Returns:
        dict | None: Словарь с данными из XLS-файла или `None` в случае ошибки.

    Raises:
        Exception: Если возникает ошибка при чтении файла.

    Example:
        >>> from pathlib import Path
        >>> xls_file = Path('example.xls')
        >>> content = read_xls_as_dict(xls_file)
        >>> if content:
        ...    print(f'File content: {content}')
        File content: {'column1': ['value1', 'value2'], 'column2': ['value3', 'value4']}
    """
    # ... 
```

**Примеры**:

```python
from src.utils.xls import read_xls_as_dict

# Пример 1: Чтение файла с абсолютным путем
xls_file = '/path/to/your/file.xls'
data = read_xls_as_dict(xls_file)
print(data)

# Пример 2: Чтение файла с относительным путем
xls_file = 'data/file.xls'
data = read_xls_as_dict(xls_file)
print(data)