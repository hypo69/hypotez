# Модуль для проверки генерации прайслиста

## Обзор

Модуль `src/endpoints/kazarinov/scenarios/_experiments/create_report.py`  предназначен для создания отчетов в формате HTML и PDF с данными, полученными из модели  генерации прайслиста. Он использует класс `ReportGenerator` из модуля `src.endpoints.kazarinov.pricelist_generator`, который выполняет рендеринг и экспорт отчетов.

## Подробней

Модуль `src/endpoints/kazarinov/scenarios/_experiments/create_report.py`  использует функции из модуля `src.endpoints.kazarinov.scenarios._experiments.ask_model` для получения данных от модели генерации прайслиста. Затем он использует класс `ReportGenerator` из модуля `src.endpoints.kazarinov.pricelist_generator` для создания отчетов в формате HTML и PDF.
В коде используются две переменные: `response_he_dict` и `response_ru_dict`, содержащие данные о товарах в формате JSON. Данные  извлекаются из модели, с помощью функций, определенных в модуле `src.endpoints.kazarinov.scenarios._experiments.ask_model`.

## Классы

### `ReportGenerator`

**Описание**: Класс `ReportGenerator`  предназначен для рендеринга и экспорта прайслистов в формате HTML и PDF.

**Наследует**:  `None`

**Атрибуты**: `None`

**Методы**:

- `create_report(data: dict, lang: str, html_file: Path, pdf_file: Path)`:  Функция создает отчет в формате HTML и PDF. 

## Функции

### `create_report`

**Назначение**:  Функция создает отчет в формате HTML и PDF. 

**Параметры**:

- `data (dict)`: Словарь, содержащий данные о товарах для генерации прайслиста.
- `lang (str)`: Язык, на котором будет создан отчет.
- `html_file (Path)`: Путь к файлу, в который будет сохранен отчет в формате HTML.
- `pdf_file (Path)`: Путь к файлу, в который будет сохранен отчет в формате PDF.

**Возвращает**: `None`

**Вызывает исключения**: `None`


**Как работает функция**:

- Функция  использует  класса `ReportGenerator` для  рендеринга отчета в формате HTML и PDF. 
- Функция `create_report` из  `src.endpoints.kazarinov.pricelist_generator.ReportGenerator` принимает  словарь данных, язык, путь к HTML-файлу и путь к PDF-файлу. 
- Затем,  `create_report`  использует  библиотеку `pdfkit`  для  преобразования  HTML  в  PDF.

**Примеры**:

```python
# Пример вызова функции create_report
report_generator.create_report(response_he_dict['he'], 'he', html_file_he, pdf_file_he)
report_generator.create_report(response_ru_dict['ru'], 'ru', html_file_ru, pdf_file_ru)