# Модуль для подготовки данных, обработки AI и интеграции с Facebook для публикации продуктов.
## Обзор

Модуль `quotation_builder.py` предназначен для извлечения, разбора и обработки данных о продуктах от различных поставщиков. Он включает в себя подготовку данных, обработку с использованием AI и интеграцию с Facebook для публикации продуктов.

## Подробнее

Модуль предоставляет класс `QuotationBuilder`, который автоматизирует процесс создания коммерческих предложений (мехироним) на основе данных о продуктах, полученных от разных поставщиков. Он использует веб-драйвер для взаимодействия с сайтами поставщиков, AI модель (Google Gemini) для обработки и структурирования данных, а также интеграцию с Facebook для публикации рекламных объявлений. Модуль также включает функциональность для генерации отчетов в различных форматах (HTML, PDF, DOCX).

## Классы

### `QuotationBuilder`

**Описание**: Класс `QuotationBuilder` обрабатывает извлечение, разбор и сохранение данных о продуктах поставщиков.

**Атрибуты**:

- `base_path` (Path): Базовый путь к каталогу модуля.
- `config` (SimpleNamespace): Конфигурация, загруженная из JSON файла.
- `html_path` (str | Path): Путь к HTML файлу отчета.
- `pdf_path` (str | Path): Путь к PDF файлу отчета.
- `docx_path` (str | Path): Путь к DOCX файлу отчета.
- `driver` (Driver): Экземпляр Selenium WebDriver.
- `export_path` (Path): Путь для экспорта данных.
- `mexiron_name` (str): Название мехирона.
- `price` (float): Цена.
- `timestamp` (str): Временная метка.
- `products_list` (List): Список обработанных данных о продуктах.
- `model` (GoogleGenerativeAI): Экземпляр AI модели Google Gemini.
- `translations` (SimpleNamespace): Переводы, загруженные из JSON файла.
- `required_fields` (tuple): Кортеж необходимых полей товара.

**Методы**:

- `__init__(self, mexiron_name: Optional[str] = gs.now, driver: Optional[Firefox | Playwrid | str] = None, **kwards)`: Инициализирует класс `QuotationBuilder` с требуемыми компонентами.
- `convert_product_fields(self, f: ProductFields) -> dict`: Преобразует поля продукта в словарь.
- `process_ai(self, products_list: List[str], lang: str, attempts: int = 3) -> tuple | bool`: Обрабатывает список продуктов с использованием AI модели.
- `process_ai_async(self, products_list: List[str], lang: str, attempts: int = 3) -> tuple | bool`: Асинхронно обрабатывает список продуктов с использованием AI модели.
- `save_product_data(self, product_data: dict) -> bool`: Сохраняет данные о продукте в файл.
- `post_facebook_async(self, mexiron: SimpleNamespace) -> bool`: Исполняет сценарий рекламного модуля `facebook`.

## Методы класса

### `__init__`

```python
def __init__(self, mexiron_name:Optional[str] = gs.now, driver:Optional[Firefox | Playwrid | str] = None,  **kwards) -> None:
    """
    Initializes Mexiron class with required components.

    Args:
        driver (Driver): Selenium WebDriver instance.
        mexiron_name (Optional[str]): Custom name for the Mexiron process.
        webdriver_name (Optional[str]): Name of the WebDriver to use. Defaults to 'firefox'. call to Firefox or Playwrid
        window_mode (Optional[str]): Оконный режим вебдрайвера. Может быть 'maximized', 'headless', 'minimized', 'fullscreen', 'normal', 'hidden', 'kiosk'
    """
```

**Назначение**: Инициализирует класс `QuotationBuilder`, настраивает веб-драйвер, модель Gemini и пути для экспорта данных.

**Параметры**:

- `mexiron_name` (Optional[str]): Название процесса мехирона. По умолчанию используется текущее время.
- `driver` (Optional[Firefox | Playwrid | str]): Экземпляр веб-драйвера или его название. По умолчанию `Firefox`.
- `**kwards`: Дополнительные аргументы для инициализации веб-драйвера.

**Как работает функция**:

1.  Устанавливает имя мехирона.
2.  Определяет путь для экспорта данных.
3.  Инициализирует веб-драйвер на основе переданного аргумента `driver`. Если `driver` является экземпляром `Driver`, используется он. Если `driver` является классом `Firefox` или `Playwrid`, создается экземпляр `Driver` с этим классом. Если `driver` является строкой, соответствующий веб-драйвер инициализируется по имени. Если `driver` не передан, используется `Firefox` по умолчанию.
4.  Инициализирует модель Gemini с использованием ключа API и системной инструкции из файла.

**Примеры**:

```python
quotation = QuotationBuilder(mexiron_name='test_mexiron', driver='firefox', window_mode='maximized')
quotation = QuotationBuilder(driver=Playwrid())
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

**Назначение**: Преобразует поля продукта из объекта `ProductFields` в словарь для дальнейшей обработки AI моделью.

**Параметры**:

- `f` (ProductFields): Объект, содержащий распарсенные данные продукта.

**Возвращает**:

- `dict`: Словарь с данными продукта, готовый для обработки AI моделью.

**Как работает функция**:

1.  Проверяет наличие `id_product` в данных продукта. Если отсутствует, возвращает пустой словарь и логирует ошибку.
2.  Извлекает значения полей `name`, `description`, `description_short` и `specification` из объекта `ProductFields`.
3.  Формирует словарь с данными продукта, используя извлеченные значения.

**Примеры**:

```python
product_fields = ProductFields(...)
product_data = quotation.convert_product_fields(product_fields)
```

### `process_ai`

```python
def process_ai(self, products_list: List[str], lang:str,  attempts: int = 3) -> tuple | bool:
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

**Назначение**: Обрабатывает список продуктов с использованием AI модели (Google Gemini).

**Параметры**:

- `products_list` (List[str]): Список данных о продуктах в виде строки.
- `lang` (str): Язык, на котором требуется получить ответ от AI модели.
- `attempts` (int): Количество попыток повторной отправки запроса в случае неудачи. По умолчанию 3.

**Возвращает**:

- `dict`: Обработанный ответ от AI модели в виде словаря.
- `bool`: `False`, если не удалось получить валидный ответ после всех попыток.

**Как работает функция**:

1.  Проверяет количество оставшихся попыток. Если попыток не осталось, возвращает пустой словарь.
2.  Формирует запрос к AI модели, объединяя команду из файла инструкций и данные о продуктах.
3.  Отправляет запрос к AI модели и получает ответ.
4.  Парсит ответ из JSON в словарь. В случае ошибки парсинга повторяет запрос, если остались попытки.

**Примеры**:

```python
products = [{'product_name': '...', 'product_id': '...', ...}, ...]
response = quotation.process_ai(str(products), lang='ru')
```

### `process_ai_async`

```python
async def process_ai_async(self, products_list: List[str], lang:str,  attempts: int = 3) -> tuple | bool:
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

**Назначение**: Асинхронно обрабатывает список продуктов с использованием AI модели (Google Gemini).

**Параметры**:

- `products_list` (List[str]): Список данных о продуктах в виде строки.
- `lang` (str): Язык, на котором требуется получить ответ от AI модели.
- `attempts` (int): Количество попыток повторной отправки запроса в случае неудачи. По умолчанию 3.

**Возвращает**:

- `dict`: Обработанный ответ от AI модели в виде словаря.
- `bool`: `False`, если не удалось получить валидный ответ после всех попыток.

**Как работает функция**:

1.  Проверяет количество оставшихся попыток. Если попыток не осталось, возвращает пустой словарь.
2.  Формирует запрос к AI модели, объединяя команду из файла инструкций и данные о продуктах.
3.  Асинхронно отправляет запрос к AI модели и получает ответ.
4.  Парсит ответ из JSON в словарь. В случае ошибки парсинга повторяет запрос, если остались попытки.

**Примеры**:

```python
products = [{'product_name': '...', 'product_id': '...', ...}, ...]
response = await quotation.process_ai_async(str(products), lang='ru')
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

- `product_data` (dict): Словарь с данными продукта.

**Возвращает**:

- `bool`: `True`, если данные успешно сохранены, `False` в случае ошибки.

**Как работает функция**:

1.  Формирует путь к файлу для сохранения данных продукта.
2.  Сохраняет данные продукта в файл в формате JSON с использованием функции `j_dumps`.
3.  В случае ошибки логирует ошибку и возвращает `False`.

**Примеры**:

```python
product_data = {'product_name': '...', 'product_id': '...', ...}
await quotation.save_product_data(product_data)
```

### `post_facebook_async`

```python
async def post_facebook_async(self, mexiron:SimpleNamespace) -> bool:
    """Функция исполняет сценарий рекламного модуля `facvebook`."""
```

**Назначение**: Выполняет сценарий публикации рекламного объявления в Facebook.

**Параметры**:

- `mexiron` (SimpleNamespace): Объект, содержащий данные для публикации в Facebook (заголовок, описание, цена, медиафайлы).

**Возвращает**:

- `bool`: `True`, если публикация прошла успешно, `False` в случае ошибки.

**Как работает функция**:

1.  Переходит на страницу профиля Facebook.
2.  Формирует заголовок для публикации, объединяя название, описание и цену мехирона.
3.  Публикует заголовок, медиафайлы и отправляет сообщение в Facebook, используя функции `post_message_title`, `upload_post_media` и `message_publish` из модуля `src.endpoints.advertisement.facebook.scenarios`.
4.  В случае ошибки логирует предупреждение и возвращает `False`.

**Примеры**:

```python
mexiron_data = SimpleNamespace(title='...', description='...', price=100, products=['...', ...])
await quotation.post_facebook_async(mexiron_data)
```

## Функции

### `main`

```python
def main() -> None:
    """"""
```

**Назначение**: Главная функция модуля, которая выполняет создание отчетов на основе данных о продуктах.

**Как работает функция**:

1.  Определяет язык отчета.
2.  Формирует пути к файлам для сохранения отчетов в различных форматах (HTML, PDF, DOCX).
3.  Загружает данные о продуктах из JSON файла.
4.  Создает экземпляр класса `QuotationBuilder`.
5.  Асинхронно запускает создание отчетов с использованием метода `create_reports`.

**Примеры**:

```python
if __name__ == '__main__':
    main()
```