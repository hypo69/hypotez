## \\file /src/endpoints/emil/report_generator/pricelist_generator.py

# Модуль генерации прайс-листов

```rst
.. module:: src.endpoints.kazarinov.react
	:platform: Windows, Unix
	:synopsis: Генератор HTML и PDF для мехиронов Казаринова

Описание работы:

*   Конструктор `__init__`: Принимает шаблон, базовый путь, метку времени и язык.
*   Метод `load_data`: Загружает данные из JSON-файла.
*   Метод `generate_html`: Генерирует HTML с использованием Jinja2.
*   Метод `save_html`: Сохраняет HTML в файл.
*   Метод `generate_pdf`: Преобразует HTML в PDF.
*   Метод `create_report`: Запускает полный цикл генерации отчёта.

```

Модуль предназначен для генерации HTML и PDF-отчетов на основе данных из JSON.

## Обзор

Модуль `src.endpoints.emil.report_generator.pricelist_generator` предоставляет класс `ReportGenerator` для создания HTML- и PDF-отчетов на основе данных из JSON-файла.

## Подробней

Модуль использует Jinja2 для генерации HTML-контента и PDFKit для преобразования HTML в PDF.

## Классы

### `ReportGenerator`

**Описание**: Класс для генерации HTML- и PDF-отчетов на основе данных из JSON.

**Атрибуты**:

*   `env` (Environment): Окружение Jinja2 для загрузки шаблонов.

**Методы**:

*   `generate_html(self, data: dict, lang: str) -> str`: Генерирует HTML-контент на основе шаблона и данных.
*   `create_report(self, data: dict, lang: str, html_file: str| Path, pdf_file: str | Path) -> bool`: Полный цикл генерации отчёта.

## Функции

### `main`

```python
def main(mexiron: str,lang: str) ->bool:
```

**Назначение**: Функция для запуска процесса генерации отчета.

**Параметры**:

*   `mexiron` (str): Имя мехирона.
*   `lang` (str): Язык отчета.

**Как работает функция**:

1.  Определяет базовый путь к данным мехирона.
2.  Загружает данные из JSON-файла.
3.  Определяет пути к HTML- и PDF-файлам.
4.  Создает экземпляр класса `ReportGenerator`.
5.  Запускает процесс создания отчета.

### `ReportGenerator`

### `__init__`

**Назначение**:  Инициализирует окружение Jinja2 для работы с шаблонами.

### `generate_html`

```python
async def generate_html(self, data:dict, lang: str) -> str:
```

**Назначение**: Генерирует HTML-контент на основе шаблона и данных.

**Параметры**:

*   `data` (dict): Данные для заполнения шаблона.
*   `lang` (str): Язык отчёта.

**Возвращает**:

*   `str`: HTML-контент.

**Как работает функция**:

1.  Определяет путь к шаблону HTML в зависимости от языка.
2.  Читает содержимое шаблона в виде строки.
3.  Создает шаблон Jinja2 из строки.
4.  Рендерит шаблон с использованием переданных данных и возвращает HTML-контент.

### `create_report`

```python
async def create_report(self, data: dict, lang:str, html_file:str| Path, pdf_file:str |Path) -> bool:
```

**Назначение**: Полный цикл генерации отчёта.

**Параметры**:

*   `data` (dict): Данные для отчёта.
*   `lang` (str): Язык отчёта.
*   `html_file` (str | Path): Путь для сохранения HTML-файла.
*   `pdf_file` (str | Path): Путь для сохранения PDF-файла.

**Возвращает**:

*   `bool`: True, если отчет успешно создан, False в противном случае.

**Как работает функция**:

1.  Добавляет в данные информацию об обслуживании (service).
2.  Генерирует HTML-контент, используя метод `generate_html`.
3.  Сохраняет HTML-контент в файл.
4.  Преобразует HTML-файл в PDF, используя `PDFUtils`.
5.  Логирует результаты выполнения.