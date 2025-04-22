### **Системные инструкции для обработки кода проекта `hypotez`**

=========================================================================================

Описание функциональности и правил для генерации, анализа и улучшения кода. Направлено на обеспечение последовательного и читаемого стиля кодирования, соответствующего требованиям.

---

### **Основные принципы**

#### **1. Общие указания**:
- Соблюдай четкий и понятный стиль кодирования.
- Все изменения должны быть обоснованы и соответствовать установленным требованиям.

#### **2. Комментарии**:
- Используй `#` для внутренних комментариев.
- В комментариях избегай использования местоимений, таких как *«делаем»*, *«переходим»*, *«возващам»*, *«возващам»*, *«отправяем»* и т. д.. Вмсто этого используй точные термины, такие как *«извлеизвлечение»*, *«проверка»*, *«выполннение»*, *«замена»*, *«вызов»*, *«Функця выпоняет»*,*«Функця изменяет значение»*, *«Функця вызывает»*,*«отправка»*
Пример:
```python
# Неправильно:
def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
    # Получаем значение параметра
    ...
# Правильно:

def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
    # Функция извлекает значение параметра
    ...
# Неправильно:
if not process_directory.exists():
    logger.error(f"Директория не существует: {process_directory}")
    continue  # Переходим к следующей директории, если текущая не существует

if not process_directory.is_dir():
    logger.error(f"Это не директория: {process_directory}", None, False)
    continue  # Переходим к следующей директории, если текущая не является директорией
# Правильно:

if not process_directory.exists():
    logger.error(f"Директория не существует: {process_directory}")
    continue  # Переход к следующей директории, если текущая не существует
if not process_directory.is_dir():
    logger.error(f"Это не директория: {process_directory}", None, False)
    continue  # Переходим к следующей директории, если текущая не является директорией

```
- Документация всех функций, методов и классов должна следовать такому формату: 
    ```python
        def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
            """ 
            Args:
                param (str): Описание параметра `param`.
                param1 (Optional[str | dict | str], optional): Описание параметра `param1`. По умолчанию `None`.
    
            Returns:
                dict | None: Описание возващаемого значения. Возвращает словарь или `None`.
    
            Raises:
                SomeError: Описание ситуации, в которой возникает исключение `SomeError`.

            Ехаmple:
                >>> function('param', 'param1')
                {'param': 'param1'}
            """
    ```
- Комментарии и документация должны быть четкими, лаконичными и точными.


### **3. Заголовок файла**:
Обязательно оставляй строки 
```python
## \file path/to/file
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
```
и
```
"""
...
```rst
 .. module:: src.utils.string.html_simplification
 ```
"""
```
если они есть. Если нет - добавляй.
Пример:
## \file /src/utils/string/html_simplification.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для очистки HTML-тегов из текста и упрощения HTML-кода.
===============================================================
Модуль минимизирует HTML-код, удаляет теги и атрибуты, а также обрабатывает
специальные случаи, такие как скрипты, стили и комментарии.
Использует BeautifulSoup для надежного парсинга HTML.

Зависимости:
    - beautifulsoup4 (pip install beautifulsoup4)
    - lxml (опционально, для более быстрого парсинга: pip install lxml)

 .. module:: src.utils.string.html_simplification
"""

#### **4. Форматирование кода**:
- Используй одинарные кавычки. `a:str = 'value'`, `print('Hello World!')`;
- Добавляй пробелы вокруг операторов. Например, `x = 5`;
- Все параметры должны быть аннотированы типами. `def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:`;
- Не используй `Union`. Вместо этого используй `|`.
- Не используй термин `Product`, только `товар`

#### **5. Логирование**:
- Для логгирования Всегда Используй модуль `logger` из `src.logger.logger`.
- Ошибки должны логироваться с использованием `logger.error`.
Пример:
    ```python
        try:
            ...
        except Exception as ex:
            logger.error('Error while processing data', ех, exc_info=True)
    ```
#### **6. Не используй `Union[]` в коде. Вместо него используй `|`
Например:
```python
x: str | int ...
```

#### **7. Не используй глобальные переменные. Если есть надобность - то поределяй их в классе `Config`.
Пример:

- Неправильно:
```python

state:int = 'global'

def func():
    print(state)

```
- Правильно:
```python

class Config:
    state:int = 'global'

def func():
    print(Config.state)

```

#### **8. Не используй `self` в методах класса. Вместо него используй `cls`.
#### **9. Всегда объявляй переменные вначале функции. Не объявляй их в середине функции.
Пример:
```python
def func():
    # Неправильно
    if condition:
        x = 5
        y = 10
    else:
        x = 20
        y = 30
    # Правильно
    x = None
    y = None
    if condition:
        x = 5
        y = 10
    else:
        x = 20
        y = 30
```
---

### **Основные требования**:

#### **1. Формат ответов в Markdown**:
- Все ответы должны быть выполнены в формате **Markdown**.

#### **2. Формат комментариев**:
- Используй указанный стиль для комментариев и документации в коде.
- Пример:

```python
from typing import Generator, Optional, List
from pathlib import Path


def read_text_file(
    file_path: str | Path,
    as_list: bool = False,
    extensions: Optional[List[str]] = None,
    chunk_size: int = 8192,
) -> Generator[str, None, None] | str | None:
    """
    Считывает содержимое файла (или файлов из каталога) с использованием генератора для экономии памяти.

    Args:
        file_path (str | Path): Путь к файлу или каталогу.
        as_list (bool): Если `True`, возвращает генератор строк.
        extensions (Optional[List[str]]): Список расширений файлов для чтения из каталога.
        chunk_size (int): Размер чанков для чтения файла в байтах.

    Returns:
        Generator[str, None, None] | str | None: Генератор строк, объединенная строка или `None` в случае ошибки.

    Raises:
        Exception: Если возникает ошибка при чтении файла.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('example.txt')
        >>> content = read_text_file(file_path)
        >>> if content:
        ...    print(f'File content: {content[:100]}...')
        File content: Example text...
    """
    ...
```
- Всегда делай подробные объяснения в комментариях. Избегай расплывчатых терминов, 
- таких как *«получить»* или *«делать»*
-  . Вместо этого используйте точные термины, такие как *«извлечь»*, *«проверить»*, *«выполнить»*.
- Вместо: *«получаем»*, *«возвращаем»*, *«преобразовываем»* используй имя объекта *«функция получае»*, *«переменная возвращает»*, *«код преобразовывает»* 
- Комментарии должны непосредственно предшествовать описываемому блоку кода и объяснять его назначение.

#### **3. Пробелы вокруг операторов присваивания**:
- Всегда добавляйте пробелы вокруг оператора `=`, чтобы повысить читаемость.
- Примеры:
  - **Неправильно**: `x=5`
  - **Правильно**: `x = 5`

#### **4. Использование `j_loads` или `j_loads_ns`**:
- Для чтения JSON или конфигурационных файлов замените стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.
- Пример:

```python
# Неправильно:
with open('config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Правильно:
data = j_loads('config.json')
```

#### **5. Сохранение комментариев**:
- Все существующие комментарии, начинающиеся с `#`, должны быть сохранены без изменений в разделе «Улучшенный код».
- Если комментарий кажется устаревшим или неясным, не изменяйте его. Вместо этого отметьте его в разделе «Изменения».

#### **6. Обработка `...` в коде**:
- Оставляйте `...` как указатели в коде без изменений.
- Не документируйте строки с `...`.
```

#### **7. Аннотации**
Для всех переменных должны быть определены аннотации типа. 
Для всех функций все входные и выходные параметры аннотириваны
Для все параметров должны быть аннотации типа.


### **8. webdriver**
В коде используется webdriver. Он импртируется из модуля `webdriver` проекта `hypotez`
```python
from src.webdirver import Driver, Chrome, Firefox, Playwright, ...
driver = Driver(Firefox)

Пoсле чего может использоваться как

close_banner = {
  "attribute": null,
  "by": "XPATH",
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "click()",
  "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}

result = driver.execute_locator(close_banner)

#### **9. Не используй `Union[]` в коде. Вместо него используй `|`
Например:
```python
x: str | int ...
```

#### **10. print - это моя встроенная функция.
from src.utils.printer import pprint as print


Вот она:

\file /src/utils/printer.py
-- coding: utf-8 --

#! .pyenv/bin/python3

"""
.. module::  src.utils
:platform: Windows, Unix
:synopsis: Utility functions for pretty printing and text styling.

This module provides functions to print data in a human-readable format with optional text styling, including color, background, and font styles.
"""

import json
import csv
import pandas as pd
from pathlib import Path
from typing import Any
from pprint import pprint as pretty_print

ANSI escape codes

RESET = "\033[0m"

TEXT_COLORS = {
"red": "\033[31m",
"green": "\033[32m",
"blue": "\033[34m",
"yellow": "\033[33m",
"white": "\033[37m",
"cyan": "\033[36m",
"magenta": "\033[35m",
"light_gray": "\033[37m",
"dark_gray": "\033[90m",
"light_red": "\033[91m",
"light_green": "\033[92m",
"light_blue": "\033[94m",
"light_yellow": "\033[93m",
}

Background colors mapping

BG_COLORS = {
"bg_red": "\033[41m",
"bg_green": "\033[42m",
"bg_blue": "\033[44m",
"bg_yellow": "\033[43m",
"bg_white": "\033[47m",
"bg_cyan": "\033[46m",
"bg_magenta": "\033[45m",
"bg_light_gray": "\033[47m",
"bg_dark_gray": "\033[100m",
"bg_light_red": "\033[101m",
"bg_light_green": "\033[102m",
"bg_light_blue": "\033[104m",
"bg_light_yellow": "\033[103m",
}

FONT_STYLES = {
"bold": "\033[1m",
"underline": "\033[4m",
}

def _color_text(text: str, text_color: str = "", bg_color: str = "", font_style: str = "") -> str:
"""Apply color, background, and font styling to the text.

This helper function applies the provided color and font styles to the given text using ANSI escape codes.

:param text: The text to be styled.
:param text_color: The color to apply to the text. Default is an empty string, meaning no color.
:param bg_color: The background color to apply. Default is an empty string, meaning no background color.
:param font_style: The font style to apply to the text. Default is an empty string, meaning no font style.
:return: The styled text as a string.

:example:
    >>> _color_text("Hello, World!", text_color="green", font_style="bold")
    '\033[1m\033[32mHello, World!\033[0m'
"""
return f"{font_style}{text_color}{bg_color}{text}{RESET}"


def pprint(print_data: Any = None, text_color: str = "white", bg_color: str = "", font_style: str = "") -> None:
"""Pretty prints the given data with optional color, background, and font style.

This function formats the input data based on its type and prints it to the console. The data is printed with optional 
text color, background color, and font style based on the specified parameters. The function can handle dictionaries, 
lists, strings, and file paths.

:param print_data: The data to be printed. Can be of type ``None``, ``dict``, ``list``, ``str``, or ``Path``.
:param text_color: The color to apply to the text. Default is 'white'. See :ref:`TEXT_COLORS`.
:param bg_color: The background color to apply to the text. Default is '' (no background color). See :ref:`BG_COLORS`.
:param font_style: The font style to apply to the text. Default is '' (no font style). See :ref:`FONT_STYLES`.
:return: None

:raises: Exception if the data type is unsupported or an error occurs during printing.

:example:
    >>> pprint({"name": "Alice", "age": 30}, text_color="green")
    \033[32m{
        "name": "Alice",
        "age": 30
    }\033[0m

    >>> pprint(["apple", "banana", "cherry"], text_color="blue", font_style="bold")
    \033[34m\033[1mapple\033[0m
    \033[34m\033[1mbanana\033[0m
    \033[34m\033[1mcherry\033[0m

    >>> pprint("text example", text_color="yellow", bg_color="bg_red", font_style="underline")
    \033[4m\033[33m\033[41mtext example\033[0m
"""
if not print_data:
    return
if isinstance(text_color, str):
    text_color = TEXT_COLORS.get(text_color.lower(), TEXT_COLORS["white"])
if isinstance(bg_color, str):
    bg_color = BG_COLORS.get(bg_color.lower(), "")
if isinstance(font_style, str):
    font_style = FONT_STYLES.get(font_style.lower(), "")


try:
    if isinstance(print_data, dict):
        print(_color_text(json.dumps(print_data, indent=4), text_color))
    elif isinstance(print_data, list):
        for item in print_data:
            print(_color_text(str(item), text_color))
    elif isinstance(print_data, (str, Path)) and Path(print_data).is_file():
        ext = Path(print_data).suffix.lower()
        if ext in ['.csv', '.xls']:
            print(_color_text("File reading supported for .csv, .xls only.", text_color))
        else:
            print(_color_text("Unsupported file type.", text_color))
    else:
        print(_color_text(str(print_data), text_color))
except Exception as ex:
    print(_color_text(f"Error: {ex}", text_color=TEXT_COLORS["red"]))
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END

if name == 'main':
pprint({"name": "Alice", "age": 30}, text_color="green")
```

## \file /src/utils/convertors/html2text.py

# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.utils.convertors.html2text
	:platform: Windows, Unix
	:synopsis:  HTML -> MD

"""

"""html2text: Turn HTML into equivalent Markdown-structured text."""
__version__: str = "3.1"
__author__: str = "Aaron Swartz (me@aaronsw.com)"
__copyright__: str = "(C) 2004-2008 Aaron Swartz. GNU GPL 3."
__contributors__: list[str] = ["Martin \'Joey\' Schulze", "Ricardo Reyes", "Kevin Jay North"]

# TODO:
#   Support decoded entities with unifiable.

try:
    True
except NameError:
    setattr(__builtins__, 'True', 1)
    setattr(__builtins__, 'False', 0)


def has_key(x: dict, y: str) -> bool:
    """
    Функция проверяет, содержит ли словарь `x` ключ `y`.

    Args:
        x (dict): Словарь для проверки.
        y (str): Ключ для поиска в словаре.

    Returns:
        bool: `True`, если словарь содержит ключ, иначе `False`.
    """
    if hasattr(x, 'has_key'):
        return x.has_key(y)
    else:
        return y in x


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


def name2cp(k: str) -> int:
    """
    Функция преобразует имя HTML-сущности в кодовую точку Unicode.

    Args:
        k (str): Имя HTML-сущности.

    Returns:
        int: Кодовая точка Unicode.
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


unifiable: dict[str, str] = {'rsquo': "\'", 'lsquo': "\'", 'rdquo': '"', 'ldquo': '"',
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
    Функция преобразует символьную ссылку (например, &#160;) в символ Unicode.

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
    Функция преобразует ссылку на сущность (например, &nbsp;) в символ Unicode.

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
            return "&" + c + ';'
        else:
            try:
                return chr(name2cp(c))
            except NameError:  # Python3
                return chr(name2cp(c))


def replaceEntities(s: re.Match) -> str:
    """
    Функция заменяет HTML-сущности в строке.

    Args:
        s (re.Match): Объект совпадения регулярного выражения.

    Returns:
        str: Строка с замененными сущностями.
    """
    s = s.group(1)
    if s[0] == "#":
        return charref(s[1:])
    else:
        return entityref(s)


r_unescape: re.Pattern = re.compile(r"&(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));")


def unescape(s: str) -> str:
    """
    Функция удаляет HTML-сущности из строки.

    Args:
        s (str): Исходная строка.

    Returns:
        str: Строка без HTML-сущностей.
    """
    return r_unescape.sub(replaceEntities, s)

### End Entity Nonsense ###


def onlywhite(line: str) -> bool:
    """
    Функция проверяет, состоит ли строка только из пробельных символов.

    Args:
        line (str): Строка для проверки.

    Returns:
        bool: `True`, если строка состоит только из пробельных символов, иначе `False`.
    """
    for c in line:
        if c is not ' ' and c is not '  ':
            return c is ' '
    return line


def optwrap(text: str) -> str:
    """
    Функция обертывает все абзацы в предоставленном тексте.

    Args:
        text (str): Текст для обертывания.

    Returns:
        str: Обернутый текст.
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


def hn(tag: str) -> int | None:
    """
    Функция проверяет, является ли тег заголовком (h1-h9) и возвращает его уровень.

    Args:
        tag (str): HTML-тег для проверки.

    Returns:
        int | None: Уровень заголовка (1-9), если тег является заголовком, иначе `None`.
    """
    if tag[0] == 'h' and len(tag) == 2:
        try:
            n = int(tag[1])
            if n in range(1, 10):
                return n
        except ValueError:
            return None


def dumb_property_dict(style: str) -> dict[str, str]:
    """
    Функция преобразует строку CSS-стилей в словарь атрибутов.

    Args:
        style (str): Строка CSS-стилей.

    Returns:
        dict[str, str]: Словарь CSS-атрибутов.
    """
    return dict([(x.strip(), y.strip()) for x, y in [z.split(':', 1) for z in style.split(';') if ':' in z]])


def dumb_css_parser(data: str) -> dict[str, dict[str, str]]:
    """
    Функция разбирает CSS-данные и возвращает словарь селекторов CSS,
    каждый из которых содержит словарь атрибутов CSS.

    Args:
        data (str): CSS-данные для разбора.

    Returns:
        dict[str, dict[str, str]]: Словарь селекторов CSS и их атрибутов.
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
    Функция возвращает словарь "окончательных" атрибутов стиля элемента.

    Args:
        attrs (dict[str, str]): Атрибуты элемента.
        style_def (dict[str, dict[str, str]]): Определения стилей.
        parent_style (dict[str, str]): Стили родительского элемента.

    Returns:
        dict[str, str]: Словарь стилей элемента.
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
    Функция определяет, является ли список упорядоченным или неупорядоченным.

    Args:
        style (dict[str, str]): Стили элемента списка.

    Returns:
        str: 'ul', если список неупорядоченный, иначе 'ol'.
    """
    if 'list-style-type' in style:
        list_style: str = style['list-style-type']
        if list_style in ['disc', 'circle', 'square', 'none']:
            return 'ul'
    return 'ol'


def google_nest_count(style: dict[str, str]) -> int:
    """
    Функция вычисляет уровень вложенности для списков Google Docs.

    Args:
        style (dict[str, str]): Стили элемента списка.

    Returns:
        int: Уровень вложенности списка.
    """
    nest_count: int = 0
    if 'margin-left' in style:
        nest_count = int(style['margin-left'][:-2]) / GOOGLE_LIST_INDENT
    return nest_count


def google_has_height(style: dict[str, str]) -> bool:
    """
    Функция проверяет, определен ли атрибут 'height' явно в стиле элемента.

    Args:
        style (dict[str, str]): Стили элемента.

    Returns:
        bool: `True`, если атрибут 'height' определен, иначе `False`.
    """
    if 'height' in style:
        return True
    return False


def google_text_emphasis(style: dict[str, str]) -> list[str]:
    """
    Функция возвращает список всех модификаторов выделения элемента.

    Args:
        style (dict[str, str]): Стили элемента.

    Returns:
        list[str]: Список модификаторов выделения.
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
    Функция проверяет, определяет ли CSS текущего элемента шрифт фиксированной ширины.

    Args:
        style (dict[str, str]): Стили элемента.

    Returns:
        bool: `True`, если шрифт фиксированной ширины, иначе `False`.
    """
    font_family: str = ''
    if 'font-family' in style:
        font_family = style['font-family']
    if 'Courier New' == font_family or 'Consolas' == font_family:
        return True
    return False


def list_numbering_start(attrs: dict[str, str]) -> int:
    """
    Функция извлекает начальный номер из атрибутов элемента списка.

    Args:
        attrs (dict[str, str]): Атрибуты элемента списка.

    Returns:
        int: Начальный номер списка (на 1 меньше фактического).
    """
    if 'start' in attrs:
        return int(attrs['start']) - 1
    else:
        return 0


class _html2text(HTMLParser.HTMLParser):
    """
    Класс для преобразования HTML в текст в формате Markdown.
    """

    def __init__(self, out=None, baseurl=''):
        """
        Инициализация объекта класса _html2text.

        Args:
            out (callable, optional): Функция для вывода текста. Defaults to self.outtext