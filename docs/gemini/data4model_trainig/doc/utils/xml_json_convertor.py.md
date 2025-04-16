# Модуль `xml_json_convertor`

## Обзор

Модуль `xml_json_convertor` предоставляет утилиты для конвертации данных между форматами XML и JSON. Он включает функции для преобразования JSON-словарей в XML-строки и наоборот, а также содержит класс `Config` для хранения конфигурационных параметров.

## Подробней

Модуль содержит функции для преобразования JSON в XML и XML в JSON (словарь Python), что полезно для работы с API PrestaShop, которые могут использовать разные форматы данных.

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
    ...
```

**Назначение**: Преобразует JSON-словарь в XML-строку.

**Параметры**:
- `json_obj` (dict): JSON-словарь для преобразования.
- `root_name` (str, optional): Имя корневого элемента. По умолчанию `"product"`.

**Возвращает**:
- `str`: XML-строковое представление JSON.

**Как работает функция**:

1.  Определяет внутреннюю функцию `build_xml_element`, которая рекурсивно обходит JSON-данные и строит XML-элементы.
2.  Создает корневой элемент XML с именем `root_name`.
3.  Вызывает `build_xml_element` для заполнения корневого элемента данными из JSON.
4.  Преобразует XML-дерево в строку с кодировкой UTF-8.

**Внутренняя функция `build_xml_element`**:
- **Назначение**: Рекурсивно строит XML-элементы из JSON-данных.
- **Параметры**:
    - `parent`: Родительский XML-элемент.
    - `data`: JSON-данные для текущего уровня.
- **Как работает**:
    1. Если `data` является словарем, итерируется по его элементам:
        - Если ключ начинается с "@", то это атрибут элемента.
        - Если ключ равен "#text", то это текстовое значение элемента.
        - Иначе создается подэлемент и рекурсивно вызывается `build_xml_element` для него.
    2. Если `data` является списком, итерируется по его элементам и рекурсивно вызывается `build_xml_element` для каждого элемента.
    3. Иначе устанавливает текстовое значение родительского элемента.

### `_parse_node`

```python
def _parse_node(node: ET.Element) -> dict | str:
    """Parse an XML node into a dictionary.

    Args:
        node (ET.Element): The XML element to parse.

    Returns:
        dict | str: A dictionary representation of the XML node, or a string if the node has no attributes or children.
    """
    ...
```

**Назначение**: Разбирает XML-узел и возвращает его представление в виде словаря.

**Параметры**:
- `node` (ET.Element): XML-элемент для разбора.

**Возвращает**:
- `dict | str`: Словарь, представляющий XML-узел, или строку, если у узла нет атрибутов или дочерних элементов.

**Как работает функция**:

1.  Инициализирует пустой словарь `tree` для хранения информации об узле.
2.  Инициализирует пустой словарь `attrs` для хранения атрибутов узла.
3.  Итерируется по атрибутам узла, сохраняя их в словаре `attrs`. Атрибуты `href` с пространством имен `http://www.w3.org/1999/xlink` пропускаются.
4.  Извлекает текстовое содержимое узла и сохраняет его в переменной `value`.
5.  Если у узла есть атрибуты, добавляет их в словарь `tree` под ключом `'attrs'`.
6.  Итерируется по дочерним элементам узла, рекурсивно вызывая `_parse_node` для каждого дочернего элемента.
7.  Добавляет информацию о дочерних элементах в словарь `tree`. Если у узла есть дочерние элементы, значение текстового содержимого `value` устанавливается в пустую строку.
8.  Если у узла есть только значение (нет атрибутов и дочерних элементов), возвращает непосредственно это значение.
9.  Возвращает словарь `tree`.

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
    ...
```

**Назначение**: Создает новый словарь с тегом и значением.

**Параметры**:
- `tag` (str): Имя тега XML-элемента.
- `value` (any): Значение, связанное с тегом.

**Возвращает**:
- `dict`: Словарь с именем тега в качестве ключа и значением в качестве значения словаря.

**Как работает функция**:

1.  Проверяет, содержит ли тег пространство имен, используя регулярное выражение.
2.  Если тег содержит пространство имен, разделяет его на пространство имен и имя тега.
3.  Создает словарь с тегом и значением.

### `xml2dict`

```python
def xml2dict(xml: str) -> dict:
    """Parse XML string into a dictionary.

    Args:
        xml (str): The XML string to parse.

    Returns:
        dict: The dictionary representation of the XML.
    """
    ...
```

**Назначение**: Преобразует XML-строку в словарь.

**Параметры**:
- `xml` (str): XML-строка для разбора.

**Возвращает**:
- `dict`: Представление XML в виде словаря.

**Как работает функция**:

1.  Разбирает XML-строку с помощью `ET.fromstring()`, получая объект `element_tree`.
2.  Вызывает функцию `ET2dict()` для преобразования объекта `element_tree` в словарь.

### `ET2dict`

```python
def ET2dict(element_tree: ET.Element) -> dict:
    """Convert an XML element tree into a dictionary.

    Args:
        element_tree (ET.Element): The XML element tree.

    Returns:
        dict: The dictionary representation of the XML element tree.
    """
    ...
```

**Назначение**: Преобразует дерево XML-элементов в словарь.

**Параметры**:
- `element_tree` (ET.Element): Дерево XML-элементов.

**Возвращает**:
- `dict`: Словарь, представляющий дерево XML-элементов.

**Как работает функция**:

1.  Вызывает функцию `_make_dict()` для создания словаря с корневым тегом и результатом разбора узла с помощью функции `_parse_node()`.

### `presta_fields_to_xml`

```python
def presta_fields_to_xml(presta_fields_dict: dict) -> str:
    """! Converts a JSON dictionary to an XML string with a fixed root name 'prestashop'.

    Args:
        presta_fields_dict (dict): JSON dictionary containing the data (without 'prestashop' key).

    Returns:
        str: XML string representation of the JSON.
    """
    ...
```

**Назначение**: Преобразует JSON-словарь в XML-строку с фиксированным корневым элементом `'prestashop'`.

**Параметры**:
- `presta_fields_dict` (dict): JSON-словарь, содержащий данные (без ключа `'prestashop'`).

**Возвращает**:
- `str`: XML-строковое представление JSON.

**Как работает функция**:

1.  Определяет внутреннюю функцию `build_xml_element`, которая рекурсивно обходит JSON-данные и строит XML-элементы.
2.  Создает корневой элемент XML с именем `"prestashop"`.
3.  Извлекает динамический ключ (например, `'product'`, `'category'`) из словаря `presta_fields_dict`.
4.  Создает подэлемент корневого элемента с динамическим ключом.
5.  Вызывает `build_xml_element` для заполнения подэлемента данными из JSON.
6.  Преобразует XML-дерево в строку с кодировкой UTF-8.

## Примеры использования

```python
from pprint import pprint

s = """<?xml version="1.0" encoding="UTF-8"?>
<prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
<addresses>
<address id="1" xlink:href="http://localhost:8080/api/addresses/1"/>
<address id="2" xlink:href="http://localhost:8080/api/addresses/2"/>
<address id="3" xlink:href="http://localhost:8080/api/addresses/3"/>
<address id="4" xlink:href="http://localhost:8080/api/addresses/4"/>
<address id="5" xlink:href="http://localhost:8080/api/addresses/5"/>
<address id="6" xlink:href="http://localhost:8080/api/addresses/6"/>
<address id="7" xlink:href="http://localhost:8080/api/addresses/7"/>
<address id="8" xlink:href="http://localhost:8080/api/addresses/8"/>
</addresses>
</prestashop>"""

pprint(xml2dict(s))

s = """<?xml version="1.0" encoding="UTF-8"?>
<prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
<address>
\t<id><![CDATA[1]]></id>
\t<id_customer></id_customer>
\t<id_manufacturer xlink:href="http://localhost:8080/api/manufacturers/1"><![CDATA[1]]></id_manufacturer>
\t<id_supplier></id_supplier>
\t<id_country xlink:href="http://localhost:8080/api/countries/21"><![CDATA[21]]></id_country>
\t<id_state xlink:href="http://localhost:8080/api/states/5"><![CDATA[5]]></id_state>
\t<alias><![CDATA[manufacturer]]></alias>
\t<company></company>
\t<lastname><![CDATA[JOBS]]></lastname>
\t<firstname><![CDATA[STEVEN]]></firstname>
\t<address1><![CDATA[1 Infinite Loop]]></address1>
\t<address2></address2>
\t<postcode><![CDATA[95014]]></postcode>
\t<city><![CDATA[Cupertino]]></city>
\t<other></other>
\t<phone><![CDATA[(800) 275-2273]]></phone>
\t<phone_mobile></phone_mobile>
\t<dni></dni>
\t<vat_number></vat_number>
\t<deleted><![CDATA[0]]></deleted>
\t<date_add><![CDATA[2012-02-06 09:33:52]]></date_add>
\t<date_upd><![CDATA[2012-02-07 11:18:48]]></date_upd>
</address>
</prestashop>"""

pprint(xml2dict(s))
```

**Пример преобразования JSON в XML:**

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