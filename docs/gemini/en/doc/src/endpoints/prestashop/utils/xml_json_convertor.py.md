# Module for converting XML data to dictionaries and vice versa

## Overview

The module `src.endpoints.prestashop.utils.xml_json_convertor.py` provides utilities for converting XML data into dictionaries and vice versa. It includes functions for parsing XML strings and converting XML element trees into dictionary representations. It is used by the PrestaShop endpoint to handle data exchange in XML format.


## Details

This module uses the `xml.etree.ElementTree` library for parsing XML data. It provides functions for converting dictionaries to XML strings and vice versa, with specific focus on handling PrestaShop data structures.

## Table of Contents

- [Functions](#functions)
    - [`dict2xml(json_obj: dict, root_name: str = "product") -> str`](#dict2xmljson_obj-dict-root_name-str--product--str)
    - [`_parse_node(node: ET.Element) -> dict | str`](#_parse_node_node-et_element--dict-str)
    - [`_make_dict(tag: str, value: any) -> dict`](#_make_dict_tag-str-value-any--dict)
    - [`xml2dict(xml: str) -> dict`](#xml2dict_xml-str--dict)
    - [`ET2dict(element_tree: ET.Element) -> dict`](#et2dict_element_tree-et_element--dict)
    - [`presta_fields_to_xml(presta_fields_dict: dict) -> str`](#presta_fields_to_xml_presta_fields_dict-dict--str)

## Functions

### `dict2xml(json_obj: dict, root_name: str = "product") -> str`

**Purpose**: Конвертирует JSON-словарь в строку XML.

**Parameters**:
- `json_obj` (dict): JSON-словарь для преобразования.
- `root_name` (str, optional): Имя корневого элемента. По умолчанию "product".

**Returns**:
- `str`: Строка XML-представления JSON.

**How the Function Works**:
1. **Создаёт корневой элемент:**  Функция создаёт корневой элемент XML-дерева с именем `root_name`.
2. **Рекурсивное построение элементов:**  Используется рекурсивная функция `build_xml_element`, которая строит XML-элементы, рекурсивно проходя по JSON-данным. Она обрабатывает различные типы данных:
    - **Словари:**  Для каждого ключа-значения в словаре создаётся XML-элемент с именем ключа. Если имя ключа начинается с "@", то это атрибут элемента, иначе это дочерний элемент.
    - **Списки:**  Для каждого элемента в списке создаётся XML-элемент с именем, которое совпадает с именем ключа в словаре.
    - **Остальные типы:**  Если данные не являются словарем или списком, они преобразуются в строку и используются в качестве текста для XML-элемента.
3. **Преобразование в строку:**  Функция `ET.tostring` преобразует полученное XML-дерево в строку, кодируя её в UTF-8.

**Examples**:
```python
json_data = {
    "product": {
        "name": {
            "language": [
                {"@id": "1", "#text": "Test Product"},
                {"@id": "2", "#text": "Test Product"},
                {"@id": "3", "#text": "Test Product"}
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

### `_parse_node(node: ET.Element) -> dict | str`

**Purpose**: Парсит XML-узел в словарь.

**Parameters**:
- `node` (ET.Element): XML-элемент для парсинга.

**Returns**:
- `dict | str`: Словарное представление XML-узла или строка, если у узла нет атрибутов или дочерних элементов.

**How the Function Works**:
1. **Обработка атрибутов:**  Функция извлекает все атрибуты XML-элемента и сохраняет их в словарь `attrs`. Атрибуты с именем `{http://www.w3.org/1999/xlink}href` игнорируются, поскольку они не поддерживаются при преобразовании в словарь.
2. **Обработка текстового значения:**  Функция извлекает текстовое значение XML-элемента (если оно есть) и сохраняет его в переменную `value`.
3. **Обработка дочерних элементов:**  Функция рекурсивно обрабатывает все дочерние элементы XML-узла. Для каждого дочернего элемента:
    - Вызывается функция `_parse_node` для рекурсивного парсинга.
    - Полученный результат сохраняется в словарь `ctree`.
    - Если `ctree` не пустой, значение `value` очищается.
    - Дочерний элемент добавляется в словарь `tree` в виде ключа-значения, где ключ - это имя тега дочернего элемента. Если ключ уже существует, то значение превращается в список, и новый элемент добавляется в этот список.
4. **Возврат результата:**  Если у узла нет дочерних элементов, в словарь `tree` добавляется ключ `value` со значением извлеченного текстового значения. Если в словаре `tree` содержится только ключ `value`, функция возвращает непосредственно значение, а не весь словарь.

**Inner Functions**:
-  `_make_dict(tag: str, value: any) -> dict`
    - **Purpose**:  Создаёт новый словарь с тегом и значением.
    - **Parameters**:
        - `tag` (str):  Имя тега XML-элемента.
        - `value` (any):  Значение, связанное с тегом.
    - **Returns**:
        - `dict`:  Словарь с именем тега в качестве ключа и значением в качестве значения словаря.

**Examples**:
```python
xml_string = """
<product>
  <name>Test Product</name>
  <price>10.00</price>
  <attributes>
    <attribute>
      <name>Color</name>
      <value>Red</value>
    </attribute>
    <attribute>
      <name>Size</name>
      <value>Large</value>
    </attribute>
  </attributes>
</product>
"""
root = ET.fromstring(xml_string)
result = _parse_node(root)
print(result)
```

### `_make_dict(tag: str, value: any) -> dict`

**Purpose**: Создаёт новый словарь с тегом и значением.

**Parameters**:
- `tag` (str): Имя тега XML-элемента.
- `value` (any): Значение, связанное с тегом.

**Returns**:
- `dict`: Словарь с именем тега в качестве ключа и значением в качестве значения словаря.

**How the Function Works**:
1. **Проверка на наличие пространства имён:**  Функция проверяет, содержит ли тег пространство имён.
2. **Обработка пространства имён:**  Если тег содержит пространство имён, функция извлекает пространство имён и имя тега и создаёт словарь с ключами `value` и `xmlns`, содержащими соответствующие значения.
3. **Возврат словаря:**  Функция возвращает созданный словарь.

**Examples**:
```python
tag = "{http://www.w3.org/1999/xlink}href"
value = "https://example.com"
result = _make_dict(tag, value)
print(result)  # Output: {'href': {'value': 'https://example.com', 'xmlns': 'http://www.w3.org/1999/xlink'}}
```

### `xml2dict(xml: str) -> dict`

**Purpose**: Парсит строку XML в словарь.

**Parameters**:
- `xml` (str): Строка XML для парсинга.

**Returns**:
- `dict`: Словарное представление XML.

**How the Function Works**:
1. **Парсинг XML:**  Функция `ET.fromstring` используется для преобразования строки XML в XML-дерево.
2. **Преобразование в словарь:**  Функция `ET2dict` вызывается для преобразования XML-дерева в словарь.

**Examples**:
```python
xml_string = """
<product>
  <name>Test Product</name>
  <price>10.00</price>
</product>
"""
result = xml2dict(xml_string)
print(result)
```

### `ET2dict(element_tree: ET.Element) -> dict`

**Purpose**: Конвертирует XML-дерево в словарь.

**Parameters**:
- `element_tree` (ET.Element): XML-дерево.

**Returns**:
- `dict`: Словарное представление XML-дерева.

**How the Function Works**:
1. **Парсинг корневого узла:**  Функция `_parse_node` вызывается для парсинга корневого узла XML-дерева.
2. **Создание словаря:**  Функция `_make_dict` используется для создания словаря с именем тега корневого узла в качестве ключа и результата парсинга в качестве значения.

**Examples**:
```python
xml_string = """
<product>
  <name>Test Product</name>
  <price>10.00</price>
</product>
"""
root = ET.fromstring(xml_string)
result = ET2dict(root)
print(result)
```

### `presta_fields_to_xml(presta_fields_dict: dict) -> str`

**Purpose**: Конвертирует словарь с данными PrestaShop в строку XML.

**Parameters**:
- `presta_fields_dict` (dict): Словарь с данными PrestaShop (без ключа 'prestashop').

**Returns**:
- `str`: Строка XML-представления словаря.

**How the Function Works**:
1. **Проверка наличия данных:**  Функция проверяет, не пуст ли словарь `presta_fields_dict`.
2. **Получение динамического ключа:**  Функция извлекает первый ключ из словаря `presta_fields_dict` (например, 'product', 'category').
3. **Создаёт корневой элемент "prestashop":**  Функция создаёт корневой элемент XML-дерева с именем "prestashop".
4. **Создаёт динамический элемент:**  Функция создаёт дочерний элемент XML-дерева с именем, полученным из динамического ключа.
5. **Рекурсивное построение элементов:**  Функция `build_xml_element` используется для рекурсивного построения XML-элементов из данных словаря `presta_fields_dict`.
6. **Преобразование в строку:**  Функция `ET.tostring` преобразует полученное XML-дерево в строку, кодируя её в UTF-8.

**Inner Functions**:
-  `build_xml_element(parent, data)`
    - **Purpose**:  Рекурсивно строит XML-элементы из JSON-данных.
    - **Parameters**:
        - `parent` (ET.Element):  Родительский XML-элемент.
        - `data` (any):  Данные для построения XML-элементов.
    - **How the Function Works**:
        - **Обработка словарей:**  Для каждого ключа-значения в словаре создаётся XML-элемент с именем ключа. Если имя ключа начинается с "@", то это атрибут элемента, иначе это дочерний элемент.
        - **Обработка списков:**  Для каждого элемента в списке создаётся XML-элемент с именем, которое совпадает с именем ключа в словаре.
        - **Остальные типы:**  Если данные не являются словарем или списком, они преобразуются в строку и используются в качестве текста для XML-элемента.

**Examples**:
```python
json_data = {
    "product": {
        "name": {
            "language": [
                {"@id": "1", "#text": "Test Product"},
                {"@id": "2", "#text": "Test Product"},
                {"@id": "3", "#text": "Test Product"}
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