# Модуль для конвертации HTML в Markdown

## Обзор

Модуль `html2text` предназначен для преобразования HTML-документов в Markdown-формат. Он предоставляет функции для обработки HTML-разметки и создания удобочитаемого текста в формате Markdown.

## Подробнее

Этот модуль анализирует HTML-структуру и преобразует ее в соответствующий Markdown, поддерживая различные элементы, такие как заголовки, списки, ссылки и изображения. Он также включает опции для настройки форматирования, такие как перенос строк и обработка списков Google Docs.

## Классы

### `_html2text`

**Описание**: Класс `_html2text` является основным классом, который выполняет преобразование HTML в Markdown.

**Наследует**:
- `HTMLParser.HTMLParser`

**Атрибуты**:
- `out (Callable[[str], None])`: Функция для вывода текста. По умолчанию используется `self.outtextf`.
- `outtextlist (List[str])`: Список для хранения выводимых символов перед их объединением.
- `outtext (str)`: Строка, содержащая преобразованный текст.
- `quiet (int)`: Флаг, указывающий на необходимость подавления вывода.
- `p_p (int)`: Количество символов новой строки для вывода перед следующим текстом.
- `outcount (int)`: Счетчик выведенных символов.
- `start (int)`: Флаг, указывающий на начало документа.
- `space (int)`: Флаг, указывающий на необходимость добавления пробела.
- `a (List[dict])`: Список ссылок.
- `astack (List[dict])`: Стек ссылок.
- `acount (int)`: Счетчик ссылок.
- `list (List[dict])`: Список списков.
- `blockquote (int)`: Уровень цитирования.
- `pre (int)`: Флаг, указывающий на необходимость сохранения форматирования `<pre>`.
- `startpre (int)`: Флаг, указывающий на начало блока `<pre>`.
- `code (bool)`: Флаг, указывающий на нахождение внутри элемента `code`.
- `br_toggle (str)`: Строка для вставки перед символом новой строки.
- `lastWasNL (bool)`: Флаг, указывающий, был ли последний символ новой строкой.
- `lastWasList (bool)`: Флаг, указывающий, был ли последний элемент списком.
- `style (int)`: Флаг, указывающий на нахождение внутри элемента `style`.
- `style_def (dict)`: Словарь CSS-стилей.
- `tag_stack (List[Tuple[str, dict, dict]])`: Стек тегов.
- `emphasis (int)`: Уровень выделения текста.
- `drop_white_space (int)`: Флаг, указывающий на необходимость удаления пробелов.
- `inheader (bool)`: Флаг, указывающий на нахождение внутри заголовка.
- `abbr_title (Optional[str])`: Заголовок текущего определения аббревиатуры.
- `abbr_data (Optional[str])`: Последний внутренний HTML (для определяемой аббревиатуры).
- `abbr_list (dict)`: Стек аббревиатур для записи позже.
- `baseurl (str)`: Базовый URL для ссылок.

**Методы**:

### `__init__`

```python
def __init__(self, out=None, baseurl=''):
    """
    Инициализирует экземпляр класса `_html2text`.

    Args:
        out (Callable[[str], None], optional): Функция для вывода текста. По умолчанию `self.outtextf`.
        baseurl (str, optional): Базовый URL для ссылок. По умолчанию ''.
    """
```

### `feed`

```python
def feed(self, data):
    """
    Обрабатывает данные HTML, заменяя "</\' + \'script>" на "</ignore>".

    Args:
        data (str): HTML данные для обработки.
    """
```

### `outtextf`

```python
def outtextf(self, s):
    """
    Добавляет строку `s` в список `self.outtextlist` и обновляет флаг `self.lastWasNL`.

    Args:
        s (str): Строка для добавления.
    """
```

### `close`

```python
def close(self):
    """
    Завершает обработку HTML, объединяет накопленный текст и возвращает результат.

    Returns:
        str: Преобразованный текст в формате Markdown.
    """
```

### `handle_charref`

```python
def handle_charref(self, c):
    """
    Обрабатывает символьные ссылки (character references) в HTML.

    Args:
        c (str): Символьная ссылка для обработки.
    """
```

### `handle_entityref`

```python
def handle_entityref(self, c):
    """
    Обрабатывает ссылки на сущности (entity references) в HTML.

    Args:
        c (str): Ссылка на сущность для обработки.
    """
```

### `handle_starttag`

```python
def handle_starttag(self, tag, attrs):
    """
    Обрабатывает начальные теги HTML.

    Args:
        tag (str): Имя тега.
        attrs (list): Список атрибутов тега.
    """
```

### `handle_endtag`

```python
def handle_endtag(self, tag):
    """
    Обрабатывает конечные теги HTML.

    Args:
        tag (str): Имя тега.
    """
```

### `previousIndex`

```python
def previousIndex(self, attrs):
    """
    Возвращает индекс набора атрибутов (ссылки) в списке `self.a`.

    Args:
        attrs (dict): Атрибуты для поиска.

    Returns:
        int | None: Индекс, если набор атрибутов найден, иначе `None`.
    """
```

### `drop_last`

```python
def drop_last(self, nLetters):
    """
    Удаляет последние `nLetters` символов из `self.outtext`, если не включен тихий режим.

    Args:
        nLetters (int): Количество символов для удаления.
    """
```

### `handle_emphasis`

```python
def handle_emphasis(self, start, tag_style, parent_style):
    """
    Обрабатывает различные виды выделения текста.

    Args:
        start (bool): Флаг, указывающий на начало или конец выделения.
        tag_style (dict): Стили тега.
        parent_style (dict): Стили родительского тега.
    """
```

### `handle_tag`

```python
def handle_tag(self, tag, attrs, start):
    """
    Обрабатывает HTML-теги, определяет их тип и применяет соответствующее форматирование.

    Args:
        tag (str): Имя тега.
        attrs (dict | None): Атрибуты тега.
        start (bool): Флаг, указывающий на начало (1) или конец (0) тега.
    """
```

### `pbr`

```python
def pbr(self):
    """
    Устанавливает значение `self.p_p` равным 1, если оно равно 0.
    """
```

### `p`

```python
def p(self):
    """
    Устанавливает значение `self.p_p` равным 2.
    """
```

### `soft_br`

```python
def soft_br(self):
    """
    Вызывает `self.pbr()` и устанавливает `self.br_toggle` в "  ".
    """
```

### `o`

```python
def o(self, data, puredata=0, force=0):
    """
    Выводит данные с учетом текущего состояния форматирования.

    Args:
        data (str): Данные для вывода.
        puredata (int, optional): Флаг, указывающий на необходимость очистки данных от лишних пробелов. По умолчанию 0.
        force (int | str, optional): Флаг, указывающий на принудительный вывод данных. По умолчанию 0.
    """
```

### `handle_data`

```python
def handle_data(self, data):
    """
    Обрабатывает текстовые данные внутри HTML-тегов.

    Args:
        data (str): Текстовые данные для обработки.
    """
```

### `unknown_decl`

```python
def unknown_decl(self, data):
     """
    Обрабатывает неизвестные объявления в HTML (ничего не делает).

    Args:
        data (str): Неизвестные данные объявления.
    """
    pass
```

## Функции

### `name2cp`

```python
def name2cp(k):
    """
    Преобразует имя HTML-сущности в Unicode code point.

    Args:
        k (str): Имя HTML-сущности.

    Returns:
        int: Unicode code point.
    """
```

### `charref`

```python
def charref(name):
    """
    Преобразует символьную ссылку в символ Unicode.

    Args:
        name (str): Символьная ссылка.

    Returns:
        str: Символ Unicode.
    """
```

### `entityref`

```python
def entityref(c):
    """
    Преобразует ссылку на сущность в символ Unicode.

    Args:
        c (str): Ссылка на сущность.

    Returns:
        str: Символ Unicode.
    """
```

### `replaceEntities`

```python
def replaceEntities(s):
    """
    Заменяет HTML-сущности в строке на соответствующие символы Unicode.

    Args:
        s (re.Match): Объект Match, содержащий HTML-сущность.

    Returns:
        str: Символ Unicode.
    """
```

### `unescape`

```python
def unescape(s):
    """
    Заменяет HTML-сущности в строке на соответствующие символы Unicode.

    Args:
        s (str): Строка для замены сущностей.

    Returns:
        str: Строка с замененными сущностями.
    """
```

### `onlywhite`

```python
def onlywhite(line):
    """
    Проверяет, состоит ли строка только из пробельных символов.

    Args:
        line (str): Строка для проверки.

    Returns:
        bool: True, если строка состоит только из пробельных символов, иначе False.
    """
```

### `optwrap`

```python
def optwrap(text):
    """
    Переносит длинные абзацы в тексте.

    Args:
        text (str): Текст для переноса.

    Returns:
        str: Текст с перенесенными абзацами.
    """
```

### `hn`

```python
def hn(tag):
    """
    Определяет уровень заголовка HTML-тега.

    Args:
        tag (str): HTML-тег.

    Returns:
        int | None: Уровень заголовка (1-9) или None, если тег не является заголовком.
    """
```

### `dumb_property_dict`

```python
def dumb_property_dict(style):
    """
    Преобразует строку CSS-стилей в словарь атрибутов.

    Args:
        style (str): Строка CSS-стилей.

    Returns:
        dict: Словарь атрибутов CSS.
    """
```

### `dumb_css_parser`

```python
def dumb_css_parser(data):
    """
    Разбирает CSS-данные и возвращает словарь селекторов CSS, каждый из которых содержит словарь атрибутов CSS.

    Args:
        data (str): CSS данные для разбора.

    Returns:
        dict: Словарь селекторов CSS и их атрибутов.
    """
```

### `element_style`

```python
def element_style(attrs, style_def, parent_style):
    """
    Определяет итоговый стиль элемента на основе атрибутов, определений стилей и стиля родительского элемента.

    Args:
        attrs (dict): Атрибуты элемента.
        style_def (dict): Определения стилей CSS.
        parent_style (dict): Стили родительского элемента.

    Returns:
        dict: Итоговый стиль элемента.
    """
```

### `google_list_style`

```python
def google_list_style(style):
    """
    Определяет, является ли список упорядоченным или неупорядоченным, на основе CSS-стилей Google Docs.

    Args:
        style (dict): Стили элемента списка.

    Returns:
        str: "ul" для неупорядоченного списка, "ol" для упорядоченного списка.
    """
```

### `google_nest_count`

```python
def google_nest_count(style):
    """
    Вычисляет уровень вложенности списка Google Docs на основе CSS-стилей.

    Args:
        style (dict): Стили элемента списка.

    Returns:
        int: Уровень вложенности списка.
    """
```

### `google_has_height`

```python
def google_has_height(style):
    """
    Проверяет, определен ли атрибут "height" в CSS-стилях элемента Google Docs.

    Args:
        style (dict): Стили элемента.

    Returns:
        bool: True, если атрибут "height" определен, иначе False.
    """
```

### `google_text_emphasis`

```python
def google_text_emphasis(style):
    """
    Возвращает список всех модификаторов выделения текста элемента Google Docs.

    Args:
        style (dict): Стили элемента.

    Returns:
        list: Список модификаторов выделения текста.
    """
```

### `google_fixed_width_font`

```python
def google_fixed_width_font(style):
    """
    Проверяет, определяет ли CSS текущего элемента шрифт фиксированной ширины.

    Args:
        style (dict): Стили элемента.

    Returns:
        bool: True, если определен шрифт фиксированной ширины, иначе False.
    """
```

### `list_numbering_start`

```python
def list_numbering_start(attrs):
    """
    Извлекает начальное значение нумерации из атрибутов элемента списка.

    Args:
        attrs (dict): Атрибуты элемента списка.

    Returns:
        int: Начальное значение нумерации (на 1 меньше фактического значения).
    """
```

### `html2text_file`

```python
def html2text_file(html, out=wrapwrite, baseurl=''):
    """
    Преобразует HTML-файл в Markdown, используя указанную функцию вывода.

    Args:
        html (str): HTML-контент для преобразования.
        out (Callable[[str], None], optional): Функция для вывода текста. По умолчанию `wrapwrite`.
        baseurl (str, optional): Базовый URL для ссылок. По умолчанию ''.

    Returns:
        str: Преобразованный текст в формате Markdown.
    """
```

### `html2text`

```python
def html2text(html, baseurl=''):
    """
    Преобразует HTML-контент в Markdown с переносом строк.

    Args:
        html (str): HTML-контент для преобразования.
        baseurl (str, optional): Базовый URL для ссылок. По умолчанию ''.

    Returns:
        str: Преобразованный текст в формате Markdown с переносом строк.
    """
```

### `wrapwrite`

```python
def wrapwrite(text):
    """
    Записывает текст в стандартный вывод, кодируя его в UTF-8.

    Args:
        text (str): Текст для записи.
    """
```

## Параметры класса

- `UNICODE_SNOB (int)`: Флаг, определяющий использование символов Unicode вместо их ASCII-аналогов.
- `LINKS_EACH_PARAGRAPH (int)`: Флаг, определяющий размещение ссылок после каждого абзаца, а не в конце документа.
- `BODY_WIDTH (int)`: Ширина тела текста в символах. Используется для переноса строк.
- `SKIP_INTERNAL_LINKS (bool)`: Флаг, определяющий пропуск внутренних ссылок (якорей).
- `INLINE_LINKS (bool)`: Флаг, определяющий использование встроенных ссылок вместо ссылок по сноскам.
- `GOOGLE_LIST_INDENT (int)`: Количество пикселей, на которое Google Docs сдвигает вложенные списки.
- `IGNORE_ANCHORS (bool)`: Флаг, определяющий игнорирование якорей.
- `IGNORE_IMAGES (bool)`: Флаг, определяющий игнорирование изображений.

## Примеры

Пример использования функций `html2text` и `html2text_file`:

```python
html_content = "<h1>Заголовок</h1><p>Текст с <a href='http://example.com'>ссылкой</a>.</p>"
markdown_text = html2text(html_content)
print(markdown_text)
# => Заголовок
#
# Текст с [ссылкой](http://example.com).

# или с записью в файл

with open("output.md", "w", encoding="utf-8") as f:
    html2text_file(html_content, out=f.write)