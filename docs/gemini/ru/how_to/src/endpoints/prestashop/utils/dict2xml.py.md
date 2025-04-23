### **Инструкция по использованию блока кода**

=========================================================================================

Описание
-------------------------
Этот код преобразует словарь Python в XML-строку. Он рекурсивно обрабатывает словарь, создавая XML-узлы и атрибуты на основе структуры данных. Поддерживаются простые типы данных, такие как строки, числа, а также вложенные словари и списки.

Шаги выполнения
-------------------------
1. **Инициализация**: Функция `dict2xml` принимает словарь `data` и кодировку `encoding` (по умолчанию UTF-8) в качестве аргументов.
2. **Создание документа XML**: Создается новый XML-документ с помощью `getDOMImplementation().createDocument(None, None, None)`.
3. **Обработка корневого элемента**: Вызывается внутренняя функция `_process_complex` для обработки элементов словаря.
4. **Рекурсивное создание узлов**: Функция `_process` рекурсивно обрабатывает элементы словаря, создавая узлы и атрибуты XML.
   - Если значением является словарь с ключом `value`, то берется только значение.
   - Для простых типов (строка, число) создается текстовый узел.
   - Для списков создается список узлов с одинаковым тегом.
   - Для словарей создается узел и добавляются все под узлы.
5. **Обработка атрибутов**: Функция `_process_attr` создает атрибуты для XML-элементов.
6. **Преобразование в XML-строку**: XML-документ преобразуется в строку с заданной кодировкой с помощью `doc.toxml(encoding)`.

Пример использования
-------------------------

```python
    from src.endpoints.prestashop.utils.dict2xml import dict2xml

    data = {
        'prestashop': {
            'address': {
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
                'description': {
                    'language': [
                        {
                            'attrs': {
                                'id': '1',
                                'href': {
                                    'value': 'http://localhost:8080/api/languages/1',
                                    'xmlns': 'http://www.w3.org/1999/xlink'
                                }
                            },
                            'value': 'test description english'
                        },
                        {
                            'attrs': {
                                'id': '2',
                                'href': {
                                    'value': 'http://localhost:8080/api/languages/1',
                                    'xmlns': 'http://www.w3.org/1999/xlink'
                                }
                            },
                            'value': 'test description french'
                        }
                    ]
                }
            }
        }
    }

    xml_string = dict2xml(data)
    print(xml_string)