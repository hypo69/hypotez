# Модуль dict2xml

## Обзор

Модуль `dict2xml` предоставляет функцию `dict2xml`, которая преобразует словарь Python в XML-строку. Этот модуль был адаптирован из библиотеки `lhammer` для использования в `Prestapyt`. 

## Подробности

Этот модуль используется для генерации XML-строки из словаря Python. Он может быть использован для отправки данных в веб-сервисы, которые принимают XML-формат. Модуль `dict2xml` использует библиотеку `xml.dom.minidom` для создания XML-документа.

## Функции

### `dict2xml(data, encoding='UTF-8')`

**Назначение**: Преобразует словарь Python в XML-строку.

**Параметры**:
- `data` (dict): Словарь Python, который нужно преобразовать.
- `encoding` (str, optional): Кодировка данных. По умолчанию `UTF-8`.

**Возвращает**:
- `str`: XML-строка.

**Вызывает исключения**:
- `Exception`: Возникает, если словарь содержит более одного корневого узла.

**Как работает функция**:
- Функция `dict2xml` принимает словарь Python в качестве аргумента и возвращает XML-строку.
- Сначала создается объект `xml.dom.minidom.Document`.
- Затем, используя рекурсивные функции `_process`, `_process_complex` и `_process_simple`, словарь преобразуется в структуру XML-документа.
- В конце функция `toxml` объекта `xml.dom.minidom.Document` используется для генерации XML-строки.

**Примеры**:
```python
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
```

## Внутренние функции

### `_process(doc, tag, tag_value)`

**Назначение**: Генерирует объект DOM для тега и его значения.

**Параметры**:
- `doc`: Объект `xml.dom.minidom.Document`.
- `tag`: Имя тега.
- `tag_value`: Значение тега.

**Возвращает**:
- `xml.dom.minidom.Node` или `xml.dom.minidom.NodeList`.

**Как работает функция**:
- Функция `_process` рекурсивно обрабатывает значение тега и создает соответствующий объект DOM. 
- Если значение тега - это словарь, содержащий только ключ `'value'`, значение извлекается из этого ключа.
- Если значение тега - это список, создается список объектов DOM с тем же именем тега для каждого элемента списка.
- Если значение тега - это словарь, создается новый объект DOM с именем тега, в который добавляются под-узлы из словаря. 
- Если значение тега - это простой тип (int, str, float), создается простой объект DOM с заданным именем тега и значением.

### `_process_complex(doc, children)`

**Назначение**: Генерирует список узлов DOM для списка или словаря.

**Параметры**:
- `doc`: Объект `xml.dom.minidom.Document`.
- `children`: Список кортежей (`tag`, `value`), где `tag` - имя тега, а `value` - значение тега.

**Возвращает**:
- `xml.dom.minidom.NodeList`, список атрибутов.

**Как работает функция**:
- Функция `_process_complex` проходит по списку кортежей (`tag`, `value`) и для каждого элемента создает объект DOM с помощью функции `_process`.
- Если имя тега - `'attrs'`, узлы добавляются в список атрибутов.
- Возвращает список узлов DOM и список атрибутов.

### `_process_attr(doc, attr_value)`

**Назначение**: Генерирует атрибуты элемента.

**Параметры**:
- `doc`: Объект `xml.dom.minidom.Document`.
- `attr_value`: Значение атрибута.

**Возвращает**:
- `list`: Список атрибутов.

**Как работает функция**:
- Функция `_process_attr` проходит по значениям атрибутов и для каждого элемента создает объект `xml.dom.minidom.Attr`. 
- Если значение атрибута - это словарь, создается атрибут с пространством имен, заданным в словаре.
- В противном случае создается атрибут без пространства имен.
- Возвращает список атрибутов.

### `_process_simple(doc, tag, tag_value)`

**Назначение**: Генерирует узел DOM для простых типов (int, str).

**Параметры**:
- `doc`: Объект `xml.dom.minidom.Document`.
- `tag`: Имя тега.
- `tag_value`: Значение тега.

**Возвращает**:
- `xml.dom.minidom.Node`.

**Как работает функция**:
- Функция `_process_simple` создает новый объект DOM с заданным именем тега и значением. 
- Затем создается объект `xml.dom.minidom.Text`, в который записывается значение тега.
- Объект `xml.dom.minidom.Text` добавляется как дочерний узел к объекту DOM.
- Возвращает объект DOM.