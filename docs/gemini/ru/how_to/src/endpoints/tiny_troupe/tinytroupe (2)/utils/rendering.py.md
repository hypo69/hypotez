## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предоставляет набор функций и класс для форматирования и обработки текста. 
Он включает в себя функции для вставки CSS-стилей, обрезки текста, форматирования дат, удаления отступов, 
обёртывания текста, а также класс `RichTextStyle` для определения стилей текста.

Шаги выполнения
-------------------------
1. **Вставка стилей**: Функция `inject_html_css_style_prefix` позволяет добавлять префикс ко всем 
   атрибутам стиля в HTML-строке.
2. **Обрезка текста**: Функция `break_text_at_length` обрезает текст или JSON-строку до заданной 
   длины, добавляя в точку обрезания "(...)".
3. **Форматирование дат**: Функция `pretty_datetime` форматирует объект `datetime` в строку 
   в виде "YYYY-MM-DD HH:MM".
4. **Удаление отступов**: Функция `dedent` удаляет ведущие пробелы и отступы из текста.
5. **Обёртывание текста**: Функция `wrap_text` обёртывает текст по заданной ширине.
6. **Определение стилей**: Класс `RichTextStyle` предоставляет статические методы для определения 
   стилей текста, таких как `STIMULUS_CONVERSATION_STYLE`, `ACTION_TALK_STYLE` и т.д.

Пример использования
-------------------------

```python
from datetime import datetime
from tinytroupe.utils.rendering import (
    inject_html_css_style_prefix,
    break_text_at_length,
    pretty_datetime,
    dedent,
    wrap_text,
    RichTextStyle,
)

# Вставка стилей в HTML
html_with_style = inject_html_css_style_prefix(
    '<div style="color: red;">Hello</div>', "font-size: 20px;"
)
print(html_with_style)  # <div style="font-size: 20px;color: red;">Hello</div>

# Обрезка текста
text = "This is a long text that needs to be broken at a certain length."
truncated_text = break_text_at_length(text, max_length=20)
print(truncated_text)  # This is a long text (...)

# Форматирование даты
dt = datetime.now()
pretty_dt = pretty_datetime(dt)
print(pretty_dt)  # 2023-12-14 18:14

# Удаление отступов
text_with_indent = """
    This text has some leading whitespace and indentation.
"""
dedented_text = dedent(text_with_indent)
print(dedented_text)  # This text has some leading whitespace and indentation.

# Обёртывание текста
wrapped_text = wrap_text("This text will be wrapped at a specified width.", width=30)
print(wrapped_text)  # This text will be
                # wrapped at a
                # specified width.

# Получение стиля текста
stimulus_style = RichTextStyle.get_style_for("stimulus", event_type="CONVERSATION")
print(stimulus_style)  # bold italic cyan1
```

**Важно**: 
* Все стили в `RichTextStyle` определены с использованием палитры цветов `rich`.
* Для получения доступных цветов обратитесь к документации `rich` по адресу `https://rich.readthedocs.io/en/stable/appendix/colors.html`.