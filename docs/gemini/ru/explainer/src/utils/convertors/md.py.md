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
```

### 1. **Блок-схема**:

```mermaid
graph LR
    A[Начало: Функция md2dict] --> B{Преобразование Markdown в HTML через md2html};
    B -- Успешно --> C{Инициализация словаря sections и current_section};
    B -- Ошибка --> E[Логгирование ошибки и возврат пустого словаря];
    C --> D{Разбиение HTML на строки};
    D --> Loop{Для каждой строки};
    Loop --> F{Строка начинается с '<h'?};
    F -- Да --> G{Извлечение уровня заголовка и текста};
    G --> H{Уровень заголовка == 1?};
    H -- Да --> I{Установка заголовка как current_section и создание нового списка в sections};
    H -- Нет --> J{current_section существует?};
    J -- Да --> K{Добавление заголовка в текущий раздел sections};
    J -- Нет --> Loop;
    F -- Нет --> L{Строка не пустая и current_section существует?};
    L -- Да --> M{Удаление HTML тегов и добавление текста в текущий раздел sections};
    L -- Нет --> Loop;
    Loop --> N{Конец цикла?};
    N -- Да --> O[Возврат словаря sections];
    N -- Нет --> Loop;
```

**Примеры для каждого логического блока:**

- **A**: Функция `md2dict` получает строку Markdown как входные данные.
  ```python
  md_string = "# Section 1\nThis is the content of section 1."
  ```
- **B**: Markdown преобразуется в HTML. Если возникает ошибка, она логируется, и возвращается пустая строка.
  ```python
  html = md2html(md_string)
  ```
- **C**: Инициализируются пустой словарь `sections` и переменная `current_section`.
  ```python
  sections: Dict[str, list[str]] = {}
  current_section: str | None = None
  ```
- **D**: HTML разбивается на строки для последующей обработки.
  ```python
  lines = html.splitlines()
  ```
- **F**: Проверяется, начинается ли строка с HTML-тега заголовка `<h`.
  ```python
  line = "<h1>Section 1</h1>"
  if line.startswith('<h'):
      # ...
  ```
- **G**: Извлекается уровень заголовка и текст заголовка.
  ```python
  heading_level_match = re.search(r'h(\\d)', line)
  if heading_level_match:
      heading_level = int(heading_level_match.group(1))
      section_title = re.sub(r'<.*?>', '', line).strip()
  ```
- **H**: Проверяется, является ли уровень заголовка равным 1 (<h1>).
  ```python
  if heading_level == 1:
      # ...
  ```
- **I**: Устанавливается текущий раздел и создается новый список для него.
  ```python
  current_section = section_title
  sections[current_section] = []
  ```
- **J**: Проверяется, существует ли `current_section`.
  ```python
  if current_section:
      # ...
  ```
- **K**: Добавляется текст заголовка в текущий раздел.
  ```python
  sections[current_section].append(section_title)
  ```
- **L**: Проверяется, не является ли строка пустой и существует ли `current_section`.
  ```python
  line = "This is the content."
  if line.strip() and current_section:
      # ...
  ```
- **M**: Очищается текст от HTML-тегов и добавляется в текущий раздел.
  ```python
  clean_text = re.sub(r'<.*?>', '', line).strip()
  sections[current_section].append(clean_text)
  ```
- **O**: Возвращается структурированный словарь `sections`.
  ```python
  return sections
  ```

### 2. **Диаграмма**:

```mermaid
graph TD
    A[md2dict: Преобразование Markdown в словарь] --> B(md2html: Преобразование Markdown в HTML);
    B --> C{markdown2.markdown: Основная функция преобразования};
    C --> D[logger.error: Логгирование ошибок];
    A --> E{re.search: Поиск уровня заголовка};
    A --> F{re.sub: Удаление HTML тегов};
    A --> G[logger.error: Логгирование ошибок];
```

**Объяснение зависимостей:**

- `md2dict` вызывает функцию `md2html` для преобразования Markdown в HTML.
- `md2html` использует `markdown2.markdown` для фактического преобразования Markdown в HTML и `logger.error` для логгирования ошибок.
- `md2dict` использует `re.search` для поиска уровня заголовка и `re.sub` для удаления HTML тегов.
- `md2dict` использует `logger.error` для логгирования ошибок.

### 3. **Объяснение**:

- **Импорты**:
  - `re`: Используется для работы с регулярными выражениями, необходимо для поиска и извлечения информации из HTML-строк (например, уровней заголовков).
  - `typing.Dict`, `typing.List`, `typing.Any`: Используются для аннотации типов, что улучшает читаемость и помогает в отладке. `Dict` для словарей, `List` для списков, `Any` для переменных любого типа.
  - `markdown2.markdown`: Используется для преобразования Markdown-строки в HTML-формат.
  - `src.logger.logger.logger`: Используется для логгирования ошибок и отладочной информации.

- **Функции**:
  - `md2html(md_string: str, extras: List[str] = None) -> str`:
    - Аргументы:
      - `md_string` (str): Строка в формате Markdown, которую необходимо преобразовать в HTML.
      - `extras` (List[str], optional): Список расширений для `markdown2`. По умолчанию `None`.
    - Возвращаемое значение:
      - `str`: HTML-представление входной Markdown-строки.
    - Назначение:
      - Функция преобразует Markdown в HTML, используя библиотеку `markdown2`. Если происходит ошибка, она логируется, и возвращается пустая строка.
  - `md2dict(md_string: str, extras: List[str] = None) -> Dict[str, list[str]]`:
    - Аргументы:
      - `md_string` (str): Строка в формате Markdown, которую необходимо преобразовать в структурированный словарь.
      - `extras` (List[str], optional): Список расширений для `markdown2`. По умолчанию `None`.
    - Возвращаемое значение:
      - `Dict[str, list[str]]`: Структурированный словарь, где ключи — это заголовки первого уровня, а значения — списки содержимого этих разделов.
    - Назначение:
      - Функция принимает Markdown-строку, преобразует её в HTML, затем структурирует HTML-контент в словарь, где ключами являются заголовки разделов, а значениями — содержимое этих разделов.

- **Переменные**:
  - `html (str)`: Содержит HTML-представление Markdown-строки, полученное из функции `md2html`.
  - `sections (Dict[str, list[str]])`: Словарь, который хранит структурированное представление Markdown-контента. Ключи — заголовки разделов, значения — списки строк содержимого.
  - `current_section (str | None)`: Переменная, которая хранит текущий обрабатываемый раздел (заголовок).
  - `line (str)`: Текущая строка HTML-кода при итерации по строкам.
  - `heading_level_match (re.Match[str] | None)`: Результат поиска уровня заголовка с использованием регулярного выражения.
  - `heading_level (int)`: Уровень заголовка (например, 1 для `<h1>`, 2 для `<h2>`).
  - `section_title (str)`: Текст заголовка, очищенный от HTML-тегов.
  - `clean_text (str)`: Текст строки, очищенный от HTML-тегов.

- **Потенциальные ошибки и области для улучшения**:
  - **Обработка вложенных заголовков**: Текущая реализация обрабатывает только заголовки первого уровня как разделы. Необходимо расширить функциональность для обработки вложенных заголовков разных уровней.
  - **Более надежная очистка HTML**: Использование простого `re.sub` для удаления HTML-тегов может быть недостаточным. Рассмотреть использование более надежных инструментов, таких как `BeautifulSoup`.
  - **Обработка других элементов Markdown**: В текущей реализации обрабатываются только заголовки и простой текст. Необходимо добавить поддержку для других элементов Markdown, таких как списки, ссылки, изображения и т.д.
  - **Логирование**: Добавить больше логгирования для отслеживания процесса и облегчения отладки.

**Цепочка взаимосвязей с другими частями проекта**:

1.  **Входные данные**: Модуль получает Markdown-текст, который может быть прочитан из файла или получен из внешнего источника.
2.  **Преобразование в HTML**: Markdown преобразуется в HTML с использованием `markdown2`.
3.  **Структурирование данных**: HTML анализируется и структурируется в словарь, где ключи — это заголовки разделов, а значения — содержимое этих разделов.
4.  **Выходные данные**: Структурированный словарь может быть использован другими модулями для дальнейшей обработки, например, для создания отчетов или другого представления данных.
5.  **Логгирование**: Все ошибки и важные события логируются с использованием модуля `src.logger.logger`.