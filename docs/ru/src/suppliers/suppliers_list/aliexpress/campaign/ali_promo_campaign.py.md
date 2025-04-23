# Модуль: src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign

## Обзор

Модуль `ali_promo_campaign.py` предназначен для управления рекламными кампаниями на платформе AliExpress. Он включает в себя функциональность для обработки данных о категориях и товарах, создания и редактирования JSON-файлов с информацией о кампаниях, а также использование AI для генерации данных о кампаниях.

## Подробнее

Класс `AliPromoCampaign` позволяет загружать и обрабатывать данные рекламных кампаний, управлять категориями и товарами, а также использовать ИИ для генерации описаний и других данных. Модуль поддерживает различные языки и валюты, обеспечивая гибкость в настройке кампаний.
Он использует классы из `src.llm.gemini` и `src.llm.openai` для взаимодействия с AI-моделями, а также утилиты из `src.utils.file` и `src.utils.jjson` для работы с файлами и JSON-данными.

## Классы

### `AliPromoCampaign`

**Описание**: Управляет рекламной кампанией на AliExpress.

**Атрибуты**:
- `language` (str): Язык кампании.
- `currency` (str): Валюта кампании.
- `base_path` (Path): Базовый путь к файлам кампании.
- `campaign_name` (str): Название кампании.
- `campaign` (SimpleNamespace): Объект, представляющий данные кампании.
- `campaign_ai` (SimpleNamespace): Объект, представляющий данные кампании, сгенерированные ИИ.
- `gemini` (GoogleGenerativeAi): Объект для взаимодействия с моделью Gemini.
- `openai` (OpenAIModel): Объект для взаимодействия с моделью OpenAI.

**Методы**:
- `__init__`: Инициализирует объект `AliPromoCampaign`.
- `_models_payload`: Загружает параметры моделей ИИ.
- `process_campaign`: Итерируется по категориям и обрабатывает товары с использованием AI.
- `process_campaign_category`: Обрабатывает определенную категорию кампании для всех языков и валют.
- `process_new_campaign`: Создает новую рекламную кампанию.
- `process_llm_category`: Обрабатывает AI данные для указанной категории.
- `process_category_products`: Обрабатывает товары в указанной категории.
- `dump_category_products_files`: Сохраняет данные о товарах в JSON-файлы.
- `set_categories_from_directories`: Устанавливает категории из названий директорий.
- `generate_output`: Сохраняет данные о товарах в различных форматах (JSON, TXT, HTML).
- `generate_html`: Создает HTML-файл для категории и индексный файл для кампании.
- `generate_html_for_campaign`: Генерирует HTML-страницы для рекламной кампании.

## Методы класса

### `__init__`

```python
def __init__(
    self,
    campaign_name: str,
    language: Optional[str] = None,
    currency: Optional[str] = None,
    model: str = 'openai'
) -> None:
    """Инициализация объекта AliPromoCampaign для рекламной кампании.

    Args:
        campaign_name (str): Название кампании.
        language (Optional[str]): Язык, используемый в кампании.
        currency (Optional[str]): Валюта, используемая в кампании.
        model (str): Модель, используемая для генерации данных (по умолчанию 'openai').

    Returns:
        None

    Example:
        >>> campaign = AliPromoCampaign(campaign_name="SummerSale", language="EN", currency="USD")
        >>> print(campaign.campaign_name)
    """
```
**Назначение**: Инициализирует объект `AliPromoCampaign` с заданными параметрами, такими как название кампании, язык и валюта. Загружает существующую кампанию из JSON-файла, если он существует, или запускает процесс создания новой кампании, если файл не найден.

**Параметры**:
- `campaign_name` (str): Название рекламной кампании.
- `language` (Optional[str]): Язык кампании. По умолчанию `None`.
- `currency` (Optional[str]): Валюта кампании. По умолчанию `None`.
- `model` (str): Модель ИИ для использования. По умолчанию 'openai'.

**Как работает функция**:
- Определяет базовый путь к файлам кампании.
- Пытается загрузить данные кампании из JSON-файла.
- Если файл не найден, запускает процесс создания новой кампании.
- Устанавливает язык и валюту кампании.
- Инициализирует модели ИИ.

**Примеры**:
```python
campaign = AliPromoCampaign(campaign_name="SummerSale", language="EN", currency="USD")
print(campaign.campaign_name)
```

### `_models_payload`

```python
def _models_payload(self) -> None:
    """Загружает параметры моделей ИИ."""
```
**Назначение**: Загружает системные инструкции для моделей ИИ (Google Gemini и OpenAI) из текстового файла и инициализирует соответствующие объекты моделей.

**Параметры**:
- Отсутствуют.

**Как работает функция**:
- Определяет путь к файлу с системными инструкциями.
- Читает содержимое файла.
- Инициализирует объекты `GoogleGenerativeAi` и `OpenAIModel` с использованием прочитанных инструкций и идентификаторов ассистентов.

**Примеры**:
```python
campaign._models_payload()
```

### `process_campaign`

```python
def process_campaign(self) -> None:
    """Функция итерируется по категориям рекламной кампании и обрабатывает товары категории через генератор партнерских ссылок."""
```

**Назначение**: Итерируется по категориям рекламной кампании и обрабатывает товары каждой категории, генерируя партнерские ссылки и обрабатывая AI-данные.

**Параметры**:
- Отсутствуют.

**Как работает функция**:
- Получает список названий категорий из директории `category` в базовом пути кампании.
- Для каждой категории вызывает методы `process_category_products` и `process_llm_category`.

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
```

**Назначение**: Обрабатывает указанную категорию в кампании для всех языков и валют, вызывая методы для обработки товаров и AI-данных.

**Параметры**:
- `category_name` (str): Название категории для обработки.

**Возвращает**:
- `list[SimpleNamespace] | None`: Список названий товаров в категории.

**Как работает функция**:
- Вызывает методы `process_category_products` и `process_llm_category` для указанной категории.

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
        None

    Example:
        >>> campaign.process_new_campaign(campaign_name="HolidaySale", language="RU", currency="ILS")
    """
```

**Назначение**: Создает новую рекламную кампанию, обрабатывая все локали (языки и валюты) и категории.

**Параметры**:
- `campaign_name` (str): Название рекламной кампании.
- `language` (Optional[str]): Язык кампании. По умолчанию `None`.
- `currency` (Optional[str]): Валюта кампании. По умолчанию `None`.

**Как работает функция**:
- Определяет список локалей для обработки.
- Для каждой локали создает объект `SimpleNamespace` для кампании.
- Вызывает метод `set_categories_from_directories` для установки категорий.
- Копирует данные кампании в объект `campaign_ai`.
- Для каждой категории вызывает методы `process_category_products` и `process_llm_category`.
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
    """
```

**Назначение**: Обрабатывает AI-данные для указанной категории или для всех категорий в кампании.

**Параметры**:
- `category_name` (Optional[str]): Название категории для обработки. Если `None`, обрабатываются все категории.

**Как работает функция**:

- Определяет внутреннюю функцию `_process_category`, которая выполняет следующие действия:
    - Читает названия товаров из файла `product_titles.txt`.
    - Формирует запрос к AI модели.
    - Получает ответ от AI модели.
    - Преобразует ответ в объект `SimpleNamespace`.
    - Обновляет или создает категорию в `campaign_ai` с использованием данных из ответа AI.
- Итерируется по категориям и вызывает `_process_category` для каждой из них.
- Сохраняет обновленные данные кампании в JSON-файл.

Внутренняя функция `_process_category` обрабатывает AI-сгенерированные данные для категории и обновляет информацию о категории в кампании.

```python
def _process_category(category_name: str) -> None:
    """Processes AI-generated category data and updates the campaign category."""
```

- **Назначение**: Обрабатывает AI-сгенерированные данные для указанной категории и обновляет соответствующую информацию в объекте кампании (`campaign_ai`).

- **Параметры**:
    - `category_name` (str): Название категории, для которой требуется обработать AI-данные.

- **Как работает функция**:
    1. **Определение путей и чтение данных**:
        - Формирует путь к файлу `product_titles.txt`, содержащему названия товаров для данной категории.
        - Читает названия товаров из файла, используя функцию `read_text_file` и сохраняет их в список `product_titles`.
    2. **Формирование запроса к AI**:
        - Формирует строку запроса (`prompt`) на основе языка кампании, названия категории и списка названий товаров.
    3. **Инициализация моделей AI**:
        - Проверяет, инициализированы ли модели `gemini` и `openai`. Если нет, вызывает метод `_models_payload` для их инициализации.
    4. **Получение ответа от AI**:
        - Определяет внутреннюю функцию `get_response`, которая отправляет запрос в модель Gemini.
        ```python
        def get_response(_attempts: int = 5) -> str:
            """Gets the response from the AI model."""
        ```
        - Функция `get_response` отправляет запрос в модель Gemini.
    5. **Обработка ответа от AI**:
        - Преобразует полученный от AI ответ в объект `SimpleNamespace`, используя функцию `j_loads_ns`.
    6. **Обновление данных кампании**:
        - Проверяет, существует ли уже категория с указанным именем в объекте `campaign_ai.category`.
        - Если категория существует:
            - Обновляет атрибуты существующей категории данными из ответа AI.
        - Если категория не существует:
            - Создает новую категорию в `campaign_ai.category` и устанавливает её атрибуты на основе данных из ответа AI.
    7. **Обработка исключений**:
        - Если в процессе обработки ответа AI возникает исключение, функция логирует ошибку.

**Примеры**:
```python
campaign.process_llm_category("Electronics")
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
    """
```

**Назначение**: Обрабатывает товары в указанной категории, извлекая идентификаторы товаров из HTML-файлов и текстовых файлов, а затем генерируя партнерские ссылки.

**Параметры**:
- `category_name` (str): Название категории для обработки.

**Возвращает**:
- `Optional[List[SimpleNamespace]]`: Список объектов `SimpleNamespace`, представляющих товары. Возвращает `None`, если товары не найдены.

**Как работает функция**:

- Определяет внутреннюю функцию `read_sources`, которая выполняет следующие действия:
    - Ищет файлы HTML и `sources.txt` в каталоге `sources` указанной категории.
    - Извлекает идентификаторы товаров из HTML-файлов и текстового файла `sources.txt`.
    - Возвращает список идентификаторов товаров.

Внутренняя функция `read_sources` извлекает идентификаторы товаров из HTML-файлов и `sources.txt` в каталоге категории.

```python
def read_sources(category_name: str) -> Optional[List[str]]:
    """Reads product sources and extracts product IDs.

    Args:
        category_name (str): The name of the category.

    Returns:
        Optional[List[str]]: A list of product IDs if found; otherwise, `None`.
    """
```

- **Назначение**: Извлекает идентификаторы товаров из HTML-файлов и файла `sources.txt`, расположенных в директории `sources` указанной категории.

- **Параметры**:
    - `category_name` (str): Название категории, для которой требуется извлечь идентификаторы товаров.

- **Как работает функция**:
    1. **Инициализация**:
        - Создает пустой список `product_ids` для хранения извлеченных идентификаторов товаров.
    2. **Поиск HTML-файлов**:
        - Использует функцию `get_filenames` для поиска HTML-файлов в директории `sources` указанной категории.
    3. **Извлечение идентификаторов из HTML-файлов**:
        - Если HTML-файлы найдены, извлекает идентификаторы товаров из этих файлов, используя функцию `extract_prod_ids`, и добавляет их в список `product_ids`.
    4. **Чтение файла `sources.txt`**:
        - Читает содержимое файла `sources.txt`, расположенного в директории `sources` указанной категории, используя функцию `read_text_file`, и сохраняет URL товаров в список `product_urls`.
    5. **Извлечение идентификаторов из `sources.txt`**:
        - Если файл `sources.txt` прочитан успешно, извлекает идентификаторы товаров из URL товаров, используя функцию `extract_prod_ids`, и добавляет их в список `product_ids`.
    6. **Проверка наличия идентификаторов**:
        - Если список `product_ids` пуст (т.е. не было найдено ни одного идентификатора товара), функция возвращает `None`.
    7. **Возврат результатов**:
        - Если идентификаторы товаров были найдены, функция возвращает список `product_ids`.

- **Пример**:
```python
product_ids: Optional[List[str]] = read_sources("Electronics")
print(product_ids)
```

- Вызывает функцию `read_sources` для получения списка идентификаторов товаров.
- Если идентификаторы товаров не найдены, регистрирует ошибку и возвращает `None`.
- Инициализирует объект `AliAffiliatedProducts` с указанным языком и валютой.
- Вызывает метод `process_affiliate_products` для генерации партнерских ссылок.
- Возвращает список объектов `SimpleNamespace`, представляющих товары с партнерскими ссылками.

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
```

**Назначение**: Сохраняет данные о товарах в JSON-файлы в директории категории.

**Параметры**:
- `category_name` (str): Название категории.
- `products` (List[SimpleNamespace]): Список объектов `SimpleNamespace`, представляющих товары.

**Как работает функция**:
- Проверяет, есть ли товары для сохранения.
- Для каждого товара извлекает `product_id`.
- Сохраняет данные товара в JSON-файл с именем `<product_id>.json` в директории категории.

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
```

**Назначение**: Устанавливает категории рекламной кампании на основе названий директорий, найденных в директории `category`.

**Параметры**:
- Отсутствуют.

**Как работает функция**:
- Получает список названий директорий в директории `category`.
- Для каждой директории создает объект `SimpleNamespace` с атрибутами `category_name`, `title` и `description`.
- Добавляет каждый объект `SimpleNamespace` в качестве атрибута к объекту `self.campaign.category`.

**Примеры**:
```python
campaign.set_categories_from_directories()
print(campaign.category.category1.category_name)
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
    """
```

**Назначение**: Сохраняет данные о товарах в различных форматах, включая JSON-файлы для каждого товара, текстовые файлы со ссылками на товары и HTML-файлы для отображения информации о товарах.

**Параметры**:
- `campaign_name` (str): Название рекламной кампании.
- `category_path` (str | Path): Путь к директории категории.
- `products_list` (list[SimpleNamespace] | SimpleNamespace): Список объектов `SimpleNamespace`, представляющих товары.

**Как работает функция**:
- Форматирует текущую дату и время для использования в именах файлов.
- Преобразует `products_list` в список, если это не список.
- Инициализирует пустые списки для сбора данных.
- Для каждого товара в `products_list`:
    - Создает словарь `categories_convertor` с информацией о категориях товара.
    - Добавляет `categories_convertor` в объект товара.
    - Сохраняет данные товара в JSON-файл.
    - Добавляет название товара и ссылку на товар в соответствующие списки.
- Вызывает методы `save_product_titles`, `save_promotion_links` и `generate_html` для сохранения данных в файлы и генерации HTML-страниц.

Вспомогательные функции:

### `save_product_titles`

```python
async def save_product_titles(self, product_titles: list[str], category_path: str | Path) -> None:
        """
        Saves product titles to a text file.

        Args:
            product_titles (list[str]): List of product titles to save.
            category_path (str | Path): The path to save the output file.
        """
```
-   Сохраняет названия продуктов в текстовый файл.
### `save_promotion_links`

```python
async def save_promotion_links(self, promotion_links: list[str], category_path: str | Path) -> None:
    """
    Saves promotion links to a text file.

    Args:
        promotion_links (list[str]): List of promotion links to save.
        category_path (str | Path): The path to save the output file.
    """
```
-   Сохраняет ссылки на продвижение продуктов в текстовый файл.

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
await campaign.generate_output("CampaignName", category_path, products_list)
```

### `generate_html`

```python
async def generate_html(self, campaign_name:str, category_path: str | Path, products_list: list[SimpleNamespace] | SimpleNamespace) -> None:
    """ Creates an HTML file for the category and a root index file.
    
    @param products_list: List of products to include in the HTML.
    @param category_path: Path to save the HTML file.
    """
```

**Назначение**: Создает HTML-файл для категории и индексный файл для кампании, отображающие информацию о товарах.

**Параметры**:
- `campaign_name` (str): Название рекламной кампании.
- `category_path` (str | Path): Путь к директории категории.
- `products_list` (list[SimpleNamespace] | SimpleNamespace): Список объектов `SimpleNamespace`, представляющих товары.

**Как работает функция**:
- Преобразует `products_list` в список, если это не список.
- Создает HTML-контент для каждого товара в списке, включая изображение, название, цену и ссылку для покупки.
- Сохраняет HTML-контент в файл `<category_name>.html` в директории категории.
- Создает индексный HTML-файл, содержащий ссылки на все категории кампании.
- Сохраняет индексный HTML-файл в корневой директории кампании.

**Примеры**:
```python
await campaign.generate_html(campaign_name="SummerSale", category_path=Path("/path/to/category"), products_list=products)
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
```

**Назначение**: Генерирует HTML-страницы для рекламной кампании, создавая страницы для каждой категории и для каждого товара в категории.

**Параметры**:
- `campaign_name` (str): Название рекламной кампании.

**Как работает функция**:
- Определяет корневую директорию кампании.
- Получает список категорий в кампании.
- Для каждой категории:
    - Получает список товаров в категории.
    - Для каждого товара генерирует HTML-страницу с помощью `ProductHTMLGenerator`.
    - Генерирует HTML-страницу для категории с помощью `CategoryHTMLGenerator`.
- Генерирует HTML-страницу для всей кампании с помощью `CampaignHTMLGenerator`.

**Примеры**:
```python
campaign.generate_html_for_campaign("HolidaySale")
```