### **Анализ кода модуля `rendering.py`**

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Четкая структура и разделение функциональности.
    - Использование `textwrap` для работы с текстом.
    - Наличие класса `RichTextStyle` для определения стилей текста.
- **Минусы**:
    - Отсутствуют docstring для некоторых функций и класса.
    - Жестко заданные стили в классе `RichTextStyle`.
    - Смешанный стиль кавычек (использование как двойных, так и одинарных).

**Рекомендации по улучшению**:

1.  **Документирование кода**:
    *   Добавить docstring для всех функций и класса `RichTextStyle`, чтобы пояснить их назначение, параметры и возвращаемые значения.

2.  **Унификация кавычек**:
    *   Использовать только одинарные кавычки (`'`) для строк.

3.  **Улучшение класса `RichTextStyle`**:
    *   Предоставить возможность настройки стилей через параметры, а не только через жестко заданные значения.
    *   Добавить docstring для класса и его методов.

4.  **Логирование**:
    *   В важных местах добавить логирование с использованием модуля `logger` из `src.logger`.

5.  **Обработка исключений**:
    *   Рассмотреть возможность добавления обработки исключений в функциях, где это может быть необходимо.

**Оптимизированный код**:

```python
import json
import textwrap
from datetime import datetime
from typing import Union

from tinytroupe.utils import logger


################################################################################
# Rendering and markup
################################################################################
def inject_html_css_style_prefix(html: str, style_prefix_attributes: str) -> str:
    """
    Добавляет префикс стиля ко всем атрибутам style в заданной HTML-строке.

    Args:
        html (str): HTML-строка для изменения.
        style_prefix_attributes (str): Префикс стиля для добавления.

    Returns:
        str: HTML-строка с добавленным префиксом стиля.

    Example:
        >>> inject_html_css_style_prefix('<div style="color: red;">Hello</div>', 'font-size: 20px;')
        '<div style="font-size: 20px;color: red;">Hello</div>'
    """
    # Заменяем 'style="' на 'style="{style_prefix_attributes};'
    return html.replace('style="', f'style="{style_prefix_attributes};')


def break_text_at_length(text: str | dict, max_length: int | None = None) -> str:
    """
    Разбивает текст (или JSON) на указанной длине, вставляя строку "(...)".
    Если максимальная длина не указана (`None`), возвращает текст как есть.

    Args:
        text (str | dict): Текст для разбивки или JSON-объект.
        max_length (int | None): Максимальная длина текста. По умолчанию `None`.

    Returns:
        str: Разбитый текст с добавлением "(...)", если необходимо.

    Example:
        >>> break_text_at_length("Hello world!", 5)
        'Hello (...)'
        >>> break_text_at_length("Hello world!", None)
        'Hello world!'
    """
    # Преобразуем словарь в JSON-строку с отступами, если это словарь
    if isinstance(text, dict):
        text = json.dumps(text, indent=4)

    # Проверяем, нужно ли разбивать текст
    if max_length is None or len(text) <= max_length:
        return text
    else:
        # Разбиваем текст и добавляем "(...)"
        return text[:max_length] + " (...)"


def pretty_datetime(dt: datetime) -> str:
    """
    Возвращает строковое представление объекта datetime в формате "YYYY-MM-DD HH:MM".

    Args:
        dt (datetime): Объект datetime для преобразования.

    Returns:
        str: Строковое представление даты и времени.

    Example:
        >>> import datetime
        >>> dt = datetime.datetime(2024, 1, 1, 12, 30)
        >>> pretty_datetime(dt)
        '2024-01-01 12:30'
    """
    # Форматируем datetime объект в строку
    return dt.strftime('%Y-%m-%d %H:%M')


def dedent(text: str) -> str:
    """
    Удаляет лишние пробелы и отступы в начале текста.

    Args:
        text (str): Текст для обработки.

    Returns:
        str: Текст без лишних пробелов и отступов.

    Example:
        >>> text = "  Hello\\n   World!"
        >>> dedent(text)
        'Hello\\nWorld!'
    """
    # Удаляем отступы и пробелы в начале текста
    return textwrap.dedent(text).strip()


def wrap_text(text: str, width: int = 100) -> str:
    """
    Переносит текст на новую строку после указанной ширины.

    Args:
        text (str): Текст для переноса.
        width (int): Ширина строки. По умолчанию 100.

    Returns:
        str: Текст с переносами строк.

    Example:
        >>> text = "This is a long text that needs to be wrapped."
        >>> wrap_text(text, 20)
        'This is a long text\\nthat needs to be\\nwrapped.'
    """
    # Переносим текст на новую строку после указанной ширины
    return textwrap.fill(text, width=width)


class RichTextStyle:
    """
    Класс для хранения стилей текста, используемых в Rich.

    Атрибуты класса:
        STIMULUS_CONVERSATION_STYLE (str): Стиль для сообщений в формате разговора.
        STIMULUS_THOUGHT_STYLE (str): Стиль для мыслей.
        STIMULUS_DEFAULT_STYLE (str): Стиль по умолчанию для стимулов.
        ACTION_DONE_STYLE (str): Стиль для завершенных действий.
        ACTION_TALK_STYLE (str): Стиль для речи.
        ACTION_THINK_STYLE (str): Стиль для размышлений.
        ACTION_DEFAULT_STYLE (str): Стиль по умолчанию для действий.
        INTERVENTION_DEFAULT_STYLE (str): Стиль по умолчанию для интервенций.

    Методы класса:
        get_style_for(kind: str, event_type: str = None) -> str: Возвращает стиль для указанного типа события.
    """

    # Consult color options here: https://rich.readthedocs.io/en/stable/appendix/colors.html

    STIMULUS_CONVERSATION_STYLE = 'bold italic cyan1'
    STIMULUS_THOUGHT_STYLE = 'dim italic cyan1'
    STIMULUS_DEFAULT_STYLE = 'italic'

    ACTION_DONE_STYLE = 'grey82'
    ACTION_TALK_STYLE = 'bold green3'
    ACTION_THINK_STYLE = 'green'
    ACTION_DEFAULT_STYLE = 'purple'

    INTERVENTION_DEFAULT_STYLE = 'bright_magenta'

    @classmethod
    def get_style_for(cls, kind: str, event_type: str | None = None) -> str:
        """
        Возвращает стиль для указанного типа события.

        Args:
            kind (str): Тип события ("stimulus", "action", "intervention").
            event_type (str | None): Подтип события (например, "CONVERSATION", "THOUGHT", "DONE", "TALK", "THINK"). По умолчанию `None`.

        Returns:
            str: Строка стиля для Rich.

        Example:
            >>> RichTextStyle.get_style_for('stimulus', 'CONVERSATION')
            'bold italic cyan1'
            >>> RichTextStyle.get_style_for('action', 'TALK')
            'bold green3'
        """
        # Возвращаем стиль для стимула
        if kind == 'stimulus' or kind == 'stimuli':
            if event_type == 'CONVERSATION':
                return cls.STIMULUS_CONVERSATION_STYLE
            elif event_type == 'THOUGHT':
                return cls.STIMULUS_THOUGHT_STYLE
            else:
                return cls.STIMULUS_DEFAULT_STYLE

        # Возвращаем стиль для действия
        elif kind == 'action':
            if event_type == 'DONE':
                return cls.ACTION_DONE_STYLE
            elif event_type == 'TALK':
                return cls.ACTION_TALK_STYLE
            elif event_type == 'THINK':
                return cls.ACTION_THINK_STYLE
            else:
                return cls.ACTION_DEFAULT_STYLE

        # Возвращаем стиль для интервенции
        elif kind == 'intervention':
            return cls.INTERVENTION_DEFAULT_STYLE