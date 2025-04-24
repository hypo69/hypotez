# Модуль исполнения сценария `emil-design.com`

## Обзор

Модуль предоставляет функциональность для извлечения, разбора и обработки данных о товарах от различных поставщиков. Модуль обрабатывает подготовку данных, обработку с использованием ИИ и интеграцию с Prestashop для размещения товаров.

## Подробнее

Этот модуль предназначен для автоматизации процесса получения данных о товарах от поставщиков, их обработки с использованием моделей машинного обучения и последующего добавления этих товаров в интернет-магазин на платформе Prestashop. Он включает в себя инструменты для парсинга данных с сайтов поставщиков, преобразования данных в нужный формат, обработки изображений и интеграции с API Prestashop.

## Классы

### `SupplierToPrestashopProvider`

Обрабатывает извлечение, разбор и сохранение данных о продуктах поставщиков. Данные могут быть получены как из сторонних сайтов, так и из файла JSON.

**Attributes:**

- `base_dir` (Path): Базовая директория модуля.
- `driver` (Driver): Экземпляр Selenium WebDriver.
- `export_path` (Path): Путь для экспорта данных.
- `mexiron_name` (str): Название товара.
- `price` (float): Цена товара.
- `timestamp` (str): Временная метка.
- `products_list` (List[dict]): Список обработанных данных о продуктах.
- `model` (GoogleGenerativeAi): Модель Google Gemini для обработки текста.
- `config` (SimpleNamespace): Конфигурация модуля, загруженная из JSON-файла.
- `local_images_path` (Path): Локальный путь для сохранения изображений товаров.
- `lang` (str): Язык, используемый в модуле.
- `gemini_api` (str): API ключ для доступа к Google Gemini.
- `presta_api` (str): API ключ для доступа к Prestashop.
- `presta_url` (str): URL адрес Prestashop.

**Working principle:**
Класс `SupplierToPrestashopProvider` предназначен для автоматизации процесса получения данных о товарах от поставщиков, их обработки с использованием моделей машинного обучения и последующего добавления этих товаров в интернет-магазин на платформе Prestashop. Он включает в себя инструменты для парсинга данных с сайтов поставщиков, преобразования данных в нужный формат, обработки изображений и интеграции с API Prestashop.

**Methods:**

- `__init__`: Инициализирует класс `SupplierToPrestashopProvider`.
- `initialise_ai_model`: Инициализирует модель Gemini.
- `process_graber`: Выполняет сценарий: парсит продукты, обрабатывает их через ИИ и сохраняет данные.
- `process_scenarios`: Обрабатывает сценарии для заданных префиксов поставщиков.
- `save_product_data`: Сохраняет данные отдельного продукта в файл.
- `process_llm`: Обрабатывает список продуктов через AI модель.
- `save_in_prestashop`: Сохраняет товары в Prestashop emil-design.com.
- `post_facebook`: Исполняет сценарий рекламного модуля `facebook`.
- `create_report`: Отправляет задание на создание отчета о мехироне в формате `html` и `pdf`.

## Class Methods

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

Инициализирует класс `SupplierToPrestashopProvider` с необходимыми компонентами.

**Параметры:**

- `lang` (str): Язык, используемый в модуле.
- `gemini_api` (str): API ключ для доступа к Google Gemini.
- `presta_api` (str): API ключ для доступа к Prestashop.
- `presta_url` (str): URL адрес Prestashop.
- `driver` (Optional[Driver]): Экземпляр Selenium WebDriver. По умолчанию `None`.

**Примеры:**

```python
suppier_to_presta = SupplierToPrestashopProvider(
    lang="he",
    gemini_api="your_gemini_api_key",
    presta_api="your_presta_api_key",
    presta_url="https://emil-design.com/api",
    driver=Driver(Firefox)
)
```

### `initialise_ai_model`

```python
 def initialise_ai_model(self):
        """Инициализация модели Gemini"""
        try:
            system_instruction = (gs.path.endpoints / 'emil' / 'instructions' / f'system_instruction_mexiron.{self.lang}.md').read_text(encoding='UTF-8')
            return GoogleGenerativeAi(
                api_key=gs.credentials.gemini.kazarinov,
                system_instruction=system_instruction,
                generation_config={'response_mime_type': 'application/json'}
            )
        except Exception as ex:
            logger.error(f"Error loading instructions", ex)
            return
```

Инициализирует модель Gemini.

**Как работает функция:**

- Пытается прочитать системные инструкции для модели Gemini из файла.
- Создает экземпляр класса `GoogleGenerativeAi` с использованием API-ключа, системных инструкций и конфигурации генерации.
- В случае ошибки логирует ошибку и возвращает `None`.

**Примеры:**

```python
model = self.initialise_ai_model()
```

### `process_graber`

```python
async def process_graber(
        self, 
        urls: list[str],\
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

Выполняет сценарий: парсит продукты, обрабатывает их через ИИ и сохраняет данные.

**Параметры:**

- `urls` (list[str]): Список URL-адресов страниц товаров.
- `price` (Optional[str]): Цена товара. По умолчанию ''.
- `mexiron_name` (Optional[str]): Название товара. По умолчанию ''.
- `scenarios` (dict | list[dict, dict], optional): Сценарии для выполнения. По умолчанию `None`.

**Как работает функция:**

- Для каждого URL-адреса в списке `urls`:
    - Определяет грабер на основе URL-адреса.
    - Если грабер не найден, логирует сообщение и переходит к следующему URL.
    - Извлекает данные о продукте с использованием грабера.
    - Преобразует полученные данные о продукте.
    - Сохраняет данные о продукте.

**Примеры:**

```python
urls = ["https://example.com/product1", "https://example.com/product2"]
result = await self.process_graber(urls=urls, price="100", mexiron_name="Product Name")
```

### `process_scenarios`

```python
 async def process_scenarios(self, suppliers_prefixes:Optional[str] = '') -> bool:
        """"""
        ...
        suppliers_prefixes = suppliers_prefixes if isinstance(suppliers_prefixes, list) else [suppliers_prefixes] if isinstance(suppliers_prefixes, str) else []
```

Обрабатывает сценарии для заданных префиксов поставщиков.

**Параметры:**

- `suppliers_prefixes` (Optional[str]): Префиксы поставщиков. По умолчанию ''.

**Как работает функция:**
- Преобразует `suppliers_prefixes` в список, если это строка.

**Примеры:**

```python
await self.process_scenarios(suppliers_prefixes=["supplier1", "supplier2"])
```

### `save_product_data`

```python
async def save_product_data(self, product_data: dict):
        """
        Saves individual product data to a file.

        Args:
            product_data (dict): Formatted product data.
        """
        file_path = self.export_path / 'products' / f"{product_data['product_id']}.json"
        if not j_dumps(product_data, file_path, ensure_ascii=False):
            logger.error(f'Ошибка сохранения словаря {print(product_data)}\\n Путь: {file_path}')
            ...
            return
        return True
```

Сохраняет данные отдельного продукта в файл.

**Параметры:**

- `product_data` (dict): Форматированные данные продукта.

**Как работает функция:**

- Формирует путь к файлу для сохранения данных продукта.
- Сохраняет данные продукта в формате JSON.
- Логирует ошибку, если не удалось сохранить данные.

**Примеры:**

```python
product_data = {"product_id": "123", "name": "Test Product"}
await self.save_product_data(product_data)
```

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
        if attempts < 1:
            ...
            return {}  # return early if no attempts are left
        model_command = Path(gs.path.endpoints / 'emil' / 'instructions' / f'command_instruction_mexiron_{lang}.md').read_text(encoding='UTF-8')
        # Request response from the AI model
        q = model_command + '\n' + str(products_list)
        response = await self.model.ask(q)
        if not response:
            logger.error(f"Нет ответа от модели")
            ...
            return {}

        response_dict:dict = j_loads(response)

        if not response_dict:
            logger.error("Ошибка парсинга ответа модели", None, False)
            if attempts > 1:
                ...
                await self.process_llm(products_list, lang, attempts -1 )
            return {}
        return  response_dict
```

Обрабатывает список продуктов через AI модель.

**Параметры:**

- `products_list` (List[str]): Список данных о продуктах в виде строки.
- `lang` (str): Язык, используемый в запросе к модели.
- `attempts` (int, optional): Количество попыток для повторного запроса в случае неудачи. По умолчанию 3.

**Как работает функция:**

- Читает команду для модели из файла.
- Отправляет запрос к модели.
- Обрабатывает ответ от модели.
- В случае ошибки повторяет запрос несколько раз.

**Примеры:**

```python
products_list = [{"name": "Product 1", "description": "Description 1"}]
response = await self.process_llm(products_list=products_list, lang="ru")
```

### `save_in_prestashop`

```python
 async def save_in_prestashop(self, products_list:ProductFields | list[ProductFields]) -> bool:
        """Функция, которая сохраняет товары в Prestashop emil-design.com """

        products_list: list = products_list if isinstance(products_list, list) else [products_list]

        p = PrestaProduct(api_key=self.presta_api, api_domain=self.presta_url)

        for f in products_list:
            p.add_new_product(f)
```

Сохраняет товары в Prestashop emil-design.com.

**Параметры:**

- `products_list` (ProductFields | list[ProductFields]): Список товаров для сохранения.

**Как работает функция:**

- Создает экземпляр класса `PrestaProduct`.
- Для каждого товара вызывает метод `add_new_product`.

**Примеры:**

```python
products = [ProductFields(...), ProductFields(...)]
await self.save_in_prestashop(products_list=products)
```

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

Исполняет сценарий рекламного модуля `facebook`.

**Параметры:**

- `mexiron` (SimpleNamespace): Данные о товаре.

**Как работает функция:**

- Открывает страницу Facebook.
- Формирует заголовок сообщения.
- Отправляет заголовок и медиафайлы.
- Публикует сообщение.

**Примеры:**

```python
mexiron_data = SimpleNamespace(title="Title", description="Description", price="100", products=["image1.jpg", "image2.jpg"])
await self.post_facebook(mexiron=mexiron_data)
```

### `create_report`

```python
async def create_report(self, data: dict, lang:str, html_file: Path, pdf_file: Path) -> bool:
        """Функция отправляет задание на создание мехирона в формате `html` и `pdf`.
        Если мехорон в pdf создался (`generator.create_report()` вернул True) - 
        отправить его боту
        """

        report_generator = ReportGenerator()

        if await report_generator.create_report(data, lang, html_file, pdf_file):
            # Проверка, существует ли файл и является ли он файлом
            if pdf_file.exists() and pdf_file.is_file():
                # Отправка боту PDF-файл через reply_document()
                await self.update.message.reply_document(document=pdf_file)
                return True
            else:
                logger.error(f"PDF файл не найден или не является файлом: {pdf_file}")
                return
```

Отправляет задание на создание отчета о товаре в формате `html` и `pdf`.

**Параметры:**

- `data` (dict): Данные для отчета.
- `lang` (str): Язык отчета.
- `html_file` (Path): Путь к HTML файлу.
- `pdf_file` (Path): Путь к PDF файлу.

**Как работает функция:**

- Создает отчет в формате HTML и PDF.
- Отправляет PDF файл боту.

**Примеры:**

```python
data = {"name": "Product Name", "description": "Description"}
html_file = Path("report.html")
pdf_file = Path("report.pdf")
await self.create_report(data=data, lang="ru", html_file=html_file, pdf_file=pdf_file)
```

## Функции

### `upload_redacted_images_from_emil`

```python
async def upload_redacted_images_from_emil():
    """
    На данный момент функция читает JSON со списком фотографий , которые были получены от Эмиля
    """
```

На данный момент функция читает JSON со списком фотографий, которые были получены от Эмиля.

**Как работает функция:**

- Читает JSON файл со списком товаров.
- Сохраняет товары в Prestashop.

**Примеры:**

```python
await upload_redacted_images_from_emil()
```

### `main`

```python
async def main():
    """
    """
```

**Как работает функция:**

- Вызывает функцию `upload_redacted_images_from_emil`.

**Примеры:**

```python
await main()
```