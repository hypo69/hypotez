# Модуль для форматированного вывода в консоль (printer.py)

## Обзор

Этот модуль предоставляет утилиты для форматированного вывода данных в консоль, включая поддержку цветового оформления текста, фона и стилей шрифта.

## Подробней

Модуль `src.utils.printer` предназначен для улучшения читаемости вывода в консоль. Он предоставляет функцию `pprint`, которая позволяет выводить данные различных типов (словари, списки, строки, пути к файлам) с применением цветового оформления и стилей шрифта. Модуль использует ANSI escape-коды для управления цветом и стилем текста в консоли.

## Функции

### `_color_text`

**Назначение**: Применяет цвет, фон и стили шрифта к тексту.

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

**Параметры**:

-   `text` (str): Текст, к которому нужно применить стили.
-   `text_color` (str, optional): Цвет текста. По умолчанию "".
-   `bg_color` (str, optional): Цвет фона. По умолчанию "".
-   `font_style` (str, optional): Стиль шрифта. По умолчанию "".

**Возвращает**:

-   `str`: Текст со стилями, представленный в виде строки.

**Как работает функция**:

1.  Принимает текст и опциональные параметры для цвета текста, цвета фона и стиля шрифта.
2.  Формирует строку, содержащую ANSI escape-коды для применения указанных стилей к тексту.
3.  Возвращает отформатированную строку.

### `pprint`

**Назначение**: Форматированный вывод данных с опциональным цветом, фоном и стилем шрифта.

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
        \033[32m{\n            "name": "Alice",\n            "age": 30\n        }\033[0m

        >>> pprint(["apple", "banana", "cherry"], text_color="blue", font_style="bold")
        \033[34m\033[1mapple\033[0m
        \033[34m\033[1mbanana\033[0m
        \033[34m\033[1mcherry\033[0m

        >>> pprint("text example", text_color="yellow", bg_color="bg_red", font_style="underline")
        \033[4m\033[33m\033[41mtext example\033[0m
    """
    ...
```

**Параметры**:

-   `print_data` (Any, optional): Данные для вывода. Может быть `None`, словарем, списком, строкой или путем к файлу. По умолчанию `None`.
-   `text_color` (str, optional): Цвет текста. По умолчанию "white".
-   `bg_color` (str, optional): Цвет фона. По умолчанию "".
-   `font_style` (str, optional): Стиль шрифта. По умолчанию "".

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Проверяет, является ли `print_data` None и возвращает None если это так
2.  Принимает данные для вывода и опциональные параметры для цвета текста, цвета фона и стиля шрифта.
3.  Определяет тип данных и выполняет вывод в консоль соответствующим образом:
    -   Если данные - словарь, использует `json.dumps` для форматирования словаря в JSON и выводит его с отступами.
    -   Если данные - список, выводит каждый элемент списка на отдельной строке.
    -   Если данные - путь к файлу, пытается прочитать файл и вывести его содержимое (поддерживаются только `.csv` и `.xls` файлы).
    -   В противном случае выводит данные как строку.
4.  Применяет цветовое оформление и стиль шрифта к выводимым данным, используя функцию `_color_text`.
5.  Обрабатывает исключения, которые могут возникнуть при выводе данных.

## Переменные модуля

-   `RESET` (str): ANSI escape-код для сброса всех стилей.
-   `TEXT_COLORS` (dict): Словарь, содержащий соответствия между названиями цветов текста и их ANSI escape-кодами.
-   `BG_COLORS` (dict): Словарь, содержащий соответствия между названиями цветов фона и их ANSI escape-кодами.
-   `FONT_STYLES` (dict): Словарь, содержащий соответствия между названиями стилей шрифта и их ANSI escape-кодами.

## Пример использования

```python
from src.utils.printer import pprint

# Вывод словаря с цветовым оформлением
pprint({"name": "Alice", "age": 30}, text_color="green")

# Вывод списка с жирным шрифтом
pprint(["apple", "banana", "cherry"], text_color="blue", font_style="bold")

# Вывод строки с подчеркиванием и желтым цветом на красном фоне
pprint("text example", text_color="yellow", bg_color="bg_red", font_style="underline")
```

## Взаимосвязь с другими частями проекта

Этот модуль может использоваться другими модулями проекта `hypotez` для форматированного вывода данных в консоль. Он предоставляет удобный способ добавления цветового оформления и стилей шрифта к выводу, что может быть полезно для улучшения читаемости отладочной информации и пользовательского интерфейса.