## Как использовать этот блок кода
=========================================================================================

### Описание
-------------------------
Этот блок кода преобразует XML-строку в Python-словарь. 
Он использует библиотеку `xml.etree.ElementTree` для парсинга XML и собственный алгоритм для преобразования результатов в структуру Python-словаря.

### Шаги выполнения
-------------------------
1. **Парсинг XML:** 
    - Функция `xml2dict` принимает XML-строку в качестве аргумента.
    - Используя `ET.fromstring`, код парсит XML-строку, создавая дерево элементов.
    - Затем он вызывает `ET2dict` для дальнейшего преобразования дерева элементов в словарь.

2. **Преобразование дерева в словарь:**
    - Функция `ET2dict` принимает корневой элемент XML-дерева.
    - Она использует `_make_dict` для преобразования элемента в словарь, рекурсивно обрабатывая вложенные элементы.

3. **Рекурсивное преобразование:**
    - Функция `_parse_node` рекурсивно обрабатывает каждый элемент XML-дерева.
    - Она создает словарь, сохраняя имя тега и значение. 
    - Для атрибутов создается отдельный словарь 'attrs'.
    - Она обрабатывает случаи с несколькими элементами с одинаковым именем, сохраняя их в виде списка.

4. **Обработка пространств имен:**
    - Функция `_make_dict` обрабатывает пространства имен в XML-тегах.
    - Она извлекает префикс пространства имен и имя тега, сохраняя их в соответствующие ключи словаря.

### Пример использования
-------------------------
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
```

**Результат:**
```python
{'prestashop': {'xmlns:xlink': 'http://www.w3.org/1999/xlink', 'addresses': [{'address': {'attrs': {'id': '1', 'xlink:href': 'http://localhost:8080/api/addresses/1'}}}, {'address': {'attrs': {'id': '2', 'xlink:href': 'http://localhost:8080/api/addresses/2'}}}, {'address': {'attrs': {'id': '3', 'xlink:href': 'http://localhost:8080/api/addresses/3'}}}, {'address': {'attrs': {'id': '4', 'xlink:href': 'http://localhost:8080/api/addresses/4'}}}, {'address': {'attrs': {'id': '5', 'xlink:href': 'http://localhost:8080/api/addresses/5'}}}, {'address': {'attrs': {'id': '6', 'xlink:href': 'http://localhost:8080/api/addresses/6'}}}, {'address': {'attrs': {'id': '7', 'xlink:href': 'http://localhost:8080/api/addresses/7'}}}, {'address': {'attrs': {'id': '8', 'xlink:href': 'http://localhost:8080/api/addresses/8'}}}]}}
```