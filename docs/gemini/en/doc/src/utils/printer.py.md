# Модуль `src.utils.printer`

## Обзор

Модуль `src.utils.printer` предоставляет функции для вывода данных в удобочитаемом формате с возможностью применения стилей текста, включая цвет, фон и стиль шрифта.

## Детали

Модуль реализует функцию `pprint`, которая принимает на вход данные любого типа (словарь, список, строка, путь к файлу) и выводит их в консоль в отформатированном виде. Дополнительно функция `pprint` позволяет задать цвет текста, цвет фона и стиль шрифта. 

## Классы

### `None`

#### Description

Модуль не содержит классов.

## Функции

### `_color_text`

**Purpose**: Применяет цвет, фон и стиль шрифта к тексту.

**Parameters**:

- `text` (str): Текст, к которому нужно применить стили.
- `text_color` (str, optional): Цвет текста. По умолчанию - пустая строка, что означает отсутствие цвета.
- `bg_color` (str, optional): Цвет фона. По умолчанию - пустая строка, что означает отсутствие цвета фона.
- `font_style` (str, optional): Стиль шрифта. По умолчанию - пустая строка, что означает отсутствие стиля шрифта.

**Returns**:

- `str`: Текст с примененными стилями.

**Raises Exceptions**:

- `None`

**Examples**:

```python
>>> _color_text("Hello, World!", text_color="green", font_style="bold")
'\033[1m\033[32mHello, World!\033[0m'
```

**How the Function Works**:

Функция `_color_text` принимает на вход текст и опциональные параметры цвета текста, фона и стиля шрифта. Используя ANSI-последовательности, функция применяет заданные стили к тексту и возвращает отформатированную строку.

### `pprint`

**Purpose**: Выводит данные в отформатированном виде с возможностью применения цвета, фона и стиля шрифта.

**Parameters**:

- `print_data` (Any, optional): Данные, которые нужно вывести. Может быть `None`, словарь, список, строка или путь к файлу. По умолчанию - `None`.
- `text_color` (str, optional): Цвет текста. По умолчанию - 'white'. См. :ref:`TEXT_COLORS`.
- `bg_color` (str, optional): Цвет фона. По умолчанию - '' (отсутствует). См. :ref:`BG_COLORS`.
- `font_style` (str, optional): Стиль шрифта. По умолчанию - '' (отсутствует). См. :ref:`FONT_STYLES`.

**Returns**:

- `None`

**Raises Exceptions**:

- `Exception`: Если тип данных не поддерживается или при печати возникла ошибка.

**Examples**:

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
```

**How the Function Works**:

Функция `pprint` принимает на вход данные и опциональные параметры цвета текста, фона и стиля шрифта. 

-  В зависимости от типа данных функция выводит их в отформатированном виде:
    - Если `print_data` - словарь, функция выводит его в формате JSON с отступом.
    - Если `print_data` - список, функция выводит каждый элемент списка на отдельной строке.
    - Если `print_data` - строка или путь к файлу, функция проверяет, является ли файл доступным. 
        -  Если файл доступен, функция выводит сообщение о поддержке файлов .csv, .xls и .xlsx.
        -  Если тип файла не поддерживается, функция выводит сообщение об ошибке.
    -  В противном случае, функция выводит `print_data` в виде строки.

-  Функция `pprint` использует функцию `_color_text` для применения заданных стилей текста.

## Parameter Details

- `text_color` (str):  Цвет текста. По умолчанию - 'white'. Доступные цвета: 
    - `red`, `green`, `blue`, `yellow`, `white`, `cyan`, `magenta`, `light_gray`, `dark_gray`, `light_red`, `light_green`, `light_blue`, `light_yellow`.
- `bg_color` (str):  Цвет фона. По умолчанию - '' (отсутствует). Доступные цвета:
    - `bg_red`, `bg_green`, `bg_blue`, `bg_yellow`, `bg_white`, `bg_cyan`, `bg_magenta`, `bg_light_gray`, `bg_dark_gray`, `bg_light_red`, `bg_light_green`, `bg_light_blue`, `bg_light_yellow`.
- `font_style` (str):  Стиль шрифта. По умолчанию - '' (отсутствует). Доступные стили: 
    - `bold`, `underline`.

## Examples

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
```