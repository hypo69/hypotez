# Модуль для преобразования словарей и объектов SimpleNamespace
## Обзор

Модуль `src.utils.convertors.dict` предоставляет функции для рекурсивного преобразования между словарями и объектами `SimpleNamespace`, а также для экспорта данных в различные форматы, такие как XML, CSV, JSON, XLS, HTML и PDF.

## Подробнее

Этот модуль содержит набор функций для работы с данными, представленными в виде словарей и объектов `SimpleNamespace`. Он обеспечивает возможность преобразования данных между этими форматами, а также экспорта данных в различные форматы файлов.

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
```

**Назначение**: Рекурсивно заменяет ключ в словаре или списке.

**Параметры**:
- `data` (dict | list): Словарь или список, в котором производится замена ключа.
- `old_key` (str): Ключ, который нужно заменить.
- `new_key` (str): Новый ключ.

**Возвращает**:
- `dict`: Обновленный словарь с замененными ключами.

**Как работает функция**:
- Если `data` является словарем, функция проходит по всем ключам словаря.
- Если ключ совпадает с `old_key`, он заменяется на `new_key`.
- Если значение по ключу является словарем или списком, функция рекурсивно вызывает себя для этого значения.
- Если `data` является списком, функция проходит по всем элементам списка и рекурсивно вызывает себя для каждого элемента.

**Примеры**:

```python
data = {"old_key": "value"}
updated_data = replace_key_in_dict(data, "old_key", "new_key")
# updated_data становится {"new_key": "value"}

data = {"outer": {"old_key": "value"}}
updated_data = replace_key_in_dict(data, "old_key", "new_key")
# updated_data становится {"outer": {"new_key": "value"}}

data = [{"old_key": "value1"}, {"old_key": "value2"}]
updated_data = replace_key_in_dict(data, "old_key", "new_key")
# updated_data становится [{"new_key": "value1"}, {"new_key": "value2"}]

data = {"outer": [{"inner": {"old_key": "value"}}]}
updated_data = replace_key_in_dict(data, "old_key", "new_key")
# updated_data становится {"outer": [{"inner": {"new_key": "value"}}]}
```

### `dict2pdf`

```python
def dict2pdf(data: dict | SimpleNamespace, file_path: str | Path):
    """
    Save dictionary data to a PDF file.

    Args:
        data (dict | SimpleNamespace): The dictionary to convert to PDF.
        file_path (str | Path): Path to the output PDF file.
    """
```

**Назначение**: Сохраняет данные словаря в PDF-файл.

**Параметры**:
- `data` (dict | SimpleNamespace): Словарь, который нужно преобразовать в PDF.
- `file_path` (str | Path): Путь к выходному PDF-файлу.

**Как работает функция**:
- Если `data` является объектом `SimpleNamespace`, он преобразуется в словарь.
- Создается PDF-файл с использованием библиотеки `reportlab`.
- Для каждой пары "ключ-значение" в словаре создается строка, которая записывается в PDF-файл.
- Если места на странице недостаточно, создается новая страница.

**Примеры**:
```python
data = {"name": "John", "age": 30, "city": "New York"}
file_path = "data.pdf"
dict2pdf(data, file_path)
```

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
```

**Назначение**: Рекурсивно преобразует словари в объекты `SimpleNamespace`.

**Параметры**:
- `data` (Dict[str, Any] | List[Any]): Данные для преобразования.

**Возвращает**:
- `Any`: Преобразованные данные в виде объекта `SimpleNamespace` или списка объектов `SimpleNamespace`.

**Как работает функция**:
- Если `data` является словарем, функция проходит по всем элементам словаря.
- Если значение является словарем, функция рекурсивно вызывает себя для этого значения.
- Если значение является списком, функция преобразует каждый элемент списка в `SimpleNamespace`, если это возможно.
- Если `data` является списком, функция преобразует каждый элемент списка в `SimpleNamespace`, если это возможно.

**Примеры**:
```python
data = {"name": "John", "age": 30, "city": "New York"}
ns_data = dict2ns(data)
# ns_data будет SimpleNamespace(name='John', age=30, city='New York')

data = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]
ns_data = dict2ns(data)
# ns_data будет [SimpleNamespace(name='John', age=30), SimpleNamespace(name='Jane', age=25)]
```

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
```

**Назначение**: Генерирует XML-строку из словаря.

**Параметры**:
- `data` (Dict[str, Any]): Данные для преобразования в XML.
- `encoding` (str, optional): Кодировка данных. По умолчанию 'UTF-8'.

**Возвращает**:
- `str`: XML-строка, представляющая входной словарь.

**Вызывает исключения**:
- `Exception`: Если предоставлено более одного корневого узла.

**Как работает функция**:

Функция `dict2xml` преобразует словарь в XML-строку. Она использует внутренние функции для обработки простых типов (int, str), атрибутов XML и сложных типов (списки, словари). Основные шаги:

1.  Определяются внутренние функции `_process_simple`, `_process_attr`, `_process_complex` и `_process` для рекурсивной обработки данных.
2.  Создается XML-документ с помощью `getDOMImplementation().createDocument()`.
3.  Проверяется, что в словаре `data` только один корневой узел.
4.  Вызывается функция `_process_complex` для преобразования данных словаря в XML-элементы.
5.  Добавляется корневой элемент в XML-документ.
6.  XML-документ преобразуется в строку с указанной кодировкой.

**Внутренние функции**:

*   `_process_simple(doc, tag, tag_value)`:
    *   Создает XML-узел для простых типов данных (int, str).
    *   **Параметры**:
        *   `doc` (xml.dom.minidom.Document): XML-документ.
        *   `tag` (str): Имя тега.
        *   `tag_value` (Any): Значение тега.
    *   **Возвращает**: XML-узел.
*   `_process_attr(doc, attr_value: Dict[str, Any])`:
    *   Создает атрибуты для XML-элемента.
    *   **Параметры**:
        *   `doc` (xml.dom.minidom.Document): XML-документ.
        *   `attr_value` (Dict[str, Any]): Словарь атрибутов.
    *   **Возвращает**: Список атрибутов.
*   `_process_complex(doc, children)`:
    *   Создает узлы для сложных типов данных (списки, словари).
    *   **Параметры**:
        *   `doc` (xml.dom.minidom.Document): XML-документ.
        *   `children` (List[Tuple[str, Any]]): Список пар тег-значение.
    *   **Возвращает**: Список узлов и атрибутов.
*   `_process(doc, tag, tag_value)`:
    *   Генерирует XML DOM объект для тега и его значения.
    *   **Параметры**:
        *   `doc` (xml.dom.minidom.Document): XML-документ.
        *   `tag` (str): Имя тега.
        *   `tag_value` (Any): Значение тега.
    *   **Возвращает**: XML-узел или список узлов.

**Примеры**:

```python
data = {"root": {"name": "John", "age": 30}}
xml_string = dict2xml(data)
# xml_string будет строкой, представляющей XML-документ
```

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
```

**Назначение**: Сохраняет данные словаря или `SimpleNamespace` в CSV-файл.

**Параметры**:
- `data` (dict | SimpleNamespace): Данные для сохранения в CSV-файл.
- `file_path` (str | Path): Путь к CSV-файлу.

**Возвращает**:
- `bool`: `True`, если файл был успешно сохранен, `False` в противном случае.

**Как работает функция**:
- Вызывает функцию `save_csv_file` из модуля `src.utils.csv` для сохранения данных в CSV-файл.

**Примеры**:
```python
data = {"name": "John", "age": 30, "city": "New York"}
file_path = "data.csv"
result = dict2csv(data, file_path)
# result будет True, если файл был успешно сохранен
```

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
```

**Назначение**: Сохраняет данные словаря или `SimpleNamespace` в XLS-файл.

**Параметры**:
- `data` (dict | SimpleNamespace): Данные для сохранения в XLS-файл.
- `file_path` (str | Path): Путь к XLS-файлу.

**Возвращает**:
- `bool`: `True`, если файл был успешно сохранен, `False` в противном случае.

**Как работает функция**:
- Вызывает функцию `save_xls_file` из модуля `src.utils.xls` для сохранения данных в XLS-файл.

**Примеры**:
```python
data = {"name": "John", "age": 30, "city": "New York"}
file_path = "data.xls"
result = dict2xls(data, file_path)
# result будет True, если файл был успешно сохранен
```

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
```

**Назначение**: Генерирует HTML-строку таблицы из словаря или объекта `SimpleNamespace`.

**Параметры**:
- `data` (dict | SimpleNamespace): Данные для преобразования в HTML.
- `encoding` (str, optional): Кодировка данных. По умолчанию 'UTF-8'.

**Возвращает**:
- `str`: HTML-строка, представляющая входной словарь.

**Как работает функция**:

Функция `dict2html` преобразует словарь или объект `SimpleNamespace` в HTML-таблицу. Она использует внутреннюю функцию `dict_to_html_table` для рекурсивного преобразования данных в HTML-таблицу. Основные шаги:

1.  Определяется внутренняя функция `dict_to_html_table` для рекурсивного преобразования данных в HTML-таблицу.
2.  Если `data` является объектом `SimpleNamespace`, он преобразуется в словарь.
3.  Вызывается функция `dict_to_html_table` для преобразования данных словаря в HTML-таблицу.
4.  HTML-таблица оборачивается в HTML-документ с указанной кодировкой.

**Внутренние функции**:

*   `dict_to_html_table(data: dict, depth: int = 0)`:
    *   Рекурсивно преобразует словарь в HTML-таблицу.
    *   **Параметры**:
        *   `data` (dict): Данные словаря для преобразования.
        *   `depth` (int, optional): Глубина рекурсии, используется для вложенных таблиц. По умолчанию 0.
    *   **Возвращает**: HTML-таблица в виде строки.

**Примеры**:

```python
data = {"name": "John", "age": 30, "city": "New York"}
html_string = dict2html(data)
# html_string будет строкой, представляющей HTML-документ с таблицей
```

### `example_json2xml`

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

**Назначение**: Приводит пример использования функции `json2xml`. <в оригинальном коде нет функции `json2xml`. Вероятно, она была удалена или переименована. Я заменил ее на `dict2xml`>

**Как работает функция**:
1.  Определяет словарь `json_data`, содержащий структуру данных о продукте.
2.  Вызывает функцию `dict2xml` <в оригинальном коде была вызвана несуществующая функция `json2xml`. Я заменил ее на `dict2xml`>, передавая в нее `json_data` для преобразования в XML-формат.
3.  Выводит полученную XML-строку в консоль.

**Примеры**:
```python
example_json2xml()