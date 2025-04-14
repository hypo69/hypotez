# Модуль `report_generator.py`

## Обзор

Модуль предназначен для генерации отчётов в формате HTML и PDF на основе данных, полученных в формате JSON. Он использует шаблонизатор Jinja2 для создания HTML-страниц и библиотеку pdfkit для конвертации HTML в PDF. Модуль предназначен для использования в проекте `hypotez` и интегрирован с системой логирования и утилитами проекта.

## Подробней

Этот модуль предоставляет класс `ReportGenerator`, который позволяет генерировать отчёты в форматах HTML, PDF и DOCX на основе данных, полученных из JSON-файлов. Он использует шаблоны Jinja2 для создания HTML-страниц и библиотеки `pdfkit` для конвертации HTML в PDF. Модуль интегрирован с системой логирования и утилитами проекта `hypotez`. Расположение файла в структуре проекта `/src/endpoints/kazarinov/report_generator/report_generator.py` указывает на его использование в качестве одной из конечных точек (endpoint) для обработки и генерации отчётов, предположительно, связанных с мехиронами Казаринова.

## Классы

### `ReportGenerator`

**Описание**: Класс для генерации HTML- и PDF-отчётов на основе данных из JSON.

**Атрибуты**:
- `if_need_html` (bool): Флаг, указывающий, требуется ли генерировать HTML-отчёт.
- `if_need_pdf` (bool): Флаг, указывающий, требуется ли генерировать PDF-отчёт.
- `if_need_docx` (bool): Флаг, указывающий, требуется ли генерировать DOCX-отчёт.
- `storage_path` (Path): Путь к директории хранения отчётов. По умолчанию `Path(gs.path.external_storage, ENDPOINT)`.
- `html_path` (Path | str): Путь к HTML-файлу.
- `pdf_path` (Path | str): Путь к PDF-файлу.
- `docs_path` (Path | str): Путь к DOCX-файлу.
- `html_content` (str): Содержимое HTML-страницы.
- `data` (dict): Данные для отчёта.
- `lang` (str): Язык отчёта.
- `mexiron_name` (str): Название мехирона.
- `env` (Environment): Объект окружения Jinja2.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `ReportGenerator`.
- `create_reports_async`: Создаёт все типы отчётов (HTML, PDF, DOCX) асинхронно.
- `service_apendix`: Генерирует сервисное дополнение к отчёту.
- `create_html_report_async`: Генерирует HTML-контент на основе шаблона и данных.
- `create_pdf_report_async`: Генерирует PDF-отчёт на основе HTML-контента.
- `create_docx_report_async`: Генерирует DOCX-отчёт на основе HTML-контента.

#### `__init__`

```python
def __init__(self, 
             if_need_pdf:Optional[bool] = True, 
             if_need_docx:Optional[bool] = True, 
        ):
    """Определение, какие форматы данных требуется вернуть"""
```

**Назначение**: Инициализирует экземпляр класса `ReportGenerator`. Определяет, какие форматы отчетов (PDF, DOCX) необходимо генерировать.

**Параметры**:
- `if_need_pdf` (Optional[bool], optional): Определяет, нужно ли генерировать PDF-отчет. По умолчанию `True`.
- `if_need_docx` (Optional[bool], optional): Определяет, нужно ли генерировать DOCX-отчет. По умолчанию `True`.

#### `create_reports_async`

```python
async def create_reports_async(self,
                         bot: telebot.TeleBot,
                         chat_id: int,
                         data:dict,
                         lang:str,
                         mexiron_name:str,
                         ) -> tuple:
    """Create ALL types: HTML, PDF, DOCX"""
    ...
```

**Назначение**: Асинхронно создает отчеты всех указанных типов (HTML, PDF, DOCX).

**Параметры**:
- `bot` (telebot.TeleBot): Экземпляр бота TeleBot для отправки отчетов.
- `chat_id` (int): ID чата, куда отправлять отчеты.
- `data` (dict): Данные для генерации отчета.
- `lang` (str): Язык отчета.
- `mexiron_name` (str): Название мехирона.

**Возвращает**:
- `tuple`: Не определено. Предположительно, кортеж, содержащий результаты операций.

**Как работает функция**:
- Формирует пути для сохранения HTML, PDF и DOCX файлов на основе имени мехирона и языка.
- Вызывает метод `create_html_report_async` для генерации HTML-контента.
- Если HTML-контент не создан, возвращает `False`.
- Если установлен флаг `if_need_pdf`, вызывает метод `create_pdf_report_async` для генерации PDF-отчета.
- Если установлен флаг `if_need_docx`, вызывает метод `create_docx_report_async` для генерации DOCX-отчета.

#### `service_apendix`

```python
def service_apendix(self, lang:str) -> dict:
    return  {
            "product_id":"00000",
            "product_name":"Сервис" if lang == 'ru' else "שירות",
            "specification":Path(__root__ / 'src' / 'endpoints' / ENDPOINT / 'report_generator' / 'templates' / f'service_as_product_{lang}.html').read_text(encoding='UTF-8').replace('/n','<br>'),
            "image_local_saved_path":random_image(self.storage_path / 'converted_images' )
            }

    ...
```

**Назначение**: Создает и возвращает словарь с данными для сервисного дополнения к отчету (например, информация об услуге).

**Параметры**:
- `lang` (str): Язык, на котором должно быть представлено название сервиса.

**Возвращает**:
- `dict`: Словарь, содержащий информацию о сервисном дополнении:
    - `"product_id"` (str): ID продукта (всегда "00000").
    - `"product_name"` (str): Название продукта ("Сервис" на русском или "שירות" на иврите).
    - `"specification"` (str): Спецификация продукта, загруженная из HTML-шаблона и отформатированная для вставки в отчет.
    - `"image_local_saved_path"` (str): Путь к случайному изображению, сохраненному локально.

**Как работает функция**:
- Определяет название продукта в зависимости от языка (`lang`).
- Загружает HTML-шаблон спецификации продукта из файла, соответствующего языку.
- Заменяет символы новой строки (`/n`) на теги `<br>`, чтобы корректно отображать спецификацию в HTML-отчете.
- Генерирует путь к случайному изображению, используя функцию `random_image` из модуля `src.utils.image`.
- Возвращает словарь с собранными данными.

#### `create_html_report_async`

```python
async def create_html_report_async(self, data:dict, lang:str, html_path:Optional[ str|Path] ) -> str | None:
    """
    Генерирует HTML-контент на основе шаблона и данных.

    Args:
        lang (str): Язык отчёта.

    Returns:
        str: HTML-контент.
    """
```

**Назначение**: Асинхронно генерирует HTML-контент на основе шаблона и данных.

**Параметры**:
- `data` (dict): Данные для вставки в HTML-шаблон.
- `lang` (str): Язык отчёта (используется для выбора шаблона).
- `html_path` (Optional[str | Path], optional): Путь для сохранения HTML-файла. Если не указан, используется значение по умолчанию `self.html_path`.

**Возвращает**:
- `str | None`: HTML-контент в случае успешной генерации и сохранения, или `None` в случае ошибки.

**Как работает функция**:
- Определяет путь для сохранения HTML-файла, используя переданный аргумент `html_path` или значение по умолчанию `self.html_path`.
- Добавляет сервисное приложение к данным отчёта, используя метод `self.service_apendix(lang)`.
- Определяет имя шаблона в зависимости от языка отчёта (`template_table_he.html` для иврита, `template_table_ru.html` для русского).
- Формирует полный путь к шаблону.
- Загружает шаблон из файла и создаёт объект шаблона Jinja2.
- Генерирует HTML-контент, передавая данные в шаблон (`template.render(**data)`).
- Пытается сохранить HTML-контент в файл по указанному пути.
- Логирует информацию об успешном сохранении файла.
- В случае ошибки логирует сообщение об ошибке и возвращает `None`.

#### `create_pdf_report_async`

```python
async def create_pdf_report_async(self, 
                            data: dict, 
                            lang:str, 
                            pdf_path:str |Path) -> bool:
    """
    Полный цикл генерации отчёта.

    Args:
        lang (str): Язык отчёта.
    """
```

**Назначение**: Асинхронно генерирует PDF-отчёт на основе HTML-контента.

**Параметры**:
- `data` (dict): Данные для генерации PDF-отчета (HTML-контент).
- `lang` (str): Язык отчёта (не используется в данной функции, но может быть полезен для расширения функциональности).
- `pdf_path` (str | Path): Путь для сохранения PDF-файла.

**Возвращает**:
- `bool`: `True` в случае успешной генерации и отправки отчёта, `False` в случае ошибки.

**Как работает функция**:
- Определяет путь для сохранения PDF-файла, используя переданный аргумент `pdf_path` или значение по умолчанию `self.pdf_path`.
- Инициализирует `html_content` данными, переданными в функцию, или использует сохраненный `self.html_content`.
- Создает экземпляр класса `PDFUtils` из модуля `src.utils.pdf`.
- Сохраняет PDF-файл, используя метод `save_pdf_pdfkit` объекта `PDFUtils`.
- Если сохранение не удалось, логирует сообщение об ошибке и отправляет сообщение об ошибке в чат (если указан бот).
- Если указан бот, пытается отправить PDF-файл в чат.
- В случае успеха возвращает `True`, в случае ошибки отправляет сообщение об ошибке в чат и возвращает `False`.

#### `create_docx_report_async`

```python
async def create_docx_report_async(self, html_path:str|Path, docx_path:str|Path) -> bool :
    """Создаю docx файл """
```

**Назначение**: Асинхронно создает DOCX-файл на основе HTML-контента.

**Параметры**:
- `html_path` (str | Path): Путь к HTML-файлу, на основе которого будет создан DOCX-файл.
- `docx_path` (str | Path): Путь для сохранения DOCX-файла.

**Возвращает**:
- `bool`: `True` в случае успешной генерации DOCX-файла, `False` в случае ошибки.

**Как работает функция**:
- Вызывает функцию `html_to_docx` из модуля `src.utils.convertors.html2docx` для преобразования HTML-файла в DOCX-файл.
- Логирует сообщение об ошибке, если преобразование не удалось.
- Возвращает `True` в случае успеха и `False` в случае ошибки.

## Функции

### `main`

```python
def main(maxiron_name:str, lang:str) ->bool:
    ...
```

**Назначение**: Главная функция, запускающая процесс генерации отчётов.

**Параметры**:
- `maxiron_name` (str): Имя мехирона.
- `lang` (str): Язык отчёта.

**Возвращает**:
- `bool`: Возвращает `True` в случае успешного завершения, `False` в случае ошибки.

**Как работает функция**:
- Определяет пути к данным и файлам отчетов на основе имени мехирона и языка.
- Загружает данные из JSON-файла с использованием функции `j_loads`.
- Определяет, какие типы отчетов необходимо генерировать (HTML, PDF, DOCX).
- Создаёт экземпляр класса `ReportGenerator`.
- Запускает асинхронную генерацию отчетов с использованием `asyncio.run`.

## Примеры

Пример использования модуля для генерации отчётов:

```python
from src.endpoints.kazarinov.report_generator.report_generator import ReportGenerator
from pathlib import Path
import asyncio

async def main():
    maxiron_name = '250127221657987'
    lang = 'ru'
    
    # Пример путей (замените на актуальные пути к вашим файлам)
    external_storage_path = Path('/путь/к/external_storage')
    html_path = external_storage_path / 'mexironim' / maxiron_name / f'{maxiron_name}_{lang}.html'
    pdf_path = external_storage_path / 'mexironim' / maxiron_name / f'{maxiron_name}_{lang}.pdf'
    docx_path = external_storage_path / 'mexironim' / maxiron_name / f'{maxiron_name}_{lang}.docx'
    data_path = external_storage_path / 'mexironim' / maxiron_name / f'{maxiron_name}_{lang}.json'
    
    # Загружаем данные из JSON-файла (предполагается, что j_loads определена)
    from src.utils.jjson import j_loads
    data = j_loads(data_path)

    # Создаем экземпляр ReportGenerator
    report_generator = ReportGenerator()

    # Генерируем отчеты
    #await report_generator.create_reports_async(bot, chat_id, data, lang, maxiron_name) #нужно передать bot и chat_id

if __name__ == "__main__":
    asyncio.run(main())