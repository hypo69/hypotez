# Модуль для конвертации HTML в Markdown

## Обзор

Модуль `html2text` предназначен для преобразования HTML-документов в Markdown-форматированный текст. Он включает классы и функции для разбора HTML, обработки различных элементов и стилей, а также для создания Markdown-эквивалента исходного HTML-контента. Модуль поддерживает различные опции, такие как обработка HTML, экспортированного из Google Docs, использование символов Unicode, настройка ширины текста и т.д.

## Подробнее

Модуль предоставляет класс `_html2text`, который наследуется от `HTMLParser.HTMLParser` и выполняет основную работу по преобразованию HTML в текст. Он обрабатывает различные теги, атрибуты и стили, преобразуя их в соответствующую Markdown-разметку. Модуль также содержит функции для обработки HTML-сущностей, обертки текста и разбора CSS-стилей.

## Функции

### `has_key(x, y)`

**Назначение**: Проверяет, содержит ли словарь `x` ключ `y`.

**Параметры**:
- `x` (dict): Проверяемый словарь.
- `y` (str): Ключ для проверки.

**Возвращает**:
- `bool`: `True`, если словарь содержит ключ, иначе `False`.

**Как работает функция**:
Функция `has_key` проверяет наличие ключа `y` в словаре `x`. Сначала она проверяет, имеет ли объект `x` метод `has_key`. Если да, то использует его для проверки наличия ключа. Если нет, то использует оператор `in` для проверки наличия ключа в словаре.

**Примеры**:
```python
has_key({'a': 1, 'b': 2}, 'a')  # Вернет True
has_key({'a': 1, 'b': 2}, 'c')  # Вернет False
```

### `name2cp(k)`

**Назначение**: Преобразует имя HTML-сущности в кодовую точку Unicode.

**Параметры**:
- `k` (str): Имя HTML-сущности.

**Возвращает**:
- `int`: Кодовая точка Unicode для данной сущности.

**Как работает функция**:
Функция `name2cp` преобразует имя HTML-сущности в соответствующую кодовую точку Unicode. Если сущность `apos`, возвращает код символа апострофа. Если модуль `htmlentitydefs` имеет атрибут `name2codepoint`, использует его для преобразования. В противном случае пытается получить значение из `entitydefs` и преобразовать его в целое число, если это возможно.

**Примеры**:
```python
name2cp('copy')  # Вернет код символа копирайта
```

### `charref(name)`

**Назначение**: Преобразует символьную ссылку HTML (например, `&#123;`) в символ Unicode.

**Параметры**:
- `name` (str): Символьная ссылка HTML без префикса `&#` и суффикса `;`.

**Возвращает**:
- `str`: Соответствующий символ Unicode.

**Как работает функция**:
Функция `charref` преобразует символьную ссылку HTML в символ Unicode. Если ссылка начинается с `x` или `X`, она интерпретируется как шестнадцатеричное число. В противном случае она интерпретируется как десятичное число. Если символ присутствует в словаре `unifiable_n`, возвращается соответствующее значение. В противном случае символ преобразуется в Unicode с использованием функции `chr`.

**Примеры**:
```python
charref('65')   # Вернет 'A'
charref('x41')  # Вернет 'A'
```

### `entityref(c)`

**Назначение**: Преобразует ссылку на HTML-сущность (например, `&copy;`) в символ Unicode.

**Параметры**:
- `c` (str): Имя HTML-сущности.

**Возвращает**:
- `str`: Соответствующий символ Unicode.

**Как работает функция**:
Функция `entityref` преобразует ссылку на HTML-сущность в символ Unicode. Если сущность присутствует в словаре `unifiable`, возвращается соответствующее значение. В противном случае функция пытается преобразовать сущность с использованием `name2cp` и `chr`. Если преобразование не удается, возвращается исходная ссылка на сущность.

**Примеры**:
```python
entityref('copy')  # Вернет '(C)'
```

### `replaceEntities(s)`

**Назначение**: Заменяет HTML-сущности в строке на соответствующие символы Unicode.

**Параметры**:
- `s` (re.Match): Объект соответствия регулярного выражения, содержащий HTML-сущность.

**Возвращает**:
- `str`: Символ Unicode, соответствующий HTML-сущности.

**Как работает функция**:
Функция `replaceEntities` извлекает HTML-сущность из объекта соответствия регулярного выражения и заменяет ее соответствующим символом Unicode. Если сущность является символьной ссылкой (начинается с `#`), она преобразуется с использованием `charref`. В противном случае она преобразуется с использованием `entityref`.

**Примеры**:
```python
match = re.search(r"&(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));", '&copy;')
replaceEntities(match)  # Вернет '(C)'
```

### `unescape(s)`

**Назначение**: Заменяет все HTML-сущности в строке на соответствующие символы Unicode.

**Параметры**:
- `s` (str): Строка, содержащая HTML-сущности.

**Возвращает**:
- `str`: Строка, в которой все HTML-сущности заменены на соответствующие символы Unicode.

**Как работает функция**:
Функция `unescape` использует регулярное выражение `r_unescape` для поиска всех HTML-сущностей в строке `s` и заменяет их соответствующими символами Unicode с помощью функции `replaceEntities`.

**Примеры**:
```python
unescape('&copy; &amp;')  # Вернет '(C) &'
```

### `onlywhite(line)`

**Назначение**: Проверяет, состоит ли строка только из пробельных символов.

**Параметры**:
- `line` (str): Проверяемая строка.

**Возвращает**:
- `bool`: `True`, если строка состоит только из пробельных символов, иначе `False`.

**Как работает функция**:
Функция `onlywhite` проверяет, состоит ли строка только из пробельных символов. Она проходит по каждому символу в строке и проверяет, является ли он пробелом. Если найден не пробельный символ, функция возвращает `False`. В противном случае функция возвращает `True`.

**Примеры**:
```python
onlywhite('   ')  # Вернет True
onlywhite('  a ')  # Вернет False
```

### `optwrap(text)`

**Назначение**: Переносит текст по заданной ширине.

**Параметры**:
- `text` (str): Исходный текст.

**Возвращает**:
- `str`: Текст, перенесенный по заданной ширине.

**Как работает функция**:
Функция `optwrap` переносит длинные строки в тексте на заданную ширину `BODY_WIDTH`. Она разделяет текст на параграфы и переносит каждый параграф, если его длина превышает заданную ширину.

**Примеры**:
```python
BODY_WIDTH = 20
text = 'This is a long line of text that needs to be wrapped.'
optwrap(text)  # Вернет текст, перенесенный по ширине 20 символов
```

### `hn(tag)`

**Назначение**: Определяет уровень заголовка HTML-тега.

**Параметры**:
- `tag` (str): HTML-тег.

**Возвращает**:
- `int`: Уровень заголовка (1-9), или `None`, если тег не является заголовком.

**Как работает функция**:
Функция `hn` проверяет, является ли переданный тег HTML-заголовком (h1-h9). Если тег является заголовком, функция возвращает уровень заголовка в виде целого числа. В противном случае функция возвращает `None`.

**Примеры**:
```python
hn('h1')  # Вернет 1
hn('h6')  # Вернет 6
hn('p')   # Вернет None
```

### `dumb_property_dict(style)`

**Назначение**: Преобразует строку CSS-стилей в словарь атрибутов.

**Параметры**:
- `style` (str): Строка CSS-стилей.

**Возвращает**:
- `dict`: Словарь атрибутов CSS.

**Как работает функция**:
Функция `dumb_property_dict` преобразует строку CSS-стилей в словарь, где ключами являются имена атрибутов, а значениями - их значения. Она разделяет строку на пары атрибут-значение и создает словарь на основе этих пар.

**Примеры**:
```python
style = 'color: red; font-size: 12px;'
dumb_property_dict(style)  # Вернет {'color': 'red', 'font-size': '12px'}
```

### `dumb_css_parser(data)`

**Назначение**: Преобразует CSS-данные в словарь селекторов и атрибутов.

**Параметры**:
- `data` (str): CSS-данные.

**Возвращает**:
- `dict`: Словарь CSS-селекторов и их атрибутов.

**Как работает функция**:
Функция `dumb_css_parser` преобразует CSS-данные в словарь, где ключами являются CSS-селекторы, а значениями - словари атрибутов и их значений. Она удаляет `@import` предложения и разделяет данные на селекторы и атрибуты.

**Примеры**:
```python
css_data = 'body { color: black; } p { font-size: 14px; }'
dumb_css_parser(css_data)  # Вернет словарь с селекторами 'body' и 'p' и их атрибутами
```

### `element_style(attrs, style_def, parent_style)`

**Назначение**: Определяет окончательный стиль элемента на основе атрибутов, CSS-определений и стиля родительского элемента.

**Параметры**:
- `attrs` (dict): Атрибуты HTML-элемента.
- `style_def` (dict): Определения CSS-стилей.
- `parent_style` (dict): Стиль родительского элемента.

**Возвращает**:
- `dict`: Окончательный стиль элемента.

**Как работает функция**:
Функция `element_style` определяет окончательный стиль HTML-элемента на основе его атрибутов, CSS-определений и стиля родительского элемента. Она начинает со копирования стиля родительского элемента, затем обновляет его стилями из CSS-классов, указанных в атрибуте `class`, и, наконец, обновляет его стилями, указанными в атрибуте `style`.

**Примеры**:
```python
attrs = {'class': 'highlight', 'style': 'font-weight: bold;'}
style_def = {'.highlight': {'color': 'red'}}
parent_style = {'font-size': '12px'}
element_style(attrs, style_def, parent_style)  # Вернет объединенный стиль
```

### `google_list_style(style)`

**Назначение**: Определяет, является ли список упорядоченным или неупорядоченным.

**Параметры**:
- `style` (dict): Словарь CSS-стилей.

**Возвращает**:
- `str`: `'ul'`, если список неупорядоченный, `'ol'` в противном случае.

**Как работает функция**:
Функция `google_list_style` определяет, является ли список упорядоченным или неупорядоченным, на основе значения атрибута `list-style-type` в CSS-стиле. Если значение атрибута равно `'disc'`, `'circle'`, `'square'` или `'none'`, функция возвращает `'ul'`. В противном случае функция возвращает `'ol'`.

**Примеры**:
```python
style = {'list-style-type': 'disc'}
google_list_style(style)  # Вернет 'ul'
```

### `google_nest_count(style)`

**Назначение**: Вычисляет уровень вложенности списка Google Docs.

**Параметры**:
- `style` (dict): Словарь CSS-стилей.

**Возвращает**:
- `int`: Уровень вложенности списка.

**Как работает функция**:
Функция `google_nest_count` вычисляет уровень вложенности списка Google Docs на основе значения атрибута `margin-left` в CSS-стиле. Она делит значение атрибута на `GOOGLE_LIST_INDENT` и возвращает результат в виде целого числа.

**Примеры**:
```python
style = {'margin-left': '72pt'}
google_nest_count(style)  # Вернет 2
```

### `google_has_height(style)`

**Назначение**: Проверяет, определен ли атрибут `height` в стиле элемента.

**Параметры**:
- `style` (dict): Словарь CSS-стилей.

**Возвращает**:
- `bool`: `True`, если атрибут `height` определен, иначе `False`.

**Как работает функция**:
Функция `google_has_height` проверяет, определен ли атрибут `height` в CSS-стиле элемента. Если атрибут определен, функция возвращает `True`. В противном случае функция возвращает `False`.

**Примеры**:
```python
style = {'height': '10px'}
google_has_height(style)  # Вернет True
```

### `google_text_emphasis(style)`

**Назначение**: Возвращает список всех модификаторов выделения текста элемента.

**Параметры**:
- `style` (dict): Словарь CSS-стилей.

**Возвращает**:
- `list`: Список модификаторов выделения текста.

**Как работает функция**:
Функция `google_text_emphasis` возвращает список всех модификаторов выделения текста элемента на основе значений атрибутов `text-decoration`, `font-style` и `font-weight` в CSS-стиле.

**Примеры**:
```python
style = {'text-decoration': 'underline', 'font-style': 'italic'}
google_text_emphasis(style)  # Вернет ['underline', 'italic']
```

### `google_fixed_width_font(style)`

**Назначение**: Проверяет, использует ли элемент шрифт фиксированной ширины.

**Параметры**:
- `style` (dict): Словарь CSS-стилей.

**Возвращает**:
- `bool`: `True`, если элемент использует шрифт фиксированной ширины, иначе `False`.

**Как работает функция**:
Функция `google_fixed_width_font` проверяет, использует ли элемент шрифт фиксированной ширины на основе значения атрибута `font-family` в CSS-стиле. Если значение атрибута равно `'Courier New'` или `'Consolas'`, функция возвращает `True`. В противном случае функция возвращает `False`.

**Примеры**:
```python
style = {'font-family': 'Courier New'}
google_fixed_width_font(style)  # Вернет True
```

### `list_numbering_start(attrs)`

**Назначение**: Извлекает начальное значение нумерации из атрибутов списка.

**Параметры**:
- `attrs` (dict): Атрибуты HTML-элемента.

**Возвращает**:
- `int`: Начальное значение нумерации списка.

**Как работает функция**:
Функция `list_numbering_start` извлекает начальное значение нумерации из атрибутов HTML-элемента списка. Если атрибут `start` присутствует, функция возвращает его значение в виде целого числа, уменьшенного на 1. В противном случае функция возвращает 0.

**Примеры**:
```python
attrs = {'start': '5'}
list_numbering_start(attrs)  # Вернет 4
```

### `class _html2text(HTMLParser.HTMLParser)`

**Описание**: Класс для преобразования HTML в Markdown-форматированный текст.

**Наследует**:
- `HTMLParser.HTMLParser`: Этот класс наследует функциональность стандартного парсера HTML для разбора структуры HTML-документа.

**Атрибуты**:
- `out` (function): Функция для вывода текста.
- `outtextlist` (list): Список для хранения выводимых символов.
- `outtext` (str): Строка, содержащая преобразованный текст.
- `quiet` (int): Уровень "тишины" (игнорирования) определенных тегов.
- `p_p` (int): Количество символов новой строки для вывода перед следующим выводом.
- `outcount` (int): Счетчик выведенных символов.
- `start` (int): Флаг, указывающий на начало документа.
- `space` (int): Флаг, указывающий на необходимость добавления пробела.
- `a` (list): Список ссылок.
- `astack` (list): Стек атрибутов ссылок.
- `acount` (int): Счетчик ссылок.
- `list` (list): Список списков.
- `blockquote` (int): Уровень цитирования.
- `pre` (int): Флаг, указывающий на наличие тега `<pre>`.
- `startpre` (int): Флаг, указывающий на начало тега `<pre>`.
- `code` (bool): Флаг, указывающий на наличие тега `<code>`.
- `br_toggle` (str): Строка для переключения тега `<br>`.
- `lastWasNL` (bool): Флаг, указывающий на то, что последний символ был новой строкой.
- `lastWasList` (bool): Флаг, указывающий на то, что последним тегом был список.
- `style` (int): Флаг, указывающий на наличие тега `<style>`.
- `style_def` (dict): Определения CSS-стилей.
- `tag_stack` (list): Стек тегов.
- `emphasis` (int): Уровень выделения текста.
- `drop_white_space` (int): Флаг для удаления пробелов.
- `inheader` (bool): Флаг, указывающий на нахождение внутри заголовка.
- `abbr_title` (str): Заголовок текущего определения аббревиатуры.
- `abbr_data` (str): Последний внутренний HTML для определения аббревиатуры.
- `abbr_list` (dict): Стек аббревиатур для последующей записи.
- `baseurl` (str): Базовый URL для ссылок.

**Методы**:
- `__init__(self, out=None, baseurl='')`: Инициализирует объект класса `_html2text`.
- `feed(self, data)`: Обрабатывает данные HTML.
- `outtextf(self, s)`: Добавляет текст в список вывода.
- `close(self)`: Завершает обработку HTML и возвращает преобразованный текст.
- `handle_charref(self, c)`: Обрабатывает символьные ссылки.
- `handle_entityref(self, c)`: Обрабатывает ссылки на сущности.
- `handle_starttag(self, tag, attrs)`: Обрабатывает начальные теги.
- `handle_endtag(self, tag)`: Обрабатывает конечные теги.
- `previousIndex(self, attrs)`: Возвращает индекс заданного набора атрибутов ссылки в списке `self.a`.
- `drop_last(self, nLetters)`: Удаляет последние `nLetters` символов из вывода.
- `handle_emphasis(self, start, tag_style, parent_style)`: Обрабатывает различные выделения текста.
- `handle_tag(self, tag, attrs, start)`: Обрабатывает теги.
- `pbr(self)`: Добавляет символ новой строки.
- `p(self)`: Добавляет два символа новой строки.
- `soft_br(self)`: Добавляет мягкий перенос строки.
- `o(self, data, puredata=0, force=0)`: Выводит данные.
- `handle_data(self, data)`: Обрабатывает данные внутри тегов.
- `unknown_decl(self, data)`: Обрабатывает неизвестные объявления.

#### `__init__(self, out=None, baseurl='')`

**Назначение**: Инициализирует объект класса `_html2text`.

**Параметры**:
- `out` (function, optional): Функция для вывода текста. По умолчанию `self.outtextf`.
- `baseurl` (str, optional): Базовый URL для ссылок. По умолчанию пустая строка.

**Как работает функция**:
Функция `__init__` инициализирует объект класса `_html2text`. Она устанавливает функцию вывода, создает списки и флаги для хранения и обработки данных, а также устанавливает базовый URL для ссылок.

#### `feed(self, data)`

**Назначение**: Обрабатывает данные HTML.

**Параметры**:
- `data` (str): Данные HTML для обработки.

**Как работает функция**:
Функция `feed` заменяет определенные последовательности символов в данных HTML и передает их базовому классу `HTMLParser.HTMLParser` для дальнейшей обработки.

#### `outtextf(self, s)`

**Назначение**: Добавляет текст в список вывода.

**Параметры**:
- `s` (str): Текст для добавления.

**Как работает функция**:
Функция `outtextf` добавляет текст `s` в список `self.outtextlist`. Если текст не пустой, она устанавливает флаг `self.lastWasNL` в зависимости от того, заканчивается ли текст символом новой строки.

#### `close(self)`

**Назначение**: Завершает обработку HTML и возвращает преобразованный текст.

**Возвращает**:
- `str`: Преобразованный текст.

**Как работает функция**:
Функция `close` завершает обработку HTML. Она вызывает функцию `self.pbr` для добавления символов новой строки, вызывает функцию `self.o` с параметром `force='end'` для завершения вывода, объединяет все элементы списка `self.outtextlist` в одну строку и возвращает ее.

#### `handle_charref(self, c)`

**Назначение**: Обрабатывает символьные ссылки.

**Параметры**:
- `c` (str): Символьная ссылка для обработки.

**Как работает функция**:
Функция `handle_charref` вызывает функцию `charref` для преобразования символьной ссылки `c` в символ Unicode и выводит его с помощью функции `self.o`.

#### `handle_entityref(self, c)`

**Назначение**: Обрабатывает ссылки на сущности.

**Параметры**:
- `c` (str): Ссылка на сущность для обработки.

**Как работает функция**:
Функция `handle_entityref` вызывает функцию `entityref` для преобразования ссылки на сущность `c` в символ Unicode и выводит его с помощью функции `self.o`.

#### `handle_starttag(self, tag, attrs)`

**Назначение**: Обрабатывает начальные теги.

**Параметры**:
- `tag` (str): Имя тега.
- `attrs` (list): Список атрибутов тега.

**Как работает функция**:
Функция `handle_starttag` вызывает функцию `handle_tag` для обработки начального тега `tag` с атрибутами `attrs`.

#### `handle_endtag(self, tag)`

**Назначение**: Обрабатывает конечные теги.

**Параметры**:
- `tag` (str): Имя тега.

**Как работает функция**:
Функция `handle_endtag` вызывает функцию `handle_tag` для обработки конечного тега `tag`.

#### `previousIndex(self, attrs)`

**Назначение**: Возвращает индекс заданного набора атрибутов ссылки в списке `self.a`.

**Параметры**:
- `attrs` (dict): Атрибуты ссылки для поиска.

**Возвращает**:
- `int`: Индекс ссылки в списке `self.a`, если найдена, иначе `None`.

**Как работает функция**:
Функция `previousIndex` ищет ссылку с заданными атрибутами в списке `self.a`. Если ссылка найдена, функция возвращает ее индекс. В противном случае функция возвращает `None`.

#### `drop_last(self, nLetters)`

**Назначение**: Удаляет последние `nLetters` символов из вывода.

**Параметры**:
- `nLetters` (int): Количество символов для удаления.

**Как работает функция**:
Функция `drop_last` удаляет последние `nLetters` символов из строки `self.outtext`, если режим "тишины" не активен.

#### `handle_emphasis(self, start, tag_style, parent_style)`

**Назначение**: Обрабатывает различные выделения текста.

**Параметры**:
- `start` (bool): Флаг, указывающий на начало или конец выделения.
- `tag_style` (dict): Стиль текущего тега.
- `parent_style` (dict): Стиль родительского тега.

**Как работает функция**:
Функция `handle_emphasis` обрабатывает различные выделения текста, такие как полужирный, курсив, зачеркнутый и моноширинный текст. Она определяет, какие стили применяются к текущему тегу и выводит соответствующие символы Markdown для выделения текста.

#### `handle_tag(self, tag, attrs, start)`

**Назначение**: Обрабатывает теги.

**Параметры**:
- `tag` (str): Имя тега.
- `attrs` (dict): Атрибуты тега.
- `start` (bool): Флаг, указывающий на начало или конец тега.

**Как работает функция**:
Функция `handle_tag` обрабатывает различные теги HTML и выводит соответствующие символы Markdown. Она обрабатывает заголовки, параграфы, разрывы строк, горизонтальные линии, теги стиля и скриптов, цитаты, выделения текста, ссылки, изображения, списки и другие теги.

#### `pbr(self)`

**Назначение**: Добавляет символ новой строки.

**Как работает функция**:
Функция `pbr` добавляет символ новой строки, если `self.p_p` равно 0.

#### `p(self)`

**Назначение**: Добавляет два символа новой строки.

**Как работает функция**:
Функция `p` добавляет два символа новой строки, устанавливая `self.p_p` в 2.

#### `soft_br(self)`

**Назначение**: Добавляет мягкий перенос строки.

**Как работает функция**:
Функция `soft_br` добавляет мягкий перенос строки, вызывая функцию `self.pbr` и устанавливая `self.br_toggle` в `'  '`.

#### `o(self, data, puredata=0, force=0)`

**Назначение**: Выводит данные.

**Параметры**:
- `data` (str): Данные для вывода.
- `puredata` (int, optional): Флаг, указывающий на то, что данные не содержат HTML-тегов. По умолчанию 0.
- `force` (int, optional): Флаг, указывающий на принудительный вывод данных. По умолчанию 0.

**Как работает функция**:
Функция `o` выводит данные, добавляя соответствующие префиксы и суффиксы в зависимости от контекста. Она обрабатывает цитаты, теги `<pre>`, пробелы, ссылки и аббревиатуры.

#### `handle_data(self, data)`

**Назначение**: Обрабатывает данные внутри тегов.

**Параметры**:
- `data` (str): Данные для обработки.

**Как работает функция**:
Функция `handle_data` обрабатывает данные внутри тегов. Если данные содержат закрывающий тег `</script>`, она уменьшает уровень "тишины". Если активен тег `<style>`, она обновляет определения стилей. Затем функция выводит данные с помощью функции `self.o`.

#### `unknown_decl(self, data)`

**Назначение**: Обрабатывает неизвестные объявления.

**Параметры**:
- `data` (str): Данные объявления.

**Как работает функция**:
Функция `unknown_decl` ничего не делает. Она предназначена для обработки неизвестных объявлений, но в текущей реализации она просто пропускает их.

### `wrapwrite(text)`

**Назначение**: Записывает текст в стандартный поток вывода, кодируя его в UTF-8.

**Параметры**:
- `text` (str): Текст для записи.

**Как работает функция**:
Функция `wrapwrite` кодирует текст в UTF-8 и записывает его в стандартный поток вывода. Она обрабатывает исключение `AttributeError`, которое может возникнуть в Python 2.

**Примеры**:
```python
wrapwrite('Hello, world!')  # Выведет 'Hello, world!' в стандартный поток вывода
```

### `html2text_file(html, out=wrapwrite, baseurl='')`

**Назначение**: Преобразует HTML-код в текст, используя указанную функцию вывода.

**Параметры**:
- `html` (str): HTML-код для преобразования.
- `out` (function, optional): Функция для вывода текста. По умолчанию `wrapwrite`.
- `baseurl` (str, optional): Базовый URL для разрешения относительных ссылок. По умолчанию пустая строка.

**Возвращает**:
- `str`: Преобразованный текст.

**Как работает функция**:
Функция `html2text_file` создает экземпляр класса `_html2text`, передает ему HTML-код для обработки и возвращает преобразованный текст.

**Примеры**:
```python
html = '<html><body><h1>Hello, world!</h1></body></html>'
html2text_file(html)  # Вернет 'Hello, world!' в стандартный поток вывода
```

### `html2text(html, baseurl='')`

**Назначение**: Преобразует HTML-код в текст с переносом строк.

**Параметры**:
- `html` (str): HTML-код для преобразования.
- `baseurl` (str, optional): Базовый URL для разрешения относительных ссылок. По умолчанию пустая строка.

**Возвращает**:
- `str`: Преобразованный текст с переносом строк.

**Как работает функция**:
Функция `html2text` вызывает функцию `html2text_file` для преобразования HTML-кода в текст и затем переносит строки в тексте с помощью функции `optwrap`.

**Примеры**:
```python
html = '<html><body><h1>Hello, world!</h1></body></html>'
html2text(html)  # Вернет 'Hello, world!' с переносом строк
```

### `class Storage`

**Описание**: Пустой класс для хранения опций.

**Принцип работы**:
Класс `Storage` используется для хранения различных опций, которые могут быть переданы в модуль `html2text`.

### `options`

**Описание**: Экземпляр класса `Storage`, содержащий опции по умолчанию.

**Атрибуты**:
- `google_doc` (bool): Флаг, указывающий на то, что входной HTML-код является экспортированным документом Google Docs. По умолчанию `False`.
- `ul_item_mark` (str): Символ, используемый для обозначения элементов неупорядоченного списка. По умолчанию `'*'`.

## Запуск из командной строки

Модуль можно запустить из командной строки для преобразования HTML-файла или URL в текст.

**Использование**:
```
python html2text.py [(filename|url) [encoding]]
```

**Опции**:
- `-g, --google-doc`: Преобразовать HTML-код, экспортированный из Google Docs.
- `-d, --dash-unordered-list`: Использовать дефис вместо звездочки для элементов неупорядоченного списка.
- `-b, --body-width`: Количество символов в строке вывода (0 для отключения переноса).
- `-i, --google-list-indent`: Количество пикселей отступа для вложенных списков Google Docs.
- `-s, --hide-strikethrough`: Скрыть зачеркнутый текст (только для Google Docs).

**Примеры**:
```
python html2text.py example.html
python html2text.py http://example.com
python html2text.py example.html utf-8
```