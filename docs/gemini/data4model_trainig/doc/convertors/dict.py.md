### Анализ кода модуля `hypotez/src/utils/convertors/dict.py`

## Обзор

Этот модуль предоставляет утилиты для преобразования между словарями и другими форматами данных, такими как SimpleNamespace, XML, CSV, XLS и HTML.

## Подробнее

Модуль содержит функции для преобразования словарей Python в различные форматы, облегчая интеграцию и обработку данных в разных частях проекта.

## Функции

### `replace_key_in_dict`

```python
def replace_key_in_dict(data, old_key, new_key) -> dict:
    """
    Recursively replaces a key in a dictionary or list.
    
    Args:
        data (dict | list): The dictionary or list where key replacement occurs.
        old_key (str): The key to be replaced.
        new_key (str): The new key.
    
    Returns:
        dict: The updated dictionary with replaced keys.

    Example Usage:

        replace_key_in_json(data, 'name', 'category_name')

        # Example 1: Simple dictionary
        data = {"old_key": "value"}
        updated_data = replace_key_in_json(data, "old_key", "new_key")
        # updated_data becomes {"new_key": "value"}

        # Example 2: Nested dictionary
        data = {"outer": {"old_key": "value"}}
        updated_data = replace_key_in_json(data, "old_key", "new_key")
        # updated_data becomes {"outer": {"new_key": "value"}}

        # Example 3: List of dictionaries
        data = [{"old_key": "value1"}, {"old_key": "value2"}]
        updated_data = replace_key_in_json(data, "old_key", "new_key")
        # updated_data becomes [{"new_key": "value1"}, {"new_key": "value2"}]

        # Example 4: Mixed nested structure with lists and dictionaries
        data = {"outer": [{"inner": {"old_key": "value"}}]}
        updated_data = replace_key_in_json(data, "old_key", "new_key")
        # updated_data becomes {"outer": [{"inner": {"new_key": "value"}}]}

    """
    ...
```

**Назначение**:
Рекурсивно заменяет ключ в словаре или списке.

**Параметры**:
- `data` (dict | list): Словарь или список, где происходит замена ключа.
- `old_key` (str): Ключ, который нужно заменить.
- `new_key` (str): Новый ключ.

**Возвращает**:
- `dict`: Обновленный словарь с замененными ключами.

**Как работает функция**:
1. Если `data` является словарем, функция перебирает ключи словаря и заменяет `old_key` на `new_key`. Если значение по ключу является словарем или списком, функция рекурсивно вызывает себя для этого значения.
2. Если `data` является списком, функция перебирает элементы списка и рекурсивно вызывает себя для каждого элемента.
3. Возвращает обновленный словарь.

**Примеры**:

```python
data = {"old_key": "value"}
updated_data = replace_key_in_dict(data, "old_key", "new_key")
print(updated_data)  # Вывод: {'new_key': 'value'}
```

### `dict2pdf`

```python
def dict2pdf(data: Any, file_path: str | Path) -> None:
    """
    Save dictionary data to a PDF file.

    Args:
        data (dict | SimpleNamespace): The dictionary to convert to PDF.
        file_path (str | Path): Path to the output PDF file.
    """
    ...
```

**Назначение**:
Сохраняет данные словаря в PDF-файл.

**Параметры**:
- `data` (dict | SimpleNamespace): Словарь или SimpleNamespace для преобразования в PDF.
- `file_path` (str | Path): Путь к выходному PDF-файлу.

**Возвращает**:
- None

**Как работает функция**:
1. Если входные данные являются экземпляром `SimpleNamespace`, они преобразуются в словарь.
2. Создается объект `canvas.Canvas` для генерации PDF.
3. Устанавливается шрифт по умолчанию.
4. Перебираются пары ключ-значение в словаре и записываются в PDF, при необходимости добавляются новые страницы для размещения всего содержимого.

### `dict2ns`

```python
def dict2ns(data: Dict[str, Any] | List[Any]) -> Any:
    """
    Recursively convert dictionaries to SimpleNamespace.

    Args:
        data (Dict[str, Any] | List[Any]): The data to convert.

    Returns:
        Any: Converted data as a SimpleNamespace or a list of SimpleNamespace.
    """
    ...
```

**Назначение**:
Рекурсивно преобразует словари в объекты `SimpleNamespace`.

**Параметры**:
- `data` (Dict[str, Any] | List[Any]): Данные для преобразования.

**Возвращает**:
- `Any`: Преобразованные данные в виде `SimpleNamespace` или списка `SimpleNamespace`.

**Как работает функция**:
1. Проверяет, является ли входные данные словарем или списком.
2. Если это словарь, функция рекурсивно преобразует каждое значение, которое является словарем, в `SimpleNamespace`.
3. Если это список, функция рекурсивно преобразует каждый элемент списка, который является словарем, в `SimpleNamespace`.
4. Если это не словарь и не список, возвращает параметр как есть.

### `dict2xml`

```python
def dict2xml(data: Dict[str, Any], encoding: str = 'UTF-8') -> str:
    """
    Generate an XML string from a dictionary.

    Args:
        data (Dict[str, Any]): The data to convert to XML.
        encoding (str, optional): Data encoding. Defaults to 'UTF-8'.

    Returns:
        str: The XML string representing the input dictionary.

    Raises:
        Exception: If more than one root node is provided.
    """
    ...
```

**Назначение**:
Генерирует XML-строку из словаря.

**Параметры**:
- `data` (Dict[str, Any]): Данные для преобразования в XML.
- `encoding` (str, optional): Кодировка данных. По умолчанию 'UTF-8'.

**Возвращает**:
- `str`: XML-строка, представляющая входной словарь.

**Вызывает исключения**:
- `Exception`: Если предоставлено больше одного корневого узла.

**Как работает функция**:
1. Использует внутренние функции `_process_simple`, `_process_attr`, `_process_complex` и `_process` для рекурсивного преобразования словаря в XML DOM.
2. Присоединяет корневой элемент к XML-документу.
3. Возвращает XML-строку.

### `dict2csv`

```python
def dict2csv(data: dict | SimpleNamespace, file_path: str | Path) -> bool:
    """
    Save dictionary or SimpleNamespace data to a CSV file.

    Args:
        data (dict | SimpleNamespace): The data to save to a CSV file.
        file_path (str | Path): Path to the CSV file.

    Returns:
        bool: True if the file was saved successfully, False otherwise.
    """
    ...
```

**Назначение**:
Сохраняет данные словаря или SimpleNamespace в CSV-файл.

**Параметры**:
- `data` (dict | SimpleNamespace): Данные для сохранения в CSV-файл.
- `file_path` (str | Path): Путь к CSV-файлу.

**Возвращает**:
- `bool`: True, если файл был успешно сохранен, False в противном случае.

**Как работает функция**:
1. Вызывает функцию `save_csv_file` для сохранения данных в CSV-файл.

### `dict2xls`

```python
def dict2xls(data: dict | SimpleNamespace, file_path: str | Path) -> bool:
    """
    Save dictionary or SimpleNamespace data to an XLS file.

    Args:
        data (dict | SimpleNamespace): The data to save to an XLS file.
        file_path (str | Path): Path to the XLS file.

    Returns:
        bool: True if the file was saved successfully, False otherwise.
    """
    ...
```

**Назначение**:
Сохраняет данные словаря или SimpleNamespace в XLS-файл.

**Параметры**:
- `data` (dict | SimpleNamespace): Данные для сохранения в XLS-файл.
- `file_path` (str | Path): Путь к XLS-файлу.

**Возвращает**:
- `bool`: True, если файл был успешно сохранен, False в противном случае.

**Как работает функция**:
1.  Вызывает функцию `save_xls_file` для сохранения данных в XLS-файл.

### `dict2html`

```python
def dict2html(data: dict | SimpleNamespace, encoding: str = 'UTF-8') -> str:
    """
    Generate an HTML table string from a dictionary or SimpleNamespace object.

    Args:
        data (dict | SimpleNamespace): The data to convert to HTML.
        encoding (str, optional): Data encoding. Defaults to 'UTF-8'.

    Returns:
        str: The HTML string representing the input dictionary.
    """
    ...
```

**Назначение**:
Генерирует HTML-таблицу из словаря или объекта SimpleNamespace.

**Параметры**:
- `data` (dict | SimpleNamespace): Данные для преобразования в HTML.
- `encoding` (str, optional): Кодировка данных. По умолчанию 'UTF-8'.

**Возвращает**:
- `str`: HTML-строка, представляющая входной словарь.

**Как работает функция**:
1. Определяет внутреннюю функцию `dict_to_html_table`, которая рекурсивно преобразует словарь в HTML-таблицу.
2. Если входные данные являются SimpleNamespace, преобразует их в словарь.
3. Преобразует данные в HTML-таблицу, используя рекурсивную функцию `dict_to_html_table`.
4. Оборачивает HTML-таблицу в базовый HTML-документ.

## Переменные

Отсутствуют

## Запуск

Для использования этого модуля необходимо установить библиотеки `pandas`, `xlwt`, `reportlab` и `src.logger.logger`. Также необходимо установить `WeasyPrint`.

Пример использования:

```python
from src.utils.convertors.dict import dict2ns, dict2xml, dict2csv, dict2xls, dict2html
from pathlib import Path
from types import SimpleNamespace

# Преобразование словаря в SimpleNamespace
data = {"name": "John", "age": 30}
ns = dict2ns(data)

# Преобразование словаря в XML
data = {"root": {"item": "value"}}
xml_string = dict2xml(data)

# Преобразование словаря в CSV
data = {"name": "John", "age": 30}
dict2csv(data, "data.csv")

# Преобразование словаря в XLS
data = {"name": "John", "age": 30}
dict2xls(data, "data.xls")

# Преобразование словаря в HTML
html_string = dict2html(data)
print(html_string)