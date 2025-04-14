# Модуль для работы с API AliExpress
## Обзор

Модуль предоставляет класс `AliexpressApi`, который используется для взаимодействия с API AliExpress и получения информации о товарах, категориях и партнерских ссылках.

## Подробней

Этот модуль упрощает взаимодействие с API AliExpress, предоставляя удобные методы для получения информации о продуктах, создания партнерских ссылок и получения списка категорий. Он использует API AliExpress для получения данных и возвращает их в виде структурированных объектов.

## Классы

### `AliexpressApi`

**Описание**: Предоставляет методы для получения информации из AliExpress с использованием API-ключей.

**Атрибуты**:
- `_key` (str): API ключ.
- `_secret` (str): API секрет.
- `_tracking_id` (str): ID отслеживания для партнерских ссылок.
- `_language` (str): Код языка. По умолчанию EN.
- `_currency` (str): Код валюты. По умолчанию USD.
- `_app_signature` (str): Подпись приложения.
- `categories` (list): Список категорий.

**Методы**:
- `retrieve_product_details()`: Получает информацию о продуктах.
- `get_affiliate_links()`: Преобразует ссылки в партнерские ссылки.
- `get_hotproducts()`: Ищет партнерские продукты с высокой комиссией.
- `get_categories()`: Получает все доступные категории.
- `get_parent_categories()`: Получает все доступные родительские категории.
- `get_child_categories()`: Получает все доступные дочерние категории для определенной родительской категории.

#### `__init__`

```python
def __init__(self, key: str, secret: str, language: model_Language, currency: model_Currency, tracking_id: str = None, app_signature: str = None, **kwargs):
    """
    Args:
        key (str): Your API key.
        secret (str): Your API secret.
        language (str): Language code. Defaults to EN.
        currency (str): Currency code. Defaults to USD.
        tracking_id (str): The tracking id for link generator. Defaults to None.
    """
    ...
```

**Назначение**: Инициализирует экземпляр класса `AliexpressApi` с предоставленными API-ключом, секретом, языком, валютой и ID отслеживания.

**Параметры**:
- `key` (str): API ключ.
- `secret` (str): API секрет.
- `language` (str): Код языка.
- `currency` (str): Код валюты.
- `tracking_id` (str, optional): ID отслеживания для партнерских ссылок. По умолчанию `None`.
- `app_signature` (str, optional): Подпись приложения.
- `**kwargs`: Дополнительные параметры.

**Как работает**:
- Присваивает значения атрибутам экземпляра класса.
- Устанавливает значения API-ключа и секрета по умолчанию с помощью функции `setDefaultAppInfo`.

**Примеры**:

```python
api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
```

#### `retrieve_product_details`

```python
def retrieve_product_details(self, product_ids: str | list, fields: str | list = None, country: str = None, **kwargs) -> List[model_Product]:
    """ Get products information.

    Args:
        product_ids (``str | list[str]``): One or more links or product IDs.
        fields (``str | list[str]``): The fields to include in the results. Defaults to all.
        country (``str``): Filter products that can be sent to that country. Returns the price
            according to the country's tax rate policy.

    Returns:
        ``list[model_Product]``: A list of products.

    Raises:
        ``ProductsNotFoudException``
        ``InvalidArgumentException``
        ``ApiRequestException``
        ``ApiRequestResponseException``
    """
    ...
```

**Назначение**: Получает информацию о продуктах из AliExpress на основе предоставленных ID продуктов.

**Параметры**:
- `product_ids` (str | list): Один или несколько ID продуктов или ссылок на продукты.
- `fields` (str | list, optional): Список полей, которые необходимо включить в результаты. По умолчанию `None` (включает все поля).
- `country` (str, optional): Страна, в которую может быть отправлен продукт. Возвращает цену с учетом налоговой политики страны. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `list[model_Product]`: Список объектов `Product`, содержащих информацию о продуктах.

**Вызывает исключения**:
- `ProductsNotFoudException`: Если продукты не найдены.
- `InvalidArgumentException`: Если предоставлены неверные аргументы.
- `ApiRequestException`: Если произошла ошибка при выполнении запроса к API.
- `ApiRequestResponseException`: Если получен некорректный ответ от API.

**Как работает**:
1. Преобразует `product_ids` в список ID продуктов с помощью функции `get_product_ids`.
2. Преобразует список ID продуктов в строку с помощью функции `get_list_as_string`.
3. Создает объект запроса `AliexpressAffiliateProductdetailGetRequest`.
4. Устанавливает параметры запроса, такие как `app_signature`, `fields`, `product_ids`, `country`, `target_currency`, `target_language` и `tracking_id`.
5. Выполняет API-запрос с помощью функции `api_request` и получает ответ.
6. Проверяет, есть ли продукты в ответе.
7. Если продукты найдены, разбирает ответ с помощью функции `parse_products` и возвращает список объектов `Product`.
8. Если продукты не найдены, логирует предупреждение с помощью `logger.warning` и возвращает `None`.
9. В случае возникновения исключения, логирует ошибку с помощью `logger.error` и возвращает `None`.

**Примеры**:

```python
api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
product_details = api.retrieve_product_details(product_ids=['1234567890', '0987654321'], fields=['product_title', 'product_price'])
if product_details:
    for product in product_details:
        print(f'Product Title: {product.product_title}, Price: {product.product_price}')
```

#### `get_affiliate_links`

```python
def get_affiliate_links(self, links: str | list, link_type: model_LinkType = model_LinkType.NORMAL, **kwargs) -> List[model_AffiliateLink]:
    """ Converts a list of links in affiliate links.
    Args:
        links (``str | list[str]``): One or more links to convert.
        link_type (``model_LinkType``): Choose between normal link with standard commission
            or hot link with hot product commission. Defaults to NORMAL.
            @code
            link_type: model_LinkType = model_LinkType.HOTLINK
            @endcode

    Returns:
        ``list[model_AffiliateLink]``: A list containing the affiliate links.

    Raises:
        ``InvalidArgumentException``
        ``InvalidTrackingIdException``
        ``ProductsNotFoudException``
        ``ApiRequestException``
        ``ApiRequestResponseException``
    """
    ...
```

**Назначение**: Преобразует список ссылок в партнерские ссылки AliExpress.

**Параметры**:
- `links` (str | list): Одна или несколько ссылок для преобразования.
- `link_type` (model_LinkType, optional): Тип ссылки (NORMAL или HOTLINK). По умолчанию `model_LinkType.NORMAL`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `list[model_AffiliateLink]`: Список объектов `AffiliateLink`, содержащих партнерские ссылки.

**Вызывает исключения**:
- `InvalidArgumentException`: Если предоставлены неверные аргументы.
- `InvalidTrackingIdException`: Если не указан ID отслеживания.
- `ProductsNotFoudException`: Если партнерские ссылки не доступны.
- `ApiRequestException`: Если произошла ошибка при выполнении запроса к API.
- `ApiRequestResponseException`: Если получен некорректный ответ от API.

**Как работает**:
1. Проверяет, указан ли ID отслеживания (`self._tracking_id`). Если ID отслеживания не указан, логирует ошибку с помощью `logger.error` и возвращает `None`.
2. Преобразует список ссылок в строку с помощью функции `get_list_as_string`.
3. Создает объект запроса `AliexpressAffiliateLinkGenerateRequest`.
4. Устанавливает параметры запроса, такие как `app_signature`, `source_values`, `promotion_link_type` и `tracking_id`.
5. Выполняет API-запрос с помощью функции `api_request` и получает ответ.
6. Проверяет, есть ли партнерские ссылки в ответе.
7. Если партнерские ссылки найдены, возвращает список объектов `AffiliateLink`.
8. Если партнерские ссылки не найдены, логирует предупреждение с помощью `logger.warning` и возвращает `None`.

**Примеры**:

```python
api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
affiliate_links = api.get_affiliate_links(links=['https://www.aliexpress.com/item/1234567890.html', 'https://www.aliexpress.com/item/0987654321.html'], link_type=model_LinkType.HOTLINK)
if affiliate_links:
    for link in affiliate_links:
        print(f'Affiliate Link: {link.promotion_url}')
```

#### `get_hotproducts`

```python
def get_hotproducts(self, category_ids: str | list = None, delivery_days: int = None,
                   fields: str | list = None, keywords: str = None,
                   max_sale_price: int = None, min_sale_price: int = None,
                   page_no: int = None, page_size: int = None,
                   platform_product_type: model_ProductType = None,
                   ship_to_country: str = None, sort: model_SortBy = None,
                   **kwargs) -> model_HotProductsResponse:
    """Search for affiliated products with high commission.

    Args:
        category_ids (``str | list[str]``): One or more category IDs.
        delivery_days (``int``): Estimated delivery days.
        fields (``str | list[str]``): The fields to include in the results list. Defaults to all.
        keywords (``str``): Search products based on keywords.
        max_sale_price (``int``): Filters products with price below the specified value.
            Prices appear in lowest currency denomination. So $31.41 should be 3141.
        min_sale_price (``int``): Filters products with price above the specified value.
            Prices appear in lowest currency denomination. So $31.41 should be 3141.
        page_no (``int``):\
        page_size (``int``): Products on each page. Should be between 1 and 50.
        platform_product_type (``model_ProductType``): Specify platform product type.
        ship_to_country (``str``): Filter products that can be sent to that country.
            Returns the price according to the country's tax rate policy.
        sort (``model_SortBy``): Specifies the sort method.

    Returns:
        ``model_HotProductsResponse``: Contains response information and the list of products.

    Raises:
        ``ProductsNotFoudException``
        ``ApiRequestException``
        ``ApiRequestResponseException``
    """
    ...
```

**Назначение**: Ищет партнерские продукты с высокой комиссией на AliExpress.

**Параметры**:
- `category_ids` (str | list, optional): Один или несколько ID категорий. По умолчанию `None`.
- `delivery_days` (int, optional): Предполагаемое количество дней доставки. По умолчанию `None`.
- `fields` (str | list, optional): Список полей, которые необходимо включить в результаты. По умолчанию `None` (включает все поля).
- `keywords` (str, optional): Ключевые слова для поиска продуктов. По умолчанию `None`.
- `max_sale_price` (int, optional): Максимальная цена продукта (в минимальной валютной единице, например, 3141 для $31.41). По умолчанию `None`.
- `min_sale_price` (int, optional): Минимальная цена продукта (в минимальной валютной единице, например, 3141 для $31.41). По умолчанию `None`.
- `page_no` (int, optional): Номер страницы. По умолчанию `None`.
- `page_size` (int, optional): Количество продуктов на странице (от 1 до 50). По умолчанию `None`.
- `platform_product_type` (model_ProductType, optional): Тип продукта платформы. По умолчанию `None`.
- `ship_to_country` (str, optional): Страна, в которую может быть отправлен продукт. По умолчанию `None`.
- `sort` (model_SortBy, optional): Метод сортировки. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `model_HotProductsResponse`: Объект `HotProductsResponse`, содержащий информацию об ответе и список продуктов.

**Вызывает исключения**:
- `ProductsNotFoudException`: Если продукты не найдены.
- `ApiRequestException`: Если произошла ошибка при выполнении запроса к API.
- `ApiRequestResponseException`: Если получен некорректный ответ от API.

**Как работает**:
1. Создает объект запроса `AliexpressAffiliateHotproductQueryRequest`.
2. Устанавливает параметры запроса на основе предоставленных аргументов.
3. Выполняет API-запрос с помощью функции `api_request` и получает ответ.
4. Проверяет, есть ли продукты в ответе.
5. Если продукты найдены, разбирает ответ с помощью функции `parse_products` и возвращает объект `HotProductsResponse`.
6. Если продукты не найдены, вызывает исключение `ProductsNotFoudException`.

**Примеры**:

```python
api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
hot_products = api.get_hotproducts(category_ids=['123', '456'], keywords='shoes', max_sale_price=5000, min_sale_price=1000, page_size=20)
if hot_products and hot_products.products:
    for product in hot_products.products:
        print(f'Product Title: {product.product_title}, Price: {product.product_price}')
```

#### `get_categories`

```python
def get_categories(self, **kwargs) -> List[model_Category | model_ChildCategory]:
    """Get all available categories, both parent and child.

    Returns:
        ``list[model_Category | model_ChildCategory]``: A list of categories.

    Raises:
        ``CategoriesNotFoudException``
        ``ApiRequestException``
        ``ApiRequestResponseException``
    """
    ...
```

**Назначение**: Получает все доступные категории AliExpress (родительские и дочерние).

**Параметры**:
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `list[model_Category | model_ChildCategory]`: Список объектов `Category` и `ChildCategory`, представляющих категории.

**Вызывает исключения**:
- `CategoriesNotFoudException`: Если категории не найдены.
- `ApiRequestException`: Если произошла ошибка при выполнении запроса к API.
- `ApiRequestResponseException`: Если получен некорректный ответ от API.

**Как работает**:
1. Создает объект запроса `AliexpressAffiliateCategoryGetRequest`.
2. Выполняет API-запрос с помощью функции `api_request` и получает ответ.
3. Проверяет, есть ли категории в ответе.
4. Если категории найдены, сохраняет их в атрибуте `self.categories` и возвращает список категорий.
5. Если категории не найдены, вызывает исключение `CategoriesNotFoudException`.

**Примеры**:

```python
api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
categories = api.get_categories()
if categories:
    for category in categories:
        print(f'Category ID: {category.category_id}, Name: {category.category_name}')
```

#### `get_parent_categories`

```python
def get_parent_categories(self, use_cache=True, **kwargs) -> List[model_Category]:
    """Get all available parent categories.

    Args:
        use_cache (``bool``): Uses cached categories to reduce API requests.

    Returns:
        ``list[model_Category]``: A list of parent categories.

    Raises:
        ``CategoriesNotFoudException``
        ``ApiRequestException``
        ``ApiRequestResponseException``
    """
    ...
```

**Назначение**: Получает все доступные родительские категории AliExpress.

**Параметры**:
- `use_cache` (bool, optional): Использовать ли кэшированные категории для уменьшения количества запросов к API. По умолчанию `True`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `list[model_Category]`: Список объектов `Category`, представляющих родительские категории.

**Вызывает исключения**:
- `CategoriesNotFoudException`: Если категории не найдены.
- `ApiRequestException`: Если произошла ошибка при выполнении запроса к API.
- `ApiRequestResponseException`: Если получен некорректный ответ от API.

**Как работает**:
1. Проверяет, следует ли использовать кэшированные категории (`use_cache`) и существуют ли они в атрибуте `self.categories`.
2. Если кэш не используется или категории не кэшированы, вызывает метод `self.get_categories()` для получения категорий из API.
3. Фильтрует родительские категории из списка категорий с помощью функции `filter_parent_categories` и возвращает их.

**Примеры**:

```python
api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
parent_categories = api.get_parent_categories(use_cache=True)
if parent_categories:
    for category in parent_categories:
        print(f'Category ID: {category.category_id}, Name: {category.category_name}')
```

#### `get_child_categories`

```python
def get_child_categories(self, parent_category_id: int, use_cache=True, **kwargs) -> List[model_ChildCategory]:
    """Get all available child categories for a specific parent category.

    Args:
        parent_category_id (``int``): The parent category id.
        use_cache (``bool``): Uses cached categories to reduce API requests.

    Returns:
        ``list[model_ChildCategory]``: A list of child categories.

    Raises:
        ``CategoriesNotFoudException``
        ``ApiRequestException``
        ``ApiRequestResponseException``
    """
    ...
```

**Назначение**: Получает все доступные дочерние категории для указанной родительской категории AliExpress.

**Параметры**:
- `parent_category_id` (int): ID родительской категории.
- `use_cache` (bool, optional): Использовать ли кэшированные категории для уменьшения количества запросов к API. По умолчанию `True`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `list[model_ChildCategory]`: Список объектов `ChildCategory`, представляющих дочерние категории.

**Вызывает исключения**:
- `CategoriesNotFoudException`: Если категории не найдены.
- `ApiRequestException`: Если произошла ошибка при выполнении запроса к API.
- `ApiRequestResponseException`: Если получен некорректный ответ от API.

**Как работает**:
1. Проверяет, следует ли использовать кэшированные категории (`use_cache`) и существуют ли они в атрибуте `self.categories`.
2. Если кэш не используется или категории не кэшированы, вызывает метод `self.get_categories()` для получения категорий из API.
3. Фильтрует дочерние категории из списка категорий с помощью функции `filter_child_categories` и возвращает их.

**Примеры**:

```python
api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
child_categories = api.get_child_categories(parent_category_id=123456, use_cache=True)
if child_categories:
    for category in child_categories:
        print(f'Category ID: {category.category_id}, Name: {category.category_name}')
```