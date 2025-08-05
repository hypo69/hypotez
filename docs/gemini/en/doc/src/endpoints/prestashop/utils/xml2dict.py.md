# Модуль xml2dict

## Обзор

Модуль `xml2dict` предоставляет функции для преобразования XML-строки в словарь Python. Он использует библиотеку `xml.etree.ElementTree` для парсинга XML и рекурсивно создает словарь, представляющий структуру XML-документа.

## Детали

Этот модуль адаптирован из проекта `lhammer` (https://github.com/nkchenz/lhammer) для использования в `PrestaShop` API с помощью библиотеки `prestapyt`. 

## Функции

### `xml2dict(xml)`

**Назначение**: Преобразует XML-строку в словарь Python.

**Параметры**:

- `xml` (str): XML-строка, которую необходимо преобразовать.

**Возвращает**:

- `dict`: Словарь, представляющий структуру XML-документа.

**Пример**:

```python
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
```

### `ET2dict(element_tree)`

**Назначение**: Преобразует объект `ElementTree` в словарь Python.

**Параметры**:

- `element_tree` (ElementTree): Объект `ElementTree`, представляющий XML-документ.

**Возвращает**:

- `dict`: Словарь, представляющий структуру XML-документа.

**Пример**:

```python
from . import dict2xml
from .prestapyt import PrestaShopWebService
prestashop = PrestaShopWebService('http://localhost:8080/api',
                                      'BVWPFFYBT97WKM959D7AVVD0M4815Y1L')

products_xml = prestashop.get('products', 1)

products_dict = ET2dict(products_xml)
pprint(dict2xml.dict2xml(products_dict))
```

## Внутренние функции

### `_parse_node(node)`

**Назначение**: Парсит узел XML-дерева и рекурсивно создает словарь, представляющий его структуру.

**Параметры**:

- `node` (Element): Узел XML-дерева.

**Возвращает**:

- `dict`: Словарь, представляющий структуру узла.

**Как работает**:

1. Создает пустой словарь `tree`.
2. Добавляет атрибуты узла в `tree['attrs']` (если они есть).
3. Извлекает текст узла, если он существует.
4. Рекурсивно вызывает функцию `_parse_node` для каждого дочернего узла и добавляет их в `tree`.
5. Если узел имеет только текст, то возвращает значение текста.
6. В противном случае возвращает словарь `tree`.

### `_make_dict(tag, value)`

**Назначение**: Создает словарь, представляющий тег и его значение.

**Параметры**:

- `tag` (str): Тег XML-элемента.
- `value` (str): Значение тега.

**Возвращает**:

- `dict`: Словарь, представляющий тег и его значение.

**Как работает**:

1. Проверяет, содержит ли `tag` пространство имен.
2. Если да, то разделяет `tag` на пространство имен и имя тега.
3. Создает словарь с ключом `tag` и значением `value`.
4. Если `tag` содержит пространство имен, то добавляет ключ `xmlns` со значением пространства имен.
5. Возвращает созданный словарь.

## Примеры

```python
s = """<?xml version="1.0" encoding="UTF-8"?>
<prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
<address>
    <id><![CDATA[1]]></id>
    <id_customer></id_customer>
    <id_manufacturer xlink:href="http://localhost:8080/api/manufacturers/1"><![CDATA[1]]></id_manufacturer>
    <id_supplier></id_supplier>
    <id_country xlink:href="http://localhost:8080/api/countries/21"><![CDATA[21]]></id_country>
    <id_state xlink:href="http://localhost:8080/api/states/5"><![CDATA[5]]></id_state>
    <alias><![CDATA[manufacturer]]></alias>
    <company></company>
    <lastname><![CDATA[JOBS]]></lastname>
    <firstname><![CDATA[STEVEN]]></firstname>
    <address1><![CDATA[1 Infinite Loop]]></address1>
    <address2></address2>
    <postcode><![CDATA[95014]]></postcode>
    <city><![CDATA[Cupertino]]></city>
    <other></other>
    <phone><![CDATA[(800) 275-2273]]></phone>
    <phone_mobile></phone_mobile>
    <dni></dni>
    <vat_number></vat_number>
    <deleted><![CDATA[0]]></deleted>
    <date_add><![CDATA[2012-02-06 09:33:52]]></date_add>
    <date_upd><![CDATA[2012-02-07 11:18:48]]></date_upd>
</address>
</prestashop>"""

pprint(xml2dict(s))
```
```python
## \file hypotez/src/endpoints/prestashop/utils/xml2dict.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
  Code from https://github.com/nkchenz/lhammer/blob/master/lhammer/xml2dict.py
  Distributed under GPL2 Licence
  CopyRight (C) 2009 Chen Zheng

  Adapted for Prestapyt by Guewen Baconnier
  Copyright 2012 Camptocamp SA
"""

import re

try:
    import xml.etree.cElementTree as ET
except ImportError as err:
    import xml.etree.ElementTree as ET


def _parse_node(node):
    """
    Парсит узел XML-дерева и рекурсивно создает словарь, представляющий его структуру.

    Args:
        node (Element): Узел XML-дерева.

    Returns:
        dict: Словарь, представляющий структуру узла.
    """
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

        # no value when there is child elements
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

def _make_dict(tag, value):
    """
    Создает словарь, представляющий тег и его значение.

    Args:
        tag (str): Тег XML-элемента.
        value (str): Значение тега.

    Returns:
        dict: Словарь, представляющий тег и его значение.
    """
    tag_values = value
    result = re.compile("\\{(.*)\\}(.*)").search(tag)
    if result:
        tag_values = {'value': value}
        tag_values['xmlns'], tag = result.groups() # We have a namespace!
    return {tag: tag_values}

def xml2dict(xml):
    """
    Преобразует XML-строку в словарь Python.

    Args:
        xml (str): XML-строка, которую необходимо преобразовать.

    Returns:
        dict: Словарь, представляющий структуру XML-документа.
    """
    element_tree = ET.fromstring(xml)
    return ET2dict(element_tree)

def ET2dict(element_tree):
    """
    Преобразует объект ElementTree в словарь Python.

    Args:
        element_tree (ElementTree): Объект ElementTree, представляющий XML-документ.

    Returns:
        dict: Словарь, представляющий структуру XML-документа.
    """
    return _make_dict(element_tree.tag, _parse_node(element_tree))

if __name__ == '__main__':
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

    from . import dict2xml
    from .prestapyt import PrestaShopWebService
    prestashop = PrestaShopWebService('http://localhost:8080/api',
                                      'BVWPFFYBT97WKM959D7AVVD0M4815Y1L')

    products_xml = prestashop.get('products', 1)

    products_dict = ET2dict(products_xml)
    pprint(dict2xml.dict2xml(products_dict))