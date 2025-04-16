# Модуль `xml2dict`

## Обзор

Модуль `xml2dict` предоставляет утилиты для преобразования XML-строки в словарь Python. Он содержит функции `xml2dict` и `ET2dict`, которые используют библиотеку `xml.etree.ElementTree` для разбора XML и создания словаря.

## Подробней

Модуль предоставляет удобный способ для работы с XML-данными, полученными из API PrestaShop или других источников, путем преобразования их в структуру данных Python, с которой легче работать.

## Функции

### `_parse_node`

```python
def _parse_node(node):
    tree = {}
    attrs = {}
    for attr_tag, attr_value in node.attrib.items():
        #  skip href attributes, not supported when converting to dict
        if attr_tag == '{http://www.w3.org/1999/xlink}href':
            continue
        attrs.update(_make_dict(attr_tag, attr_value))

    value = node.text.strip() if node.text is not None else ''

    if attrs:
        tree['attrs'] = attrs

    #Save childrens
    has_child = False
    for child in list(node):
        has_child = True
        ctag = child.tag
        ctree = _parse_node(child)
        cdict = _make_dict(ctag, ctree)

        # no value when there are child elements
        if ctree:
            value = ''

        # first time an attribute is found
        if ctag not in tree: # First time found
            tree.update(cdict)
            continue

        # many times the same attribute, we change to a list
        old = tree[ctag]
        if not isinstance(old, list):
            tree[ctag] = [old] # change to list
        tree[ctag].append(ctree) # Add new entry

    if not has_child:
        tree['value'] = value

    # if there is only a value; no attribute, no child, we return directly the value
    if list(tree.keys()) == ['value']:
        tree = tree['value']
    return tree
```

**Назначение**: Рекурсивно разбирает XML-узел и возвращает его представление в виде словаря.

**Параметры**:
- `node`: XML-узел (ElementTree.Element).

**Возвращает**:
- `tree`: Словарь, представляющий XML-узел.

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
def _make_dict(tag, value):
    """Generate a new dict with tag and value
       If tag is like '{http://cs.sfsu.edu/csc867/myscheduler}patients',
       split it first to: http://cs.sfsu.edu/csc867/myscheduler, patients
    """
    tag_values = value
    result = re.compile("\\{(.*)\\}(.*)").search(tag)
    if result:
        tag_values = {'value': value}
        tag_values['xmlns'], tag = result.groups() # We have a namespace!
    return {tag: tag_values}
```

**Назначение**: Создает новый словарь с тегом и значением. Если тег содержит пространство имен, разделяет его.

**Параметры**:
- `tag`: Тег.
- `value`: Значение.

**Возвращает**:
- `dict`: Словарь с тегом и значением.

**Как работает функция**:

1.  Проверяет, содержит ли тег пространство имен.
2.  Если тег содержит пространство имен, разделяет его на пространство имен и имя тега.
3.  Создает словарь с тегом и значением.

### `xml2dict`

```python
def xml2dict(xml):
    """Parse xml string to dict"""
    element_tree = ET.fromstring(xml)
    return ET2dict(element_tree)
```

**Назначение**: Преобразует XML-строку в словарь.

**Параметры**:
- `xml`: XML-строка.

**Возвращает**:
- `dict`: Словарь, представляющий XML-структуру.

**Как работает функция**:

1.  Разбирает XML-строку с помощью `ET.fromstring()`, получая объект `element_tree`.
2.  Вызывает функцию `ET2dict()` для преобразования объекта `element_tree` в словарь.

### `ET2dict`

```python
def ET2dict(element_tree):
    """Parse xml string to dict"""
    return _make_dict(element_tree.tag, _parse_node(element_tree))
```

**Назначение**: Преобразует объект ElementTree в словарь.

**Параметры**:
- `element_tree`: Объект ElementTree.

**Возвращает**:
- `dict`: Словарь, представляющий XML-структуру.

**Как работает функция**:

1.  Вызывает функцию `_make_dict()` для создания словаря с корневым тегом и результатом разбора узла с помощью функции `_parse_node()`.

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