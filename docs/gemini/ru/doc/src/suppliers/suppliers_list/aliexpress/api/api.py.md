# Модуль для работы с API AliExpress
## Обзор
Модуль предоставляет класс `AliexpressApi`, который используется для взаимодействия с API AliExpress.
Он позволяет получать информацию о товарах, генерировать партнерские ссылки и получать список категорий.

## Подробнее

Модуль предназначен для упрощения работы с API AliExpress. Он инкапсулирует логику запросов к API,
обработки ответов и возвращает данные в удобном для использования формате.

## Классы

### `AliexpressApi`

**Описание**: Предоставляет методы для получения информации с AliExpress с использованием API.

**Атрибуты**:
- `_key` (str): API ключ.
- `_secret` (str): API секрет.
- `_tracking_id` (str | None): ID отслеживания для генерации ссылок.
- `_language` (model_Language): Язык.
- `_currency` (model_Currency): Валюта.
- `_app_signature` (str | None): Подпись приложения.
- `categories` (List[model_Category | model_ChildCategory] | None): Список категорий.

**Методы**:
- `__init__`: Конструктор класса.
- `retrieve_product_details`: Получает информацию о товарах.
- `get_affiliate_links`: Генерирует партнерские ссылки.
- `get_hotproducts`: Поиск партнерских товаров с высокой комиссией.
- `get_categories`: Получает все доступные категории.
- `get_parent_categories`: Получает все родительские категории.
- `get_child_categories`: Получает все дочерние категории для указанной родительской категории.

### `__init__`

```python
def __init__(self,
        key: str,
        secret: str,
        language: model_Language,
        currency: model_Currency,
        tracking_id: str = None,
        app_signature: str = None,
        **kwargs):
    """
    Args:
        key (str): Your API key.
        secret (str): Your API secret.
        language (str): Language code. Defaults to EN.
        currency (str): Currency code. Defaults to USD.
        tracking_id (str): The tracking id for link generator. Defaults to None.
    """
```
**Назначение**: Инициализирует экземпляр класса `AliexpressApi`.

**Параметры**:
- `key` (str): API ключ.
- `secret` (str): API секрет.
- `language` (model_Language): Язык.
- `currency` (model_Currency): Валюта.
- `tracking_id` (str, optional): ID отслеживания для генерации ссылок. По умолчанию `None`.
- `app_signature` (str, optional): Подпись приложения. По умолчанию `None`.

**Как работает функция**:
- Функция сохраняет переданные параметры в атрибуты экземпляра класса.
- Устанавливает значения API ключа и секрета по умолчанию с помощью `setDefaultAppInfo`.

**Примеры**:
```python
api = AliexpressApi(
    key='your_api_key',
    secret='your_api_secret',
    language=model_Language.RU,
    currency=model_Currency.RUB,
    tracking_id='your_tracking_id'
)
```

### `retrieve_product_details`

```python
def retrieve_product_details(self,
        product_ids: str | list,
        fields: str | list = None,
        country: str = None,
        **kwargs) -> List[model_Product]:
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
```

**Назначение**: Получает информацию о товарах по их ID.

**Параметры**:
- `product_ids` (str | list): ID товаров.
- `fields` (str | list, optional): Список полей, которые необходимо включить в результаты. По умолчанию `None` (все поля).
- `country` (str, optional): Страна, для которой необходимо отфильтровать товары. По умолчанию `None`.

**Возвращает**:
- `List[model_Product]`: Список объектов `Product`.

**Вызывает исключения**:
- `ProductsNotFoudException`: Если товары не найдены.

**Как работает функция**:
- Функция принимает ID товаров в виде строки или списка.
- Преобразует ID товаров в строку, разделенную запятыми.
- Выполняет запрос к API AliExpress для получения информации о товарах.
- Обрабатывает ответ API и возвращает список объектов `Product`.
- В случае ошибки логирует ее и возвращает `None`.

**Примеры**:
```python
product_ids = '1234567890,0987654321'
products = api.retrieve_product_details(product_ids=product_ids)
if products:
    for product in products:
        print(product.title)
```

### `get_affiliate_links`

```python
def get_affiliate_links(self,
        links: str | list,
        link_type: model_LinkType = model_LinkType.NORMAL,
        **kwargs) -> List[model_AffiliateLink]:
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
```

**Назначение**: Преобразует список ссылок в партнерские ссылки.

**Параметры**:
- `links` (str | list): Список ссылок для преобразования.
- `link_type` (model_LinkType, optional): Тип ссылки (NORMAL или HOTLINK). По умолчанию `model_LinkType.NORMAL`.

**Возвращает**:
- `List[model_AffiliateLink]`: Список партнерских ссылок.

**Вызывает исключения**:
- `InvalidTrackingIdException`: Если не указан tracking_id.

**Как работает функция**:
- Проверяет, указан ли `tracking_id`. Если нет, то функция логирует ошибку и возвращает `None`.
- Преобразует список ссылок в строку, разделенную запятыми.
- Выполняет запрос к API AliExpress для генерации партнерских ссылок.
- Обрабатывает ответ API и возвращает список объектов `AffiliateLink`.

**Примеры**:
```python
links = 'https://www.aliexpress.com/item/1234567890.html'
affiliate_links = api.get_affiliate_links(links=links, link_type=model_LinkType.HOTLINK)
if affiliate_links:
    for link in affiliate_links:
        print(link)
```

### `get_hotproducts`

```python
def get_hotproducts(self,
        category_ids: str | list = None,
        delivery_days: int = None,
		fields: str | list = None,
		keywords: str = None,
		max_sale_price: int = None,
		min_sale_price: int = None,
		page_no: int = None,
		page_size: int = None,
		platform_product_type: model_ProductType = None,
		ship_to_country: str = None,
		sort: model_SortBy = None,
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
```

**Назначение**: Поиск партнерских товаров с высокой комиссией.

**Параметры**:
- `category_ids` (str | list, optional): Список ID категорий. По умолчанию `None`.
- `delivery_days` (int, optional): Количество дней доставки. По умолчанию `None`.
- `fields` (str | list, optional): Список полей для включения в результаты. По умолчанию `None` (все поля).
- `keywords` (str, optional): Ключевые слова для поиска товаров. По умолчанию `None`.
- `max_sale_price` (int, optional): Максимальная цена товара. По умолчанию `None`.
- `min_sale_price` (int, optional): Минимальная цена товара. По умолчанию `None`.
- `page_no` (int, optional): Номер страницы. По умолчанию `None`.
- `page_size` (int, optional): Количество товаров на странице. По умолчанию `None`.
- `platform_product_type` (model_ProductType, optional): Тип платформы товара. По умолчанию `None`.
- `ship_to_country` (str, optional): Страна доставки. По умолчанию `None`.
- `sort` (model_SortBy, optional): Метод сортировки. По умолчанию `None`.

**Возвращает**:
- `model_HotProductsResponse`: Объект, содержащий информацию об ответе и список товаров.

**Вызывает исключения**:
- `ProductsNotFoudException`: Если товары не найдены.

**Как работает функция**:
- Функция принимает различные параметры для фильтрации и сортировки товаров.
- Выполняет запрос к API AliExpress для поиска товаров с высокой комиссией.
- Обрабатывает ответ API и возвращает объект `HotProductsResponse`.

**Примеры**:
```python
hot_products = api.get_hotproducts(
    category_ids='123',
    keywords='phone',
    page_size=20,
    sort=model_SortBy.COMMISSION_RATE_DESC
)
if hot_products:
    for product in hot_products.products:
        print(product.title)
```

### `get_categories`

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
```

**Назначение**: Получает список всех доступных категорий (родительских и дочерних).

**Возвращает**:
- `List[model_Category | model_ChildCategory]`: Список объектов `Category` и `ChildCategory`.

**Вызывает исключения**:
- `CategoriesNotFoudException`: Если категории не найдены.

**Как работает функция**:
- Выполняет запрос к API AliExpress для получения списка категорий.
- Обрабатывает ответ API и возвращает список объектов `Category` и `ChildCategory`.

**Примеры**:
```python
categories = api.get_categories()
if categories:
    for category in categories:
        print(category.name)
```

### `get_parent_categories`

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
```

**Назначение**: Получает список всех родительских категорий.

**Параметры**:
- `use_cache` (bool, optional): Использовать кэшированные категории. По умолчанию `True`.

**Возвращает**:
- `List[model_Category]`: Список объектов `Category`.

**Как работает функция**:
- Если `use_cache` равен `True` и категории уже были загружены, то функция возвращает отфильтрованный список родительских категорий из кэша.
- Если `use_cache` равен `False` или категории еще не были загружены, то функция вызывает метод `get_categories` для загрузки всех категорий, а затем возвращает отфильтрованный список родительских категорий.

**Примеры**:
```python
parent_categories = api.get_parent_categories()
if parent_categories:
    for category in parent_categories:
        print(category.name)
```

### `get_child_categories`

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
```

**Назначение**: Получает список дочерних категорий для указанной родительской категории.

**Параметры**:
- `parent_category_id` (int): ID родительской категории.
- `use_cache` (bool, optional): Использовать кэшированные категории. По умолчанию `True`.

**Возвращает**:
- `List[model_ChildCategory]`: Список объектов `ChildCategory`.

**Как работает функция**:
- Если `use_cache` равен `True` и категории уже были загружены, то функция возвращает отфильтрованный список дочерних категорий из кэша.
- Если `use_cache` равен `False` или категории еще не были загружены, то функция вызывает метод `get_categories` для загрузки всех категорий, а затем возвращает отфильтрованный список дочерних категорий для указанной родительской категории.

**Примеры**:
```python
child_categories = api.get_child_categories(parent_category_id=123)
if child_categories:
    for category in child_categories:
        print(category.name)
```