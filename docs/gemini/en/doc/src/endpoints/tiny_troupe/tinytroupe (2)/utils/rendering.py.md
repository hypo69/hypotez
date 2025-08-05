# Rendering and Markup Utilities

## Overview

This module provides a set of utility functions for rendering and markup manipulation within the `hypotez` project. It includes functions for:

- Injecting CSS style prefixes into HTML strings
- Breaking text (or JSON) at a specified length
- Formatting datetime objects into pretty strings
- Dedenting text
- Wrapping text at a specified width
- Defining styles for different event types using the `RichTextStyle` class

## Details

This module plays a crucial role in the `hypotez` project by handling the presentation and formatting of various types of text and data. The functions within this module ensure that:

- HTML elements are styled consistently across the project by injecting custom style prefixes.
- Text output is appropriately formatted and limited in length to avoid exceeding display boundaries.
- Datetime objects are displayed in a user-friendly and readable format.
- Text is correctly indented and formatted for improved readability.
- Text can be wrapped at specific widths to maintain consistent layout.
- The `RichTextStyle` class provides pre-defined styles for different event types, ensuring consistent styling across different parts of the project.

## Classes

### `RichTextStyle`

**Description**: Класс для определения стилей для разных типов событий.

**Attributes**:
- `STIMULUS_CONVERSATION_STYLE (str)`: Стиль для стимула типа "разговор".
- `STIMULUS_THOUGHT_STYLE (str)`: Стиль для стимула типа "мысль".
- `STIMULUS_DEFAULT_STYLE (str)`: Стиль по умолчанию для стимулов.
- `ACTION_DONE_STYLE (str)`: Стиль для завершенного действия.
- `ACTION_TALK_STYLE (str)`: Стиль для действия типа "говорить".
- `ACTION_THINK_STYLE (str)`: Стиль для действия типа "думать".
- `ACTION_DEFAULT_STYLE (str)`: Стиль по умолчанию для действий.
- `INTERVENTION_DEFAULT_STYLE (str)`: Стиль по умолчанию для вмешательств.

**Methods**:
- `get_style_for(kind:str, event_type:str=None)`: Метод для получения стиля для указанного типа события.

**Principle of Operation**:
- Класс предоставляет набор статических атрибутов, которые определяют стили для разных типов событий.
- Метод `get_style_for` позволяет получить стиль для указанного типа события.
- Стиль определяется на основе типа события (стимул, действие, вмешательство) и типа события (например, "разговор", "мысль", "DONE", "TALK").

**Examples**:

```python
>>> RichTextStyle.STIMULUS_CONVERSATION_STYLE
"bold italic cyan1"
>>> RichTextStyle.get_style_for("stimulus", "CONVERSATION")
"bold italic cyan1"
```

## Functions

### `inject_html_css_style_prefix(html, style_prefix_attributes)`

**Purpose**: Вставляет префикс стиля ко всем атрибутам стиля в заданной HTML-строке.

**Parameters**:
- `html (str)`: HTML-строка, в которую нужно вставить префикс стиля.
- `style_prefix_attributes (str)`: Префикс стиля, который нужно добавить к атрибутам стиля.

**How the Function Works**:
- Функция заменяет все вхождения `style="` в HTML-строке на `style="{style_prefix_attributes};`.

**Examples**:

```python
>>> inject_html_css_style_prefix('<div style="color: red;">Hello</div>', 'font-size: 20px;')
'<div style="font-size: 20px;color: red;">Hello</div>'
```

### `break_text_at_length(text: Union[str, dict], max_length: int=None) -> str`

**Purpose**: Разбивает текст (или JSON) на указанную длину, вставляя строку "(...)" в точку разрыва.

**Parameters**:
- `text (Union[str, dict])`: Текст или JSON-объект, который нужно разбить.
- `max_length (int, optional)`: Максимальная длина текста. Если `None`, текст возвращается без изменений.

**Returns**:
- `str`: Разбитый текст.

**How the Function Works**:
- Если текст представляет собой словарь, он преобразуется в JSON-строку.
- Если длина текста меньше или равна максимальной длине, текст возвращается без изменений.
- Если длина текста превышает максимальную длину, функция возвращает текст, усеченный до максимальной длины, с добавлением "(...)".

**Examples**:

```python
>>> break_text_at_length("This is a long text.", max_length=10)
"This is a (...)"
>>> break_text_at_length({"key1": "value1", "key2": "value2"}, max_length=20)
'{\n    "key1": "value1",\n    "key2": "value2"\n}'
```

### `pretty_datetime(dt: datetime) -> str`

**Purpose**: Возвращает строковое представление указанного объекта datetime в удобочитаемом формате.

**Parameters**:
- `dt (datetime)`: Объект datetime, который нужно преобразовать в строку.

**Returns**:
- `str`: Строковое представление объекта datetime в формате "YYYY-MM-DD HH:MM".

**Examples**:

```python
>>> from datetime import datetime
>>> dt = datetime(2023, 10, 26, 12, 30)
>>> pretty_datetime(dt)
"2023-10-26 12:30"
```

### `dedent(text: str) -> str`

**Purpose**: Удаляет отступы из указанного текста, удаляя все ведущие пробелы и отступы.

**Parameters**:
- `text (str)`: Текст, из которого нужно удалить отступы.

**Returns**:
- `str`: Текст без отступов.

**Examples**:

```python
>>> dedent("    This is a text with indentations.\n    Another line with indentations.")
"This is a text with indentations.\nAnother line with indentations."
```

### `wrap_text(text: str, width: int=100) -> str`

**Purpose**: Переносит текст на заданную ширину.

**Parameters**:
- `text (str)`: Текст, который нужно переносить.
- `width (int, optional)`: Ширина переноса. По умолчанию `100`.

**Returns**:
- `str`: Текст, перенесенный на заданную ширину.

**Examples**:

```python
>>> wrap_text("This is a long text that needs to be wrapped.", width=20)
'This is a long text that\nneeds to be wrapped.'
```

## Parameter Details

- `html (str)`: Строка с HTML-кодом.
- `style_prefix_attributes (str)`: Префикс, который будет добавлен к каждому атрибуту стиля в HTML.
- `text (Union[str, dict])`: Строка с текстом или словарь с данными, которые необходимо преобразовать в JSON-строку.
- `max_length (int, optional)`: Максимальное количество символов в тексте. По умолчанию `None`.
- `dt (datetime)`: Объект `datetime`, который нужно преобразовать в строку.
- `text (str)`: Строка с текстом, из которой нужно удалить отступы.
- `width (int, optional)`: Ширина строки для переноса текста. По умолчанию `100`.

## Examples

### Usage Examples

```python
>>> from tinytroupe.utils.rendering import inject_html_css_style_prefix, break_text_at_length, pretty_datetime
>>> html = '<div style="color: red;">Hello</div>'
>>> injected_html = inject_html_css_style_prefix(html, 'font-size: 20px;')
>>> print(injected_html)
'<div style="font-size: 20px;color: red;">Hello</div>'

>>> text = "This is a long text that needs to be broken."
>>> broken_text = break_text_at_length(text, max_length=15)
>>> print(broken_text)
"This is a long (...)"

>>> from datetime import datetime
>>> dt = datetime(2023, 10, 26, 12, 30)
>>> pretty_dt = pretty_datetime(dt)
>>> print(pretty_dt)
"2023-10-26 12:30"
```