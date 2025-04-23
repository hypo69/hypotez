### **Инструкции для генерации документации к коду**

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
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END

if name == 'main':
pprint({"name": "Alice", "age": 30}, text_color="green")
```

### Как использовать асинхронный метод `create_reports_async`
=========================================================================================

Описание
-------------------------
Метод `create_reports_async` создает отчеты в форматах HTML, PDF и DOCX, используя предоставленные данные и настройки. Он запускает асинхронное создание HTML-отчета и, если необходимо, асинхронное создание PDF- и DOCX-отчетов на основе сгенерированного HTML-контента.

Шаги выполнения
-------------------------
1. **Инициализация**: Метод принимает экземпляр `telebot.TeleBot`, `chat_id`, данные (`data`), язык (`lang`) и имя мехирона (`mexiron_name`).
2. **Настройка путей**: Определяет пути для сохранения HTML, PDF и DOCX файлов на основе имени мехирона и языка.
3. **Создание HTML-отчета**: Вызывает асинхронный метод `create_html_report_async` для генерации HTML-контента.
4. **Создание PDF-отчета**: Если `self.if_need_pdf` равен `True`, вызывает асинхронный метод `create_pdf_report_async` для генерации PDF-отчета на основе HTML-контента.
5. **Создание DOCX-отчета**: Если `self.if_need_docx` равен `True`, вызывает асинхронный метод `create_pdf_report_async` (ошибка в коде, должен быть `create_docx_report_async`) для генерации DOCX-отчета.
6. **Возврат результата**: Возвращает `False`, если не удалось создать HTML-контент.

Пример использования
-------------------------

```python
import asyncio
import telebot
from src.endpoints.kazarinov.report_generator.report_generator import ReportGenerator

async def main():
    # Инициализация бота (замените 'YOUR_BOT_TOKEN' на реальный токен)
    bot = telebot.TeleBot('YOUR_BOT_TOKEN')
    chat_id = 123456789  # ID чата, куда будут отправляться отчеты
    data = {
        "products": [
            {"product_id": "123", "product_name": "Товар 1", "specification": "Описание 1", "image_local_saved_path": "path/to/image1.jpg"},
            {"product_id": "456", "product_name": "Товар 2", "specification": "Описание 2", "image_local_saved_path": "path/to/image2.jpg"}
        ]
    }
    lang = 'ru'
    mexiron_name = 'test_mexiron'

    # Создание экземпляра ReportGenerator
    report_generator = ReportGenerator()

    # Запуск создания отчетов
    result = await report_generator.create_reports_async(bot, chat_id, data, lang, mexiron_name)

    if result:
        print("Отчеты успешно созданы и отправлены.")
    else:
        print("Не удалось создать отчеты.")

if __name__ == "__main__":
    asyncio.run(main())
```
### Как использовать метод `service_apendix`
=========================================================================================

Описание
-------------------------
Метод `service_apendix` создает словарь, представляющий "сервисный" товар, который добавляется в отчет. Этот товар содержит информацию о сервисе, такую как ID, имя, спецификация и путь к изображению. Спецификация сервиса извлекается из HTML-шаблона и преобразуется для использования в отчете.

Шаги выполнения
-------------------------
1. **Определение имени продукта**: В зависимости от языка (`lang`) устанавливает имя продукта как "Сервис" (для русского) или "שירות" (для иврита).
2. **Извлечение спецификации из шаблона**: Читает содержимое HTML-шаблона `service_as_product_{lang}.html`, заменяет символы новой строки (`/n`) на `<br>`, чтобы корректно отображать переносы строк в HTML.
3. **Генерация случайного изображения**: Вызывает функцию `random_image` для получения случайного пути к изображению, которое будет использоваться для сервисного товара.
4. **Создание и возврат словаря**: Создает словарь с информацией о сервисном товаре, включая ID, имя, спецификацию и путь к изображению.

Пример использования
-------------------------

```python
from pathlib import Path
from src.endpoints.kazarinov.report_generator.report_generator import ReportGenerator
from src import gs
from src.utils.image import random_image
from src.logger.logger import logger

class Config:
    ENDPOINT = 'kazarinov'

def random_image(path: Path) -> str:
    """
    Функция возвращает путь к случайной картинке из указанной директории.

    Args:
        path (Path): Путь к директории с картинками.

    Returns:
        str: Путь к случайной картинке или пустая строка, если директория не существует или пуста.
    """
    try:
        if not path.exists() or not path.is_dir():
            logger.error(f"Директория не существует или не является директорией: {path}")
            return ''

        images = [f for f in path.iterdir() if f.is_file() and f.suffix.lower() in ('.png', '.jpg', '.jpeg', '.gif')]
        if not images:
            logger.warning(f"В директории нет изображений: {path}")
            return ''

        return str(random.choice(images)) if images else ''
    except Exception as ex:
        logger.error(f"Произошла ошибка при выборе случайной картинки: {ex}")
        return ''
    
# Пример использования в ReportGenerator (или другом классе/функции)
def example_usage():
    # Создание экземпляра ReportGenerator
    report_generator = ReportGenerator()
    report_generator.storage_path = Path('/tmp')  # Укажите путь к директории для хранения изображений

    # Генерация сервисного приложения для русского языка
    service_info_ru = report_generator.service_apendix(lang='ru')
    print(service_info_ru)

    # Генерация сервисного приложения для иврита
    service_info_he = report_generator.service_apendix(lang='he')
    print(service_info_he)

example_usage()
```

### Как использовать асинхронный метод `create_html_report_async`
=========================================================================================

Описание
-------------------------
Метод `create_html_report_async` генерирует HTML-контент на основе шаблона и предоставленных данных. Он подготавливает данные, выбирает шаблон в зависимости от языка и рендерит HTML-контент с использованием Jinja2.

Шаги выполнения
-------------------------
1. **Установка пути для сохранения HTML**: Если передан `html_path`, метод устанавливает его как путь для сохранения HTML. В противном случае используется `self.html_path`.
2. **Подготовка данных**:
   - Вызывает метод `service_apendix` для получения информации о сервисном товаре.
   - Добавляет информацию о сервисном товаре в список товаров (`data['products']`).
3. **Выбор шаблона**: В зависимости от языка (`lang`) выбирается шаблон: `template_table_he.html` для иврита и `template_table_ru.html` для русского.
4. **Рендеринг HTML**:
   - Читает содержимое выбранного шаблона из файла.
   - Создает Jinja2-шаблон из строки.
   - Рендерит шаблон с использованием предоставленных данных (`data`).
5. **Возврат HTML-контента**: Возвращает сгенерированный HTML-контент.
6. **Обработка ошибок**: Если происходит ошибка во время генерации HTML, метод логирует ошибку и возвращает пустую строку.

Пример использования
-------------------------

```python
import asyncio
from pathlib import Path
from src.endpoints.kazarinov.report_generator.report_generator import ReportGenerator

async def main():
    # Создание экземпляра ReportGenerator
    report_generator = ReportGenerator()
    report_generator.storage_path = Path('/tmp')  # Укажите путь к директории для хранения файлов
    report_generator.html_path = report_generator.storage_path / 'test.html'

    # Пример данных для отчета
    data = {
        "products": [
            {"product_id": "123", "product_name": "Товар 1", "specification": "Описание 1", "image_local_saved_path": "path/to/image1.jpg"},
            {"product_id": "456", "product_name": "Товар 2", "specification": "Описание 2", "image_local_saved_path": "path/to/image2.jpg"}
        ]
    }
    lang = 'ru'

    # Создание HTML-отчета
    html_content = await report_generator.create_html_report_async(data, lang, report_generator.html_path)

    if html_content:
        print("HTML-отчет успешно создан.")
        #print(html_content)  # Вывод HTML-контента
    else:
        print("Не удалось создать HTML-отчет.")

if __name__ == "__main__":
    asyncio.run(main())
```

### Как использовать асинхронный метод `create_pdf_report_async`
=========================================================================================

Описание
-------------------------
Метод `create_pdf_report_async` генерирует PDF-отчет на основе предоставленного HTML-контента. Он использует утилиты PDF для сохранения HTML в PDF-файл и, если указан бот, отправляет PDF-файл в чат.

Шаги выполнения
-------------------------
1. **Установка пути для сохранения PDF**: Если передан `pdf_path`, метод устанавливает его как путь для сохранения PDF. В противном случае используется `self.pdf_path`.
2. **Подготовка HTML-контента**: Если передан `data`, метод устанавливает его как HTML-контент. В противном случае используется `self.html_content`.
3. **Сохранение HTML в PDF**:
   - Создает экземпляр `PDFUtils`.
   - Вызывает метод `save_pdf_pdfkit` для сохранения HTML-контента в PDF-файл.
   - Если не удается сохранить PDF-файл, метод логирует ошибку и, если указан бот, отправляет сообщение об ошибке в чат.
4. **Отправка PDF-файла в чат**: Если указан бот (`self.bot`):
   - Открывает PDF-файл для чтения в бинарном режиме.
   - Отправляет PDF-файл в чат с использованием `self.bot.send_document`.
   - Если не удается отправить файл, метод логирует ошибку и отправляет сообщение об ошибке в чат.
5. **Возврат результата**: Возвращает `True`, если PDF-файл успешно создан и (если указано) отправлен, иначе возвращает `False`.

Пример использования
-------------------------

```python
import asyncio
from pathlib import Path
import telebot
from src.endpoints.kazarinov.report_generator.report_generator import ReportGenerator

async def main():
    # Инициализация бота (замените 'YOUR_BOT_TOKEN' на реальный токен)
    bot = telebot.TeleBot('YOUR_BOT_TOKEN')
    chat_id = 123456789  # ID чата, куда будут отправляться отчеты

    # Создание экземпляра ReportGenerator
    report_generator = ReportGenerator()
    report_generator.bot = bot
    report_generator.chat_id = chat_id
    report_generator.pdf_path = Path('/tmp/test.pdf')  # Укажите путь для сохранения PDF
    report_generator.storage_path = Path('/tmp')  # Укажите путь для хранения файлов

    # HTML-контент для отчета
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Report</title>
    </head>
    <body>
        <h1>Test Report</h1>
        <p>This is a test PDF report generated from HTML.</p>
    </body>
    </html>
    """

    # Создание PDF-отчета
    result = await report_generator.create_pdf_report_async(html_content, 'ru', report_generator.pdf_path)

    if result:
        print("PDF-отчет успешно создан и отправлен.")
    else:
        print("Не удалось создать PDF-отчет.")

if __name__ == "__main__":
    asyncio.run(main())
```

### Как использовать асинхронный метод `create_docx_report_async`
=========================================================================================

Описание
-------------------------
Метод `create_docx_report_async` создает DOCX-файл из HTML-файла, используя функцию `html_to_docx`.

Шаги выполнения
-------------------------
1. **Вызов функции `html_to_docx`**: Метод вызывает функцию `html_to_docx`, передавая путь к HTML-файлу (`self.html_path`) и путь, куда нужно сохранить DOCX-файл (`docx_path`).
2. **Проверка результата**: Если функция `html_to_docx` возвращает `False`, это означает, что не удалось скомпилировать DOCX-файл. В этом случае метод логирует ошибку.
3. **Возврат результата**: Метод возвращает `True`, если DOCX-файл успешно создан, и `False` в противном случае.

Пример использования
-------------------------

```python
import asyncio
from pathlib import Path
from src.endpoints.kazarinov.report_generator.report_generator import ReportGenerator

async def main():
    # Создание экземпляра ReportGenerator
    report_generator = ReportGenerator()
    report_generator.html_path = Path('/tmp/test.html')  # Укажите путь к HTML-файлу
    docx_path = Path('/tmp/test.docx')  # Укажите путь, куда нужно сохранить DOCX-файл

    # Создание HTML-файла для примера
    with open(report_generator.html_path, 'w', encoding='utf-8') as f:
        f.write("<h1>Test DOCX Report</h1><p>This is a test DOCX report generated from HTML.</p>")

    # Создание DOCX-отчета
    result = await report_generator.create_docx_report_async(report_generator.html_path, docx_path)

    if result:
        print("DOCX-отчет успешно создан.")
    else:
        print("Не удалось создать DOCX-отчет.")

if __name__ == "__main__":
    asyncio.run(main())
```

### Как использовать функцию `main`
=========================================================================================

Описание
-------------------------
Функция `main` является точкой входа для генерации отчетов. Она принимает имя мехирона (`maxiron_name`) и язык (`lang`), загружает данные из JSON-файла, создает экземпляр `ReportGenerator` и запускает процесс создания отчетов.

Шаги выполнения
-------------------------
1. **Определение путей**: Функция определяет пути к файлам данных (JSON), HTML, PDF и DOCX на основе имени мехирона и языка.
2. **Загрузка данных**: Загружает данные из JSON-файла с использованием функции `j_loads`.
3. **Создание экземпляра `ReportGenerator`**: Создает экземпляр класса `ReportGenerator`, передавая пути к файлам и флаги для создания HTML, PDF и DOCX отчетов.
4. **Запуск создания отчетов**: Запускает асинхронный процесс создания отчетов с использованием метода `create_reports_async`.

Пример использования
-------------------------

```python
import asyncio
from pathlib import Path
from src.endpoints.kazarinov.report_generator.report_generator import main, ReportGenerator
from src.utils.jjson import j_loads
from src import gs

class Config:
    ENDPOINT = 'kazarinov'

# Mock gs.path для работы примера
class MockGsPath:
    def __init__(self, base_path):