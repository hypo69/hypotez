### Анализ кода модуля `src/utils/convertors/html2text.py`

## Обзор

Этот модуль предоставляет утилиты для преобразования HTML-контента в Markdown-текст.

## Подробней

Модуль `src/utils/convertors/html2text.py` содержит функции и классы для преобразования HTML-кода в удобочитаемый Markdown-текст. Он использует библиотеку `html.parser` для разбора HTML и применяет различные правила и стили для создания Markdown-эквивалента. Этот модуль может быть полезен для извлечения информации из веб-страниц, очистки HTML-кода и подготовки текста для дальнейшей обработки.

## Функции

### `has_key`

```python
def has_key(x, y):\n    if hasattr(x, 'has_key'): return x.has_key(y)\n    else: return y in x
```

Проверяет, содержит ли объект `x` ключ `y`.

**Параметры**:

-   `x`: Объект для проверки (словарь или объект с методом `has_key`).
-   `y`: Ключ для поиска.

**Возвращает**:

-   `bool`: `True`, если объект содержит ключ, `False` - в противном случае.

**Как работает функция**:

1.  Проверяет, имеет ли объект `x` метод `has_key`.
2.  Если метод `has_key` существует, использует его для проверки наличия ключа `y`.
3.  В противном случае использует оператор `in` для проверки наличия ключа `y` в объекте `x`.

### `charref`

```python
def charref(name):\n    if name[0] in ['x','X']:\n        c = int(name[1:], 16)\n    else:\n        c = int(name)\n    \n    if not UNICODE_SNOB and c in unifiable_n.keys():\n        return unifiable_n[c]\n    else:\n        try:\n            return chr(c)\n        except NameError: #Python3\n            return chr(c)
```

Преобразует числовую ссылку на символ в Unicode символ.

**Параметры**:

-   `name`: Числовая ссылка на символ (например, "x20" или "160").

**Возвращает**:

-   `str`: Unicode символ, соответствующий числовой ссылке.

**Как работает функция**:

1.  Определяет, является ли ссылка шестнадцатеричной (начинается с "x" или "X").
2.  Преобразует ссылку в целое число.
3.  Если `UNICODE_SNOB` выключен и символ найден в `unifiable_n`, возвращает соответствующее значение из `unifiable_n`.
4.  В противном случае пытается преобразовать число в Unicode символ с помощью `chr(c)`.

### `entityref`

```python
def entityref(c):\n    if not UNICODE_SNOB and c in unifiable.keys():\n        return unifiable[c]\n    else:\n        try: name2cp(c)\n        except KeyError: return "&" + c + \';\'\n        else:\n            try:\n                return chr(name2cp(c))\n            except NameError: #Python3\n                return chr(name2cp(c))
```

Преобразует ссылку на символ HTML в Unicode символ.

**Параметры**:

-   `c`: Строка, представляющая ссылку на символ (например, "nbsp").

**Возвращает**:

-   `str`: Unicode символ, соответствующий ссылке, или исходная ссылка, если символ не найден.

**Как работает функция**:

1.  Проверяет, находится ли ссылка `c` в словаре `unifiable`. Если да, возвращает соответствующее значение.
2.  В противном случае пытается преобразовать ссылку в Unicode символ, используя `name2cp(c)` и `chr()`.
3.  Если преобразование не удалось, возвращает исходную ссылку в формате "&c;".

### `replaceEntities`

```python
def replaceEntities(s):\n    s = s.group(1)\n    if s[0] == "#": \n        return charref(s[1:])\n    else: return entityref(s)
```

Заменяет HTML-сущности в строке на соответствующие символы.

**Параметры**:

-   `s`: Объект Match, полученный в результате применения регулярного выражения.

**Возвращает**:

-   `str`: Замененная строка.

**Как работает функция**:

1.  Извлекает группу из объекта `Match`.
2.  Если группа начинается с "#", вызывает функцию `charref` для преобразования числовой ссылки на символ.
3.  В противном случае вызывает функцию `entityref` для преобразования именованной ссылки на символ.

### `unescape`

```python
def unescape(s):\n    return r_unescape.sub(replaceEntities, s)
```

Заменяет HTML-сущности в строке, используя регулярное выражение.

**Параметры**:

-   `s` (str): Строка для обработки.

**Возвращает**:

-   `str`: Строка с замененными HTML-сущностями.

**Как работает функция**:

1.  Использует регулярное выражение `r_unescape` для поиска HTML-сущностей в строке `s`.
2.  Заменяет все найденные сущности, используя функцию `replaceEntities`.

### `onlywhite`

```python
def onlywhite(line):\n    """Return true if the line does only consist of whitespace characters."""\n    for c in line:\n        if c is not \' \' and c is not \'  \':\n            return c is \' \'\n    return line
```

Проверяет, состоит ли строка только из пробельных символов.

**Параметры**:

-   `line` (str): Строка для проверки.

**Возвращает**:

-   `bool`: `True`, если строка состоит только из пробельных символов, `False` - в противном случае.

**Как работает функция**:

1.  Перебирает все символы в строке `line`.
2.  Если находит символ, который не является пробелом или табуляцией, возвращает `False`.
3.  Если все символы являются пробельными, возвращает `True`.

### `optwrap`

```python
def optwrap(text):\n    """Wrap all paragraphs in the provided text."""\n    if not BODY_WIDTH:\n        return text\n    \n    assert wrap, "Requires Python 2.3."\n    result = \'\'\n    newlines = 0\n    for para in text.split("\\n"):\n        if len(para) > 0:\n            if para[0] != \' \' and para[0] != \'-\' and para[0] != \'*\':\n                for line in wrap(para, BODY_WIDTH):\n                    result += line + "\\n"\n                result += "\\n"\n                newlines = 2\n            else:\n                if not onlywhite(para):\n                    result += para + "\\n"\n                    newlines = 1\n        else:\n            if newlines < 2:\n                result += "\\n"\n                newlines += 1\n    return result
```

Переносит все абзацы в предоставленном тексте.

**Параметры**:

-   `text` (str): Текст для переноса.

**Возвращает**:

-   `str`: Текст с перенесенными абзацами.

**Как работает функция**:

1.  Проверяет, включено ли перенос строк (если `BODY_WIDTH` равно 0, возвращает исходный текст).
2.  Разбивает текст на абзацы по символу новой строки (`\n`).
3.  Для каждого абзаца, если он не начинается с пробела, дефиса или звездочки, переносит его на строки заданной ширины (`BODY_WIDTH`) с помощью функции `wrap`.
4.  Добавляет перенесенные строки и символы новой строки в результат.

### `hn`

```python
def hn(tag):\n    if tag[0] == \'h\' and len(tag) == 2:\n        try:\n            n = int(tag[1])\n            if n in range(1, 10): return n\n        except ValueError: return 0
```

Определяет уровень заголовка HTML (h1, h2, h3 и т.д.).

**Параметры**:

-   `tag` (str): Имя HTML-тега.

**Возвращает**:

-   `int`: Уровень заголовка (1 для h1, 2 для h2 и т.д.) или 0, если тег не является заголовком.

**Как работает функция**:

1.  Проверяет, начинается ли имя тега с "h" и имеет ли длину 2 символа.
2.  Пытается преобразовать второй символ тега в целое число.
3.  Если преобразование удалось и число находится в диапазоне от 1 до 9, возвращает это число.
4.  В противном случае возвращает 0.

### `dumb_property_dict`

```python
def dumb_property_dict(style):\n    """returns a hash of css attributes"""\n    return dict([(x.strip(), y.strip()) for x, y in [z.split(\':\', 1) for z in style.split(\';\') if \':\' in z]]);
```

Возвращает словарь CSS-атрибутов.

**Параметры**:

-   `style` (str): Строка, содержащая CSS-стили.

**Возвращает**:

-   `dict`: Словарь, где ключи - это имена CSS-атрибутов, а значения - их значения.

**Как работает функция**:

1.  Разбивает строку стилей на части по символу ";".
2.  Для каждой части, содержащей символ ":", разделяет ее на имя атрибута и значение.
3.  Удаляет пробельные символы в начале и конце имени атрибута и значения.
4.  Формирует словарь, используя имя атрибута в качестве ключа и значение в качестве значения словаря.

### `dumb_css_parser`

```python
def dumb_css_parser(data):\n    """returns a hash of css selectors, each of which contains a hash of css attributes"""\n    # remove @import sentences\n    importIndex = data.find(\'@import\')\n    while importIndex != -1:\n        data = data[0:importIndex] + data[data.find(\';\', importIndex) + 1:]\n        importIndex = data.find(\'@import\')\n\n    # parse the css. reverted from dictionary compehension in order to support older pythons\n    elements =  [x.split(\'{\') for x in data.split(\'}\') if \'{\' in x.strip()]
    elements = dict([(a.strip(), dumb_property_dict(b)) for a, b in elements])

    return elements
```

Возвращает словарь CSS-селекторов, каждый из которых содержит словарь CSS-атрибутов.

**Параметры**:

-   `data` (str): Строка, содержащая CSS-код.

**Возвращает**:

-   `dict`: Словарь, где ключи - это CSS-селекторы, а значения - словари CSS-атрибутов.

**Как работает функция**:

1.  Удаляет все `@import` из CSS-кода.
2.  Разбивает CSS-код на элементы по символу "}".
3.  Для каждого элемента, содержащего символ "{", разделяет его на селектор и стили.
4.  Преобразует стили в словарь с помощью функции `dumb_property_dict`.
5.  Формирует словарь, используя селектор в качестве ключа и словарь стилей в качестве значения.

### `element_style`

```python
def element_style(attrs, style_def, parent_style):\n    """returns a hash of the \'final\' style attributes of the element"""\n    style = parent_style.copy()\n    if \'class\' in attrs:\n        for css_class in attrs[\'class\'].split():\n            css_style = style_def[\'.\' + css_class]\n            style.update(css_style)\n    if \'style\' in attrs:\n        immediate_style = dumb_property_dict(attrs[\'style\'])\n        style.update(immediate_style)\n    return style
```

Возвращает словарь "окончательных" атрибутов стиля элемента.

**Параметры**:

-   `attrs` (dict): Словарь атрибутов элемента.
-   `style_def` (dict): Словарь определений стилей CSS.
-   `parent_style` (dict): Словарь стилей родительского элемента.

**Возвращает**:

-   `dict`: Словарь, содержащий "окончательные" атрибуты стиля элемента.

**Как работает функция**:

1.  Копирует стили родительского элемента в новый словарь `style`.
2.  Если элемент имеет атрибут `class`, перебирает все классы, указанные в атрибуте, и добавляет соответствующие стили из `style_def` в словарь `style`.
3.  Если элемент имеет атрибут `style`, преобразует его в словарь стилей с помощью функции `dumb_property_dict` и добавляет эти стили в словарь `style`.
4.  Возвращает словарь `style`, содержащий все стили элемента.

### `google_list_style`

```python
def google_list_style(style):\n    """finds out whether this is an ordered or unordered list"""\n    if \'list-style-type\' in style:\n        list_style = style[\'list-style-type\']\n        if list_style in [\'disc\', \'circle\', \'square\', \'none\']:\n            return \'ul\'\n    return \'ol\'
```

Определяет, является ли список упорядоченным или неупорядоченным (для Google Docs).

**Параметры**:

-   `style` (dict): Словарь CSS-стилей.

**Возвращает**:

-   `str`: "ul" для неупорядоченного списка или "ol" для упорядоченного списка.

**Как работает функция**:

1.  Проверяет наличие атрибута `list-style-type` в словаре стилей.
2.  Если атрибут присутствует и его значение равно "disc", "circle" или "square", возвращает "ul" (неупорядоченный список).
3.  В противном случае возвращает "ol" (упорядоченный список).

### `google_nest_count`

```python
def google_nest_count(style):\n    """calculate the nesting count of google doc lists"""\n    nest_count = 0\n    if \'margin-left\' in style:\n        nest_count = int(style[\'margin-left\'][:-2]) / GOOGLE_LIST_INDENT\n    return nest_count
```

Вычисляет уровень вложенности списка Google Docs.

**Параметры**:

-   `style` (dict): Словарь CSS-стилей.

**Возвращает**:

-   `int`: Уровень вложенности списка.

**Как работает функция**:

1.  Проверяет наличие атрибута `margin-left` в словаре стилей.
2.  Если атрибут присутствует, извлекает значение отступа, удаляет "px" в конце и делит на `GOOGLE_LIST_INDENT` (количество пикселей, на которое Google Docs отступает вложенные списки).
3.  Возвращает полученное значение уровня вложенности.

### `google_has_height`

```python
def google_has_height(style):\n    """check if the style of the element has the \'height\' attribute explicitly defined"""\n    if \'height\' in style:\n        return True\n    return False
```

Проверяет, определен ли атрибут "height" в стилях элемента Google Docs.

**Параметры**:

-   `style` (dict): Словарь CSS-стилей.

**Возвращает**:

-   `bool`: `True`, если атрибут "height" определен, `False` - в противном случае.

**Как работает функция**:

1.  Проверяет наличие атрибута `height` в словаре стилей.
2.  Возвращает `True`, если атрибут присутствует, и `False` - в противном случае.

### `google_text_emphasis`

```python
def google_text_emphasis(style):\n    """return a list of all emphasis modifiers of the element"""\n    emphasis = []\n    if \'text-decoration\' in style:\n        emphasis.append(style[\'text-decoration\'])\n    if \'font-style\' in style:\n        emphasis.append(style[\'font-style\'])\n    if \'font-weight\' in style:\n        emphasis.append(style[\'font-weight\'])\n    return emphasis
```

Возвращает список всех модификаторов выделения текста элемента Google Docs.

**Параметры**:

-   `style` (dict): Словарь CSS-стилей.

**Возвращает**:

-   `list`: Список модификаторов выделения (например, ["line-through", "italic", "bold"]).

**Как работает функция**:

1.  Создает пустой список `emphasis`.
2.  Проверяет наличие атрибутов `text-decoration`, `font-style` и `font-weight` в словаре стилей.
3.  Если атрибуты присутствуют, добавляет их значения в список `emphasis`.
4.  Возвращает список `emphasis`.

### `google_fixed_width_font`

```python
def google_fixed_width_font(style):\n    """check if the css of the current element defines a fixed width font"""\n    font_family = \'\'\n    if \'font-family\' in style:\n        font_family = style[\'font-family\']\n    if \'Courier New\' == font_family or \'Consolas\' == font_family:\n        return True\n    return False
```

Проверяет, использует ли элемент шрифт с фиксированной шириной (для Google Docs).

**Параметры**:

-   `style` (dict): Словарь CSS-стилей.

**Возвращает**:

-   `bool`: `True`, если используется шрифт с фиксированной шириной, `False` - в противном случае.

**Как работает функция**:

1.  Проверяет наличие атрибута `font-family` в словаре стилей.
2.  Если атрибут присутствует и его значение равно "Courier New" или "Consolas", возвращает `True`.
3.  В противном случае возвращает `False`.

### `list_numbering_start`

```python
def list_numbering_start(attrs):\n    """extract numbering from list element attributes"""\n    if \'start\' in attrs:\n        return int(attrs[\'start\']) - 1\n    else:\n        return 0
```

Извлекает начальное значение нумерации из атрибутов элемента списка.

**Параметры**:

-   `attrs` (dict): Словарь атрибутов элемента.

**Возвращает**:

-   `int`: Начальное значение нумерации (или 0, если атрибут "start" отсутствует).

**Как работает функция**:

1.  Проверяет наличие атрибута `start` в словаре атрибутов.
2.  Если атрибут присутствует, преобразует его значение в целое число и вычитает 1.
3.  Возвращает полученное значение.

### `_html2text`

Этот класс выполняет преобразование HTML в Markdown

*Методы*:

-`__init__`: инициализирует класс
-`feed`: подает данные в парсер
-`outhandler_charref`: обрабатывает числовые символьные ссылки
-`handle_entityref`: обрабатывает символьные ссылки на объекты
-`handle_starttag`: обрабатывает открывающие теги html
-`handle_endtag`: обрабатывает закрывающие теги html
-`previousIndex`: находит предыдущий индекс
-`drop_last`: обрезает строку
-`handle_emphasis`: обрабатывает выделение текста
-`handle_tag`: обрабатывает теги
-`pbr`: добавляет отступ
-`p`: добавляет отступ
-`soft_br`: добавляет мягкий перенос
-`o`: оборачивает данные
-`handle_data`: обрабатывает данные
-`unknown_decl`: обрабатывает неизвестные объявления

### `wrapwrite`

```python
def wrapwrite(text):\n    text = text.encode(\'utf-8\')\n    try: #Python3\n        sys.stdout.buffer.write(text)\n    except AttributeError:\n        sys.stdout.write(text)
```

Записывает текст в стандартный поток вывода, кодируя его в UTF-8.

**Параметры**:

-   `text` (str): Текст для записи.

**Как работает функция**:

1.  Кодирует текст в UTF-8.
2.  Пытается записать текст в стандартный поток вывода, используя `sys.stdout.buffer.write` (для Python 3).
3.  Если возникает исключение `AttributeError` (например, в Python 2), использует `sys.stdout.write`.

### `html2text_file`

```python
def html2text_file(html, out=wrapwrite, baseurl='\'):\n    h = _html2text(out, baseurl)\n    h.feed(html)\n    h.feed("")\n    return h.close()
```

Преобразует HTML в текст и записывает его в указанный поток вывода.

**Параметры**:

-   `html` (str): HTML-код для преобразования.
-   `out` (function, optional): Функция для вывода текста. По умолчанию `wrapwrite`.
-   `baseurl` (str, optional): Базовый URL для разрешения относительных ссылок. По умолчанию пустая строка.

**Возвращает**:

-   `str`: Преобразованный текст.

**Как работает функция**:

1.  Создает экземпляр класса `_html2text` (внутренний класс для парсинга HTML).
2.  Передает HTML-код в метод `feed` объекта `_html2text`.
3.  Вызывает метод `close` объекта `_html2text` для завершения обработки и получения результата.

### `html2text`

```python
def html2text(html, baseurl='\'):\n    return optwrap(html2text_file(html, None, baseurl))
```

Преобразует HTML в Markdown-текст, оборачивая абзацы.

**Параметры**:

-   `html` (str): HTML-код для преобразования.
-   `baseurl` (str, optional): Базовый URL для разрешения относительных ссылок. По умолчанию пустая строка.

**Возвращает**:

-   `str`: Markdown-текст.

**Как работает функция**:

1.  Преобразует HTML в текст, используя функцию `html2text_file`.
2.  Переносит абзацы в полученном тексте, используя функцию `optwrap`.

## Переменные модуля

-   `__version__` (str): Версия модуля.
-   `__author__` (str): Автор модуля.
-   `__copyright__` (str): Информация об авторских правах.
-   `UNICODE_SNOB` (int): Флаг, определяющий использование символов Unicode вместо их ascii-аналогов.
-   `LINKS_EACH_PARAGRAPH` (int): Флаг, определяющий размещение ссылок после каждого параграфа.
-   `BODY_WIDTH` (int): Ширина строки для переноса текста.
-   `SKIP_INTERNAL_LINKS` (bool): Флаг, определяющий пропуск внутренних ссылок.
-   `INLINE_LINKS` (bool): Флаг, определяющий использование встроенных ссылок.
-   `GOOGLE_LIST_INDENT` (int): Отступ для вложенных списков в Google Docs.
-   `IGNORE_ANCHORS` (bool): Флаг, определяющий игнорирование якорей.
-   `IGNORE_IMAGES` (bool): Флаг, определяющий игнорирование изображений.
- `options`:  Объект, используемый для хранения параметров

## Пример использования

```python
from src.utils.convertors import html2text

html_code = "<p>Hello, world!</p><a href='https://example.com'>Example</a>"
markdown_text = html2text.html2text(html_code)
print(markdown_text)
```

## Взаимосвязь с другими частями проекта

-   Этот модуль может использоваться другими модулями проекта `hypotez` для преобразования HTML-контента в Markdown-текст.
-   Функции `_html2text.o` и `wrapwrite` используются для вывода результата.