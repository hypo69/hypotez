# Модуль `src.utils.printer`

## Обзор

Модуль `src.utils.printer` предоставляет утилиты для форматированного вывода данных в консоль с возможностью стилизации текста, включая изменение цвета, фона и шрифта. Он предназначен для улучшения читаемости выводимой информации, особенно при отладке и логировании.

## Более подробно

Этот модуль содержит функции для стилизации текста с использованием ANSI escape-кодов, что позволяет настраивать цвет текста, фона и стиль шрифта. Он также включает функцию `pprint`, которая автоматически форматирует данные различных типов (например, словари, списки) и выводит их в консоль с применением указанных стилей. Модуль поддерживает чтение и стилизацию содержимого файлов `.csv` и `.xls`.

## Содержание

1.  [Константы](#константы)
2.  [Функции](#функции)
    *   [`_color_text`](#_color_text)
    *   [`pprint`](#pprint)

## Константы

### `RESET`

```python
RESET = "\\033[0m"
```

Сброс всех стилей текста ANSI escape-кодом.

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

Словарь, содержащий ANSI escape-коды для различных цветов фона.

### `FONT_STYLES`

```python
FONT_STYLES = {
    "bold": "\\033[1m",
    "underline": "\\033[4m",
}
```

Словарь, содержащий ANSI escape-коды для различных стилей шрифта (например, полужирный, подчеркнутый).

## Функции

### `_color_text`

```python
def _color_text(text: str, text_color: str = "", bg_color: str = "", font_style: str = "") -> str:
    """Применяет цвет, фон и стиль шрифта к тексту.

    Эта вспомогательная функция применяет заданные цвет и стили шрифта к данному тексту, используя ANSI escape-коды.

    Args:
        text (str): Текст, к которому нужно применить стили.
        text_color (str, optional): Цвет текста. По умолчанию "".
        bg_color (str, optional): Цвет фона. По умолчанию "".
        font_style (str, optional): Стиль шрифта. По умолчанию "".

    Returns:
        str: Стилизованный текст.
    """
    return f"{font_style}{text_color}{bg_color}{text}{RESET}"
```

**Назначение**:
Применяет стили к тексту, используя ANSI escape-коды.

**Параметры**:

*   `text` (str): Текст для стилизации.
*   `text_color` (str, optional): Цвет текста (ключ из `TEXT_COLORS`). По умолчанию "".
*   `bg_color` (str, optional): Цвет фона (ключ из `BG_COLORS`). По умолчанию "".
*   `font_style` (str, optional): Стиль шрифта (ключ из `FONT_STYLES`). По умолчанию "".

**Возвращает**:

*   `str`: Стилизованная строка текста.

**Пример**:

```python
_color_text("Hello, World!", text_color="green", font_style="bold")
```

### `pprint`

```python
def pprint(print_data: Any = None, text_color: str = "white", bg_color: str = "", font_style: str = "") -> None:
    """Форматированный вывод данных с возможностью задания цвета, фона и стиля шрифта.

    Эта функция форматирует входные данные в зависимости от их типа и выводит их в консоль. Данные выводятся с необязательным
    цветом текста, цветом фона и стилем шрифта на основе указанных параметров. Функция может обрабатывать словари,
    списки, строки и пути к файлам.

    Args:
        print_data (Any, optional): Данные для вывода. Может быть типа None, dict, list, str или Path. По умолчанию None.
        text_color (str, optional): Цвет текста. По умолчанию 'white'. См. TEXT_COLORS.
        bg_color (str, optional): Цвет фона. По умолчанию '' (нет цвета фона). См. BG_COLORS.
        font_style (str, optional): Стиль шрифта. По умолчанию '' (нет стиля шрифта). См. FONT_STYLES.

    Returns:
        None

    Raises:
        Exception: Если тип данных не поддерживается или возникает ошибка во время вывода.
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

**Назначение**:
Форматированный вывод данных с возможностью стилизации.

**Параметры**:

*   `print_data` (Any, optional): Данные для вывода. Может быть `None`, `dict`, `list`, `str` или `Path`. По умолчанию `None`.
*   `text_color` (str, optional): Цвет текста (ключ из `TEXT_COLORS`). По умолчанию "white".
*   `bg_color` (str, optional): Цвет фона (ключ из `BG_COLORS`). По умолчанию "".
*   `font_style` (str, optional): Стиль шрифта (ключ из `FONT_STYLES`). По умолчанию "".

**Возвращает**:

*   `None`

**Как работает функция**:

1.  Проверяет, переданы ли данные для вывода. Если `print_data` равен `None`, функция завершается.
2.  Определяет цвет текста, цвет фона и стиль шрифта на основе переданных параметров и словарей `TEXT_COLORS`, `BG_COLORS` и `FONT_STYLES`. Если передан некорректный ключ, используется значение по умолчанию.
3.  В блоке `try` проверяет тип данных `print_data` и выполняет соответствующие действия:
    *   Если это словарь (`dict`), преобразует его в JSON-строку с отступами и выводит с применением стилей.
    *   Если это список (`list`), выводит каждый элемент списка с применением стилей.
    *   Если это строка (`str`) или путь (`Path`) к файлу, проверяет расширение файла и выводит сообщение о поддержке только для `.csv` и `.xls` файлов.
    *   В противном случае выводит строковое представление данных с применением стилей.
4.  В блоке `except` перехватывает исключения, которые могут возникнуть во время вывода, и выводит сообщение об ошибке красным цветом.

**Примеры**:

```python
pprint({"name": "Alice", "age": 30}, text_color="green")
```

```python
pprint(["apple", "banana", "cherry"], text_color="blue", font_style="bold")
```

```python
pprint("text example", text_color="yellow", bg_color="bg_red", font_style="underline")
```