# Module Name

## Overview

Модуль предназначен для генерации HTML и PDF отчетов для мехиронов Казаринова на основе данных из JSON.

## More details

Этот модуль автоматизирует процесс создания отчетов, используя шаблоны Jinja2 для генерации HTML и библиотеку pdfkit для преобразования HTML в PDF. Он включает в себя функциональность для загрузки данных, генерации HTML, сохранения HTML в файл и создания PDF-отчета.

## Classes

### `ReportGenerator`

**Description**: Класс для генерации HTML- и PDF-отчетов на основе данных из JSON.

**Inherits**: Отсутствует.

**Attributes**:
- `env` (Environment): Окружение Jinja2 для работы с шаблонами. Инициализируется с загрузчиком файловой системы, указывающим на текущую директорию.

**Methods**:
- `generate_html(data:dict, lang:str)`: Генерирует HTML-контент на основе шаблона и данных.
- `create_report(data: dict, lang:str, html_file:str| Path, pdf_file:str |Path)`: Запускает полный цикл генерации отчёта.

**Working principle**:
Класс `ReportGenerator` использует окружение Jinja2 для загрузки и обработки HTML-шаблонов. Метод `generate_html` заполняет шаблон данными и возвращает HTML-контент. Метод `create_report` выполняет полный цикл генерации отчета, начиная с добавления сервисной информации, генерации HTML-контента, его сохранения в файл и заканчивая преобразованием HTML в PDF.

## Class Methods

### `generate_html`

```python
async def generate_html(self, data:dict, lang:str ) -> str:
    """
    Генерирует HTML-контент на основе шаблона и данных.

    Args:
        lang (str): Язык отчёта.

    Returns:
        str: HTML-контент.
    """
    ...
```

**Purpose**:
Генерирует HTML-контент на основе шаблона и данных. Функция определяет, какой шаблон использовать в зависимости от языка (`he` или `ru`), загружает шаблон из файла, заполняет его данными и возвращает полученный HTML-контент.

**Parameters**:
- `data` (dict): Данные для заполнения шаблона.
- `lang` (str): Язык отчёта (`ru` или `he`).

**Returns**:
- `str`: HTML-контент, сгенерированный на основе шаблона и данных.

**How the function works**:
1. Определяет, какой шаблон использовать в зависимости от языка отчёта.
2. Формирует путь к файлу шаблона.
3. Читает содержимое файла шаблона.
4. Создает объект шаблона Jinja2 из строки.
5. Заполняет шаблон данными из словаря `data`.
6. Возвращает сгенерированный HTML-контент.

**Examples**:
```python
r = ReportGenerator()
data = {"ключ": "значение"}
lang = "ru"
html_content = asyncio.run(r.generate_html(data, lang))
print(html_content)
```

### `create_report`

```python
async def create_report(self, data: dict, lang:str, html_file:str| Path, pdf_file:str |Path) -> bool:
    """
    Полный цикл генерации отчёта.

    Args:
        lang (str): Язык отчёта.
    """
    ...
```

**Purpose**:
Осуществляет полный цикл генерации отчета, включая добавление сервисной информации, генерацию HTML-контента, сохранение HTML в файл и преобразование HTML в PDF.

**Parameters**:
- `data` (dict): Данные для отчета.
- `lang` (str): Язык отчета.
- `html_file` (str | Path): Путь к файлу для сохранения HTML-контента.
- `pdf_file` (str | Path): Путь к файлу для сохранения PDF-отчета.

**Returns**:
- `bool`: `True`, если отчет успешно сгенерирован, `False` в противном случае.

**How the function works**:
1. Формирует словарь `service_dict` с информацией об услуге, включая заголовок продукта, спецификацию и путь к изображению.
2. Добавляет словарь `service_dict` в список продуктов в данных отчета.
3. Генерирует HTML-контент с использованием метода `generate_html`.
4. Сохраняет HTML-контент в файл, указанный в `html_file`.
5. Инициализирует объект `PDFUtils`.
6. Преобразует HTML-контент в PDF и сохраняет его в файл, указанный в `pdf_file`.
7. Логирует ошибку, если не удалось скомпилировать PDF.
8. Возвращает `True`, если отчет успешно сгенерирован, `False` в противном случае.

**Examples**:
```python
r = ReportGenerator()
data = {"products": []}
lang = "ru"
html_file = "report.html"
pdf_file = "report.pdf"
result = asyncio.run(r.create_report(data, lang, html_file, pdf_file))
print(result)
```

## Functions

### `main`

```python
def main(mexiron:str,lang:str) ->bool:
    ...
```

**Purpose**:
Основная функция для запуска процесса генерации отчета.

**Parameters**:
- `mexiron` (str): Идентификатор мехирона.
- `lang` (str): Язык отчета.

**Returns**:
- `bool`: `True`, если отчет успешно сгенерирован, `False` в противном случае.

**How the function works**:
1. Формирует путь к данным на основе идентификатора мехирона и языка.
2. Загружает данные из JSON-файла.
3. Формирует пути к файлам для сохранения HTML и PDF.
4. Создает экземпляр класса `ReportGenerator`.
5. Запускает асинхронную генерацию отчета.

**Examples**:
```python
mexiron = "24_12_01_03_18_24_269"
lang = "ru"
main(mexiron, lang)