# Модуль для рендеринга и разметки в Tiny Troupe
## Обзор

Модуль содержит набор функций и класс `RichTextStyle`, предназначенных для рендеринга текста, форматирования HTML и работы со стилями текста для использования в проекте Tiny Troupe. Он предоставляет инструменты для добавления префиксов к стилям, обрезки текста, форматирования даты и времени, удаления отступов и переноса текста.

## Подробнее

Модуль предоставляет функции для манипуляции со строками и текстом, включая добавление префиксов к стилям HTML, обрезку текста до заданной длины, форматирование дат и времени, удаление отступов и перенос текста. Также модуль содержит класс `RichTextStyle`, который определяет стили для различных типов событий и действий, используемых для визуализации в Tiny Troupe.

## Функции

### `inject_html_css_style_prefix`

**Назначение**: Добавляет префикс к атрибутам style в HTML-строке.

**Параметры**:
- `html` (str): HTML-строка, в которой нужно добавить префикс к стилям.
- `style_prefix_attributes` (str): Префикс, который нужно добавить к атрибутам style.

**Возвращает**:
- `str`: HTML-строка с добавленным префиксом к стилям.

**Пример**:
```python
html = '<div style="color: red;">Hello</div>'
style_prefix = 'font-size: 20px;'
result = inject_html_css_style_prefix(html, style_prefix)
print(result)  # Вывод: <div style="font-size: 20px;color: red;">Hello</div>
```

### `break_text_at_length`

**Назначение**: Обрезает текст или JSON до указанной длины, добавляя в конце строку "(...)".

**Параметры**:
- `text` (Union[str, dict]): Текст или словарь, который нужно обрезать.
- `max_length` (int, optional): Максимальная длина текста. Если `None`, текст не обрезается. По умолчанию `None`.

**Возвращает**:
- `str`: Обрезанный текст с добавленной строкой "(...)", если текст превышает `max_length`. В противном случае возвращает исходный текст.

**Как работает функция**:
- Если входной текст является словарем, он преобразуется в JSON-строку с отступами.
- Если `max_length` не указана или длина текста меньше или равна `max_length`, текст возвращается без изменений.
- Если длина текста превышает `max_length`, текст обрезается до `max_length`, и к нему добавляется строка "(...)".

**Примеры**:
```python
text = "This is a long text that needs to be truncated."
result = break_text_at_length(text, max_length=20)
print(result)  # Вывод: This is a long text (...)

data = {"key": "value", "another_key": "another_value"}
result = break_text_at_length(data, max_length=30)
print(result)
# Вывод: {
#     "key": "value",
#     "a (...)
```

### `pretty_datetime`

**Назначение**: Преобразует объект datetime в строку в формате "YYYY-MM-DD HH:MM".

**Параметры**:
- `dt` (datetime): Объект datetime для преобразования.

**Возвращает**:
- `str`: Строковое представление даты и времени в формате "YYYY-MM-DD HH:MM".

**Пример**:
```python
now = datetime.now()
result = pretty_datetime(now)
print(result)  # Вывод: 2023-10-26 15:30 (текущая дата и время)
```

### `dedent`

**Назначение**: Удаляет общие начальные пробелы из каждой строки текста.

**Параметры**:
- `text` (str): Текст, из которого нужно удалить отступы.

**Возвращает**:
- `str`: Текст без начальных отступов.

**Пример**:
```python
text = """
    This is a
    multiline text
    with indentation.
"""
result = dedent(text)
print(result)
# Вывод:
# This is a
# multiline text
# with indentation.
```

### `wrap_text`

**Назначение**: Переносит текст на строки указанной ширины.

**Параметры**:
- `text` (str): Текст для переноса.
- `width` (int, optional): Максимальная ширина строки. По умолчанию 100.

**Возвращает**:
- `str`: Текст, перенесенный на строки указанной ширины.

**Пример**:
```python
text = "This is a long text that needs to be wrapped to a specific width."
result = wrap_text(text, width=40)
print(result)
# Вывод:
# This is a long text that needs to be
# wrapped to a specific width.
```

## Классы

### `RichTextStyle`

**Описание**: Класс, содержащий стили текста для различных типов событий и действий.

**Атрибуты**:
- `STIMULUS_CONVERSATION_STYLE` (str): Стиль для реплик в разговоре.
- `STIMULUS_THOUGHT_STYLE` (str): Стиль для мыслей.
- `STIMULUS_DEFAULT_STYLE` (str): Стиль для обычных реплик.
- `ACTION_DONE_STYLE` (str): Стиль для завершенных действий.
- `ACTION_TALK_STYLE` (str): Стиль для речи.
- `ACTION_THINK_STYLE` (str): Стиль для размышлений.
- `ACTION_DEFAULT_STYLE` (str): Стиль для обычных действий.
- `INTERVENTION_DEFAULT_STYLE` (str): Стиль для интервенций.

**Методы**:
- `get_style_for(kind: str, event_type: str = None) -> str`: Возвращает стиль для указанного типа события и действия.

#### `get_style_for`

```python
@classmethod
def get_style_for(cls, kind: str, event_type: str = None) -> str
```

**Назначение**: Возвращает стиль для указанного типа события и действия.

**Параметры**:
- `kind` (str): Тип события ("stimulus", "action", "intervention").
- `event_type` (str, optional): Подтип события. По умолчанию `None`.

**Возвращает**:
- `str`: Стиль для указанного типа события и действия.

**Примеры**:
```python
style = RichTextStyle.get_style_for("stimulus", "CONVERSATION")
print(style)  # Вывод: bold italic cyan1

style = RichTextStyle.get_style_for("action", "DONE")
print(style)  # Вывод: grey82

style = RichTextStyle.get_style_for("intervention")
print(style)  # Вывод: bright_magenta
```