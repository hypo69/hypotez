## Анализ кода модуля `html2text`

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код выполняет преобразование HTML в Markdown.
    - Присутствуют настройки для обработки HTML, экспортированного из Google Docs.
    - Поддерживается определение кодировки входных данных.
- **Минусы**:
    - Используются глобальные переменные (например, `UNICODE_SNOB`, `LINKS_EACH_PARAGRAPH`, `BODY_WIDTH`, `SKIP_INTERNAL_LINKS`, `INLINE_LINKS`, `GOOGLE_LIST_INDENT`, `IGNORE_ANCHORS`, `IGNORE_IMAGES`).
    - В коде встречаются устаревшие конструкции, такие как проверка наличия ключа в словаре через `has_key(x, y)` вместо `y in x`.
    - Отсутствуют аннотации типов для переменных и функций.
    - Смешанный стиль кода (использование `True` вместо `1` и `False` вместо `0`).
    - Не хватает документации и комментариев для важных частей кода.
    - Не используется модуль `logger` для логирования.

**Рекомендации по улучшению:**

1.  **Заменить глобальные переменные**:
    - Создать класс `Config` и перенести туда все глобальные переменные, чтобы избежать глобальной области видимости.

2.  **Добавить аннотации типов**:
    - Добавить аннотации типов для всех переменных и аргументов функций.

3.  **Использовать f-strings**:
    - Заменить конкатенацию строк на f-strings для улучшения читаемости.

4.  **Удалить устаревшие конструкции**:
    - Заменить `has_key(x, y)` на `y in x`.
    - Использовать `True` и `False` вместо `1` и `0`.

5.  **Добавить логирование**:
    - Использовать модуль `logger` для логирования ошибок и важных событий.

6.  **Улучшить документацию**:
    - Добавить docstring для всех функций и классов с описанием их назначения, аргументов и возвращаемых значений.

7.  **Рефакторинг кода**:
    - Разбить большие функции на более мелкие и переиспользовать код.
    - Избегать дублирования кода.

8.  **Обработка исключений**:
    - Добавить обработку исключений с использованием `logger.error` для записи ошибок.

9. **Документировать внутренние функции**:
   - Документировать все внутренние функции с использованием docstring.

**Оптимизированный код:**

```python
## \file /src/utils/convertors/html2text.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для преобразования HTML в Markdown
==========================================

Этот модуль предоставляет функции для преобразования HTML-контента в Markdown-форматированный текст.
Он включает в себя парсинг HTML, обработку различных HTML-элементов и преобразование их в соответствующие
Markdown-эквиваленты.

Пример использования
----------------------

>>> from src.utils.convertors.html2text import html2text
>>> html_content = "<p>Это <b>жирный</b> текст.</p>"
>>> markdown_text = html2text(html_content)
>>> print(markdown_text)
Это **жирный** текст.

.. module:: src.utils.convertors.html2text
"""

import html.entities as htmlentitydefs
import urllib.parse as urlparse
import html.parser as HTMLParser
import urllib.request as urllib
import optparse
import re
import sys
import codecs
import types
from textwrap import wrap
from typing import Optional, Dict, List, Any
from pathlib import Path

from src.logger import logger  # Import logger module

class Config:
    """
    Конфигурационный класс для хранения глобальных параметров.
    """
    UNICODE_SNOB: int = 0
    LINKS_EACH_PARAGRAPH: int = 0
    BODY_WIDTH: int = 78
    SKIP_INTERNAL_LINKS: bool = True
    INLINE_LINKS: bool = True
    GOOGLE_LIST_INDENT: int = 36
    IGNORE_ANCHORS: bool = False
    IGNORE_IMAGES: bool = False
    ul_item_mark: str = '*'
    google_doc: bool = False
    hide_strikethrough: bool = False


__version__ = "3.1"
__author__ = "Aaron Swartz (me@aaronsw.com)"
__copyright__ = "(C) 2004-2008 Aaron Swartz. GNU GPL 3."
__contributors__ = ["Martin \'Joey\' Schulze", "Ricardo Reyes", "Kevin Jay North"]


def name2cp(k: str) -> Optional[int]:
    """
    Преобразует имя HTML-сущности в кодовую точку Unicode.

    Args:
        k (str): Имя HTML-сущности.

    Returns:
        Optional[int]: Кодовая точка Unicode или None, если не найдено.
    """
    if k == 'apos':
        return ord("'")
    if hasattr(htmlentitydefs, "name2codepoint"):  # requires Python 2.3
        return htmlentitydefs.name2codepoint.get(k)
    else:
        entity = htmlentitydefs.entitydefs.get(k)
        if entity and entity.startswith("&#") and entity.endswith(";"):
            try:
                return int(entity[2:-1])  # not in latin-1
            except ValueError as ex:
                logger.error(f'Ошибка при преобразовании {entity} в int', ex, exc_info=True)
                return None
        return ord(codecs.latin_1_decode(entity)[0]) if entity else None


unifiable: Dict[str, str] = {'rsquo': "'", 'lsquo': "'", 'rdquo': '"', 'ldquo': '"',
                             'copy': '(C)', 'mdash': '--', 'nbsp': ' ', 'rarr': '->', 'larr': '<-', 'middot': '*',
                             'ndash': '-', 'oelig': 'oe', 'aelig': 'ae',
                             'agrave': 'a', 'aacute': 'a', 'acirc': 'a', 'atilde': 'a', 'auml': 'a', 'aring': 'a',
                             'egrave': 'e', 'eacute': 'e', 'ecirc': 'e', 'euml': 'e',
                             'igrave': 'i', 'iacute': 'i', 'icirc': 'i', 'iuml': 'i',
                             'ograve': 'o', 'oacute': 'o', 'ocirc': 'o', 'otilde': 'o', 'ouml': 'o',
                             'ugrave': 'u', 'uacute': 'u', 'ucirc': 'u', 'uuml': 'u',
                             'lrm': '', 'rlm': ''}

unifiable_n: Dict[Optional[int], str] = {}

for k, v in unifiable.items():
    code_point = name2cp(k)
    if code_point is not None:
        unifiable_n[code_point] = v


def charref(name: str) -> str:
    """
    Преобразует числовую ссылку на символ в символ Unicode.

    Args:
        name (str): Числовая ссылка на символ.

    Returns:
        str: Символ Unicode.
    """
    try:
        if name[0] in ['x', 'X']:
            c = int(name[1:], 16)
        else:
            c = int(name)
    except ValueError as ex:
        logger.error(f'Ошибка при преобразовании {name} в int', ex, exc_info=True)
        return ''

    if not Config.UNICODE_SNOB and c in unifiable_n:
        return unifiable_n.get(c, '')
    else:
        try:
            return chr(c)
        except ValueError as ex:  # catch исключение для недопустимых символов Unicode
            logger.error(f'Недопустимый символ Unicode {c}', ex, exc_info=True)
            return ''


def entityref(c: str) -> str:
    """
    Преобразует ссылку на сущность HTML в символ Unicode.

    Args:
        c (str): Ссылка на сущность HTML.

    Returns:
        str: Символ Unicode.
    """
    if not Config.UNICODE_SNOB and c in unifiable:
        return unifiable.get(c, '')
    else:
        code_point = name2cp(c)
        if code_point is None:
            return f'&{c};'
        try:
            return chr(code_point)
        except ValueError as ex:  # Обработка исключения для недопустимых символов Unicode
            logger.error(f'Недопустимый символ Unicode {code_point}', ex, exc_info=True)
            return f'&{c};'


r_unescape = re.compile(r"&(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));")


def replaceEntities(s: re.Match) -> str:
    """
    Заменяет HTML-сущности в строке.

    Args:
        s (re.Match): Объект Match, содержащий найденную сущность.

    Returns:
        str: Замененная строка.
    """
    s = s.group(1)
    if s[0] == "#":
        return charref(s[1:])
    else:
        return entityref(s)


def unescape(s: str) -> str:
    """
    Удаляет HTML-сущности из строки.

    Args:
        s (str): Строка для обработки.

    Returns:
        str: Строка без HTML-сущностей.
    """
    return r_unescape.sub(replaceEntities, s)


def onlywhite(line: str) -> bool:
    """
    Проверяет, состоит ли строка только из пробельных символов.

    Args:
        line (str): Строка для проверки.

    Returns:
        bool: True, если строка состоит только из пробельных символов, иначе False.
    """
    for c in line:
        if c != ' ' and c != '  ':
            return c == ' '
    return True


def optwrap(text: str) -> str:
    """
    Переносит длинные абзацы в тексте.

    Args:
        text (str): Текст для переноса.

    Returns:
        str: Текст с перенесенными абзацами.
    """
    if not Config.BODY_WIDTH:
        return text

    assert wrap, "Требуется Python 2.3."
    result = ''
    newlines = 0
    for para in text.split("\n"):
        if len(para) > 0:
            if para[0] != ' ' and para[0] != '-' and para[0] != '*':
                for line in wrap(para, Config.BODY_WIDTH):
                    result += line + "\n"
                result += "\n"
                newlines = 2
            else:
                if not onlywhite(para):
                    result += para + "\n"
                    newlines = 1
        else:
            if newlines < 2:
                result += "\n"
                newlines += 1
    return result


def hn(tag: str) -> int:
    """
    Определяет уровень заголовка на основе тега.

    Args:
        tag (str): HTML-тег.

    Returns:
        int: Уровень заголовка (1-9) или 0, если тег не является заголовком.
    """
    if tag[0] == 'h' and len(tag) == 2:
        try:
            n = int(tag[1])
            if n in range(1, 10):
                return n
        except ValueError:
            return 0
    return 0


def dumb_property_dict(style: str) -> Dict[str, str]:
    """
    Преобразует строку CSS-стилей в словарь атрибутов.

    Args:
        style (str): Строка CSS-стилей.

    Returns:
        Dict[str, str]: Словарь атрибутов CSS.
    """
    return dict([(x.strip(), y.strip()) for x, y in [z.split(':', 1) for z in style.split(';') if ':' in z]])


def dumb_css_parser(data: str) -> Dict[str, Dict[str, str]]:
    """
    Парсит CSS-данные и возвращает словарь селекторов с атрибутами.

    Args:
        data (str): CSS-данные.

    Returns:
        Dict[str, Dict[str, str]]: Словарь CSS-селекторов и их атрибутов.
    """
    # Удаляем @import предложения
    import_index = data.find('@import')
    while import_index != -1:
        data = data[:import_index] + data[data.find(';', import_index) + 1:]
        import_index = data.find('@import')

    # Парсим CSS. Возвращено из словарного включения для поддержки старых версий Python
    elements = [x.split('{') for x in data.split('}') if '{' in x.strip()]
    elements = dict([(a.strip(), dumb_property_dict(b)) for a, b in elements])

    return elements


def element_style(attrs: Dict[str, str], style_def: Dict[str, Dict[str, str]], parent_style: Dict[str, str]) -> Dict[str, str]:
    """
    Определяет финальные стили элемента.

    Args:
        attrs (Dict[str, str]): Атрибуты элемента.
        style_def (Dict[str, Dict[str, str]]): Определения стилей.
        parent_style (Dict[str, str]): Стили родительского элемента.

    Returns:
        Dict[str, str]: Финальные стили элемента.
    """
    style = parent_style.copy()
    if 'class' in attrs:
        for css_class in attrs['class'].split():
            css_style = style_def.get('.' + css_class, {})
            style.update(css_style)
    if 'style' in attrs:
        immediate_style = dumb_property_dict(attrs['style'])
        style.update(immediate_style)
    return style


def google_list_style(style: Dict[str, str]) -> str:
    """
    Определяет, является ли список упорядоченным или неупорядоченным (для Google Docs).

    Args:
        style (Dict[str, str]): Стили элемента.

    Returns:
        str: 'ul' для неупорядоченного списка, 'ol' для упорядоченного списка.
    """
    if 'list-style-type' in style:
        list_style = style['list-style-type']
        if list_style in ['disc', 'circle', 'square', 'none']:
            return 'ul'
    return 'ol'


def google_nest_count(style: Dict[str, str]) -> int:
    """
    Вычисляет уровень вложенности списка (для Google Docs).

    Args:
        style (Dict[str, str]): Стили элемента.

    Returns:
        int: Уровень вложенности списка.
    """
    nest_count = 0
    if 'margin-left' in style:
        margin_left = style['margin-left']
        try:
            nest_count = int(margin_left[:-2]) / Config.GOOGLE_LIST_INDENT
        except ValueError as ex:
            logger.error(f'Не удалось преобразовать margin-left {margin_left} в int', ex, exc_info=True)
            return 0
    return nest_count


def google_has_height(style: Dict[str, str]) -> bool:
    """
    Проверяет, определен ли атрибут 'height' в стилях элемента (для Google Docs).

    Args:
        style (Dict[str, str]): Стили элемента.

    Returns:
        bool: True, если атрибут 'height' определен, иначе False.
    """
    return 'height' in style


def google_text_emphasis(style: Dict[str, str]) -> List[str]:
    """
    Возвращает список модификаторов выделения текста (для Google Docs).

    Args:
        style (Dict[str, str]): Стили элемента.

    Returns:
        List[str]: Список модификаторов выделения текста.
    """
    emphasis = []
    if 'text-decoration' in style:
        emphasis.append(style['text-decoration'])
    if 'font-style' in style:
        emphasis.append(style['font-style'])
    if 'font-weight' in style:
        emphasis.append(style['font-weight'])
    return emphasis


def google_fixed_width_font(style: Dict[str, str]) -> bool:
    """
    Проверяет, используется ли шрифт фиксированной ширины (для Google Docs).

    Args:
        style (Dict[str, str]): Стили элемента.

    Returns:
        bool: True, если используется шрифт фиксированной ширины, иначе False.
    """
    font_family = style.get('font-family', '')
    return font_family in ['Courier New', 'Consolas']


def list_numbering_start(attrs: Dict[str, str]) -> int:
    """
    Извлекает начальный номер из атрибутов элемента списка.

    Args:
        attrs (Dict[str, str]): Атрибуты элемента.

    Returns:
        int: Начальный номер списка или 0, если атрибут 'start' отсутствует.
    """
    if 'start' in attrs:
        try:
            return int(attrs['start']) - 1
        except ValueError as ex:
            logger.error(f'Не удалось преобразовать start {attrs["start"]} в int', ex, exc_info=True)
            return 0
    else:
        return 0


class _html2text(HTMLParser.HTMLParser):
    """
    Класс для преобразования HTML в Markdown.
    """

    def __init__(self, out=None, baseurl=''):
        """
        Инициализирует объект класса _html2text.

        Args:
            out (Optional[Callable[[str], None]]): Функция для вывода текста.
            baseurl (str): Базовый URL для разрешения относительных ссылок.
        """
        HTMLParser.HTMLParser.__init__(self)

        if out is None:
            self.out = self.outtextf
        else:
            self.out = out
        self.outtextlist: List[str] = []  # Список для хранения выходных символов
        try:
            self.outtext: str = ""
        except NameError as ex:  # Python3
            logger.error('Проблема совместимости с Python2', ex, exc_info=True)
            self.outtext: str = ""
        self.quiet: int = 0
        self.p_p: int = 0  # Количество символов новой строки для печати перед следующим выводом
        self.outcount: int = 0
        self.start: int = 1
        self.space: int = 0
        self.a: List[Dict[str, str]] = []
        self.astack: List[Optional[Dict[str, str]]] = []
        self.acount: int = 0
        self.list: List[Dict[str, Any]] = []
        self.blockquote: int = 0
        self.pre: int = 0
        self.startpre: int = 0
        self.code: bool = False
        self.br_toggle: str = ''
        self.lastWasNL: bool = False
        self.lastWasList: bool = False
        self.style: int = 0
        self.style_def: Dict[str, Dict[str, str]] = {}
        self.tag_stack: List[Any] = []
        self.emphasis: int = 0
        self.drop_white_space: int = 0
        self.inheader: bool = False
        self.abbr_title: Optional[str] = None  # Текущее определение аббревиатуры
        self.abbr_data: Optional[str] = None  # Последний внутренний HTML (для определения аббревиатуры)
        self.abbr_list: Dict[str, str] = {}  # Стек аббревиатур для записи позже
        self.baseurl: str = baseurl

        if Config.google_doc:
            del unifiable_n[name2cp('nbsp')]
            unifiable['nbsp'] = '&nbsp_place_holder;'

    def feed(self, data: str) -> None:
        """
        Подает данные в парсер HTML.

        Args:
            data (str): HTML-данные.
        """
        data = data.replace("</\' + \'script>", "</ignore>")
        HTMLParser.HTMLParser.feed(self, data)

    def outtextf(self, s: str) -> None:
        """
        Выводит текст.

        Args:
            s (str): Текст для вывода.
        """
        self.outtextlist.append(s)
        if s:
            self.lastWasNL = s[-1] == '\n'

    def close(self) -> str:
        """
        Завершает парсинг HTML и возвращает преобразованный текст.

        Returns:
            str: Преобразованный текст.
        """
        HTMLParser.HTMLParser.close(self)

        self.pbr()
        self.o('', 0, 'end')

        self.outtext = "".join(self.outtextlist)

        if Config.google_doc:
            self.outtext = self.outtext.replace('&nbsp_place_holder;', ' ')

        return self.outtext

    def handle_charref(self, c: str) -> None:
        """
        Обрабатывает числовые ссылки на символы.

        Args:
            c (str): Числовая ссылка на символ.
        """
        self.o(charref(c), 1)

    def handle_entityref(self, c: str) -> None:
        """
        Обрабатывает ссылки на сущности HTML.

        Args:
            c (str): Ссылка на сущность HTML.
        """
        self.o(entityref(c), 1)

    def handle_starttag(self, tag: str, attrs: List[tuple[str, str | None]]) -> None:
        """
        Обрабатывает начальные теги HTML.

        Args:
            tag (str): Имя тега.
            attrs (List[tuple[str, str | None]]): Список атрибутов тега.
        """
        self.handle_tag(tag, attrs, 1)

    def handle_endtag(self, tag: str) -> None:
        """
        Обрабатывает конечные теги HTML.

        Args:
            tag (str): Имя тега.
        """
        self.handle_tag(tag, None, 0)

    def previousIndex(self, attrs: Dict[str, str]) -> Optional[int]:
        """
        Возвращает индекс набора атрибутов (ссылки) в списке self.a.

        Args:
            attrs (Dict[str, str]): Атрибуты ссылки.

        Returns:
            Optional[int]: Индекс набора атрибутов или None, если не найдено.
        """
        if 'href' not in attrs:
            return None

        i = -1
        for a in self.a:
            i += 1
            match = False

            if 'href' in a and a['href'] == attrs['href']:
                if 'title' in a or 'title' in attrs:
                    if ('title' in a and 'title' in attrs and
                            a['title'] == attrs['title']):
                        match = True
                else:
                    match = True

            if match:
                return i
        return None

    def drop_last(self, nLetters: int) -> None:
        """
        Удаляет последние n символов из выходного текста.

        Args:
            nLetters (int): Количество символов для удаления.
        """
        if not self.quiet:
            self.outtext = self.outtext[:-nLetters]

    def handle_emphasis(self, start: bool, tag_style: Dict[str, str], parent_style: Dict[str, str]) -> None:
        """
        Обрабатывает различные текстовые выделения.

        Args:
            start (bool): True, если это начальный тег, иначе False.
            tag_style (Dict[str, str]): Стили текущего тега.
            parent_style (Dict[str, str]): Стили родительского тега.
        """
        tag_emphasis = google_text_emphasis(tag_style)
        parent_emphasis = google_text_emphasis(parent_style)

        # Обрабатываем выделение текста Google
        strikethrough = 'line-through' in tag_emphasis and Config.hide_strikethrough
        bold = 'bold' in tag_emphasis and 'bold' not in parent_emphasis
        italic = 'italic' in tag_emphasis and 'italic' not in parent_emphasis
        fixed = google_fixed_width_font(tag_style) and not \
            google_fixed_width_font(parent_style) and not self.pre

        if start:
            # Зачеркнутый текст должен быть обработан до других атрибутов
            # чтобы не выводить квалификаторы без необходимости
            if bold or italic or fixed:
                self.emphasis += 1
            if strikethrough:
                self.quiet += 1
            if italic:
                self.o("_")
                self.drop_white_space += 1
            if bold:
                self.o("**")
                self.drop_white_space += 1
            if fixed:
                self.o("`")
                self.drop_white_space += 1
                self.code = True
        else:
            if bold or italic or fixed:
                # Не должно быть пробелов перед закрывающим знаком выделения
                self.emphasis -= 1
                self.space = 0
                self.outtext = self.outtext.rstrip()
            if fixed:
                if self.drop_white_space:
                    # Пустое выделение, удаляем его
                    self.drop_last(1)
                    self.drop_white_space -= 1
                else:
                    self.o("`")
                self.code = False
            if bold:
                if self.drop_white_space:
                    # Пустое выделение, удаляем его
                    self.drop_last(2)
                    self.drop_white_space -= 1
                else:
                    self.o("**")
            if italic:
                if self.drop_white_space:
                    # Пустое выделение, удаляем его
                    self.drop_last(1)
                    self.drop_white_space -= 1
                else:
                    self.o("_")
            # Пробел разрешен только после *всех* знаков выделения
            if (bold or italic) and not self.emphasis:
                self.o(" ")
            if strikethrough:
                self.quiet -= 1

    def handle_tag(self, tag: str, attrs: Optional[List[tuple[str, str | None]]], start: bool) -> None:
        """
        Обрабатывает HTML-теги.

        Args:
            tag (str): Имя тега.
            attrs (Optional[List[tuple[str, str | None]]]): Атрибуты тега.
            start (bool): True, если это начальный тег, иначе False.
        """
        if attrs is None:
            attrs = {}
        else:
            attrs = dict(attrs)

        if Config.google_doc:
            # Параметр attrs пуст для закрывающего тега. Кроме того, нам нужны
            # атрибуты родительских узлов, чтобы получить полное описание стиля
            # для текущего элемента. Предполагаем, что Google Docs экспортирует хорошо сформированный HTML.
            parent_style: Dict[str, str] = {}
            if start:
                if self.tag_stack:
                    parent_style = self.tag_stack[-1][2]
                tag_style = element_style(attrs, self.style_def, parent_style)
                self.tag_stack.append((tag, attrs, tag_style))
            else:
                dummy, attrs, tag_style = self.tag_stack.pop()
                if self.tag_stack:
                    parent_style = self.tag_stack[-1][2]

        if hn(tag):
            self.p()
            if start:
                self.inheader = True
                self.o(hn(tag) * "#" + ' ')
            else:
                self.inheader = False
                return  # Предотвращаем избыточные знаки выделения в заголовках

        if tag in ['p', 'div']:
            if Config.google_doc:
                if start and google_has_height(tag_style):
                    self.p()
                else:
                    self.soft_br()
            else:
                self.p()

        if tag == "br" and start:
            self.o("  \n")

        if tag == "hr" and start:
            self.p()
            self.o("* * *")
            self.p()

        if tag in ["head", "style", 'script']:
            if start:
                self.quiet += 1
            else:
                self.quiet -= 1

        if tag == "style":
            if start:
                self.style += 1
            else:
                self.style -= 1

        if tag in ["body"]:
            self.quiet = 0  # Сайты вроде 9rules.com никогда не закрывают <head>

        if tag == "blockquote":
            if start:
                self.p()
                self.o('> ', 0, 1)
                self.start = 1
                self.blockquote += 1
            else:
                self.blockquote -= 1
                self.p()

        if tag in ['em', 'i', 'u']:
            self.o("_")
        if tag in ['strong', 'b']:
            self.o("**")
        if tag in ['del', 'strike']:
            if start:
                self.o("<" + tag + ">")
            else:
                self.o("</" + tag + ">")

        if Config.google_doc:
            if not self.inheader:
                # Обрабатываем некоторые атрибуты шрифта, но оставляем заголовки чистыми
                self.handle_emphasis(start, tag_style, parent_style)

        if tag == "code" and not self.pre:
            self.o("`")  # TODO: `` `this` ``
        if tag == "abbr":
            if start:
                self.abbr_title = None
                self.abbr_data = ''
                if 'title' in attrs:
                    self.abbr_title = attrs['title']
            else:
                if self.abbr_title is not None:
                    self.abbr_list[self.abbr_data] = self.abbr_title
                    self.abbr_title = None
                self.abbr_data = ''

        if tag == "a" and not Config.IGNORE_ANCHORS:
            if start:
                if 'href' in attrs and not (Config.SKIP_INTERNAL_LINKS and attrs['href'].startswith('#')):
                    self.astack.append(attrs)
                    self.o("[")
                else:
                    self.astack.append(None)
            else:
                if self.astack:
                    a = self.astack.pop()
                    if a:
                        if Config.INLINE_LINKS:
                            self.o("](" + a['href'] + ")")
                        else:
                            i = self.previousIndex(a)
                            if i is not None:
                                a = self.a[i]
                            else:
                                self.acount += 1
                                a['count'] = self.acount
                                a['outcount'] = self.outcount
                                self.a.append(a)
                            self.o("][" + str(a['count']) + "]")

        if tag == "img" and start and not Config.IGNORE_IMAGES:
            if 'src' in attrs:
                attrs['href'] = attrs['src']
                alt = attrs.get('alt', '')
                if Config.INLINE_LINKS:
                    self.o("![")
                    self.o(alt)
                    self.o("](" + attrs['href'] + ")")
                else:
                    i = self.previousIndex(attrs)
                    if i is not None:
                        attrs = self.a[i]
                    else:
                        self.acount += 1
                        attrs['count'] = self.acount
                        attrs['outcount'] = self.outcount
                        self.a.append(attrs)
                    self.o("![")
                    self.o(alt)
                    self.o("][" + str(attrs['count']) + "]")

        if tag == 'dl' and start:
            self.p()
        if tag == 'dt' and not start:
            self.pbr()
        if tag == 'dd' and start:
            self.o('    ')
        if tag == 'dd' and not start:
            self.pbr()

        if tag in ["ol", "ul"]:
            # Google Docs создает подсписки как списки верхнего уровня
            if (not self.list) and (not self.lastWasList):
                self.p()
            if start:
                if Config.google_doc:
                    list_style = google_list_style(tag_style)
                else:
                    list_style = tag
                numbering_start = list_numbering_start(attrs)
                self.list.append({'name': list_style, 'num': numbering_start})
            else:
                if self.list:
                    self.list.pop()
            self.lastWasList = True
        else:
            self.lastWasList = False

        if tag == 'li':
            self.pbr()
            if start:
                if self.list:
                    li = self.list[-1