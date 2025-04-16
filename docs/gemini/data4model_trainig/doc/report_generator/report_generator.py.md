# Модуль `report_generator`

## Обзор

Модуль `report_generator` предназначен для генерации HTML и PDF отчетов на основе данных из JSON для проекта Казаринова.

## Подробней

Модуль предоставляет класс `ReportGenerator`, который позволяет создавать отчеты в формате HTML и PDF, используя шаблоны Jinja2 и библиотеку pdfkit. Он также включает функции для загрузки данных, настройки параметров отчета и сохранения результатов в файлы.

## Классы

### `Config`

**Описание**: Класс конфигурации для модуля `report_generator`.

**Атрибуты**:

*   `ENDPOINT` (str): Конечная точка API (значение: `'kazarinov'`).

### `ReportGenerator`

**Описание**: Класс для генерации HTML- и PDF-отчётов на основе данных из JSON.

**Атрибуты**:

*   `if_need_html` (bool): Флаг, указывающий, требуется ли генерация HTML-отчета.
*   `if_need_pdf` (bool): Флаг, указывающий, требуется ли генерация PDF-отчета.
*   `if_need_docx` (bool): Флаг, указывающий, требуется ли генерация DOCX-отчета.
*   `storage_path` (Path): Путь к директории хранения отчетов.
*   `html_path` (Path | str): Путь к HTML-файлу.
*   `pdf_path` (Path | str): Путь к PDF-файлу.
*   `docs_path` (Path | str): Путь к DOCX-файлу.
*   `html_content` (str): HTML-контент отчета.
*   `data` (dict): Данные для отчета в формате словаря.
*   `lang` (str): Язык отчета.
*   `mexiron_name` (str): Имя мехирона.
*   `env` (Environment): Окружение Jinja2 для работы с шаблонами.

**Методы**:

*   `__init__`: Инициализирует объект `ReportGenerator`.
*   `create_reports_async`: Асинхронно создает отчеты во всех поддерживаемых форматах (HTML, PDF, DOCX).
*   `service_apendix`: Создает словарь с информацией об услуге для добавления в отчет.
*   `create_html_report_async`: Асинхронно генерирует HTML-контент на основе шаблона и данных.
*   `create_pdf_report_async`: Асинхронно преобразует HTML-контент в PDF-отчет.
*   `create_docx_report_async`: Асинхронно создает DOCX-файл на основе HTML-отчета.

### `__init__`

```python
def __init__(self, 
             if_need_pdf:Optional[bool] = True, 
             if_need_docx:Optional[bool] = True, 
        ):
    """Определение, какие форматы данных требуется вернуть"""
    ...
```

**Назначение**: Инициализирует объект `ReportGenerator`.

**Параметры**:
- `if_need_pdf` (Optional[bool]): Если `True`, генерируется PDF отчет. По умолчанию `True`.
- `if_need_docx` (Optional[bool]): Если `True`, генерируется DOCX отчет. По умолчанию `True`.

**Как работает функция**:

1.  Устанавливает значения атрибутов `if_need_pdf` и `if_need_docx` на основе переданных аргументов.

### `create_reports_async`

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

**Назначение**: Асинхронно создает отчеты во всех поддерживаемых форматах (HTML, PDF, DOCX).

**Параметры**:
- `bot` (telebot.TeleBot): Объект телеграм-бота.
- `chat_id` (int): ID чата телеграм.
- `data` (dict): Данные для отчета.
- `lang` (str): Язык отчета.
- `mexiron_name` (str): Имя мехирона.

**Возвращает**:
- `tuple`: Кортеж с результатами выполнения (пока не определен).

**Как работает функция**:

1.  Формирует пути к файлам HTML, PDF и DOCX.
2.  Генерирует HTML-контент с помощью метода `create_html_report_async`.
3.  Если требуется, генерирует PDF-отчет с помощью метода `create_pdf_report_async`.
4.  Если требуется, генерирует DOCX-отчет с помощью метода `create_docx_report_async`.

### `service_apendix`

```python
def service_apendix(self, lang:str) -> dict:
    return  {
            "product_id":"00000",
            "product_name":"Сервис" if lang == 'ru' else "שירות",
            "specification":Path(__root__ / 'src' / 'endpoints' / Config.ENDPOINT / 'report_generator' / 'templates' / f'service_as_product_{lang}.html').read_text(encoding='UTF-8').replace('/n','<br>'),
            "image_local_saved_path":random_image(self.storage_path / 'converted_images' )
            }
```

**Назначение**: Создает словарь с информацией об услуге для добавления в отчет.

**Параметры**:
- `lang` (str): Язык отчета.

**Возвращает**:
- `dict`: Словарь с информацией об услуге.

**Как работает функция**:

1.  Определяет название услуги в зависимости от языка.
2.  Читает спецификацию услуги из HTML-шаблона.
3.  Генерирует случайное изображение для услуги.
4.  Возвращает словарь с информацией об услуге.

### `create_html_report_async`

```python
async def create_html_report_async(self, data:dict, lang:str, html_path:Optional[ str|Path] ) -> str:
    """
    Генерирует HTML-контент на основе шаблона и данных.

    Args:
        lang (str): Язык отчёта.

    Returns:
        str: HTML-контент.
    """
    ...
```

**Назначение**: Асинхронно генерирует HTML-контент на основе шаблона и данных.

**Параметры**:
- `data` (dict): Данные для отчета.
- `lang` (str): Язык отчета.
- `html_path` (Optional[str | Path]): Путь для сохранения HTML-файла

**Возвращает**:
- `str`: HTML-контент.

**Как работает функция**:

1.  Определяет путь к шаблону HTML в зависимости от языка.
2.  Загружает шаблон HTML.
3.  Рендерит шаблон с использованием данных и добавляет информацию об услуге.
4.  Сохраняет HTML-контент в файл.

### `create_pdf_report_async`

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
    ...
```

**Назначение**: Асинхронно генерирует PDF-отчет на основе HTML-контента.

**Параметры**:
- `data` (dict): Данные для отчета.
- `lang` (str): Язык отчета.
- `pdf_path` (str | Path): Путь для сохранения PDF-файла

**Возвращает**:
- `bool`: `True`, если PDF-отчет успешно создан и отправлен, иначе `False`.

**Как работает функция**:

1.  Преобразует HTML-контент в PDF с использованием библиотеки `pdfkit`.
2.  Отправляет PDF-файл пользователю через телеграм-бота.

### `create_docx_report_async`

```python
async def create_docx_report_async(self, html_path:str|Path, docx_path:str|Path) -> bool :
    """Создаю docx файл """
    ...
```

**Назначение**: Асинхронно создает DOCX-файл на основе HTML-отчета.

**Параметры**:
- `html_path` (str | Path): Путь к HTML-файлу.
- `docx_path` (str | Path): Путь для сохранения DOCX-файла

**Возвращает**:
- `bool`: `True`, если DOCX-файл успешно создан, иначе `False`.

**Как работает функция**:

1.  Преобразует HTML-файл в DOCX-файл с помощью функции `html_to_docx`.

## Функции

### `main`

```python
def main(maxiron_name:str, lang:str) ->bool:
    ...
```

**Назначение**: Главная функция модуля, запускающая процесс создания отчетов.

**Параметры**:
- `maxiron_name` (str): Имя мехирона.
- `lang` (str): Язык отчета.

**Как работает функция**:

1.  Формирует пути к файлам данных и отчетов.
2.  Загружает данные из JSON-файла.
3.  Создает экземпляр класса `ReportGenerator`.
4.  Вызывает метод `create_reports_async` для генерации отчетов.

## Примеры

В конце модуля приведен пример вызова функции `main` с указанием имени мехирона и языка.
```python
if __name__ == "__main__":
    maxiron_name = '250127221657987' # <- debug
    lang:str = 'ru'
    
    main(maxiron_name, lang)