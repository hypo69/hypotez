# Модуль `rendering`

## Обзор

Модуль `rendering` предоставляет функции и классы для форматирования, рендеринга и стилизации текста и HTML-кода. Модуль использует библиотеку `rich` для стилизации текста, а также стандартные библиотеки Python для работы с датами, строками и JSON.

##  Подробней

Данный модуль предназначен для форматирования и рендеринга различных элементов пользовательского интерфейса, например,  для визуального представления действий и ответов системы. Он использует библиотеку `rich` для стилизации текста и стандартные библиотеки Python для работы с датами, строками и JSON. 

## Классы

### `RichTextStyle`

**Описание**: Класс `RichTextStyle` предоставляет набор констант для стилизации текста в соответствии с контекстом события.

**Атрибуты**:

- `STIMULUS_CONVERSATION_STYLE` (str): Стиль для текста, который представляет диалог. 
- `STIMULUS_THOUGHT_STYLE` (str): Стиль для текста, который представляет мысли. 
- `STIMULUS_DEFAULT_STYLE` (str): Стиль для текста, который представляет стимул. 
- `ACTION_DONE_STYLE` (str): Стиль для текста, который представляет выполненное действие. 
- `ACTION_TALK_STYLE` (str): Стиль для текста, который представляет действие общения. 
- `ACTION_THINK_STYLE` (str): Стиль для текста, который представляет действие размышления. 
- `ACTION_DEFAULT_STYLE` (str): Стиль для текста, который представляет действие.
- `INTERVENTION_DEFAULT_STYLE` (str): Стиль для текста, который представляет вмешательство.

**Методы**:

- `get_style_for(kind:str, event_type:str=None)`: Возвращает стиль для текста в соответствии с типом события.

**Как работает класс**:

Класс `RichTextStyle` хранит набор предустановленных стилей для форматирования текста. Он предоставляет удобный способ получить стиль для текста, основываясь на типе события, например, диалог, мысли, действие или вмешательство.

**Примеры**:

```python
from tinytroupe.utils.rendering import RichTextStyle

# Получение стиля для диалога
style = RichTextStyle.get_style_for("stimulus", "CONVERSATION")
print(f"Стиль для диалога: {style}")

# Получение стиля для мысли
style = RichTextStyle.get_style_for("stimulus", "THOUGHT")
print(f"Стиль для мысли: {style}")
```

## Функции

### `inject_html_css_style_prefix`

**Назначение**: Добавляет префикс к стилям CSS в HTML-коде.

**Параметры**:

- `html` (str): Строка HTML-кода.
- `style_prefix_attributes` (str): Префикс для CSS-стилей.

**Возвращает**:

- `str`: Строка HTML-кода с добавленным префиксом к стилям CSS.

**Как работает функция**:

Функция `inject_html_css_style_prefix` заменяет атрибут `style` в HTML-коде, добавляя к нему заданный префикс. Префикс добавляется к каждому атрибуту `style` в HTML-коде, что позволяет изменить стили всех элементов.

**Примеры**:

```python
from tinytroupe.utils.rendering import inject_html_css_style_prefix

html = '<div style="color: red;">Hello</div>'
style_prefix = 'font-size: 20px;'

new_html = inject_html_css_style_prefix(html, style_prefix)
print(f"Новый HTML-код: {new_html}")
```

### `break_text_at_length`

**Назначение**: Разбивает текст или JSON-данные на строки определенной длины, вставляя "(...)" в точку разрыва.

**Параметры**:

- `text` (Union[str, dict]): Строка или словарь с JSON-данными.
- `max_length` (int): Максимальная длина строки.

**Возвращает**:

- `str`: Строка с добавленным разрывом и "(...)" в точке разрыва.

**Как работает функция**:

Функция `break_text_at_length` проверяет, превышает ли длина текста заданное значение `max_length`. Если да, то текст разбивается на строки, добавляется "(...)" в точку разрыва, и возвращается строка с добавленным разрывом.

**Примеры**:

```python
from tinytroupe.utils.rendering import break_text_at_length

text = "This is a very long text that needs to be broken at a certain length."
max_length = 20

new_text = break_text_at_length(text, max_length)
print(f"Новый текст: {new_text}")

# JSON-данные
data = {"name": "John", "age": 30, "address": "123 Main Street"}
new_data = break_text_at_length(data, max_length)
print(f"Новый текст: {new_data}")
```

### `pretty_datetime`

**Назначение**: Преобразует объект `datetime` в строку с форматом `YYYY-MM-DD HH:MM`.

**Параметры**:

- `dt` (datetime): Объект `datetime`.

**Возвращает**:

- `str`: Строка с форматом `YYYY-MM-DD HH:MM`.

**Как работает функция**:

Функция `pretty_datetime` использует метод `strftime` для форматирования объекта `datetime` в строку с заданным форматом `YYYY-MM-DD HH:MM`.

**Примеры**:

```python
from tinytroupe.utils.rendering import pretty_datetime
from datetime import datetime

dt = datetime.now()
pretty_dt = pretty_datetime(dt)
print(f"Форматированная дата и время: {pretty_dt}")
```

### `dedent`

**Назначение**: Удаляет отступы в строке.

**Параметры**:

- `text` (str): Строка с отступами.

**Возвращает**:

- `str`: Строка без отступов.

**Как работает функция**:

Функция `dedent` использует метод `dedent` из модуля `textwrap` для удаления отступов в строке.

**Примеры**:

```python
from tinytroupe.utils.rendering import dedent

text = """
    This is a text with indentation.
    It needs to be dedented.
"""

new_text = dedent(text)
print(f"Текст без отступов: {new_text}")
```

### `wrap_text`

**Назначение**: Разбивает строку на строки заданной длины.

**Параметры**:

- `text` (str): Строка, которую нужно разбить.
- `width` (int): Максимальная длина строки.

**Возвращает**:

- `str`: Строка, разбитая на строки заданной длины.

**Как работает функция**:

Функция `wrap_text` использует метод `fill` из модуля `textwrap` для разбивки строки на строки заданной длины.

**Примеры**:

```python
from tinytroupe.utils.rendering import wrap_text

text = "This is a very long text that needs to be wrapped at a certain width."
width = 20

new_text = wrap_text(text, width)
print(f"Текст, разбитый на строки: {new_text}")
```

##  Внутренние функции

**Пример**:

```python
def internal_function():
    """
    Внутренняя функция.

    **Назначение**: 
        Описание назначения внутренней функции.

    **Как работает**:
        - Делает что-то.
        - Делает что-то еще.
        - Возвращает результат.
    """
    # Тело внутренней функции
```

## Примеры

**Пример 1**: 

```python
from tinytroupe.utils.rendering import RichTextStyle, inject_html_css_style_prefix, break_text_at_length, pretty_datetime, dedent, wrap_text

# Стиль для диалога
style = RichTextStyle.get_style_for("stimulus", "CONVERSATION")
print(f"Стиль для диалога: {style}")

# Добавление префикса к CSS-стилям в HTML-коде
html = '<div style="color: red;">Hello</div>'
style_prefix = 'font-size: 20px;'
new_html = inject_html_css_style_prefix(html, style_prefix)
print(f"Новый HTML-код: {new_html}")

# Разбивка текста
text = "This is a very long text that needs to be broken at a certain length."
max_length = 20
new_text = break_text_at_length(text, max_length)
print(f"Новый текст: {new_text}")

# Форматирование даты
dt = datetime.now()
pretty_dt = pretty_datetime(dt)
print(f"Форматированная дата и время: {pretty_dt}")

# Удаление отступов
text = """
    This is a text with indentation.
    It needs to be dedented.
"""
new_text = dedent(text)
print(f"Текст без отступов: {new_text}")

# Разбивка текста на строки
text = "This is a very long text that needs to be wrapped at a certain width."
width = 20
new_text = wrap_text(text, width)
print(f"Текст, разбитый на строки: {new_text}")