### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Этот блок кода предоставляет набор функций для конвертации данных между форматами XML и JSON. Он включает функции для преобразования JSON в XML и XML в JSON (словарь Python). Эти функции полезны при работе с API PrestaShop, который часто использует XML для обмена данными.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортирует `json` для работы с JSON.
   - Импортирует `re` для использования регулярных выражений.
   - Импортирует `xml.etree.ElementTree` как `ET` для работы с XML.

2. **Преобразование JSON в XML**:
   - Функция `dict2xml` преобразует словарь JSON в XML-строку.
   - Функция `presta_fields_to_xml` преобразует JSON в XML с фиксированным корневым элементом "prestashop".

3. **Преобразование XML в JSON**:
   - Функция `xml2dict` преобразует XML-строку в словарь Python.
   - Функция `ET2dict` преобразует дерево элементов XML в словарь Python.
   - Функция `_parse_node` рекурсивно разбирает XML-узел в словарь.
   - Функция `_make_dict` генерирует новый словарь с тегом и значением.

Пример использования
-------------------------

```python
import xml.etree.ElementTree as ET

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

# Преобразование JSON в XML для PrestaShop
def build_xml_element(parent, data):
    """Рекурсивно конструирует XML-элементы из JSON-данных."""
    if isinstance(data, dict):
        for key, value in data.items():
            if key.startswith("@"):  # Attribute
                parent.set(key[1:], value)
            elif key == "#text":  # Text value
                parent.text = value
            else:
                if isinstance(value, list):
                    for item in value:
                        child = ET.SubElement(parent, key)
                        build_xml_element(child, item)
                else:
                    child = ET.SubElement(parent, key)
                    build_xml_element(child, value)
    elif isinstance(data, list):
        for item in data:
            build_xml_element(parent, item)
    else:
        parent.text = str(data)

presta_fields_dict = json_data
if not presta_fields_dict:
    xml_output = ""
else:
    dynamic_key = next(iter(presta_fields_dict))  # Функция извлекает первый ключ (например, \'product\', \'category\' и т. д.)

    # Создаёт корневой элемент "prestashop"
    root = ET.Element("prestashop")
    dynamic_element = ET.SubElement(root, dynamic_key)
    build_xml_element(dynamic_element, presta_fields_dict[dynamic_key])

    # Функция преобразует в строку
    xml_output = ET.tostring(root, encoding="utf-8").decode("utf-8")

print(xml_output)