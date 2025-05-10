# Сценарий создания мехирона для Сергея Казаринова

## Обзор

Этот скрипт, расположенный в директории `hypotez/src/endpoints/kazarinov/scenarios`, предназначен для автоматизации процесса создания "мехирона" для Сергея Казаринова. Он включает извлечение, парсинг и обработку данных о товарах от различных поставщиков, их подготовку, обработку с использованием ИИ и интеграцию с Facebook для публикации товаров.

## Подробнее

Скрипт автоматизирует процесс сбора, обработки и публикации информации о товарах. Он предназначен для упрощения и ускорения работы по созданию "мехирона" для Сергея Казаринова.
Он извлекает данные от различных поставщиков, преобразует их в нужный формат, обрабатывает с помощью ИИ и публикует в Facebook.

## Классы

### `MexironBuilder`

**Описание**: Класс `MexironBuilder` предназначен для автоматизации процесса создания "мехирона", включая парсинг данных о товарах, их обработку с помощью ИИ и публикацию в Facebook.

**Атрибуты**:

- `driver`: Экземпляр Selenium WebDriver для управления браузером.
- `export_path`: Путь для экспорта обработанных данных.
- `mexiron_name`: Пользовательское имя для процесса мехирона.
- `price`: Цена, используемая при обработке данных.
- `timestamp`: Временная метка для процесса мехирона.
- `products_list`: Список обработанных данных о товарах.
- `model`: Модель Google Generative AI для обработки текста.
- `config`: Конфигурация, загруженная из JSON файла.

**Принцип работы**:
Класс инициализируется с экземпляром драйвера WebDriver и пользовательским именем мехирона. Он загружает конфигурацию, системные инструкции и инициализирует модель ИИ. Основной метод `run_scenario` выполняет шаги по парсингу данных о товарах, их обработке через ИИ, сохранению и публикации в Facebook.

**Методы**:

- `__init__(self, driver: Driver, mexiron_name: Optional[str] = None)`
- `run_scenario(self, system_instruction: Optional[str] = None, price: Optional[str] = None, mexiron_name: Optional[str] = None, urls: Optional[str | List[str]] = None, bot = None) -> bool`
- `get_graber_by_supplier_url(self, url: str)`
- `convert_product_fields(self, f: ProductFields) -> dict`
- `save_product_data(self, product_data: dict)`
- `process_llm(self, products_list: List[str], lang: str, attempts: int = 3) -> tuple | bool`
- `post_facebook(self, mexiron: SimpleNamespace) -> bool`
- `create_report(self, data: dict, html_file: Path, pdf_file: Path)`

## Методы класса

### `__init__(self, driver: Driver, mexiron_name: Optional[str] = None)`

**Назначение**: Инициализирует класс `MexironBuilder` с необходимыми компонентами.

**Параметры**:

- `driver` (Driver): Экземпляр Selenium WebDriver для управления браузером.
- `mexiron_name` (Optional[str], optional): Пользовательское имя для процесса мехирона. По умолчанию `None`.

**Пример**:

```python
from src.webdriver.driver import Driver
from src.endpoints.kazarinov.scenarios.scenario_pricelist import MexironBuilder

driver = Driver(browser_name='chrome')
mexiron_builder = MexironBuilder(driver, mexiron_name='test_mexiron')
```

### `run_scenario(self, system_instruction: Optional[str] = None, price: Optional[str] = None, mexiron_name: Optional[str] = None, urls: Optional[str | List[str]] = None, bot = None) -> bool`

**Назначение**: Выполняет основной сценарий: парсит товары, обрабатывает их через ИИ и сохраняет данные.

**Параметры**:

- `system_instruction` (Optional[str], optional): Системные инструкции для модели ИИ. По умолчанию `None`.
- `price` (Optional[str], optional): Цена для обработки. По умолчанию `None`.
- `mexiron_name` (Optional[str], optional): Пользовательское имя мехирона. По умолчанию `None`.
- `urls` (Optional[str | List[str]], optional): URL-адреса страниц товаров. По умолчанию `None`.
- `bot`: Экземпляр бота (необходимо уточнить, что это за бот).

**Возвращает**:

- `bool`: `True`, если сценарий выполнен успешно, иначе `False`.

**Как работает функция**:

1. Проверяет, предоставлены ли URL-адреса для парсинга.
2. Если URL-адреса предоставлены, определяет грабер для каждого URL.
3. Извлекает данные о товарах с помощью грабера.
4. Конвертирует поля товара в нужный формат.
5. Сохраняет данные о товаре.
6. Обрабатывает данные с использованием модели ИИ.
7. Генерирует отчеты в формате HTML и PDF.
8. Публикует данные в Facebook.

**Примеры**:

```python
from src.webdriver.driver import Driver
from src.endpoints.kazarinov.scenarios.scenario_pricelist import MexironBuilder

driver = Driver(browser_name='chrome')
mexiron_builder = MexironBuilder(driver, mexiron_name='test_mexiron')
urls = ['https://example.com/product1', 'https://example.com/product2']
success = mexiron_builder.run_scenario(urls=urls, price='100', system_instruction='Some instruction')
print(f"Scenario success: {success}")
```

### `get_graber_by_supplier_url(self, url: str)`

**Назначение**: Возвращает соответствующий грабер для данного URL поставщика.

**Параметры**:

- `url` (str): URL страницы поставщика.

**Возвращает**:

- Экземпляр грабера, если найден, иначе `None`.

**Как работает функция**:
Функция определяет поставщика на основе URL и возвращает соответствующий грабер, который используется для извлечения данных с сайта поставщика.

**Пример**:

```python
from src.webdriver.driver import Driver
from src.endpoints.kazarinov.scenarios.scenario_pricelist import MexironBuilder

driver = Driver(browser_name='chrome')
mexiron_builder = MexironBuilder(driver, mexiron_name='test_mexiron')
url = 'https://example.com/product'
graber = mexiron_builder.get_graber_by_supplier_url(url)
if graber:
    print("Graber found")
else:
    print("Graber not found")
```

### `convert_product_fields(self, f: ProductFields) -> dict`

**Назначение**: Конвертирует поля товара в словарь.

**Параметры**:

- `f` (ProductFields): Объект, содержащий парсированные данные о товаре.

**Возвращает**:

- `dict`: Форматированный словарь данных о товаре.

**Как работает функция**:
Функция преобразует объект `ProductFields` в словарь, чтобы данные было удобно обрабатывать и сохранять.

**Пример**:

```python
from src.webdriver.driver import Driver
from src.endpoints.kazarinov.scenarios.scenario_pricelist import MexironBuilder

driver = Driver(browser_name='chrome')
mexiron_builder = MexironBuilder(driver, mexiron_name='test_mexiron')

class ProductFields:
    def __init__(self):
        self.name = "Example Product"
        self.price = "100"

product_fields = ProductFields()
product_data = mexiron_builder.convert_product_fields(product_fields)
print(product_data)
```

### `save_product_data(self, product_data: dict)`

**Назначение**: Сохраняет данные о товаре в файл.

**Параметры**:

- `product_data` (dict): Форматированные данные о товаре.

**Как работает функция**:
Функция сохраняет данные о товаре в файл, чтобы их можно было использовать для дальнейшей обработки или анализа.

**Пример**:

```python
from src.webdriver.driver import Driver
from src.endpoints.kazarinov.scenarios.scenario_pricelist import MexironBuilder

driver = Driver(browser_name='chrome')
mexiron_builder = MexironBuilder(driver, mexiron_name='test_mexiron')
product_data = {'name': 'Example Product', 'price': '100'}
mexiron_builder.save_product_data(product_data)
```

### `process_llm(self, products_list: List[str], lang: str, attempts: int = 3) -> tuple | bool`

**Назначение**: Обрабатывает список товаров через модель ИИ.

**Параметры**:

- `products_list` (List[str]): Список словарей данных о товарах в виде строки.
- `lang` (str): Язык обработки (`ru` или `he`).
- `attempts` (int): Количество попыток повторного запроса в случае неудачи. По умолчанию `3`.

**Возвращает**:

- `tuple | bool`: Обработанный ответ в форматах `ru` и `he` или `False` в случае неудачи.

**Как работает функция**:
Функция использует модель ИИ для обработки списка товаров на указанном языке и возвращает обработанные данные.

**Пример**:

```python
from src.webdriver.driver import Driver
from src.endpoints.kazarinov.scenarios.scenario_pricelist import MexironBuilder

driver = Driver(browser_name='chrome')
mexiron_builder = MexironBuilder(driver, mexiron_name='test_mexiron')
products_list = ["{'name': 'Example Product', 'price': '100'}"]
result = mexiron_builder.process_llm(products_list, 'ru')
print(result)
```

### `post_facebook(self, mexiron: SimpleNamespace) -> bool`

**Назначение**: Выполняет сценарий публикации в Facebook.

**Параметры**:

- `mexiron` (SimpleNamespace): Обработанные данные для публикации.

**Возвращает**:

- `bool`: `True`, если публикация успешна, иначе `False`.

**Как работает функция**:
Функция публикует данные о товаре в Facebook, используя предоставленные обработанные данные.

**Пример**:

```python
from src.webdriver.driver import Driver
from src.endpoints.kazarinov.scenarios.scenario_pricelist import MexironBuilder
from types import SimpleNamespace

driver = Driver(browser_name='chrome')
mexiron_builder = MexironBuilder(driver, mexiron_name='test_mexiron')
mexiron = SimpleNamespace(name='Example Product', price='100')
success = mexiron_builder.post_facebook(mexiron)
print(f"Facebook post success: {success}")
```

### `create_report(self, data: dict, html_file: Path, pdf_file: Path)`

**Назначение**: Генерирует отчеты в формате HTML и PDF из обработанных данных.

**Параметры**:

- `data` (dict): Обработанные данные.
- `html_file` (Path): Путь для сохранения HTML отчета.
- `pdf_file` (Path): Путь для сохранения PDF отчета.

**Как работает функция**:
Функция создает HTML и PDF отчеты на основе предоставленных данных и сохраняет их по указанным путям.

**Пример**:

```python
from src.webdriver.driver import Driver
from src.endpoints.kazarinov.scenarios.scenario_pricelist import MexironBuilder
from pathlib import Path

driver = Driver(browser_name='chrome')
mexiron_builder = MexironBuilder(driver, mexiron_name='test_mexiron')
data = {'name': 'Example Product', 'price': '100'}
html_file = Path('report.html')
pdf_file = Path('report.pdf')
mexiron_builder.create_report(data, html_file, pdf_file)
```

## Параметры класса

- `driver` (Driver): Экземпляр Selenium WebDriver для управления браузером.
- `export_path` (str): Путь для экспорта обработанных данных.
- `mexiron_name` (str): Пользовательское имя для процесса мехирона.
- `price` (str): Цена, используемая при обработке данных.
- `timestamp` (datetime): Временная метка для процесса мехирона.
- `products_list` (List[dict]): Список обработанных данных о товарах.
- `model` (Google Generative AI): Модель Google Generative AI для обработки текста.
- `config` (dict): Конфигурация, загруженная из JSON файла.

## Использование

Для использования этого скрипта выполните следующие шаги:

1. **Инициализация Driver**: Создайте экземпляр класса `Driver`.
2. **Инициализация MexironBuilder**: Создайте экземпляр класса `MexironBuilder` с драйвером.
3. **Запуск сценария**: Вызовите метод `run_scenario` с необходимыми параметрами.

## Зависимости

- `selenium`: Для веб-автоматизации.
- `asyncio`: Для асинхронных операций.
- `pathlib`: Для обработки путей к файлам.
- `types`: Для создания простых пространств имен.
- `typing`: Для аннотаций типов.
- `src.ai.gemini`: Для обработки данных через ИИ.
- `src.suppliers.*.graber`: Для извлечения данных от различных поставщиков.
- `src.endpoints.advertisement.facebook.scenarios`: Для публикации в Facebook.

## Обработка ошибок

Скрипт включает надежную обработку ошибок, чтобы обеспечить продолжение выполнения даже в случае, если некоторые элементы не найдены или если возникли проблемы с веб-страницей. Это особенно полезно для обработки динамических или нестабильных веб-страниц.

## Вклад

Вклад в этот скрипт приветствуется. Пожалуйста, убедитесь, что любые изменения хорошо документированы и включают соответствующие тесты.

## Лицензия

Этот скрипт лицензирован под MIT License. Подробности смотрите в файле `LICENSE`.