# Модуль `report_generator`

## Обзор

Модуль предназначен для генерации отчетов в форматах HTML и PDF на основе данных, полученных в формате JSON. 
Модуль является частью endpoint'а `kazarinov` и используется для формирования отчетов для "мехиронов" (mexironim).

## Подробней

Модуль содержит класс `ReportGenerator`, который выполняет следующие функции:

- Инициализация параметров отчета, таких как необходимость генерации PDF и DOCX.
- Создание HTML-отчета на основе шаблона Jinja2 и данных.
- Преобразование HTML-отчета в формат PDF.
- Сохранение отчетов в указанные пути.

Модуль использует библиотеки `jinja2` для генерации HTML из шаблонов, `pdfkit` или другие инструменты для конвертации HTML в PDF, а также вспомогательные функции из других модулей проекта для чтения/записи файлов и обработки изображений.

## Классы

### `Config`

**Описание**: Класс конфигурации, содержащий endpoint для отчетов `kazarinov`.

**Атрибуты**:
- `ENDPOINT` (str): Строка, содержащая название endpoint'а ('kazarinov').

### `ReportGenerator`

**Описание**: Класс для генерации отчетов в формате HTML и PDF.

**Атрибуты**:
- `if_need_html` (bool): Флаг, определяющий необходимость генерации HTML-отчета.
- `if_need_pdf` (bool): Флаг, определяющий необходимость генерации PDF-отчета.
- `if_need_docx` (bool): Флаг, определяющий необходимость генерации DOCX-отчета.
- `storage_path` (Path): Путь к директории хранения отчетов. По умолчанию использует `gs.path.external_storage` и `Config.ENDPOINT`.
- `html_path` (Path | str): Путь к HTML-файлу.
- `pdf_path` (Path | str): Путь к PDF-файлу.
- `docs_path` (Path | str): Путь к DOCX-файлу.
- `html_content` (str): Содержимое HTML-отчета.
- `data` (dict): Данные для генерации отчета.
- `lang` (str): Язык отчета.
- `mexiron_name` (str): Имя "мехирона", для которого генерируется отчет.
- `env` (Environment): Объект окружения Jinja2 для загрузки шаблонов.

**Методы**:
- `__init__`: Инициализирует объект `ReportGenerator`.
- `create_reports_async`: Создает отчеты всех требуемых типов (HTML, PDF, DOCX).
- `service_apendix`: Подготавливает данные для сервисного приложения.
- `create_html_report_async`: Генерирует HTML-отчет на основе шаблона и данных.
- `create_pdf_report_async`: Генерирует PDF-отчет на основе HTML-контента.
- `create_docx_report_async`: Создает DOCX-файл на основе HTML.

## Методы класса

### `__init__(self, if_need_pdf: Optional[bool] = True, if_need_docx: Optional[bool] = True)`

**Назначение**: Инициализирует объект `ReportGenerator` и определяет, какие форматы отчетов необходимо генерировать.

**Параметры**:
- `if_need_pdf` (Optional[bool], optional): Флаг, указывающий на необходимость генерации PDF-отчета. По умолчанию `True`.
- `if_need_docx` (Optional[bool], optional): Флаг, указывающий на необходимость генерации DOCX-отчета. По умолчанию `True`.

```python
def __init__(self, 
                 if_need_pdf:Optional[bool] = True, 
                 if_need_docx:Optional[bool] = True, 
            ):
        """Определение, какие форматы данных требуется вернуть"""
```

### `create_reports_async(self, bot: telebot.TeleBot, chat_id: int, data: dict, lang: str, mexiron_name: str) -> tuple`

**Назначение**: Создает отчеты всех требуемых типов: HTML, PDF, DOCX.

**Параметры**:
- `bot` (telebot.TeleBot): Объект бота Telegram для отправки отчетов.
- `chat_id` (int): ID чата Telegram, куда отправлять отчеты.
- `data` (dict): Данные для генерации отчета.
- `lang` (str): Язык отчета.
- `mexiron_name` (str): Имя "мехирона", для которого генерируется отчет.

```python
async def create_reports_async(self,
                             bot: telebot.TeleBot,
                             chat_id: int,
                             data:dict,
                             lang:str,
                             mexiron_name:str,
                             ) -> tuple:
        """Create ALL types: HTML, PDF, DOCX"""
```

### `service_apendix(self, lang: str) -> dict`

**Назначение**: Подготавливает данные для сервисного приложения, такие как ID продукта, имя продукта, спецификация и путь к изображению.

**Параметры**:
- `lang` (str): Язык отчета.

**Возвращает**:
- `dict`: Словарь с данными для сервисного приложения.

```python
def service_apendix(self, lang:str) -> dict:
        return  {
                "product_id":"00000",
                "product_name":"Сервис" if lang == 'ru' else "שירות",
                "specification":Path(__root__ / 'src' / 'endpoints' / Config.ENDPOINT / 'report_generator' / 'templates' / f'service_as_product_{lang}.html').read_text(encoding='UTF-8').replace('/n','<br>'),
                "image_local_saved_path":random_image(self.storage_path / 'converted_images' )
                }
```

### `create_html_report_async(self, data: dict, lang: str, html_path: Optional[str | Path]) -> str`

**Назначение**: Генерирует HTML-контент на основе шаблона и данных.

**Параметры**:
- `data` (dict): Данные для генерации отчета.
- `lang` (str): Язык отчета.
- `html_path` (Optional[str | Path], optional): Путь для сохранения HTML-файла. По умолчанию `None`.

**Возвращает**:
- `str`: HTML-контент.

```python
async def create_html_report_async(self, data:dict, lang:str, html_path:Optional[ str|Path] ) -> str:
        """
        Генерирует HTML-контент на основе шаблона и данных.

        Args:
            lang (str): Язык отчёта.

        Returns:
            str: HTML-контент.
        """
```

### `create_pdf_report_async(self, data: dict, lang: str, pdf_path: str | Path) -> bool`

**Назначение**: Генерирует PDF-отчет на основе HTML-контента.

**Параметры**:
- `data` (dict): Данные для генерации отчета.
- `lang` (str): Язык отчета.
- `pdf_path` (str | Path): Путь для сохранения PDF-файла.

**Возвращает**:
- `bool`: `True`, если PDF-отчет успешно создан и отправлен (если указан бот), иначе `False`.

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

### `create_docx_report_async(self, html_path: str | Path, docx_path: str | Path) -> bool`

**Назначение**: Создает DOCX-файл на основе HTML.

**Параметры**:
- `html_path` (str | Path): Путь к HTML-файлу.
- `docx_path` (str | Path): Путь для сохранения DOCX-файла.

**Возвращает**:
- `bool`: `True`, если DOCX-файл успешно создан, иначе `False`.

```python
async def create_docx_report_async(self, html_path:str|Path, docx_path:str|Path) -> bool :
        """Создаю docx файл """
```

## Функции

### `main(maxiron_name: str, lang: str) -> bool`

**Назначение**: Главная функция для запуска процесса генерации отчетов.

**Параметры**:
- `maxiron_name` (str): Имя "мехирона", для которого генерируется отчет.
- `lang` (str): Язык отчета.

```python
def main(maxiron_name:str, lang:str) ->bool:
```
## Примеры

```python
if __name__ == "__main__":
    maxiron_name = '250127221657987' # <- debug
    lang:str = 'ru'
    
    main(maxiron_name, lang)
```
В данном примере вызывается функция `main` с именем "мехирона" `'250127221657987'` и языком отчета `'ru'`.