# Модуль `xml2dict`

## Обзор

Модуль предоставляет утилиты для преобразования XML данных в словари. Он включает функции для парсинга XML строк и преобразования деревьев XML элементов в словарные представления.

## Подробнее

Этот модуль упрощает работу с XML данными, позволяя преобразовывать их в более удобный формат словарей. Он использует библиотеки `xml.etree.cElementTree` или `xml.etree.ElementTree` для парсинга XML и рекурсивные функции для обработки структуры XML дерева.

## Функции

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

**Назначение**: Преобразует XML-узел в словарь.

**Параметры**:
- `node` (ET.Element): XML-элемент для парсинга.

**Возвращает**:
- `dict | str`: Словарь, представляющий XML-узел, или строка, если у узла нет атрибутов или дочерних элементов.

**Как работает функция**:
- Инициализирует два пустых словаря: `tree` для хранения структуры узла и `attrs` для атрибутов.
- Итерируется по атрибутам узла, пропуская атрибуты `href`.
- Извлекает текстовое значение узла, удаляя начальные и конечные пробелы.
- Если у узла есть атрибуты, добавляет их в словарь `tree` под ключом `'attrs'`.
- Проверяет наличие дочерних элементов. Для каждого дочернего элемента рекурсивно вызывает `_parse_node` и добавляет результат в `tree`.
- Если узел не имеет дочерних элементов, сохраняет его значение в `tree` под ключом `'value'`.
- Если в словаре `tree` есть только ключ `'value'`, возвращает значение этого ключа.

**Примеры**:

Предположим, у нас есть XML узел:

```xml
<element attr1="value1">text</element>
```

Тогда `_parse_node` вернет словарь:

```python
{'attrs': {'attr1': {'value': 'value1'}}, 'value': 'text'}
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

**Назначение**: Создает новый словарь с тегом и значением.

**Параметры**:
- `tag` (str): Имя тега XML-элемента.
- `value` (any): Значение, связанное с тегом.

**Возвращает**:
- `dict`: Словарь с именем тега в качестве ключа и значением в качестве значения словаря.

**Как работает функция**:
- Инициализирует `tag_values` значением параметра `value`.
- Использует регулярное выражение для поиска namespace в теге. Если namespace найден, создает словарь `tag_values` со значением и namespace.
- Возвращает словарь с тегом в качестве ключа и `tag_values` в качестве значения.

**Примеры**:

```python
_make_dict('tag', 'value') # вернет {'tag': 'value'}
_make_dict('{http://example.com}tag', 'value') # вернет {'tag': {'value': 'value', 'xmlns': 'http://example.com'}}
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

**Назначение**: Преобразует XML строку в словарь.

**Параметры**:
- `xml` (str): XML строка для парсинга.

**Возвращает**:
- `dict`: Словарь, представляющий XML.

**Как работает функция**:
- Использует `ET.fromstring` для преобразования XML строки в дерево элементов.
- Вызывает `ET2dict` для преобразования дерева элементов в словарь.

**Примеры**:

```python
xml_string = '<root><element>text</element></root>'
xml2dict(xml_string) # вернет {'root': {'element': {'value': 'text'}}}
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

**Назначение**: Преобразует дерево XML элементов в словарь.

**Параметры**:
- `element_tree` (ET.Element): Дерево XML элементов.

**Возвращает**:
- `dict`: Словарь, представляющий дерево XML элементов.

**Как работает функция**:
- Вызывает `_make_dict` для преобразования корневого элемента дерева в словарь.

**Примеры**:

```python
import xml.etree.ElementTree as ET
xml_string = '<root><element>text</element></root>'
element_tree = ET.fromstring(xml_string)
ET2dict(element_tree) # вернет {'root': {'element': {'value': 'text'}}}
```