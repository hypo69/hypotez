# Модуль `ali_promo_campaign.py`

## Обзор

Модуль предназначен для управления рекламными кампаниями на платформе AliExpress. Он включает в себя функциональность для обработки данных о категориях и товарах, создания и редактирования JSON-файлов с информацией о кампаниях, а также использование AI для генерации данных о кампаниях.

## Подробней

Класс `AliPromoCampaign` позволяет загружать и обрабатывать данные рекламных кампаний, управлять категориями и товарами, а также использовать ИИ для генерации описаний и других данных. Модуль поддерживает различные языки и валюты, обеспечивая гибкость в настройке кампаний. Расположен в `src/suppliers/aliexpress/campaign/ali_promo_campaign.py` и является частью подсистемы управления рекламными кампаниями AliExpress.

## Классы

### `AliPromoCampaign`

**Описание**: Управляет рекламной кампанией.

**Принцип работы**:
Класс `AliPromoCampaign` предназначен для управления рекламными кампаниями на платформе AliExpress. Он позволяет инициализировать кампанию, загружать существующие данные или создавать новые, обрабатывать товары в категориях, использовать AI для генерации контента и сохранять результаты в файлы. Класс обеспечивает гибкость в настройке и управлении кампаниями, поддерживая различные языки и валюты.

**Атрибуты**:
- `language` (str): Язык, используемый в кампании.
- `currency` (str): Валюта, используемая в кампании.
- `base_path` (Path): Базовый путь к файлам кампании в Google Drive.
- `campaign_name` (str): Название кампании.
- `campaign` (SimpleNamespace): Объект, представляющий кампанию.
- `campaign_ai` (SimpleNamespace): Объект, представляющий AI-сгенерированные данные для кампании.
- `gemini` (GoogleGenerativeAI): Инстанс модели Gemini для генерации текста.
- `openai` (OpenAIModel): Инстанс модели OpenAI для генерации текста.

**Методы**:
- `__init__`: Инициализирует объект `AliPromoCampaign`.
- `_models_payload`: Загружает параметры для AI моделей.
- `process_campaign`: Итерируется по категориям кампании и обрабатывает товары.
- `process_campaign_category`: Обрабатывает указанную категорию кампании для всех языков и валют.
- `process_new_campaign`: Создает новую рекламную кампанию.
- `process_ai_category`: Обрабатывает AI-генерацию данных для категорий.
- `process_category_products`: Обрабатывает товары в указанной категории.
- `dump_category_products_files`: Сохраняет данные о товарах в JSON-файлы.
- `set_categories_from_directories`: Устанавливает категории из названий директорий.
- `generate_output`: Сохраняет данные о товарах в различных форматах.
- `generate_html`: Создает HTML-файлы для категорий и корневой индексный файл.
- `generate_html_for_campaign`: Генерирует HTML-страницы для рекламной кампании.

### `__init__`

```python
def __init__(
    self,
    campaign_name: str,
    language: Optional[str] = None,
    currency: Optional[str] = None,
    model:str = 'openai'
)
```

**Назначение**: Инициализация объекта AliPromoCampaign для рекламной кампании.

**Параметры**:
- `campaign_name` (str): Название кампании.
- `language` (Optional[str]): Язык, используемый в кампании. По умолчанию `None`.
- `currency` (Optional[str]): Валюта, используемая в кампании. По умолчанию `None`.
- `model` (str): Модель искусственного интеллекта для использования. По умолчанию `'openai'`.

**Возвращает**:
- `None`

**Как работает функция**:
1. Функция инициализирует объект `AliPromoCampaign` с указанным названием, языком и валютой.
2. Определяет базовый путь к файлам кампании в Google Drive.
3. Загружает файл кампании в формате JSON, если он существует.
4. Если файл не найден, запускает процесс создания новой кампании.
5. Устанавливает язык и валюту кампании.
6. Вызывает метод `_models_payload` для загрузки параметров AI моделей.

**Примеры**:
```python
campaign = AliPromoCampaign(campaign_name="SummerSale", language="EN", currency="USD")
print(campaign.campaign_name)
```

### `_models_payload`

```python
def _models_payload(self):
```

**Назначение**: Загружает параметры для AI моделей.

**Параметры**:
- `self` (AliPromoCampaign): Экземпляр класса `AliPromoCampaign`.

**Возвращает**:
- `None`

**Как работает функция**:
1. Определяет путь к файлу с системными инструкциями для AI моделей.
2. Читает содержимое файла с инструкциями.
3. Инициализирует модели Gemini и OpenAI с использованием загруженных инструкций.

**Примеры**:
```python
campaign._models_payload()
```

### `process_campaign`

```python
def process_campaign(self):
```

**Назначение**: Итерируется по категориям рекламной кампании и обрабатывает товары категории через генератор партнерских ссылок.

**Параметры**:
- `self` (AliPromoCampaign): Экземпляр класса `AliPromoCampaign`.

**Возвращает**:
- `None`

**Как работает функция**:
1. Получает список названий категорий из директории `category`.
2. Для каждой категории вызывает методы `process_category_products` и `process_ai_category`.

**Примеры**:
```python
campaign.process_campaign()
```

### `process_campaign_category`

```python
def process_campaign_category(
    self, category_name: str
) -> list[SimpleNamespace] | None:
```

**Назначение**: Обрабатывает указанную категорию кампании для всех языков и валют.

**Параметры**:
- `self` (AliPromoCampaign): Экземпляр класса `AliPromoCampaign`.
- `category_name` (str): Название категории для обработки.

**Возвращает**:
- `list[SimpleNamespace] | None`: Список названий товаров в категории.

**Как работает функция**:
1. Вызывает методы `process_category_products` и `process_ai_category` для указанной категории.

**Примеры**:
```python
campaign.process_campaign_category(category_name="Electronics")
```

### `process_new_campaign`

```python
def process_new_campaign(
    self,
    campaign_name: str,
    language: Optional[str] = None,
    currency: Optional[str] = None,
):
```

**Назначение**: Создает новую рекламную кампанию.

**Параметры**:
- `self` (AliPromoCampaign): Экземпляр класса `AliPromoCampaign`.
- `campaign_name` (str): Название рекламной кампании.
- `language` (Optional[str]): Язык для кампании. По умолчанию `None`.
- `currency` (Optional[str]): Валюта для кампании. По умолчанию `None`.

**Возвращает**:
- `List[Tuple[str, Any]]`: Список кортежей с именами категорий и их обработанными результатами.

**Как работает функция**:
1. Если язык и валюта не указаны, обрабатывает все локали из списка `locales`.
2. Для каждой локали устанавливает язык и валюту.
3. Создает объект `SimpleNamespace` для представления кампании.
4. Вызывает метод `set_categories_from_directories` для заполнения категорий.
5. Копирует данные кампании в `campaign_ai`.
6. Для каждой категории вызывает методы `process_category_products` и `process_ai_category`.
7. Сохраняет данные кампании в JSON-файл.

**Flowchart**:

```
    ┌──────────────────────────────────────────────┐
    │ Start                                        │
    └──────────────────────────────────────────────┘
                      │
                      ▼
    ┌───────────────────────────────────────────────┐
    │ Check if `self.language` and `self.currency`  │
    │ are set                                       │
    └───────────────────────────────────────────────┘
                      │
            ┌─────────┴──────────────────────────┐
            │                                    │
            ▼                                    ▼
    ┌─────────────────────────────┐   ┌──────────────────────────────────────┐
    │Yes: `locale` = `{language:  │   │No: `locale` = {                      │
    │currency}`                   │   │     "EN": "USD",                     │
    │                             │   │     "HE": "ILS",                     │
    │                             │   │     "RU": "ILS"                      │
    │                             │   │    }                                 │
    └─────────────────────────────┘   └──────────────────────────────────────┘
                     │                         │
                     ▼                         ▼
    ┌───────────────────────────────────────────────┐
    │ For each `language`, `currency` in `locale`:  │
    │ - Set `self.language`, `self.currency`        │
    │ - Initialize `self.campaign`                  │
    └───────────────────────────────────────────────┘
                     │
                     ▼
    ┌───────────────────────────────────────────────┐
    │ Call `self.set_categories_from_directories()` │
    │ to populate categories                        │
    └───────────────────────────────────────────────┘
                     │
                     ▼
    ┌───────────────────────────────────────────────┐
    │ Copy `self.campaign` to `self.campaign_ai`    │
    │ and set `self.campaign_ai_file_name`          │
    └───────────────────────────────────────────────┘
                     │
                     ▼
    ┌───────────────────────────────────────────────┐
    │ For each `category_name` in campaign:         │
    │ - Call `self.process_category_products`       │
    │ - Call `self.process_ai_category`             │
    └───────────────────────────────────────────────┘
                     │
                     ▼
    ┌──────────────────────────────────────────────┐
    │ End                                          │
    └──────────────────────────────────────────────┘
```

**Примеры**:
```python
campaign.process_new_campaign(campaign_name="HolidaySale", language="RU", currency="ILS")
```

### `process_ai_category`

```python
def process_ai_category(self, category_name: Optional[str] = None):
```

**Назначение**: Обрабатывает AI-генерацию данных для категорий.

**Параметры**:
- `self` (AliPromoCampaign): Экземпляр класса `AliPromoCampaign`.
- `category_name` (Optional[str]): Название категории для обработки. Если не указано, обрабатываются все категории. По умолчанию `None`.

**Возвращает**:
- `None`

**Как работает функция**:
1. Создает копию данных кампании в `campaign_ai`.
2. Определяет внутреннюю функцию `_process_category` для обработки данных категории.
3. Если указано имя категории, обрабатывает только эту категорию, иначе обрабатывает все категории.
4. Сохраняет AI-сгенерированные данные в JSON-файл.

**Внутренние функции**:
- `_process_category`: обрабатывает AI-генерацию данных для указанной категории. Читает заголовки товаров из файла, формирует запрос к AI модели и обновляет данные категории в кампании.
- `get_response`: получает ответ от AI модели.

**Flowchart**:

```
    ┌──────────────────────────────────────────────┐
    │ Start                                        │
    └──────────────────────────────────────────────┘
                        │
                        ▼
    ┌───────────────────────────────────────────────┐
    │ Load system instructions from JSON file       │
    └───────────────────────────────────────────────┘
                        │
                        ▼
    ┌───────────────────────────────────────────────┐
    │ Initialize AI model with system instructions  │
    └───────────────────────────────────────────────┘
                        │
                        ▼
    ┌───────────────────────────────────────────────┐
    │ Check if `category_name` is provided          │
    └───────────────────────────────────────────────┘
                        │
        ┌─────────────────┴───────────────────┐
        │                                     │
        ▼                                     ▼
┌─────────────────────────────────────┐   ┌────────────────────────────────────┐
│ Process specified category          │   │ Iterate over all categories        │
│ - Load product titles               │   │ - Call `_process_category`         │
│ - Generate prompt                   │   │   for each category                │
│ - Get response from AI model        │   └────────────────────────────────────┘
│ - Update or add category            │
└─────────────────────────────────────┘
                        │
                        ▼
    ┌───────────────────────────────────────────────┐
    │ Save updated campaign data to file            │
    └───────────────────────────────────────────────┘
                        │
                        ▼
    ┌──────────────────────────────────────────────┐
    │ End                                          │
    └──────────────────────────────────────────────┘
```

**Примеры**:
```python
campaign.process_ai_category("Electronics")
campaign.process_ai_category()
```

### `process_category_products`

```python
def process_category_products(
    self, category_name: str
) -> Optional[List[SimpleNamespace]]:
```

**Назначение**: Обрабатывает товары в указанной категории.

**Параметры**:
- `self` (AliPromoCampaign): Экземпляр класса `AliPromoCampaign`.
- `category_name` (str): Название категории для обработки.

**Возвращает**:
- `Optional[List[SimpleNamespace]]`: Список объектов `SimpleNamespace`, представляющих товары. Возвращает `None`, если товары не найдены.

**Как работает функция**:
1. Определяет внутреннюю функцию `read_sources` для чтения идентификаторов товаров из файлов.
2. Вызывает `read_sources` для получения списка идентификаторов товаров.
3. Если идентификаторы не найдены, логирует ошибку и возвращает `None`.
4. Инициализирует объект `AliAffiliatedProducts` для генерации партнерских ссылок.
5. Вызывает метод `process_affiliate_products` для обработки товаров.
6. Возвращает список обработанных товаров.

**Внутренние функции**:
- `read_sources`: читает идентификаторы товаров из HTML-файлов и файла `sources.txt`.

**Flowchart**:

```
    ┌───────────────────────────────────────────────────────────┐
    │ Start                                                     │
    └───────────────────────────────────────────────────────────┘
                  │
                  ▼
    ┌───────────────────────────────────────────────────────────┐
    │ Call `read_sources(category_name)` to get product IDs     │
    │ - Searches for product IDs in HTML files and sources.txt  │
    └───────────────────────────────────────────────────────────┘
                  │
                  ▼
    ┌───────────────────────────────────────────────────────────┐
    │ Check if `prod_ids` is empty                              │
    │ - If empty, log an error and return `None`                │
    └───────────────────────────────────────────────────────────┘
                  │
                  ▼
    ┌───────────────────────────────────────────────────────────┐
    │ Initialize `AliAffiliatedProducts` with `language`        │
    │ and `currency`                                            │
    └───────────────────────────────────────────────────────────┘
                  │
                  ▼
    ┌───────────────────────────────────────────────────────────┐
    │ Call `process_affiliate_products`                         │
    │ - Pass `campaign`, `category_name`, and `prod_ids`        │
    └───────────────────────────────────────────────────────────┘
                  │
                  ▼
    ┌───────────────────────────────────────────────────────────┐
    │ Check if `affiliated_products` is empty                   │
    │ - If empty, log an error and return `None`                │
    └───────────────────────────────────────────────────────────┘
                  │
                  ▼
    ┌───────────────────────────────────────────────────────────┐
    │ Return `affiliated_products`                              │
    └───────────────────────────────────────────────────────────┘
                  │
                  ▼
    ┌───────────────────────────────────────────────────────────┐
    │ End                                                       │
    └───────────────────────────────────────────────────────────┘
```

**Примеры**:
```python
products: List[SimpleNamespace] = campaign.process_category_products("Electronics")
print(len(products))
```

### `dump_category_products_files`

```python
def dump_category_products_files(
    self, category_name: str, products: List[SimpleNamespace]
):
```

**Назначение**: Сохраняет данные о товарах в JSON-файлы.

**Параметры**:
- `self` (AliPromoCampaign): Экземпляр класса `AliPromoCampaign`.
- `category_name` (str): Имя категории.
- `products` (List[SimpleNamespace]): Список объектов `SimpleNamespace`, представляющих товары.

**Возвращает**:
- `None`

**Как работает функция**:
1. Проверяет, есть ли товары для сохранения.
2. Для каждого товара получает идентификатор и сохраняет данные в JSON-файл.

**Примеры**:
```python
campaign.dump_category_products_files("Electronics", products)
```

### `set_categories_from_directories`

```python
def set_categories_from_directories(self):
```

**Назначение**: Устанавливает категории рекламной кампании из названий директорий в `category`.

**Параметры**:
- `self` (AliPromoCampaign): Экземпляр класса `AliPromoCampaign`.

**Возвращает**:
- `None`

**Как работает функция**:
1. Получает список названий директорий из директории `category`.
2. Для каждой директории создает объект `SimpleNamespace` с атрибутами `category_name`, `title` и `description`.
3. Добавляет объект `SimpleNamespace` в объект `self.campaign.category`.

**Примеры**:
```python
self.set_categories_from_directories()
print(self.campaign.category.category1.category_name)
```

### `generate_output`

```python
async def generate_output(self, campaign_name: str, category_path: str | Path, products_list: list[SimpleNamespace] | SimpleNamespace):
```

**Назначение**: Сохраняет данные о товарах в различных форматах.

**Параметры**:
- `self` (AliPromoCampaign): Экземпляр класса `AliPromoCampaign`.
- `campaign_name` (str): Название кампании.
- `category_path` (str | Path): Путь к файлу категории.
- `products_list` (list[SimpleNamespace] | SimpleNamespace): Список продуктов или один продукт для сохранения.

**Возвращает**:
- `None`

**Как работает функция**:
1. Форматирует текущую временную метку для использования в именах файлов.
2. Преобразует входной список продуктов в список, если он не является списком.
3. Инициализирует пустые списки для хранения данных.
4. Итерирует по списку продуктов.
5. Создает словарь `categories_convertor` для преобразования категорий.
6. Сохраняет каждый продукт в виде отдельного JSON-файла с именем `<product_id>.json`.
7. Вызывает функции для сохранения заголовков продуктов и ссылок на продвижение.
8. Вызывает функцию для генерации HTML-файла для продуктов.

**Flowchart**:

```
        ┌───────────────────────────────┐
        │  Start `generate_output`      │
        └───────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────────┐
        │ Format `timestamp` for file   │
        │ names.                        │
        └───────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────────┐
        │ Check if `products_list` is   │
        │ a list; if not, convert it to │
        │ a list.                       │
        └───────────────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │ Initialize `_data_for_openai`,│
    │ `_promotion_links_list`, and  │
    │ `_product_titles` lists.      │
    └───────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ For each `product` in `products_list`:  │
└─────────────────────────────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────────┐
│ 1. Create `categories_convertor` dictionary   │
│ for `product`.                                │
└───────────────────────────────────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────────┐
│ 2. Add `categories_convertor` to `product`.   │
└───────────────────────────────────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────────┐
│ 3. Save `product` as `<product_id>.json`.     │
└───────────────────────────────────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────────┐
│ 4. Append `product_title` and                 │
│ `promotion_link` to their respective lists.   │
└───────────────────────────────────────────────┘
                    │                                               
                    ▼
    ┌───────────────────────────────┐
    │ Call `save_product_titles`    │
    │ with `_product_titles` and    │
    │ `category_path`.              │
    └───────────────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │ Call `save_promotion_links`   │
    │ with `_promotion_links_list`  │
    │ and `category_path`.          │
    └───────────────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────────┐
    │ Call `generate_html` with         │
    │ `campaign_name`, `category_path`, │
    │ and `products_list`.              │
    └───────────────────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │  End `generate_output`        │
    └───────────────────────────────┘
```

**Примеры**:
```python
products_list: list[SimpleNamespace] = [
    SimpleNamespace(product_id="123", product_title="Product A", promotion_link="http://example.com/product_a", 
                    first_level_category_id=1, first_level_category_name="Category1",
                    second_level_category_id=2, second_level_category_name="Subcategory1", 
                    product_main_image_url="http://example.com/image.png", product_video_url="http://example.com/video.mp4"),
    SimpleNamespace(product_id="124", product_title="Product B", promotion_link="http://example.com/product_b",
                    first_level_category_id=1, first_level_category_name="Category1",
                    second_level_category_id=3, second_level_category_name="Subcategory2",
                    product_main_image_url="http://example.com/image2.png", product_video_url="http://example.com/video2.mp4")
]
category_path: Path = Path("/path/to/category")
await generate_output("CampaignName", category_path, products_list)
```

### `generate_html`

```python
async def generate_html(self, campaign_name:str, category_path: str | Path, products_list: list[SimpleNamespace] | SimpleNamespace):
```

**Назначение**: Создает HTML-файлы для категорий и корневой индексный файл.

**Параметры**:
- `self` (AliPromoCampaign): Экземпляр класса `AliPromoCampaign`.
- `campaign_name` (str): Имя кампании.
- `category_path` (str | Path): Путь к файлу категории.
- `products_list` (list[SimpleNamespace] | SimpleNamespace): Список продуктов или один продукт для сохранения.

**Возвращает**:
- `None`

**Как работает функция**:
1. Преобразует `products_list` в список, если он не является списком.
2. Получает имя категории из `category_path`.
3. Инициализирует путь к HTML-файлу категории.
4. Создает словарь `category` для хранения заголовков продуктов.
5. Формирует HTML-содержимое, включая детали каждого продукта.
6. Сохраняет HTML-содержимое в файл категории.
7. Создает индексный HTML-файл кампании, содержащий ссылки на все категории.

**Примеры**:
```python
await self.generate_html(campaign_name, category_path, products_list)
```

### `generate_html_for_campaign`

```python
def generate_html_for_campaign(self, campaign_name: str):
```

**Назначение**: Генерирует HTML-страницы для рекламной кампании.

**Параметры**:
- `self` (AliPromoCampaign): Экземпляр класса `AliPromoCampaign`.
- `campaign_name` (str): Имя рекламной кампании.

**Возвращает**:
- `None`

**Как работает функция**:
1. Определяет корневой путь к кампании и извлекает список категорий.
2. Для каждой категории получает список продуктов.
3. Генерирует HTML-страницы для каждого продукта и категории.
4. Генерирует HTML-страницу кампании, отображающую все категории.

**Примеры**:
```python
campaign.generate_html_for_campaign("HolidaySale")