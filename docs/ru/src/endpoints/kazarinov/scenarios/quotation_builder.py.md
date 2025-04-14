# Модуль для создания коммерческих предложений
## Обзор

Модуль `quotation_builder.py` предназначен для автоматизации процесса извлечения, обработки и сохранения данных о продуктах от различных поставщиков. Он включает в себя функции для взаимодействия с веб-драйвером, обработки данных с использованием моделей искусственного интеллекта и подготовки отчетов. Модуль обеспечивает интеграцию с Facebook для публикации рекламных материалов.

## Подробней

Модуль выполняет следующие основные функции:
- Извлечение данных о продуктах из различных источников.
- Преобразование и форматирование данных для обработки моделями ИИ.
- Использование моделей ИИ для обработки данных и генерации описаний продуктов на разных языках.
- Сохранение обработанных данных о продуктах в формате JSON.
- Интеграция с Facebook для публикации рекламных материалов.
- Создание отчетов в форматах HTML, PDF и DOCX.

## Классы

### `QuotationBuilder`

**Описание**: Класс `QuotationBuilder` управляет процессом создания коммерческих предложений, включая извлечение данных о продуктах, их обработку с использованием ИИ и сохранение результатов.

**Принцип работы**:
Класс инициализируется с именем процесса (`mexiron_name`) и экземпляром веб-драйвера. Он загружает конфигурацию из JSON-файла, инициализирует модель ИИ Google Gemini и подготавливает пути для экспорта данных. Основные методы класса включают преобразование данных о продуктах, обработку данных с использованием ИИ, сохранение данных и публикацию рекламных материалов в Facebook.

**Атрибуты**:
- `base_path` (Path): Базовый путь к каталогу модуля.
- `config` (SimpleNamespace): Конфигурация, загруженная из JSON-файла.
- `html_path` (str | Path): Путь к HTML-файлу отчета.
- `pdf_path` (str | Path): Путь к PDF-файлу отчета.
- `docx_path` (str | Path): Путь к DOCX-файлу отчета.
- `driver` (Driver): Экземпляр веб-драйвера.
- `export_path` (Path): Путь для экспорта данных.
- `mexiron_name` (str): Имя процесса.
- `price` (float): Цена продукта.
- `timestamp` (str): Временная метка.
- `products_list` (List): Список обработанных данных о продуктах.
- `model` (GoogleGenerativeAI): Экземпляр модели ИИ Google Gemini.
- `translations` (SimpleNamespace): Переводы, загруженные из JSON-файла.
- `required_fields` (tuple): Кортеж необходимых полей продукта.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `QuotationBuilder`.
- `convert_product_fields`: Преобразует поля продукта в словарь.
- `process_llm`: Обрабатывает список продуктов с использованием модели ИИ.
- `process_llm_async`: Асинхронно обрабатывает список продуктов с использованием модели ИИ.
- `save_product_data`: Сохраняет данные продукта в файл.
- `post_facebook_async`: Публикует рекламные материалы в Facebook.

### `__init__`

```python
def __init__(self, mexiron_name:Optional[str] = gs.now, driver:Optional[Firefox | Playwrid | str] = None,  **kwards):
    """
    Initializes Mexiron class with required components.

    Args:
        driver (Driver): Selenium WebDriver instance.
        mexiron_name (Optional[str]): Custom name for the Mexiron process.
        webdriver_name (Optional[str]): Name of the WebDriver to use. Defaults to 'firefox'. call to Firefox or Playwrid
        window_mode (Optional[str]): Оконный режим вебдрайвера. Может быть 'maximized', 'headless', 'minimized', 'fullscreen', 'normal', 'hidden', 'kiosk'

    """
```

**Назначение**: Инициализирует класс `QuotationBuilder`, настраивая веб-драйвер, модель ИИ и пути для экспорта.

**Параметры**:
- `mexiron_name` (Optional[str]): Имя процесса. По умолчанию используется текущее время.
- `driver` (Optional[Firefox | Playwrid | str]): Экземпляр веб-драйвера или его название. По умолчанию используется Firefox.
- `**kwards`: Дополнительные аргументы для настройки веб-драйвера.

**Как работает функция**:

1. **Инициализация имени процесса и путей экспорта**:
   - Устанавливает имя процесса (`mexiron_name`).
   - Строит путь для экспорта данных, используя имя процесса. Если возникает ошибка при построении пути, логирует ошибку и завершает работу.

2. **Инициализация веб-драйвера**:
   - Проверяет, передан ли экземпляр драйвера.
   - Если передан экземпляр `Driver`, использует его.
   - Если передан класс `Firefox` или `Playwrid`, создает экземпляр `Driver` с этим классом.
   - Если передана строка, определяет, какой драйвер использовать (Firefox или Playwright), и создает соответствующий экземпляр `Driver`.
   - Если драйвер не передан, создает экземпляр `Driver` с `Firefox` по умолчанию.

3. **Инициализация модели Gemini**:
   - Читает системную инструкцию из файла.
   - Получает API-ключ для Gemini.
   - Инициализирует модель `GoogleGenerativeAI` с API-ключом и системной инструкцией.
   - Если возникает ошибка при загрузке модели, инструкции или API-ключа, логирует ошибку и завершает работу.

**Пример**:
```python
quotation = QuotationBuilder(mexiron_name='test_mexiron', driver='firefox', window_mode='headless')
```

### `convert_product_fields`

```python
def convert_product_fields(self, f: ProductFields) -> dict:
    """
    Converts product fields into a dictionary. 
    Функция конвертирует поля из объекта `ProductFields` в простой словарь для модели ии.


    Args:
        f (ProductFields): Object containing parsed product data.

    Returns:
        dict: Formatted product data dictionary.

    .. note:: Правила построения полей определяются в `ProductFields`
    """
```

**Назначение**: Преобразует поля продукта из объекта `ProductFields` в словарь.

**Параметры**:
- `f` (ProductFields): Объект, содержащий данные о продукте.

**Возвращает**:
- `dict`: Словарь с данными о продукте.

**Как работает функция**:

1. **Проверка наличия ID продукта**:
   - Проверяет, существует ли `id_product` в объекте `f`. Если `id_product` отсутствует, функция логирует ошибку и возвращает пустой словарь.

2. **Извлечение данных о продукте**:
   - Извлекает значения полей `name`, `description`, `description_short` и `specification` из объекта `f`. Если какое-либо из этих полей отсутствует, для него устанавливается пустая строка.

3. **Создание словаря с данными о продукте**:
   - Создает словарь, содержащий извлеченные данные о продукте, включая `product_name`, `product_id`, `description_short`, `description`, `specification` и `local_image_path`.

**Пример**:
```python
product_fields = ProductFields(...)
product_data = quotation.convert_product_fields(product_fields)
```

### `process_llm`

```python
def process_llm(self, products_list: List[str], lang:str,  attempts: int = 3) -> tuple | bool:
    """
    Processes the product list through the AI model.

    Args:
        products_list (str): List of product data dictionaries as a string.
        attempts (int, optional): Number of attempts to retry in case of failure. Defaults to 3.

    Returns:
        tuple: Processed response in `ru` and `he` formats.
        bool: False if unable to get a valid response after retries.

    .. note::
        Модель может возвращать невалидный результат.
        В таком случае я переспрашиваю модель разумное количество раз.
    """
```

**Назначение**: Обрабатывает список продуктов с использованием модели ИИ.

**Параметры**:
- `products_list` (List[str]): Список данных о продуктах в виде строки.
- `lang` (str): Язык, на котором требуется получить ответ от модели ИИ.
- `attempts` (int, optional): Количество попыток повторного запроса в случае неудачи. По умолчанию равно 3.

**Возвращает**:
- `dict`: Обработанный ответ от модели ИИ в формате словаря.
- `bool`: `False`, если не удалось получить валидный ответ после всех попыток.

**Как работает функция**:

1. **Проверка количества попыток**:
   - Проверяет, осталось ли доступное количество попыток (`attempts`). Если `attempts` меньше 1, функция завершает работу и возвращает пустой словарь.

2. **Подготовка запроса к модели**:
   - Читает команду для модели из файла, используя указанный язык (`lang`).
   - Формирует запрос (`q`), объединяя команду и список продуктов.

3. **Запрос к модели ИИ**:
   - Отправляет запрос (`q`) к модели ИИ с помощью метода `self.model.ask(q)`.
   - Если ответ от модели отсутствует, логирует ошибку и завершает работу.

4. **Обработка ответа от модели**:
   - Пытается распарсить ответ от модели (`response`) в словарь с помощью `j_loads`.
   - Если парсинг не удался, логирует ошибку и, если остались попытки, рекурсивно вызывает `self.process_llm` с уменьшенным количеством попыток.

**Пример**:
```python
products = [...]
response = quotation.process_llm(products, lang='ru')
```

### `process_llm_async`

```python
async def process_llm_async(self, products_list: List[str], lang:str,  attempts: int = 3) -> tuple | bool:
    """
    Processes the product list through the AI model.

    Args:
        products_list (str): List of product data dictionaries as a string.
        attempts (int, optional): Number of attempts to retry in case of failure. Defaults to 3.

    Returns:
        tuple: Processed response in `ru` and `he` formats.
        bool: False if unable to get a valid response after retries.

    .. note::
        Модель может возвращать невалидный результат.
        В таком случае я переспрашиваю модель разумное количество раз.
    """
```

**Назначение**: Асинхронно обрабатывает список продуктов с использованием модели ИИ.

**Параметры**:
- `products_list` (List[str]): Список данных о продуктах в виде строки.
- `lang` (str): Язык, на котором требуется получить ответ от модели ИИ.
- `attempts` (int, optional): Количество попыток повторного запроса в случае неудачи. По умолчанию равно 3.

**Возвращает**:
- `dict`: Обработанный ответ от модели ИИ в формате словаря.
- `bool`: `False`, если не удалось получить валидный ответ после всех попыток.

**Как работает функция**:

1. **Проверка количества попыток**:
   - Проверяет, осталось ли доступное количество попыток (`attempts`). Если `attempts` меньше 1, функция завершает работу и возвращает пустой словарь.

2. **Подготовка запроса к модели**:
   - Читает команду для модели из файла, используя указанный язык (`lang`).
   - Формирует запрос (`q`), объединяя команду и список продуктов.

3. **Асинхронный запрос к модели ИИ**:
   - Отправляет асинхронный запрос (`q`) к модели ИИ с помощью метода `self.model.ask_async(q)`.
   - Если ответ от модели отсутствует, логирует ошибку и завершает работу.

4. **Обработка ответа от модели**:
   - Пытается распарсить ответ от модели (`response`) в словарь с помощью `j_loads`.
   - Если парсинг не удался, логирует ошибку и, если остались попытки, рекурсивно вызывает `self.process_llm_async` с уменьшенным количеством попыток.

**Пример**:
```python
products = [...]
response = await quotation.process_llm_async(products, lang='ru')
```

### `save_product_data`

```python
async def save_product_data(self, product_data: dict) -> bool:
    """
    Saves individual product data to a file.

    Args:
        product_data (dict): Formatted product data.
    """
```

**Назначение**: Сохраняет данные о продукте в файл в формате JSON.

**Параметры**:
- `product_data` (dict): Словарь с данными о продукте.

**Возвращает**:
- `bool`: `True`, если данные успешно сохранены, иначе - `False`.

**Как работает функция**:

1. **Формирование пути к файлу**:
   - Формирует путь к файлу, используя `export_path` и `product_id` из `product_data`.

2. **Сохранение данных в файл**:
   - Использует `j_dumps` для сохранения данных в файл по указанному пути.
   - Если сохранение не удалось, логирует ошибку и возвращает `False`.

**Пример**:
```python
product_data = {...}
result = await quotation.save_product_data(product_data)
```

### `post_facebook_async`

```python
async def post_facebook_async(self, mexiron:SimpleNamespace) -> bool:
    """Функция исполняет сценарий рекламного модуля `facvebook`."""
```

**Назначение**: Публикует рекламные материалы в Facebook.

**Параметры**:
- `mexiron` (SimpleNamespace): Объект, содержащий данные для публикации в Facebook.

**Возвращает**:
- `bool`: `True`, если публикация прошла успешно, иначе - `False`.

**Как работает функция**:

1. **Переход на страницу Facebook**:
   - Использует `self.driver.get_url` для перехода на страницу Facebook.

2. **Формирование заголовка**:
   - Формирует заголовок (`title`) для публикации, объединяя название, описание и цену из объекта `mexiron`.

3. **Публикация сообщения и медиа**:
   - Вызывает функции `post_message_title`, `upload_post_media` и `message_publish` для публикации сообщения и медиа в Facebook.
   - Если какая-либо из этих функций завершается неудачно, логирует предупреждение и возвращает `False`.

**Пример**:
```python
mexiron_data = SimpleNamespace(...)
result = await quotation.post_facebook_async(mexiron_data)
```

## Функции

### `main`

```python
def main():
    """"""
```

**Назначение**: Главная функция модуля, которая выполняет основные шаги по созданию отчетов на основе данных о продуктах.

**Как работает функция**:

1. **Определение параметров**:
   - Устанавливает язык (`lang`) на `he` (иврит).
   - Определяет имя мехирона (`mexiron_name`).
   - Строит пути к файлам HTML, PDF, DOCX и файлу данных JSON.

2. **Загрузка данных**:
   - Загружает данные из JSON-файла с использованием `j_loads`.

3. **Создание и запуск отчетов**:
   - Создает экземпляр класса `QuotationBuilder`.
   - Асинхронно запускает создание отчетов с использованием метода `quotation.create_reports`.

**Пример**:

```python
if __name__ == '__main__':
    main()