# Модуль для преобразования XML и JSON данных
## Обзор

Модуль `xml_json_convertor.py` предоставляет утилиты для преобразования данных между форматами XML и JSON. Он включает функции для разбора XML-строк и преобразования деревьев элементов XML в представления словарей, а также для преобразования словарей JSON в XML.

## Подробней

Этот модуль предоставляет набор функций для преобразования данных между форматами XML и JSON. Он включает в себя функции для анализа XML-строк и преобразования деревьев элементов XML в представления словарей, а также для преобразования словарей JSON в XML. Модуль использует библиотеку `xml.etree.ElementTree` для работы с XML и предоставляет гибкие возможности для настройки преобразований.

## Функции

### `dict2xml`

```python
def dict2xml(json_obj: dict, root_name: str = "product") -> str:
    """! Converts a JSON dictionary to an XML string.

    Args:
        json_obj (dict): JSON dictionary to convert.
        root_name (str, optional): Root element name. Defaults to "product".

    Returns:
        str: XML string representation of the JSON.
    """
```

**Назначение**: Преобразует словарь JSON в XML-строку.

**Параметры**:
- `json_obj` (dict): Словарь JSON, который требуется преобразовать.
- `root_name` (str, optional): Имя корневого элемента XML. По умолчанию "product".

**Возвращает**:
- `str`: XML-строка, представляющая JSON.

**Как работает функция**:
Функция `dict2xml` принимает словарь JSON и преобразует его в XML-строку. Она использует рекурсивную функцию `build_xml_element` для построения XML-элементов на основе структуры JSON. Если ключи словаря начинаются с "@", они обрабатываются как атрибуты XML-элемента. Если ключ равен "#text", значение становится текстовым содержимым элемента. Списки в JSON преобразуются в последовательность одноименных XML-элементов.

**Внутренние функции**:

#### `build_xml_element`

```python
def build_xml_element(parent, data):
    """Recursively constructs XML elements from JSON data."""
    if isinstance(data, dict):
        for key, value in data.items():
            if key.startswith("@"):  # Attribute
                parent.set(key[1:], value)
            elif key == "#text":  # Text value
                parent.text = value
            else:
                if isinstance(value, list):
                    for item in value:
                        child = ET.SubElement(parent, key)
                        build_xml_element(child, item)
                else:
                    child = ET.SubElement(parent, key)
                    build_xml_element(child, value)
    elif isinstance(data, list):
        for item in data:
            build_xml_element(parent, item)
    else:
        parent.text = str(data)
```

**Назначение**: Рекурсивно строит XML-элементы на основе JSON-данных.

**Параметры**:
- `parent`: Родительский XML-элемент, к которому добавляются новые элементы.
- `data`: Данные JSON (словарь, список или значение), которые необходимо преобразовать в XML.

**Как работает функция**:
Функция `build_xml_element` рекурсивно строит XML-элементы на основе JSON-данных. Она обрабатывает словари, списки и отдельные значения, создавая соответствующие XML-элементы и атрибуты.

**Примеры**:

```python
json_data = {"product": {"name": "Test Product", "price": "10.00"}}
xml_output = dict2xml(json_data)
print(xml_output)
# Expected output: <product><name>Test Product</name><price>10.00</price></product>
```

### `_parse_node`

```python
def _parse_node(node: ET.Element) -> dict | str:
    """Parse an XML node into a dictionary.

    Args:
        node (ET.Element): The XML element to parse.

    Returns:
        dict | str: A dictionary representation of the XML node, or a string if the node has no attributes or children.
    """
```

**Назначение**: Разбирает XML-узел в словарь.

**Параметры**:
- `node` (ET.Element): XML-элемент для разбора.

**Возвращает**:
- `dict | str`: Представление XML-узла в виде словаря или строка, если у узла нет атрибутов или дочерних элементов.

**Как работает функция**:
Функция `_parse_node` преобразует XML-узел в словарь. Атрибуты узла сохраняются в словаре под ключом `attrs`. Если у узла есть дочерние элементы, они рекурсивно обрабатываются и добавляются в словарь. Если у узла нет атрибутов и дочерних элементов, возвращается только текстовое значение узла.

**Примеры**:
```python
xml_string = '<product name="Test Product"><price>10.00</price></product>'
element_tree = ET.fromstring(xml_string)
dict_output = _parse_node(element_tree)
print(dict_output)
# Пример вывода (может немного отличаться в зависимости от структуры):
# {'attrs': {'name': 'Test Product'}, 'price': '10.00'}
```

### `_make_dict`

```python
def _make_dict(tag: str, value: any) -> dict:
    """Generate a new dictionary with tag and value.

    Args:
        tag (str): The tag name of the XML element.
        value (any): The value associated with the tag.

    Returns:
        dict: A dictionary with the tag name as the key and the value as the dictionary value.
    """
```

**Назначение**: Генерирует новый словарь с тегом и значением.

**Параметры**:
- `tag` (str): Имя тега XML-элемента.
- `value` (any): Значение, связанное с тегом.

**Возвращает**:
- `dict`: Словарь с именем тега в качестве ключа и значением в качестве значения словаря.

**Как работает функция**:
Функция `_make_dict` создает словарь, где ключом является имя тега XML-элемента, а значением - переданное значение. Если в имени тега присутствует пространство имен, оно извлекается и добавляется в словарь.

**Примеры**:
```python
tag = 'product'
value = {'name': 'Test Product'}
dict_output = _make_dict(tag, value)
print(dict_output)
# Expected output: {'product': {'name': 'Test Product'}}
```

### `xml2dict`

```python
def xml2dict(xml: str) -> dict:
    """Parse XML string into a dictionary.

    Args:
        xml (str): The XML string to parse.

    Returns:
        dict: The dictionary representation of the XML.
    """
```

**Назначение**: Преобразует XML-строку в словарь.

**Параметры**:
- `xml` (str): XML-строка для разбора.

**Возвращает**:
- `dict`: Представление XML в виде словаря.

**Как работает функция**:
Функция `xml2dict` принимает XML-строку, преобразует ее в дерево элементов с помощью `ET.fromstring()` и затем вызывает функцию `ET2dict` для преобразования дерева в словарь.

**Примеры**:
```python
xml_string = '<product name="Test Product"><price>10.00</price></product>'
dict_output = xml2dict(xml_string)
print(dict_output)
# Пример вывода (может немного отличаться в зависимости от структуры):
# {'product': {'attrs': {'name': 'Test Product'}, 'price': '10.00'}}
```

### `ET2dict`

```python
def ET2dict(element_tree: ET.Element) -> dict:
    """Convert an XML element tree into a dictionary.

    Args:
        element_tree (ET.Element): The XML element tree.

    Returns:
        dict: The dictionary representation of the XML element tree.
    """
```

**Назначение**: Преобразует дерево элементов XML в словарь.

**Параметры**:
- `element_tree` (ET.Element): Дерево элементов XML.

**Возвращает**:
- `dict`: Представление дерева элементов XML в виде словаря.

**Как работает функция**:
Функция `ET2dict` принимает дерево элементов XML и преобразует его в словарь, вызывая функцию `_make_dict` для создания корневого элемента словаря и функцию `_parse_node` для рекурсивной обработки дочерних элементов.

**Примеры**:
```python
xml_string = '<product name="Test Product"><price>10.00</price></product>'
element_tree = ET.fromstring(xml_string)
dict_output = ET2dict(element_tree)
print(dict_output)
# Пример вывода (может немного отличаться в зависимости от структуры):
# {'product': {'attrs': {'name': 'Test Product'}, 'price': '10.00'}}
```

### `presta_fields_to_xml`

```python
def presta_fields_to_xml(presta_fields_dict: dict) -> str:
    """! Converts a JSON dictionary to an XML string with a fixed root name 'prestashop'.

    Args:
        presta_fields_dict (dict): JSON dictionary containing the data (without 'prestashop' key).

    Returns:
        str: XML string representation of the JSON.
    """
```

**Назначение**: Преобразует JSON-словарь в XML-строку с фиксированным корневым элементом 'prestashop'.

**Параметры**:
- `presta_fields_dict` (dict): JSON-словарь, содержащий данные (без ключа 'prestashop').

**Возвращает**:
- `str`: XML-строка, представляющая JSON.

**Как работает функция**:
Функция `presta_fields_to_xml` принимает JSON-словарь и преобразует его в XML-строку с фиксированным корневым элементом "prestashop". Она использует рекурсивную функцию `build_xml_element` для построения XML-элементов на основе структуры JSON. Ключ первого уровня в словаре используется как имя элемента под корневым элементом "prestashop".

**Внутренние функции**:

#### `build_xml_element`

```python
def build_xml_element(parent, data):
    """Recursively constructs XML elements from JSON data."""
    if isinstance(data, dict):
        for key, value in data.items():
            if key.startswith("@"):  # Attribute
                parent.set(key[1:], value)
            elif key == "#text":  # Text value
                parent.text = value
            else:
                if isinstance(value, list):
                    for item in value:
                        child = ET.SubElement(parent, key)
                        build_xml_element(child, item)
                else:
                    child = ET.SubElement(parent, key)
                    build_xml_element(child, value)
    elif isinstance(data, list):
        for item in data:
            build_xml_element(parent, item)
    else:
        parent.text = str(data)
```

**Назначение**: Рекурсивно строит XML-элементы на основе JSON-данных.

**Параметры**:
- `parent`: Родительский XML-элемент, к которому добавляются новые элементы.
- `data`: Данные JSON (словарь, список или значение), которые необходимо преобразовать в XML.

**Как работает функция**:
Функция `build_xml_element` рекурсивно строит XML-элементы на основе JSON-данных. Она обрабатывает словари, списки и отдельные значения, создавая соответствующие XML-элементы и атрибуты.

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

xml_output = presta_fields_to_xml(json_data)
print(xml_output)
```
```
# Expected output: 
# <prestashop><product><name><language @id="1">Test Product</language><language @id="2">Test Product</language><language @id="3">Test Product</language></name><price>10.00</price><id_tax_rules_group>13</id_tax_rules_group><id_category_default>2</id_category_default></product></prestashop>