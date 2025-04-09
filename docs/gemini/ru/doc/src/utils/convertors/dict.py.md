# Модуль `src.utils.convertors.dict`

## Обзор

Модуль предназначен для преобразования данных между форматами `dict` и `SimpleNamespace`, а также для экспорта данных в различные форматы, такие как `XML`, `CSV`, `JSON`, `XLS`, `HTML` и `PDF`.

## Подробней

Модуль содержит набор функций, которые облегчают преобразование и экспорт данных из словарей `dict` и объектов `SimpleNamespace` в различные форматы. Он включает функции для рекурсивного преобразования словарей в объекты `SimpleNamespace` и обратно, а также функции для сохранения данных в форматы `CSV`, `JSON`, `XLS`, `HTML` и `PDF`. Модуль использует различные библиотеки, такие как `json`, `xml.etree.ElementTree`, `reportlab` и `src.utils.xls`, чтобы обеспечить поддержку различных форматов экспорта.

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
- `data` (dict | list): Словарь или список, в котором происходит замена ключа.
- `old_key` (str): Ключ, который нужно заменить.
- `new_key` (str): Новый ключ.

**Возвращает**:
- `dict`: Обновленный словарь с замененными ключами.

**Как работает функция**:

1.  **Проверка типа данных**: Функция начинает с проверки типа входных данных `data`.
2.  **Обработка словаря**: Если `data` является словарем, функция итерируется по его ключам.
    *   Если текущий ключ совпадает с `old_key`, он заменяется на `new_key` с помощью методов `pop` и присваивания.
    *   Если значение по текущему ключу является словарем или списком, функция рекурсивно вызывает себя для этого значения.
3.  **Обработка списка**: Если `data` является списком, функция итерируется по его элементам.
    *   Для каждого элемента функция рекурсивно вызывает себя.
4.  **Возврат обновленных данных**: После обработки всех элементов или ключей функция возвращает обновленный словарь `data`.

**ASCII flowchart**:

```
   Начало
     ↓
   Проверка типа data (dict/list)
     ├── dict: Итерация по ключам
     │   ├── Ключ == old_key: Замена ключа
     │   ├── Значение - dict/list: Рекурсивный вызов
     │   └── Конец итерации
     └── list: Итерация по элементам
         └── Рекурсивный вызов для элемента
     ↓
   Возврат обновленных данных
```

**Примеры**:

```python
# Пример 1: Простой словарь
data = {"old_key": "value"}
updated_data = replace_key_in_dict(data, "old_key", "new_key")
# updated_data становится {"new_key": "value"}

# Пример 2: Вложенный словарь
data = {"outer": {"old_key": "value"}}
updated_data = replace_key_in_dict(data, "old_key", "new_key")
# updated_data становится {"outer": {"new_key": "value"}}

# Пример 3: Список словарей
data = [{"old_key": "value1"}, {"old_key": "value2"}]
updated_data = replace_key_in_dict(data, "old_key", "new_key")
# updated_data становится [{"new_key": "value1"}, {"new_key": "value2"}]

# Пример 4: Смешанная вложенная структура со списками и словарями
data = {"outer": [{"inner": {"old_key": "value"}}]}
updated_data = replace_key_in_dict(data, "old_key", "new_key")
# updated_data становится {"outer": [{"inner": {"new_key": "value"}}]}
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
- `Any`: Преобразованные данные в виде `SimpleNamespace` или списка `SimpleNamespace`.

**Как работает функция**:

1.  **Проверка типа данных**: Функция начинает с проверки типа входных данных `data`.
2.  **Обработка словаря**: Если `data` является словарем, функция итерируется по его элементам.
    *   Если значение является словарем, функция рекурсивно вызывает себя для этого значения.
    *   Если значение является списком, функция преобразует каждый элемент списка, который является словарем, в `SimpleNamespace` и оставляет остальные элементы без изменений.
    *   Возвращает `SimpleNamespace`, созданный из словаря `data`.
3.  **Обработка списка**: Если `data` является списком, функция преобразует каждый элемент списка, который является словарем, в `SimpleNamespace` и оставляет остальные элементы без изменений.
    *   Возвращает список преобразованных элементов.
4.  **Возврат неизмененных данных**: Если `data` не является ни словарем, ни списком, функция возвращает его без изменений.

**ASCII flowchart**:

```
   Начало
     ↓
   Проверка типа data (dict/list)
     ├── dict: Итерация по элементам
     │   ├── Значение - dict: Рекурсивный вызов
     │   ├── Значение - list: Преобразование элементов списка (dict -> SimpleNamespace)
     │   └── Конец итерации
     │   ↓
     │   Возврат SimpleNamespace(**data)
     └── list: Преобразование элементов списка (dict -> SimpleNamespace)
         ↓
         Возврат списка
     ↓
   Возврат неизмененных данных
```

**Примеры**:

```python
data = {'a': 1, 'b': {'c': 2, 'd': 3}, 'e': [4, {'f': 5}]}
ns = dict2ns(data)
print(ns.a)  # Вывод: 1
print(ns.b.c) # Вывод: 2
print(ns.e[0]) # Вывод: 4
print(ns.e[1].f) # Вывод: 5
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

**Назначение**: Генерирует XML строку из словаря.

**Параметры**:
- `data` (Dict[str, Any]): Данные для преобразования в XML.
- `encoding` (str, optional): Кодировка данных. По умолчанию 'UTF-8'.

**Возвращает**:
- `str`: XML строка, представляющая входной словарь.

**Вызывает исключения**:
- `Exception`: Если предоставлено более одного корневого узла.

**Как работает функция**:

1.  **Внутренние функции**: Функция использует несколько внутренних функций для обработки различных типов данных и создания XML-элементов.
    *   `_process_simple`: Создает узел для простых типов данных (int, str).
    *   `_process_attr`: Создает атрибуты для XML-элемента.
    *   `_process_complex`: Создает узлы для сложных типов данных, таких как списки или словари.
    *   `_process`: Генерирует XML DOM объект для тега и его значения.
2.  **Создание XML документа**: Функция создает XML документ с помощью `getDOMImplementation().createDocument()`.
3.  **Обработка данных**: Функция вызывает `_process_complex` для обработки входных данных и создания корневого элемента XML.
4.  **Добавление корневого элемента**: Функция добавляет корневой элемент в XML документ.
5.  **Преобразование в строку**: Функция преобразует XML документ в строку с указанной кодировкой.

**ASCII flowchart**:

```
   Начало
     ↓
   Определение внутренних функций (_process_simple, _process_attr, _process_complex, _process)
     ↓
   Создание XML документа
     ↓
   Обработка данных с помощью _process_complex
     ↓
   Добавление корневого элемента в XML документ
     ↓
   Преобразование XML документа в строку
     ↓
   Возврат XML строки
```

**Примеры**:

```python
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

xml_output = dict2xml(json_data)
print(xml_output)
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

**Назначение**: Сохраняет данные из словаря или `SimpleNamespace` в CSV файл.

**Параметры**:
- `data` (dict | SimpleNamespace): Данные для сохранения в CSV файл.
- `file_path` (str | Path): Путь к CSV файлу.

**Возвращает**:
- `bool`: `True`, если файл был успешно сохранен, `False` в противном случае.

**Как работает функция**:

1.  **Вызов функции сохранения**: Функция вызывает функцию `save_csv_file` из модуля <укажите модуль, если он существует в коде, иначе: "из другого модуля">, передавая ей данные и путь к файлу.
2.  **Возврат результата**: Функция возвращает результат вызова `save_csv_file`, который указывает, был ли файл успешно сохранен.

**ASCII flowchart**:

```
   Начало
     ↓
   Вызов save_csv_file(data, file_path)
     ↓
   Возврат результата вызова save_csv_file
```

**Примеры**:

```python
data = {'a': 1, 'b': 2, 'c': 3}
file_path = 'data.csv'
result = dict2csv(data, file_path)
print(result)
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

**Назначение**: Сохраняет данные из словаря или `SimpleNamespace` в XLS файл.

**Параметры**:
- `data` (dict | SimpleNamespace): Данные для сохранения в XLS файл.
- `file_path` (str | Path): Путь к XLS файлу.

**Возвращает**:
- `bool`: `True`, если файл был успешно сохранен, `False` в противном случае.

**Как работает функция**:

1.  **Вызов функции сохранения**: Функция вызывает функцию `save_xls_file` из модуля `src.utils.xls`, передавая ей данные и путь к файлу.
2.  **Возврат результата**: Функция возвращает результат вызова `save_xls_file`, который указывает, был ли файл успешно сохранен.

**ASCII flowchart**:

```
   Начало
     ↓
   Вызов save_xls_file(data, file_path)
     ↓
   Возврат результата вызова save_xls_file
```

**Примеры**:

```python
data = {'a': 1, 'b': 2, 'c': 3}
file_path = 'data.xls'
result = dict2xls(data, file_path)
print(result)
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

**Назначение**: Генерирует HTML строку таблицы из словаря или объекта `SimpleNamespace`.

**Параметры**:
- `data` (dict | SimpleNamespace): Данные для преобразования в HTML.
- `encoding` (str, optional): Кодировка данных. По умолчанию 'UTF-8'.

**Возвращает**:
- `str`: HTML строка, представляющая входной словарь.

**Внутренние функции**:

#### `dict_to_html_table`

```python
def dict_to_html_table(data: dict, depth: int = 0) -> str:
    """
    Recursively convert dictionary to HTML table.

    Args:
        data (dict): The dictionary data to convert.
        depth (int, optional): The depth of recursion, used for nested tables. Defaults to 0.

    Returns:
        str: The HTML table as a string.
    """
```

**Назначение**: Рекурсивно преобразует словарь в HTML таблицу.

**Параметры**:
- `data` (dict): Данные словаря для преобразования.
- `depth` (int, optional): Глубина рекурсии, используется для вложенных таблиц. По умолчанию 0.

**Возвращает**:
- `str`: HTML таблица в виде строки.

**Как работает функция `dict_to_html_table`**:

1.  **Инициализация HTML**: Функция начинает с инициализации списка `html`, который будет содержать HTML код таблицы.
2.  **Обработка словаря**: Если `data` является словарем, функция итерируется по его элементам.
    *   Для каждого элемента создается строка таблицы (`<tr>`).
    *   В первую ячейку (`<td>`) добавляется ключ элемента, обернутый в тег `<strong>`.
    *   Если значение является словарем, функция рекурсивно вызывает себя для этого значения и добавляет результат во вторую ячейку.
    *   Если значение является списком, функция создает неупорядоченный список (`<ul>`) и добавляет каждый элемент списка в виде элемента списка (`<li>`).
    *   Если значение не является ни словарем, ни списком, оно добавляется во вторую ячейку.
3.  **Обработка не-словаря**: Если `data` не является словарем, функция создает строку таблицы с одной ячейкой, содержащей данные.
4.  **Завершение HTML**: Функция добавляет закрывающий тег `</table>` и объединяет все элементы списка `html` в одну строку.

**Как работает функция `dict2html`**:

1.  **Преобразование в словарь**: Если входные данные являются объектом `SimpleNamespace`, они преобразуются в словарь.
2.  **Создание HTML таблицы**: Функция вызывает `dict_to_html_table` для преобразования данных в HTML таблицу.
3.  **Создание HTML документа**: Функция создает HTML документ, включая мета-тег с указанной кодировкой и добавляет HTML таблицу в тело документа.

**ASCII flowchart**:

```
   Начало (dict2html)
     ↓
   Преобразование SimpleNamespace в dict (если необходимо)
     ↓
   Вызов dict_to_html_table(data)
     ↓
   Создание HTML документа с таблицей
     ↓
   Возврат HTML строки
```

**Примеры**:

```python
data = {'a': 1, 'b': {'c': 2, 'd': 3}, 'e': [4, 5, 6]}
html = dict2html(data)
print(html)
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

**Назначение**: Функция `example_json2xml` предназначена для демонстрации использования функции `json2xml`.

**Как работает функция**:

1.  **Определение примера данных**: Внутри функции определен пример словаря `json_data`, который имитирует структуру JSON данных о продукте. Этот словарь содержит информацию о названии продукта (с указанием языка), цене, группе налоговых правил и категории по умолчанию.
2.  **Преобразование JSON в XML**: Функция вызывает функцию `json2xml`, передавая ей `json_data` для преобразования в XML формат.
3.  **Вывод результата**: Результат преобразования, который представляет собой XML строку, выводится в консоль с помощью `print(xml_output)`.

**Примеры**:

```python
example_json2xml()