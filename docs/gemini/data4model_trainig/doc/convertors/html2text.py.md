### Анализ кода модуля `hypotez/src/utils/convertors/html2text.py`

## Обзор

Этот модуль предназначен для преобразования HTML в текст с Markdown-подобной структурой.

## Подробнее

Модуль содержит функции для преобразования HTML-контента в удобочитаемый текст, используя разметку, аналогичную Markdown. Он включает поддержку различных HTML-элементов, обработки ссылок, изображений и форматирования текста.

## Функции

### `has_key`

```python
def has_key(x, y):
    if hasattr(x, 'has_key'): return x.has_key(y)
    else: return y in x
```

**Назначение**:
Проверяет наличие ключа в словаре или объекте, поддерживающем доступ по ключу.

**Параметры**:
- `x`: Объект, в котором нужно проверить наличие ключа.
- `y`: Ключ для проверки.

**Возвращает**:
- `bool`: `True`, если ключ присутствует в объекте, иначе `False`.

**Как работает функция**:
1. Проверяет, имеет ли объект `x` метод `has_key`.
2. Если метод `has_key` существует, вызывает его для проверки наличия ключа `y`.
3. В противном случае проверяет наличие ключа `y` в объекте `x` с помощью оператора `in`.

### `name2cp`

```python
def name2cp(k):
    if k == 'apos': return ord("\'")
    if hasattr(htmlentitydefs, "name2codepoint"): # requires Python 2.3
        return htmlentitydefs.name2codepoint[k]
    else:
        k = htmlentitydefs.entitydefs[k]
        if k.startswith("&#") and k.endswith(";"): return int(k[2:-1]) # not in latin-1
        return ord(codecs.latin_1_decode(k)[0])
```

**Назначение**:
Преобразует имя HTML-сущности в её кодовую точку Unicode.

**Параметры**:
- `k` (str): Имя HTML-сущности.

**Возвращает**:
- `int`: Кодовая точка Unicode для сущности.

**Как работает функция**:

1. Если `k` равно `'apos'`, возвращает кодовую точку символа апострофа.
2. Если в модуле `htmlentitydefs` есть атрибут `name2codepoint` (Python 2.3+), возвращает соответствующую кодовую точку.
3. В противном случае получает значение сущности из `htmlentitydefs.entitydefs`.
4. Если значение начинается с `"&#"` и заканчивается `";"`, преобразует подстроку между `"&#"` и `";"` в целое число.
5. Возвращает кодовую точку символа, полученную декодированием значения сущности в кодировке latin-1.

### `charref`

```python
def charref(name):
    if name[0] in ['x','X']:
        c = int(name[1:], 16)
    else:
        c = int(name)
    
    if not UNICODE_SNOB and c in unifiable_n.keys():
        return unifiable_n[c]
    else:
        try:
            return chr(c)
        except NameError: #Python3
            return chr(c)
```

**Назначение**:
Преобразует числовую ссылку на символ в Unicode символ.

**Параметры**:
- `name` (str): Числовая ссылка на символ.

**Возвращает**:
- `str`: Unicode символ.

**Как работает функция**:

1. Проверяет, начинается ли `name` с `'x'` или `'X'`, чтобы определить, является ли ссылка шестнадцатеричной.
2. Преобразует `name` в целое число (по основанию 16, если ссылка шестнадцатеричная).
3. Если включен режим `UNICODE_SNOB` или кодовая точка `c` отсутствует в `unifiable_n`, пытается преобразовать `c` в Unicode символ с помощью `chr()`.
4. Возвращает Unicode символ.

### `entityref`

```python
def entityref(c):
    if not UNICODE_SNOB and c in unifiable.keys():
        return unifiable[c]
    else:
        try: name2cp(c)
        except KeyError: return "&" + c + ';'
        else:
            try:
                return chr(name2cp(c))
            except NameError: #Python3
                return chr(name2cp(c))
```

**Назначение**:
Преобразует именованную ссылку на сущность в Unicode символ.

**Параметры**:
- `c` (str): Именованная ссылка на сущность.

**Возвращает**:
- `str`: Unicode символ или строка в формате "&c;", если преобразование невозможно.

**Как работает функция**:

1. Если включен режим `UNICODE_SNOB` или сущность `c` отсутствует в `unifiable`, пытается преобразовать `c` в Unicode символ с помощью `name2cp(c)` и `chr()`.
2. Если преобразование успешно, возвращает Unicode символ.
3. В противном случае возвращает строку в формате "&c;".

### `replaceEntities`

```python
def replaceEntities(s):
    s = s.group(1)
    if s[0] == "#": 
        return charref(s[1:])
    else: return entityref(s)
```

**Назначение**:
Заменяет HTML-сущности в строке Unicode символами.

**Параметры**:
- `s`: Объект соответствия регулярного выражения.

**Возвращает**:
- `str`: Unicode символ или строка в формате "&c;", если преобразование невозможно.

**Как работает функция**:

1. Извлекает группу из объекта соответствия `s`.
2. Если первый символ извлеченной группы равен "#", вызывает функцию `charref` для преобразования числовой ссылки на символ.
3. В противном случае вызывает функцию `entityref` для преобразования именованной ссылки на сущность.
4. Возвращает результат.

### `unescape`

```python
r_unescape = re.compile(r"&(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));")
def unescape(s):
    return r_unescape.sub(replaceEntities, s)
```

**Назначение**:
Заменяет HTML-сущности в строке Unicode символами.

**Параметры**:
- `s` (str): Строка, содержащая HTML-сущности.

**Возвращает**:
- `str`: Строка с замененными HTML-сущностями.

**Как работает функция**:

1. Использует регулярное выражение `r_unescape` для поиска HTML-сущностей в строке `s`.
2. Заменяет каждую найденную сущность результатом вызова функции `replaceEntities`.

### `onlywhite`

```python
def onlywhite(line):
    """Return true if the line does only consist of whitespace characters."""
    for c in line:
        if c is not ' ' and c is not '\t':
            return c is ' '
    return line
```

**Назначение**:
Проверяет, состоит ли строка только из пробельных символов.

**Параметры**:
- `line` (str): Строка для проверки.

**Возвращает**:
- `bool`: `True`, если строка состоит только из пробельных символов, иначе `False`.

**Как работает функция**:

1. Перебирает каждый символ в строке `line`.
2. Если символ не является пробелом или символом табуляции, возвращает `False`.
3. Если все символы являются пробелами или символами табуляции, возвращает `True`.

### `optwrap`

```python
def optwrap(text):
    """Wrap all paragraphs in the provided text."""
    if not BODY_WIDTH:
        return text
    
    assert wrap, "Requires Python 2.3."
    result = ''
    newlines = 0
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
```

**Назначение**:
Переносит все абзацы в предоставленном тексте на новую строку, соблюдая ограничение по ширине строки.

**Параметры**:
- `text` (str): Текст для переноса.

**Возвращает**:
- `str`: Текст с перенесенными абзацами.

**Как работает функция**:

1.  Если `BODY_WIDTH` равно 0, возвращает исходный текст без изменений.
2.  Использует `textwrap.wrap` для переноса каждого абзаца в тексте.
3.  Перебирает абзацы в тексте, разделенном символом новой строки.
4.  Если абзац не начинается с пробела, тире или звездочки, переносит абзац на новые строки, используя `textwrap.wrap` с указанной шириной `BODY_WIDTH`.
5.  Добавляет перенесенные строки и символы новой строки в результат.
6.  Возвращает результат.

### `hn`

```python
def hn(tag):
    if tag[0] == 'h' and len(tag) == 2:
        try:
            n = int(tag[1])
            if n in range(1, 10): return n
        except ValueError: return 0
```

**Назначение**:
Определяет уровень заголовка (h1, h2, и т. д.) из тега HTML.

**Параметры**:
- `tag` (str): Строка, представляющая HTML-тег.

**Возвращает**:
- `int`: Уровень заголовка (1-9), или 0, если тег не является заголовком.

**Как работает функция**:

1. Проверяет, начинается ли тег с 'h' и имеет ли длину 2.
2. Пытается преобразовать второй символ тега в целое число.
3. Если преобразование успешно и число находится в диапазоне от 1 до 9, возвращает это число.
4. В противном случае возвращает 0.

### `dumb_property_dict`

```python
def dumb_property_dict(style):
    """returns a hash of css attributes"""
    return dict([(x.strip(), y.strip()) for x, y in [z.split(':', 1) for z in style.split(';') if ':' in z]]);
```

**Назначение**:
Преобразует строку стилей CSS в словарь атрибутов.

**Параметры**:
- `style` (str): Строка, содержащая стили CSS.

**Возвращает**:
- `dict`: Словарь, где ключами являются атрибуты CSS, а значениями - их значения.

**Как работает функция**:

1.  Разделяет строку `style` на части по символу `;`.
2.  Фильтрует части, оставляя только те, которые содержат символ `:`.
3.  Для каждой части разделяет ее на атрибут и значение по символу `:`.
4.  Удаляет пробелы в начале и конце атрибута и значения.
5.  Создает словарь, где ключами являются атрибуты, а значениями - их значения.

### `dumb_css_parser`

```python
def dumb_css_parser(data):
    """returns a hash of css selectors, each of which contains a hash of css attributes"""
    # remove @import sentences
    importIndex = data.find('@import')
    while importIndex != -1:
        data = data[0:importIndex] + data[data.find(';', importIndex) + 1:]
        importIndex = data.find('@import')

    # parse the css. reverted from dictionary compehension in order to support older pythons
    elements =  [x.split('{') for x in data.split('}') if '{' in x.strip()]
    elements = dict([(a.strip(), dumb_property_dict(b)) for a, b in elements])

    return elements
```

**Назначение**:
Преобразует строку CSS в словарь селекторов, каждый из которых содержит словарь атрибутов CSS.

**Параметры**:
- `data` (str): Строка, содержащая CSS.

**Возвращает**:
- `dict`: Словарь селекторов CSS, где значения - словари атрибутов.

**Как работает функция**:

1.  Удаляет все строки `@import` из CSS-данных.
2.  Разделяет CSS-данные на блоки по символу `}`.
3.  Фильтрует блоки, оставляя только те, которые содержат символ `{`.
4.  Для каждого блока разделяет его на селектор и свойства по символу `{`.
5.  Удаляет пробелы в начале и конце селектора.
6.  Преобразует строку свойств в словарь атрибутов с помощью функции `dumb_property_dict`.
7.  Создает словарь, где ключами являются селекторы, а значениями - словари атрибутов.

### `element_style`

```python
def element_style(attrs, style_def, parent_style):
    """returns a hash of the 'final' style attributes of the element"""
    style = parent_style.copy()
    if 'class' in attrs:
        for css_class in attrs['class'].split():
            css_style = style_def['.' + css_class]
            style.update(css_style)
    if 'style' in attrs:
        immediate_style = dumb_property_dict(attrs['style'])
        style.update(immediate_style)
    return style
```

**Назначение**:
Формирует окончательный набор стилей для элемента на основе атрибутов, стилей CSS и стилей родительского элемента.

**Параметры**:
- `attrs` (dict): Атрибуты элемента.
- `style_def` (dict): Определения стилей CSS.
- `parent_style` (dict): Стили родительского элемента.

**Возвращает**:
- `dict`: Словарь стилей для элемента.

**Как работает функция**:

1. Копирует стили родительского элемента в новый словарь `style`.
2. Если элемент имеет атрибут `class`, перебирает все классы, указанные в этом атрибуте.
3. Для каждого класса получает соответствующие стили из `style_def` и добавляет их в словарь `style`.
4. Если элемент имеет атрибут `style`, преобразует его в словарь стилей с помощью `dumb_property_dict` и добавляет их в словарь `style`.
5. Возвращает полученный словарь стилей.

### `google_list_style`

```python
def google_list_style(style):
    """finds out whether this is an ordered or unordered list"""
    if 'list-style-type' in style:
        list_style = style['list-style-type']
        if list_style in ['disc', 'circle', 'square', 'none']:
            return 'ul'
    return 'ol'
```

**Назначение**:
Определяет, является ли список упорядоченным или неупорядоченным, на основе CSS-стилей Google Docs.

**Параметры**:
- `style` (dict): Словарь стилей CSS.

**Возвращает**:
- `str`: `'ul'`, если список неупорядоченный, иначе `'ol'` (упорядоченный).

**Как работает функция**:

1. Проверяет наличие атрибута `list-style-type` в стилях.
2. Если атрибут присутствует и его значение - один из маркеров неупорядоченного списка (`'disc'`, `'circle'`, `'square'`, `'none'`), возвращает `'ul'`.
3. В противном случае возвращает `'ol'`.

### `google_nest_count`

```python
def google_nest_count(style):
    """calculate the nesting count of google doc lists"""
    nest_count = 0
    if 'margin-left' in style:
        nest_count = int(style['margin-left'][:-2]) / GOOGLE_LIST_INDENT
    return nest_count
```

**Назначение**:
Вычисляет уровень вложенности списка Google Docs на основе CSS-стилей.

**Параметры**:
- `style` (dict): Словарь стилей CSS.

**Возвращает**:
- `int`: Уровень вложенности списка.

**Как работает функция**:

1.  Инициализирует `nest_count` значением 0.
2.  Проверяет, присутствует ли атрибут `margin-left` в стилях.
3.  Если атрибут присутствует, извлекает значение отступа слева, удаляет последние два символа (предположительно "px") и преобразует значение в целое число.
4.  Делит полученное число на `GOOGLE_LIST_INDENT` (количество пикселей, на которое Google Docs сдвигает вложенные списки).
5.  Возвращает уровень вложенности.

### `google_has_height`

```python
def google_has_height(style):
    """check if the style of the element has the 'height' attribute explicitly defined"""
    if 'height' in style:
        return True
    return False
```

**Назначение**:
Проверяет, определен ли атрибут 'height' в стилях элемента Google Docs.

**Параметры**:
- `style` (dict): Словарь стилей CSS.

**Возвращает**:
- `bool`: True, если атрибут 'height' явно определен, иначе False.

**Как работает функция**:

1.  Проверяет наличие ключа `'height'` в словаре `style`.
2.  Возвращает `True`, если ключ существует, и `False` в противном случае.

### `google_text_emphasis`

```python
def google_text_emphasis(style):
    """return a list of all emphasis modifiers of the element"""
    emphasis = []
    if 'text-decoration' in style:
        emphasis.append(style['text-decoration'])
    if 'font-style' in style:
        emphasis.append(style['font-style'])
    if 'font-weight' in style:
        emphasis.append(style['font-weight'])
    return emphasis
```

**Назначение**:
Возвращает список всех модификаторов выделения текста элемента Google Docs.

**Параметры**:
- `style` (dict): Словарь стилей CSS.

**Возвращает**:
- `list`: Список модификаторов выделения текста.

**Как работает функция**:

1. Создает пустой список `emphasis`.
2.  Проверяет наличие атрибутов `'text-decoration'`, `'font-style'` и `'font-weight'` в стилях.
3.  Если атрибут присутствует, добавляет его значение в список `emphasis`.
4.  Возвращает список `emphasis`.

### `google_fixed_width_font`

```python
def google_fixed_width_font(style):
    """check if the css of the current element defines a fixed width font"""
    font_family = ''
    if 'font-family' in style:
        font_family = style['font-family']
    if 'Courier New' == font_family or 'Consolas' == font_family:
        return True
    return False
```

**Назначение**:
Проверяет, определяет ли CSS текущего элемента шрифт фиксированной ширины.

**Параметры**:
- `style` (dict): Словарь стилей CSS.

**Возвращает**:
- `bool`: `True`, если определен шрифт фиксированной ширины, иначе `False`.

**Как работает функция**:

1.  Извлекает значение атрибута `font-family` из стилей.
2.  Если значение равно `'Courier New'` или `'Consolas'`, возвращает `True`.
3.  В противном случае возвращает `False`.

### `list_numbering_start`

```python
def list_numbering_start(attrs):
    """extract numbering from list element attributes"""
    if 'start' in attrs:
        return int(attrs['start']) - 1
    else:
        return 0
```

**Назначение**:
Извлекает начальное значение нумерации из атрибутов элемента списка.

**Параметры**:
- `attrs` (dict): Словарь атрибутов элемента списка.

**Возвращает**:
- `int`: Начальное значение нумерации или 0, если атрибут 'start' не найден.

**Как работает функция**:

1.  Проверяет, присутствует ли атрибут `start` в атрибутах элемента списка.
2.  Если атрибут присутствует, преобразует его значение в целое число и вычитает 1.
3.  Возвращает полученное число или 0, если атрибут отсутствует.

### `_html2text`

```python
class _html2text(HTMLParser.HTMLParser):
    def __init__(self, out=None, baseurl=''):
        HTMLParser.HTMLParser.__init__(self)
        
        if out is None: self.out = self.outtextf
        else: self.out = out
        self.outtextlist = [] # empty list to store output characters before they are  "joined"
        try:
            self.outtext = unicode()
        except NameError: # Python3
            self.outtext = str()
        self.quiet = 0
        self.p_p = 0 # number of newline character to print before next output
        self.outcount = 0
        self.start = 1
        self.space = 0
        self.a = []
        self.astack = []
        self.acount = 0
        self.list = []
        self.blockquote = 0
        self.pre = 0
        self.startpre = 0
        self.code = False
        self.br_toggle = ''
        self.lastWasNL = 0
        self.lastWasList = False
        self.style = 0
        self.style_def = {}
        self.tag_stack = []
        self.emphasis = 0
        self.drop_white_space = 0
        self.inheader = False
        self.abbr_title = None # current abbreviation definition
        self.abbr_data = None # last inner HTML (for abbr being defined)
        self.abbr_list = {} # stack of abbreviations to write later
        self.baseurl = baseurl

        if options.google_doc:
            del unifiable_n[name2cp('nbsp')]
            unifiable['nbsp'] = '&nbsp_place_holder;'
    
    def feed(self, data):
        data = data.replace("</\' + \'script>", "</ignore>")
        HTMLParser.HTMLParser.feed(self, data)
    
    def outtextf(self, s): 
        self.outtextlist.append(s)
        if s: self.lastWasNL = s[-1] == '\n'
    
    def close(self):
        HTMLParser.HTMLParser.close(self)
        
        self.pbr()
        self.o('', 0, 'end')

        self.outtext = self.outtext.join(self.outtextlist)
        
        if options.google_doc:
            self.outtext = self.outtext.replace('&nbsp_place_holder;', ' ');
        
        return self.outtext
        
    def handle_charref(self, c):
        self.o(charref(c), 1)

    def handle_entityref(self, c):
        self.o(entityref(c), 1)
            
    def handle_starttag(self, tag, attrs):
        self.handle_tag(tag, attrs, 1)
    
    def handle_endtag(self, tag):
        self.handle_tag(tag, None, 0)
        
    def previousIndex(self, attrs):
        """ returns the index of certain set of attributes (of a link) in the
            self.a list
 
            If the set of attributes is not found, returns None
        """
        if not has_key(attrs, 'href'): return
        
        i = -1
        for a in self.a:
            i += 1
            match = 0
            
            if has_key(a, 'href') and a['href'] == attrs['href']:
                if has_key(a, 'title') or has_key(attrs, 'title'):
                        if (has_key(a, 'title') and has_key(attrs, 'title') and
                            a['title'] == attrs['title']):
                            match = True
                else:
                    match = True

            if match: return i

    def drop_last(self, nLetters):
        if not self.quiet:
            self.outtext = self.outtext[:-nLetters]
           
    def handle_emphasis(self, start, tag_style, parent_style):
        """handles various text emphases"""
        tag_emphasis = google_text_emphasis(tag_style)
        parent_emphasis = google_text_emphasis(parent_style)

        # handle Google\'s text emphasis
        strikethrough =  \'line-through\' in tag_emphasis and options.hide_strikethrough
        bold = \'bold\' in tag_emphasis and not \'bold\' in parent_emphasis
        italic = \'italic\' in tag_emphasis and not \'italic\' in parent_emphasis
        fixed = google_fixed_width_font(tag_style) and not \
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
                self.o(\'`\')
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
                    self.o(\'`\')
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

    def handle_tag(self, tag, attrs, start):
        #attrs = fixattrs(attrs)
        if attrs is None:
            attrs = {}
        else:
            attrs = dict(attrs)

        if options.google_doc:
            # the attrs parameter is empty for a closing tag. in addition, we
            # need the attributes of the parent nodes in order to get a
            # complete style description for the current element. we assume
            # that google docs export well formed html.
            parent_style = {}
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
                self.o(hn(tag)*"#" + ' ')
            else:
                self.inheader = False
                return # prevent redundant emphasis marks on headers

        if tag in ['p', 'div']:
            if options.google_doc:
                if start and google_has_height(tag_style):
                    self.p()
                else:
                    self.soft_br()
            else:
                self.p()
        
        if tag == "br" and start: self.o("  \n")

        if tag == "hr" and start:
            self.p()
            self.o("* * *")
            self.p()

        if tag in ["head", "style", 'script']: 
            if start: self.quiet += 1
            else: self.quiet -= 1

        if tag == "style":
            if start: self.style += 1
            else: self.style -= 1

        if tag in ["body"]:
            self.quiet = 0 # sites like 9rules.com never close <head>
        
        if tag == "blockquote":
            if start: 
                self.p(); self.o('> ', 0, 1); self.start = 1
                self.blockquote += 1
            else:
                self.blockquote -= 1
                self.p()
        
        if tag in ['em', 'i', 'u']: self.o("_")
        if tag in ['strong', 'b']: self.o("**")
        if tag in ['del', 'strike']:\n            if start:\n                self.o("<"+tag+">")
            else:
                self.o("</"+tag+">")

        if options.google_doc:
            if not self.inheader:
                # handle some font attributes, but leave headers clean
                self.handle_emphasis(start, tag_style, parent_style)

        if tag == "code" and not self.pre: self.o(\'`\') #TODO: `` `this` ``
        if tag == "abbr":
            if start:
                self.abbr_title = None
                self.abbr_data = \'\'
                if has_key(attrs, \'title\'):
                    self.abbr_title = attrs[\'title\']
            else:
                if self.abbr_title != None:
                    self.abbr_list[self.abbr_data] = self.abbr_title
                    self.abbr_title = None
                self.abbr_data = \'\'
        
        if tag == "a" and not IGNORE_ANCHORS:
            if start:
                if has_key(attrs, \'href\') and not (SKIP_INTERNAL_LINKS and attrs[\'href\'].startswith(\'#\')): 
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
            if has_key(attrs, \'src\'):
                attrs[\'href\'] = attrs[\'src\']
                alt = attrs.get(\'alt\', \'\')
                if INLINE_LINKS:
                    self.o("![")
                    self.o(alt)
                    self.o("]("+ attrs['href'] +")")
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
                    self.o("]["+ str(attrs['count']) +"]")
        
        if tag == \'dl\' and start: self.p()
        if tag == \'dt\' and not start: self.pbr()
        if tag == \'dd\' and start: self.o(\'    \')
        if tag == \'dd\' and not start: self.pbr()
        
        if tag in ["ol", "ul"]:\n            # Google Docs create sub lists as top level lists\n            if (not self.list) and (not self.lastWasList):\n                self.p()\n            if start:\n                if options.google_doc:\n                    list_style = google_list_style(tag_style)\n                else:\n                    list_style = tag\n                numbering_start = list_numbering_start(attrs)\n                self.list.append({\'name\':list_style, \'num\':numbering_start})\n            else:\n                if self.list: self.list.pop()\n            self.lastWasList = True\n        else:\n            self.lastWasList = False\n        \n        if tag == \'li\':\n            self.pbr()\n            if start:\n                if self.list: li = self.list[-1]\n                else: li = {\'name\':\'ul\', \'num\':0}\n                if options.google_doc:\n                    nest_count = google_nest_count(tag_style)\n                else:\n                    nest_count = len(self