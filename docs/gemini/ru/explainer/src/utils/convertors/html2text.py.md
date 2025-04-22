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
```python
                ## \file /src/utils/convertors/html2text.py
# -*- coding: utf-8 -*-\n\n#! .pyenv/bin/python3\n\n\"\"\"\n.. module:: src.utils.convertors.html2text \n\t:platform: Windows, Unix\n\t:synopsis:  HTML -> MD\n\n\"\"\"\n\n\n\n\n\n\n\"\"\"html2text: Turn HTML into equivalent Markdown-structured text.\"\"\"\n__version__ = "3.1"\n__author__ = "Aaron Swartz (me@aaronsw.com)"\n__copyright__ = "(C) 2004-2008 Aaron Swartz. GNU GPL 3."\n__contributors__ = ["Martin \'Joey\' Schulze", "Ricardo Reyes", "Kevin Jay North"]\n\n# TODO:\n#   Support decoded entities with unifiable.\n\ntry:\n    True\nexcept NameError:\n    setattr(__builtins__, \'True\', 1)\n    setattr(__builtins__, \'False\', 0)\n\ndef has_key(x, y):\n    if hasattr(x, \'has_key\'): return x.has_key(y)\n    else: return y in x\n\n\nimport html.entities as htmlentitydefs\nimport urllib.parse as urlparse\nimport html.parser as HTMLParser\nimport urllib.request as urllib\nimport optparse, re, sys, codecs, types\nfrom textwrap import wrap\n\n\n# Use Unicode characters instead of their ascii psuedo-replacements\nUNICODE_SNOB = 0\n\n# Put the links after each paragraph instead of at the end.\nLINKS_EACH_PARAGRAPH = 0\n\n# Wrap long lines at position. 0 for no wrapping. (Requires Python 2.3.)\nBODY_WIDTH = 78\n\n# Don\'t show internal links (href="#local-anchor") -- corresponding link targets\n# won\'t be visible in the plain text file anyway.\nSKIP_INTERNAL_LINKS = True\n\n# Use inline, rather than reference, formatting for images and links\nINLINE_LINKS = True\n\n# Number of pixels Google indents nested lists\nGOOGLE_LIST_INDENT = 36\n\nIGNORE_ANCHORS = False\nIGNORE_IMAGES = False\n\n### Entity Nonsense ###\n\ndef name2cp(k):\n    if k == \'apos\': return ord("\'")\n    if hasattr(htmlentitydefs, "name2codepoint"): # requires Python 2.3\n        return htmlentitydefs.name2codepoint[k]\n    else:\n        k = htmlentitydefs.entitydefs[k]\n        if k.startswith("&#") and k.endswith(";"): return int(k[2:-1]) # not in latin-1\n        return ord(codecs.latin_1_decode(k)[0])\n\nunifiable = {\'rsquo\':"\'", \'lsquo\':"\'", \'rdquo\':\'"\', \'ldquo\':\'"\', \n\'copy\':\'(C)\', \'mdash\':\'--\', \'nbsp\':\' \', \'rarr\':\'->\', \'larr\':\'<-\', \'middot\':\'*\',\n\'ndash\':\'-\', \'oelig\':\'oe\', \'aelig\':\'ae\',\n\'agrave\':\'a\', \'aacute\':\'a\', \'acirc\':\'a\', \'atilde\':\'a\', \'auml\':\'a\', \'aring\':\'a\', \n\'egrave\':\'e\', \'eacute\':\'e\', \'ecirc\':\'e\', \'euml\':\'e\', \n\'igrave\':\'i\', \'iacute\':\'i\', \'icirc\':\'i\', \'iuml\':\'i\',\n\'ograve\':\'o\', \'oacute\':\'o\', \'ocirc\':\'o\', \'otilde\':\'o\', \'ouml\':\'o\', \n\'ugrave\':\'u\', \'uacute\':\'u\', \'ucirc\':\'u\', \'uuml\':\'u\',\n\'lrm\':\'\', \'rlm\':\'\'}\n\nunifiable_n = {}\n\nfor k in unifiable.keys():\n    unifiable_n[name2cp(k)] = unifiable[k]\n\ndef charref(name):\n    if name[0] in [\'x\',\'X\']:\n        c = int(name[1:], 16)\n    else:\n        c = int(name)\n    \n    if not UNICODE_SNOB and c in unifiable_n.keys():\n        return unifiable_n[c]\n    else:\n        try:\n            return chr(c)\n        except NameError: #Python3\n            return chr(c)\n\ndef entityref(c):\n    if not UNICODE_SNOB and c in unifiable.keys():\n        return unifiable[c]\n    else:\n        try: name2cp(c)\n        except KeyError: return "&" + c + \';\'\n        else:\n            try:\n                return chr(name2cp(c))\n            except NameError: #Python3\n                return chr(name2cp(c))\n\ndef replaceEntities(s):\n    s = s.group(1)\n    if s[0] == "#": \n        return charref(s[1:])\n    else: return entityref(s)\n\nr_unescape = re.compile(r"&(#?[xX]?(?:[0-9a-fA-F]+|\\w{1,8}));")\ndef unescape(s):\n    return r_unescape.sub(replaceEntities, s)\n\n### End Entity Nonsense ###\n\ndef onlywhite(line):\n    \"\"\"Return true if the line does only consist of whitespace characters.\"\"\"\n    for c in line:\n        if c is not \' \' and c is not \'  \':\n            return c is \' \'\n    return line\n\ndef optwrap(text):\n    \"\"\"Wrap all paragraphs in the provided text.\"\"\"\n    if not BODY_WIDTH:\n        return text\n    \n    assert wrap, "Requires Python 2.3."\n    result = \'\'\n    newlines = 0\n    for para in text.split("\\n"):\n        if len(para) > 0:\n            if para[0] != \' \' and para[0] != \'-\' and para[0] != \'*\':\n                for line in wrap(para, BODY_WIDTH):\n                    result += line + "\\n"\n                result += "\\n"\n                newlines = 2\n            else:\n                if not onlywhite(para):\n                    result += para + "\\n"\n                    newlines = 1\n        else:\n            if newlines < 2:\n                result += "\\n"\n                newlines += 1\n    return result\n\ndef hn(tag):\n    if tag[0] == \'h\' and len(tag) == 2:\n        try:\n            n = int(tag[1])\n            if n in range(1, 10): return n\n        except ValueError: return 0\n\ndef dumb_property_dict(style):\n    \"\"\"returns a hash of css attributes\"\"\"\n    return dict([(x.strip(), y.strip()) for x, y in [z.split(\':\', 1) for z in style.split(\';\') if \':\' in z]]);\n\ndef dumb_css_parser(data):\n    \"\"\"returns a hash of css selectors, each of which contains a hash of css attributes\"\"\"\n    # remove @import sentences\n    importIndex = data.find(\'@import\')\n    while importIndex != -1:\n        data = data[0:importIndex] + data[data.find(\';\', importIndex) + 1:]\n        importIndex = data.find(\'@import\')\n\n    # parse the css. reverted from dictionary compehension in order to support older pythons\n    elements =  [x.split(\'{\') for x in data.split(\'}\') if \'{\' in x.strip()]\n    elements = dict([(a.strip(), dumb_property_dict(b)) for a, b in elements])\n\n    return elements\n\ndef element_style(attrs, style_def, parent_style):\n    \"\"\"returns a hash of the \'final\' style attributes of the element\"\"\"\n    style = parent_style.copy()\n    if \'class\' in attrs:\n        for css_class in attrs[\'class\'].split():\n            css_style = style_def[\'.\' + css_class]\n            style.update(css_style)\n    if \'style\' in attrs:\n        immediate_style = dumb_property_dict(attrs[\'style\'])\n        style.update(immediate_style)\n    return style\n\ndef google_list_style(style):\n    \"\"\"finds out whether this is an ordered or unordered list\"\"\"\n    if \'list-style-type\' in style:\n        list_style = style[\'list-style-type\']\n        if list_style in [\'disc\', \'circle\', \'square\', \'none\']:\n            return \'ul\'\n    return \'ol\'\n\ndef google_nest_count(style):\n    \"\"\"calculate the nesting count of google doc lists\"\"\"\n    nest_count = 0\n    if \'margin-left\' in style:\n        nest_count = int(style[\'margin-left\'][:-2]) / GOOGLE_LIST_INDENT\n    return nest_count\n\ndef google_has_height(style):\n    \"\"\"check if the style of the element has the \'height\' attribute explicitly defined\"\"\"\n    if \'height\' in style:\n        return True\n    return False\n\ndef google_text_emphasis(style):\n    \"\"\"return a list of all emphasis modifiers of the element\"\"\"\n    emphasis = []\n    if \'text-decoration\' in style:\n        emphasis.append(style[\'text-decoration\'])\n    if \'font-style\' in style:\n        emphasis.append(style[\'font-style\'])\n    if \'font-weight\' in style:\n        emphasis.append(style[\'font-weight\'])\n    return emphasis\n\ndef google_fixed_width_font(style):\n    \"\"\"check if the css of the current element defines a fixed width font\"\"\"\n    font_family = \'\'\n    if \'font-family\' in style:\n        font_family = style[\'font-family\']\n    if \'Courier New\' == font_family or \'Consolas\' == font_family:\n        return True\n    return False\n\ndef list_numbering_start(attrs):\n    \"\"\"extract numbering from list element attributes\"\"\"\n    if \'start\' in attrs:\n        return int(attrs[\'start\']) - 1\n    else:\n        return 0\n\nclass _html2text(HTMLParser.HTMLParser):\n    def __init__(self, out=None, baseurl=\'\'):\n        HTMLParser.HTMLParser.__init__(self)\n        \n        if out is None: self.out = self.outtextf\n        else: self.out = out\n        self.outtextlist = [] # empty list to store output characters before they are  "joined"\n        try:\n            self.outtext = unicode()\n        except NameError: # Python3\n            self.outtext = str()\n        self.quiet = 0\n        self.p_p = 0 # number of newline character to print before next output\n        self.outcount = 0\n        self.start = 1\n        self.space = 0\n        self.a = []\n        self.astack = []\n        self.acount = 0\n        self.list = []\n        self.blockquote = 0\n        self.pre = 0\n        self.startpre = 0\n        self.code = False\n        self.br_toggle = \'\'\n        self.lastWasNL = 0\n        self.lastWasList = False\n        self.style = 0\n        self.style_def = {}\n        self.tag_stack = []\n        self.emphasis = 0\n        self.drop_white_space = 0\n        self.inheader = False\n        self.abbr_title = None # current abbreviation definition\n        self.abbr_data = None # last inner HTML (for abbr being defined)\n        self.abbr_list = {} # stack of abbreviations to write later\n        self.baseurl = baseurl\n\n        if options.google_doc:\n            del unifiable_n[name2cp(\'nbsp\')]\n            unifiable[\'nbsp\'] = \'&nbsp_place_holder;\'\n    \n    def feed(self, data):\n        data = data.replace("</\' + \'script>", "</ignore>")\n        HTMLParser.HTMLParser.feed(self, data)\n    \n    def outtextf(self, s): \n        self.outtextlist.append(s)\n        if s: self.lastWasNL = s[-1] == \'\\n\'\n    \n    def close(self):\n        HTMLParser.HTMLParser.close(self)\n        \n        self.pbr()\n        self.o(\'\', 0, \'end\')\n\n        self.outtext = self.outtext.join(self.outtextlist)\n        \n        if options.google_doc:\n            self.outtext = self.outtext.replace(\'&nbsp_place_holder;\', \' \');\n        \n        return self.outtext\n        \n    def handle_charref(self, c):\n        self.o(charref(c), 1)\n\n    def handle_entityref(self, c):\n        self.o(entityref(c), 1)\n            \n    def handle_starttag(self, tag, attrs):\n        self.handle_tag(tag, attrs, 1)\n    \n    def handle_endtag(self, tag):\n        self.handle_tag(tag, None, 0)\n        \n    def previousIndex(self, attrs):\n        \"\"\" returns the index of certain set of attributes (of a link) in the\n            self.a list\n \n            If the set of attributes is not found, returns None\n        \"\"\"\n        if not has_key(attrs, \'href\'): return\n        \n        i = -1\n        for a in self.a:\n            i += 1\n            match = 0\n            \n            if has_key(a, \'href\') and a[\'href\'] == attrs[\'href\']:\n                if has_key(a, \'title\') or has_key(attrs, \'title\'):\n                        if (has_key(a, \'title\') and has_key(attrs, \'title\') and\n                            a[\'title\'] == attrs[\'title\']):\n                            match = True\n                else:\n                    match = True\n\