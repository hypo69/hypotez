# Модуль `dict`

## Обзор

Модуль `dict` содержит функции для рекурсивного преобразования словарей в объекты `SimpleNamespace` и обратно, а также для экспорта данных в различные форматы, такие как XML, CSV, JSON, XLS, HTML и PDF.

## Подробнее

Модуль предоставляет набор инструментов для работы со словарями и объектами `SimpleNamespace`, позволяя преобразовывать их между собой, а также экспортировать данные в различные форматы файлов. Это может быть полезно для сериализации данных, создания отчетов и обмена данными между различными системами.

## Функции

### `replace_key_in_dict`

```python
def replace_key_in_dict(data, old_key, new_key) -> dict:
    """
    Рекурсивно заменяет ключ в словаре или списке.

    Args:
        data (dict | list): Словарь или список, в котором происходит замена ключа.
        old_key (str): Ключ, который нужно заменить.
        new_key (str): Новый ключ.

    Returns:
        dict: Обновленный словарь с замененными ключами.

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

**Назначение**: Рекурсивно заменяет ключ `old_key` на `new_key` в словаре или списке.

**Параметры**:
- `data` (dict | list): Словарь или список, в котором необходимо произвести замену ключа.
- `old_key` (str): Ключ, который нужно заменить.
- `new_key` (str): Новый ключ.

**Возвращает**:
- `dict`: Обновленный словарь с замененными ключами.

**Как работает функция**:
Функция рекурсивно проходит по словарю или списку. Если текущий элемент является словарем, она перебирает его ключи и заменяет `old_key` на `new_key`. Если текущий элемент является списком, она перебирает его элементы и рекурсивно вызывает себя для каждого элемента.

**Примеры**:

```python
data = {"old_key": "value"}
updated_data = replace_key_in_dict(data, "old_key", "new_key")
print(updated_data)  # Вывод: {"new_key": "value"}

data = {"outer": {"old_key": "value"}}
updated_data = replace_key_in_dict(data, "old_key", "new_key")
print(updated_data)  # Вывод: {"outer": {"new_key": "value"}}

data = [{"old_key": "value1"}, {"old_key": "value2"}]
updated_data = replace_key_in_dict(data, "old_key", "new_key")
print(updated_data)  # Вывод: [{"new_key": "value1"}, {"new_key": "value2"}]

data = {"outer": [{"inner": {"old_key": "value"}}]}
updated_data = replace_key_in_dict(data, "old_key", "new_key")
print(updated_data)  # Вывод: {"outer": [{"inner": {"new_key": "value"}}]}
```

### `dict2pdf`

```python
def dict2pdf(data: dict | SimpleNamespace, file_path: str | Path):
    """
    Сохраняет данные словаря в PDF-файл.

    Args:
        data (dict | SimpleNamespace): Словарь для преобразования в PDF.
        file_path (str | Path): Путь к выходному PDF-файлу.
    """
```

**Назначение**: Сохраняет данные из словаря или объекта `SimpleNamespace` в PDF-файл.

**Параметры**:
- `data` (dict | SimpleNamespace): Словарь или объект `SimpleNamespace`, содержащий данные для сохранения в PDF.
- `file_path` (str | Path): Путь к выходному PDF-файлу.

**Как работает функция**:
Функция создает PDF-файл по указанному пути и записывает в него данные из словаря. Она перебирает элементы словаря и записывает каждый ключ и значение в PDF-файл. Если места на странице недостаточно, создается новая страница.

**Примеры**:

```python
data = {"name": "John", "age": 30, "city": "New York"}
dict2pdf(data, "data.pdf")
```

### `dict2ns`

```python
def dict2ns(data: Dict[str, Any] | List[Any]) -> Any:
    """
    Рекурсивно преобразует словари в SimpleNamespace.

    Args:
        data (Dict[str, Any] | List[Any]): Данные для преобразования.

    Returns:
        Any: Преобразованные данные в виде SimpleNamespace или списка SimpleNamespace.
    """
```

**Назначение**: Рекурсивно преобразует словарь или список словарей в объект `SimpleNamespace` или список объектов `SimpleNamespace`.

**Параметры**:
- `data` (Dict[str, Any] | List[Any]): Словарь или список для преобразования.

**Возвращает**:
- `Any`: Преобразованные данные в виде объекта `SimpleNamespace` или списка объектов `SimpleNamespace`.

**Как работает функция**:
Функция рекурсивно проходит по словарю или списку. Если текущий элемент является словарем, она преобразует его в объект `SimpleNamespace` и рекурсивно вызывает себя для каждого значения в словаре. Если текущий элемент является списком, она перебирает его элементы и рекурсивно вызывает себя для каждого элемента.

**Примеры**:

```python
data = {"name": "John", "age": 30, "city": "New York"}
ns = dict2ns(data)
print(ns.name)  # Вывод: John

data = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]
ns_list = dict2ns(data)
print(ns_list[0].name)  # Вывод: John
```

### `dict2xml`

```python
def dict2xml(data: Dict[str, Any], encoding: str = 'UTF-8') -> str:
    """
    Генерирует XML-строку из словаря.

    Args:
        data (Dict[str, Any]): Данные для преобразования в XML.
        encoding (str, optional): Кодировка данных. По умолчанию 'UTF-8'.

    Returns:
        str: XML-строка, представляющая входной словарь.

    Raises:
        Exception: Если предоставлено более одного корневого узла.
    """
```

**Назначение**: Генерирует XML-строку из словаря.

**Параметры**:
- `data` (Dict[str, Any]): Словарь, который необходимо преобразовать в XML.
- `encoding` (str, optional): Кодировка XML-документа. По умолчанию используется 'UTF-8'.

**Возвращает**:
- `str`: XML-строка, представляющая входной словарь.

**Вызывает исключения**:
- `Exception`: Если в словаре указано более одного корневого элемента.

**Как работает функция**:

Функция использует вспомогательные функции для обработки простых и сложных типов данных:
- `_process_simple`: создает XML-узел для простых типов данных (int, str).
- `_process_attr`: создает атрибуты для XML-элемента.
- `_process_complex`: создает узлы для сложных типов данных, таких как списки или словари.
- `_process`: генерирует XML DOM объект для тега и его значения.

Основная функция `dict2xml` создает XML-документ, преобразует входной словарь в XML-структуру и возвращает XML-строку.

**Внутренние функции**:

#### `_process_simple`

```python
def _process_simple(doc, tag, tag_value):
    """
    Создает узел для простых типов (int, str).

    Args:
        doc (xml.dom.minidom.Document): Объект XML-документа.
        tag (str): Имя тега для XML-элемента.
        tag_value (Any): Значение тега.

    Returns:
        xml.dom.minidom.Element: Узел, представляющий тег и значение.
    """
```

**Назначение**: Создает XML-узел для простых типов данных (int, str).

**Параметры**:
- `doc` (xml.dom.minidom.Document): Объект XML-документа.
- `tag` (str): Имя тега для XML-элемента.
- `tag_value` (Any): Значение тега.

**Возвращает**:
- `xml.dom.minidom.Element`: Узел, представляющий тег и значение.

**Как работает функция**:
Функция создает XML-элемент с заданным именем тега и добавляет текстовый узел со значением тега.

#### `_process_attr`

```python
def _process_attr(doc, attr_value: Dict[str, Any]):
    """
    Создает атрибуты для XML-элемента.

    Args:
        doc (xml.dom.minidom.Document): Объект XML-документа.
        attr_value (Dict[str, Any]): Словарь атрибутов.

    Returns:
        List[xml.dom.minidom.Attr]: Список атрибутов для XML-элемента.
    """
```

**Назначение**: Создает атрибуты для XML-элемента.

**Параметры**:
- `doc` (xml.dom.minidom.Document): Объект XML-документа.
- `attr_value` (Dict[str, Any]): Словарь атрибутов.

**Возвращает**:
- `List[xml.dom.minidom.Attr]: Список атрибутов для XML-элемента.

**Как работает функция**:
Функция перебирает элементы словаря атрибутов и создает XML-атрибут для каждого элемента.

#### `_process_complex`

```python
def _process_complex(doc, children):
    """
    Создает узлы для сложных типов, таких как списки или словари.

    Args:
        doc (xml.dom.minidom.Document): Объект XML-документа.
        children (List[Tuple[str, Any]]): Список пар тег-значение.

    Returns:
        Tuple[List[xml.dom.minidom.Element], List[xml.dom.minidom.Attr]]: Список дочерних узлов и атрибутов.
    """
```

**Назначение**: Создает узлы для сложных типов данных, таких как списки или словари.

**Параметры**:
- `doc` (xml.dom.minidom.Document): Объект XML-документа.
- `children` (List[Tuple[str, Any]]): Список пар тег-значение.

**Возвращает**:
- `Tuple[List[xml.dom.minidom.Element], List[xml.dom.minidom.Attr]]: Список дочерних узлов и атрибутов.

**Как работает функция**:
Функция перебирает список пар тег-значение. Если тег равен 'attrs', она вызывает функцию `_process_attr` для создания атрибутов. В противном случае она вызывает функцию `_process` для создания узлов.

#### `_process`

```python
def _process(doc, tag, tag_value):
    """
    Создает XML DOM объект для тега и его значения.

    Args:
        doc (xml.dom.minidom.Document): Объект XML-документа.
        tag (str): Имя тега для XML-элемента.
        tag_value (Any): Значение тега.

    Returns:
        xml.dom.minidom.Element | List[xml.dom.minidom.Element]: Узел или список узлов для тега и значения.
    """
```

**Назначение**: Создает XML DOM объект для тега и его значения.

**Параметры**:
- `doc` (xml.dom.minidom.Document): Объект XML-документа.
- `tag` (str): Имя тега для XML-элемента.
- `tag_value` (Any): Значение тега.

**Возвращает**:
- `xml.dom.minidom.Element | List[xml.dom.minidom.Element]: Узел или список узлов для тега и значения.

**Как работает функция**:
Функция определяет тип значения тега и вызывает соответствующую функцию для его обработки. Если значение является простым типом, она вызывает функцию `_process_simple`. Если значение является списком, она вызывает функцию `_process_complex`. Если значение является словарем, она создает XML-элемент и рекурсивно вызывает себя для каждого элемента словаря.

**Примеры**:

```python
data = {"name": "John", "age": 30, "city": "New York"}
xml_string = dict2xml(data)
print(xml_string)
```

### `dict2csv`

```python
def dict2csv(data: dict | SimpleNamespace, file_path: str | Path) -> bool:
    """
    Сохраняет данные словаря или SimpleNamespace в CSV-файл.

    Args:
        data (dict | SimpleNamespace): Данные для сохранения в CSV-файл.
        file_path (str | Path): Путь к CSV-файлу.

    Returns:
        bool: True, если файл был успешно сохранен, False в противном случае.
    """
```

**Назначение**: Сохраняет данные из словаря или объекта `SimpleNamespace` в CSV-файл.

**Параметры**:
- `data` (dict | SimpleNamespace): Словарь или объект `SimpleNamespace`, содержащий данные для сохранения в CSV-файл.
- `file_path` (str | Path): Путь к CSV-файлу.

**Возвращает**:
- `bool`: `True`, если файл был успешно сохранен, `False` в противном случае.

**Как работает функция**:
Функция вызывает функцию `save_csv_file` из модуля `src.utils.xls` для сохранения данных в CSV-файл.

**Примеры**:

```python
data = {"name": "John", "age": 30, "city": "New York"}
dict2csv(data, "data.csv")
```

### `dict2xls`

```python
def dict2xls(data: dict | SimpleNamespace, file_path: str | Path) -> bool:
    """
    Сохраняет данные словаря или SimpleNamespace в XLS-файл.

    Args:
        data (dict | SimpleNamespace): Данные для сохранения в XLS-файл.
        file_path (str | Path): Путь к XLS-файлу.

    Returns:
        bool: True, если файл был успешно сохранен, False в противном случае.
    """
```

**Назначение**: Сохраняет данные из словаря или объекта `SimpleNamespace` в XLS-файл.

**Параметры**:
- `data` (dict | SimpleNamespace): Словарь или объект `SimpleNamespace`, содержащий данные для сохранения в XLS-файл.
- `file_path` (str | Path): Путь к XLS-файлу.

**Возвращает**:
- `bool`: `True`, если файл был успешно сохранен, `False` в противном случае.

**Как работает функция**:
Функция вызывает функцию `save_xls_file` из модуля `src.utils.xls` для сохранения данных в XLS-файл.

**Примеры**:

```python
data = {"name": "John", "age": 30, "city": "New York"}
dict2xls(data, "data.xls")
```

### `dict2html`

```python
def dict2html(data: dict | SimpleNamespace, encoding: str = 'UTF-8') -> str:
    """
    Генерирует HTML-таблицу из словаря или объекта SimpleNamespace.

    Args:
        data (dict | SimpleNamespace): Данные для преобразования в HTML.
        encoding (str, optional): Кодировка данных. По умолчанию 'UTF-8'.

    Returns:
        str: HTML-строка, представляющая входной словарь.
    """
```

**Назначение**: Генерирует HTML-таблицу из словаря или объекта `SimpleNamespace`.

**Параметры**:
- `data` (dict | SimpleNamespace): Данные для преобразования в HTML.
- `encoding` (str, optional): Кодировка HTML-документа. По умолчанию используется 'UTF-8'.

**Возвращает**:
- `str`: HTML-строка, представляющая входной словарь.

**Как работает функция**:

Функция использует вспомогательную функцию `dict_to_html_table` для рекурсивного преобразования словаря в HTML-таблицу.
Основная функция `dict2html` создает HTML-документ, преобразует входной словарь в HTML-таблицу и возвращает HTML-строку.

**Внутренние функции**:

#### `dict_to_html_table`

```python
def dict_to_html_table(data: dict, depth: int = 0) -> str:
    """
    Рекурсивно преобразует словарь в HTML-таблицу.

    Args:
        data (dict): Данные словаря для преобразования.
        depth (int, optional): Глубина рекурсии, используется для вложенных таблиц. По умолчанию 0.

    Returns:
        str: HTML-таблица в виде строки.
    """
```

**Назначение**: Рекурсивно преобразует словарь в HTML-таблицу.

**Параметры**:
- `data` (dict): Данные словаря для преобразования.
- `depth` (int, optional): Глубина рекурсии, используется для вложенных таблиц. По умолчанию 0.

**Возвращает**:
- `str`: HTML-таблица в виде строки.

**Как работает функция**:
Функция рекурсивно проходит по словарю и создает HTML-таблицу. Если текущий элемент является словарем, она создает таблицу с ключами и значениями. Если текущий элемент является списком, она создает неупорядоченный список.

**Примеры**:

```python
data = {"name": "John", "age": 30, "city": "New York"}
html_string = dict2html(data)
print(html_string)
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

**Назначение**: Функция `example_json2xml` предоставляет пример использования функции `json2xml` (предположительно, определенной в другом месте), демонстрируя преобразование JSON-данных в XML-формат.

**Как работает функция**:
1. Определяются JSON-данные, представляющие информацию о товаре, включая его название на разных языках, цену, группу налоговых правил и категорию по умолчанию.
2. Вызывается функция `json2xml` с этими данными для преобразования JSON в XML.
3. Результат (XML-вывод) печатается на консоль.

**Примеры**:

Этот пример демонстрирует преобразование сложного JSON-объекта, содержащего вложенные структуры и атрибуты, в XML-формат. Результат будет XML-представлением предоставленных JSON-данных.