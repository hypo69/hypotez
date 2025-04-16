# Модуль исполнения сценария создания мехирона для Сергея Казаринова

## Обзор

Модуль предназначен для извлечения, разбора и обработки данных о товарах от различных поставщиков с целью их интеграции в Prestashop. Он включает в себя функциональность для подготовки данных, их обработки с использованием AI и публикации товаров в Prestashop.

## Подробней

Модуль автоматизирует процесс переноса данных о товарах от поставщиков в Prestashop. Он использует веб-скрапинг для извлечения данных с сайтов поставщиков, AI для обработки и улучшения этих данных, и API Prestashop для публикации товаров.

## Классы

### `SupplierToPrestashopProvider`

**Описание**: Класс обрабатывает извлечение, разбор и сохранение данных о продуктах поставщиков. Данные могут быть получены как с посторонних сайтов, так и из файла JSON.

**Атрибуты**:

- `driver (Driver)`: Экземпляр Selenium WebDriver для управления браузером.
- `export_path (Path)`: Путь для экспорта данных.
- `mexiron_name (str)`: Название мехирона.
- `price (float)`: Цена товара.
- `timestamp (str)`: Временная метка.
- `products_list (list)`: Список обработанных данных о продуктах.
- `model (GoogleGenerativeAi)`: Модель Google Gemini для обработки текста.
- `config (SimpleNamespace)`: Конфигурация модуля, загружаемая из JSON.
- `local_images_path (Path)`: Путь для хранения локальных изображений товаров.
- `lang (str)`: Язык, используемый в модуле.
- `gemini_api (str)`: Ключ API для доступа к Google Gemini.
- `presta_api (str)`: Ключ API для доступа к Prestashop.
- `presta_url (str)`: URL адрес Prestashop.

**Методы**:

- `__init__`: Инициализирует экземпляр класса `SupplierToPrestashopProvider`.
- `initialise_ai_model`: Инициализирует модель Gemini.
- `run_scenario`: Выполняет основной сценарий: разбор товаров, обработка через AI и сохранение данных.
- `save_product_data`: Сохраняет данные об отдельном товаре в файл.
- `process_llm`: Обрабатывает список товаров через AI модель.
- `read_data_from_json`: Загружает JSON файлы и фотографии, полученные через телеграм.
- `save_in_prestashop`: Сохраняет товары в Prestashop.
- `post_facebook`: Исполняет сценарий рекламного модуля `facebook`.
- `create_report`: Отправляет задание на создание мехирона в форматах `html` и `pdf`.

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

**Назначение**: Инициализирует класс `SupplierToPrestashopProvider`, загружает конфигурацию, создает экземпляр драйвера и инициализирует AI модель.

**Параметры**:

- `lang (str)`: Язык, используемый в модуле.
- `gemini_api (str)`: Ключ API для доступа к Google Gemini.
- `presta_api (str)`: Ключ API для доступа к Prestashop.
- `presta_url (str)`: URL адрес Prestashop.
- `driver (Optional[Driver])`: Экземпляр Selenium WebDriver (по умолчанию `None`). Если не указан, создается новый экземпляр `Firefox`.

**Как работает функция**:

1. Сохраняет параметры `gemini_api`, `presta_api`, `presta_url` и `lang` в атрибуты экземпляра класса.
2. Загружает конфигурацию из JSON файла `emil.json` с использованием функции `j_loads_ns` и сохраняет ее в атрибуте `config`.
3. Инициализирует атрибут `timestamp` текущей датой и временем.
4. Создает экземпляр драйвера `Firefox`, если он не был передан в качестве аргумента.
5. Инициализирует AI модель с помощью метода `initialise_ai_model`.

**Примеры**:

```python
# Пример инициализации класса с указанием всех параметров
provider = SupplierToPrestashopProvider(
    lang='ru',
    gemini_api='your_gemini_api_key',
    presta_api='your_presta_api_key',
    presta_url='https://your-prestashop.com',
    driver=Driver(Firefox)
)

# Пример инициализации класса с параметрами по умолчанию для драйвера
provider = SupplierToPrestashopProvider(
    lang='ru',
    gemini_api='your_gemini_api_key',
    presta_api='your_presta_api_key',
    presta_url='https://your-prestashop.com'
)
```

### `initialise_ai_model`

```python
def initialise_ai_model(self):
    """Инициализация модели Gemini"""
```

**Назначение**: Инициализирует модель Google Gemini с использованием системных инструкций из файла.

**Как работает функция**:

1. Формирует путь к файлу с системными инструкциями для модели Gemini.
2. Считывает содержимое файла инструкций.
3. Создает экземпляр класса `GoogleGenerativeAi` с использованием API ключа, системных инструкций и конфигурации генерации.
4. В случае ошибки логирует ее и возвращает `None`.

**Параметры**:

- Нет явных параметров, но использует атрибут экземпляра класса `self.lang` для определения файла инструкций.

**Возвращает**:

- `GoogleGenerativeAi`: Инициализированный экземпляр модели `GoogleGenerativeAi`.
- `None`: В случае ошибки.

**Примеры**:

```python
# Пример инициализации AI модели
model = self.initialise_ai_model()
if model:
    print("AI модель успешно инициализирована")
else:
    print("Ошибка инициализации AI модели")
```

### `run_scenario`

```python
async def run_scenario(
    self, 
    urls: list[str],
    price: Optional[str] = '', 
    mexiron_name: Optional[str] = '', 
    
) -> bool:
    """
    Executes the scenario: parses products, processes them via AI, and stores data.

    Args:
        system_instruction (Optional[str]): System instructions for the AI model.
        price (Optional[str]): Price to process.
        mexiron_name (Optional[str]): Custom Mexiron name.
        urls (Optional[str | List[str]]): Product page URLs.

    Returns:
        bool: True if the scenario executes successfully, False otherwise.

    .. todo:
        сделать логер перед отрицательным выходом из функции. 
        Важно! модель ошибается. 

    """
```

**Назначение**: Выполняет сценарий разбора товаров, их обработки с использованием AI и сохранения данных.

**Параметры**:

- `urls (list[str])`: Список URL-адресов страниц товаров.
- `price (Optional[str])`: Цена товара (по умолчанию '').
- `mexiron_name (Optional[str])`: Название мехирона (по умолчанию '').

**Как работает функция**:

1. Определяет необходимые поля товара.
2. Перебирает URL-адреса товаров.
3. Получает граббер для каждого URL-адреса.
4. Извлекает поля товара с помощью граббера.
5. Преобразует поля товара.
6. Сохраняет данные о товаре.

**Возвращает**:

- `bool`: `True`, если сценарий выполнен успешно, `False` в противном случае.

**Примеры**:

```python
# Пример выполнения сценария с одним URL-адресом
urls = ['https://example.com/product1']
result = await self.run_scenario(urls=urls, price='100', mexiron_name='Product 1')

# Пример выполнения сценария с несколькими URL-адресами
urls = ['https://example.com/product1', 'https://example.com/product2']
result = await self.run_scenario(urls=urls, price='200', mexiron_name='Product 2')
```

### `save_product_data`

```python
async def save_product_data(self, product_data: dict):
    """
    Saves individual product data to a file.

    Args:
        product_data (dict): Formatted product data.
    """
```

**Назначение**: Сохраняет данные об отдельном товаре в файл.

**Параметры**:

- `product_data (dict)`: Форматированные данные о товаре.

**Как работает функция**:

1. Формирует путь к файлу для сохранения данных о товаре.
2. Сохраняет данные в файл с использованием функции `j_dumps`.
3. В случае ошибки логирует ее и возвращает `None`.

**Возвращает**:

- `True`: Если данные успешно сохранены.
- `None`: В случае ошибки.

**Примеры**:

```python
# Пример сохранения данных о товаре
product_data = {'product_id': '123', 'name': 'Product 1'}
result = await self.save_product_data(product_data)
if result:
    print("Данные о товаре успешно сохранены")
else:
    print("Ошибка сохранения данных о товаре")
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
```

**Назначение**: Обрабатывает список товаров с использованием AI модели.

**Параметры**:

- `products_list (List[str])`: Список данных о товарах в виде строки.
- `lang (str)`: Язык, используемый в запросе к модели.
- `attempts (int)`: Количество попыток повтора в случае неудачи (по умолчанию 3).

**Как работает функция**:

1. Проверяет количество оставшихся попыток. Если их нет, возвращает пустой словарь.
2. Формирует команду для модели, включая системные инструкции и данные о товарах.
3. Отправляет запрос к AI модели.
4. Обрабатывает ответ от модели.
5. В случае ошибки парсинга ответа повторяет запрос, если остались попытки.

**Возвращает**:

- `dict`: Обработанный ответ от модели в виде словаря.
- `None`: В случае неудачи после всех попыток.

**Примеры**:

```python
# Пример обработки списка товаров с использованием AI модели
products_list = [{'product_id': '123', 'name': 'Product 1'}]
response = await self.process_llm(products_list=products_list, lang='ru')
if response:
    print("Ответ от AI модели:", response)
else:
    print("Ошибка обработки данных с использованием AI модели")
```

### `read_data_from_json`

```python
async def read_data_from_json(self):
    """Загружаю JSON файлы и фотки, которые я сделал через телеграм"""
```

**Назначение**: Загружает JSON файлы и фотографии, полученные через телеграм.

**Как работает функция**:

1. Загружает JSON данные из файла, расположенного по пути `self.local_images_path`, используя функцию `j_loads_ns`.
2. Выводит загруженные данные в консоль.

**Параметры**:

- Отсутствуют.

**Возвращает**:

- Функция ничего не возвращает явно.

**Примеры**:

```python
# Пример загрузки данных из JSON файла
await self.read_data_from_json()
```

### `save_in_prestashop`

```python
async def save_in_prestashop(self, products_list:ProductFields | list[ProductFields]) -> bool:
    """Функция, которая сохраняет товары в Prestashop emil-design.com """
```

**Назначение**: Сохраняет товары в Prestashop.

**Параметры**:

- `products_list (ProductFields | list[ProductFields])`: Список товаров для сохранения. Может быть как экземпляром `ProductFields`, так и списком экземпляров `ProductFields`.

**Как работает функция**:

1. Приводит входной параметр `products_list` к типу `list`, если он не является списком.
2. Создает экземпляр класса `PrestaProduct` с использованием API ключа и URL Prestashop.
3. Перебирает список товаров и добавляет каждый товар в Prestashop с помощью метода `add_new_product` класса `PrestaProduct`.

**Возвращает**:

- `bool`: Всегда возвращает `True`, если выполнение доходит до конца функции.

**Примеры**:

```python
# Пример сохранения одного товара в Prestashop
product = ProductFields(...)  # Создание экземпляра ProductFields
await self.save_in_prestashop(product)

# Пример сохранения списка товаров в Prestashop
products = [ProductFields(...), ProductFields(...)]  # Создание списка экземпляров ProductFields
await self.save_in_prestashop(products)
```

### `post_facebook`

```python
async def post_facebook(self, mexiron:SimpleNamespace) -> bool:
    """Функция исполняет сценарий рекламного модуля `facvebook`."""
```

**Назначение**: Выполняет сценарий рекламного модуля `facebook`.

**Параметры**:

- `mexiron (SimpleNamespace)`: Объект с данными для публикации в Facebook.

**Как работает функция**:

1. Переходит на страницу Facebook.
2. Формирует заголовок сообщения, включающий название, описание и цену товара.
3. Публикует заголовок сообщения.
4. Загружает медиафайлы.
5. Публикует сообщение.

**Возвращает**:

- `bool`: `True`, если сценарий выполнен успешно, `False` в противном случае.

**Примеры**:

```python
# Пример выполнения сценария публикации в Facebook
mexiron_data = SimpleNamespace(
    title='Product 1',
    description='Description of Product 1',
    price='100',
    products=['image1.jpg', 'image2.jpg']
)
result = await self.post_facebook(mexiron=mexiron_data)
if result:
    print("Сообщение успешно опубликовано в Facebook")
else:
    print("Ошибка публикации сообщения в Facebook")
```

### `create_report`

```python
async def create_report(self, data: dict, lang:str, html_file: Path, pdf_file: Path) -> bool:
    """Функция отправляет задание на создание мехирона в формате `html` и `pdf`.
    Если мехорон в pdf создался (`generator.create_report()` вернул True) - 
    отправить его боту
    """
```

**Назначение**: Создает отчет в форматах `html` и `pdf` и отправляет PDF-файл боту.

**Параметры**:

- `data (dict)`: Данные для отчета.
- `lang (str)`: Язык отчета.
- `html_file (Path)`: Путь для сохранения HTML-файла.
- `pdf_file (Path)`: Путь для сохранения PDF-файла.

**Как работает функция**:

1. Создает экземпляр класса `ReportGenerator`.
2. Создает отчет в форматах `html` и `pdf` с использованием метода `create_report` класса `ReportGenerator`.
3. Проверяет, создан ли PDF-файл.
4. Отправляет PDF-файл боту.

**Возвращает**:

- `bool`: `True`, если отчет успешно создан и отправлен, `False` в противном случае.

**Примеры**:

```python
# Пример создания отчета
data = {'product_id': '123', 'name': 'Product 1'}
html_file = Path('report.html')
pdf_file = Path('report.pdf')
result = await self.create_report(data=data, lang='ru', html_file=html_file, pdf_file=pdf_file)
if result:
    print("Отчет успешно создан и отправлен")
else:
    print("Ошибка создания или отправки отчета")
```

## Функции

### `main`

```python
async def main(suppier_to_presta):
    """На данный момент функция читает JSON со списком фотографий , которые были получены от Эмиля"""    
```

**Назначение**: Читает JSON со списком фотографий, полученных от Эмиля, и сохраняет товары в Prestashop.

**Параметры**:

- `suppier_to_presta`: Экземпляр класса `SupplierToPrestashopProvider`.

**Как работает функция**:

1. Устанавливает язык.
2. Загружает данные о товарах из JSON файла.
3. Создает экземпляр класса `SupplierToPrestashopProvider`.
4. Сохраняет товары в Prestashop.

**Примеры**:

```python
# Пример вызова функции main
asyncio.run(main())