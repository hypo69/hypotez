### **Инструкции по использованию блока кода для работы с XML**

=========================================================================================

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет функции для очистки XML от пустых элементов и сохранения XML в файл с форматированием. Он использует модули `xml.etree.ElementTree`, `xml.dom.minidom` и `re` для парсинга, очистки и форматирования XML.

Шаги выполнения
-------------------------
1. **Очистка XML от пустых элементов**:
   - Функция `clean_empty_cdata` принимает XML-строку в качестве аргумента.
   - Преобразует XML-строку в объект `ElementTree`.
   - Рекурсивно удаляет все пустые элементы (элементы без текста, атрибутов и дочерних элементов).
   - Удаляет лишние пробелы между тегами.
   - Возвращает очищенную XML-строку.

2. **Сохранение XML в файл**:
   - Функция `save_xml` принимает XML-строку и путь к файлу в качестве аргументов.
   - Вызывает `clean_empty_cdata` для очистки XML.
   - Парсит очищенную XML-строку с помощью `ET.fromstring`.
   - Преобразует XML в удобочитаемую строку с отступами с помощью `minidom.parseString` и `toprettyxml`.
   - Сохраняет отформатированную XML в файл по указанному пути.

Пример использования
-------------------------

```python
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re

def clean_empty_cdata(xml_string: str) -> str:
    """! Cleans empty CDATA sections and unnecessary whitespace in XML string.

    Args:
        xml_string (str): Raw XML content.

    Returns:
        str: Cleaned and formatted XML content.
    """
    root = ET.fromstring(xml_string)
    
    def remove_empty_elements(element):
        for child in list(element):
            remove_empty_elements(child)
            if not (child.text and child.text.strip()) and not child.attrib and not list(child):
                element.remove(child)

    remove_empty_elements(root)
    cleaned_xml = ET.tostring(root, encoding="utf-8").decode("utf-8")
    cleaned_xml = re.sub(r">\s+<", "><", cleaned_xml)  # Remove unnecessary whitespace
    return cleaned_xml

def save_xml(xml_string: str, file_path: str) -> None:
    """! Saves cleaned XML data from a string to a file with indentation.

    Args:
        xml_string (str): XML content as a string.
        file_path (str): Path to the output file.

    Returns:
        None
    """
    # Функция очищает XML от пустых элементов
    cleaned_xml = clean_empty_cdata(xml_string)
    
    # Парсинг XML-строки
    xml_tree = ET.ElementTree(ET.fromstring(cleaned_xml))
    
    # Преобразование в строку с отступами
    rough_string = ET.tostring(xml_tree.getroot(), encoding="utf-8")
    parsed_xml = minidom.parseString(rough_string)
    pretty_xml = parsed_xml.toprettyxml(indent="  ")

    # Сохранение в файл
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(pretty_xml)

# Пример использования
xml_data = "<root><item>Value</item><item attr='test'>Another</item><empty_item></empty_item></root>"
save_xml(xml_data, "output.xml")