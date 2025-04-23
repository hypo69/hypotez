# Модуль для генерации прайс-листов для Казаринова

## Обзор

Модуль предназначен для генерации HTML и PDF файлов прайс-листов на основе JSON данных. Он использует шаблоны Jinja2 для создания HTML и библиотеку pdfkit или собственные инструменты для преобразования HTML в PDF.

## Подробнее

Этот модуль предоставляет класс `ReportGenerator` для создания отчетов на основе данных из JSON файлов. Он поддерживает разные языки для генерации отчетов и использует шаблоны Jinja2 для форматирования HTML. Модуль также включает функциональность для преобразования HTML в PDF.

## Классы

### `ReportGenerator`

**Описание**: Класс для генерации HTML и PDF отчетов на основе данных из JSON.

**Атрибуты**:
- `env` (Environment): Окружение Jinja2 для загрузки и рендеринга шаблонов.

**Методы**:
- `generate_html(data: dict, lang: str) -> str`: Генерирует HTML-контент на основе шаблона и данных.
- `create_report(data: dict, lang: str, html_file: str | Path, pdf_file: str | Path) -> bool`: Запускает полный цикл генерации отчёта.

### `ReportGenerator.generate_html`

```python
async def generate_html(self, data: dict, lang: str) -> str:
    """
    Генерирует HTML-контент на основе шаблона и данных.

    Args:
        data (dict): Данные для заполнения шаблона.
        lang (str): Язык отчёта.

    Returns:
        str: HTML-контент.
    """
    ...
```

**Назначение**: Генерирует HTML-контент на основе шаблона и данных.

**Параметры**:
- `data` (dict): Данные для заполнения шаблона.
- `lang` (str): Язык отчёта (`ru` или `he`).

**Возвращает**:
- `str`: HTML-контент, сгенерированный на основе шаблона и данных.

**Как работает функция**:
- Определяет, какой шаблон использовать в зависимости от языка (`template_table_he.html` для иврита и `template_table_ru.html` для русского).
- Формирует путь к файлу шаблона.
- Читает содержимое шаблона из файла.
- Создает объект шаблона Jinja2 из строки.
- Рендерит шаблон с использованием переданных данных и возвращает полученный HTML-код.

**Примеры**:

```python
from pathlib import Path
from src.endpoints.emil.report_generator.pricelist_generator import ReportGenerator
import asyncio

async def main():
    # Пример данных для отчета
    data = {
        "products": [
            {"product_title": "Товар 1", "specification": "Описание 1", "image_local_saved_path": "path/to/image1.jpg"},
            {"product_title": "Товар 2", "specification": "Описание 2", "image_local_saved_path": "path/to/image2.jpg"}
        ]
    }
    # Создание экземпляра ReportGenerator
    report_generator = ReportGenerator()
    # Генерация HTML на русском языке
    html_content = await report_generator.generate_html(data, "ru")
    print(html_content)
    # Сохранение HTML в файл (опционально)
    # Path("report.html").write_text(html_content, encoding="UTF-8")

asyncio.run(main())
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
        bool: True в случае успешной генерации, False в случае ошибки.
    """
    ...
```

**Назначение**: Запускает полный цикл генерации отчёта, включая добавление сервисной информации, генерацию HTML и сохранение в PDF.

**Параметры**:
- `data` (dict): Данные для отчёта.
- `lang` (str): Язык отчёта (`ru` или `he`).
- `html_file` (str | Path): Путь для сохранения HTML-файла.
- `pdf_file` (str | Path): Путь для сохранения PDF-файла.

**Возвращает**:
- `bool`: `True` в случае успешной генерации, `False` в случае ошибки.

**Как работает функция**:
- Определяет словарь `service_dict` с информацией об услуге, адаптированной под язык отчета.
- Добавляет информацию об услуге в список продуктов (`data['products']`).
- Генерирует HTML-контент с использованием метода `generate_html`.
- Сохраняет HTML-контент в файл.
- Инициализирует утилиту для работы с PDF (`PDFUtils`).
- Сохраняет HTML-контент в PDF-файл, используя метод `save_pdf_pdfkit` из `PDFUtils`.
- Логирует ошибку, если не удалось создать PDF.

**Примеры**:

```python
from pathlib import Path
from src.endpoints.emil.report_generator.pricelist_generator import ReportGenerator
from src import gs
import asyncio

async def main():
    # Пример данных для отчета
    data = {
        "products": [
            {"product_title": "Товар 1", "specification": "Описание 1", "image_local_saved_path": "path/to/image1.jpg"},
            {"product_title": "Товар 2", "specification": "Описание 2", "image_local_saved_path": "path/to/image2.jpg"}
        ]
    }

    # Язык отчета
    lang = "ru"

    # Пути для сохранения HTML и PDF файлов
    html_file = Path("report.html")
    pdf_file = Path("report.pdf")

    # Создание экземпляра ReportGenerator
    report_generator = ReportGenerator()

    # Запуск генерации отчета
    success = await report_generator.create_report(data, lang, html_file, pdf_file)

    if success:
        print(f"Отчет успешно сгенерирован: {html_file}, {pdf_file}")
    else:
        print("Ошибка при генерации отчета.")

asyncio.run(main())
```

## Функции

### `main`

```python
def main(mexiron: str, lang: str) -> bool:
    """
    Основная функция для запуска генерации отчёта.

    Args:
        mexiron (str): Имя директории mexiron.
        lang (str): Язык отчёта.

    Returns:
        bool: True в случае успешной генерации, False в случае ошибки.
    """
    ...
```

**Назначение**: Основная функция для запуска генерации отчёта.

**Параметры**:
- `mexiron` (str): Имя директории mexiron.
- `lang` (str): Язык отчёта (`ru` или `he`).

**Возвращает**:
- `bool`: `True` в случае успешной генерации, `False` в случае ошибки.

**Как работает функция**:
- Формирует базовый путь к директории mexiron.
- Загружает данные из JSON-файла.
- Формирует пути для HTML и PDF файлов.
- Создает экземпляр `ReportGenerator`.
- Запускает процесс генерации отчета асинхронно.

**Примеры**:

```python
from src.endpoints.emil.report_generator.pricelist_generator import main

# Пример использования функции main
mexiron = "24_12_01_03_18_24_269"
lang = "ru"
main(mexiron, lang)