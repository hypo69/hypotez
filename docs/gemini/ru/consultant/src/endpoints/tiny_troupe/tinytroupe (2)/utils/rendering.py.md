### **Анализ кода модуля `rendering.py`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Четкая структура кода.
    - Использование аннотаций типов.
    - Использование `textwrap` для форматирования текста.
- **Минусы**:
    - Отсутствие документации модуля.
    - Не все функции имеют подробные docstring.
    - В некоторых местах можно улучшить читаемость кода.
    - Нет обработки исключений.
    - Не используется модуль `logger` для логирования.

**Рекомендации по улучшению:**

1.  **Добавить документацию модуля**:
    - Добавить общее описание модуля, его назначения и примеры использования.
2.  **Улучшить docstring**:
    - Добавить более подробные описания для каждой функции, включая аргументы, возвращаемые значения и возможные исключения.
    - Перевести docstring на русский язык, если они на английском.
3.  **Обработка исключений**:
    - Добавить блоки `try...except` для обработки возможных исключений, особенно при работе с JSON.
    - Использовать `logger.error` для логирования ошибок.
4.  **Использовать `logger`**:
    - Заменить `print` на `logger.info` или `logger.debug` для отладочной информации.
5.  **Форматирование кода**:
    - Убедиться, что код соответствует стандартам PEP8.
6.  **Использовать одинарные кавычки**:
    - Заменить двойные кавычки на одинарные, где это необходимо.
7.  **Аннотации**
    - Добавить аннотации типа для всех переменных.

**Оптимизированный код:**

```python
"""
Модуль для рендеринга и разметки текста.
=================================================

Модуль содержит функции для инъекции стилей, обрезки текста, форматирования дат и времени,
удаления отступов и переноса текста. Также включает класс :class:`RichTextStyle` для
управления стилями текста.

Пример использования
----------------------

>>> from datetime import datetime
>>> from tinytroupe.utils.rendering import pretty_datetime
>>> dt = datetime.now()
>>> pretty_datetime(dt)
'2024-07-24 14:30'
"""
import json
import textwrap
from datetime import datetime
from typing import Union, Optional

from tinytroupe.utils import logger


################################################################################
# Rendering and markup
################################################################################
def inject_html_css_style_prefix(html: str, style_prefix_attributes: str) -> str:
    """
    Вставляет префикс стиля ко всем атрибутам style в данной HTML строке.

    Args:
        html (str): HTML строка для изменения.
        style_prefix_attributes (str): Префикс стиля для вставки.

    Returns:
        str: HTML строка с добавленными префиксами стилей.

    Example:
        >>> inject_html_css_style_prefix('<div style="color: red;">Hello</div>', 'font-size: 20px;')
        '<div style="font-size: 20px;color: red;">Hello</div>'
    """
    return html.replace('style="', f'style="{style_prefix_attributes};')


def break_text_at_length(text: str | dict, max_length: Optional[int] = None) -> str:
    """
    Обрывает текст (или JSON) на указанной длине, вставляя строку "(...)".
    Если максимальная длина `None`, содержимое возвращается как есть.

    Args:
        text (str | dict): Текст или JSON для обрезки.
        max_length (Optional[int], optional): Максимальная длина текста. По умолчанию `None`.

    Returns:
        str: Обрезанный текст или исходный текст, если `max_length` равен `None`.

    Example:
        >>> break_text_at_length('This is a long text', 10)
        'This is a  (...)'
        >>> break_text_at_length('This is a long text', None)
        'This is a long text'
    """
    if isinstance(text, dict):
        try:
            text = json.dumps(text, indent=4)
        except Exception as ex:
            logger.error('Error while dumping JSON', ex, exc_info=True)
            return str(text)  # Возвращаем строковое представление объекта в случае ошибки

    if max_length is None or len(text) <= max_length:
        return text
    else:
        return text[:max_length] + ' (...)'


def pretty_datetime(dt: datetime) -> str:
    """
    Возвращает строковое представление объекта datetime в формате "YYYY-MM-DD HH:MM".

    Args:
        dt (datetime): Объект datetime для форматирования.

    Returns:
        str: Строковое представление даты и времени.

    Example:
        >>> from datetime import datetime
        >>> dt = datetime(2024, 7, 24, 14, 30)
        >>> pretty_datetime(dt)
        '2024-07-24 14:30'
    """
    return dt.strftime('%Y-%m-%d %H:%M')


def dedent(text: str) -> str:
    """
    Удаляет отступы в начале текста и возвращает очищенный текст.

    Args:
        text (str): Текст для удаления отступов.

    Returns:
        str: Текст без отступов.

    Example:
        >>> text = '  Hello\\n  World'
        >>> dedent(text)
        'Hello\\nWorld'
    """
    return textwrap.dedent(text).strip()


def wrap_text(text: str, width: int = 100) -> str:
    """
    Переносит текст на новую строку после указанной ширины.

    Args:
        text (str): Текст для переноса.
        width (int, optional): Максимальная ширина строки. По умолчанию 100.

    Returns:
        str: Текст с переносами строк.

    Example:
        >>> text = 'This is a long text that needs to be wrapped.'
        >>> wrap_text(text, width=20)
        'This is a long text\\nthat needs to be\\nwrapped.'
    """
    return textwrap.fill(text, width=width)


class RichTextStyle:
    """
    Класс для управления стилями текста, используемыми в rich.

    Атрибуты:
        STIMULUS_CONVERSATION_STYLE (str): Стиль для текста в разговоре.
        STIMULUS_THOUGHT_STYLE (str): Стиль для мыслей.
        STIMULUS_DEFAULT_STYLE (str): Стиль по умолчанию для стимулов.
        ACTION_DONE_STYLE (str): Стиль для завершенных действий.
        ACTION_TALK_STYLE (str): Стиль для речи.
        ACTION_THINK_STYLE (str): Стиль для мыслей в действиях.
        ACTION_DEFAULT_STYLE (str): Стиль по умолчанию для действий.
        INTERVENTION_DEFAULT_STYLE (str): Стиль по умолчанию для вмешательств.
    """

    # Consult color options here: https://rich.readthedocs.io/en/stable/appendix/colors.html

    STIMULUS_CONVERSATION_STYLE: str = 'bold italic cyan1'
    STIMULUS_THOUGHT_STYLE: str = 'dim italic cyan1'
    STIMULUS_DEFAULT_STYLE: str = 'italic'

    ACTION_DONE_STYLE: str = 'grey82'
    ACTION_TALK_STYLE: str = 'bold green3'
    ACTION_THINK_STYLE: str = 'green'
    ACTION_DEFAULT_STYLE: str = 'purple'

    INTERVENTION_DEFAULT_STYLE: str = 'bright_magenta'

    @classmethod
    def get_style_for(cls, kind: str, event_type: Optional[str] = None) -> str:
        """
        Возвращает стиль для указанного типа события и категории.

        Args:
            kind (str): Тип категории ("stimulus", "action", "intervention").
            event_type (str, optional): Тип события. По умолчанию `None`.

        Returns:
            str: Стиль для указанного типа события и категории.

        Raises:
            ValueError: Если указан неизвестный тип категории.

        Example:
            >>> RichTextStyle.get_style_for('stimulus', 'CONVERSATION')
            'bold italic cyan1'
            >>> RichTextStyle.get_style_for('action', 'DONE')
            'grey82'
        """
        if kind == 'stimulus' or kind == 'stimuli':
            if event_type == 'CONVERSATION':
                return cls.STIMULUS_CONVERSATION_STYLE
            elif event_type == 'THOUGHT':
                return cls.STIMULUS_THOUGHT_STYLE
            else:
                return cls.STIMULUS_DEFAULT_STYLE

        elif kind == 'action':
            if event_type == 'DONE':
                return cls.ACTION_DONE_STYLE
            elif event_type == 'TALK':
                return cls.ACTION_TALK_STYLE
            elif event_type == 'THINK':
                return cls.ACTION_THINK_STYLE
            else:
                return cls.ACTION_DEFAULT_STYLE

        elif kind == 'intervention':
            return cls.INTERVENTION_DEFAULT_STYLE
        else:
            raise ValueError(f'Unknown kind: {kind}')