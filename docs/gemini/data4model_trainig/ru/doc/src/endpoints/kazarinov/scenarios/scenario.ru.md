# Сценарий создания мехирона для Сергея Казаринова

## Обзор

Этот скрипт является частью директории `hypotez/src/endpoints/kazarinov/scenarios` и предназначен для автоматизации процесса создания "мехирона" для Сергея Казаринова. Скрипт извлекает, парсит и обрабатывает данные о продуктах от различных поставщиков, подготавливает данные, обрабатывает их через ИИ и интегрирует с Facebook для публикации продуктов.

## Подробней

Этот код автоматизирует процесс сбора, обработки и публикации информации о продуктах для Сергея Казаринова. Он использует веб-скрапинг для извлечения данных, обрабатывает их с помощью моделей искусственного интеллекта и публикует в Facebook. Скрипт предназначен для упрощения и ускорения процесса создания контента, снижая необходимость в ручном вмешательстве.

## Классы

### `MexironBuilder`

**Описание**: Класс `MexironBuilder` предназначен для автоматизации процесса создания "мехирона". Он выполняет извлечение данных о продуктах, их обработку с помощью ИИ, генерацию отчетов и публикацию в Facebook.

**Атрибуты**:
- `driver`: Экземпляр Selenium WebDriver для управления браузером.
- `export_path`: Путь для экспорта обработанных данных.
- `mexiron_name`: Пользовательское имя для процесса мехирона.
- `price`: Цена для обработки.
- `timestamp`: Метка времени для процесса.
- `products_list`: Список обработанных данных о продуктах.
- `model`: Модель Google Generative AI для обработки текста.
- `config`: Конфигурация, загруженная из JSON файла.

**Методы**: 
- `__init__(self, driver: Driver, mexiron_name: Optional[str] = None)`
- `run_scenario(self, system_instruction: Optional[str] = None, price: Optional[str] = None, mexiron_name: Optional[str] = None, urls: Optional[str | List[str]] = None, bot = None) -> bool`
- `get_graber_by_supplier_url(self, url: str)`
- `convert_product_fields(self, f: ProductFields) -> dict`
- `save_product_data(self, product_data: dict)`
- `process_llm(self, products_list: List[str], lang: str, attempts: int = 3) -> tuple | bool`
- `post_facebook(self, mexiron: SimpleNamespace) -> bool`
- `create_report(self, data: dict, html_file: Path, pdf_file: Path)`

### `__init__(self, driver: Driver, mexiron_name: Optional[str] = None)`

```python
def __init__(self, driver: Driver, mexiron_name: Optional[str] = None):
    """Инициализирует класс `MexironBuilder` с необходимыми компонентами.
    Args:
        driver: Экземпляр Selenium WebDriver.
        mexiron_name: Пользовательское имя для процесса мехирона.
    """
    ...
```

### `run_scenario(self, system_instruction: Optional[str] = None, price: Optional[str] = None, mexiron_name: Optional[str] = None, urls: Optional[str | List[str]] = None, bot = None) -> bool`

```python
def run_scenario(self, system_instruction: Optional[str] = None, price: Optional[str] = None, mexiron_name: Optional[str] = None, urls: Optional[str | List[str]] = None, bot = None) -> bool:
    """Выполняет сценарий: парсит продукты, обрабатывает их через ИИ и сохраняет данные.
    Args:
        system_instruction: Системные инструкции для модели ИИ.
        price: Цена для обработки.
        mexiron_name: Пользовательское имя мехирона.
        urls: URLs страниц продуктов.
    Returns:
        True, если сценарий выполнен успешно, иначе False.
    """
    ...
```

#### Как работает функция:
Функция `run_scenario` выполняет основной сценарий обработки данных о продуктах. Она начинается с проверки, предоставлены ли URL-адреса продуктов для обработки. Если URL-адреса предоставлены, функция определяет, являются ли они URL-адресами OneTab и обрабатывает их соответствующим образом. Затем для каждого URL-адреса функция пытается получить соответствующий грабер, извлечь данные о продукте, преобразовать поля продукта, сохранить данные и обработать их с помощью ИИ. Если все этапы выполнены успешно, функция генерирует отчеты и отправляет PDF-файл через Telegram.

**Внутренние функции**:
- Проверка источника URL (IsOneTab)
- Проверка валидности данных (IsDataValid)
- Поиск грабера (IsGraberFound)
- Парсинг страницы (StartParsing)
- Преобразование данных (ConvertProductFields)
- Сохранение данных (SaveProductData)
- Обработка через AI (ProcessAIHe, ProcessAIRu)
- Сохранение JSON (SaveHeJSON, SaveRuJSON)
- Генерация отчетов (GenerateReports)
- Отправка PDF через Telegram (SendPDF)

#### Примеры:
```python
mexiron_builder.run_scenario(urls=['https://example.com/product1', 'https://example.com/product2'])
mexiron_builder.run_scenario(urls='https://example.com/onetab_url')
```

### `get_graber_by_supplier_url(self, url: str)`

```python
def get_graber_by_supplier_url(self, url: str):
    """Возвращает соответствующий грабер для данного URL поставщика.
    Args:
        url: URL страницы поставщика.
    Returns:
        Экземпляр грабера, если найден, иначе None.
    """
    ...
```

#### Как работает функция:
Функция `get_graber_by_supplier_url` принимает URL-адрес страницы поставщика и возвращает соответствующий грабер, который используется для извлечения данных с этой страницы. Функция анализирует URL-адрес, чтобы определить, какой поставщик связан с этим URL-адресом, и затем возвращает соответствующий грабер для этого поставщика.

#### Примеры:
```python
graber = mexiron_builder.get_graber_by_supplier_url('https://example.com/product')
if graber:
    print('Graber найден')
else:
    print('Graber не найден')
```

### `convert_product_fields(self, f: ProductFields) -> dict`

```python
def convert_product_fields(self, f: ProductFields) -> dict:
    """Конвертирует поля продукта в словарь.
    Args:
        f: Объект, содержащий парсированные данные о продукте.
    Returns:
        Форматированный словарь данных о продукте.
    """
    ...
```

#### Как работает функция:
Функция `convert_product_fields` принимает объект `ProductFields`, содержащий парсированные данные о продукте, и преобразует эти данные в форматированный словарь. Это необходимо для стандартизации данных перед их сохранением или дальнейшей обработкой.

#### Примеры:
```python
product_fields = ProductFields(...)
product_data = mexiron_builder.convert_product_fields(product_fields)
print(product_data)
```

### `save_product_data(self, product_data: dict)`

```python
def save_product_data(self, product_data: dict):
    """Сохраняет данные о продукте в файл.
    Args:
        product_data: Форматированные данные о продукте.
    """
    ...
```

#### Как работает функция:
Функция `save_product_data` принимает словарь `product_data`, содержащий форматированные данные о продукте, и сохраняет эти данные в файл. Функция генерирует имя файла на основе текущей метки времени и имени мехирона и сохраняет данные в формате JSON.

#### Примеры:
```python
product_data = {'name': 'Product Name', 'price': 100}
mexiron_builder.save_product_data(product_data)
```

### `process_llm(self, products_list: List[str], lang: str, attempts: int = 3) -> tuple | bool`

```python
def process_llm(self, products_list: List[str], lang: str, attempts: int = 3) -> tuple | bool:
    """Обрабатывает список продуктов через модель ИИ.
    Args:
        products_list: Список словарей данных о продуктах в виде строки.
        attempts: Количество попыток повторного запроса в случае неудачи.
    Returns:
        Обработанный ответ в форматах `ru` и `he`.
    """
    ...
```

#### Как работает функция:
Функция `process_llm` принимает список продуктов, представленных в виде строк, и язык, на котором нужно обработать данные, и использует модель ИИ для обработки этих данных. Функция отправляет данные в модель ИИ и возвращает обработанный ответ. Если запрос к модели ИИ не удался, функция повторяет запрос несколько раз.

#### Примеры:
```python
products_list = ['{"name": "Product 1", "price": 100}', '{"name": "Product 2", "price": 200}']
result = mexiron_builder.process_llm(products_list, 'ru')
print(result)
```

### `post_facebook(self, mexiron: SimpleNamespace) -> bool`

```python
def post_facebook(self, mexiron: SimpleNamespace) -> bool:
    """Выполняет сценарий публикации в Facebook.
    Args:
        mexiron: Обработанные данные для публикации.
    Returns:
        True, если публикация успешна, иначе False.
    """
    ...
```

#### Как работает функция:
Функция `post_facebook` принимает обработанные данные о продукте и публикует их в Facebook. Функция использует API Facebook для создания публикации с данными о продукте.

#### Примеры:
```python
mexiron_data = SimpleNamespace(name='Product Name', price=100)
result = mexiron_builder.post_facebook(mexiron_data)
if result:
    print('Публикация успешна')
else:
    print('Ошибка публикации')
```

### `create_report(self, data: dict, html_file: Path, pdf_file: Path)`

```python
def create_report(self, data: dict, html_file: Path, pdf_file: Path):
    """Генерирует HTML и PDF отчеты из обработанных данных.
    Args:
        data: Обработанные данные.
        html_file: Путь для сохранения HTML отчета.
        pdf_file: Путь для сохранения PDF отчета.
    """
    ...
```

#### Как работает функция:
Функция `create_report` принимает обработанные данные и создает HTML и PDF отчеты на основе этих данных. Функция использует шаблоны HTML для форматирования данных и создает PDF-файл из HTML-файла.

#### Примеры:
```python
data = {'name': 'Product Name', 'price': 100}
mexiron_builder.create_report(data, 'report.html', 'report.pdf')
```

## Использование

Для использования этого скрипта выполните следующие шаги:

1.  **Инициализация Driver**: Создайте экземпляр класса `Driver`.
2.  **Инициализация MexironBuilder**: Создайте экземпляр класса `MexironBuilder` с драйвером.
3.  **Запуск сценария**: Вызовите метод `run_scenario` с необходимыми параметрами.

### Пример

```python
from src.webdriver.driver import Driver
from src.endpoints.kazarinov.scenarios.scenario_pricelist import MexironBuilder

# Инициализация Driver
driver = Driver(...)

# Инициализация MexironBuilder
mexiron_builder = MexironBuilder(driver)

# Запуск сценария
urls = ['https://example.com/product1', 'https://example.com/product2']
mexiron_builder.run_scenario(urls=urls)
```

## Зависимости

-   `selenium`: Для веб-автоматизации.
-   `asyncio`: Для асинхронных операций.
-   `pathlib`: Для обработки путей к файлам.
-   `types`: Для создания простых пространств имен.
-   `typing`: Для аннотаций типов.
-   `src.ai.gemini`: Для обработки данных через ИИ.
-   `src.suppliers.*.graber`: Для извлечения данных от различных поставщиков.
-   `src.endpoints.advertisement.facebook.scenarios`: Для публикации в Facebook.

## Обработка ошибок

Скрипт включает надежную обработку ошибок, чтобы обеспечить продолжение выполнения даже в случае, если некоторые элементы не найдены или если возникли проблемы с веб-страницей. Это особенно полезно для обработки динамических или нестабильных веб-страниц.

## Вклад

Вклад в этот скрипт приветствуется. Пожалуйста, убедитесь, что любые изменения хорошо документированы и включают соответствующие тесты.

## Лицензия

Этот скрипт лицензирован под MIT License. Подробности смотрите в файле `LICENSE`.