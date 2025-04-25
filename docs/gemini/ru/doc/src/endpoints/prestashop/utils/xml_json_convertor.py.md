# Модуль для преобразования XML в JSON и обратно

## Обзор

Модуль `src.endpoints.prestashop.utils.xml_json_convertor` предоставляет набор функций для конвертации XML-данных в словарь. Он включает функции для парсинга XML-строк и преобразования XML-дерева в словарь. 

## Подробности

Модуль используется для преобразования XML-структур в более легко обрабатываемые JSON-представления и наоборот. Это позволяет работать с XML-данными более гибким и удобным способом. 

## Классы

### `None`

**Описание**: Модуль не содержит классов.

## Функции

### `dict2xml`

**Назначение**: Преобразует словарь JSON в XML-строку.

**Параметры**:

- `json_obj` (dict): Словарь JSON, который нужно преобразовать.
- `root_name` (str, optional): Имя корневого элемента. По умолчанию "product".

**Возвращает**:

- `str`: Строка с XML-представлением JSON.

**Вызывает исключения**:

- `None`: Функция не вызывает исключений.

**Как работает функция**:

- Функция `dict2xml` рекурсивно перебирает словарь JSON и строит XML-дерево.
- Для каждого ключа-значения в словаре создается соответствующий XML-элемент.
- Если значение является списком, то для каждого элемента списка создается отдельный XML-элемент.
- Если значение является словарем, то для каждого ключа-значения в словаре создается отдельный XML-элемент.
- После построения XML-дерева функция возвращает его в виде XML-строки.

**Примеры**:

```python
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

xml_output = dict2xml(json_data)
print(xml_output)

# Вывод
"""
<product>
  <name>
    <language id="1">Test Product</language>
    <language id="2">Test Product</language>
    <language id="3">Test Product</language>
  </name>
  <price>10.00</price>
  <id_tax_rules_group>13</id_tax_rules_group>
  <id_category_default>2</id_category_default>
</product>
"""

```

### `_parse_node`

**Назначение**: Парсит XML-узел в словарь.

**Параметры**:

- `node` (ET.Element): XML-элемент, который нужно распарсить.

**Возвращает**:

- `dict | str`: Словарь с представлением XML-узла, или строка, если узел не имеет атрибутов или дочерних элементов.

**Вызывает исключения**:

- `None`: Функция не вызывает исключений.

**Как работает функция**:

- Функция `_parse_node` рекурсивно перебирает XML-узел и строит словарь.
- Для каждого атрибута узла создается запись в словаре с именем атрибута в качестве ключа и значением атрибута в качестве значения.
- Для каждого дочернего элемента узла создается запись в словаре с именем дочернего элемента в качестве ключа и результатом рекурсивного вызова `_parse_node` для этого элемента в качестве значения.
- Если узел имеет текстовое значение, то оно сохраняется в поле `value` словаря.
- Если узел не имеет атрибутов, дочерних элементов и текстового значения, то функция возвращает строку, содержащую имя тега.

**Примеры**:

```python
# Пример XML-узла
xml_node = ET.fromstring("<product id=\"123\"><name>Test Product</name><price>10.00</price></product>")

# Парсинг узла
parsed_node = _parse_node(xml_node)

# Вывод
print(parsed_node)

# Вывод
"""
{'id': '123', 'name': 'Test Product', 'price': '10.00'}
"""

```

### `_make_dict`

**Назначение**: Создает новый словарь с тегом и значением.

**Параметры**:

- `tag` (str): Имя тега XML-элемента.
- `value` (any): Значение, связанное с тегом.

**Возвращает**:

- `dict`: Словарь с именем тега в качестве ключа и значением в качестве значения словаря.

**Вызывает исключения**:

- `None`: Функция не вызывает исключений.

**Как работает функция**:

- Функция `_make_dict` создает новый словарь с именем тега в качестве ключа и значением в качестве значения.
- Если тег содержит пространство имен, то функция извлекает пространство имен и имя тега из тега и добавляет их в словарь.

**Примеры**:

```python
# Пример тега и значения
tag = "{http://www.w3.org/1999/xlink}href"
value = "https://example.com"

# Создание словаря
dict_value = _make_dict(tag, value)

# Вывод
print(dict_value)

# Вывод
"""
{'href': {'value': 'https://example.com', 'xmlns': 'http://www.w3.org/1999/xlink'}}
"""

```

### `xml2dict`

**Назначение**: Парсит XML-строку в словарь.

**Параметры**:

- `xml` (str): XML-строка, которую нужно распарсить.

**Возвращает**:

- `dict`: Словарь, представляющий XML.

**Вызывает исключения**:

- `None`: Функция не вызывает исключений.

**Как работает функция**:

- Функция `xml2dict` использует `ET.fromstring` для преобразования XML-строки в XML-дерево.
- Затем функция `ET2dict` вызывается для преобразования XML-дерева в словарь.

**Примеры**:

```python
# Пример XML-строки
xml_string = "<product id=\"123\"><name>Test Product</name><price>10.00</price></product>"

# Парсинг строки
parsed_dict = xml2dict(xml_string)

# Вывод
print(parsed_dict)

# Вывод
"""
{'product': {'id': '123', 'name': 'Test Product', 'price': '10.00'}}
"""

```

### `ET2dict`

**Назначение**: Преобразует XML-дерево в словарь.

**Параметры**:

- `element_tree` (ET.Element): XML-дерево.

**Возвращает**:

- `dict`: Словарь, представляющий XML-дерево.

**Вызывает исключения**:

- `None`: Функция не вызывает исключений.

**Как работает функция**:

- Функция `ET2dict` использует `_parse_node` для преобразования корневого элемента XML-дерева в словарь.
- Затем функция `_make_dict` вызывается для создания словаря с именем корневого элемента в качестве ключа и результатом `_parse_node` в качестве значения.

**Примеры**:

```python
# Пример XML-дерева
element_tree = ET.fromstring("<product id=\"123\"><name>Test Product</name><price>10.00</price></product>")

# Преобразование в словарь
parsed_dict = ET2dict(element_tree)

# Вывод
print(parsed_dict)

# Вывод
"""
{'product': {'id': '123', 'name': 'Test Product', 'price': '10.00'}}
"""

```

### `presta_fields_to_xml`

**Назначение**: Преобразует словарь JSON в XML-строку с фиксированным именем корневого элемента "prestashop".

**Параметры**:

- `presta_fields_dict` (dict): Словарь JSON, содержащий данные (без ключа "prestashop").

**Возвращает**:

- `str`: XML-строка, представляющая JSON.

**Вызывает исключения**:

- `None`: Функция не вызывает исключений.

**Как работает функция**:

- Функция `presta_fields_to_xml` создает корневой элемент "prestashop" и поддерево XML, основываясь на данных из входного словаря.
- Затем функция `build_xml_element` рекурсивно строит XML-дерево, используя данные из словаря.
- После построения XML-дерева функция возвращает его в виде XML-строки.

**Примеры**:

```python
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

# Вывод
"""
<prestashop>
  <product>
    <name>
      <language id="1">Test Product</language>
      <language id="2">Test Product</language>
      <language id="3">Test Product</language>
    </name>
    <price>10.00</price>
    <id_tax_rules_group>13</id_tax_rules_group>
    <id_category_default>2</id_category_default>
  </product>
</prestashop>
"""

```

## Внутренние функции

### `build_xml_element`

**Назначение**: Рекурсивно строит XML-элементы из JSON-данных.

**Параметры**:

- `parent` (ET.Element): Родительский XML-элемент.
- `data` (any): JSON-данные.

**Возвращает**:

- `None`: Функция не возвращает значение.

**Вызывает исключения**:

- `None`: Функция не вызывает исключений.

**Как работает функция**:

- Функция `build_xml_element` рекурсивно перебирает JSON-данные и строит XML-дерево.
- Для каждого ключа-значения в словаре создается соответствующий XML-элемент.
- Если значение является списком, то для каждого элемента списка создается отдельный XML-элемент.
- Если значение является словарем, то для каждого ключа-значения в словаре создается отдельный XML-элемент.
- После построения XML-дерева функция возвращает его в виде XML-строки.

**Примеры**:

```python
# Пример JSON-данных
json_data = {
    "name": "Test Product",
    "price": "10.00",
    "id_tax_rules_group": "13",
    "id_category_default": "2"
}

# Создание корневого элемента
root = ET.Element("product")

# Построение XML-дерева
build_xml_element(root, json_data)

# Вывод XML-дерева
print(ET.tostring(root, encoding="utf-8").decode("utf-8"))

# Вывод
"""
<product>
  <name>Test Product</name>
  <price>10.00</price>
  <id_tax_rules_group>13</id_tax_rules_group>
  <id_category_default>2</id_category_default>
</product>
"""

```

## Параметры класса

- `None`: Модуль не содержит классов.

## Примеры

```python
# Пример использования функции `dict2xml`
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

# Вывод
"""
<product>
  <name>
    <language id="1">Test Product</language>
    <language id="2">Test Product</language>
    <language id="3">Test Product</language>
  </name>
  <price>10.00</price>
  <id_tax_rules_group>13</id_tax_rules_group>
  <id_category_default>2</id_category_default>
</product>
"""

# Пример использования функции `xml2dict`
xml_string = "<product id=\"123\"><name>Test Product</name><price>10.00</price></product>"

parsed_dict = xml2dict(xml_string)
print(parsed_dict)

# Вывод
"""
{'product': {'id': '123', 'name': 'Test Product', 'price': '10.00'}}
"""

# Пример использования функции `presta_fields_to_xml`
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

# Вывод
"""
<prestashop>
  <product>
    <name>
      <language id="1">Test Product</language>
      <language id="2">Test Product</language>
      <language id="3">Test Product</language>
    </name>
    <price>10.00</price>
    <id_tax_rules_group>13</id_tax_rules_group>
    <id_category_default>2</id_category_default>
  </product>
</prestashop>
"""