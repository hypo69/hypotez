### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет набор утилит для обработки текста и стилизации, предназначенных для использования в проекте Tiny Troupe. Он включает функции для внедрения CSS, обрезки текста, форматирования даты и времени, удаления отступов, обертывания текста и управления стилями текста с использованием библиотеки Rich.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `json`, `textwrap`, `datetime` и `Union` из стандартной библиотеки Python, а также модуль `logger` из `tinytroupe.utils`.

2. **Использование `inject_html_css_style_prefix`**:
   - Функция `inject_html_css_style_prefix` вставляет префикс стиля во все атрибуты `style` в HTML-строке. Это полезно для добавления общих стилей ко всем элементам HTML.
   - Функция выполняет замену всех вхождений `style="` на `style="{style_prefix_attributes};"`, добавляя указанный префикс к существующим стилям.

3. **Использование `break_text_at_length`**:
   - Функция `break_text_at_length` обрезает текст или JSON до указанной максимальной длины, добавляя в конце строку `(...)`.
   - Если входные данные - словарь, они преобразуются в JSON-строку с отступами. Если `max_length` не указана или длина текста меньше `max_length`, текст возвращается без изменений.

4. **Использование `pretty_datetime`**:
   - Функция `pretty_datetime` форматирует объект `datetime` в строку в формате `YYYY-MM-DD HH:MM`.

5. **Использование `dedent`**:
   - Функция `dedent` удаляет все общие начальные пробелы из текста.

6. **Использование `wrap_text`**:
   - Функция `wrap_text` переносит текст на новую строку после указанной ширины.

7. **Использование класса `RichTextStyle`**:
   - Класс `RichTextStyle` определяет стили текста для различных типов событий (стимулы, действия, интервенции) с использованием предопределенных констант.
   - Метод `get_style_for` возвращает стиль для указанного типа события на основе его `kind` (стимул, действие, интервенция) и `event_type`.

Пример использования
-------------------------

```python
import json
import textwrap
from datetime import datetime
from typing import Union

# Предполагается, что logger уже настроен
# from tinytroupe.utils import logger

################################################################################
# Rendering and markup
################################################################################
def inject_html_css_style_prefix(html, style_prefix_attributes):
    """
    Вставляет префикс стиля во все атрибуты style в данной HTML-строке.

    Например, если вы хотите добавить префикс стиля ко всем атрибутам style в HTML-строке
    ``<div style="color: red;">Hello</div>``, вы можете использовать эту функцию следующим образом:
    inject_html_css_style_prefix('<div style="color: red;">Hello</div>', 'font-size: 20px;')
    """
    return html.replace('style="', f'style="{style_prefix_attributes};')

def break_text_at_length(text: Union[str, dict], max_length: int=None) -> str:
    """
    Обрезает текст (или JSON) до указанной длины, вставляя строку "(...)" в точке обрыва.
    Если максимальная длина равна None, контент возвращается как есть.
    """
    if isinstance(text, dict):
        text = json.dumps(text, indent=4)

    if max_length is None or len(text) <= max_length:
        return text
    else:
        return text[:max_length] + " (...)"

def pretty_datetime(dt: datetime) -> str:
    """
    Возвращает красивое строковое представление указанного объекта datetime.
    """
    return dt.strftime("%Y-%m-%d %H:%M")

def dedent(text: str) -> str:
    """
    Удаляет отступы из указанного текста, удаляя любые начальные пробелы и отступы.
    """
    return textwrap.dedent(text).strip()

def wrap_text(text: str, width: int=100) -> str:
    """
    Переносит текст на новую строку после указанной ширины.
    """
    return textwrap.fill(text, width=width)

class RichTextStyle:

    # Consult color options here: https://rich.readthedocs.io/en/stable/appendix/colors.html

    STIMULUS_CONVERSATION_STYLE = "bold italic cyan1"
    STIMULUS_THOUGHT_STYLE = "dim italic cyan1"
    STIMULUS_DEFAULT_STYLE = "italic"

    ACTION_DONE_STYLE = "grey82"
    ACTION_TALK_STYLE = "bold green3"
    ACTION_THINK_STYLE = "green"
    ACTION_DEFAULT_STYLE = "purple"

    INTERVENTION_DEFAULT_STYLE = "bright_magenta"

    @classmethod
    def get_style_for(cls, kind:str, event_type:str=None):
        if kind == "stimulus" or kind=="stimuli":
            if event_type == "CONVERSATION":
                return cls.STIMULUS_CONVERSATION_STYLE
            elif event_type == "THOUGHT":
                return cls.STIMULUS_THOUGHT_STYLE
            else:
                return cls.STIMULUS_DEFAULT_STYLE

        elif kind == "action":
            if event_type == "DONE":
                return cls.ACTION_DONE_STYLE
            elif event_type == "TALK":
                return cls.ACTION_TALK_STYLE
            elif event_type == "THINK":
                return cls.ACTION_THINK_STYLE
            else:
                return cls.ACTION_DEFAULT_STYLE

        elif kind == "intervention":
            return cls.INTERVENTION_DEFAULT_STYLE

# Пример использования функций
html_string = '<div style="color: red;">Hello</div>'
prefixed_html = inject_html_css_style_prefix(html_string, 'font-size: 20px;')
print(f"Prefixed HTML: {prefixed_html}")

text_to_break = "This is a long text that needs to be broken at a certain length."
broken_text = break_text_at_length(text_to_break, max_length=20)
print(f"Broken text: {broken_text}")

now = datetime.now()
formatted_datetime = pretty_datetime(now)
print(f"Formatted datetime: {formatted_datetime}")

text_with_indent = """
    This is a text
    with indent.
"""
dedented_text = dedent(text_with_indent)
print(f"Dedented text: {dedented_text}")

text_to_wrap = "This is a long text that needs to be wrapped to fit within a certain width."
wrapped_text = wrap_text(text_to_wrap, width=40)
print(f"Wrapped text: {wrapped_text}")

# Пример использования класса RichTextStyle
stimulus_style = RichTextStyle.get_style_for("stimulus", "CONVERSATION")
print(f"Stimulus style: {stimulus_style}")