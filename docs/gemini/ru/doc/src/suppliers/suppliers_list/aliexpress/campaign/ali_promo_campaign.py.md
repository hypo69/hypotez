# Модуль `ali_promo_campaign.py`

## Обзор

Модуль `ali_promo_campaign.py` предназначен для управления рекламными кампаниями на платформе AliExpress. Он включает в себя обработку данных о категориях и товарах, создание и редактирование JSON-файлов с информацией о кампаниях, а также использование AI для генерации данных о кампаниях. Класс `AliPromoCampaign` позволяет загружать и обрабатывать данные рекламных кампаний, управлять категориями и товарами, а также использовать ИИ для генерации описаний и других данных. Модуль поддерживает различные языки и валюты, обеспечивая гибкость в настройке кампаний.

## Подробнее

Модуль `ali_promo_campaign.py` предоставляет функциональность для автоматизации и управления рекламными кампаниями на AliExpress. Он позволяет создавать, обрабатывать и анализировать данные о категориях и товарах, а также использовать возможности искусственного интеллекта для оптимизации кампаний.

## Классы

### `AliPromoCampaign`

**Описание**: Класс `AliPromoCampaign` предназначен для управления рекламной кампанией на AliExpress. Он позволяет загружать, обрабатывать и генерировать данные, необходимые для проведения рекламных кампаний.

**Атрибуты**:

- `language` (str): Язык, используемый в кампании.
- `currency` (str): Валюта, используемая в кампании.
- `base_path` (Path): Базовый путь к файлам кампании в Google Drive.
- `campaign_name` (str): Название кампании.
- `campaign` (SimpleNamespace): Объект, представляющий данные кампании.
- `campaign_ai` (SimpleNamespace): Объект, представляющий AI-сгенерированные данные кампании.
- `gemini` (GoogleGenerativeAI): Объект для взаимодействия с моделью Google Gemini.
- `openai` (OpenAIModel): Объект для взаимодействия с моделью OpenAI.

**Методы**:

- `__init__`: Инициализирует объект `AliPromoCampaign`.
- `_models_payload`: Инициализирует модели AI для кампании.
- `process_campaign`: Итерируется по категориям кампании и обрабатывает товары.
- `process_campaign_category`: Обрабатывает указанную категорию кампании для всех языков и валют.
- `process_new_campaign`: Создает новую рекламную кампанию.
- `process_ai_category`: Обрабатывает AI-данные для указанной категории.
- `process_category_products`: Обрабатывает товары в указанной категории.
- `dump_category_products_files`: Сохраняет данные о товарах в JSON-файлы.
- `set_categories_from_directories`: Устанавливает категории кампании на основе названий директорий.
- `generate_output`: Сохраняет данные о товарах в различных форматах.
- `generate_html`: Создает HTML-файл для категории и корневой индексный файл.
- `generate_html_for_campaign`: Генерирует HTML-страницы для рекламной кампании.

## Методы класса

### `__init__`

```python
def __init__(
    self,
    campaign_name: str,
    language: Optional[str] = None,
    currency: Optional[str] = None,
    model:str = 'openai'
):
    """Инициализация объекта AliPromoCampaign для рекламной кампании.

    Args:
        campaign_file (Optional[str | Path]): Путь к файлу кампании или ссылка для загрузки кампании.
        campaign_name (Optional[str]): Название кампании.
        language (Optional[str | dict]): Язык, используемый в кампании.
        currency (Optional[str]): Валюта, используемая в кампании.

    Returns:
        SimpleNamespace: Объект, представляющий кампанию.

    Example:
        >>> campaign = AliPromoCampaign(campaign_name="SummerSale", language="EN", currency="USD")
        >>> print(campaign.campaign_name)

    """
```

**Назначение**: Инициализирует объект `AliPromoCampaign` с указанными параметрами кампании.

**Параметры**:

- `campaign_name` (str): Название кампании.
- `language` (Optional[str]): Язык, используемый в кампании (по умолчанию `None`).
- `currency` (Optional[str]): Валюта, используемая в кампании (по умолчанию `None`).
- `model` (str): Модель, используемая для AI (по умолчанию 'openai').

**Как работает функция**:

1. Определяет базовый путь к файлам кампании в Google Drive.
2. Пытается загрузить файл кампании из JSON. Если файл не найден, запускается процесс создания новой кампании.
3. Если файл кампании найден, устанавливает язык и валюту кампании.
4. Инициализирует модели AI.

### `_models_payload`

```python
def _models_payload(self):
    """ """
```

**Назначение**: Инициализирует модели AI (Google Gemini и OpenAI) для использования в кампании.

**Как работает функция**:

1. Определяет путь к файлу с системными инструкциями для AI.
2. Читает системные инструкции из файла.
3. Инициализирует модели Google Gemini и OpenAI с системными инструкциями.

### `process_campaign`

```python
def process_campaign(self):
    """Функция итерируется по категориям рекламной кампании и обрабатывает товары категории через генератор партнерских ссылок.

    Example:
        >>> campaign.process_campaign()
    """
```

**Назначение**: Итерируется по категориям рекламной кампании и обрабатывает товары каждой категории.

**Как работает функция**:

1. Получает список названий категорий из директорий.
2. Для каждой категории вызывает методы `process_category_products` и `process_ai_category`.

### `process_campaign_category`

```python
def process_campaign_category(
    self, category_name: str
) -> list[SimpleNamespace] | None:
    """
    Processes a specific category within a campaign for all languages and currencies.
    @param campaign_name: Name of the advertising campaign.
    @param category_name: Category for the campaign.
    @param language: Language for the campaign.
    @param currency: Currency for the campaign.
    @return: List of product titles within the category.
    """
```

**Назначение**: Обрабатывает указанную категорию в кампании для всех языков и валют.

**Параметры**:

- `category_name` (str): Название категории для обработки.

**Как работает функция**:

1. Вызывает методы `process_category_products` и `process_ai_category` для обработки указанной категории.

### `process_new_campaign`

```python
def process_new_campaign(
    self,
    campaign_name: str,
    language: Optional[str] = None,
    currency: Optional[str] = None,
):
    """Создание новой рекламной кампании.
    Условия для создания кампании:
    - директория кампании с питоник названием
    - вложенная директория `campaign`, в ней директории с питоник названиями категорий
    - файл sources.txt и/или директория `sources` с файлами `<product)id>.html`

    Args:
        campaign_name (Optional[str]): Название рекламной кампании.
        language (Optional[str]): Язык для кампании (необязательно).
        currency (Optional[str]): Валюта для кампании (необязательно).

    Returns:
        List[Tuple[str, Any]]: Список кортежей с именами категорий и их обработанными результатами.

    Example:
        >>> campaign.process_new_campaign(campaign_name="HolidaySale", language="RU", currency="ILS")

    Flowchart:
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

    """
```

**Назначение**: Создает новую рекламную кампанию, обрабатывая категории и товары.

**Параметры**:

- `campaign_name` (str): Название рекламной кампании.
- `language` (Optional[str]): Язык для кампании (по умолчанию `None`).
- `currency` (Optional[str]): Валюта для кампании (по умолчанию `None`).

**Как работает функция**:

1. Определяет язык и валюту кампании.
2. Создает объект `SimpleNamespace` для представления кампании.
3. Устанавливает категории кампании из директорий.
4. Копирует данные кампании в объект `campaign_ai`.
5. Для каждой категории вызывает методы `process_category_products` и `process_ai_category`.
6. Сохраняет данные кампании в JSON-файл.

### `process_ai_category`

```python
def process_ai_category(self, category_name: Optional[str] = None):
    """Processes the AI campaign for a specified category or all categories.

        This method processes AI-generated data for the specified category in the campaign.
        If no category name is provided, it processes all categories.

        Args:
            category_name (Optional[str]): The name of the category to process. If not provided, all categories are processed.

        Example:
            >>> campaign.process_ai_category("Electronics")
            >>> campaign.process_ai_category()

        Flowchart:
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

    """
```

**Назначение**: Обрабатывает AI-сгенерированные данные для указанной категории или для всех категорий кампании.

**Параметры**:

- `category_name` (Optional[str]): Название категории для обработки (по умолчанию `None`).

**Как работает функция**:

1. Определяет функцию `_process_category` для обработки данных категории.
2. Если указано имя категории, обрабатывает только эту категорию.
3. Если имя категории не указано, обрабатывает все категории в кампании.
4. Сохраняет AI-сгенерированные данные в JSON-файл.

**Внутренние функции**:

### `_process_category`

```python
def _process_category(category_name: str):
    """Processes AI-generated category data and updates the campaign category."""
```

**Назначение**: Обрабатывает AI-сгенерированные данные для указанной категории и обновляет данные категории в кампании.

**Параметры**:

- `category_name` (str): Название категории для обработки.

**Как работает функция**:

1. Определяет путь к файлу с названиями товаров для категории.
2. Читает названия товаров из файла.
3. Формирует запрос для AI-модели.
4. Получает ответ от AI-модели.
5. Преобразует ответ в объект `SimpleNamespace`.
6. Обновляет данные категории в кампании на основе ответа AI.

### `process_category_products`

```python
def process_category_products(
    self, category_name: str
) -> Optional[List[SimpleNamespace]]:
    """Processes products in a specific category.

            Args:
                category_name (str): The name of the category.

            Returns:
                Optional[List[SimpleNamespace]]: A list of `SimpleNamespace` objects representing the products.
                Returns `None` if no products are found.

            Example:
                >>> products: List[SimpleNamespace] = campaign.process_category_products("Electronics")
                >>> print(len(products))
                20
                >>> for product in products:
                >>>     pprint(product)  # Use pprint from `src.utils.pprint`

            Notes:
                The function attempts to read product IDs from both HTML files and text files within the specified category's
                `sources` directory. If no product IDs are found, an error is logged, and the function returns `None`.
                If affiliated products are found, they are returned; otherwise, an error is logged, and the function returns `None`.
            Flowchart:
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

    """
```

**Назначение**: Обрабатывает товары в указанной категории, извлекая информацию о товарах и генерируя партнерские ссылки.

**Параметры**:

- `category_name` (str): Название категории для обработки.

**Возвращает**:

- `Optional[List[SimpleNamespace]]`: Список объектов `SimpleNamespace`, представляющих товары, или `None`, если товары не найдены.

**Как работает функция**:

1. Определяет функцию `read_sources` для чтения идентификаторов товаров из файлов.
2. Получает список идентификаторов товаров из функции `read_sources`.
3. Если идентификаторы товаров не найдены, возвращает `None`.
4. Инициализирует объект `AliAffiliatedProducts` для генерации партнерских ссылок.
5. Вызывает метод `process_affiliate_products` для обработки товаров и генерации партнерских ссылок.

**Внутренние функции**:

### `read_sources`

```python
def read_sources(category_name: str) -> Optional[List[str]]:
    """Reads product sources and extracts product IDs.

    Args:
        category_name (str): The name of the category.

    Returns:
        Optional[List[str]]: A list of product IDs if found; otherwise, `None`.

    Example:
        >>> product_ids: Optional[List[str]] = read_sources("Electronics")
        >>> print(product_ids)
        ['12345', '67890', ...]

    Notes:
        This function looks for product IDs in both HTML files and a `sources.txt` file located
        in the category's `sources` directory. If no product IDs are found, it returns `None`.
    """
```

**Назначение**: Читает источники товаров и извлекает идентификаторы товаров из HTML-файлов и файла `sources.txt`.

**Параметры**:

- `category_name` (str): Название категории.

**Возвращает**:

- `Optional[List[str]]`: Список идентификаторов товаров, если они найдены; в противном случае `None`.

**Как работает функция**:

1. Ищет HTML-файлы в директории `sources` указанной категории.
2. Извлекает идентификаторы товаров из HTML-файлов.
3. Читает файл `sources.txt` и извлекает идентификаторы товаров из URL-адресов.
4. Объединяет все найденные идентификаторы товаров в один список.

### `dump_category_products_files`

```python
def dump_category_products_files(
    self, category_name: str, products: List[SimpleNamespace]
):
    """Сохранение данных о товарах в JSON файлы.

    Args:
        category_name (str): Имя категории.
        products (List[SimpleNamespace]): Список объектов SimpleNamespace, представляющих товары.

    Example:
        >>> campaign.dump_category_products_files("Electronics", products)
    """
```

**Назначение**: Сохраняет данные о товарах в JSON-файлы.

**Параметры**:

- `category_name` (str): Имя категории.
- `products` (List[SimpleNamespace]): Список объектов `SimpleNamespace`, представляющих товары.

**Как работает функция**:

1. Для каждого товара в списке создает JSON-файл с данными товара.

### `set_categories_from_directories`

```python
def set_categories_from_directories(self):
    """Устанавливает категории рекламной кампании из названий директорий в `category`.

    Преобразует каждый элемент списка категорий в объект `SimpleNamespace` с атрибутами
    `category_name`, `title`, и `description`.

    Example:
        >>> self.set_categories_from_directories()
        >>> print(self.campaign.category.category1.category_name)
    """
```

**Назначение**: Устанавливает категории рекламной кампании на основе названий директорий в директории `category`.

**Как работает функция**:

1. Получает список названий директорий в директории `category`.
2. Для каждой директории создает объект `SimpleNamespace` с атрибутами `category_name`, `title` и `description` и добавляет его в объект `campaign.category`.

### `generate_output`

```python
async def generate_output(self, campaign_name: str, category_path: str | Path, products_list: list[SimpleNamespace] | SimpleNamespace):
    """
    Saves product data in various formats:

    - `<product_id>.json`: Contains all product parameters, one file per product.
    - `ai_{timestamp}.json`: A common file for all products with specific keys.
    - `promotion_links.txt`: A list of product links, created in the `save_promotion_links()` function.
    - `category_products_titles.json`: File containing title, `product_id`, `first_category_name`, and `second_category_name` of each product in the category.

    Args:
        campaign_name (str): The name of the campaign for the output files.
        category_path (str | Path): The path to save the output files.
        products_list (list[SimpleNamespace] | SimpleNamespace): List of products or a single product to save.

    Returns:
        None

    Example:
        >>> products_list: list[SimpleNamespace] = [
        ...     SimpleNamespace(product_id="123", product_title="Product A", promotion_link="http://example.com/product_a", 
        ...                     first_level_category_id=1, first_level_category_name="Category1",
        ...                     second_level_category_id=2, second_level_category_name="Subcategory1", 
        ...                     product_main_image_url="http://example.com/image.png", product_video_url="http://example.com/video.mp4"),
        ...     SimpleNamespace(product_id="124", product_title="Product B", promotion_link="http://example.com/product_b",
        ...                     first_level_category_id=1, first_level_category_name="Category1",
        ...                     second_level_category_id=3, second_level_category_name="Subcategory2",
        ...                     product_main_image_url="http://example.com/image2.png", product_video_url="http://example.com/video2.mp4")
        ... ]
        >>> category_path: Path = Path("/path/to/category")
        >>> await generate_output("CampaignName", category_path, products_list)

    Flowchart:
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

    ### Flowchart Description

    1. **Start `generate_output`**: The function begins execution.
    2. **Format `timestamp` for file names**: Generate a timestamp to use in filenames.
    3. **Check if `products_list` is a list**: Ensure that `products_list` is in list format.
    4. **Initialize `_data_for_openai`, `_promotion_links_list`, and `_product_titles` lists**: Prepare empty lists to collect data.
    5. **For each `product` in `products_list`**: Process each product in the list.
    - **Create `categories_convertor` dictionary for `product`**: Create a dictionary for category conversion.
    - **Add `categories_convertor` to `product`**: Attach this dictionary to the product.
    - **Save `product` as `<product_id>.json`**: Save product details in a JSON file.
    - **Append `product_title` and `promotion_link` to their respective lists**: Collect titles and links.
    6. **Call `save_product_titles` with `_product_titles` and `category_path`**: Save titles data to a file.
    7. **Call `save_promotion_links` with `_promotion_links_list` and `category_path`**: Save promotion links to a file.
    8. **Call `generate_html` with `campaign_name`, `category_path`, and `products_list`**: Generate HTML output for products.
    9. **End `generate_output`**: The function completes execution.

    This flowchart captures the key steps and processes involved in the `generate_output` function.

    """
```

**Назначение**: Сохраняет данные о товарах в различных форматах, включая JSON-файлы, списки ссылок и HTML-страницы.

**Параметры**:

- `campaign_name` (str): Название кампании.
- `category_path` (str | Path): Путь к категории.
- `products_list` (list[SimpleNamespace] | SimpleNamespace): Список или единичный объект `SimpleNamespace`, представляющий товары.

**Как работает функция**:

1.  Форматирует текущую временную метку для использования в именах файлов.
2.  Преобразует `products_list` в список, если это не список.
3.  Инициализирует пустые списки `_data_for_openai`, `_promotion_links_list` и `_product_titles`.
4.  Для каждого продукта в `products_list`:
    *   Создает словарь `categories_convertor` для категорий продукта.
    *   Добавляет `categories_convertor` к продукту.
    *   Сохраняет продукт в формате JSON (`<product_id>.json`).
    *   Добавляет заголовок продукта и ссылку на продвижение в соответствующие списки.
5.  Вызывает `save_product_titles` для сохранения заголовков продуктов.
6.  Вызывает `save_promotion_links` для сохранения ссылок на продвижение.
7.  Вызывает `generate_html` для создания HTML-страницы.

### `generate_html`

```python
async def generate_html(self, campaign_name:str, category_path: str | Path, products_list: list[SimpleNamespace] | SimpleNamespace):
    """ Creates an HTML file for the category and a root index file.

    @param products_list: List of products to include in the HTML.
    @param category_path: Path to save the HTML file.
    """
```

**Назначение**: Создает HTML-файл для категории и корневой индексный файл.

**Параметры**:

- `products_list` (list[SimpleNamespace] | SimpleNamespace): Список продуктов для включения в HTML.
- `category_path` (str | Path): Путь для сохранения HTML-файла.

**Как работает функция**:

1. Преобразует `products_list` в список, если это не список.
2. Определяет имя категории из `category_path`.
3. Создает HTML-контент, включая информацию о продуктах (изображение, заголовок, цену, категорию и ссылку для покупки).
4. Сохраняет HTML-контент в файле `<category_name>.html`.
5. Генерирует основной файл `index.html`, который содержит ссылки на все HTML-файлы категорий.

### `generate_html_for_campaign`

```python
def generate_html_for_campaign(self, campaign_name: str):
    """Генерирует HTML-страницы для рекламной кампании.

    Args:
        campaign_name (str): Имя рекламной кампании.

    Example:
        >>> campaign.generate_html_for_campaign("HolidaySale")
    """
```

**Назначение**: Генерирует HTML-страницы для рекламной кампании, создавая страницы для каждой категории и каждого товара.

**Параметры**:

- `campaign_name` (str): Имя рекламной кампании.

**Как работает функция**:

1.  Определяет корневой каталог кампании и получает список категорий.
2.  Для каждой категории:
    *   Получает список товаров.
    *   Для каждого товара генерирует HTML-страницу.
    *   Генерирует HTML-страницу для категории.
3.  Генерирует HTML-страницу для всей кампании.

## Параметры класса

- `language` (str): Язык, используемый в кампании.
- `currency` (str): Валюта, используемая в кампании.
- `base_path` (Path): Базовый путь к файлам кампании.
- `campaign_name` (str): Название кампании.
- `campaign` (SimpleNamespace): Объект, представляющий кампанию.
- `campaign_ai` (SimpleNamespace): Объект, представляющий AI-сгенерированные данные кампании.
- `gemini` (GoogleGenerativeAI): Объект для взаимодействия с моделью Google Gemini.
- `openai` (OpenAIModel): Объект для взаимодействия с моделью OpenAI.

## Примеры

Примеры использования класса и его методов для различных сценариев управления рекламными кампаниями.
```
>>> campaign = AliPromoCampaign(campaign_name="SummerSale", language="EN", currency="USD")
>>> print(campaign.campaign_name)

>>> campaign.process_campaign()

>>> products: List[SimpleNamespace] = campaign.process_category_products("Electronics")
>>> print(len(products))

>>> campaign.generate_html_for_campaign("HolidaySale")
```