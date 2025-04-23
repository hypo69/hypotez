# Модуль исполнения сценария `emil-design.com`

## Обзор

Модуль предназначен для извлечения, разбора и сохранения данных о продуктах поставщиков, как из внешних сайтов, так и из JSON-файлов. Он обеспечивает подготовку данных, их обработку с использованием искусственного интеллекта и интеграцию с Prestashop для публикации товаров.

## Подробнее

Этот модуль является частью системы, автоматизирующей процесс добавления товаров в интернет-магазин Prestashop на основе данных, полученных от поставщиков. Он использует веб-скрапинг для извлечения информации о товарах, а также применяет AI-модели для обработки и улучшения этих данных.

## Классы

### `SupplierToPrestashopProvider`

**Описание**: Класс для обработки данных о продуктах поставщиков, их извлечения, разбора и сохранения. Данные могут быть получены как с сайтов, так и из JSON файлов.

**Атрибуты**:
- `base_dir` (Path): Базовая директория для поиска файлов поставщиков.
- `driver` (Driver): Экземпляр Selenium WebDriver.
- `export_path` (Path): Путь для экспорта данных.
- `mexiron_name` (str): Имя Mexiron.
- `price` (float): Цена товара.
- `timestamp` (str): Временная метка для идентификации данных.
- `products_list` (list): Список обработанных данных о товарах.
- `model` (GoogleGenerativeAi): Модель Google Gemini для обработки текста.
- `config` (SimpleNamespace): Конфигурация модуля, загруженная из JSON файла.
- `local_images_path` (Path): Путь для сохранения локальных изображений товаров.
- `lang` (str): Язык, используемый в процессе обработки данных.
- `gemini_api` (str): API ключ для доступа к Google Gemini.
- `presta_api` (str): API ключ для доступа к Prestashop.
- `presta_url` (str): URL адрес Prestashop.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `SupplierToPrestashopProvider`.
- `initialise_ai_model`: Инициализирует AI модель Gemini.
- `process_graber`: Извлекает данные о товарах со страниц поставщиков.
- `process_scenarios`: Обрабатывает сценарии для различных поставщиков.
- `save_product_data`: Сохраняет данные о товаре в файл.
- `process_llm`: Обрабатывает список товаров с использованием AI модели.
- `save_in_prestashop`: Сохраняет товары в Prestashop.
- `post_facebook`: Публикует информацию о товаре на Facebook.
- `create_report`: Создает отчет о товаре в формате HTML и PDF.

### `Config`

**Описание**: Класс, содержащий настройки конфигурации для модуля.

**Атрибуты**:
- `ENDPOINT` (str): Имя каталога поставщика.

## Функции

### `__init__`

```python
def __init__(self, 
             lang:str, 
             gemini_api: str,
             presta_api: str,
             presta_url: str,
             driver: Optional [Driver] = None,
             ):
    """
    Initializes SupplierToPrestashopProvider class with required components.

    Args:
        driver (Driver): Selenium WebDriver instance.
        

    """
```

**Назначение**: Инициализирует класс `SupplierToPrestashopProvider` с необходимыми компонентами.

**Параметры**:
- `lang` (str): Язык, используемый в процессе обработки данных.
- `gemini_api` (str): API ключ для доступа к Google Gemini.
- `presta_api` (str): API ключ для доступа к Prestashop.
- `presta_url` (str): URL адрес Prestashop.
- `driver` (Optional[Driver]): Экземпляр Selenium WebDriver. Если не указан, создается новый экземпляр Firefox.

**Как работает функция**:
- Функция инициализирует объект `SupplierToPrestashopProvider`, загружает конфигурацию из JSON-файла, устанавливает временную метку, инициализирует драйвер и AI модель.

### `initialise_ai_model`

```python
def initialise_ai_model(self):
    """Инициализация модели Gemini"""
```

**Назначение**: Инициализирует модель Gemini.

**Как работает функция**:
- Функция считывает системные инструкции для модели Gemini из файла, создает экземпляр класса `GoogleGenerativeAi` с использованием этих инструкций и возвращает его.

### `process_graber`

```python
async def process_graber(
    self, 
    urls: list[str],
    price: Optional[str] = '', 
    mexiron_name: Optional[str] = '', 
    scenarios: dict | list[dict,dict] = None,
    
) -> bool:
    """
    Executes the scenario: parses products, processes them via AI, and stores data.

    Args:
        system_instruction (Optional[str]): System instructions for the AI model.
        price (Optional[str]): Price to process.
        mexiron_name (Optional[str]): Custom Mexiron name.
        urls (Optional[str | List[str]]): Product page URLs.
        scenario (Optional[dict]): Сценарий исполнения, который находится в директории `src.suppliers.suppliers_list.<supplier>.sceanarios`

    Returns:
        bool: True if the scenario executes successfully, False otherwise.

    .. todo:
        сделать логер перед отрицательным выходом из функции. 
        Важно! модель ошибается. 

    """
```

**Назначение**: Извлекает данные о товарах со страниц поставщиков, обрабатывает их с помощью AI и сохраняет данные.

**Параметры**:
- `urls` (list[str]): Список URL-адресов страниц товаров.
- `price` (Optional[str]): Цена товара.
- `mexiron_name` (Optional[str]): Название Mexiron.
- `scenarios` (dict | list[dict, dict], optional): Сценарии для исполнения. По умолчанию `None`.

**Возвращает**:
- `bool`: `True`, если сценарий выполнен успешно, `False` в противном случае.

**Как работает функция**:
- Функция проходит по списку URL-адресов, получает граббер для каждого URL, извлекает данные о товаре, преобразует их и сохраняет.

### `process_scenarios`

```python
async def process_scenarios(self, suppliers_prefixes:Optional[str] = '') -> bool:
    """"""
    ...
    suppliers_prefixes = suppliers_prefixes if isinstance(suppliers_prefixes, list) else [suppliers_prefixes] if isinstance(suppliers_prefixes, str) else []
```

**Назначение**: Обрабатывает сценарии для различных поставщиков.

**Параметры**:
- `suppliers_prefixes` (Optional[str]): Префиксы поставщиков.

**Возвращает**:
- `bool`: `True`, если обработка сценариев выполнена успешно, `False` в противном случае.

**Как работает функция**:
- Функция обрабатывает сценарии для заданных префиксов поставщиков. Если `suppliers_prefixes` является строкой, она преобразуется в список.

### `save_product_data`

```python
async def save_product_data(self, product_data: dict):
    """
    Saves individual product data to a file.

    Args:
        product_data (dict): Formatted product data.
    """
```

**Назначение**: Сохраняет данные о товаре в файл.

**Параметры**:
- `product_data` (dict): Отформатированные данные о товаре.

**Как работает функция**:
- Функция сохраняет данные о товаре в JSON-файл. Имя файла формируется на основе идентификатора товара.

### `process_llm`

```python
async def process_llm(self, products_list: List[str], lang:str,  attempts: int = 3) -> tuple | bool:
    """
    Processes the product list through the AI model.

    Args:
        products_list (str): List of product data dictionaries as a string.
        attempts (int, optional): Number of attempts to retry in case of failure. Defaults to 3.

    Returns:
        tuple: Processed response in `ru` and `he` formats.
        bool: False if unable to get a valid response after retries.

    .. note::
        Модель может возвращать невелидный результат.
        В таком случае я переспрашиваю модель разумное количество раз.
    """
```

**Назначение**: Обрабатывает список товаров с использованием AI модели.

**Параметры**:
- `products_list` (List[str]): Список данных о товарах в виде строки.
- `lang` (str): Язык, используемый в процессе обработки данных.
- `attempts` (int, optional): Количество попыток повторной отправки запроса в случае неудачи. По умолчанию `3`.

**Возвращает**:
- `dict`: Обработанный ответ от AI модели.
- `bool`: `False`, если не удалось получить валидный ответ после нескольких попыток.

**Как работает функция**:
- Функция отправляет запрос в AI модель с данными о товарах, получает ответ, проверяет его валидность и возвращает обработанные данные. Если ответ невалиден, функция повторяет запрос несколько раз.

### `save_in_prestashop`

```python
async def save_in_prestashop(self, products_list:ProductFields | list[ProductFields]) -> bool:
    """Функция, которая сохраняет товары в Prestashop emil-design.com """
```

**Назначение**: Сохраняет товары в Prestashop.

**Параметры**:
- `products_list` (ProductFields | list[ProductFields]): Список товаров для сохранения.

**Как работает функция**:
- Функция проходит по списку товаров и добавляет каждый товар в Prestashop с использованием API.

### `post_facebook`

```python
async def post_facebook(self, mexiron:SimpleNamespace) -> bool:
    """Функция исполняет сценарий рекламного модуля `facvebook`."""
    ...
    self.driver.get_url(r'https://www.facebook.com/profile.php?id=61566067514123')
    currency = "ש''ח"
    title = f'{mexiron.title}\n{mexiron.description}\n{mexiron.price} {currency}'
    if not post_message_title(self.d, title):
        logger.warning(f'Не получилось отправить название мехирона')
        ...
        return

    if not upload_post_media(self.d, media = mexiron.products):
        logger.warning(f'Не получилось отправить media')
        ...
        return
    if not message_publish(self.d):
        logger.warning(f'Не получилось отправить media')
        ...
        return

    return True
```

**Назначение**: Публикует информацию о товаре на Facebook.

**Параметры**:
- `mexiron` (SimpleNamespace): Объект, содержащий данные о товаре для публикации.

**Как работает функция**:
- Функция переходит на страницу Facebook, формирует заголовок сообщения, загружает медиафайлы и публикует сообщение.

### `create_report`

```python
async def create_report(self, data: dict, lang:str, html_file: Path, pdf_file: Path) -> bool:
    """Функция отправляет задание на создание мехирона в формате `html` и `pdf`.
    Если мехорон в pdf создался (`generator.create_report()` вернул True) - 
    отправить его боту
    """
```

**Назначение**: Создает отчет о товаре в формате HTML и PDF и отправляет PDF файл боту.

**Параметры**:
- `data` (dict): Данные для отчета.
- `lang` (str): Язык, используемый в отчете.
- `html_file` (Path): Путь для сохранения HTML файла.
- `pdf_file` (Path): Путь для сохранения PDF файла.

**Как работает функция**:
- Функция создает отчет о товаре в формате HTML и PDF с использованием данных, переданных в функцию, а также отправляет PDF файл боту.

### `upload_redacted_images_from_emil`

```python
async def upload_redacted_images_from_emil():
    """
    На данный момент функция читает JSON со списком фотографий , которые были получены от Эмиля
    """
```

**Назначение**: Загружает отредактированные изображения из JSON файла, полученного от Эмиля, и сохраняет их в Prestashop.

**Как работает функция**:
- Функция считывает JSON файл, создает экземпляр `SupplierToPrestashopProvider` и сохраняет изображения в Prestashop.

### `main`

```python
async def main():
    """
    """
    await upload_redacted_images_from_emil()
```

**Назначение**: Главная функция, которая запускает процесс загрузки отредактированных изображений.

**Как работает функция**:
- Функция вызывает `upload_redacted_images_from_emil` для загрузки изображений.

## Примеры

Пример использования:

```python
# Пример использования класса SupplierToPrestashopProvider
supplier = SupplierToPrestashopProvider(lang='he', gemini_api='your_gemini_api_key', presta_api='your_presta_api_key', presta_url='your_presta_url')
asyncio.run(supplier.process_graber(urls=['http://example.com/product1', 'http://example.com/product2'], price='100', mexiron_name='Product Name'))