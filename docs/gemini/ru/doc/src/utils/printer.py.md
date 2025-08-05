# Модуль `src.utils.printer`

## Обзор

Модуль `src.utils.printer` предоставляет функции для красивого вывода данных в удобочитаемом формате с возможностью применения текстовых стилей, включая цвет, фон и стиль шрифта. 

## Подробней

Модуль `src.utils.printer`  содержит функции для форматирования различных типов данных, таких как словари, списки, строки и пути к файлам, перед выводом в консоль. 

## Функции

### `_color_text`

**Назначение**: Функция `_color_text` применяется для  стилизации текста с использованием ANSI-кодов. 

**Параметры**:

- `text` (str): Текст для стилизации.
- `text_color` (str, optional): Цвет текста. По умолчанию `""` (без цвета).
- `bg_color` (str, optional): Цвет фона. По умолчанию `""` (без цвета фона).
- `font_style` (str, optional): Стиль шрифта. По умолчанию `""` (без стиля шрифта).

**Возвращает**:

- `str`: Стилизованный текст в виде строки.

**Примеры**:

```python
>>> _color_text("Hello, World!", text_color="green", font_style="bold")
'\033[1m\033[32mHello, World!\033[0m'
```

### `pprint`

**Назначение**: Функция `pprint`  обеспечивает красивый вывод данных в консоль с использованием опциональных стилей: цвет, фон и стиль шрифта.

**Параметры**:

- `print_data` (Any, optional): Данные для вывода. Допустимые типы: `None`, `dict`, `list`, `str` или `Path`. По умолчанию `None`.
- `text_color` (str, optional): Цвет текста. По умолчанию `white`.  Доступные цвета: `red`, `green`, `blue`, `yellow`, `white`, `cyan`, `magenta`, `light_gray`, `dark_gray`, `light_red`, `light_green`, `light_blue`, `light_yellow`.
- `bg_color` (str, optional): Цвет фона. По умолчанию `""` (без цвета фона). Доступные цвета: `bg_red`, `bg_green`, `bg_blue`, `bg_yellow`, `bg_white`, `bg_cyan`, `bg_magenta`, `bg_light_gray`, `bg_dark_gray`, `bg_light_red`, `bg_light_green`, `bg_light_blue`, `bg_light_yellow`.
- `font_style` (str, optional): Стиль шрифта. По умолчанию `""` (без стиля шрифта). Доступные стили: `bold`, `underline`.

**Возвращает**:

- `None`

**Вызывает исключения**:

- `Exception`: Если тип данных не поддерживается или возникает ошибка во время вывода.

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
```

**Как работает функция**:

1. Функция `pprint`  проверяет тип данных, переданных в `print_data`. 
2. Если `print_data` - это словарь, функция преобразует его в строку с помощью `json.dumps` с отступами для улучшения читаемости и выводит результат с использованием `_color_text`.
3. Если `print_data` - это список, функция итерирует по нему, выводит каждый элемент с использованием `_color_text`.
4. Если `print_data` - это строка или путь к файлу (`Path`), функция проверяет, является ли это файл, и если да, то выводит сообщение о поддержке или неподдержке чтения файла.
5. В противном случае, функция выводит строковое представление `print_data` с использованием `_color_text`. 
6. Функция обрабатывает ошибки, возникающие во время вывода, и выводит сообщение об ошибке с использованием `_color_text` в красном цвете.

## Примеры

```python
# Вывод словаря в зеленом цвете
pprint({"name": "Alice", "age": 30}, text_color="green")

# Вывод списка с синим цветом и жирным шрифтом
pprint(["apple", "banana", "cherry"], text_color="blue", font_style="bold")

# Вывод строки с желтым цветом, красным фоном и подчеркиванием
pprint("text example", text_color="yellow", bg_color="bg_red", font_style="underline")
```