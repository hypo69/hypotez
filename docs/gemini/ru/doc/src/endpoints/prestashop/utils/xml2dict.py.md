# Модуль xml2dict

## Обзор

Модуль `xml2dict` предоставляет функции для преобразования XML-строк в Python-словари.  Он основан на модуле `xml.etree.ElementTree`, который является стандартным инструментом для работы с XML в Python.

## Функции

### `_parse_node(node)`

**Назначение**: Рекурсивная функция для преобразования XML-узла в словарь.

**Параметры**:

- `node`: XML-узел, который нужно преобразовать.

**Возвращает**:

- `dict`: Словарь, представляющий XML-узел.

**Как работает**:

- Функция создает пустой словарь `tree` для хранения данных XML-узла.
- Она перебирает все атрибуты узла и добавляет их в словарь `attrs` с использованием функции `_make_dict`.
- Затем функция извлекает текстовое значение узла (если оно есть) и сохраняет его в переменную `value`.
- Если узел имеет дочерние узлы, функция рекурсивно вызывает себя для каждого дочернего узла и добавляет полученные словари в `tree`.
- Если узел не имеет дочерних узлов, функция сохраняет текстовое значение в `tree`.
- В конце функция возвращает `tree`.

### `_make_dict(tag, value)`

**Назначение**: Функция для создания словаря с тегом и значением.

**Параметры**:

- `tag`: Тег XML-элемента.
- `value`: Значение XML-элемента.

**Возвращает**:

- `dict`: Словарь с тегом и значением.

**Как работает**:

- Функция проверяет, содержит ли `tag` пространство имен.
- Если да, она разделяет `tag` на пространство имен и имя тега и сохраняет их в словарь `tag_values`.
- В противном случае она создает словарь `tag_values` с одним ключом `value` и значением, равным `value`.
- Затем функция возвращает словарь с тегом и `tag_values` в качестве значения.

### `xml2dict(xml)`

**Назначение**: Функция для преобразования XML-строки в словарь.

**Параметры**:

- `xml`: XML-строка, которую нужно преобразовать.

**Возвращает**:

- `dict`: Словарь, представляющий XML-строку.

**Как работает**:

- Функция парсит XML-строку с использованием `ET.fromstring`.
- Затем она вызывает функцию `ET2dict` для преобразования корневого узла в словарь.

### `ET2dict(element_tree)`

**Назначение**: Функция для преобразования XML-дерева в словарь.

**Параметры**:

- `element_tree`: XML-дерево, которое нужно преобразовать.

**Возвращает**:

- `dict`: Словарь, представляющий XML-дерево.

**Как работает**:

- Функция вызывает `_make_dict` для создания словаря с тегом и значением, полученным путем вызова `_parse_node` для корневого узла XML-дерева.

## Примеры

```python
# Пример 1: Преобразование простой XML-строки
xml_string = """<?xml version="1.0" encoding="UTF-8"?>
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
dict_data = xml2dict(xml_string)
# dict_data будет содержать структурированный словарь, представляющий XML-строку

# Пример 2: Преобразование XML-дерева
from .prestapyt import PrestaShopWebService

prestashop = PrestaShopWebService('http://localhost:8080/api', 'BVWPFFYBT97WKM959D7AVVD0M4815Y1L')

products_xml = prestashop.get('products', 1)

products_dict = ET2dict(products_xml)
# products_dict будет содержать структурированный словарь, представляющий XML-дерево