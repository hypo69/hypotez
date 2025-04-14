### **Анализ кода модуля `src.utils.convertors.dict`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Модуль содержит набор функций для преобразования словарей в различные форматы данных (XML, CSV, JSON, XLS, HTML, PDF) и наоборот.
  - Код хорошо структурирован, с отдельными функциями для каждой операции преобразования.
  - Используются аннотации типов для параметров и возвращаемых значений функций.
  - Есть docstring для каждой функции, что облегчает понимание их назначения и использования.
- **Минусы**:
  - В коде встречается смешение стилей кавычек (как одинарных, так и двойных), что не соответствует стандарту.
  - Отсутствует единый стиль форматирования.
  - Некоторые docstring написаны на английском языке.
  - Не везде используется модуль `logger` для логирования исключений и ошибок.
  - Некоторые функции содержат неполные примеры использования или отсутствуют.
  - Не все функции имеют подробные docstring, описывающие их поведение и возможные исключения.

**Рекомендации по улучшению:**

1. **Форматирование кода**:
   - Привести весь код к единому стилю форматирования, используя только одинарные кавычки.
   - Добавить пробелы вокруг операторов присваивания.
   - Устранить смешение стилей кавычек.

2. **Комментарии и документация**:
   - Перевести все docstring на русский язык.
   - Дополнить docstring подробным описанием работы каждой функции, включая возможные исключения и примеры использования.
   - Уточнить docstring для внутренних функций, таких как `_process_simple`, `_process_attr` и `_process_complex` в функции `dict2xml`.

3. **Логирование**:
   - Добавить логирование с использованием модуля `logger` для обработки исключений и ошибок.

4. **Обработка исключений**:
   - Использовать `ex` вместо `e` в блоках обработки исключений.
   - Добавить обработку возможных исключений в функциях, где они могут возникнуть (например, при работе с файлами).

5. **Улучшение функциональности**:
   - Добавить проверку типов входных данных для повышения надежности функций.
   - Реализовать функцию `json2xml`, которая сейчас только объявлена как пример.
   - Рассмотреть возможность добавления обработки исключений в функциях сохранения файлов (CSV, XLS, PDF).

6. **Структура кода**:
   - Пересмотреть структуру модуля, чтобы выделить логически связанные функции в отдельные подмодули, если это необходимо.

**Оптимизированный код:**

```python
## \file /src/utils/convertors/dict.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для преобразования данных между форматами dict и SimpleNamespace
========================================================================

Модуль содержит функции для рекурсивного преобразования словарей в объекты SimpleNamespace и наоборот,
а также для экспорта данных в различные форматы, такие как XML, CSV, JSON, XLS, HTML и PDF.

Пример использования
----------------------

>>> from types import SimpleNamespace
>>> data = {'name': 'Example', 'value': 123}
>>> ns = dict2ns(data)
>>> print(ns.name)
Example
"""

import json
import xml.etree.ElementTree as ET
from types import SimpleNamespace
from typing import Any, Dict, List, Optional
from pathlib import Path
from xml.dom.minidom import getDOMImplementation

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from src.utils.xls import save_xls_file
from src.utils.csv import save_csv_file
from src.logger import logger


def replace_key_in_dict(data: dict | list, old_key: str, new_key: str) -> dict:
    """
    Рекурсивно заменяет ключ в словаре или списке.

    Args:
        data (dict | list): Словарь или список, в котором производится замена ключа.
        old_key (str): Ключ, который нужно заменить.
        new_key (str): Новый ключ.

    Returns:
        dict: Обновленный словарь с замененными ключами.

    Example Usage:

        replace_key_in_dict(data, 'name', 'category_name')

        # Example 1: Simple dictionary
        data = {'old_key': 'value'}
        updated_data = replace_key_in_dict(data, 'old_key', 'new_key')
        # updated_data becomes {'new_key': 'value'}

        # Example 2: Nested dictionary
        data = {'outer': {'old_key': 'value'}}
        updated_data = replace_key_in_dict(data, 'old_key', 'new_key')
        # updated_data becomes {'outer': {'new_key': 'value'}}

        # Example 3: List of dictionaries
        data = [{'old_key': 'value1'}, {'old_key': 'value2'}]
        updated_data = replace_key_in_dict(data, 'old_key', 'new_key')
        # updated_data becomes [{'new_key': 'value1'}, {'new_key': 'value2'}]

        # Example 4: Mixed nested structure with lists and dictionaries
        data = {'outer': [{'inner': {'old_key': 'value'}}]}
        updated_data = replace_key_in_dict(data, 'old_key', 'new_key')
        # updated_data becomes {'outer': [{'inner': {'new_key': 'value'}}]}

    Raises:
        TypeError: Если входные данные не являются словарем или списком.
    """
    if isinstance(data, dict):
        for key in list(data.keys()):
            if key == old_key:
                data[new_key] = data.pop(old_key)
            if isinstance(data[key], (dict, list)):
                replace_key_in_dict(data[key], old_key, new_key)
    elif isinstance(data, list):
        for item in data:
            replace_key_in_dict(item, old_key, new_key)
    else:
        raise TypeError('Data must be a dict or list')

    return data


def dict2pdf(data: dict | SimpleNamespace, file_path: str | Path) -> None:
    """
    Сохраняет данные из словаря в PDF-файл.

    Args:
        data (dict | SimpleNamespace): Словарь с данными для сохранения в PDF.
        file_path (str | Path): Путь к выходному PDF-файлу.

    Raises:
        TypeError: Если входные данные не являются словарем или SimpleNamespace.
        Exception: Если возникает ошибка при создании PDF-файла.
    """
    try:
        if isinstance(data, SimpleNamespace):
            data = data.__dict__

        pdf = canvas.Canvas(str(file_path), pagesize=A4)
        width, height = A4
        x, y = 50, height - 50

        pdf.setFont('Helvetica', 12)

        for key, value in data.items():
            line = f'{key}: {value}'
            pdf.drawString(x, y, line)
            y -= 20

            if y < 50:  # Создать новую страницу, если места недостаточно
                pdf.showPage()
                pdf.setFont('Helvetica', 12)
                y = height - 50

        pdf.save()
    except TypeError as ex:
        logger.error('Неверный тип данных', ex, exc_info=True)
        raise
    except Exception as ex:
        logger.error('Ошибка при создании PDF-файла', ex, exc_info=True)
        raise


def dict2ns(data: Dict[str, Any] | List[Any]) -> Any:
    """
    Рекурсивно преобразует словари в объекты SimpleNamespace.

    Args:
        data (Dict[str, Any] | List[Any]): Данные для преобразования.

    Returns:
        Any: Преобразованные данные в виде SimpleNamespace или списка SimpleNamespace.

    Raises:
        TypeError: Если входные данные не являются словарем или списком.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = dict2ns(value)
            elif isinstance(value, list):
                data[key] = [dict2ns(item) if isinstance(item, dict) else item for item in value]
        return SimpleNamespace(**data)
    elif isinstance(data, list):
        return [dict2ns(item) if isinstance(item, dict) else item for item in data]
    else:
        raise TypeError('Data must be a dict or list')


def dict2xml(data: Dict[str, Any], encoding: str = 'UTF-8') -> str:
    """
    Генерирует XML-строку из словаря.

    Args:
        data (Dict[str, Any]): Данные для преобразования в XML.
        encoding (str, optional): Кодировка данных. По умолчанию 'UTF-8'.

    Returns:
        str: XML-строка, представляющая входной словарь.

    Raises:
        Exception: Если предоставлено более одного корневого узла.
    """

    def _process_simple(doc, tag, tag_value):
        """
        Генерирует узел для простых типов (int, str).

        Args:
            doc (xml.dom.minidom.Document): Объект XML-документа.
            tag (str): Имя тега для XML-элемента.
            tag_value (Any): Значение тега.

        Returns:
            xml.dom.minidom.Element: Узел, представляющий тег и значение.
        """
        node = doc.createElement(tag)
        node.appendChild(doc.createTextNode(str(tag_value)))
        return node

    def _process_attr(doc, attr_value: Dict[str, Any]):
        """
        Генерирует атрибуты для XML-элемента.

        Args:
            doc (xml.dom.minidom.Document): Объект XML-документа.
            attr_value (Dict[str, Any]): Словарь атрибутов.

        Returns:
            List[xml.dom.minidom.Attr]: Список атрибутов для XML-элемента.
        """
        attrs = []
        for attr_name, value in attr_value.items():
            attr = doc.createAttribute(attr_name)
            attr.nodeValue = value if not isinstance(value, dict) else value.get('value', '')
            attrs.append(attr)
        return attrs

    def _process_complex(doc, children):
        """
        Генерирует узлы для сложных типов, таких как списки или словари.

        Args:
            doc (xml.dom.minidom.Document): Объект XML-документа.
            children (List[Tuple[str, Any]]): Список пар тег-значение.

        Returns:
            Tuple[List[xml.dom.minidom.Element], List[xml.dom.minidom.Attr]]: Список дочерних узлов и атрибутов.
        """
        nodelist = []
        attrs = []
        for tag, value in children:
            if tag == 'attrs':
                attrs = _process_attr(doc, value)
            else:
                nodes = _process(doc, tag, value)
                nodelist.extend(nodes if isinstance(nodes, list) else [nodes])
        return nodelist, attrs

    def _process(doc, tag, tag_value):
        """
        Генерирует XML DOM-объект для тега и его значения.

        Args:
            doc (xml.dom.minidom.Document): Объект XML-документа.
            tag (str): Имя тега для XML-элемента.
            tag_value (Any): Значение тега.

        Returns:
            xml.dom.minidom.Element | List[xml.dom.minidom.Element]: Узел или список узлов для тега и значения.
        """
        if isinstance(tag_value, dict) and list(tag_value.keys()) == ['value']:
            tag_value = tag_value['value']

        if tag_value is None:
            tag_value = ''

        if isinstance(tag_value, (float, int, str)):
            return _process_simple(doc, tag, tag_value)

        if isinstance(tag_value, list):
            return _process_complex(doc, [(tag, x) for x in tag_value])[0]

        if isinstance(tag_value, dict):
            node = doc.createElement(tag)
            nodelist, attrs = _process_complex(doc, tag_value.items())
            for child in nodelist:
                node.appendChild(child)
            for attr in attrs:
                node.setAttributeNode(attr)
            return node

    doc = getDOMImplementation().createDocument(None, None, None)
    if len(data) > 1:
        raise Exception('Only one root node allowed')

    root, _ = _process_complex(doc, data.items())
    doc.appendChild(root[0])
    return doc.toxml(encoding)


def dict2csv(data: dict | SimpleNamespace, file_path: str | Path) -> bool:
    """
    Сохраняет данные из словаря или SimpleNamespace в CSV-файл.

    Args:
        data (dict | SimpleNamespace): Данные для сохранения в CSV-файл.
        file_path (str | Path): Путь к CSV-файлу.

    Returns:
        bool: True, если файл успешно сохранен, False в противном случае.
    
    Raises:
        TypeError: Если входные данные не являются словарем или SimpleNamespace.
        Exception: Если возникает ошибка при сохранении CSV-файла.
    """
    try:
        if not isinstance(data, (dict, SimpleNamespace)):
            raise TypeError('Data must be a dict or SimpleNamespace')
        return save_csv_file(data, file_path)
    except TypeError as ex:
        logger.error('Неверный тип данных', ex, exc_info=True)
        return False
    except Exception as ex:
        logger.error('Ошибка при сохранении CSV-файла', ex, exc_info=True)
        return False


def dict2xls(data: dict | SimpleNamespace, file_path: str | Path) -> bool:
    """
    Сохраняет данные из словаря или SimpleNamespace в XLS-файл.

    Args:
        data (dict | SimpleNamespace): Данные для сохранения в XLS-файл.
        file_path (str | Path): Путь к XLS-файлу.

    Returns:
        bool: True, если файл успешно сохранен, False в противном случае.
    
    Raises:
        TypeError: Если входные данные не являются словарем или SimpleNamespace.
        Exception: Если возникает ошибка при сохранении XLS-файла.
    """
    try:
        if not isinstance(data, (dict, SimpleNamespace)):
            raise TypeError('Data must be a dict or SimpleNamespace')
        return save_xls_file(data, file_path)
    except TypeError as ex:
        logger.error('Неверный тип данных', ex, exc_info=True)
        return False
    except Exception as ex:
        logger.error('Ошибка при сохранении XLS-файла', ex, exc_info=True)
        return False


def dict2html(data: dict | SimpleNamespace, encoding: str = 'UTF-8') -> str:
    """
    Генерирует HTML-строку таблицы из словаря или объекта SimpleNamespace.

    Args:
        data (dict | SimpleNamespace): Данные для преобразования в HTML.
        encoding (str, optional): Кодировка данных. По умолчанию 'UTF-8'.

    Returns:
        str: HTML-строка, представляющая входной словарь.
    
    Raises:
        TypeError: Если входные данные не являются словарем или SimpleNamespace.
    """

    def dict_to_html_table(data: dict, depth: int = 0) -> str:
        """
        Рекурсивно преобразует словарь в HTML-таблицу.

        Args:
            data (dict): Данные словаря для преобразования.
            depth (int, optional): Глубина рекурсии, используется для вложенных таблиц. По умолчанию 0.

        Returns:
            str: HTML-таблица в виде строки.
        """
        html = ['<table border="1" cellpadding="5" cellspacing="0">']

        if isinstance(data, dict):
            for key, value in data.items():
                html.append('<tr>')
                html.append(f'<td><strong>{key}</strong></td>')
                if isinstance(value, dict):
                    html.append(f'<td>{dict_to_html_table(value, depth + 1)}</td>')
                elif isinstance(value, list):
                    html.append('<td>')
                    html.append('<ul>')
                    for item in value:
                        html.append(f'<li>{item}</li>')
                    html.append('</ul>')
                    html.append('</td>')
                else:
                    html.append(f'<td>{value}</td>')
                html.append('</tr>')
        else:
            html.append(f'<tr><td colspan="2">{data}</td></tr>')

        html.append('</table>')
        return '\n'.join(html)

    # Convert data to dictionary if it's a SimpleNamespace
    if isinstance(data, SimpleNamespace):
        data = data.__dict__

    if not isinstance(data, dict):
        raise TypeError('Data must be a dict or SimpleNamespace')

    html_content = dict_to_html_table(data)
    return f'<!DOCTYPE html>\n<html>\n<head>\n<meta charset="{encoding}">\n<title>Dictionary to HTML</title>\n</head>\n<body>\n{html_content}\n</body>\n</html>'


def json2xml(json_data: Dict[str, Any], encoding: str = 'UTF-8') -> str:
    """
    Преобразует JSON-данные в XML-строку.

    Args:
        json_data (Dict[str, Any]): JSON-данные для преобразования.
        encoding (str, optional): Кодировка данных. По умолчанию 'UTF-8'.

    Returns:
        str: XML-строка, представляющая входные JSON-данные.

    Raises:
        NotImplementedError: Если функция еще не реализована.
    """
    raise NotImplementedError('Функция json2xml еще не реализована')


def example_json2xml():
    """
    Пример использования функции json2xml.
    """
    # Example usage
    json_data = {
        'product': {
            'name': {
                'language': [
                    {
                        '@id': '1',
                        '#text': 'Test Product'
                    },
                    {
                        '@id': '2',
                        '#text': 'Test Product'
                    },
                    {
                        '@id': '3',
                        '#text': 'Test Product'
                    }
                ]
            },
            'price': '10.00',
            'id_tax_rules_group': '13',
            'id_category_default': '2'
        }
    }

    xml_output = json2xml(json_data)
    print(xml_output)


if __name__ == '__main__':
    ...
    # example_json2xml()