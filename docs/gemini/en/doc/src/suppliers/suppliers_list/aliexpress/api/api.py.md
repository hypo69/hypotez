# AliExpress API Wrapper for Python

## Overview

This module provides a simple Python wrapper for the AliExpress Open Platform API. It simplifies accessing product information and generating affiliate links from AliExpress using the official API. 

## Details

The `AliexpressApi` class is the core component of this module. It allows you to retrieve product details, generate affiliate links, search for hot products, and access category information. 

## Classes

### `AliexpressApi`

**Description**: Provides methods to interact with the AliExpress API.

**Attributes**:

- `_key` (str): Your AliExpress API key.
- `_secret` (str): Your AliExpress API secret.
- `_tracking_id` (str): The tracking ID for affiliate link generation.
- `_language` (model_Language): The language code for API requests.
- `_currency` (model_Currency): The currency code for API requests.
- `_app_signature` (str): The app signature for API requests.
- `categories` (List[model_Category | model_ChildCategory]): A list of all available AliExpress categories.

**Methods**:

- `__init__(self, key: str, secret: str, language: model_Language, currency: model_Currency, tracking_id: str = None, app_signature: str = None, **kwargs)`: Initializes the `AliexpressApi` object with your API credentials and settings.
- `retrieve_product_details(self, product_ids: str | list, fields: str | list = None, country: str = None, **kwargs) -> List[model_Product]`: Retrieves detailed information about one or more AliExpress products.
- `get_affiliate_links(self, links: str | list, link_type: model_LinkType = model_LinkType.NORMAL, **kwargs) -> List[model_AffiliateLink]`: Generates affiliate links for provided product links.
- `get_hotproducts(self, category_ids: str | list = None, delivery_days: int = None, fields: str | list = None, keywords: str = None, max_sale_price: int = None, min_sale_price: int = None, page_no: int = None, page_size: int = None, platform_product_type: model_ProductType = None, ship_to_country: str = None, sort: model_SortBy = None, **kwargs) -> model_HotProductsResponse`: Searches for hot products (products with high commission) based on specified criteria.
- `get_categories(self, **kwargs) -> List[model_Category | model_ChildCategory]`: Retrieves all available AliExpress categories, including parent and child categories.
- `get_parent_categories(self, use_cache=True, **kwargs) -> List[model_Category]`: Retrieves all available parent categories from AliExpress.
- `get_child_categories(self, parent_category_id: int, use_cache=True, **kwargs) -> List[model_ChildCategory]`: Retrieves all available child categories for a specific parent category.


## Functions

### `get_product_ids(product_ids: str | list) -> list`:

**Purpose**:  Преобразует строку или список строк в список идентификаторов продуктов.

**Parameters**:

- `product_ids` (str | list[str]): Один или несколько идентификаторов продуктов или ссылок на продукты.

**Returns**:

- `list`: Список идентификаторов продуктов.

**How the Function Works**:
 -  Функция  проверяет, является ли `product_ids` строкой или списком.
 -  Если это строка, функция разделяет ее по запятой и преобразует в список.
 -  Если это список, функция просто возвращает этот список.
 -  Функция  удаляет пробелы из полученных элементов списка.

**Examples**:

- `get_product_ids('1234567890, 9876543210')` returns `['1234567890', '9876543210']`.
- `get_product_ids(['1234567890', '9876543210'])` returns `['1234567890', '9876543210']`.


### `get_list_as_string(values: str | list, separator: str = ',') -> str`:

**Purpose**: Преобразует строку или список в строку, разделенную указанным разделителем.

**Parameters**:

- `values` (str | list): Строка или список значений.
- `separator` (str): Разделитель для строки. По умолчанию `',`.

**Returns**:

- `str`: Строка, разделенная указанным разделителем.

**How the Function Works**:
 -  Функция  проверяет, является ли `values` строкой или списком.
 -  Если это строка, функция просто возвращает эту строку.
 -  Если это список, функция объединяет все элементы списка в строку с использованием указанного разделителя.

**Examples**:

- `get_list_as_string('1234567890')` returns `'1234567890'`.
- `get_list_as_string(['1234567890', '9876543210'])` returns `'1234567890,9876543210'`.


### `parse_products(products: list) -> List[model_Product]`:

**Purpose**:  Преобразует список сырых данных продуктов в список объектов `model_Product`.

**Parameters**:

- `products` (list): Список сырых данных продуктов.

**Returns**:

- `List[model_Product]`: Список объектов `model_Product`, которые представляют продукты.

**How the Function Works**:
 -  Функция  итерирует по списку сырых данных продуктов.
 -  Для каждого элемента списка  функция  создает новый объект `model_Product`.
 -  Функция  заполняет  атрибуты  объекта `model_Product` данными из сырых данных продуктов.
 -  Функция  возвращает  список  созданных  объектов `model_Product`.

**Examples**:

- `parse_products([{'product_id': '1234567890', 'name': 'Product Name'}, {'product_id': '9876543210', 'name': 'Another Product'}])` returns `[model_Product(product_id='1234567890', name='Product Name'), model_Product(product_id='9876543210', name='Another Product')]`.


### `api_request(request: object, response_name: str) -> object`:

**Purpose**:  Выполняет API-запрос к AliExpress.

**Parameters**:

- `request` (object): Объект API-запроса.
- `response_name` (str): Имя ожидаемого ответа.

**Returns**:

- `object`: Объект ответа API.

**How the Function Works**:
 -  Функция  выполняет API-запрос к AliExpress, используя указанный объект запроса.
 -  Функция  обрабатывает  ответ  API  и  возвращает  его  в  виде  объекта.

**Examples**:

- `api_request(aliexpress_affiliate_category_get_request(), 'aliexpress_affiliate_category_get_response')` returns the response object for the category retrieval API request.


## Parameter Details

- **`product_ids`**:  Идентификаторы продуктов, которые нужно получить. Можно передать как строку с разделенными запятой идентификаторами, так и список идентификаторов. 
- **`fields`**:  Список полей, которые нужно получить.
- **`country`**:  Страна, для которой нужно получить информацию о цене. Используется для получения цены с учетом налогов в данной стране.
- **`link_type`**:  Тип сгенерированной ссылки.  
- **`category_ids`**:  Идентификаторы категорий для поиска горячих продуктов.
- **`delivery_days`**:  Предполагаемое количество дней доставки.
- **`keywords`**:  Ключевые слова для поиска горячих продуктов.
- **`max_sale_price`**:  Максимальная цена поиска горячих продуктов.
- **`min_sale_price`**:  Минимальная цена поиска горячих продуктов.
- **`page_no`**:  Номер страницы для пагинации.
- **`page_size`**:  Количество продуктов на странице.
- **`platform_product_type`**:  Тип продукта.
- **`ship_to_country`**:  Страна, для которой нужно получить информацию о цене.
- **`sort`**:  Сортировка поиска.
- **`use_cache`**:  Флаг, указывающий, использовать ли кэшированные категории. 

## Examples

### Retrieve Product Details

```python
from src.suppliers.aliexpress.api.api import AliexpressApi
from src.suppliers.aliexpress.api.models import Language, Currency

api = AliexpressApi(
    key="your_api_key",
    secret="your_api_secret",
    language=Language.EN,
    currency=Currency.USD
)

product_ids = '1234567890, 9876543210'  # Example product IDs
products = api.retrieve_product_details(product_ids)

for product in products:
    print(f"Product ID: {product.product_id}")
    print(f"Product Name: {product.product_name}")
    print(f"Price: {product.sale_price}")
```

### Generate Affiliate Links

```python
from src.suppliers.aliexpress.api.api import AliexpressApi
from src.suppliers.aliexpress.api.models import Language, Currency, LinkType

api = AliexpressApi(
    key="your_api_key",
    secret="your_api_secret",
    language=Language.EN,
    currency=Currency.USD,
    tracking_id="your_tracking_id"
)

links = ['https://www.aliexpress.com/item/1234567890.html', 'https://www.aliexpress.com/item/9876543210.html']
affiliate_links = api.get_affiliate_links(links, link_type=LinkType.NORMAL)

for link in affiliate_links:
    print(f"Affiliate Link: {link.promotion_link}")
```

### Search for Hot Products

```python
from src.suppliers.aliexpress.api.api import AliexpressApi
from src.suppliers.aliexpress.api.models import Language, Currency, SortBy, ProductType

api = AliexpressApi(
    key="your_api_key",
    secret="your_api_secret",
    language=Language.EN,
    currency=Currency.USD,
    tracking_id="your_tracking_id"
)

hot_products = api.get_hotproducts(
    category_ids='1234567890',
    keywords='phone case',
    ship_to_country='US',
    sort=SortBy.SALES,
    page_size=20
)

for product in hot_products.products:
    print(f"Product ID: {product.product_id}")
    print(f"Product Name: {product.product_name}")
    print(f"Price: {product.sale_price}")
    print(f"Commission Rate: {product.commission_rate}")
```

### Get Categories

```python
from src.suppliers.aliexpress.api.api import AliexpressApi
from src.suppliers.aliexpress.api.models import Language, Currency

api = AliexpressApi(
    key="your_api_key",
    secret="your_api_secret",
    language=Language.EN,
    currency=Currency.USD,
    tracking_id="your_tracking_id"
)

categories = api.get_categories()

for category in categories:
    print(f"Category ID: {category.category_id}")
    print(f"Category Name: {category.category_name}")
```

### Get Parent Categories

```python
from src.suppliers.aliexpress.api.api import AliexpressApi
from src.suppliers.aliexpress.api.models import Language, Currency

api = AliexpressApi(
    key="your_api_key",
    secret="your_api_secret",
    language=Language.EN,
    currency=Currency.USD,
    tracking_id="your_tracking_id"
)

parent_categories = api.get_parent_categories()

for category in parent_categories:
    print(f"Category ID: {category.category_id}")
    print(f"Category Name: {category.category_name}")
```

### Get Child Categories

```python
from src.suppliers.aliexpress.api.api import AliexpressApi
from src.suppliers.aliexpress.api.models import Language, Currency

api = AliexpressApi(
    key="your_api_key",
    secret="your_api_secret",
    language=Language.EN,
    currency=Currency.USD,
    tracking_id="your_tracking_id"
)

child_categories = api.get_child_categories(parent_category_id=1234567890)

for category in child_categories:
    print(f"Category ID: {category.category_id}")
    print(f"Category Name: {category.category_name}")
```