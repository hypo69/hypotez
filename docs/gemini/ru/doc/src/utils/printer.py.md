# Модуль `src.utils.printer`

## Обзор

Модуль `src.utils.printer` предоставляет утилиты для форматированного вывода данных в консоль. Он включает функции для стилизации текста, такие как изменение цвета, фона и стиля шрифта. Модуль предназначен для улучшения читаемости выводимой информации, что особенно полезно при отладке и логировании.

## Подробнее

Модуль содержит функции для применения стилей к тексту с использованием ANSI escape-кодов. Это позволяет настраивать внешний вид выводимых данных, делая их более информативными и удобными для восприятия. В частности, поддерживается вывод словарей, списков и содержимого файлов определенных форматов (например, CSV).

## Классы

В данном модуле классы отсутствуют.

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
        \'\\033[1m\\033[32mHello, World!\\033[0m\'
    """
    return f"{font_style}{text_color}{bg_color}{text}{RESET}"
```

**Назначение**: Применяет стили (цвет текста, цвет фона, стиль шрифта) к заданной строке текста с использованием ANSI escape-кодов.

**Параметры**:

-   `text` (str): Текст, к которому необходимо применить стили.
-   `text_color` (str, optional): Цвет текста. По умолчанию пустая строка (без цвета).
-   `bg_color` (str, optional): Цвет фона. По умолчанию пустая строка (без фона).
-   `font_style` (str, optional): Стиль шрифта. По умолчанию пустая строка (без стиля).

**Возвращает**:

-   `str`: Текст со стилями, примененными в виде ANSI escape-кодов.

**Как работает функция**:

1.  Формирует строку с ANSI escape-кодами для указанного стиля шрифта, цвета текста и цвета фона.
2.  Объединяет коды стилей с входным текстом.
3.  Добавляет код сброса (`RESET`) в конце строки, чтобы вернуть стиль консоли к исходному состоянию после вывода текста.

**Примеры**:

```python
>>> _color_text("Hello, World!", text_color="green", font_style="bold")
'\033[1m\033[32mHello, World!\033[0m'
```

### `pprint`

```python
def pprint(print_data: Any = None, text_color: str = "white", bg_color: str = "", font_style: str = "") -> None:
    """Pretty prints the given data with optional color, background, and font style.

    This function formats the input data based on its type and prints it to the console. The data is printed with optional 
    text color, background color, and font style based on the specified parameters. The function can handle dictionaries, 
    lists, strings, and file paths.

    :param print_data: The data to be printed. Can be of type ``None``, ``dict``, ``list``, ``str``, or ``Path``.\n
    :param text_color: The color to apply to the text. Default is \'white\'. See :ref:`TEXT_COLORS`.\n
    :param bg_color: The background color to apply to the text. Default is \'\' (no background color). See :ref:`BG_COLORS`.\n
    :param font_style: The font style to apply to the text. Default is \'\' (no font style). See :ref:`FONT_STYLES`.\n
    :return: None

    :raises: Exception if the data type is unsupported or an error occurs during printing.

    :example:
        >>> pprint({"name": "Alice", "age": 30}, text_color="green")
        \\033[32m{\n
            "name": "Alice",\n
            "age": 30\n
        }\\033[0m\n

        >>> pprint(["apple", "banana", "cherry"], text_color="blue", font_style="bold")
        \\033[34m\\033[1mapple\\033[0m\n
        \\033[34m\\033[1mbanana\\033[0m\n
        \\033[34m\\033[1mcherry\\033[0m\n

        >>> pprint("text example", text_color="yellow", bg_color="bg_red", font_style="underline")
        \\033[4m\\033[33m\\033[41mtext example\\033[0m
    """
    if not print_data:
        return
    if isinstance(text_color, str):
        text_color = TEXT_COLORS.get(text_color.lower(), TEXT_COLORS["white"])
    if isinstance(bg_color, str):
        bg_color = BG_COLORS.get(bg_color.lower(), "")
    if isinstance(font_style, str):
        font_style = FONT_STYLES.get(font_style.lower(), "")


    try:
        if isinstance(print_data, dict):
            print(_color_text(json.dumps(print_data, indent=4), text_color))
        elif isinstance(print_data, list):
            for item in print_data:
                print(_color_text(str(item), text_color))
        elif isinstance(print_data, (str, Path)) and Path(print_data).is_file():
            ext = Path(print_data).suffix.lower()
            if ext in ['.csv', '.xls']:
                print(_color_text("File reading supported for .csv, .xls only.", text_color))
            else:
                print(_color_text("Unsupported file type.", text_color))
        else:
            print(_color_text(str(print_data), text_color))
    except Exception as ex:
        print(_color_text(f"Error: {ex}", text_color=TEXT_COLORS["red"]))
```

**Назначение**: Выводит данные в консоль с применением стилизации текста (цвет, фон, стиль шрифта).

**Параметры**:

-   `print_data` (Any, optional): Данные для вывода. Может быть `None`, `dict`, `list`, `str` или `Path`.
-   `text_color` (str, optional): Цвет текста. По умолчанию "white".
-   `bg_color` (str, optional): Цвет фона. По умолчанию "" (без фона).
-   `font_style` (str, optional): Стиль шрифта. По умолчанию "" (без стиля).

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Проверяет, переданы ли данные для вывода. Если `print_data` равен `None`, функция завершается.
2.  Получает значения цветов и стилей из словарей `TEXT_COLORS`, `BG_COLORS` и `FONT_STYLES` соответственно. Если указанный стиль не найден, используется значение по умолчанию.
3.  Определяет тип данных для вывода и выполняет соответствующие действия:
    *   Если данные - словарь (`dict`), они преобразуются в JSON-строку с отступами и выводятся с применением стилей.
    *   Если данные - список (`list`), каждый элемент списка выводится на отдельной строке с применением стилей.
    *   Если данные - строка (`str`) или путь к файлу (`Path`), проверяется, является ли путь файлом. Если это файл с расширением `.csv` или `.xls`, выводится сообщение о поддержке чтения только для этих форматов. В противном случае выводится сообщение о неподдерживаемом типе файла.
    *   Если тип данных не соответствует ни одному из вышеперечисленных, данные преобразуются в строку и выводятся с применением стилей.
4.  В случае возникновения исключения при выводе данных, перехватывает исключение и выводит сообщение об ошибке красным цветом.

**Примеры**:

```python
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