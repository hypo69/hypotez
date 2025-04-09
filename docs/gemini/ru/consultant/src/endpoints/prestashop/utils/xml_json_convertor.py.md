### **Анализ кода модуля `xml_json_convertor.py`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код содержит функции для конвертации JSON в XML и XML в JSON, что полезно для интеграции с Prestashop.
    - Присутствуют docstring для большинства функций, что облегчает понимание кода.
    - Код достаточно хорошо структурирован.
- **Минусы**:
    - В некоторых местах используются смешанные стили комментариев (как старые docstring, так и обычные комментарии).
    - Некоторые docstring написаны на английском языке.
    - Отсутствует обработка исключений.
    - Не используются логирование.
    - Есть дублирование кода (функции `dict2xml` и `presta_fields_to_xml` очень похожи).
    - Не все переменные аннотированы типами.

**Рекомендации по улучшению:**

1.  **Общая документация модуля**:
    - Добавить общее описание модуля в начале файла, указав его назначение и примеры использования.
2.  **Унификация комментариев**:
    - Перевести все docstring на русский язык и привести к единообразному стилю.
3.  **Обработка исключений**:
    - Добавить блоки try-except для обработки возможных исключений, например, `ET.fromstring` может вызвать исключение, если XML некорректный.
4.  **Логирование**:
    - Добавить логирование для отслеживания ошибок и предупреждений.
5.  **Рефакторинг**:
    - Объединить функциональность `dict2xml` и `presta_fields_to_xml` в одну функцию, параметризовав имя корневого элемента.
6.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных и возвращаемых значений функций.
7.  **Использование одинарных кавычек**:
    - Заменить двойные кавычки на одинарные, где это необходимо.
8. **Заменить все  `Union` на `|`**

**Оптимизированный код:**

```python
## \file /src/endpoints/prestashop/utils/xml_json_convertor.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для конвертации XML данных в JSON и наоборот.
=====================================================

Модуль предоставляет утилиты для преобразования XML данных в словари и JSON в XML.
Включает функции для парсинга XML строк и конвертации XML деревьев элементов в словарные представления.

Пример использования:
----------------------

>>> from src.endpoints.prestashop.utils.xml_json_convertor import xml2dict, dict2xml
>>> xml_data = '<product><name>Test Product</name><price>10.00</price></product>'
>>> data = xml2dict(xml_data)
>>> print(data)
{'product': {'name': 'Test Product', 'price': '10.00'}}
>>> json_data = {'product': {'name': 'Test Product', 'price': '10.00'}}
>>> xml_data = dict2xml(json_data)
>>> print(xml_data)
<product><name>Test Product</name><price>10.00</product>
"""
import json
import re
import xml.etree.ElementTree as ET
from typing import Any, Optional
from src.logger import logger


def dict2xml(json_obj: dict, root_name: str = 'product') -> str:
    """
    Конвертирует JSON словарь в XML строку.

    Args:
        json_obj (dict): JSON словарь для конвертации.
        root_name (str, optional): Имя корневого элемента. По умолчанию 'product'.

    Returns:
        str: XML строковое представление JSON.

    Raises:
        TypeError: Если входные данные имеют неверный тип.
        ValueError: Если возникают проблемы при построении XML.

    Example:
        >>> data = {'product': {'name': 'Test Product', 'price': '10.00'}}
        >>> xml_data = dict2xml(data)
        >>> print(xml_data)
        <product><name>Test Product</name><price>10.00</product>
    """

    def build_xml_element(parent: ET.Element, data: Any) -> None:
        """
        Рекурсивно конструирует XML элементы из JSON данных.

        Args:
            parent (ET.Element): Родительский XML элемент.
            data (Any): Данные для добавления в XML элемент.

        Raises:
            TypeError: Если данные имеют неверный тип.
            ValueError: Если возникают проблемы при построении XML.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                if key.startswith('@'):  # Attribute
                    parent.set(key[1:], str(value)) # Преобразуем значение атрибута в строку
                elif key == '#text':  # Text value
                    parent.text = str(value) # Преобразуем текстовое значение в строку
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
            parent.text = str(data) # Преобразуем значение в строку

    try:
        # Создаем корневой элемент
        root = ET.Element(root_name)
        build_xml_element(root, json_obj[root_name])

        # Конвертируем XML дерево в строку
        return ET.tostring(root, encoding='utf-8').decode('utf-8')
    except (TypeError, ValueError) as ex:
        logger.error('Ошибка при конвертации JSON в XML', ex, exc_info=True)
        return ''


def _parse_node(node: ET.Element) -> dict | str:
    """
    Разбирает XML узел в словарь.

    Args:
        node (ET.Element): XML элемент для разбора.

    Returns:
        dict | str: Словарное представление XML узла, или строка, если узел не имеет атрибутов или потомков.
    """
    tree = {}
    attrs = {}
    for attr_tag, attr_value in node.attrib.items():
        # Пропускаем атрибуты href, не поддерживаются при конвертации в словарь
        if attr_tag == '{http://www.w3.org/1999/xlink}href':
            continue
        attrs.update(_make_dict(attr_tag, attr_value))

    value = node.text.strip() if node.text is not None else ''

    if attrs:
        tree['attrs'] = attrs

    # Сохраняем потомков
    has_child = False
    for child in list(node):
        has_child = True
        ctag = child.tag
        ctree = _parse_node(child)
        cdict = _make_dict(ctag, ctree)

        # Нет значения, когда есть дочерние элементы
        if ctree:
            value = ''

        # Первый раз найден атрибут
        if ctag not in tree:  # Первый раз нашли
            tree.update(cdict)
            continue

        # Много раз один и тот же атрибут, меняем на список
        old = tree[ctag]
        if not isinstance(old, list):
            tree[ctag] = [old]  # Меняем на список
        tree[ctag].append(ctree)  # Добавляем новую запись

    if not has_child:
        tree['value'] = value

    # Если есть только значение; нет атрибута, нет потомка, возвращаем непосредственно значение
    if list(tree.keys()) == ['value']:
        tree = tree['value']
    return tree


def _make_dict(tag: str, value: Any) -> dict:
    """
    Генерирует новый словарь с тегом и значением.

    Args:
        tag (str): Имя тега XML элемента.
        value (Any): Значение, связанное с тегом.

    Returns:
        dict: Словарь с именем тега в качестве ключа и значением в качестве значения словаря.
    """
    tag_values = value
    result = re.compile(r'\{(.*)\}(.*)').search(tag)
    if result:
        tag_values = {'value': value}
        tag_values['xmlns'], tag = result.groups()  # У нас есть @namespace src!
    return {tag: tag_values}


def xml2dict(xml: str) -> dict:
    """
    Разбирает XML строку в словарь.

    Args:
        xml (str): XML строка для разбора.

    Returns:
        dict: Словарное представление XML.

    Raises:
        ET.ParseError: Если XML строка имеет неверный формат.

    Example:
        >>> xml_data = '<product><name>Test Product</name><price>10.00</price></product>'
        >>> data = xml2dict(xml_data)
        >>> print(data)
        {'product': {'name': 'Test Product', 'price': '10.00'}}
    """
    try:
        element_tree = ET.fromstring(xml)
        return ET2dict(element_tree)
    except ET.ParseError as ex:
        logger.error('Ошибка при парсинге XML', ex, exc_info=True)
        return {}


def ET2dict(element_tree: ET.Element) -> dict:
    """
    Конвертирует XML дерево элементов в словарь.

    Args:
        element_tree (ET.Element): XML дерево элементов.

    Returns:
        dict: Словарное представление XML дерева элементов.
    """
    return _make_dict(element_tree.tag, _parse_node(element_tree))


def presta_fields_to_xml(presta_fields_dict: dict, root_name: str = 'prestashop') -> str:
    """
    Конвертирует JSON словарь в XML строку с указанным корневым элементом.

    Args:
        presta_fields_dict (dict): JSON словарь, содержащий данные (без ключа 'prestashop').
        root_name (str, optional): Имя корневого элемента. По умолчанию 'prestashop'.

    Returns:
        str: XML строковое представление JSON.
    """

    def build_xml_element(parent: ET.Element, data: Any) -> None:
        """Рекурсивно конструирует XML элементы из JSON данных."""
        if isinstance(data, dict):
            for key, value in data.items():
                if key.startswith('@'):  # Attribute
                    parent.set(key[1:], str(value))  # Преобразуем значение атрибута в строку
                elif key == '#text':  # Text value
                    parent.text = str(value)  # Преобразуем текстовое значение в строку
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
            parent.text = str(data)  # Преобразуем значение в строку

    if not presta_fields_dict:
        return ''

    dynamic_key = next(iter(presta_fields_dict))  # Берём первый ключ (например, 'product', 'category' и т. д.)

    # Создаём корневой элемент "prestashop"
    root = ET.Element(root_name)
    dynamic_element = ET.SubElement(root, dynamic_key)
    build_xml_element(dynamic_element, presta_fields_dict[dynamic_key])

    # Конвертируем в строку
    return ET.tostring(root, encoding='utf-8').decode('utf-8')


# Пример JSON
"""
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
"""