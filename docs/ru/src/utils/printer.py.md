# Модуль `src.utils.printer`

## Обзор

Модуль `src.utils.printer` предоставляет утилиты для форматированного вывода данных в консоль с возможностью стилизации текста, включая цвет, фон и шрифт. Он содержит функции для удобного вывода различных типов данных, таких как словари, списки и строки, с использованием ANSI escape-кодов для стилизации.

## Подробнее

Модуль предназначен для улучшения читаемости выводимой в консоль информации путем добавления цветового оформления и стилей шрифта. Он использует ANSI escape-коды для управления отображением текста в терминале. Это может быть полезно для выделения важной информации, отладки и визуализации данных. <Объясни, как и зачем используется данный код в проекте `hypotez`.>

## Константы

### `RESET`

```python
RESET = "\\033[0m"
```

Сброс всех стилей текста (цвет, фон, шрифт) к значениям по умолчанию.

### `TEXT_COLORS`

```python
TEXT_COLORS = {
    "red": "\\033[31m",
    "green": "\\033[32m",
    "blue": "\\033[34m",
    "yellow": "\\033[33m",
    "white": "\\033[37m",
    "cyan": "\\033[36m",
    "magenta": "\\033[35m",
    "light_gray": "\\033[37m",
    "dark_gray": "\\033[90m",
    "light_red": "\\033[91m",
    "light_green": "\\033[92m",
    "light_blue": "\\033[94m",
    "light_yellow": "\\033[93m",
}
```

Словарь, содержащий ANSI escape-коды для различных цветов текста.

### `BG_COLORS`

```python
BG_COLORS = {
    "bg_red": "\\033[41m",
    "bg_green": "\\033[42m",
    "bg_blue": "\\033[44m",
    "bg_yellow": "\\033[43m",
    "bg_white": "\\033[47m",
    "bg_cyan": "\\033[46m",
    "bg_magenta": "\\033[45m",
    "bg_light_gray": "\\033[47m",
    "bg_dark_gray": "\\033[100m",
    "bg_light_red": "\\033[101m",
    "bg_light_green": "\\033[102m",
    "bg_light_blue": "\\033[104m",
    "bg_light_yellow": "\\033[103m",
}
```

Словарь, содержащий ANSI escape-коды для различных цветов фона текста.

### `FONT_STYLES`

```python
FONT_STYLES = {
    "bold": "\\033[1m",
    "underline": "\\033[4m",
}
```

Словарь, содержащий ANSI escape-коды для различных стилей шрифта (например, жирный, подчеркнутый).

## Функции

### `_color_text`

```python
def _color_text(text: str, text_color: str = "", bg_color: str = "", font_style: str = "") -> str:
    """Apply color, background, and font styling to the text.

    This helper function applies the provided color and font styles to the given text using ANSI escape codes.

    :param text: The text to be styled.
    :param text_color: The color to apply to the text. Default is an empty string, meaning no color.
    :param bg_color: The background color to apply to the text. Default is an empty string, meaning no background color.
    :param font_style: The font style to apply to the text. Default is an empty string, meaning no font style.
    :return: The styled text as a string.

    :example:
        >>> _color_text("Hello, World!", text_color="green", font_style="bold")
        \'\\033[1m\\033[32mHello, World!\\033[0m\'
    """
    return f"{font_style}{text_color}{bg_color}{text}{RESET}"
```

**Назначение**: Применяет цвет, фон и стиль шрифта к тексту с использованием ANSI escape-кодов.

**Параметры**:

-   `text` (str): Текст, к которому применяется стилизация.
-   `text_color` (str, optional): Цвет текста. По умолчанию "".
-   `bg_color` (str, optional): Цвет фона текста. По умолчанию "".
-   `font_style` (str, optional): Стиль шрифта. По умолчанию "".

**Возвращает**:

-   `str`: Стилизованный текст.

**Как работает функция**:

Функция принимает текст и опциональные параметры для цвета текста, цвета фона и стиля шрифта. Она формирует строку, содержащую ANSI escape-коды для указанных стилей, обрамляющие входной текст, и добавляет код сброса стилей в конце, чтобы не влиять на последующий вывод.

**Примеры**:

```python
_color_text("Hello, World!", text_color="green", font_style="bold")
# Возвращает: '\033[1m\033[32mHello, World!\033[0m'
```

### `pprint`

```python
def pprint(print_data: Any = None, text_color: str = "white", bg_color: str = "", font_style: str = "") -> None:
    """Pretty prints the given data with optional color, background, and font style.

    This function formats the input data based on its type and prints it to the console. The data is printed with optional 
    text color, background color, and font style based on the specified parameters. The function can handle dictionaries, 
    lists, strings, and file paths.

    :param print_data: The data to be printed. Can be of type ``None``, ``dict``, ``list``, ``str``, or ``Path``.
    :param text_color: The color to apply to the text. Default is \'white\'. See :ref:`TEXT_COLORS`.
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
\n
        >>> pprint(["apple", "banana", "cherry"], text_color="blue", font_style="bold")
        \\033[34m\\033[1mapple\\033[0m\n
        \\033[34m\\033[1mbanana\\033[0m\n
        \\033[34m\\033[1mcherry\\033[0m\n
\n
        >>> pprint("text example", text_color="yellow", bg_color="bg_red", font_style="underline")
        \\033[4m\\033[33m\\033[41mtext example\\033[0m\n
    """
    if not print_data:\n
        return\n
    if isinstance(text_color, str):\n
        text_color = TEXT_COLORS.get(text_color.lower(), TEXT_COLORS["white"])\n
    if isinstance(bg_color, str):\n
        bg_color = BG_COLORS.get(bg_color.lower(), "")\n
    if isinstance(font_style, str):\n
        font_style = FONT_STYLES.get(font_style.lower(), "")\n
\n
\n
    try:\n
        if isinstance(print_data, dict):\n
            print(_color_text(json.dumps(print_data, indent=4), text_color))\n
        elif isinstance(print_data, list):\n
            for item in print_data:\n
                print(_color_text(str(item), text_color))\n
        elif isinstance(print_data, (str, Path)) and Path(print_data).is_file():\n
            ext = Path(print_data).suffix.lower()\n
            if ext in [\'.csv\', \'.xls\']:\n
                print(_color_text("File reading supported for .csv, .xls only.", text_color))\n
            else:\n
                print(_color_text("Unsupported file type.", text_color))\n
        else:\n
            print(_color_text(str(print_data), text_color))\n
    except Exception as ex:\n
        print(_color_text(f"Error: {ex}", text_color=TEXT_COLORS["red"]))\n
```

**Назначение**: Форматированный вывод данных с возможностью стилизации текста.

**Параметры**:

-   `print_data` (Any, optional): Данные для вывода. Может быть `None`, `dict`, `list`, `str` или `Path`.
-   `text_color` (str, optional): Цвет текста. По умолчанию "white".
-   `bg_color` (str, optional): Цвет фона. По умолчанию "".
-   `font_style` (str, optional): Стиль шрифта. По умолчанию "".

**Возвращает**:

-   `None`

**Как работает функция**:

Функция `pprint` принимает данные различных типов и выводит их в консоль с применением указанных стилей текста. Она проверяет тип входных данных и соответствующим образом форматирует вывод:

-   Если данные являются словарем, они выводятся в формате JSON с отступами.
-   Если данные являются списком, каждый элемент списка выводится на отдельной строке.
-   Если данные являются строкой или путем к файлу, функция проверяет расширение файла и выводит сообщение о поддержке чтения только для файлов `.csv` и `.xls`.
-   В случае возникновения ошибки при выводе данных, функция выводит сообщение об ошибке красным цветом.
    Если `print_data` не передано - функция ничего не делает.

Внутри функция использует `_color_text` для добавления стилей к тексту перед выводом.

**Примеры**:

```python
pprint({"name": "Alice", "age": 30}, text_color="green")
# Выводит:
# \033[32m{
#     "name": "Alice",
#     "age": 30
# }\033[0m

pprint(["apple", "banana", "cherry"], text_color="blue", font_style="bold")
# Выводит:
# \033[34m\033[1mapple\033[0m
# \033[34m\033[1mbanana\033[0m
# \033[34m\033[1mcherry\033[0m

pprint("text example", text_color="yellow", bg_color="bg_red", font_style="underline")
# Выводит: \033[4m\033[33m\033[41mtext example\033[0m
```

```python
if __name__ == '__main__':
    pprint({"name": "Alice", "age": 30}, text_color="green")
```

Этот блок кода выполняется только при запуске модуля как основной программы. В данном случае, он выводит словарь `{"name": "Alice", "age": 30}` с зеленым цветом текста.