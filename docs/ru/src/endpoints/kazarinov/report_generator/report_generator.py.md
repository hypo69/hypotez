# Модуль `report_generator.py`

## Обзор

Модуль предназначен для генерации отчётов в формате HTML, PDF и DOCX на основе данных из JSON. Отчёты формируются для мехиронов Казаринова.

## Подробней

Модуль содержит класс `ReportGenerator`, который отвечает за создание отчетов. Он использует шаблоны Jinja2 для генерации HTML, а затем конвертирует HTML в PDF и DOCX.
Основные этапы работы:

1.  Инициализация экземпляра класса `ReportGenerator` с указанием необходимости генерации PDF и DOCX.
2.  Загрузка данных из JSON-файла.
3.  Генерация HTML-контента на основе шаблона и загруженных данных.
4.  Преобразование HTML-контента в PDF и DOCX файлы.
5.  Сохранение сгенерированных отчетов в указанные пути.

## Классы

### `ReportGenerator`

**Описание**: Класс для генерации HTML- и PDF-отчётов на основе данных из JSON.

**Принцип работы**:

Класс `ReportGenerator` предназначен для создания отчетов в различных форматах (HTML, PDF, DOCX) на основе данных, полученных из JSON. Он использует шаблоны Jinja2 для генерации HTML, а затем конвертирует HTML в PDF и DOCX.

**Атрибуты**:

*   `if_need_html` (bool): Флаг, указывающий на необходимость создания HTML-отчета.
*   `if_need_pdf` (bool): Флаг, указывающий на необходимость создания PDF-отчета.
*   `if_need_docx` (bool): Флаг, указывающий на необходимость создания DOCX-отчета.
*   `storage_path` (Path): Путь к хранилищу отчетов. По умолчанию `Path(gs.path.external_storage, ENDPOINT)`.
*   `html_path` (Path | str): Путь к HTML-файлу.
*   `pdf_path` (Path | str): Путь к PDF-файлу.
*   `docs_path` (Path | str): Путь к DOCX-файлу.
*   `html_content` (str): Содержимое HTML-отчета.
*   `data` (dict): Данные для генерации отчета.
*   `lang` (str): Язык отчета.
*   `mexiron_name` (str): Имя мехирона.
*   `env` (Environment): Окружение Jinja2 для работы с шаблонами.

**Методы**:

*   `__init__`: Инициализирует объект `ReportGenerator` и определяет, какие форматы отчетов требуется создать.
*   `create_reports_async`: Создает все типы отчетов: HTML, PDF и DOCX.
*   `service_apendix`: Формирует структуру для добавления сервисной информации в отчет.
*   `create_html_report_async`: Генерирует HTML-контент на основе шаблона и данных.
*   `create_pdf_report_async`: Генерирует PDF-отчет на основе HTML-контента.
*   `create_docx_report_async`: Создает DOCX-файл на основе HTML.

### `ReportGenerator.__init__`

```python
def __init__(self, 
             if_need_pdf: Optional[bool] = True, 
             if_need_docx: Optional[bool] = True
            ) -> None:
    """Определение, какие форматы данных требуется вернуть"""
```

**Назначение**: Инициализирует экземпляр класса `ReportGenerator`.

**Параметры**:

*   `if_need_pdf` (Optional[bool], optional): Флаг, указывающий на необходимость создания PDF-отчета. По умолчанию `True`.
*   `if_need_docx` (Optional[bool], optional): Флаг, указывающий на необходимость создания DOCX-отчета. По умолчанию `True`.

**Возвращает**:

*   `None`: Функция ничего не возвращает.

**Как работает функция**:

1.  Присваивает значения атрибутам `self.if_need_pdf` и `self.if_need_docx` на основе переданных аргументов.

```
Инициализация класса
↓
Присваивание значений атрибутам self.if_need_pdf и self.if_need_docx
```

**Примеры**:

```python
report_generator = ReportGenerator(if_need_pdf=True, if_need_docx=False)
print(report_generator.if_need_pdf)  # Вывод: True
print(report_generator.if_need_docx) # Вывод: False

report_generator = ReportGenerator()
print(report_generator.if_need_pdf)  # Вывод: True
print(report_generator.if_need_docx) # Вывод: True
```

### `ReportGenerator.create_reports_async`

```python
async def create_reports_async(self,
                                 bot: telebot.TeleBot,
                                 chat_id: int,
                                 data: dict,
                                 lang: str,
                                 mexiron_name: str
                                 ) -> tuple:
    """Create ALL types: HTML, PDF, DOCX"""
    ...
```

**Назначение**: Создает отчеты во всех необходимых форматах (HTML, PDF, DOCX).

**Параметры**:

*   `bot` (telebot.TeleBot): Экземпляр бота Telebot для отправки отчетов.
*   `chat_id` (int): ID чата, куда отправлять отчеты.
*   `data` (dict): Данные для отчета.
*   `lang` (str): Язык отчета.
*   `mexiron_name` (str): Имя мехирона.

**Возвращает**:

*   `tuple`: Функция ничего не возвращает.

**Как работает функция**:

1.  Устанавливает атрибут `self.mexiron_name` равным переданному имени мехирона.
2.  Определяет пути для сохранения HTML, PDF и DOCX файлов в директории `export_path`.
3.  Вызывает метод `create_html_report_async` для создания HTML-отчета и сохраняет результат в `self.html_content`.
4.  Если `self.html_content` не был создан, функция завершается.
5.  Если `self.if_need_pdf` имеет значение `True`, вызывается метод `create_pdf_report_async` для создания PDF-отчета.
6.  Если `self.if_need_docx` имеет значение `True`, вызывается метод `create_docx_report_async` для создания DOCX-отчета.

```
Установка имени мехирона
↓
Определение путей для сохранения отчетов
↓
Создание HTML-отчета
↓
Проверка, создан ли HTML-отчет
│   └── Нет: Завершение
└── Да:
    ↓
    Проверка необходимости создания PDF
    │   └── Да: Создание PDF-отчета
    └── Нет: 
        ↓
        Проверка необходимости создания DOCX
        │   └── Да: Создание DOCX-отчета
        └── Нет: Завершение
```

**Примеры**:

```python
# Для примера необходимо создать экземпляр бота и chat_id
#bot = telebot.TeleBot(token='YOUR_TELEBOT_TOKEN')
#chat_id = 123456789

#data = {'products': [{'product_id': '123', 'product_name': 'Test'}]}
#lang = 'ru'
#mexiron_name = 'TestMexiron'

#report_generator = ReportGenerator(if_need_pdf=True, if_need_docx=True)
#asyncio.run(report_generator.create_reports_async(bot, chat_id, data, lang, mexiron_name))
```

### `ReportGenerator.service_apendix`

```python
def service_apendix(self, lang: str) -> dict:
    """Формирует структуру для добавления сервисной информации в отчет."""
    return  {
            "product_id":"00000",
            "product_name":"Сервис" if lang == 'ru' else "שירות",
            "specification":Path(__root__ / 'src' / 'endpoints' / ENDPOINT / 'report_generator' / 'templates' / f'service_as_product_{lang}.html').read_text(encoding='UTF-8').replace('/n','<br>'),
            "image_local_saved_path":random_image(self.storage_path / 'converted_images' )
            }
    ...
```

**Назначение**: Формирует словарь с информацией о сервисе для добавления в отчет.

**Параметры**:

*   `lang` (str): Язык, на котором должна быть представлена информация о сервисе.

**Возвращает**:

*   `dict`: Словарь с информацией о сервисе, включающий `product_id`, `product_name`, `specification` и `image_local_saved_path`.

**Как работает функция**:

1.  Определяет название сервиса в зависимости от языка (`"Сервис"` для русского и `"שירות"` для других языков).
2.  Читает содержимое HTML-файла, содержащего спецификацию сервиса, в зависимости от языка. Заменяет символы новой строки (`/n`) на тег `<br>`.
3.  Формирует словарь с информацией о сервисе, включая ID продукта, название, спецификацию и путь к изображению.

```
Определение названия сервиса в зависимости от языка
↓
Чтение содержимого HTML-файла спецификации сервиса
↓
Формирование словаря с информацией о сервисе
```

**Примеры**:

```python
report_generator = ReportGenerator()
service_info_ru = report_generator.service_apendix(lang='ru')
print(service_info_ru['product_name'])  # Вывод: Сервис

service_info_he = report_generator.service_apendix(lang='he')
print(service_info_he['product_name'])  # Вывод: שירות
```

### `ReportGenerator.create_html_report_async`

```python
async def create_html_report_async(self, data: dict, lang: str, html_path: Optional[str | Path]) -> str | None:
    """
    Генерирует HTML-контент на основе шаблона и данных.

    Args:
        data (dict): Данные для заполнения шаблона.
        lang (str): Язык отчёта.
        html_path (Optional[str | Path]): Путь для сохранения HTML-файла.

    Returns:
        str | None: HTML-контент.
    """
    self.html_path = html_path if html_path and isinstance(html_path, str) else Path(
        html_path) or self.html_path

    try:
        service_apendix = self.service_apendix(lang)
        data['products'].append(service_apendix)
        template: str = 'template_table_he.html' if lang == 'he' else 'template_table_ru.html'
        template_path: str = str(gs.path.endpoints / ENDPOINT / 'report_generator' / 'templates' / template)
        # template = self.env.get_template(self.template_path)
        template_string = Path(template_path).read_text(encoding='UTF-8')
        template = self.env.from_string(template_string)
        self.html_content: str = template.render(**data)

        try:
            Path(self.html_path).write_text(data=self.html_content, encoding='UTF-8')
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

*   `data` (dict): Данные для заполнения шаблона.
*   `lang` (str): Язык отчёта.
*   `html_path` (Optional[str | Path]): Путь для сохранения HTML-файла.

**Возвращает**:

*   `str | None`: HTML-контент или `None` в случае ошибки.

**Как работает функция**:

1.  Определяет путь для сохранения HTML-файла. Если `html_path` передан и является строкой, то он используется, иначе преобразуется в объект `Path` или используется значение по умолчанию `self.html_path`.
2.  Добавляет информацию о сервисе в данные отчета, используя метод `service_apendix`.
3.  Определяет имя шаблона в зависимости от языка (`template_table_he.html` для иврита и `template_table_ru.html` для русского).
4.  Формирует путь к шаблону.
5.  Читает содержимое шаблона из файла.
6.  Создает объект шаблона Jinja2 из строки.
7.  Генерирует HTML-контент на основе шаблона и данных.
8.  Пытается сохранить HTML-контент в файл. Если не удается, логирует ошибку и возвращает сгенерированный HTML-контент.
9.  Логирует информацию об успешном сохранении файла.

```
Определение пути для сохранения HTML-файла
↓
Добавление информации о сервисе в данные
↓
Определение имени шаблона в зависимости от языка
↓
Формирование пути к шаблону
↓
Чтение содержимого шаблона из файла
↓
Создание объекта шаблона Jinja2
↓
Генерация HTML-контента
↓
Попытка сохранения HTML-контента в файл
│
└── Успешно: Логирование успешного сохранения
│           └── Возврат HTML-контента
│
└── Ошибка:  Логирование ошибки сохранения
            └── Возврат HTML-контента
```

**Примеры**:

```python
# Пример использования
# report_generator = ReportGenerator()
# data = {'products': []}
# lang = 'ru'
# html_path = 'report.html'
# html_content = asyncio.run(report_generator.create_html_report_async(data, lang, html_path))
# if html_content:
#     print("HTML-контент успешно сгенерирован")
# else:
#     print("Не удалось сгенерировать HTML-контент")
```

### `ReportGenerator.create_pdf_report_async`

```python
async def create_pdf_report_async(self, 
                                    data: dict, 
                                    lang: str, 
                                    pdf_path: str | Path) -> bool:
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

**Назначение**: Генерирует PDF-отчет из HTML-контента.

**Параметры**:

*   `data` (dict): Данные для отчета.
*   `lang` (str): Язык отчета.
*   `pdf_path` (str | Path): Путь для сохранения PDF-файла.

**Возвращает**:

*   `bool`: `True`, если PDF-отчет успешно создан и отправлен (если `self.bot` определен), `False` в противном случае.

**Как работает функция**:

1.  Определяет путь для сохранения PDF-файла. Если `pdf_path` передан и является строкой или объектом `Path`, то он используется, иначе используется значение по умолчанию `self.pdf_path`.
2.  Если переданы данные, присваивает их `self.html_content`, иначе использует существующий `self.html_content`.
3.  Инициализирует класс `PDFUtils` для работы с PDF.
4.  Сохраняет HTML-контент в PDF-файл с использованием метода `save_pdf_pdfkit` из `PDFUtils`.
5.  Если сохранение не удалось, логирует ошибку и отправляет сообщение об ошибке в чат (если `self.bot` определен).
6.  Если `self.bot` определен, пытается отправить PDF-файл в чат.
7.  Возвращает `True`, если отправка удалась, и `False` в случае ошибки.

```
Определение пути для сохранения PDF-файла
↓
Инициализация класса PDFUtils
↓
Сохранение HTML-контента в PDF-файл
│
└── Успешно: Проверка наличия бота
│           └── Бот есть:  Попытка отправки PDF-файла в чат
│                           └── Успешно: Возврат True
│                           └── Ошибка: Отправка сообщения об ошибке
│                                       └── Возврат False
│           └── Бот нет:   Возврат True
│
└── Ошибка: Логирование ошибки сохранения
            └── Проверка наличия бота
                └── Бот есть: Отправка сообщения об ошибке
                └── Бот нет:   Возврат False
```

**Примеры**:

```python
# Пример использования
# report_generator = ReportGenerator()
# data = "<html><body><h1>Test Report</h1></body></html>"
# lang = 'ru'
# pdf_path = 'report.pdf'
# bot = telebot.TeleBot(token='YOUR_TELEBOT_TOKEN')  # Замените на токен вашего бота
# chat_id = 123456789  # Замените на ID чата
# report_generator.bot = bot
# report_generator.chat_id = chat_id
# result = asyncio.run(report_generator.create_pdf_report_async(data, lang, pdf_path))
# if result:
#     print("PDF-отчет успешно создан и отправлен")
# else:
#     print("Не удалось создать или отправить PDF-отчет")
```

### `ReportGenerator.create_docx_report_async`

```python
async def create_docx_report_async(self, html_path: str | Path, docx_path: str | Path) -> bool:
    """Создаю docx файл """

    if not html_to_docx(self.html_path, docx_path):
        logger.error(f"Не скопмилировался DOCX.")
        return False
    return True
```

**Назначение**: Создает DOCX-файл на основе HTML-файла.

**Параметры**:

*   `html_path` (str | Path): Путь к HTML-файлу.
*   `docx_path` (str | Path): Путь для сохранения DOCX-файла.

**Возвращает**:

*   `bool`: `True`, если DOCX-файл успешно создан, `False` в противном случае.

**Как работает функция**:

1.  Использует функцию `html_to_docx` для конвертации HTML-файла в DOCX-файл.
2.  Если конвертация не удалась, логирует ошибку и возвращает `False`.
3.  В случае успеха возвращает `True`.

```
Конвертация HTML-файла в DOCX-файл
│
└── Успешно: Возврат True
└── Ошибка: Логирование ошибки
            └── Возврат False
```

**Примеры**:

```python
# Пример использования
# report_generator = ReportGenerator()
# html_path = 'report.html'
# docx_path = 'report.docx'
# result = asyncio.run(report_generator.create_docx_report_async(html_path, docx_path))
# if result:
#     print("DOCX-файл успешно создан")
# else:
#     print("Не удалось создать DOCX-файл")
```

## Функции

### `main`

```python
def main(maxiron_name: str, lang: str) -> bool:
    """Функция генерирует HTML, PDF и DOCX файлы для указанного мехирона и языка."""
    external_storage: Path = gs.path.external_storage / ENDPOINT / 'mexironim' / maxiron_name
    data: dict = j_loads(external_storage / f'{maxiron_name}_{lang}.json')
    html_path: Path = external_storage / f'{maxiron_name}_{lang}.html'
    pdf_path: Path = external_storage / f'{maxiron_name}_{lang}.pdf'
    docx_path: Path = external_storage / f'{maxiron_name}_{lang}.docx'
    if_need_html: bool = True
    if_need_pdf: bool = True
    if_need_docx: bool = True
    r = ReportGenerator(if_need_html, if_need_pdf, if_need_docx, html_path, pdf_path, docx_path)

    asyncio.run(r.create_reports_async(data,
                                        maxiron_name,
                                        lang,
                                        html_path,
                                        pdf_path,
                                        docx_path, ))
```

**Назначение**: Генерирует HTML, PDF и DOCX файлы для указанного мехирона и языка.

**Параметры**:

*   `maxiron_name` (str): Имя мехирона.
*   `lang` (str): Язык отчета.

**Возвращает**:

*   `bool`: Функция ничего не возвращает.

**Как работает функция**:

1.  Определяет путь к внешнему хранилищу, где хранятся данные и будут сохранены отчеты.
2.  Загружает данные из JSON-файла.
3.  Определяет пути для HTML, PDF и DOCX файлов.
4.  Устанавливает флаги `if_need_html`, `if_need_pdf` и `if_need_docx` в `True`.
5.  Создает экземпляр класса `ReportGenerator`.
6.  Запускает асинхронную функцию `create_reports_async` для генерации отчетов.

```
Определение пути к внешнему хранилищу
↓
Загрузка данных из JSON-файла
↓
Определение путей для HTML, PDF и DOCX файлов
↓
Создание экземпляра класса ReportGenerator
↓
Запуск асинхронной функции create_reports_async
```

**Примеры**:

```python
# Пример использования
# main(maxiron_name='250127221657987', lang='ru')