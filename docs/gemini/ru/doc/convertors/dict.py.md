### Анализ кода модуля `src/utils/convertors/dict.py`

## Обзор

Этот модуль предоставляет утилиты для работы со словарями и преобразования данных, позволяя преобразовывать словари в другие форматы данных, такие как XML, CSV, HTML, и объекты SimpleNamespace.

## Подробней

Модуль `src/utils/convertors/dict.py` содержит ряд функций, упрощающих преобразование данных между различными форматами, используя словари Python в качестве основы. Это полезно для работы с данными, поступающими из разных источников, и для их подготовки к дальнейшей обработке или хранению.

## Функции

### `replace_key_in_dict`

**Назначение**: Рекурсивно заменяет ключ в словаре или списке.

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

**Параметры**:

-   `data` (dict | list): Словарь или список, в котором нужно заменить ключ.
-   `old_key` (str): Ключ, который нужно заменить.
-   `new_key` (str): Новый ключ.

**Возвращает**:

-   `dict`: Обновленный словарь с замененными ключами.

**Как работает функция**:

1.  Проверяет, является ли входной параметр `data` словарем или списком.
2.  Если это словарь, перебирает все ключи словаря. Если текущий ключ совпадает с `old_key`, то заменяет его на `new_key`. Рекурсивно вызывает саму себя для обработки вложенных словарей и списков.
3.  Если это список, перебирает все элементы списка и рекурсивно вызывает саму себя для обработки каждого элемента.
4.  Возвращает обновленный словарь.

### `dict2pdf`

**Назначение**: Сохраняет данные словаря в PDF файл.

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

**Параметры**:

-   `data` (dict | SimpleNamespace): Словарь или объект `SimpleNamespace`, который нужно преобразовать в PDF.
-   `file_path` (str | Path): Путь к выходному PDF файлу.

**Возвращает**:

-   None

**Как работает функция**:

1.  Проверяет, является ли входной параметр `data` объектом `SimpleNamespace`. Если да, преобразует его в словарь, используя `data.__dict__`.
2.  Создает объект `canvas.Canvas` для создания PDF-файла, используя библиотеку `reportlab`.
3.  Устанавливает шрифт и размер страницы.
4.  Перебирает элементы словаря `data` и записывает их в PDF-файл в формате "ключ: значение".
5.  Создает новую страницу, если места на текущей странице недостаточно.
6.  Сохраняет PDF-файл.

### `dict2ns`

**Назначение**: Рекурсивно преобразует словари в объекты `SimpleNamespace`.

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

**Параметры**:

-   `data` (Dict[str, Any] | List[Any]): Данные для преобразования.

**Возвращает**:

-   `Any`: Преобразованные данные в виде объекта `SimpleNamespace` или списка объектов `SimpleNamespace`.

**Как работает функция**:

1.  Проверяет, является ли входной параметр `data` словарем или списком.
2.  Если это словарь, создает объект `SimpleNamespace` из этого словаря и рекурсивно вызывает саму себя для обработки значений словаря.
3.  Если это список, рекурсивно вызывает саму себя для обработки каждого элемента списка.
4.  В противном случае возвращает исходные данные без изменений.

### `dict2xml`

**Назначение**: Генерирует XML-строку из словаря.

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

**Параметры**:

-   `data` (Dict[str, Any]): Данные для преобразования в XML.
-   `encoding` (str, optional): Кодировка данных. По умолчанию 'UTF-8'.

**Возвращает**:

-   `str`: XML-строка, представляющая входной словарь.

**Вызывает исключения**:

-   `Exception`: Если предоставлено более одного корневого узла.

**Как работает функция**:

1.  Определяет внутренние функции:
    -   `_process_simple`: Создает узел для простых типов (int, str).
    -   `_process_attr`: Создает атрибуты для XML-элемента.
    -   `_process_complex`: Создает узлы для сложных типов, таких как списки и словари.
    -   `_process`: Обрабатывает тег и его значение, вызывая соответствующие функции для создания XML DOM объектов.
2.  Создает XML DOM документ.
3.  Обрабатывает данные, преобразуя их в XML DOM.
4.  Добавляет корневой элемент в документ.
5.  Возвращает XML-представление документа в виде строки.

### `dict2csv`

**Назначение**: Сохраняет словарь или объект SimpleNamespace в CSV файл.

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

**Параметры**:

-   `data` (dict | SimpleNamespace): Данные для сохранения в CSV файл.
-   `file_path` (str | Path): Путь к CSV файлу.

**Возвращает**:

-   `bool`: `True`, если файл успешно сохранен, `False` - в противном случае.

**Как работает функция**:

1.  Вызывает функцию `save_csv_file` из модуля `src.utils.csv` для сохранения данных в CSV файл.
2.  Возвращает результат, полученный от функции `save_csv_file`.

### `dict2xls`

**Назначение**: Сохраняет словарь или объект SimpleNamespace в XLS файл.

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

**Параметры**:

-   `data` (dict | SimpleNamespace): Данные для сохранения в XLS файл.
-   `file_path` (str | Path): Путь к XLS файлу.

**Возвращает**:

-   `bool`: `True`, если файл успешно сохранен, `False` - в противном случае.

**Как работает функция**:

1.  Вызывает функцию `save_xls_file` из модуля `src.utils.xls` для сохранения данных в XLS файл.
2.  Возвращает результат, полученный от функции `save_xls_file`.

### `dict2html`

**Назначение**: Генерирует HTML-таблицу из словаря или объекта SimpleNamespace.

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

**Параметры**:

-   `data` (dict | SimpleNamespace): Данные для преобразования в HTML.
-   `encoding` (str, optional): Кодировка данных. По умолчанию 'UTF-8'.

**Возвращает**:

-   `str`: HTML-строка, представляющая входной словарь.

**Как работает функция**:

1.  Определяет внутреннюю функцию `dict_to_html_table`, которая рекурсивно преобразует словарь в HTML-таблицу.
2.  Если входные данные - объект `SimpleNamespace`, преобразует его в словарь.
3.  Вызывает `dict_to_html_table` для преобразования словаря в HTML-таблицу.
4.  Формирует полную HTML-страницу, включая заголовок и тело с таблицей.
5.  Возвращает HTML-код в виде строки.

### `example_json2xml`

**Назначение**: Функция служит для примера использования функционала json2xml.

```python
def example_json2xml():

    # Example usage
    json_data = {
        "product": {
            "name": {
                "language": [
                    {
                        "@id": "1",
                        "#text": "Test Product"
                    },
                    {
                        "@id": "2",
                        "#text": "Test Product"
                    },
                    {
                        "@id": "3",
                        "#text": "Test Product"
                    }
                ]
            },
            "price": "10.00",
            "id_tax_rules_group": "13",
            "id_category_default": "2"
        }
    }

    xml_output = json2xml(json_data)
    print(xml_output)
```

**Параметры**:

-   Отсутствуют.

**Возвращает**:

-   Отсутствует.

**Как работает функция**:

1.  Определяет JSON данные для примера.
2.  Вызывает функцию `json2xml` для преобразования JSON данных в XML.
3.  Выводит результат преобразования в консоль.

## Переменные модуля

В данном модуле отсутствуют переменные, за исключением констант, определенных внутри функций (если бы они были).

## Пример использования

**Преобразование словаря в SimpleNamespace:**

```python
from src.utils.convertors.dict import dict2ns

data = {"name": "John", "age": 30}
ns_data = dict2ns(data)
print(ns_data.name)
```

**Преобразование словаря в XML:**

```python
from src.utils.convertors.dict import dict2xml

data = {"name": "John", "age": 30}
xml_data = dict2xml(data)
print(xml_data)
```

## Взаимосвязь с другими частями проекта

-   Модуль `src.utils.convertors.dict` используется другими модулями проекта для преобразования данных между различными форматами (JSON, XML, CSV, SimpleNamespace).
-   Зависит от модуля `src.utils.xls` для сохранения данных в формате Excel, от `src.logger.logger` для логирования.