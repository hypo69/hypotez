# Модуль: src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign

## Обзор

Модуль `ali_promo_campaign.py` предназначен для управления рекламными кампаниями на платформе AliExpress. Он включает в себя обработку данных о категориях и товарах, создание и редактирование JSON-файлов с информацией о кампаниях, а также использование AI для генерации данных о кампаниях.

## Подробней

Модуль предоставляет класс `AliPromoCampaign`, который позволяет загружать и обрабатывать данные рекламных кампаний, управлять категориями и товарами, а также использовать ИИ для генерации описаний и других данных. Модуль поддерживает различные языки и валюты, обеспечивая гибкость в настройке кампаний.

## Классы

### `AliPromoCampaign`

**Описание**: Класс для управления рекламными кампаниями AliExpress.

**Атрибуты**:
- `language` (str): Язык кампании.
- `currency` (str): Валюта кампании.
- `base_path` (Path): Базовый путь к директории кампании.
- `campaign_name` (str): Название кампании.
- `campaign` (SimpleNamespace): Объект, представляющий данные кампании.
- `campaign_ai` (SimpleNamespace): Объект, представляющий AI-данные кампании.
- `gemini` (GoogleGenerativeAi): Объект для взаимодействия с моделью Gemini AI.
- `openai` (OpenAIModel): Объект для взаимодействия с моделью OpenAI.

**Методы**:
- `__init__`: Инициализирует объект `AliPromoCampaign`.
- `_models_payload`: Настраивает модели AI для использования в кампании.
- `process_campaign`: Итерируется по категориям кампании и обрабатывает товары.
- `process_campaign_category`: Обрабатывает определенную категорию в кампании для всех языков и валют.
- `process_new_campaign`: Создает новую рекламную кампанию.
- `process_llm_category`: Обрабатывает AI-данные для указанной категории.
- `process_category_products`: Обрабатывает товары в указанной категории.
- `dump_category_products_files`: Сохраняет данные о товарах в JSON-файлы.
- `set_categories_from_directories`: Устанавливает категории кампании на основе директорий.
- `generate_output`: Сохраняет данные о товарах в различных форматах (JSON, txt, HTML).
- `generate_html`: Создает HTML-файлы для категорий.
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
) -> None:
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
    ...
```

**Назначение**: Инициализирует объект `AliPromoCampaign` с указанными параметрами.

**Параметры**:
- `campaign_name` (str): Название рекламной кампании.
- `language` (Optional[str]): Язык кампании (по умолчанию `None`).
- `currency` (Optional[str]): Валюта кампании (по умолчанию `None`).
- `model` (str): Модель AI для использования (по умолчанию `'openai'`).

**Возвращает**:
- `None`

**Как работает функция**:
- Определяет базовый путь к файлам кампании.
- Загружает данные кампании из JSON-файла, если он существует.
- Если файл не найден, запускает процесс создания новой кампании (`process_new_campaign`).
- Устанавливает язык и валюту кампании.
- Инициализирует модели AI (`_models_payload`).

**Примеры**:
```python
campaign = AliPromoCampaign(campaign_name="SummerSale", language="EN", currency="USD")
print(campaign.campaign_name)
```

### `_models_payload`

```python
def _models_payload(self) -> None:
    """ """
    ...
```

**Назначение**: Настраивает модели AI (Gemini и OpenAI) для использования в кампании.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `None`

**Как работает функция**:
- Определяет путь к файлу с системными инструкциями для AI.
- Загружает системные инструкции из файла.
- Инициализирует объекты `GoogleGenerativeAi` (Gemini) и `OpenAIModel` (OpenAI) с загруженными инструкциями.

**Примеры**:
```python
campaign._models_payload()
```

### `process_campaign`

```python
def process_campaign(self) -> None:
    """Функция итерируется по категориям рекламной кампании и обрабатывает товары категории через генератор партнерских ссылок.

    Example:
        >>> campaign.process_campaign()
    """
    ...
```

**Назначение**: Итерируется по категориям рекламной кампании и обрабатывает товары в каждой категории.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `None`

**Как работает функция**:
- Получает список названий категорий из директории `category` в базовом пути кампании.
- Для каждой категории вызывает `process_category_products` для обработки товаров.
- Вызывает `process_llm_category` для обработки AI-данных.

**Примеры**:
```python
campaign.process_campaign()
```

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
    ...
```

**Назначение**: Обрабатывает определенную категорию в кампании для всех языков и валют.

**Параметры**:
- `category_name` (str): Название категории для обработки.

**Возвращает**:
- `list[SimpleNamespace] | None`: Список заголовков товаров в категории.

**Как работает функция**:
- Вызывает `process_category_products` для обработки товаров в категории.
- Вызывает `process_llm_category` для обработки AI-данных категории.

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
) -> None:
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
    │ - Call `self.process_llm_category`             │
    └───────────────────────────────────────────────┘
                     │
                     ▼
    ┌──────────────────────────────────────────────┐
    │ End                                          │
    └──────────────────────────────────────────────┘

    """
    ...
```

**Назначение**: Создает новую рекламную кампанию.

**Параметры**:
- `campaign_name` (str): Название рекламной кампании.
- `language` (Optional[str]): Язык кампании (по умолчанию `None`).
- `currency` (Optional[str]): Валюта кампании (по умолчанию `None`).

**Возвращает**:
- `None`

**Как работает функция**:
- Определяет локали кампании на основе предоставленных языка и валюты.
- Для каждой локали:
  - Устанавливает язык и валюту кампании.
  - Инициализирует объект `SimpleNamespace` для представления данных кампании.
  - Вызывает `set_categories_from_directories` для установки категорий кампании.
  - Копирует данные кампании в `campaign_ai`.
  - Для каждой категории вызывает `process_category_products` и `process_llm_category`.
  - Сохраняет данные кампании в JSON-файл.

**Примеры**:
```python
campaign.process_new_campaign(campaign_name="HolidaySale", language="RU", currency="ILS")
```

### `process_llm_category`

```python
def process_llm_category(self, category_name: Optional[str] = None) -> None:
    """Processes the AI campaign for a specified category or all categories.

        This method processes AI-generated data for the specified category in the campaign.
        If no category name is provided, it processes all categories.

        Args:
            category_name (Optional[str]): The name of the category to process. If not provided, all categories are processed.

        Example:
            >>> campaign.process_llm_category("Electronics")
            >>> campaign.process_llm_category()

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
    ...
```

**Назначение**: Обрабатывает AI-данные для указанной категории или для всех категорий кампании.

**Параметры**:
- `category_name` (Optional[str]): Название категории для обработки (по умолчанию `None`, что означает обработку всех категорий).

**Возвращает**:
- `None`

**Как работает функция**:
- Функция `_process_category` извлекает заголовки товаров для указанной категории, формирует запрос для AI-модели (Gemini или OpenAI) и обновляет данные кампании AI на основе ответа модели.
- Если указано имя категории, обрабатывается только эта категория. В противном случае обрабатываются все категории кампании.
- Результаты сохраняются в JSON-файл.

**Внутренние функции**:
- `_process_category(category_name: str)`: обрабатывает AI-сгенерированные данные для категории и обновляет категорию кампании.
  - Читает заголовки товаров из файла `product_titles.txt`.
  - Формирует запрос для AI-модели.
  - Получает ответ от AI-модели.
  - Преобразует ответ в объект `SimpleNamespace`.
  - Обновляет или создает категорию в `campaign_ai.category` с использованием полученных данных.

  - `get_response(_attempts: int = 5)`: получает ответ от AI модели
  - Вызывает AI модель, возвращает ответ.

**Примеры**:
```python
campaign.process_llm_category(category_name="Electronics")
campaign.process_llm_category()
```

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
                The function attempts to read product IDs from both HTML files and text files within the specified category\'s
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
    ...
```

**Назначение**: Обрабатывает товары в указанной категории.

**Параметры**:
- `category_name` (str): Название категории для обработки.

**Возвращает**:
- `Optional[List[SimpleNamespace]]`: Список объектов `SimpleNamespace`, представляющих товары. Возвращает `None`, если товары не найдены.

**Как работает функция**:
- Функция `read_sources` извлекает идентификаторы товаров из HTML-файлов и файла `sources.txt` в директории категории.
- Если идентификаторы товаров не найдены, возвращается `None`.
- Инициализируется `AliAffiliatedProducts` для генерации партнерских ссылок.
- Вызывается `process_affiliate_products` для обработки товаров и получения данных о партнерских продуктах.
- Если партнерские продукты не найдены, возвращается `None`.

**Внутренние функции**:
- `read_sources(category_name: str)`: Читает источники продуктов и извлекает идентификаторы продуктов.
  - Ищет product ID в HTML-файлах и файле `sources.txt`.
  - Возвращает список product ID, если они найдены, иначе `None`.

**Примеры**:
```python
products: List[SimpleNamespace] = campaign.process_category_products("Electronics")
print(len(products))
for product in products:
    pprint(product)  # Use pprint from `src.utils.pprint`
```

### `dump_category_products_files`

```python
def dump_category_products_files(
    self, category_name: str, products: List[SimpleNamespace]
) -> None:
    """Сохранение данных о товарах в JSON файлы.

    Args:
        category_name (str): Имя категории.
        products (List[SimpleNamespace]): Список объектов SimpleNamespace, представляющих товары.

    Example:
        >>> campaign.dump_category_products_files("Electronics", products)
    """
    ...
```

**Назначение**: Сохраняет данные о товарах в JSON-файлы.

**Параметры**:
- `category_name` (str): Имя категории.
- `products` (List[SimpleNamespace]): Список объектов `SimpleNamespace`, представляющих товары.

**Возвращает**:
- `None`

**Как работает функция**:
- Проверяет, есть ли товары для сохранения.
- Для каждого товара генерирует JSON-файл с данными товара в директории категории.
- Если у товара нет идентификатора, он пропускается.

**Примеры**:
```python
campaign.dump_category_products_files("Electronics", products)
```

### `set_categories_from_directories`

```python
def set_categories_from_directories(self) -> None:
    """Устанавливает категории рекламной кампании из названий директорий в `category`.

    Преобразует каждый элемент списка категорий в объект `SimpleNamespace` с атрибутами
    `category_name`, `title`, и `description`.

    Example:
        >>> self.set_categories_from_directories()
        >>> print(self.campaign.category.category1.category_name)
    """
    ...
```

**Назначение**: Устанавливает категории рекламной кампании на основе названий директорий в директории `category`.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `None`

**Как работает функция**:
- Получает список названий директорий в директории `category`.
- Для каждой директории создает объект `SimpleNamespace` с атрибутами `category_name`, `title` и `description` и добавляет его в `self.campaign.category`.

**Примеры**:
```python
self.set_categories_from_directories()
print(self.campaign.category.category1.category_name)
```

### `generate_output`

```python
async def generate_output(self, campaign_name: str, category_path: str | Path, products_list: list[SimpleNamespace] | SimpleNamespace) -> None:
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
    ...
```

**Назначение**: Сохраняет данные о товарах в различных форматах: JSON-файлы для каждого товара, общий JSON-файл, текстовый файл со ссылками на товары и файл с заголовками товаров.

**Параметры**:
- `campaign_name` (str): Имя кампании.
- `category_path` (str | Path): Путь к директории категории.
- `products_list` (list[SimpleNamespace] | SimpleNamespace): Список товаров или один товар для сохранения.

**Возвращает**:
- `None`

**Как работает функция**:
- Преобразует `products_list` в список, если это не список.
- Создает пустые списки `_data_for_openai`, `_promotion_links_list` и `_product_titles`.
- Для каждого товара в `products_list`:
  - Создает словарь `categories_convertor` и добавляет его к товару.
  - Сохраняет данные товара в JSON-файл (`<product_id>.json`).
  - Добавляет заголовок товара и ссылку на продвижение в соответствующие списки.
- Вызывает функции `save_product_titles`, `save_promotion_links` и `generate_html`.

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
async def generate_html(self, campaign_name:str, category_path: str | Path, products_list: list[SimpleNamespace] | SimpleNamespace) -> None:
    """ Creates an HTML file for the category and a root index file.
    
    @param products_list: List of products to include in the HTML.
    @param category_path: Path to save the HTML file.
    """
    ...
```

**Назначение**: Создает HTML-файл для категории и корневой индексный файл.

**Параметры**:
- `campaign_name` (str): Имя кампании.
- `category_path` (str | Path): Путь для сохранения HTML-файла.
- `products_list` (list[SimpleNamespace] | SimpleNamespace): Список продуктов для включения в HTML.

**Возвращает**:
- `None`

**Как работает функция**:
- Преобразует `products_list` в список, если это не список.
- Создает HTML-содержимое для страницы категории на основе списка продуктов.
- Сохраняет HTML-содержимое в файл `<category_name>.html`.
- Генерирует основной индексный файл `index.html` для кампании, содержащий ссылки на все категории.

**Примеры**:
```python
await campaign.generate_html(campaign_name="HolidaySale", category_path="/path/to/category", products_list=products)
```

### `generate_html_for_campaign`

```python
def generate_html_for_campaign(self, campaign_name: str) -> None:
    """Генерирует HTML-страницы для рекламной кампании.

    Args:
        campaign_name (str): Имя рекламной кампании.

    Example:
        >>> campaign.generate_html_for_campaign("HolidaySale")
    """
    ...
```

**Назначение**: Генерирует HTML-страницы для рекламной кампании.

**Параметры**:
- `campaign_name` (str): Имя рекламной кампании.

**Возвращает**:
- `None`

**Как работает функция**:
- Определяет корневую директорию кампании.
- Получает список категорий в кампании.
- Для каждой категории:
  - Получает список товаров.
  - Генерирует HTML-страницу для каждого товара.
  - Генерирует HTML-страницу для категории.
- Генерирует HTML-страницу для всей кампании.

**Примеры**:
```python
campaign.generate_html_for_campaign("HolidaySale")
```

## Параметры класса

- `language` (str): Язык кампании.
- `currency` (str): Валюта кампании.
- `base_path` (Path): Базовый путь к директории кампании.
- `campaign_name` (str): Название кампании.
- `campaign` (SimpleNamespace): Объект, представляющий данные кампании.
- `campaign_ai` (SimpleNamespace): Объект, представляющий AI-данные кампании.
- `gemini` (GoogleGenerativeAi): Объект для взаимодействия с моделью Gemini AI.
- `openai` (OpenAIModel): Объект для взаимодействия с моделью OpenAI.