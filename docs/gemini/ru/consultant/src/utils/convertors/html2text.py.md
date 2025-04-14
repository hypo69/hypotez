### **Анализ кода модуля `html2text`**

#### **Качество кода**:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код выполняет полезную функцию преобразования HTML в Markdown.
    - Присутствуют базовые комментарии и метаданные модуля.
- **Минусы**:
    - Отсутствует подробная документация функций и классов.
    - Используются устаревшие конструкции, такие как `has_key`.
    - Не хватает единообразия в стиле кодирования.
    - Переменные не аннотированы типами.
    - Нет логирования.
    - Docstring написаны на английском языке.

#### **Рекомендации по улучшению**:

1.  **Документирование кода**:
    *   Добавить docstring к каждой функции и классу, описывающие их назначение, параметры, возвращаемые значения и возможные исключения.
    *   Перевести существующие docstring на русский язык.
    *   Использовать более конкретные и понятные комментарии.
2.  **Стандартизация кода**:
    *   Заменить `has_key(x, y)` на `y in x`.
    *   Добавить аннотации типов для переменных и параметров функций.
    *   Удалить неиспользуемые импорты.
3.  **Логирование**:
    *   Добавить логирование для отслеживания ошибок и предупреждений.
4.  **Обработка исключений**:
    *   Использовать `ex` вместо `e` в блоках `except`.
5.  **Обновление зависимостей**:
    *   Рассмотреть возможность обновления используемых библиотек, таких как `html.parser`.
6.  **Улучшение структуры**:
    *   Разбить крупные функции на более мелкие и управляемые.
    *   Использовать более современные методы работы со строками и регулярными выражениями.
7.  **Перевод docstring на русский язык**
8.  **Заменить множественное определение типа с `Union[]` на `|`**

#### **Оптимизированный код**:

```python
## \file /src/utils/convertors/html2text.py
# -*- coding: utf-8 -*-

"""
Модуль для преобразования HTML в Markdown
==========================================

Модуль содержит класс `_html2text`, который используется для преобразования HTML-кода в Markdown-форматированный текст.

Пример использования
----------------------

>>> from src.utils.convertors.html2text import html2text
>>> html_content = "<h1>Заголовок</h1><p>Текст параграфа.</p>"
>>> markdown_text = html2text(html_content)
>>> print(markdown_text)
# Заголовок

Текст параграфа.
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
from typing import Optional, List
from src.logger import logger

# Use Unicode characters instead of their ascii psuedo-replacements
UNICODE_SNOB: int = 0

# Put the links after each paragraph instead of at the end.
LINKS_EACH_PARAGRAPH: int = 0

# Wrap long lines at position. 0 for no wrapping. (Requires Python 2.3.)
BODY_WIDTH: int = 78

# Don't show internal links (href="#local-anchor") -- corresponding link targets
# won't be visible in the plain text file anyway.
SKIP_INTERNAL_LINKS: bool = True

# Use inline, rather than reference, formatting for images and links
INLINE_LINKS: bool = True

# Number of pixels Google indents nested lists
GOOGLE_LIST_INDENT: int = 36

IGNORE_ANCHORS: bool = False
IGNORE_IMAGES: bool = False

### Entity Nonsense ###

def name2cp(k: str) -> Optional[int]:
    """
    Преобразует имя HTML-сущности в кодовую точку Unicode.

    Args:
        k (str): Имя HTML-сущности.

    Returns:
        Optional[int]: Кодовая точка Unicode или None, если не найдена.
    """
    if k == 'apos':
        return ord("\'")
    if hasattr(htmlentitydefs, "name2codepoint"):  # requires Python 2.3
        return htmlentitydefs.name2codepoint[k]
    else:
        k = htmlentitydefs.entitydefs[k]
        if k.startswith("&#") and k.endswith(";"):
            return int(k[2:-1])  # not in latin-1
        return ord(codecs.latin_1_decode(k)[0])

unifiable: dict[str, str] = {'rsquo': "'", 'lsquo': "'", 'rdquo': '"', 'ldquo': '"',
'copy': '(C)', 'mdash': '--', 'nbsp': ' ', 'rarr': '->', 'larr': '<-', 'middot': '*',
'ndash': '-', 'oelig': 'oe', 'aelig': 'ae',
'agrave': 'a', 'aacute': 'a', 'acirc': 'a', 'atilde': 'a', 'auml': 'a', 'aring': 'a',
'egrave': 'e', 'eacute': 'e', 'ecirc': 'e', 'euml': 'e',
'igrave': 'i', 'iacute': 'i', 'icirc': 'i', 'iuml': 'i',
'ograve': 'o', 'oacute': 'o', 'ocirc': 'o', 'otilde': 'o', 'ouml': 'o',
'ugrave': 'u', 'uacute': 'u', 'ucirc': 'u', 'uuml': 'u',
'lrm': '', 'rlm': ''}

unifiable_n: dict[int, str] = {}

for k in unifiable.keys():
    unifiable_n[name2cp(k)] = unifiable[k]

def charref(name: str) -> str:
    """
    Преобразует числовую ссылку на символ в символ Unicode.

    Args:
        name (str): Числовая ссылка на символ.

    Returns:
        str: Символ Unicode.
    """
    if name[0] in ['x', 'X']:
        c = int(name[1:], 16)
    else:
        c = int(name)

    if not UNICODE_SNOB and c in unifiable_n.keys():
        return unifiable_n[c]
    else:
        try:
            return chr(c)
        except NameError:  # Python3
            return chr(c)

def entityref(c: str) -> str:
    """
    Преобразует ссылку на сущность HTML в символ Unicode.

    Args:
        c (str): Ссылка на сущность HTML.

    Returns:
        str: Символ Unicode.
    """
    if not UNICODE_SNOB and c in unifiable.keys():
        return unifiable[c]
    else:
        try:
            name2cp(c)
        except KeyError:
            return "&" + c + ';'
        else:
            try:
                return chr(name2cp(c))
            except NameError:  # Python3
                return chr(name2cp(c))

def replaceEntities(s: re.Match) -> str:
    """
    Заменяет HTML-сущности в строке.

    Args:
        s (re.Match): Объект Match, содержащий HTML-сущность.

    Returns:
        str: Замененная строка.
    """
    s = s.group(1)
    if s[0] == "#":
        return charref(s[1:])
    else:
        return entityref(s)

r_unescape: re.Pattern = re.compile(r"&(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));")

def unescape(s: str) -> str:
    """
    Удаляет HTML-сущности из строки.

    Args:
        s (str): Исходная строка.

    Returns:
        str: Строка без HTML-сущностей.
    """
    return r_unescape.sub(replaceEntities, s)

### End Entity Nonsense ###

def onlywhite(line: str) -> bool:
    """
    Проверяет, состоит ли строка только из пробельных символов.

    Args:
        line (str): Проверяемая строка.

    Returns:
        bool: True, если строка состоит только из пробельных символов, иначе False.
    """
    for c in line:
        if c != ' ' and c != '  ':
            return c == ' '
    return line

def optwrap(text: str) -> str:
    """
    Переносит текст по заданной ширине.

    Args:
        text (str): Исходный текст.

    Returns:
        str: Текст, перенесенный по ширине.
    """
    if not BODY_WIDTH:
        return text

    assert wrap, "Requires Python 2.3."
    result: str = ''
    newlines: int = 0
    for para in text.split("\\n"):
        if len(para) > 0:
            if para[0] != ' ' and para[0] != '-' and para[0] != '*':
                for line in wrap(para, BODY_WIDTH):
                    result += line + "\\n"
                result += "\\n"
                newlines = 2
            else:
                if not onlywhite(para):
                    result += para + "\\n"
                    newlines = 1
        else:
            if newlines < 2:
                result += "\\n"
                newlines += 1
    return result

def hn(tag: str) -> Optional[int]:
    """
    Определяет уровень заголовка HTML.

    Args:
        tag (str): HTML-тег.

    Returns:
        Optional[int]: Уровень заголовка (1-9) или None, если это не заголовок.
    """
    if tag[0] == 'h' and len(tag) == 2:
        try:
            n = int(tag[1])
            if n in range(1, 10):
                return n
        except ValueError:
            return None
    return None

def dumb_property_dict(style: str) -> dict[str, str]:
    """
    Преобразует строку CSS-стилей в словарь.

    Args:
        style (str): Строка CSS-стилей.

    Returns:
        dict[str, str]: Словарь CSS-свойств.
    """
    return dict([(x.strip(), y.strip()) for x, y in [z.split(':', 1) for z in style.split(';') if ':' in z]])

def dumb_css_parser(data: str) -> dict[str, dict[str, str]]:
    """
    Разбирает CSS-данные и возвращает словарь селекторов и их свойств.

    Args:
        data (str): CSS-данные.

    Returns:
        dict[str, dict[str, str]]: Словарь CSS-селекторов и их свойств.
    """
    # remove @import sentences
    importIndex: int = data.find('@import')
    while importIndex != -1:
        data = data[0:importIndex] + data[data.find(';', importIndex) + 1:]
        importIndex = data.find('@import')

    # parse the css. reverted from dictionary compehension in order to support older pythons
    elements: list[list[str]] = [x.split('{') for x in data.split('}') if '{' in x.strip()]
    elements = dict([(a.strip(), dumb_property_dict(b)) for a, b in elements])

    return elements

def element_style(attrs: dict[str, str], style_def: dict[str, dict[str, str]], parent_style: dict[str, str]) -> dict[str, str]:
    """
    Определяет окончательный стиль элемента на основе атрибутов, стилей и родительских стилей.

    Args:
        attrs (dict[str, str]): Атрибуты элемента.
        style_def (dict[str, dict[str, str]]): Определения стилей.
        parent_style (dict[str, str]): Стили родительского элемента.

    Returns:
        dict[str, str]: Окончательный стиль элемента.
    """
    style: dict[str, str] = parent_style.copy()
    if 'class' in attrs:
        for css_class in attrs['class'].split():
            css_style: dict[str, str] = style_def['.' + css_class]
            style.update(css_style)
    if 'style' in attrs:
        immediate_style: dict[str, str] = dumb_property_dict(attrs['style'])
        style.update(immediate_style)
    return style

def google_list_style(style: dict[str, str]) -> str:
    """
    Определяет, является ли список упорядоченным или неупорядоченным (для Google Docs).

    Args:
        style (dict[str, str]): Стили списка.

    Returns:
        str: 'ul' для неупорядоченного списка, 'ol' для упорядоченного списка.
    """
    if 'list-style-type' in style:
        list_style: str = style['list-style-type']
        if list_style in ['disc', 'circle', 'square', 'none']:
            return 'ul'
    return 'ol'

def google_nest_count(style: dict[str, str]) -> int:
    """
    Вычисляет уровень вложенности списка (для Google Docs).

    Args:
        style (dict[str, str]): Стили списка.

    Returns:
        int: Уровень вложенности списка.
    """
    nest_count: int = 0
    if 'margin-left' in style:
        nest_count = int(style['margin-left'][:-2]) / GOOGLE_LIST_INDENT
    return nest_count

def google_has_height(style: dict[str, str]) -> bool:
    """
    Проверяет, задана ли высота элемента явно (для Google Docs).

    Args:
        style (dict[str, str]): Стили элемента.

    Returns:
        bool: True, если высота задана явно, иначе False.
    """
    if 'height' in style:
        return True
    return False

def google_text_emphasis(style: dict[str, str]) -> list[str]:
    """
    Возвращает список модификаторов выделения текста (для Google Docs).

    Args:
        style (dict[str, str]): Стили текста.

    Returns:
        list[str]: Список модификаторов выделения текста.
    """
    emphasis: list[str] = []
    if 'text-decoration' in style:
        emphasis.append(style['text-decoration'])
    if 'font-style' in style:
        emphasis.append(style['font-style'])
    if 'font-weight' in style:
        emphasis.append(style['font-weight'])
    return emphasis

def google_fixed_width_font(style: dict[str, str]) -> bool:
    """
    Проверяет, используется ли шрифт фиксированной ширины.

    Args:
        style (dict[str, str]): Стили текста.

    Returns:
        bool: True, если используется шрифт фиксированной ширины, иначе False.
    """
    font_family: str = ''
    if 'font-family' in style:
        font_family = style['font-family']
    if 'Courier New' == font_family or 'Consolas' == font_family:
        return True
    return False

def list_numbering_start(attrs: dict[str, str]) -> int:
    """
    Извлекает начальный номер из атрибутов элемента списка.

    Args:
        attrs (dict[str, str]): Атрибуты элемента списка.

    Returns:
        int: Начальный номер списка.
    """
    if 'start' in attrs:
        return int(attrs['start']) - 1
    else:
        return 0

class _html2text(HTMLParser.HTMLParser):
    """
    Преобразует HTML в Markdown-форматированный текст.
    """
    def __init__(self, out=None, baseurl=''):
        """
        Инициализирует экземпляр класса _html2text.

        Args:
            out: Объект для вывода текста.
            baseurl (str): Базовый URL для разрешения относительных ссылок.
        """
        HTMLParser.HTMLParser.__init__(self)

        if out is None:
            self.out = self.outtextf
        else:
            self.out = out
        self.outtextlist: list[str] = []  # empty list to store output characters before they are  "joined"
        try:
            self.outtext: str = str()
        except NameError as ex:  # Python3
            logger.error('Ошибка NameError', ех, exc_info=True)
            self.outtext: str = str()
        self.quiet: int = 0
        self.p_p: int = 0  # number of newline character to print before next output
        self.outcount: int = 0
        self.start: int = 1
        self.space: int = 0
        self.a: list[dict] = []
        self.astack: list[dict] = []
        self.acount: int = 0
        self.list: list[dict] = []
        self.blockquote: int = 0
        self.pre: int = 0
        self.startpre: int = 0
        self.code: bool = False
        self.br_toggle: str = ''
        self.lastWasNL: int = 0
        self.lastWasList: bool = False
        self.style: int = 0
        self.style_def: dict[str, dict[str, str]] = {}
        self.tag_stack: list[tuple[str, dict, dict]] = []
        self.emphasis: int = 0
        self.drop_white_space: int = 0
        self.inheader: bool = False
        self.abbr_title: Optional[str] = None  # current abbreviation definition
        self.abbr_data: Optional[str] = None  # last inner HTML (for abbr being defined)
        self.abbr_list: dict[str, str] = {}  # stack of abbreviations to write later
        self.baseurl: str = baseurl

        if options.google_doc:
            del unifiable_n[name2cp('nbsp')]
            unifiable['nbsp'] = '&nbsp_place_holder;'

    def feed(self, data: str) -> None:
        """
        Подает данные в парсер HTML.

        Args:
            data (str): HTML-данные для обработки.
        """
        data = data.replace("</\' + \'script>", "</ignore>")
        HTMLParser.HTMLParser.feed(self, data)

    def outtextf(self, s: str) -> None:
        """
        Добавляет текст в список вывода.

        Args:
            s (str): Текст для добавления.
        """
        self.outtextlist.append(s)
        if s:
            self.lastWasNL = s[-1] == '\n'

    def close(self) -> str:
        """
        Завершает обработку HTML и возвращает Markdown-текст.

        Returns:
            str: Markdown-текст.
        """
        HTMLParser.HTMLParser.close(self)

        self.pbr()
        self.o('', 0, 'end')

        self.outtext = self.outtext.join(self.outtextlist)

        if options.google_doc:
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

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        """
        Обрабатывает начальные теги HTML.

        Args:
            tag (str): Имя тега.
            attrs (list[tuple[str, str]]): Список атрибутов тега.
        """
        self.handle_tag(tag, attrs, 1)

    def handle_endtag(self, tag: str) -> None:
        """
        Обрабатывает конечные теги HTML.

        Args:
            tag (str): Имя тега.
        """
        self.handle_tag(tag, None, 0)

    def previousIndex(self, attrs: dict[str, str]) -> Optional[int]:
        """
        Возвращает индекс набора атрибутов (ссылки) в списке self.a.

        Args:
            attrs (dict[str, str]): Атрибуты ссылки.

        Returns:
            Optional[int]: Индекс набора атрибутов или None, если не найден.
        """
        if 'href' not in attrs:
            return None

        i: int = -1
        for a in self.a:
            i += 1
            match: bool = False

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
        Удаляет последние символы из вывода.

        Args:
            nLetters (int): Количество символов для удаления.
        """
        if not self.quiet:
            self.outtext = self.outtext[:-nLetters]

    def handle_emphasis(self, start: bool, tag_style: dict[str, str], parent_style: dict[str, str]) -> None:
        """
        Обрабатывает различные виды выделения текста.

        Args:
            start (bool): True, если это начало выделения, False - если конец.
            tag_style (dict[str, str]): Стили тега.
            parent_style (dict[str, str]): Стили родительского тега.
        """
        tag_emphasis: list[str] = google_text_emphasis(tag_style)
        parent_emphasis: list[str] = google_text_emphasis(parent_style)

        # handle Google's text emphasis
        strikethrough: bool = 'line-through' in tag_emphasis and options.hide_strikethrough
        bold: bool = 'bold' in tag_emphasis and not 'bold' in parent_emphasis
        italic: bool = 'italic' in tag_emphasis and not 'italic' in parent_emphasis
        fixed: bool = google_fixed_width_font(tag_style) and not \
            google_fixed_width_font(parent_style) and not self.pre

        if start:
            # crossed-out text must be handled before other attributes
            # in order not to output qualifiers unnecessarily
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
                self.o('`')
                self.drop_white_space += 1
                self.code = True
        else:
            if bold or italic or fixed:
                # there must not be whitespace before closing emphasis mark
                self.emphasis -= 1
                self.space = 0
                self.outtext = self.outtext.rstrip()
            if fixed:
                if self.drop_white_space:
                    # empty emphasis, drop it
                    self.drop_last(1)
                    self.drop_white_space -= 1
                else:
                    self.o('`')
                self.code = False
            if bold:
                if self.drop_white_space:
                    # empty emphasis, drop it
                    self.drop_last(2)
                    self.drop_white_space -= 1
                else:
                    self.o("**")
            if italic:
                if self.drop_white_space:
                    # empty emphasis, drop it
                    self.drop_last(1)
                    self.drop_white_space -= 1
                else:
                    self.o("_")
            # space is only allowed after *all* emphasis marks
            if (bold or italic) and not self.emphasis:
                self.o(" ")
            if strikethrough:
                self.quiet -= 1

    def handle_tag(self, tag: str, attrs: Optional[list[tuple[str, str]]], start: bool) -> None:
        """
        Обрабатывает HTML-теги.

        Args:
            tag (str): Имя тега.
            attrs (Optional[list[tuple[str, str]]]): Атрибуты тега.
            start (bool): True, если это начальный тег, False - если конечный.
        """
        if attrs is None:
            attrs = {}
        else:
            attrs = dict(attrs)

        if options.google_doc:
            # the attrs parameter is empty for a closing tag. in addition, we
            # need the attributes of the parent nodes in order to get a
            # complete style description for the current element. we assume
            # that google docs export well formed html.
            parent_style: dict[str, str] = {}
            if start:
                if self.tag_stack:
                    parent_style = self.tag_stack[-1][2]
                tag_style: dict[str, str] = element_style(attrs, self.style_def, parent_style)
                self.tag_stack.append((tag, attrs, tag_style))
            else:
                dummy, attrs, tag_style = self.tag_stack.pop()
                if self.tag_stack:
                    parent_style = self.tag_stack[-1][2]

        if hn(tag):
            self.p()
            if start:
                self.inheader = True
                self.o(str(hn(tag)) * "#" + ' ')
            else:
                self.inheader = False
                return  # prevent redundant emphasis marks on headers

        if tag in ['p', 'div']:
            if options.google_doc:
                if start and google_has_height(tag_style):
                    self.p()
                else:
                    self.soft_br()
            else:
                self.p()

        if tag == "br" and start:
            self.o("  \\n")

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
            self.quiet = 0  # sites like 9rules.com never close <head>

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

        if options.google_doc:
            if not self.inheader:
                # handle some font attributes, but leave headers clean
                self.handle_emphasis(start, tag_style, parent_style)

        if tag == "code" and not self.pre:
            self.o('`')  # TODO: `` `this` ``
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

        if tag == "a" and not IGNORE_ANCHORS:
            if start:
                if 'href' in attrs and not (SKIP_INTERNAL_LINKS and attrs['href'].startswith('#')):
                    self.astack.append(attrs)
                    self.o("[")
                else:
                    self.astack.append(None)
            else:
                if self.astack:
                    a = self.astack.pop()
                    if a:
                        if INLINE_LINKS:
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

        if tag == "img" and start and not IGNORE_IMAGES:
            if 'src' in attrs:
                attrs['href'] = attrs['src']
                alt: str = attrs.get('alt', '')
                if INLINE_LINKS:
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
            # Google Docs create sub lists as top level lists
            if (not self.list) and (not self.lastWasList):
                self.p()
            if start:
                if options.google_doc:
                    list_style: str = google_list_style(tag_style)
                else:
                    list_style = tag
                numbering_start: int = list_numbering_start(attrs)
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
                    li = self.list[-1]
                else:
                    li = {'name': 'ul', 'num': 0}
                if options.google_doc:
                    nest_count: int = google_nest_count(tag_style)
                else:
                    nest_count = len(self.list)
                self.o("  " * nest_count)  # TODO: line up <ol><li>s > 9 correctly.
                if li['name'] == "ul":
                    self.o(options.ul_item_mark + " ")
                elif li['name'] == "ol":
                    li['num'] += 1
                    self.o(str(li['num']) + ". ")
                self.start = 1

        if tag in ["table", "tr"] and start:
            self.p()
        if tag == 'td':
            self.pbr()

        if tag == "pre":
            if start:
                self.startpre = 1
                self.pre = 1
            else:
                self.pre = 0
            self.p()

    def pbr(self) -> None:
        """
        Добавляет перенос строки, если необходимо.
        """
        if self.p_p == 0:
            self.p_p = 1

    def p(self) -> None:
        """
        Устанавливает необходимость добавления переноса строки.
        """
        self.p_p = 2

    def soft_br(self) -> None:
        """
        Добавляет мягкий перенос строки.
        """
        self.pbr()
        self.br_toggle = '  '

    def o(self, data: str, puredata: int = 0, force: int = 0) -> None:
        """
        Выводит данные.

        Args:
            data (str): Данные для вывода.
            puredata (int): Флаг, указывающий, что данные не требуют дополнительной обработки.
            force (int): Ф