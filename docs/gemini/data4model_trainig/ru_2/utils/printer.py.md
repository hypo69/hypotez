### Анализ кода `hypotez/src/utils/printer.py.md`

## Обзор

Модуль предоставляет утилиты для форматированного вывода текста в консоль с использованием ANSI escape-кодов для стилизации.

## Подробнее

Этот модуль содержит функции для красивого и структурированного вывода данных в консоль. Он включает функцию `pprint` для вывода данных различных типов (словари, списки, строки, пути к файлам) с возможностью настройки цвета текста, фона и стиля шрифта. Также определены константы для задания цветов и стилей.

## Функции

### `_color_text`

```python
def _color_text(text: str, text_color: str = "", bg_color: str = "", font_style: str = "") -> str:
    """Apply color, background, and font styling to the text.

    This helper function applies the provided color and font styles to the given text using ANSI escape codes.

    :param text: The text to be styled.
    :param text_color: The color to apply to the text. Default is an empty string, meaning no color.
    :param bg_color: The background color to apply. Default is an empty string, meaning no background color.
    :param font_style: The font style to apply to the text. Default is an empty string, meaning no font style.
    :return: The styled text as a string.

    :example:
        >>> _color_text("Hello, World!", text_color="green", font_style="bold")
        '\033[1m\033[32mHello, World!\033[0m'
    """
    ...
```

**Назначение**:
Применяет цвет, фон и стиль шрифта к тексту с использованием ANSI escape-кодов.

**Параметры**:

*   `text` (str): Текст, который нужно стилизовать.
*   `text_color` (str, optional): Цвет текста. По умолчанию "".
*   `bg_color` (str, optional): Цвет фона. По умолчанию "".
*   `font_style` (str, optional): Стиль шрифта. По умолчанию "".

**Возвращает**:

*   `str`: Стилизованный текст.

**Как работает функция**:

1.  Формирует строку, содержащую ANSI escape-коды для указанных стилей и цветов, а также сам текст.
2.  Возвращает полученную строку.

### `pprint`

```python
def pprint(print_data: Any = None, text_color: str = "white", bg_color: str = "", font_style: str = "") -> None:
    """Pretty prints the given data with optional color, background, and font style.

    This function formats the input data based on its type and prints it to the console. The data is printed with optional 
    text color, background color, and font style based on the specified parameters. The function can handle dictionaries, 
    lists, strings, and file paths.

    :param print_data: The data to be printed. Can be of type ``None``, ``dict``, ``list``, ``str``, or ``Path``.\n    :param text_color: The color to apply to the text. Default is \'white\'. See :ref:`TEXT_COLORS`.\n    :param bg_color: The background color to apply to the text. Default is \'\' (no background color). See :ref:`BG_COLORS`.\n    :param font_style: The font style to apply to the text. Default is \'\' (no font style). See :ref:`FONT_STYLES`.
    :return: None

    :raises: Exception if the data type is unsupported or an error occurs during printing.

    :example:
        >>> pprint({"name": "Alice", "age": 30}, text_color="green")
        \033[32m{
            "name": "Alice",
            "age": 30
        }\033[0m

        >>> pprint(["apple", "banana", "cherry"], text_color="blue", font_style="bold")
        \033[34m\033[1mapple\033[0m
        \033[34m\033[1mbanana\033[0m
        \033[34m\033[1mcherry\033[0m

        >>> pprint("text example", text_color="yellow", bg_color="bg_red", font_style="underline")
        \033[4m\033[33m\033[41mtext example\033[0m
    """
    ...
```

**Назначение**:
Выводит данные в консоль с возможностью указания цвета текста, фона и стиля шрифта.

**Параметры**:

*   `print_data` (Any, optional): Данные для вывода. Может быть `None`, `dict`, `list`, `str` или `Path`. По умолчанию `None`.
*   `text_color` (str, optional): Цвет текста. По умолчанию "white". См. `TEXT_COLORS`.
*   `bg_color` (str, optional): Цвет фона. По умолчанию "" (нет цвета фона). См. `BG_COLORS`.
*   `font_style` (str, optional): Стиль шрифта. По умолчанию "" (нет стиля шрифта). См. `FONT_STYLES`.

**Возвращает**:

*   `None`

**Вызывает исключения**:

*   `Exception`: Если тип данных не поддерживается или произошла ошибка во время вывода.

**Как работает функция**:

1.  Проверяет, переданы ли данные для вывода. Если нет, завершает работу.
2.  Преобразует названия цветов и стилей в соответствующие ANSI escape-коды.
3.  В зависимости от типа данных:

    *   Если данные - словарь, выводит его в формате JSON с отступами.
    *   Если данные - список, выводит каждый элемент списка на отдельной строке.
    *   Если данные - путь к файлу, выводит сообщение о поддержке чтения только для файлов `.csv` и `.xls`.
    *   В противном случае выводит данные как строку.
4.  Применяет стилизацию текста с помощью функции `_color_text`.
5.  Выводит стилизованный текст в консоль.
6.  В случае возникновения исключения выводит сообщение об ошибке.

## Константы

### `RESET`

**Назначение**: ANSI escape-код для сброса всех стилей.

### `TEXT_COLORS`

**Назначение**: Словарь, содержащий соответствие между названиями цветов текста и ANSI escape-кодами для этих цветов.

### `BG_COLORS`

**Назначение**: Словарь, содержащий соответствие между названиями цветов фона и ANSI escape-кодами для этих цветов.

### `FONT_STYLES`

**Назначение**: Словарь, содержащий соответствие между названиями стилей шрифта и ANSI escape-кодами для этих стилей.

## Примеры использования

```python
from src.utils.printer import pprint

pprint({"name": "Alice", "age": 30}, text_color="green")
pprint(["apple", "banana", "cherry"], text_color="blue", font_style="bold")
pprint("text example", text_color="yellow", bg_color="bg_red", font_style="underline")
```

## Зависимости

*   `json`: Для работы с JSON-данными.
*   `csv`:  Хотя и импортирован, в коде не используется
*   `pandas`:  Хотя и импортирован, в коде не используется
*   `pathlib.Path`: Для работы с путями к файлам.
*   `typing.Any`: Для аннотаций типов.
*   `pprint`: для форматированного вывода.
*   `src.logger.logger`: Для логирования событий и ошибок.

## Взаимосвязи с другими частями проекта

Модуль `printer.py` предоставляет утилиты для форматированного вывода данных в консоль, которые могут использоваться в различных частях проекта `hypotez` для улучшения читаемости вывода и облегчения отладки.