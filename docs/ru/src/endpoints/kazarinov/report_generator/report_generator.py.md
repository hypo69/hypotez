# Модуль `report_generator`

## Обзор

Модуль предназначен для генерации HTML и PDF отчетов для мехиронов Казаринова на основе данных из JSON файлов. Он использует шаблонизатор Jinja2 для создания HTML, а затем преобразует его в PDF с помощью pdfkit. Модуль также поддерживает создание DOCX файлов.

## Подробней

Модуль предоставляет класс `ReportGenerator`, который содержит методы для загрузки данных, генерации HTML, сохранения HTML в файл, преобразования HTML в PDF и создания отчета. Основная цель модуля - автоматизировать процесс создания отчетов на основе структурированных данных.

## Классы

### `ReportGenerator`

**Описание**: Класс для генерации HTML- и PDF-отчётов на основе данных из JSON.

**Принцип работы**:
Класс инициализируется с параметрами, указывающими, какие типы отчетов необходимо создать (PDF, DOCX). Он также содержит методы для загрузки данных, рендеринга HTML с использованием Jinja2, сохранения HTML в файл и преобразования HTML в PDF.

**Атрибуты**:

- `if_need_html` (bool): Флаг, указывающий, нужно ли генерировать HTML отчет.
- `if_need_pdf` (bool): Флаг, указывающий, нужно ли генерировать PDF отчет.
- `if_need_docx` (bool): Флаг, указывающий, нужно ли генерировать DOCX отчет.
- `storage_path` (Path): Путь к директории для хранения сгенерированных отчетов.
- `html_path` (Path | str): Путь к HTML файлу.
- `pdf_path` (Path | str): Путь к PDF файлу.
- `docs_path` (Path | str): Путь к DOCX файлу.
- `html_content` (str): Содержимое HTML отчета.
- `data` (dict): Данные для генерации отчета.
- `lang` (str): Язык отчета.
- `mexiron_name` (str): Имя мехирона.
- `env` (Environment): Экземпляр окружения Jinja2 для работы с шаблонами.

**Методы**:

- `__init__`: Инициализирует объект `ReportGenerator`.
- `create_reports_async`: Создает HTML, PDF и DOCX отчеты асинхронно.
- `service_apendix`: Возвращает словарь с данными для сервисного приложения.
- `create_html_report_async`: Генерирует HTML контент на основе шаблона и данных.
- `create_pdf_report_async`: Генерирует PDF отчет на основе HTML контента.
- `create_docx_report_async`: Создает DOCX файл на основе HTML файла.

### `__init__`

```python
def __init__(self, 
             if_need_pdf:Optional[bool] = True, 
             if_need_docx:Optional[bool] = True, 
        ):
    """Определение, какие форматы данных требуется вернуть"""
```

**Назначение**: Инициализирует экземпляр класса `ReportGenerator`.

**Параметры**:

- `if_need_pdf` (Optional[bool], optional): Флаг, указывающий, нужно ли генерировать PDF отчет. По умолчанию `True`.
- `if_need_docx` (Optional[bool], optional): Флаг, указывающий, нужно ли генерировать DOCX отчет. По умолчанию `True`.

**Возвращает**:
    - None

**Как работает функция**:
1. Устанавливает значения атрибутов `if_need_pdf` и `if_need_docx` на основе переданных параметров.

**Примеры**:

```python
report_generator = ReportGenerator(if_need_pdf=True, if_need_docx=False)
```

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
    self.mexiron_name = mexiron_name 
    export_path = self.storage_path / 'mexironim' / self.mexiron_name

    self.html_path = export_path / f"{self.mexiron_name}_{lang}.html"
    self.pdf_path = export_path / f"{self.mexiron_name}_{lang}.pdf"
    self.docx_path = export_path / f"{self.mexiron_name}_{lang}.docx"
    self.bot = bot
    self.chat_id = chat_id

    self.html_content = await self.create_html_report_async(data, lang, self.html_path)

    if not self.html_content:
        return False


    if self.if_need_pdf:
        await self.create_pdf_report_async(self.html_content, lang, self.pdf_path)

    if self.if_need_docx:
        await self.create_pdf_report_async(self.html_content, lang, self.pdf_path)
```

**Назначение**: Создает HTML, PDF и DOCX отчеты асинхронно.

**Параметры**:

- `bot` (telebot.TeleBot): Экземпляр Telegram бота для отправки уведомлений.
- `chat_id` (int): ID чата для отправки уведомлений.
- `data` (dict): Данные для генерации отчета.
- `lang` (str): Язык отчета.
- `mexiron_name` (str): Имя мехирона.

**Возвращает**:
- `tuple`: Кортеж, содержащий пути к сгенерированным файлам.

**Как работает функция**:

```
A[Установка имени мехирона и путей для экспорта]
|
B[Создание HTML отчета]
|
C[Проверка, создан ли HTML отчет]
|
D[Создание PDF отчета (если необходимо)]
|
E[Создание DOCX отчета (если необходимо)]
```

A: Устанавливает имя мехирона и формирует пути для сохранения HTML, PDF и DOCX файлов.
B: Вызывает метод `create_html_report_async` для генерации HTML контента.
C: Проверяет, успешно ли создан HTML контент. Если нет, возвращает `False`.
D: Если флаг `if_need_pdf` установлен в `True`, вызывает метод `create_pdf_report_async` для генерации PDF отчета.
E: Если флаг `if_need_docx` установлен в `True`, вызывает метод `create_pdf_report_async` для генерации DOCX отчета.

**Примеры**:

```python
bot = telebot.TeleBot('YOUR_TELEGRAM_BOT_TOKEN')
chat_id = 123456789
data = {'products': []}
lang = 'ru'
mexiron_name = 'test_mexiron'

report_generator = ReportGenerator(if_need_pdf=True, if_need_docx=True)
asyncio.run(report_generator.create_reports_async(bot, chat_id, data, lang, mexiron_name))
```

### `service_apendix`

```python
def service_apendix(self, lang:str) -> dict:
    return  {
            "product_id":"00000",
            "product_name":"Сервис" if lang == 'ru' else "שירות",
            "specification":Path(__root__ / 'src' / 'endpoints' / ENDPOINT / 'report_generator' / 'templates' / f'service_as_product_{lang}.html').read_text(encoding='UTF-8').replace('/n','<br>'),
            "image_local_saved_path":random_image(self.storage_path / 'converted_images' )
            }
```

**Назначение**: Создает словарь с информацией о сервисном приложении для добавления в отчет.

**Параметры**:
- `lang` (str): Язык, на котором должна быть информация о сервисе ("ru" или "he").

**Возвращает**:
- `dict`: Словарь с информацией о сервисном приложении, содержащий `product_id`, `product_name`, `specification` и `image_local_saved_path`.

**Как работает функция**:
1. Определяет название сервиса в зависимости от языка (`lang`). Если язык русский, название будет "Сервис", иначе "שירות" (иврит).
2. Считывает спецификацию сервиса из HTML-файла, расположенного в каталоге `templates`. Заменяет символы новой строки (`/n`) на теги `<br>`, чтобы обеспечить правильное отображение в HTML.
3. Генерирует случайное изображение для сервиса с помощью функции `random_image`.
4. Возвращает словарь, содержащий всю эту информацию.

**Примеры**:

```python
report_generator = ReportGenerator()
service_info = report_generator.service_apendix(lang='ru')
print(service_info)
```

### `create_html_report_async`

```python
async def create_html_report_async(self, data:dict, lang:str, html_path:Optional[ str|Path] ) -> str | None:
    """
    Генерирует HTML-контент на основе шаблона и данных.

    Args:
        lang (str): Язык отчёта.

    Returns:
        str: HTML-контент.
    """
    self.html_path = html_path if html_path and isinstance(html_path, str)  else Path(html_path) or self.html_path

    try:
        service_apendix = self.service_apendix(lang)
        data['products'].append(service_apendix)
        template:str = 'template_table_he.html' if lang == 'he' else  'template_table_ru.html'
        template_path: str  =  str(gs.path.endpoints / ENDPOINT / 'report_generator' / 'templates' / template)
        #template = self.env.get_template(self.template_path)
        template_string = Path(template_path).read_text(encoding = 'UTF-8')
        template = self.env.from_string(template_string)
        self.html_content:str = template.render(**data)

        try:
            Path(self.html_path).write_text(data = self.html_content, encoding='UTF-8')
        except Exception as ex:
            logger.error(f"Не удалось сохранить файл")
            return self.html_content
            

        logger.info(f"Файл HTML удачно сохранен в {html_path}")
        return self.html_content

    except Exception as ex:
        logger.error(f"Не удалось сгенерирпвать HTML файл {html_path}", ex)
        return 
```

**Назначение**: Генерирует HTML-контент на основе шаблона и данных.

**Параметры**:

- `data` (dict): Данные для заполнения шаблона.
- `lang` (str): Язык отчёта.
- `html_path` (Optional[str  |  Path], optional): Путь для сохранения HTML файла. По умолчанию `None`.

**Возвращает**:

- `str | None`: HTML-контент в виде строки, или `None` в случае ошибки.

**Как работает функция**:

```
A[Определение пути к HTML файлу]
|
B[Добавление сервисного приложения к данным]
|
C[Выбор шаблона в зависимости от языка]
|
D[Чтение шаблона и рендеринг HTML]
|
E[Сохранение HTML в файл]
|
F[Обработка исключений]
```

A: Определяет путь к HTML файлу. Если `html_path` передан и является строкой, использует его. В противном случае, использует `html_path` как `Path` или значение по умолчанию `self.html_path`.
B: Добавляет информацию о сервисном приложении к данным, используя метод `self.service_apendix(lang)`.
C: Выбирает шаблон в зависимости от языка: `template_table_he.html` для иврита (`he`), `template_table_ru.html` для русского (`ru`).
D: Читает содержимое выбранного шаблона из файла и рендерит HTML, подставляя данные с помощью Jinja2.
E: Сохраняет сгенерированный HTML контент в файл, указанный в `self.html_path`.
F: Обрабатывает исключения, которые могут возникнуть при чтении шаблона, рендеринге HTML или сохранении файла. В случае ошибки логирует информацию и возвращает `None`.

**Примеры**:

```python
data = {'products': []}
lang = 'ru'
html_path = 'report.html'
report_generator = ReportGenerator()
html_content = asyncio.run(report_generator.create_html_report_async(data, lang, html_path))
if html_content:
    print(f"HTML content: {html_content[:100]}...")
```

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
    pdf_path = pdf_path if pdf_path and isinstance(pdf_path, (str,Path)) else self.pdf_path

    self.html_content = data if data else self.html_content

    from src.utils.pdf import PDFUtils
    pdf = PDFUtils()

    if not pdf.save_pdf_pdfkit(self.html_content, pdf_path):
        logger.error(f"Не удалось сохранить PDF файл {pdf_path}")
        if self.bot: self.bot.send_message(self.chat_id, f"Не удалось сохранить файл {pdf_path}")
        ...
        return False
    

    if self.bot:
        try:
            with open(pdf_path, 'rb') as f:
                self.bot.send_document(self.chat_id, f)
                return True
        except Exception as ex:
            self.bot.send_message(self.chat_id, f"Не удалось отправить файл {pdf_path} по причине: {ex}")
            return False
```

**Назначение**: Генерирует PDF отчет на основе HTML контента.

**Параметры**:

- `data` (dict): Данные для генерации отчета (HTML контент).
- `lang` (str): Язык отчёта.
- `pdf_path` (str | Path): Путь для сохранения PDF файла.

**Возвращает**:

- `bool`: `True`, если PDF файл успешно создан и отправлен (если `bot` указан), `False` в случае ошибки.

**Как работает функция**:

```
A[Определение пути к PDF файлу]
|
B[Инициализация PDFUtils]
|
C[Сохранение PDF с использованием PDFUtils]
|
D[Отправка PDF файла через Telegram бот (если указан)]
```

A: Определяет путь к PDF файлу. Если `pdf_path` передан и является строкой или `Path`, использует его. В противном случае использует `self.pdf_path`.
B: Инициализирует класс `PDFUtils` из модуля `src.utils.pdf`.
C: Сохраняет HTML контент в PDF файл с использованием метода `save_pdf_pdfkit` класса `PDFUtils`. Если сохранение не удалось, логирует ошибку и отправляет сообщение через Telegram бот (если `bot` указан).
D: Если `bot` указан, пытается отправить PDF файл через Telegram. В случае успеха возвращает `True`, в случае ошибки отправляет сообщение об ошибке через Telegram и возвращает `False`.

**Примеры**:

```python
data = "<html><body><h1>Test Report</h1></body></html>"
lang = 'ru'
pdf_path = 'report.pdf'
report_generator = ReportGenerator()
result = asyncio.run(report_generator.create_pdf_report_async(data, lang, pdf_path))
print(f"PDF creation result: {result}")
```

### `create_docx_report_async`

```python
async def create_docx_report_async(self, html_path:str|Path, docx_path:str|Path) -> bool :
    """Создаю docx файл """

    if not html_to_docx(self.html_path, docx_path):
        logger.error(f"Не скопмилировался DOCX.")
        return False
    return True
```

**Назначение**: Создает DOCX файл на основе HTML файла.

**Параметры**:

- `html_path` (str | Path): Путь к HTML файлу.
- `docx_path` (str | Path): Путь для сохранения DOCX файла.

**Возвращает**:

- `bool`: `True`, если DOCX файл успешно создан, `False` в случае ошибки.

**Как работает функция**:

```
A[Преобразование HTML в DOCX]
|
B[Обработка ошибок]
```

A: Преобразует HTML файл в DOCX файл с использованием функции `html_to_docx` из модуля `src.utils.convertors.html2docx`.
B: Если преобразование не удалось, логирует ошибку и возвращает `False`. В противном случае возвращает `True`.

**Примеры**:

```python
html_path = 'report.html'
docx_path = 'report.docx'
report_generator = ReportGenerator()
result = asyncio.run(report_generator.create_docx_report_async(html_path, docx_path))
print(f"DOCX creation result: {result}")
```

## Функции

### `main`

```python
def main(maxiron_name:str, lang:str) ->bool:
    
    external_storage: Path =  gs.path.external_storage / ENDPOINT / 'mexironim' /  maxiron_name
    data: dict = j_loads(external_storage / f'{maxiron_name}_{lang}.json')
    html_path: Path =  external_storage / f'{maxiron_name}_{lang}.html' 
    pdf_path: Path = external_storage / f'{maxiron_name}_{lang}.pdf'
    docx_path: Path = external_storage / f'{maxiron_name}_{lang}.docx'
    if_need_html: bool = True
    if_need_pdf: bool = True
    if_need_docx: bool = True 
    r = ReportGenerator(if_need_html, if_need_pdf, if_need_docx, html_path, pdf_path, docx_path)

    asyncio.run( r.create_reports_async( data,
                                    maxiron_name,
                                    lang, 
                                    html_path, 
                                    pdf_path, 
                                    docx_path, )   
                )
```

**Назначение**: Главная функция для запуска процесса генерации отчетов.

**Параметры**:

- `maxiron_name` (str): Имя мехирона.
- `lang` (str): Язык отчета.

**Возвращает**:

- `bool`: Возвращает `True` в случае успешного выполнения, `False` в случае ошибки.

**Как работает функция**:

```
A[Определение путей к файлам и загрузка данных]
|
B[Создание экземпляра ReportGenerator]
|
C[Запуск асинхронного процесса создания отчетов]
```

A: Определяет пути к файлам HTML, PDF, DOCX и загружает данные из JSON файла с использованием функции `j_loads`.
B: Создает экземпляр класса `ReportGenerator` с параметрами, указывающими необходимость создания HTML, PDF и DOCX отчетов, а также путями к файлам.
C: Запускает асинхронный процесс создания отчетов с использованием метода `create_reports_async` класса `ReportGenerator`.

**Примеры**:

```python
maxiron_name = '250127221657987'
lang = 'ru'
main(maxiron_name, lang)