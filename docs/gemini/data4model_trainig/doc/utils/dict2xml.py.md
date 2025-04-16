# Модуль `dict2xml`

## Обзор

Модуль `dict2xml` предназначен для преобразования словаря Python в XML строку. Он содержит функцию `dict2xml`, которая рекурсивно обходит словарь и создает соответствующие XML элементы.

## Подробней

Модуль предоставляет удобный способ для преобразования структуры данных Python в формат XML, который может быть использован для взаимодействия с API PrestaShop или другими системами, требующими данные в формате XML.

## Функции

### `_process`

```python
def _process(doc, tag, tag_value):
    """
    Generate dom object for tag: tag_value

    Args:
        doc: xml doc
        tag: tag
        tag_value: tag value

    Returns:
        node or nodelist, be careful
    """
    ...
```

**Назначение**: Генерирует DOM-объект для тега `tag` со значением `tag_value`.

**Параметры**:
- `doc`: xml doc
- `tag`: tag
- `tag_value`: tag value

**Возвращает**:
- `node` или `nodelist`: DOM-объект или список DOM-объектов.

**Как работает функция**:

1.  Обрабатывает случай, когда значение тега является словарем с ключом `'value'`.
2.  Обрабатывает случай, когда значение тега равно `None`.
3.  Обрабатывает простые типы данных (float, int, str) с помощью функции `_process_simple`.
4.  Обрабатывает списки с помощью функции `_process_complex`.
5.  Обрабатывает словари, создавая новый узел и вставляя в него все дочерние узлы из словаря.

### `_process_complex`

```python
def _process_complex(doc, children):
    """
    Generate multi nodes for list, dict

    Args:
        doc: xml doc
        children: tuple of (tag, value)

    Returns:
        nodelist, attrs
    """
    ...
```

**Назначение**: Генерирует несколько узлов для списка или словаря.

**Параметры**:
- `doc`: XML документ.
- `children`: Список кортежей (tag, value).

**Возвращает**:
- `nodelist, attrs`: Список узлов и список атрибутов.

**Как работает функция**:

1.  Итерируется по списку дочерних элементов.
2.  Если тег равен `'attrs'`, обрабатывает атрибуты с помощью функции `_process_attr`.
3.  Иначе обрабатывает тег и значение с помощью функции `_process`.
4.  Возвращает список узлов и список атрибутов.

### `_process_attr`

```python
def _process_attr(doc, attr_value):
    """
    Generate attributes of an element

    Args:
        doc: xml doc
        attr_value: attribute value

    Returns:
        list of attributes
    """
    ...
```

**Назначение**: Генерирует атрибуты элемента.

**Параметры**:
- `doc`: XML документ.
- `attr_value`: Значение атрибута.

**Возвращает**:
- `list of attributes`: Список атрибутов.

**Как работает функция**:

1.  Итерируется по словарю атрибутов.
2.  Создает атрибут с помощью методов `doc.createAttributeNS` или `doc.createAttribute`.
3.  Устанавливает значение атрибута.
4.  Возвращает список атрибутов.

### `_process_simple`

```python
def _process_simple(doc, tag, tag_value):
    """
    Generate node for simple types (int, str)

    Args:
        doc: xml doc
        tag: tag
        tag_value: tag value

    Returns:
        node
    """
    ...
```

**Назначение**: Генерирует узел для простых типов данных (int, str).

**Параметры**:
- `doc`: XML документ.
- `tag`: Тег.
- `tag_value`: Значение тега.

**Возвращает**:
- `node`: DOM-объект.

**Как работает функция**:

1.  Создает элемент с помощью метода `doc.createElement`.
2.  Создает текстовый узел со значением тега с помощью метода `doc.createTextNode`.
3.  Добавляет текстовый узел к элементу.
4.  Возвращает элемент.

### `dict2xml`

```python
def dict2xml(data, encoding='UTF-8'):
    """
    Generate a xml string from a dict

    Args:
        data:     data as a dict
        encoding: data encoding, default: UTF-8

    Returns:
        the data as a xml string
    """
    ...
```

**Назначение**: Генерирует XML строку из словаря.

**Параметры**:
- `data`: Данные в виде словаря.
- `encoding`: Кодировка данных (по умолчанию `'UTF-8'`).

**Возвращает**:
- `the data as a xml string`: Данные в виде XML строки.

**Как работает функция**:

1.  Создает XML документ с помощью метода `getDOMImplementation().createDocument`.
2.  Проверяет, что в словаре только один корневой элемент.
3.  Обрабатывает корневой элемент с помощью функции `_process_complex`.
4.  Добавляет корневой элемент к документу.
5.  Возвращает XML строку с помощью метода `doc.toxml`.

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

# Пример 1
x = {'prestashop': {'addresses': {'address': [
    {'attrs': {'href': {'value': 'http://localhost:8080/api/addresses/1', 'xmlns': 'http://www.w3.org/1999/xlink'}, 'id': '1'}, 'value': None},
    {'attrs': {'href': {'value': 'http://localhost:8080/api/addresses/2', 'xmlns': 'http://www.w3.org/1999/xlink'}, 'id': '2'}, 'value': None}
]}}}

print(dict2xml(x))

# Пример 2
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

# Пример JSON
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