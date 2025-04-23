# Модуль `xml2dict`

## Обзор

Модуль предоставляет утилиты для преобразования XML данных в словари. Он включает функции для разбора XML строк и преобразования деревьев XML элементов в представления словарей.

## Подробнее

Модуль `xml2dict` предназначен для упрощения работы с XML данными, предоставляя инструменты для их преобразования в удобный формат словарей Python. Это может быть полезно, например, при обработке конфигурационных файлов в формате XML или при интеграции с системами, использующими XML для обмена данными.

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
    ...
```

**Назначение**: Преобразует XML-ноду в словарь.

**Параметры**:
- `node` (ET.Element): XML элемент для разбора.

**Возвращает**:
- `dict | str`: Представление XML-ноды в виде словаря, или строка, если у ноды нет атрибутов или дочерних элементов.

**Как работает функция**:
Функция рекурсивно разбирает XML-элемент, преобразуя его в словарь. Атрибуты элемента сохраняются в словаре под ключом `'attrs'`, а дочерние элементы добавляются в словарь как новые ключи. Если у элемента есть только текстовое значение и нет атрибутов или дочерних элементов, функция возвращает это значение напрямую.

**Примеры**:

Предположим, у нас есть XML-элемент `<root><child>value</child></root>`. Функция `_parse_node` преобразует его в словарь `{'child': {'value': 'value'}}`.

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
Функция создает словарь, где ключом является имя тега XML-элемента, а значением - переданное значение. Если тег содержит пространство имен (например, `xmlns`), функция извлекает пространство имен и создает словарь с информацией о пространстве имен.

**Примеры**:

Если вызвать `_make_dict('tag', 'value')`, функция вернет `{'tag': 'value'}`.

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

**Назначение**: Преобразует XML строку в словарь.

**Параметры**:
- `xml` (str): XML строка для разбора.

**Возвращает**:
- `dict`: Представление XML в виде словаря.

**Как работает функция**:
Функция принимает XML строку, разбирает её с помощью `ET.fromstring()` и преобразует полученное дерево элементов в словарь с помощью функции `ET2dict()`.

**Примеры**:

Если вызвать `xml2dict('<root><child>value</child></root>')`, функция вернет `{'root': {'child': {'value': 'value'}}}`.

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

**Назначение**: Преобразует дерево XML элементов в словарь.

**Параметры**:
- `element_tree` (ET.Element): Дерево XML элементов.

**Возвращает**:
- `dict`: Представление дерева XML элементов в виде словаря.

**Как работает функция**:
Функция принимает дерево XML элементов и преобразует его в словарь, используя функцию `_make_dict()` для создания словаря верхнего уровня, и функцию `_parse_node()` для рекурсивного разбора дерева элементов.

**Примеры**:

Если вызвать `ET2dict(ET.fromstring('<root><child>value</child></root>'))`, функция вернет `{'root': {'child': {'value': 'value'}}}`.