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
                dict | None: Описание возващаемого значения. Возвращает словарь или `None`.
    
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
except Exception as ex:
    print(_color_text(f"Error: {ex}", text_color=TEXT_COLORS["red"]))
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END

if name == 'main':
pprint({"name": "Alice", "age": 30}, text_color="green")
```

## \file /src/utils/image.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для работы с изображениями.
===============================================================
Модуль предоставляет асинхронные функции для скачивания, сохранения и обработки изображений.
Включает в себя функциональность сохранения изображений из URL, сохранения данных изображения в файлы,
получения данных изображения, поиска случайных изображений в каталогах, добавления водяных знаков, изменения размера
и преобразования форматов изображений.

 .. module:: src.utils.image
"""

### 1. **Блок-схема**

```mermaid
graph LR
    A[Начало] --> B{Функция вызвана?};
    B -- Да --> C{Определить функцию};
    B -- Нет --> Z[Конец];

    subgraph save_image_from_url_async
        C --> D[Скачать изображение по URL асинхронно];
        D --> E{Успешно скачано?};
        E -- Да --> F[Сохранить изображение асинхронно];
        E -- Нет --> G[Логировать ошибку];
        F --> H{Успешно сохранено?};
        H -- Да --> I[Вернуть путь к сохраненному файлу];
        H -- Нет --> J[Логировать ошибку];
        I --> K[Конец save_image_from_url_async];
        J --> K
        G --> K
    end

    subgraph save_image
        L[Получить данные изображения и имя файла] --> M[Создать родительские директории при необходимости];
        M --> N[Открыть BytesIO для работы с данными в памяти];
        N --> O[Открыть изображение с помощью PIL];
        O --> P[Сохранить изображение в BytesIO];
        P --> Q[Записать данные из BytesIO в файл];
        Q --> R[Проверить, создан ли файл и не пустой ли он];
        R -- Да --> S[Вернуть путь к сохраненному файлу];
        R -- Нет --> T[Логировать ошибку];
        S --> U[Конец save_image];
        T --> U;
    end

    subgraph save_image_async
        V[Получить данные изображения и имя файла] --> W[Создать родительские директории асинхронно];
        W --> X[Открыть файл для записи асинхронно];
        X --> Y[Записать данные изображения в файл асинхронно];
        Y --> BB[Проверить, создан ли файл и не пустой ли он асинхронно];
        BB -- Да --> CC[Вернуть путь к сохраненному файлу];
        BB -- Нет --> DD[Логировать ошибку];
        CC --> EE[Конец save_image_async];
        DD --> EE;
    end
    
    subgraph get_image_bytes
        FF[Получить путь к изображению] --> GG[Открыть изображение с помощью PIL];
        GG --> HH[Создать BytesIO для хранения данных];
        HH --> II[Сохранить изображение в формате JPEG в BytesIO];
        II --> JJ[Вернуть BytesIO или его содержимое в виде байтов];
        JJ --> KK[Конец get_image_bytes];
    end
    
    subgraph get_raw_image_data
        LL[Получить имя файла] --> MM[Проверить, существует ли файл];
        MM -- Да --> NN[Прочитать байты файла];
        MM -- Нет --> OO[Логировать, что файл не существует и вернуть None];
        NN --> PP[Вернуть байты файла];
        OO --> PP;
        PP --> QQ[Конец get_raw_image_data];
    end

    subgraph random_image
        RR[Получить путь к директории] --> SS[Найти все файлы изображений в директории и поддиректориях];
        SS --> TT{Найдены ли изображения?};
        TT -- Да --> UU[Выбрать случайное изображение];
        TT -- Нет --> VV[Логировать отсутствие изображений и вернуть None];
        UU --> WW[Вернуть путь к случайному изображению];
        VV --> WW;
        WW --> XX[Конец random_image];
    end
    
    subgraph add_text_watermark
        YY[Получить путь к изображению и текст водяного знака] --> ZZ[Открыть изображение с помощью PIL и конвертировать в RGBA];
        ZZ --> AAA[Создать прозрачный слой для водяного знака];
        AAA --> BBB[Определить размер шрифта на основе размера изображения];
        BBB --> CCC[Загрузить шрифт (Arial или стандартный)];
        CCC --> DDD[Определить размеры текста водяного знака];
        DDD --> EEE[Рассчитать позицию для текста водяного знака];
        EEE --> FFF[Нарисовать текст на прозрачном слое];
        FFF --> GGG[Объединить изображение и водяной знак];
        GGG --> HHH[Сохранить изображение с водяным знаком];
        HHH --> III[Вернуть путь к изображению с водяным знаком];
        III --> JJJ[Конец add_text_watermark];
    end

    subgraph add_image_watermark
        KKK[Получить пути к основному изображению и изображению водяного знака] --> LLL[Открыть основное изображение с помощью PIL];
        LLL --> MMM[Открыть изображение водяного знака и конвертировать в RGBA];
        MMM --> NNN[Изменить размер водяного знака (8% от ширины основного изображения)];
        NNN --> OOO[Определить позицию для размещения водяного знака в нижнем правом углу];
        OOO --> PPP[Создать новый прозрачный слой для объединения изображений];
        PPP --> QQQ[Вставить основное изображение на новый слой];
        QQQ --> RRR[Вставить водяной знак поверх основного изображения];
        RRR --> SSS[Проверить режим изображения и конвертировать прозрачный слой при необходимости];
        SSS --> TTT[Сохранить итоговое изображение с водяным знаком];
        TTT --> UUU[Вернуть путь к сохраненному изображению];
        UUU --> VVV[Конец add_image_watermark];
    end

    subgraph resize_image
        WWW[Получить путь к изображению и желаемый размер] --> XXX[Открыть изображение с помощью PIL];
        XXX --> YYY[Изменить размер изображения];
        YYY --> ZZZ[Сохранить измененное изображение];
        ZZZ --> AAAA[Вернуть путь к измененному изображению];
        AAAA --> BBBB[Конец resize_image];
    end

    subgraph convert_image
        CCCC[Получить путь к изображению и желаемый формат] --> DDDD[Открыть изображение с помощью PIL];
        DDDD --> EEEE[Сохранить изображение в новом формате];
        EEEE --> FFFF[Вернуть путь к конвертированному изображению];
        FFFF --> GGGG[Конец convert_image];
    end

    subgraph process_images_with_watermark
        HHHH[Получить путь к папке с изображениями и путь к водяному знаку] --> IIII{Является ли путь к папке директорией?};
        IIII -- Да --> JJJJ[Создать выходную директорию, если она не существует];
        IIII -- Нет --> KKKK[Залогировать, что папка не существует и закончить выполнение];
        JJJJ --> LLLL[Итерироваться по файлам в папке];
        LLLL --> MMMM{Является ли файл изображением?};
        MMMM -- Да --> NNNN[Определить путь для сохранения изображения с водяным знаком в выходной директории];
        MMMM -- Нет --> LLLL;
        NNNN --> OOOO[Добавить водяной знак на изображение];
        OOOO --> LLLL;
        KKKK --> PPPP[Конец process_images_with_watermark];
    end
```

### 2. **Диаграмма**

```mermaid
graph TD
    subgraph src.utils.image
    A[save_image_from_url_async] --> B[save_image_async]
    C[save_image_async]
    D[save_image]
    E[get_image_bytes]
    F[get_raw_image_data]
    G[random_image]
    H[add_text_watermark]
    I[add_image_watermark]
    J[resize_image]
    K[convert_image]
    L[process_images_with_watermark] --> I
    end
    
    A --> aiohttp
    C --> aiofiles
    D --> PIL
    E --> PIL
    H --> PIL
    I --> PIL
    J --> PIL
    K --> PIL
    L --> pathlib
    G --> pathlib
    D --> pathlib
    C --> pathlib
    F --> pathlib
    H --> pathlib
    I --> pathlib
    J --> pathlib
    K --> pathlib
    L --> pathlib
    A --> logger
    C --> logger
    D --> logger
    E --> logger
    F --> logger
    G --> logger
    H --> logger
    I --> logger
    J --> logger
    K --> logger
    L --> logger
    
    style src.utils.image fill:#f9f,stroke:#333,stroke-width:2px
    
    subgraph External Libraries
        aiohttp
        aiofiles
        PIL[PIL (Image, ImageDraw, ImageFont)]
        pathlib
        logger[src.logger.logger]
    end
```

**Зависимости:**

- **aiohttp**: Используется в `save_image_from_url_async` для асинхронной загрузки изображений из сети.
- **aiofiles**: Используется в `save_image_async` для асинхронной записи изображений в файлы.
- **PIL (Pillow)**: Используется для открытия, обработки и сохранения изображений.  Включает модули `Image`, `ImageDraw` и `ImageFont`.
  - `Image`: Основной модуль для работы с изображениями.
  - `ImageDraw`: Используется для добавления графических элементов, таких как водяные знаки.
  - `ImageFont`: Используется для работы со шрифтами при добавлении текстовых водяных знаков.
- **pathlib**: Используется для работы с путями к файлам и директориям.
- **logger (src.logger.logger)**: Используется для логирования ошибок и предупреждений.

### 3. **Объяснение**

#### **Импорты:**

- `aiohttp`: Асинхронная HTTP клиентская библиотека, используется для загрузки изображений из URL.
- `aiofiles`: Асинхронная библиотека для работы с файлами, используется для асинхронного сохранения изображений.
- `asyncio`: Библиотека для написания конкурентного кода с использованием синтаксиса async/await.
- `random`: Модуль для генерации случайных чисел, используется для выбора случайного изображения.
- `pathlib`: Модуль для представления путей к файлам и директориям как объектов.
- `typing`: Модуль для аннотации типов.
- `io`: Модуль для работы с потоками ввода-вывода.
- `PIL (Pillow)`: Библиотека для работы с изображениями.
- `src.logger.logger`: Пользовательский модуль логирования.

#### **Классы:**

- `ImageError`: Пользовательское исключение для ошибок, связанных с обработкой изображений.

#### **Функции:**

- `save_image_from_url_async(image_url: str, filename: Union[str, Path]) -> Optional[str]`:
  - **Аргументы:**
    - `image_url` (str): URL изображения.
    - `filename` (Union[str, Path]): Имя файла для сохранения изображения.
  - **Возвращаемое значение:** Путь к сохраненному файлу (str) или None в случае ошибки.
  - **Назначение:** Асинхронно загружает изображение из URL и сохраняет его локально.
  - **Пример:**

```python
image_url = "http://example.com/image.jpg"
filename = "path/to/save/image.jpg"
saved_path = await save_image_from_url_async(image_url, filename)
if saved_path:
    print(f"Изображение успешно сохранено по пути: {saved_path}")
else:
    print("Не удалось сохранить изображение.")
```

- `save_image(image_data: bytes, file_name: str | Path, format: str = 'PNG') -> Optional[str]`:
  - **Аргументы:**
    - `image_data` (bytes): Бинарные данные изображения.
    - `file_name` (Union[str, Path]): Имя файла для сохранения изображения.
    - `format` (str): Формат изображения (по умолчанию 'PNG').
  - **Возвращаемое значение:** Путь к сохраненному файлу (str) или None в случае ошибки.
  - **Назначение:** Сохраняет данные изображения в файл в указанном формате.
  - **Пример:**

```python
image_data = b"..."  # some image bytes
file_name = "path/to/save/image.png"
saved_path = save_image(image_data, file_name)
if saved_path:
    print(f"Изображение успешно сохранено по пути: {saved_path}")
else:
    print("Не удалось сохранить изображение.")
```

- `save_image_async(image_data: bytes, file_name: str | Path, format: str = 'PNG') -> Optional[str]`:
  - **Аргументы:**
    - `image_data` (bytes): Бинарные данные изображения.
    - `file_name` (Union[str, Path]): Имя файла для сохранения изображения.
    - `format` (str): Формат изображения (по умолчанию 'PNG').
  - **Возвращаемое значение:** Путь к сохраненному файлу (str) или None в случае ошибки.
  - **Назначение:** Асинхронно сохраняет данные изображения в файл в указанном формате.
  - **Пример:**

```python
image_data = b"..."  # some image bytes
file_name = "path/to/save/image.png"
saved_path = await save_image_async(image_data, file_name)
if saved_path:
    print(f"Изображение успешно сохранено по пути: {saved_path}")
else:
    print("Не удалось сохранить изображение.")
```

- `get_image_bytes(image_path: Path, raw: bool = True) -> Optional[BytesIO | bytes]`:
  - **Аргументы:**
    - `image_path` (Path): Путь к файлу изображения.
    - `raw` (bool): Если True, возвращает BytesIO объект; иначе возвращает bytes. По умолчанию True.
  - **Возвращаемое значение:** BytesIO объект или байты изображения в формате JPEG, или None в случае ошибки.
  - **Назначение:** Читает изображение и возвращает его байты в формате JPEG.
  - **Пример:**

```python
image_path = Path("path/to/image.jpg")
image_bytes = get_image_bytes(image_path)
if image_bytes:
    print(f"Изображение успешно прочитано в байты.")
else:
    print("Не удалось прочитать изображение.")
```

- `get_raw_image_data(file_name: Union[str, Path]) -> Optional[bytes]`:
  - **Аргументы:**
    - `file_name` (Union[str, Path]): Имя файла.
  - **Возвращаемое значение:** Бинарные данные файла или None, если файл не существует или произошла ошибка.
  - **Назначение:** Получает бинарные данные файла.
  - **Пример:**