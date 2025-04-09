### **Анализ кода модуля `html2text`**

=========================================================================================

Модуль преобразует HTML в Markdown-текст.

#### **1. Качество кода**:
   - **Соответствие стандартам**: 6/10
   - **Плюсы**:
     - Код выполняет заявленную функцию преобразования HTML в текст, сохраняя структуру.
     - Присутствуют обработки различных HTML-тегов и стилей для форматирования текста.
   - **Минусы**:
     - Присутствуют устаревшие конструкции, такие как использование `has_key` вместо оператора `in`.
     - Недостаточно аннотаций типов для переменных и функций.
     - Смешанный стиль кодирования (использование как двойных, так и одинарных кавычек).
     - Не хватает комментариев и документации, особенно на русском языке.
     - Отсутствует логирование важных событий и ошибок.

#### **2. Рекомендации по улучшению**:
   - Заменить устаревшие конструкции, такие как `has_key(x, y)` на `y in x`.
   - Добавить аннотации типов для всех переменных и функций.
   - Унифицировать использование кавычек (использовать только одинарные).
   - Добавить комментарии и документацию на русском языке для всех функций и классов.
   - Реализовать логирование с использованием модуля `logger` из `src.logger`.
   - Пересмотреть обработку исключений с использованием `ex` вместо `e`.
   - Обновить и привести в порядок docstring'и.
   - Использовать `|` вместо `Union[]`

#### **3. Оптимизированный код**:

```python
## \file /src/utils/convertors/html2text.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для преобразования HTML в Markdown-текст
=================================================

Модуль содержит класс `_html2text`, который используется для преобразования HTML-контента в Markdown-формат.
Он обрабатывает различные HTML-теги и атрибуты, чтобы сохранить структуру и форматирование текста.

Пример использования
----------------------

>>> from src.utils.convertors.html2text import html2text
>>> html_content = "<p>Это <b>пример</b> HTML-текста.</p>"
>>> markdown_text = html2text(html_content)
>>> print(markdown_text)
Это **пример** HTML-текста.
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
from typing import Optional, List, Dict, Union

from src.logger import logger  # Добавлен импорт logger

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
        return ord("'")
    if hasattr(htmlentitydefs, 'name2codepoint'):  # requires Python 2.3
        return htmlentitydefs.name2codepoint[k]
    else:
        k = htmlentitydefs.entitydefs[k]
        if k.startswith('&#') and k.endswith(';'):
            return int(k[2:-1])  # not in latin-1
        return ord(codecs.latin_1_decode(k)[0])


unifiable: Dict[str, str] = {
    'rsquo': "'", 'lsquo': "'", 'rdquo': '"', 'ldquo': '"',
    'copy': '(C)', 'mdash': '--', 'nbsp': ' ', 'rarr': '->', 'larr': '<-', 'middot': '*',
    'ndash': '-', 'oelig': 'oe', 'aelig': 'ae',
    'agrave': 'a', 'aacute': 'a', 'acirc': 'a', 'atilde': 'a', 'auml': 'a', 'aring': 'a',
    'egrave': 'e', 'eacute': 'e', 'ecirc': 'e', 'euml': 'e',
    'igrave': 'i', 'iacute': 'i', 'icirc': 'i', 'iuml': 'i',
    'ograve': 'o', 'oacute': 'o', 'ocirc': 'o', 'otilde': 'o', 'ouml': 'o',
    'ugrave': 'u', 'uacute': 'u', 'ucirc': 'u', 'uuml': 'u',
    'lrm': '', 'rlm': ''
}

unifiable_n: Dict[Optional[int], str] = {}

for k in unifiable.keys():
    unifiable_n[name2cp(k)] = unifiable[k]


def charref(name: str) -> str:
    """
    Преобразует символьную ссылку в символ Unicode.

    Args:
        name (str): Символьная ссылка.

    Returns:
        str: Соответствующий символ Unicode.
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
    Преобразует ссылку на сущность в символ Unicode.

    Args:
        c (str): Ссылка на сущность.

    Returns:
        str: Соответствующий символ Unicode.
    """
    if not UNICODE_SNOB and c in unifiable.keys():
        return unifiable[c]
    else:
        try:
            name2cp(c)
        except KeyError:
            return '&' + c + ';'
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
        str: Строка с замененными HTML-сущностями.
    """
    s = s.group(1)
    if s[0] == '#':
        return charref(s[1:])
    else:
        return entityref(s)


r_unescape: re.Pattern = re.compile(r'&(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));')


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
        line (str): Строка для проверки.

    Returns:
        bool: True, если строка состоит только из пробельных символов, иначе False.
    """
    for c in line:
        if c != ' ' and c != '  ':
            return c == ' '
    return line


def optwrap(text: str) -> str:
    """
    Оборачивает абзацы в тексте.

    Args:
        text (str): Исходный текст.

    Returns:
        str: Текст с обернутыми абзацами.
    """
    if not BODY_WIDTH:
        return text

    assert wrap, 'Requires Python 2.3.'
    result: str = ''
    newlines: int = 0
    for para in text.split('\n'):
        if len(para) > 0:
            if para[0] != ' ' and para[0] != '-' and para[0] != '*':
                for line in wrap(para, BODY_WIDTH):
                    result += line + '\n'
                result += '\n'
                newlines = 2
            else:
                if not onlywhite(para):
                    result += para + '\n'
                    newlines = 1
        else:
            if newlines < 2:
                result += '\n'
                newlines += 1
    return result


def hn(tag: str) -> Optional[int]:
    """
    Определяет уровень заголовка HTML-тега.

    Args:
        tag (str): HTML-тег.

    Returns:
        Optional[int]: Уровень заголовка (1-9) или None, если тег не является заголовком.
    """
    if tag[0] == 'h' and len(tag) == 2:
        try:
            n = int(tag[1])
            if n in range(1, 10):
                return n
        except ValueError:
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
    Преобразует CSS-данные в словарь селекторов и атрибутов.

    Args:
        data (str): CSS-данные.

    Returns:
        Dict[str, Dict[str, str]]: Словарь селекторов CSS, каждый из которых содержит словарь атрибутов.
    """
    # remove @import sentences
    importIndex: int = data.find('@import')
    while importIndex != -1:
        data = data[0:importIndex] + data[data.find(';', importIndex) + 1:]
        importIndex = data.find('@import')

    # parse the css. reverted from dictionary compehension in order to support older pythons
    elements: List[List[str]] = [x.split('{') for x in data.split('}') if '{' in x.strip()]
    elements = dict([(a.strip(), dumb_property_dict(b)) for a, b in elements])

    return elements


def element_style(attrs: Dict[str, str], style_def: Dict[str, Dict[str, str]], parent_style: Dict[str, str]) -> Dict[str, str]:
    """
    Определяет итоговые стили элемента на основе атрибутов, определений стилей и стилей родительского элемента.

    Args:
        attrs (Dict[str, str]): Атрибуты элемента.
        style_def (Dict[str, Dict[str, str]]): Определения стилей.
        parent_style (Dict[str, str]): Стили родительского элемента.

    Returns:
        Dict[str, str]: Итоговый стиль элемента.
    """
    style: Dict[str, str] = parent_style.copy()
    if 'class' in attrs:
        for css_class in attrs['class'].split():
            css_style: Dict[str, str] = style_def.get('.' + css_class, {})
            style.update(css_style)
    if 'style' in attrs:
        immediate_style: Dict[str, str] = dumb_property_dict(attrs['style'])
        style.update(immediate_style)
    return style


def google_list_style(style: Dict[str, str]) -> str:
    """
    Определяет тип списка (ordered или unordered) на основе стилей Google Docs.

    Args:
        style (Dict[str, str]): Стили элемента.

    Returns:
        str: 'ul' для unordered list, 'ol' для ordered list.
    """
    if 'list-style-type' in style:
        list_style: str = style['list-style-type']
        if list_style in ['disc', 'circle', 'square', 'none']:
            return 'ul'
    return 'ol'


def google_nest_count(style: Dict[str, str]) -> int:
    """
    Вычисляет глубину вложенности списка Google Docs.

    Args:
        style (Dict[str, str]): Стили элемента.

    Returns:
        int: Глубина вложенности списка.
    """
    nest_count: int = 0
    if 'margin-left' in style:
        margin_left: str = style['margin-left']
        nest_count = int(margin_left[:-2]) / GOOGLE_LIST_INDENT
    return nest_count


def google_has_height(style: Dict[str, str]) -> bool:
    """
    Проверяет, определен ли атрибут 'height' в стилях элемента Google Docs.

    Args:
        style (Dict[str, str]): Стили элемента.

    Returns:
        bool: True, если атрибут 'height' определен, иначе False.
    """
    if 'height' in style:
        return True
    return False


def google_text_emphasis(style: Dict[str, str]) -> List[str]:
    """
    Возвращает список модификаторов выделения текста элемента Google Docs.

    Args:
        style (Dict[str, str]): Стили элемента.

    Returns:
        List[str]: Список модификаторов выделения текста.
    """
    emphasis: List[str] = []
    if 'text-decoration' in style:
        emphasis.append(style['text-decoration'])
    if 'font-style' in style:
        emphasis.append(style['font-style'])
    if 'font-weight' in style:
        emphasis.append(style['font-weight'])
    return emphasis


def google_fixed_width_font(style: Dict[str, str]) -> bool:
    """
    Проверяет, используется ли шрифт фиксированной ширины в стилях элемента Google Docs.

    Args:
        style (Dict[str, str]): Стили элемента.

    Returns:
        bool: True, если используется шрифт фиксированной ширины, иначе False.
    """
    font_family: str = ''
    if 'font-family' in style:
        font_family = style['font-family']
    if 'Courier New' == font_family or 'Consolas' == font_family:
        return True
    return False


def list_numbering_start(attrs: Dict[str, str]) -> int:
    """
    Извлекает начальный номер из атрибутов элемента списка.

    Args:
        attrs (Dict[str, str]): Атрибуты элемента.

    Returns:
        int: Начальный номер списка.
    """
    if 'start' in attrs:
        return int(attrs['start']) - 1
    else:
        return 0


class _html2text(HTMLParser.HTMLParser):
    """
    Класс для преобразования HTML в Markdown-текст.
    """

    def __init__(self, out: Optional[callable] = None, baseurl: str = ''):
        """
        Инициализирует экземпляр класса _html2text.

        Args:
            out (Optional[callable]): Функция для вывода текста.
            baseurl (str): Базовый URL для ссылок.
        """
        HTMLParser.HTMLParser.__init__(self)

        if out is None:
            self.out = self.outtextf
        else:
            self.out = out
        self.outtextlist: List[str] = []  # empty list to store output characters before they are  "joined"
        try:
            self.outtext: str = str()
        except NameError as ex:  # Python3
            logger.error('Error initializing outtext', ex, exc_info=True)
            self.outtext: str = str()
        self.quiet: int = 0
        self.p_p: int = 0  # number of newline character to print before next output
        self.outcount: int = 0
        self.start: int = 1
        self.space: int = 0
        self.a: List[Dict[str, str]] = []
        self.astack: List[Optional[Dict[str, str]]] = []
        self.acount: int = 0
        self.list: List[Dict[str, Union[str, int]]] = []
        self.blockquote: int = 0
        self.pre: int = 0
        self.startpre: int = 0
        self.code: bool = False
        self.br_toggle: str = ''
        self.lastWasNL: bool = 0
        self.lastWasList: bool = False
        self.style: int = 0
        self.style_def: Dict[str, Dict[str, str]] = {}
        self.tag_stack: List[tuple[str, Dict[str, str], Dict[str, str]]] = []
        self.emphasis: int = 0
        self.drop_white_space: int = 0
        self.inheader: bool = False
        self.abbr_title: Optional[str] = None  # current abbreviation definition
        self.abbr_data: Optional[str] = None  # last inner HTML (for abbr being defined)
        self.abbr_list: Dict[str, str] = {}  # stack of abbreviations to write later
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
        Выводит текст.

        Args:
            s (str): Текст для вывода.
        """
        self.outtextlist.append(s)
        if s:
            self.lastWasNL = s[-1] == '\n'

    def close(self) -> str:
        """
        Завершает обработку HTML и возвращает преобразованный текст.

        Returns:
            str: Преобразованный Markdown-текст.
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
        Обрабатывает символьные ссылки.

        Args:
            c (str): Символьная ссылка.
        """
        self.o(charref(c), 1)

    def handle_entityref(self, c: str) -> None:
        """
        Обрабатывает ссылки на сущности.

        Args:
            c (str): Ссылка на сущность.
        """
        self.o(entityref(c), 1)

    def handle_starttag(self, tag: str, attrs: List[tuple[str, str]]) -> None:
        """
        Обрабатывает начальные теги.

        Args:
            tag (str): Имя тега.
            attrs (List[tuple[str, str]]): Список атрибутов тега.
        """
        self.handle_tag(tag, attrs, 1)

    def handle_endtag(self, tag: str) -> None:
        """
        Обрабатывает конечные теги.

        Args:
            tag (str): Имя тега.
        """
        self.handle_tag(tag, None, 0)

    def previousIndex(self, attrs: Dict[str, str]) -> Optional[int]:
        """
        Возвращает индекс набора атрибутов (ссылки) в списке self.a.

        Args:
            attrs (Dict[str, str]): Атрибуты для поиска.

        Returns:
            Optional[int]: Индекс найденного набора атрибутов или None, если не найдено.
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

    def drop_last(self, nLetters: int) -> None:
        """
        Удаляет последние символы из вывода.

        Args:
            nLetters (int): Количество символов для удаления.
        """
        if not self.quiet:
            self.outtext = self.outtext[:-nLetters]

    def handle_emphasis(self, start: bool, tag_style: Dict[str, str], parent_style: Dict[str, str]) -> None:
        """
        Обрабатывает различные выделения текста.

        Args:
            start (bool): True, если это начальный тег, иначе False.
            tag_style (Dict[str, str]): Стили текущего тега.
            parent_style (Dict[str, str]): Стили родительского тега.
        """
        tag_emphasis: List[str] = google_text_emphasis(tag_style)
        parent_emphasis: List[str] = google_text_emphasis(parent_style)

        # handle Google's text emphasis
        strikethrough: bool = 'line-through' in tag_emphasis and options.hide_strikethrough
        bold: bool = 'bold' in tag_emphasis and 'bold' not in parent_emphasis
        italic: bool = 'italic' in tag_emphasis and 'italic' not in parent_emphasis
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
                self.o('_')
                self.drop_white_space += 1
            if bold:
                self.o('**')
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
                    self.o('**')
            if italic:
                if self.drop_white_space:
                    # empty emphasis, drop it
                    self.drop_last(1)
                    self.drop_white_space -= 1
                else:
                    self.o('_')
            # space is only allowed after *all* emphasis marks
            if (bold or italic) and not self.emphasis:
                self.o(' ')
            if strikethrough:
                self.quiet -= 1

    def handle_tag(self, tag: str, attrs: Optional[List[tuple[str, str]]], start: bool) -> None:
        """
        Обрабатывает HTML-теги.

        Args:
            tag (str): Имя тега.
            attrs (Optional[List[tuple[str, str]]]): Список атрибутов тега.
            start (bool): True, если это начальный тег, иначе False.
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
            parent_style: Dict[str, str] = {}
            if start:
                if self.tag_stack:
                    parent_style = self.tag_stack[-1][2]
                tag_style: Dict[str, str] = element_style(attrs, self.style_def, parent_style)
                self.tag_stack.append((tag, attrs, tag_style))
            else:
                dummy, attrs, tag_style = self.tag_stack.pop()
                if self.tag_stack:
                    parent_style = self.tag_stack[-1][2]

        if hn(tag):
            self.p()
            if start:
                self.inheader = True
                self.o(hn(tag) * '#' + ' ')
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

        if tag == 'br' and start:
            self.o('  \n')

        if tag == 'hr' and start:
            self.p()
            self.o('* * *')
            self.p()

        if tag in ['head', 'style', 'script']:
            if start:
                self.quiet += 1
            else:
                self.quiet -= 1

        if tag == 'style':
            if start:
                self.style += 1
            else:
                self.style -= 1

        if tag in ['body']:
            self.quiet = 0  # sites like 9rules.com never close <head>

        if tag == 'blockquote':
            if start:
                self.p()
                self.o('> ', 0, 1)
                self.start = 1
                self.blockquote += 1
            else:
                self.blockquote -= 1
                self.p()

        if tag in ['em', 'i', 'u']:
            self.o('_')
        if tag in ['strong', 'b']:
            self.o('**')
        if tag in ['del', 'strike']:
            if start:
                self.o('<' + tag + '>')
            else:
                self.o('</' + tag + '>')

        if options.google_doc:
            if not self.inheader:
                # handle some font attributes, but leave headers clean
                self.handle_emphasis(start, tag_style, parent_style)

        if tag == 'code' and not self.pre:
            self.o('`')  # TODO: `` `this` ``
        if tag == 'abbr':
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

        if tag == 'a' and not IGNORE_ANCHORS:
            if start:
                if 'href' in attrs and not (SKIP_INTERNAL_LINKS and attrs['href'].startswith('#')):
                    self.astack.append(attrs)
                    self.o('[')
                else:
                    self.astack.append(None)
            else:
                if self.astack:
                    a = self.astack.pop()
                    if a:
                        if INLINE_LINKS:
                            self.o('](' + a['href'] + ')')
                        else:
                            i = self.previousIndex(a)
                            if i is not None:
                                a = self.a[i]
                            else:
                                self.acount += 1
                                a['count'] = self.acount
                                a['outcount'] = self.outcount
                                self.a.append(a)
                            self.o('][' + str(a['count']) + ']')

        if tag == 'img' and start and not IGNORE_IMAGES:
            if 'src' in attrs:
                attrs['href'] = attrs['src']
                alt: str = attrs.get('alt', '')
                if INLINE_LINKS:
                    self.o('![')
                    self.o(alt)
                    self.o('](' + attrs['href'] + ')')
                else:
                    i = self.previousIndex(attrs)
                    if i is not None:
                        attrs = self.a[i]
                    else:
                        self.acount += 1
                        attrs['count'] = self.acount
                        attrs['outcount'] = self.outcount
                        self.a.append(attrs)
                    self.o('![')
                    self.o(alt)
                    self.o('][' + str(attrs['count']) + ']')

        if tag == 'dl' and start:
            self.p()
        if tag == 'dt' and not start:
            self.pbr()
        if tag == 'dd' and start:
            self.o('    ')
        if tag == 'dd' and not start:
            self.pbr()

        if tag in ['ol', 'ul']:
            # Google Docs create sub lists as top level lists
            if (not self.list) and (not self.lastWasList):
                self.p()
            if start:
                if options.google_doc:
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
                    li = self.list[-1]
                else:
                    li = {'name': 'ul', 'num': 0}
                if options.google_doc:
                    nest_count = google_nest_count(tag_style)
                else:
                    nest_count = len(self.list)
                self.o('  ' * nest_count)  # TODO: line up <ol><li>s > 9 correctly.
                if li['name'] == 'ul':
                    self.o(options.ul_item_mark + ' ')
                elif li['name'] == 'ol':
                    li['num'] += 1
                    self.o(str(li['num']) + '. ')
                self.start = 1

        if tag in ['table', 'tr'] and start:
            self.p()
        if tag == 'td':
            self.pbr()

        if tag == 'pre':
            if start:
                self.startpre = 1
                self.pre = 1
            else:
                self.pre = 0
            self.p()

    def pbr(self) -> None:
        """
        Управляет добавлением разрывов строк.
        """
        if self.p_p == 0:
            self.p_p = 1

    def p(self) -> None:
        """
        Добавляет два разрыва строк.
        """
        self.p_p = 2

    def soft_br(self) -> None:
        """
        Добавляет мягкий разрыв строки.
        """
        self.pbr()
        self.br_toggle = '  '

    def o(self, data: str, puredata: int = 0, force: Union[int, str] = 0) -> None:
        """
        Выводит данные с учетом различных состояний и опций.

        Args:
            data (str): Данные для вывода.
            puredata (int): Флаг, указывающий на необходимость обработки данных.
            force (Union[int, str]): Фла