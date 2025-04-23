## \file /src/utils/convertors/md2dict.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: src.utils.convertors.md2dict 
	:platform: Windows, Unix
	:synopsis: Модуль для конвертации строки Markdown в структурированный словарь, включая извлечение JSON содержимого, если оно присутствует.
"""

import re
from typing import Dict, List, Any
from markdown2 import markdown
from src.logger.logger import logger


def md2html(md_string: str, extras: List[str] = None) -> str:
    """
    Конвертирует строку Markdown в HTML.

    Args:
        md_string (str): Строка Markdown для конвертации.
        extras (list, optional): Список расширений markdown2. Defaults to None.

    Returns:
        str: HTML-представление Markdown.
    """
    try:
        if extras is None:
            return markdown(md_string)
        return markdown(md_string, extras=extras)
    except Exception as ex:
        logger.error("Ошибка при преобразовании Markdown в HTML.", exc_info=True)
        return ""


def md2dict(md_string: str, extras: List[str] = None) -> Dict[str, list[str]]:
    """
    Конвертирует строку Markdown в структурированный словарь.

    Args:
        md_string (str): Строка Markdown для конвертации.
        extras (list, optional): Список расширений markdown2 для md2html. Defaults to None.

    Returns:
         Dict[str, list[str]]: Структурированное представление Markdown содержимого.
    """
    try:

        html = md2html(md_string, extras)
        sections: Dict[str, list[str]] = {}
        current_section: str | None = None

        for line in html.splitlines():
            if line.startswith('<h'):
                heading_level_match = re.search(r'h(\\d)', line)
                if heading_level_match:
                    heading_level = int(heading_level_match.group(1))
                    section_title = re.sub(r'<.*?>', '', line).strip()
                    if heading_level == 1:
                        current_section = section_title
                        sections[current_section] = []
                    elif current_section:
                        sections[current_section].append(section_title)

            elif line.strip() and current_section:
                clean_text = re.sub(r'<.*?>', '', line).strip()
                sections[current_section].append(clean_text)

        return sections

    except Exception as ex:
        logger.error("Ошибка при парсинге Markdown в структурированный словарь.", exc_info=True)
        return {}
                
Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код преобразует строку в формате Markdown в структурированный словарь, где ключами являются заголовки первого уровня, а значениями - списки, содержащие подзаголовки и текст, относящиеся к этим заголовкам. Сначала Markdown преобразуется в HTML, затем HTML анализируется для извлечения структуры.

Шаги выполнения
-------------------------
1. **Преобразование Markdown в HTML**: Функция `md2html` преобразует входную строку Markdown в HTML с использованием библиотеки `markdown2`. Если указаны дополнительные расширения (`extras`), они также используются при преобразовании.
2. **Инициализация структуры данных**: Создается пустой словарь `sections`, который будет содержать структурированные данные из Markdown.
3. **Обработка строк HTML**: Код проходит по каждой строке HTML. Если строка начинается с тега заголовка (`<h`), извлекается уровень заголовка и текст заголовка.
4. **Определение секций**: Если уровень заголовка равен 1, устанавливается текущая секция (`current_section`), и в словарь `sections` добавляется новый ключ с названием секции и пустым списком в качестве значения.
5. **Добавление контента в секции**: Если строка содержит текст и текущая секция определена, текст очищается от HTML-тегов и добавляется в список, соответствующий текущей секции.
6. **Возврат структурированного словаря**: После обработки всех строк HTML функция возвращает словарь `sections`, содержащий структурированное представление Markdown.

Пример использования
-------------------------

```python
from src.utils.convertors.md import md2dict

markdown_text = """
# Заголовок первого уровня
Текст, относящийся к первому уровню.
## Заголовок второго уровня
Текст, относящийся ко второму уровню.
"""

result = md2dict(markdown_text)
print(result)
#  {'Заголовок первого уровня': ['Текст, относящийся к первому уровню.', 'Заголовок второго уровня', 'Текст, относящийся ко второму уровню.']}