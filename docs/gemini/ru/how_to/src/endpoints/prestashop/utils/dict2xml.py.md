## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода представляет функцию `dict2xml`, которая позволяет преобразовать словарь Python в строку XML-кода.

Шаги выполнения
-------------------------
1. **Создание XML-документа:**  Функция использует библиотеку `xml.dom.minidom` для создания нового XML-документа.
2. **Обработка вложенных данных:**  Рекурсивная функция `_process` обрабатывает вложенные структуры данных в словаре. Она анализирует типы данных (строки, числа, списки, словари) и создает соответствующие узлы XML.
3. **Создание узлов:** Для каждого элемента словаря функция создает соответствующий узел XML. Для вложенных словарей рекурсивно вызывается функция `_process`.
4. **Обработка атрибутов:**  Для атрибутов элементов используются отдельные функции: `_process_attr`, `_process_complex`.
5. **Преобразование в строку:** После построения структуры XML-документа функция `doc.toxml(encoding)` преобразует его в строку XML-кода.

Пример использования
-------------------------

```python
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

**Важно:** Данный блок кода предназначен для преобразования словарей в XML-строки. Он работает с разными типами данных, включая списки, словари и атрибуты.