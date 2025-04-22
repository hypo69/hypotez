### **Системные инструкции для обработки кода проекта `hypotez`**

=========================================================================================

Описание функциональности и правил для генерации, анализа и улучшения кода. Направлено на обеспечение последовательного и читаемого стиля кодирования, соответствующего требованиям.

---

### **Основные принципы**

#### **1. Общие указания**:
- Соблюдай четкий и понятный стиль кодирования.
- Все изменения должны быть обоснованы и соответствовать установленным требованиям.

#### **2. Комментарии**:
- Используй `#` для внутренних комментариев.
- В комментариях избегай использования местоимений, таких как *«делаем»*, *«переходим»*, *«возващам»*, *«возващам»*, *«отправяем»* и т. д.. Вмсто этого используй точные термины, такие как *«извлеизвлечение»*, *«проверка»*, *«выполннение»*, *«замена»*, *«вызов»*, *«Функця выпоняет»*,*«Функця изменяет значение»*, *«Функця вызывает»*,*«отправка»*
Пример:
```python
# Неправильно:
def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
    # Получаем значение параметра
    ...
# Правильно:

def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
    # Функция извлекает значение параметра
    ...
# Неправильно:
if not process_directory.exists():
    logger.error(f"Директория не существует: {process_directory}")
    continue  # Переходим к следующей директории, если текущая не существует

if not process_directory.is_dir():
    logger.error(f"Это не директория: {process_directory}", None, False)
    continue  # Переходим к следующей директории, если текущая не является директорией
# Правильно:

if not process_directory.exists():
    logger.error(f"Директория не существует: {process_directory}")
    continue  # Переход к следующей директории, если текущая не существует
if not process_directory.is_dir():
    logger.error(f"Это не директория: {process_directory}", None, False)
    continue  # Переходим к следующей директории, если текущая не является директорией

```
- Документация всех функций, методов и классов должна следовать такому формату: 
    ```python
        def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
            """ 
            Args:
                param (str): Описание параметра `param`.
                param1 (Optional[str | dict | str], optional): Описание параметра `param1`. По умолчанию `None`.
    
            Returns:
                dict | None: Описание возвращаемого значения. Возвращает словарь или `None`.
    
            Raises:
                SomeError: Описание ситуации, в которой возникает исключение `SomeError`.

            Ехаmple:
                >>> function('param', 'param1')
                {'param': 'param1'}
            """
    ```
- Комментарии и документация должны быть четкими, лаконичными и точными.


### **3. Заголовок файла**:
Обязательно оставляй строки 
```python
## \file path/to/file
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
```
и
```
"""
...
```rst
 .. module:: src.utils.string.html_simplification
 ```
"""
```
если они есть. Если нет - добавляй.
Пример:
## \file /src/utils/string/html_simplification.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для очистки HTML-тегов из текста и упрощения HTML-кода.
===============================================================
Модуль минимизирует HTML-код, удаляет теги и атрибуты, а также обрабатывает
специальные случаи, такие как скрипты, стили и комментарии.
Использует BeautifulSoup для надежного парсинга HTML.

Зависимости:
    - beautifulsoup4 (pip install beautifulsoup4)
    - lxml (опционально, для более быстрого парсинга: pip install lxml)

 .. module:: src.utils.string.html_simplification
"""

#### **4. Форматирование кода**:
- Используй одинарные кавычки. `a:str = 'value'`, `print('Hello World!')`;
- Добавляй пробелы вокруг операторов. Например, `x = 5`;
- Все параметры должны быть аннотированы типами. `def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:`;
- Не используй `Union`. Вместо этого используй `|`.
- Не используй термин `Product`, только `товар`

#### **5. Логирование**:
- Для логгирования Всегда Используй модуль `logger` из `src.logger.logger`.
- Ошибки должны логироваться с использованием `logger.error`.
Пример:
    ```python
        try:
            ...
        except Exception as ex:
            logger.error('Error while processing data', ех, exc_info=True)
    ```
#### **6. Не используй `Union[]` в коде. Вместо него используй `|`
Например:
```python
x: str | int ...
```

#### **7. Не используй глобальные переменные. Если есть надобность - то поределяй их в классе `Config`.
Пример:

- Неправильно:
```python

state:int = 'global'

def func():
    print(state)

```
- Правильно:
```python

class Config:
    state:int = 'global'

def func():
    print(Config.state)

```

#### **8. Не используй `self` в методах класса. Вместо него используй `cls`.
#### **9. Всегда объявляй переменные вначале функции. Не объявляй их в середине функции.
Пример:
```python
def func():
    # Неправильно
    if condition:
        x = 5
        y = 10
    else:
        x = 20
        y = 30
    # Правильно
    x = None
    y = None
    if condition:
        x = 5
        y = 10
    else:
        x = 20
        y = 30
```
---

### **Основные требования**:

#### **1. Формат ответов в Markdown**:
- Все ответы должны быть выполнены в формате **Markdown**.

#### **2. Формат комментариев**:
- Используй указанный стиль для комментариев и документации в коде.
- Пример:

```python
from typing import Generator, Optional, List
from pathlib import Path


def read_text_file(
    file_path: str | Path,
    as_list: bool = False,
    extensions: Optional[List[str]] = None,
    chunk_size: int = 8192,
) -> Generator[str, None, None] | str | None:
    """
    Считывает содержимое файла (или файлов из каталога) с использованием генератора для экономии памяти.

    Args:
        file_path (str | Path): Путь к файлу или каталогу.
        as_list (bool): Если `True`, возвращает генератор строк.
        extensions (Optional[List[str]]): Список расширений файлов для чтения из каталога.
        chunk_size (int): Размер чанков для чтения файла в байтах.

    Returns:
        Generator[str, None, None] | str | None: Генератор строк, объединенная строка или `None` в случае ошибки.

    Raises:
        Exception: Если возникает ошибка при чтении файла.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('example.txt')
        >>> content = read_text_file(file_path)
        >>> if content:
        ...    print(f'File content: {content[:100]}...')
        File content: Example text...
    """
    ...
```
- Всегда делай подробные объяснения в комментариях. Избегай расплывчатых терминов, 
- таких как *«получить»* или *«делать»*
-  . Вместо этого используйте точные термины, такие как *«извлечь»*, *«проверить»*, *«выполнить»*.
- Вместо: *«получаем»*, *«возвращаем»*, *«преобразовываем»* используй имя объекта *«функция получае»*, *«переменная возвращает»*, *«код преобразовывает»* 
- Комментарии должны непосредственно предшествовать описываемому блоку кода и объяснять его назначение.

#### **3. Пробелы вокруг операторов присваивания**:
- Всегда добавляйте пробелы вокруг оператора `=`, чтобы повысить читаемость.
- Примеры:
  - **Неправильно**: `x=5`
  - **Правильно**: `x = 5`

#### **4. Использование `j_loads` или `j_loads_ns`**:
- Для чтения JSON или конфигурационных файлов замените стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.
- Пример:

```python
# Неправильно:
with open('config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Правильно:
data = j_loads('config.json')
```

#### **5. Сохранение комментариев**:
- Все существующие комментарии, начинающиеся с `#`, должны быть сохранены без изменений в разделе «Улучшенный код».
- Если комментарий кажется устаревшим или неясным, не изменяйте его. Вместо этого отметьте его в разделе «Изменения».

#### **6. Обработка `...` в коде**:
- Оставляйте `...` как указатели в коде без изменений.
- Не документируйте строки с `...`.
```

#### **7. Аннотации**
Для всех переменных должны быть определены аннотации типа. 
Для всех функций все входные и выходные параметры аннотириваны
Для все параметров должны быть аннотации типа.


### **8. webdriver**
В коде используется webdriver. Он импртируется из модуля `webdriver` проекта `hypotez`
```python
from src.webdirver import Driver, Chrome, Firefox, Playwright, ...
driver = Driver(Firefox)

Пoсле чего может использоваться как

close_banner = {
  "attribute": null,
  "by": "XPATH",
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "click()",
  "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}

result = driver.execute_locator(close_banner)

#### **9. Не используй `Union[]` в коде. Вместо него используй `|`
Например:
```python
x: str | int ...
```

#### **10. print - это моя встроенная функция.
from src.utils.printer import pprint as print


Вот она:

\file /src/utils/printer.py
-- coding: utf-8 --

#! .pyenv/bin/python3

"""
.. module::  src.utils
:platform: Windows, Unix
:synopsis: Utility functions for pretty printing and text styling.

This module provides functions to print data in a human-readable format with optional text styling, including color, background, and font styles.
"""

import json
import csv
import pandas as pd
from pathlib import Path
from typing import Any
from pprint import pprint as pretty_print

ANSI escape codes

RESET = "\033[0m"

TEXT_COLORS = {
"red": "\033[31m",
"green": "\033[32m",
"blue": "\033[34m",
"yellow": "\033[33m",
"white": "\033[37m",
"cyan": "\033[36m",
"magenta": "\033[35m",
"light_gray": "\033[37m",
"dark_gray": "\033[90m",
"light_red": "\033[91m",
"light_green": "\033[92m",
"light_blue": "\033[94m",
"light_yellow": "\033[93m",
}

Background colors mapping

BG_COLORS = {
"bg_red": "\033[41m",
"bg_green": "\033[42m",
"bg_blue": "\033[44m",
"bg_yellow": "\033[43m",
"bg_white": "\033[47m",
"bg_cyan": "\033[46m",
"bg_magenta": "\033[45m",
"bg_light_gray": "\033[47m",
"bg_dark_gray": "\033[100m",
"bg_light_red": "\033[101m",
"bg_light_green": "\033[102m",
"bg_light_blue": "\033[104m",
"bg_light_yellow": "\033[103m",
}

FONT_STYLES = {
"bold": "\033[1m",
"underline": "\033[4m",
}

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
return f"{font_style}{text_color}{bg_color}{text}{RESET}"


def pprint(print_data: Any = None, text_color: str = "white", bg_color: str = "", font_style: str = "") -> None:
"""Pretty prints the given data with optional color, background, and font style.

This function formats the input data based on its type and prints it to the console. The data is printed with optional 
text color, background color, and font style based on the specified parameters. The function can handle dictionaries, 
lists, strings, and file paths.

:param print_data: The data to be printed. Can be of type ``None``, ``dict``, ``list``, ``str``, or ``Path``.
:param text_color: The color to apply to the text. Default is 'white'. See :ref:`TEXT_COLORS`.
:param bg_color: The background color to apply to the text. Default is '' (no background color). See :ref:`BG_COLORS`.
:param font_style: The font style to apply to the text. Default is '' (no font style). See :ref:`FONT_STYLES`.
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
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END

if name == 'main':
pprint({"name": "Alice", "age": 30}, text_color="green")
```

## \file /src/utils/convertors/_experiments/webp2png.py

# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.utils.convertors._experiments
	:platform: Windows, Unix
	:synopsis:

"""

"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""

""" module: src.utils.convertors._experiments """

""" This module converts WebP images to PNG format.

It retrieves WebP files from a specified directory and converts them to PNG format,
saving the output to another directory. The conversion is handled by the `webp2png` function.
"""

import header
from pathlib import Path
from src import gs
from src.utils.convertors.webp2png import webp2png
from src.utils.file import get_filenames


def convert_images(webp_dir: Path, png_dir: Path) -> None:
    """ Convert all WebP images in the specified directory to PNG format.

    Args:
        webp_dir (Path): Directory containing the source WebP images.
        png_dir (Path): Directory to save the converted PNG images.

    Example:
        convert_images(
            gs.path.google_drive / 'emil' / 'raw_images_from_openai',
            gs.path.google_drive / 'emil' / 'converted_images'
        )
    """
    webp_files: list = get_filenames(webp_dir)

    for webp in webp_files:
        png = png_dir / f"{Path(webp).stem}.png"  # Use `stem` to get the file name without extension
        webp_path = webp_dir / webp
        result = webp2png(webp_path, png)
        print(result)


if __name__ == '__main__':
    # Define the directories for WebP and PNG images
    webp_dir = gs.path.google_drive / 'kazarinov' / 'raw_images_from_openai'
    png_dir = gs.path.google_drive / 'kazarinov' / 'converted_images'
    print(f"from: {webp_dir=}\nto:{png_dir=}")
    # Run the conversion
    convert_images(webp_dir, png_dir)
```

### 1. **Блок-схема**:

```mermaid
graph TD
    A[Начало] --> B{Определить каталоги webp_dir и png_dir};
    B --> C{Вызов convert_images(webp_dir, png_dir)};
    C --> D{Вызов get_filenames(webp_dir)};
    D --> E[Получить список файлов WebP];
    E --> F{Цикл по каждому файлу WebP в списке};
    F --> G{Создать путь для PNG файла};
    G --> H{Вызов webp2png(webp_path, png)};
    H --> I[Преобразование WebP в PNG];
    I --> J{Вывод результата преобразования};
    J --> K{Конец цикла?};
    K -- Нет --> F;
    K -- Да --> L[Конец];
```

### 2. **Диаграмма**:

```mermaid
flowchart TD
    subgraph src.utils.convertors._experiments
        A[<code>webp2png.py</code><br>Конвертация WebP в PNG]
    end

    B[<code>header.py</code><br>Определение корня проекта]
    C[<code>src/__init__.py</code><br>Инициализация пакета src]
    D[<code>src.utils.convertors.webp2png.py</code><br>Функция webp2png]
    E[<code>src.utils.file.py</code><br>Функция get_filenames]
    F[<code>pathlib.Path</code><br>Работа с путями к файлам]

    A --> B
    A --> C
    A --> D
    A --> E
    A --> F

    style A fill:#f9f,stroke:#333,stroke-width:2px
```

```mermaid
flowchart TD
    Start --> Header[<code>header.py</code><br> Determine Project Root]

    Header --> import[Import Global Settings: <br><code>from src import gs</code>]
```

**Объяснение зависимостей:**

*   **header.py**: Используется для определения корня проекта и настройки путей. Без него не будет корректно работать импорт `gs` из пакета `src`.
*   **src/\_\_init\_\_.py**: Инициализирует пакет `src`, что позволяет импортировать глобальные настройки (`gs`).
*   **src.utils.convertors.webp2png.py**: Содержит функцию `webp2png`, которая выполняет преобразование WebP в PNG.
*   **src.utils.file.py**: Содержит функцию `get_filenames`, используемую для получения списка файлов WebP в указанной директории.
*   **pathlib.Path**: Используется для работы с путями к файлам и директориям, что необходимо для определения входных и выходных путей для преобразования.

### 3. **Объяснение**:

#### **Импорты**:

*   `import header`: Импортирует модуль `header`, который, вероятно, содержит логику для определения корневой директории проекта и, возможно, другие настройки.
*   `from pathlib import Path`: Импортирует класс `Path` из модуля `pathlib` для работы с путями к файлам и директориям.
*   `from src import gs`: Импортирует глобальные настройки `gs` из пакета `src`. Вероятно, `gs` содержит пути к директориям и другие глобальные параметры конфигурации.
*   `from src.utils.convertors.webp2png import webp2png`: Импортирует функцию `webp2png` из модуля `src.utils.convertors.webp2png`, которая выполняет фактическое преобразование изображений WebP в PNG.
*   `from src.utils.file import get_filenames`: Импортирует функцию `get_filenames` из модуля `src.utils.file`, которая используется для получения списка файлов в указанной директории.

#### **Функции**:

*   `convert_images(webp_dir: Path, png_dir: Path) -> None`:
    *   Аргументы:
        *   `webp_dir (Path)`: Путь к директории, содержащей исходные изображения WebP.
        *   `png_dir (Path)`: Путь к директории, в которую будут сохранены преобразованные изображения PNG.
    *   Возвращаемое значение: `None` (функция ничего не возвращает).
    *   Назначение: Функция выполняет преобразование всех WebP-изображений в указанной директории в формат PNG и сохраняет их в другую директорию.
    *   Пример:
        ```python
        convert_images(
            gs.path.google_drive / 'emil' / 'raw_images_from_openai',
            gs.path.google_drive / 'emil' / 'converted_images'
        )
        ```
        В этом примере функция вызывается с путями, полученными из глобальных настроек `gs`.

#### **Переменные**:

*   `webp_files: list`: Список файлов WebP, полученный с помощью функции `get_filenames(webp_dir)`.
*   `webp_dir: Path`:  Путь к директории с WebP изображениями, определяется в блоке `if __name__ == '__main__':`.
*   `png_dir: Path`: Путь к директории для сохранения PNG изображений, определяется в блоке `if __name__ == '__main__':`.
*   `webp_path: Path`: Полный путь к конкретному WebP файлу.
*   `png: Path`: Полный путь к PNG файлу, который будет создан.
*   `result`: Результат выполнения функции `webp2png`.

#### **Потенциальные ошибки и области для улучшения**:

1.  **Обработка ошибок**: В коде отсутствует явная обработка ошибок. Например, если функция `webp2png` не сможет преобразовать изображение, программа может завершиться с ошибкой. Рекомендуется добавить блоки `try...except` для обработки возможных исключений.
2.  **Логирование**: Отсутствует логирование процесса преобразования. Было бы полезно добавить логирование для отслеживания успешных и неуспешных преобразований, а также для записи ошибок. Использовать `logger.error` из `src.logger.logger`.
3.  **Проверка существования директорий**: Перед началом преобразования можно добавить проверку существования директорий `webp_dir` и `png_dir`. Если директории не существуют, можно создать их или вывести сообщение об ошибке.
4.  **Параллельное выполнение**: Для ускорения процесса преобразования можно использовать многопоточность или многопроцессорность для параллельного выполнения преобразования нескольких изображений.

#### **Взаимосвязи с другими частями проекта**:

*   Модуль использует глобальные настройки `gs` для получения путей к директориям, что позволяет легко конфигурировать пути к входным и выходным данным.
*   Функция `get_filenames` используется для получения списка файлов, что позволяет повторно использовать эту функцию в других модулях проекта.
*   Функция `webp2png` выполняет фактическое преобразование, и этот модуль служит как orchestrator, координируя процесс преобразования для всех файлов в директории.

```python
import header
from pathlib import Path
from src import gs
from src.utils.convertors.webp2png import webp2png
from src.utils.file import get_filenames
from src.logger.logger import logger

def convert_images(webp_dir: Path, png_dir: Path) -> None:
    """ Convert all WebP images in the specified directory to PNG format.

    Args:
        webp_dir (Path): Directory containing the source WebP images.
        png_dir (Path): Directory to save the converted PNG images.

    Example:
        convert_images(
            gs.path.google_drive / 'emil' / 'raw_images_from_openai',
            gs.path.google_drive / 'emil' / 'converted_images'
        )
    """
    webp_files: list = get_filenames(webp_dir)

    for webp in webp_files:
        png = png_dir / f"{Path(webp).stem}.png"  # Use `stem` to get the file name without extension
        webp_path = webp_dir / webp
        try:
            result = webp2png(webp_path, png)
            logger.info(f"Изображение {webp} успешно преобразовано в {png}")
            print(result)
        except Exception as e:
            logger.error(f"Ошибка при преобразовании {webp} в {png}: {e}", exc_info=True)

if __name__ == '__main__':
    # Define the directories for WebP and PNG images
    webp_dir = gs.path.google_drive / 'kazarinov' / 'raw_images_from_openai'
    png_dir = gs.path.google_drive / 'kazarinov' / 'converted_images'
    print(f"from: {webp_dir=}\nto:{png_dir=}")
    # Run the conversion
    convert_images(webp_dir, png_dir)