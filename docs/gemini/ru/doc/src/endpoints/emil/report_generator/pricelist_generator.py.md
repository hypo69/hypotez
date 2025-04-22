# Модуль для генерации прайс-листов Казаринова

## Обзор

Модуль предназначен для генерации HTML и PDF отчётов на основе данных о мехиронах Казаринова. Он использует шаблоны Jinja2 для создания HTML-страниц и библиотеку pdfkit для преобразования HTML в PDF.

## Подробней

Этот модуль предоставляет функциональность для автоматического создания отчётов о ценах в формате HTML и PDF. Он принимает данные в формате JSON, загружает их, генерирует HTML на основе шаблонов Jinja2 и сохраняет в файл. Затем HTML преобразуется в PDF с использованием `pdfkit`.

## Классы

### `ReportGenerator`

**Описание**: Класс для генерации HTML- и PDF-отчётов на основе данных из JSON.

**Атрибуты**:

- `env` (Environment): Окружение Jinja2 для загрузки и рендеринга шаблонов. Инициализируется с FileSystemLoader, указывающим на текущую директорию.

**Методы**:

- `generate_html(self, data: dict, lang: str) -> str`: Генерирует HTML-контент на основе шаблона и данных.
- `create_report(self, data: dict, lang: str, html_file: str | Path, pdf_file: str | Path) -> bool`: Полный цикл генерации отчёта.

### `ReportGenerator.generate_html`

```python
async def generate_html(self, data: dict, lang: str) -> str:
    """
    Генерирует HTML-контент на основе шаблона и данных.

    Args:
        data (dict): Словарь с данными для заполнения шаблона.
        lang (str): Язык отчёта ('he' для иврита, любой другой - для русского).

    Returns:
        str: HTML-контент.
    """
```

**Назначение**: Генерирует HTML-контент на основе шаблона и переданных данных.

**Параметры**:

- `data` (dict): Словарь с данными для заполнения шаблона.
- `lang` (str): Язык отчёта (`'he'` для иврита, любой другой - для русского).

**Возвращает**:

- `str`: HTML-контент, сгенерированный на основе шаблона и данных.

**Как работает функция**:

1. Определяет, какой шаблон использовать в зависимости от языка (`lang`). Если язык `'he'`, используется шаблон `'template_table_he.html'`, иначе используется шаблон `'template_table_ru.html'`.
2. Формирует путь к выбранному шаблону.
3. Читает содержимое шаблона из файла.
4. Создаёт Jinja2-шаблон из строки.
5. Рендерит шаблон с использованием переданных данных (`data`).
6. Возвращает сгенерированный HTML-контент.

**Примеры**:

```python
from pathlib import Path
from src.endpoints.kazarinov.react.pricelist_generator import ReportGenerator
import asyncio
from src.utils.jjson import j_loads
from src import gs

# Пример использования (требуется наличие файлов шаблонов и данных)
# gs.path.external_storage = Path('./') # for local test
# gs.path.endpoints = Path('./') # for local test

# data = j_loads(gs.path.endpoints / 'kazarinov' / 'pricelist_generator' / 'templates' / 'example_data.json')  # Загрузка данных из JSON-файла
# report_generator = ReportGenerator()
# html_content = asyncio.run(report_generator.generate_html(data, 'ru'))
# print(html_content)

# Пример с ивритским языком
# html_content_he = asyncio.run(report_generator.generate_html(data, 'he'))
# print(html_content_he)
```

### `ReportGenerator.create_report`

```python
async def create_report(self, data: dict, lang: str, html_file: str | Path, pdf_file: str | Path) -> bool:
    """
    Полный цикл генерации отчёта.

    Args:
        data (dict): Данные для отчёта.
        lang (str): Язык отчёта.
        html_file (str | Path): Путь для сохранения HTML-файла.
        pdf_file (str | Path): Путь для сохранения PDF-файла.

    Returns:
        bool: True, если отчёт успешно сгенерирован, иначе False.
    """
```

**Назначение**: Генерирует HTML- и PDF-отчёт на основе предоставленных данных и языка.

**Параметры**:

- `data` (dict): Словарь с данными для отчёта.
- `lang` (str): Язык отчёта (`'ru'` или `'he'`).
- `html_file` (str | Path): Путь для сохранения HTML-файла.
- `pdf_file` (str | Path): Путь для сохранения PDF-файла.

**Возвращает**:

- `bool`: `True`, если отчёт успешно сгенерирован, иначе `False`.

**Как работает функция**:

1. Создаёт словарь `service_dict` для добавления информации об услугах. Этот словарь содержит:
   - `product_title`: Заголовок продукта ("Сервис" или "שירות" в зависимости от языка).
   - `specification`: HTML-содержимое спецификации услуги, загруженное из файла и отформатированное.
   - `image_local_saved_path`: Случайный путь к изображению.
2. Добавляет `service_dict` в список продуктов в данных (`data['products']`).
3. Генерирует HTML-контент, вызывая `self.generate_html(data, lang)`.
4. Сохраняет HTML-контент в файл по пути `html_file`.
5. Создаёт экземпляр класса `PDFUtils`.
6. Преобразует HTML-контент в PDF-файл с использованием `pdf.save_pdf_pdfkit(html_content, pdf_file)`.
7. Если преобразование в PDF не удалось, логирует ошибку и возвращает `False`.
8. Возвращает `True` в случае успешной генерации отчёта.

**Примеры**:

```python
from pathlib import Path
from src.endpoints.kazarinov.react.pricelist_generator import ReportGenerator
import asyncio
from src.utils.jjson import j_loads
from src import gs

# Пример использования (требуется наличие файлов шаблонов и данных)
# gs.path.external_storage = Path('./') # for local test
# gs.path.endpoints = Path('./') # for local test

# data = j_loads(gs.path.endpoints / 'kazarinov' / 'pricelist_generator' / 'templates' / 'example_data.json')
# report_generator = ReportGenerator()
# html_file = Path('report.html')
# pdf_file = Path('report.pdf')

# success = asyncio.run(report_generator.create_report(data, 'ru', html_file, pdf_file))
# print(f"Отчёт создан: {success}")
```

## Функции

### `main`

```python
def main(mexiron: str, lang: str) -> bool:
    """
    Основная функция для генерации отчёта.

    Args:
        mexiron (str): Название мехирона.
        lang (str): Язык отчёта ('ru' или 'he').

    Returns:
        bool: True, если отчёт успешно сгенерирован, иначе False.
    """
```

**Назначение**: Функция выполняет основную логику для генерации HTML- и PDF-отчётов.

**Параметры**:

- `mexiron` (str): Название мехирона (используется для формирования путей к файлам).
- `lang` (str): Язык отчёта (`'ru'` или `'he'`).

**Возвращает**:

- `bool`: `True`, если отчёт успешно сгенерирован, иначе `False`.

**Как работает функция**:

1. Формирует базовый путь к данным и файлам отчёта на основе `mexiron`.
2. Загружает данные из JSON-файла.
3. Определяет пути для HTML- и PDF-файлов.
4. Создаёт экземпляр класса `ReportGenerator`.
5. Запускает асинхронную генерацию отчёта с использованием `asyncio.run()`.

**Примеры**:

```python
from pathlib import Path
from src.endpoints.kazarinov.react.pricelist_generator import main

# Пример использования (требуется наличие файлов шаблонов и данных)
# success = main('24_12_01_03_18_24_269', 'ru')
# print(f"Отчёт создан: {success}")