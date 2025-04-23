# Модуль `dict2xml`

## Обзор

Модуль `dict2xml` предназначен для преобразования словаря Python в XML-строку. Он был адаптирован для использования с Prestapyt и основан на коде из репозитория lhammer.

## Подробней

Модуль содержит функции для обработки различных типов данных, встречающихся в словарях, и преобразования их в соответствующие XML-узлы и атрибуты. Он обрабатывает простые типы данных (строки, числа), списки и вложенные словари.

## Функции

### `_process`

```python
def _process(doc, tag, tag_value):
    """
    Генерирует DOM-объект для тега: значение тега.

    Args:
        doc: XML-документ.
        tag: Тег.
        tag_value: Значение тега.

    Returns:
        node или nodelist.
    """
```

**Назначение**: Преобразует значение тега в XML-совместимый формат. Функция рекурсивно обрабатывает простые типы данных, списки и словари, создавая соответствующие XML-узлы.

**Параметры**:
- `doc` (xml.dom.minidom.Document): XML-документ, к которому добавляются узлы.
- `tag` (str): Имя тега для создания XML-узла.
- `tag_value` (Any): Значение тега, которое может быть строкой, числом, списком или словарем.

**Возвращает**:
- `xml.dom.minidom.Node | list[xml.dom.minidom.Node]`: XML-узел или список узлов, в зависимости от типа входных данных.

**Как работает функция**:
- Проверяет, является ли значение тега словарем с ключом 'value'. Если да, извлекает значение.
- Обрабатывает `None` значения, заменяя их пустой строкой.
- Для простых типов данных (int, float, str) вызывает `_process_simple` для создания узла.
- Для списков вызывает `_process_complex` для создания списка узлов с одинаковым тегом.
- Для словарей создает новый узел и добавляет все дочерние узлы, полученные из элементов словаря.

**Примеры**:

```python
from xml.dom.minidom import getDOMImplementation

doc = getDOMImplementation().createDocument(None, None, None)
tag = 'item'
tag_value = 'Пример значения'
node = _process(doc, tag, tag_value)
print(node.toxml())  # Вывод: <item>Пример значения</item>
```

### `_process_complex`

```python
def _process_complex(doc, children):
    """
    Генерирует несколько узлов для списка, словаря.

    Args:
        doc: XML-документ.
        children: Список кортежей (тег, значение).

    Returns:
        nodelist, attrs
    """
```

**Назначение**: Создает список XML-узлов и атрибутов на основе списка дочерних элементов.

**Параметры**:
- `doc` (xml.dom.minidom.Document): XML-документ, к которому добавляются узлы.
- `children` (list[tuple[str, Any]]): Список кортежей, где каждый кортеж содержит имя тега и его значение.

**Возвращает**:
- `tuple[list[xml.dom.minidom.Node], list[xml.dom.minidom.Attr]]`: Кортеж, содержащий список XML-узлов и список атрибутов.

**Как работает функция**:
- Итерируется по списку `children`, обрабатывая каждый тег и значение.
- Если тег равен 'attrs', добавляет атрибуты к списку атрибутов.
- В противном случае вызывает `_process` для создания XML-узла на основе тега и значения.
- Возвращает список узлов и атрибутов.

**Примеры**:

```python
from xml.dom.minidom import getDOMImplementation

doc = getDOMImplementation().createDocument(None, None, None)
children = [('item1', 'Значение 1'), ('item2', 'Значение 2')]
nodelist, attrs = _process_complex(doc, children)
for node in nodelist:
    print(node.toxml())
# Вывод:
# <item1>Значение 1</item1>
# <item2>Значение 2</item2>
```

### `_process_attr`

```python
def _process_attr(doc, attr_value):
    """
    Генерирует атрибуты элемента.

    Args:
        doc: XML-документ.
        attr_value: Значение атрибута.

    Returns:
        Список атрибутов.
    """
```

**Назначение**: Создает список XML-атрибутов на основе словаря атрибутов.

**Параметры**:
- `doc` (xml.dom.minidom.Document): XML-документ, к которому добавляются атрибуты.
- `attr_value` (dict[str, Any]): Словарь, где ключи - имена атрибутов, а значения - их значения.

**Возвращает**:
- `list[xml.dom.minidom.Attr]`: Список XML-атрибутов.

**Как работает функция**:
- Итерируется по словарю `attr_value`, создавая XML-атрибуты для каждого элемента.
- Обрабатывает атрибуты с пространством имен (xmlns).
- Возвращает список атрибутов.

**Примеры**:

```python
from xml.dom.minidom import getDOMImplementation

doc = getDOMImplementation().createDocument(None, None, None)
attr_value = {'name': 'Пример', 'value': 'значение'}
attrs = _process_attr(doc, attr_value)
for attr in attrs:
    print(attr.name, attr.value)
# Вывод:
# name Пример
# value значение
```

### `_process_simple`

```python
def _process_simple(doc, tag, tag_value):
    """
    Генерирует узел для простых типов (int, str).

    Args:
        doc: XML-документ.
        tag: Тег.
        tag_value: Значение тега.

    Returns:
        Узел.
    """
```

**Назначение**: Создает XML-узел для простых типов данных, таких как строки и числа.

**Параметры**:
- `doc` (xml.dom.minidom.Document): XML-документ, к которому добавляется узел.
- `tag` (str): Имя тега для создания XML-узла.
- `tag_value` (str | int): Значение тега, которое будет преобразовано в строку.

**Возвращает**:
- `xml.dom.minidom.Node`: XML-узел с заданным тегом и значением.

**Как работает функция**:
- Создает новый XML-элемент с заданным тегом.
- Создает текстовый узел с заданным значением и добавляет его к элементу.
- Возвращает созданный XML-элемент.

**Примеры**:

```python
from xml.dom.minidom import getDOMImplementation

doc = getDOMImplementation().createDocument(None, None, None)
tag = 'item'
tag_value = 'Пример значения'
node = _process_simple(doc, tag, tag_value)
print(node.toxml())  # Вывод: <item>Пример значения</item>
```

### `dict2xml`

```python
def dict2xml(data, encoding='UTF-8'):
    """
    Генерирует XML-строку из словаря.

    Args:
        data: Данные в виде словаря.
        encoding: Кодировка данных, по умолчанию: UTF-8.

    Returns:
        Данные в виде XML-строки.

    Raises:
        Exception: Если в данных больше одного корневого узла.
    """
```

**Назначение**: Преобразует словарь Python в XML-строку.

**Параметры**:
- `data` (dict): Словарь, который нужно преобразовать в XML.
- `encoding` (str): Кодировка XML-документа (по умолчанию 'UTF-8').

**Возвращает**:
- `str`: XML-строка, представляющая входной словарь.

**Вызывает исключения**:
- `Exception`: Если входной словарь содержит более одного корневого элемента.

**Как работает функция**:
- Создает новый XML-документ с помощью `getDOMImplementation().createDocument()`.
- Проверяет, что входной словарь содержит только один корневой элемент.
- Вызывает `_process_complex` для преобразования словаря в XML-узлы и атрибуты.
- Добавляет корневой узел к XML-документу.
- Преобразует XML-документ в строку с заданной кодировкой.

**Примеры**:

```python
data = {'root': {'item1': 'Значение 1', 'item2': 'Значение 2'}}
xml_string = dict2xml(data)
print(xml_string)
# Вывод:
# <?xml version="1.0" encoding="UTF-8"?>
# <root>
#   <item1>Значение 1</item1>
#   <item2>Значение 2</item2>
# </root>
```
```python
data = {'prestashop': {'addresses': {'address': [
    {'attrs': {'href': {'value': 'http://localhost:8080/api/addresses/1', 'xmlns': 'http://www.w3.org/1999/xlink'}, 'id': '1'}, 'value': None},
    {'attrs': {'href': {'value': 'http://localhost:8080/api/addresses/2', 'xmlns': 'http://www.w3.org/1999/xlink'}, 'id': '2'}, 'value': None}
]}}}

print(dict2xml(data))
```
## Примеры использования

В `if __name__ == '__main__':` приведены примеры использования функции `dict2xml` с различными структурами данных.
```
from pprint import pprint

# Example 1
x = {'prestashop': {'addresses': {'address': [
    {'attrs': {'href': {'value': 'http://localhost:8080/api/addresses/1', 'xmlns': 'http://www.w3.org/1999/xlink'}, 'id': '1'}, 'value': None},
    {'attrs': {'href': {'value': 'http://localhost:8080/api/addresses/2', 'xmlns': 'http://www.w3.org/1999/xlink'}, 'id': '2'}, 'value': None}
]}}}

print(dict2xml(x))

# Example 2
x = {'prestashop': {'address': {
    'address1': '1 Infinite Loop',
    'address2': None,
    'alias': 'manufacturer',
    'city': 'Cupertino',
    'company': None,
    'date_add': '2012-02-06 09:33:52',
    'date_upd': '2012-02-07 11:18:48',
    'deleted': '0',
    'dni': None,
    'firstname': 'STEVEN',
    'id': 1,
    'id_country': 21,
    'id_customer': None,
    'id_manufacturer': 1,
    'id_state': 5,
    'id_supplier': None,
    'lastname': 'JOBS',
    'other': None,
    'phone': '(800) 275-2273',
    'phone_mobile': None,
    'postcode': '95014',
    'vat_number': 'XXX',
    'description': {'language': [
        {'attrs': {'id': '1', 'href': {'value': 'http://localhost:8080/api/languages/1', 'xmlns': 'http://www.w3.org/1999/xlink'}}, 'value': 'test description english'},
        {'attrs': {'id': '2', 'href': {'value': 'http://localhost:8080/api/languages/1', 'xmlns': 'http://www.w3.org/1999/xlink'}}, 'value': 'test description french'}
    ]}
}}}

print(dict2xml(x))
```
```rst
 .. module:: src.endpoints.prestashop.utils.dict2xml
```
```
## \file hypotez/src/endpoints/prestashop/utils/dict2xml.py
# -*- coding: utf-8 -*-

```
"""
Модуль для преобразования словаря Python в XML-строку.
==========================================================

Модуль содержит функции для обработки различных типов данных,
встречающихся в словарях, и преобразования их в соответствующие XML-узлы
и атрибуты. Он обрабатывает простые типы данных (строки, числа),
списки и вложенные словари.

Зависимости:
    - xml.dom.minidom

 .. module:: src.endpoints.prestashop.utils.dict2xml
"""