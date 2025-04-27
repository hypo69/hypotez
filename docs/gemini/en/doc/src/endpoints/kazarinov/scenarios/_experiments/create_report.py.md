# Модуль для проверки генерации прайслиста

## Обзор

Модуль `create_report.py` предоставляет функциональность для создания отчетов в формате HTML и PDF, основанных на данных, полученных в результате обработки прайслиста. Он используется для проверки корректности генерации прайслиста и выявления возможных ошибок.

## Детали

Модуль использует класс `ReportGenerator`, который отвечает за создание отчетов. Внутри модуля определены пути к HTML и PDF файлам, которые будут генерироваться для проверки.

## Классы

### `ReportGenerator`

**Описание**: Класс `ReportGenerator` предназначен для создания отчетов в формате HTML и PDF.

**Атрибуты**: 

- `report_generator` (ReportGenerator): Экземпляр класса `ReportGenerator`, который используется для генерации отчетов.

**Методы**:

- `create_report(response_dict: dict, lang: str, html_file: Path, pdf_file: Path)`: Метод создает отчет в форматах HTML и PDF, используя данные из `response_dict` и указанные пути к файлам.

**Принцип работы**:

Класс `ReportGenerator` использует внутренние методы для создания HTML и PDF отчетов. Метод `create_report()` принимает словарь с данными, язык, пути к HTML и PDF файлам. Он обрабатывает данные и генерирует отчеты в указанных форматах.

## Файлы

- `html_file_he:Path`: Путь к файлу с HTML-отчетом на иврите.
- `pdf_file_he:Path`: Путь к файлу с PDF-отчетом на иврите.
- `html_file_ru:Path`: Путь к файлу с HTML-отчетом на русском языке.
- `pdf_file_ru:Path`: Путь к файлу с PDF-отчетом на русском языке.

## Функции

### `create_report(response_dict: dict, lang: str, html_file: Path, pdf_file: Path)`

**Описание**: Функция создает отчеты в форматах HTML и PDF на основе данных, полученных от модели.

**Параметры**:

- `response_dict` (dict): Словарь с данными, полученными от модели.
- `lang` (str): Язык, на котором будет создан отчет.
- `html_file` (Path): Путь к файлу с HTML-отчетом.
- `pdf_file` (Path): Путь к файлу с PDF-отчетом.

**Возвращает**:

- None

**Примеры**:

```python
# Создание отчета на иврите
report_generator.create_report(response_he_dict['he'], 'he', html_file_he, pdf_file_he)

# Создание отчета на русском языке
report_generator.create_report(response_ru_dict['ru'], 'ru', html_file_ru, pdf_file_ru)
```

**Как работает функция**:

Функция использует класс `ReportGenerator` для создания HTML и PDF отчетов. Она передает данные, язык и пути к файлам в метод `create_report()` класса `ReportGenerator`. Метод `create_report()` обрабатывает данные и генерирует отчеты в указанных форматах.

## Примеры

```python
# Пример использования функции `create_report()` для создания отчета на иврите:
response_he_dict = {'he': {'product_name': 'Товар на иврите', 'price': 100}}
html_file_he = Path('he.html')
pdf_file_he = Path('he.pdf')
report_generator.create_report(response_he_dict['he'], 'he', html_file_he, pdf_file_he)
```