### Анализ кода `hypotez/src/utils/convertors/dict.py.md`

## Обзор

Модуль предоставляет утилиты для преобразования словарей Python и объектов SimpleNamespace в различные форматы.

## Подробнее

Этот модуль содержит функции, упрощающие преобразование данных между различными форматами, что полезно для интеграции с различными системами и сервисами. Он использует библиотеки `xml.etree.ElementTree` для работы с XML, `reportlab` для создания PDF, `pandas` для работы с табличными данными (CSV и XLS) и стандартные модули `json`, `codecs` и `collections`.

## Функции

### `_convert_to_dict`

```python
def _convert_to_dict(value: Any) -> Any:
    """Convert SimpleNamespace and lists to dict."""
    ...
```

**Назначение**:
Рекурсивно преобразует объекты `SimpleNamespace` и списки в словари.

**Параметры**:

*   `value` (Any): Значение для преобразования.

**Возвращает**:

*   `Any`: Преобразованное значение (словарь, список или исходное значение, если оно не требует преобразования).

**Как работает функция**:

1.  Если значение является экземпляром `SimpleNamespace`, преобразует его в словарь, рекурсивно применяя `_convert_to_dict` к каждому значению.
2.  Если значение является словарем, рекурсивно применяет `_convert_to_dict` к каждому значению в словаре.
3.  Если значение является списком, рекурсивно применяет `_convert_to_dict` к каждому элементу списка.
4.  В противном случае возвращает входное значение без изменений.

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
    """
    ...
```

**Назначение**:
Рекурсивно заменяет ключ в словаре или списке.

**Параметры**:

*   `data` (dict | list): Словарь или список, в котором производится замена ключа.
*   `old_key` (str): Ключ, который нужно заменить.
*   `new_key` (str): Новый ключ.

**Возвращает**:

*   `dict`: Обновленный словарь с замененными ключами.

**Как работает функция**:

1.  Если входные данные - словарь, перебирает его ключи. Если ключ совпадает с `old_key`, заменяет его на `new_key`. Затем рекурсивно вызывает `replace_key_in_dict` для каждого значения в словаре.
2.  Если это список, перебирает его элементы и рекурсивно вызывает `replace_key_in_dict` для каждого элемента.
3.  Возвращает измененный словарь или список.

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
Сохраняет данные из словаря в PDF-файл.

**Параметры**:

*   `data` (dict | SimpleNamespace): Словарь или объект `SimpleNamespace` для сохранения в PDF.
*   `file_path` (str | Path): Путь к выходному PDF-файлу.

**Как работает функция**:

1.  Преобразует объект `SimpleNamespace` в словарь, если входные данные являются объектом `SimpleNamespace`.
2.  Создает объект `canvas.Canvas` для создания PDF-файла.
3.  Устанавливает шрифт и размер шрифта.
4.  Перебирает элементы словаря и записывает их в PDF-файл в виде строк "ключ: значение".
5.  Если достигнут конец страницы, создает новую страницу.
6.  Сохраняет PDF-файл.

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

*   `data` (Dict[str, Any] | List[Any]): Данные для преобразования.

**Возвращает**:

*   `Any`: Преобразованные данные в виде `SimpleNamespace` или списка `SimpleNamespace`.

**Как работает функция**:

1.  Проверяет, является ли входное значение словарем или списком.
2.  Если это словарь, создает `SimpleNamespace` из него и рекурсивно преобразует все вложенные словари и списки в объекты `SimpleNamespace`.
3.  Если это список, рекурсивно преобразует каждый элемент списка в `SimpleNamespace`, если это возможно.
4.  Возвращает преобразованные данные.

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

*   `data` (Dict[str, Any]): Данные для преобразования в XML.
*   `encoding` (str, optional): Кодировка данных. По умолчанию `'UTF-8'`.

**Возвращает**:

*   `str`: XML-строка, представляющая входной словарь.

**Вызывает исключения**:

*   `Exception`: Если предоставлено более одного корневого узла.

**Как работает функция**:

1.  Определяет внутренние функции `_process_simple`, `_process_attr` и `_process_complex` для рекурсивной обработки данных.
2.  Создает XML-документ с помощью `xml.dom.minidom`.
3.  Проверяет, что в словаре `data` есть только один корневой элемент.
4.  Рекурсивно преобразует словарь в XML-структуру.
5.  Возвращает XML-строку, используя указанную кодировку.

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
Сохраняет данные из словаря или объекта `SimpleNamespace` в CSV-файл.

**Параметры**:

*   `data` (dict | SimpleNamespace): Данные для сохранения в CSV-файл.
*   `file_path` (str | Path): Путь к CSV-файлу.

**Возвращает**:

*   `bool`: `True`, если файл был успешно сохранен, `False` в противном случае.

**Как работает функция**:

1.  Передаёт входные данные и путь к файлу в функцию `save_csv_file`.
2.  Возвращает результат, возвращённый функцией `save_csv_file`.

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
Сохраняет данные из словаря или объекта `SimpleNamespace` в XLS-файл.

**Параметры**:

*   `data` (dict | SimpleNamespace): Данные для сохранения в XLS-файл.
*   `file_path` (str | Path): Путь к XLS-файлу.

**Возвращает**:

*   `bool`: `True`, если файл был успешно сохранен, `False` в противном случае.

**Как работает функция**:

1.  Передаёт входные данные и путь к файлу в функцию `save_xls_file`.
2.  Возвращает результат, возвращённый функцией `save_xls_file`.

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
Генерирует HTML-таблицу из словаря или объекта `SimpleNamespace`.

**Параметры**:

*   `data` (dict | SimpleNamespace): Данные для преобразования в HTML.
*   `encoding` (str, optional): Кодировка данных. По умолчанию 'UTF-8'.

**Возвращает**:

*   `str`: HTML-строка, представляющая входной словарь.

**Как работает функция**:

1.  Преобразует данные в словарь, если они представлены объектом `SimpleNamespace`.
2.  Определяет внутреннюю рекурсивную функцию `dict_to_html_table` для преобразования словаря в HTML-таблицу.
3.  Формирует HTML-структуру с таблицей, рекурсивно обрабатывая вложенные словари и списки.
4.  Возвращает полную HTML-страницу с таблицей внутри.

### Функция dict_to_html_table(data: dict, depth: int = 0) -> str

    *   **Назначение**:
    Рекурсивно преобразует словарь в HTML-таблицу.
    *   **Параметры**:
    *  `data` (dict): The dictionary data to convert.\
        *   `depth (int, optional)`: The depth of recursion, used for nested tables. Defaults to 0.\
    *  **Возвращает**:
    *   `str`: The HTML table as a string.
    *   **Как работает**:
    1. Создает  HTML-разметку для таблиц
    2. Проверяет входной параметр `data`. Если  является экземпляром словаря, функция проходит в цикле по всем парам ключ-значение в словаре.

## Константы

Отсутствуют.

## Примеры использования

```python
from src.utils.convertors.dict import dict2ns, dict2xml, dict2csv, dict2xls, dict2html
import types
from pathlib import Path

# Пример создания SimpleNamespace из словаря
data = {'name': 'John', 'age': 30}
ns = types.SimpleNamespace(**data)
print(ns.name, ns.age)

# Пример создания XML из словаря
data = {'root': {'item': 'value'}}
xml_string = dict2xml(data)
print(xml_string)

# Создание CSV из данных
#data_to_save = {'Sheet1': [{'column1': 'value1', 'column2': 'value2'}]}
#success = dict2csv(data_to_save, 'output.csv')

# Создание XLS из данных
#success = dict2xls(data_to_save, 'output.xls')

# Создание HTML из данных
data = {'name': 'John', 'age': 30}
html_string = dict2html(data)
#print(html_string)
```

## Зависимости

*   `json`: Для работы с JSON-данными.
*   `xml.etree.ElementTree`: Для работы с XML-данными.
*   `types.SimpleNamespace`: Для создания объектов `SimpleNamespace`.
*   `typing.Any, typing.Dict, typing.List`: Для аннотаций типов.
*   `pathlib.Path`: Для работы с путями к файлам.
*   `xml.dom.minidom`: Для создания XML-документов с отступами.
*   `reportlab.lib.pagesizes.A4`: Для определения размера страницы при создании PDF.
*   `reportlab.pdfgen.canvas`: Для создания PDF-файлов.
*   `hypotez.src.utils.xls.save_xls_file`: Для сохранения данных в Excel-файл.

## Взаимосвязи с другими частями проекта

*   Модуль `dict.py` предоставляет набор утилит для преобразования словарей в различные форматы и может использоваться в других частях проекта `hypotez`, где требуется преобразование данных между различными представлениями.
*   Он использует `save_xls_file` из `src.utils.xls`.