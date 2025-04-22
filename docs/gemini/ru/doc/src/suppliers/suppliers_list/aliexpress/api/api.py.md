# Модуль для работы с API AliExpress
## Обзор

Модуль `api.py` предоставляет класс `AliexpressApi`, который упрощает взаимодействие с API AliExpress Open Platform. Он позволяет получать информацию о товарах и партнерские ссылки, используя официальный API AliExpress.
Модуль расположен в `src.suppliers.suppliers_list.aliexpress.api`.

## Подробнее

Модуль предназначен для работы с API AliExpress, предоставляя удобные методы для получения информации о товарах, генерации партнерских ссылок и получения категорий товаров. Он использует классы моделей данных из подмодуля `models` и обрабатывает ошибки с помощью исключений из подмодуля `errors`.

## Классы

### `AliexpressApi`

**Описание**: Класс предоставляет методы для получения информации из AliExpress с использованием API ключа и секрета.

**Атрибуты**:
- `_key` (str): API ключ.
- `_secret` (str): API секрет.
- `_tracking_id` (str): ID отслеживания для генерации ссылок.
- `_language` (model_Language): Код языка.
- `_currency` (model_Currency): Код валюты.
- `_app_signature` (str): Подпись приложения.
- `categories` (List[model_Category | model_ChildCategory]): Список категорий.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `AliexpressApi`.
- `retrieve_product_details`: Получает информацию о товарах.
- `get_affiliate_links`: Преобразует список ссылок в партнерские ссылки.
- `get_hotproducts`: Ищет партнерские товары с высокой комиссией.
- `get_categories`: Получает все доступные категории.
- `get_parent_categories`: Получает все родительские категории.
- `get_child_categories`: Получает все дочерние категории для указанной родительской категории.

### `__init__`

```python
def __init__(
    self,
    key: str,
    secret: str,
    language: model_Language,
    currency: model_Currency,
    tracking_id: str = None,
    app_signature: str = None,
    **kwargs,
):
    """Инициализирует экземпляр класса `AliexpressApi`.

    Args:
        key (str): API ключ.
        secret (str): API секрет.
        language (str): Код языка. По умолчанию EN.
        currency (str): Код валюты. По умолчанию USD.
        tracking_id (str): ID отслеживания для генерации ссылок. По умолчанию None.
    """
```

**Параметры**:
- `key` (str): API ключ.
- `secret` (str): API секрет.
- `language` (model_Language): Код языка.
- `currency` (model_Currency): Код валюты.
- `tracking_id` (str, optional): ID отслеживания для генерации ссылок. По умолчанию `None`.
- `app_signature` (str, optional): Подпись приложения. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Как работает функция**:
- Функция выполняет инициализацию экземпляра класса `AliexpressApi`.
- API ключ, API секрет, ID отслеживания, язык и валюта сохраняются в атрибуты экземпляра класса.
- Устанавливает значения по умолчанию для API ключа и секрет, используя функцию `setDefaultAppInfo`.

**Примеры**:

```python
api = AliexpressApi(
    key="your_api_key",
    secret="your_api_secret",
    language=model_Language.RU,
    currency=model_Currency.RUB,
    tracking_id="your_tracking_id",
)
```

### `retrieve_product_details`

```python
def retrieve_product_details(
    self,
    product_ids: str | list,
    fields: str | list = None,
    country: str = None,
    **kwargs,
) -> List[model_Product]:
    """Получает информацию о товарах.

    Args:
        product_ids (str | list[str]): Один или несколько ID товаров или ссылок на товары.
        fields (str | list[str], optional): Список полей, которые нужно включить в результаты. По умолчанию None (включает все поля).
        country (str, optional): Страна, для которой нужно отфильтровать товары. Возвращает цену с учетом налоговой политики страны. По умолчанию None.

    Returns:
        list[model_Product]: Список товаров.

    Raises:
        ProductsNotFoudException: Если товары не найдены.
        InvalidArgumentException: Если переданы неверные аргументы.
        ApiRequestException: Если произошла ошибка при выполнении запроса к API.
        ApiRequestResponseException: Если получен некорректный ответ от API.
    """
```

**Параметры**:
- `product_ids` (str | list[str]): ID товара или список ID товаров.
- `fields` (str | list[str], optional): Список полей для включения в ответ. По умолчанию `None`.
- `country` (str, optional): Страна доставки. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `list[model_Product]`: Список объектов `Product`.

**Вызывает исключения**:
- `ProductsNotFoudException`: Если продукты не найдены.
- `InvalidArgumentException`: Если переданы некорректные аргументы.
- `ApiRequestException`: При ошибке запроса к API.
- `ApiRequestResponseException`: При ошибке ответа от API.

**Как работает функция**:
- Функция выполняет получение информации о товарах по их идентификаторам.
- Преобразует идентификаторы товаров в строку, разделенную запятыми.
- Выполняет запрос к API AliExpress для получения информации о товарах.
- Обрабатывает полученный ответ и возвращает список объектов `Product`.
- В случае отсутствия товаров функция логирует предупреждение и возвращает `None`.

**Примеры**:

```python
api = AliexpressApi(
    key="your_api_key",
    secret="your_api_secret",
    language=model_Language.RU,
    currency=model_Currency.RUB,
    tracking_id="your_tracking_id",
)
product_ids = "10050000000001,10050000000002"
products = api.retrieve_product_details(product_ids=product_ids, fields=["product_title", "product_price"])
if products:
    for product in products:
        print(product.product_title, product.product_price)
```

### `get_affiliate_links`

```python
def get_affiliate_links(
    self,
    links: str | list,
    link_type: model_LinkType = model_LinkType.NORMAL,
    **kwargs,
) -> List[model_AffiliateLink]:
    """Преобразует список ссылок в партнерские ссылки.
    Args:
        links (str | list[str]): Одна или несколько ссылок для преобразования.
        link_type (model_LinkType, optional): Тип ссылки: `NORMAL` (стандартная комиссия) или `HOTLINK` (высокая комиссия). По умолчанию `NORMAL`.

    Returns:
        list[model_AffiliateLink]: Список партнерских ссылок.

    Raises:
        InvalidArgumentException: Если переданы неверные аргументы.
        InvalidTrackingIdException: Если не указан ID отслеживания.
        ProductsNotFoudException: Если товары не найдены.
        ApiRequestException: Если произошла ошибка при выполнении запроса к API.
        ApiRequestResponseException: Если получен некорректный ответ от API.
    """
```

**Параметры**:
- `links` (str | list[str]): Ссылка или список ссылок для преобразования.
- `link_type` (model_LinkType, optional): Тип ссылки (NORMAL или HOTLINK). По умолчанию `model_LinkType.NORMAL`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `list[model_AffiliateLink]`: Список партнерских ссылок.

**Вызывает исключения**:
- `InvalidArgumentException`: Если переданы некорректные аргументы.
- `InvalidTrackingIdException`: Если не указан tracking_id.
- `ProductsNotFoudException`: Если продукты не найдены.
- `ApiRequestException`: При ошибке запроса к API.
- `ApiRequestResponseException`: При ошибке ответа от API.

**Как работает функция**:
- Функция выполняет преобразование обычных ссылок на товары AliExpress в партнерские ссылки, которые позволяют получать комиссионные вознаграждения за покупки, совершенные по этим ссылкам.
- Если `tracking_id` не указан, функция логирует ошибку и возвращает `None`.
- Преобразует входные ссылки в строку, разделенную запятыми.
- Выполняет запрос к API AliExpress для генерации партнерских ссылок.
- Обрабатывает полученный ответ и возвращает список объектов `AffiliateLink`.
- Если партнерские ссылки не доступны, функция логирует предупреждение и возвращает `None`.

**Примеры**:

```python
api = AliexpressApi(
    key="your_api_key",
    secret="your_api_secret",
    language=model_Language.RU,
    currency=model_Currency.RUB,
    tracking_id="your_tracking_id",
)
links = "https://www.aliexpress.com/item/10050000000001.html,https://www.aliexpress.com/item/10050000000002.html"
affiliate_links = api.get_affiliate_links(links=links, link_type=model_LinkType.HOTLINK)
if affiliate_links:
    for link in affiliate_links:
        print(link)
```

### `get_hotproducts`

```python
def get_hotproducts(
    self,
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
    **kwargs,
) -> model_HotProductsResponse:
    """Ищет партнерские товары с высокой комиссией.

    Args:
        category_ids (str | list[str], optional): ID категории или список ID категорий. По умолчанию None.
        delivery_days (int, optional): Количество дней доставки. По умолчанию None.
        fields (str | list[str], optional): Список полей для включения в результаты. По умолчанию None.
        keywords (str, optional): Ключевые слова для поиска товаров. По умолчанию None.
        max_sale_price (int, optional): Максимальная цена товара (в минимальной валютной единице, например, центах). По умолчанию None.
        min_sale_price (int, optional): Минимальная цена товара (в минимальной валютной единице, например, центах). По умолчанию None.
        page_no (int, optional): Номер страницы. По умолчанию None.
        page_size (int, optional): Количество товаров на странице (от 1 до 50). По умолчанию None.
        platform_product_type (model_ProductType, optional): Тип платформы продукта. По умолчанию None.
        ship_to_country (str, optional): Страна доставки. По умолчанию None.
        sort (model_SortBy, optional): Метод сортировки. По умолчанию None.

    Returns:
        model_HotProductsResponse: Объект, содержащий информацию об ответе и список товаров.

    Raises:
        ProductsNotFoudException: Если товары не найдены.
        ApiRequestException: Если произошла ошибка при выполнении запроса к API.
        ApiRequestResponseException: Если получен некорректный ответ от API.
    """
```

**Параметры**:
- `category_ids` (str | list[str], optional): ID категории или список ID категорий. По умолчанию `None`.
- `delivery_days` (int, optional): Количество дней доставки. По умолчанию `None`.
- `fields` (str | list[str], optional): Список полей для включения в результаты. По умолчанию `None`.
- `keywords` (str, optional): Ключевые слова для поиска. По умолчанию `None`.
- `max_sale_price` (int, optional): Максимальная цена товара. По умолчанию `None`.
- `min_sale_price` (int, optional): Минимальная цена товара. По умолчанию `None`.
- `page_no` (int, optional): Номер страницы. По умолчанию `None`.
- `page_size` (int, optional): Размер страницы. По умолчанию `None`.
- `platform_product_type` (model_ProductType, optional): Тип платформы продукта. По умолчанию `None`.
- `ship_to_country` (str, optional): Страна доставки. По умолчанию `None`.
- `sort` (model_SortBy, optional): Метод сортировки. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `model_HotProductsResponse`: Ответ, содержащий список товаров.

**Вызывает исключения**:
- `ProductsNotFoudException`: Если продукты не найдены.
- `ApiRequestException`: При ошибке запроса к API.
- `ApiRequestResponseException`: При ошибке ответа от API.

**Как работает функция**:
- Функция выполняет поиск товаров с высокой комиссией на AliExpress.
- Формирует запрос к API AliExpress с указанными параметрами.
- Обрабатывает полученный ответ и возвращает объект `HotProductsResponse`, содержащий список товаров.

**Примеры**:

```python
api = AliexpressApi(
    key="your_api_key",
    secret="your_api_secret",
    language=model_Language.RU,
    currency=model_Currency.RUB,
    tracking_id="your_tracking_id",
)
hot_products = api.get_hotproducts(category_ids="200003402", keywords="dress", page_size=10)
if hot_products:
    for product in hot_products.products:
        print(product.product_title, product.product_price)
```

### `get_categories`

```python
def get_categories(self, **kwargs) -> List[model_Category | model_ChildCategory]:
    """Получает все доступные категории (родительские и дочерние).

    Returns:
        list[model_Category | model_ChildCategory]: Список категорий.

    Raises:
        CategoriesNotFoudException: Если категории не найдены.
        ApiRequestException: Если произошла ошибка при выполнении запроса к API.
        ApiRequestResponseException: Если получен некорректный ответ от API.
    """
```

**Параметры**:
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `list[model_Category | model_ChildCategory]`: Список категорий.

**Вызывает исключения**:
- `CategoriesNotFoudException`: Если категории не найдены.
- `ApiRequestException`: При ошибке запроса к API.
- `ApiRequestResponseException`: При ошибке ответа от API.

**Как работает функция**:
- Функция выполняет запрос к API AliExpress для получения списка всех доступных категорий товаров.
- Сохраняет полученный список категорий в атрибуте `categories` экземпляра класса.
- Возвращает список категорий.

**Примеры**:

```python
api = AliexpressApi(
    key="your_api_key",
    secret="your_api_secret",
    language=model_Language.RU,
    currency=model_Currency.RUB,
    tracking_id="your_tracking_id",
)
categories = api.get_categories()
if categories:
    for category in categories:
        print(category.category_name, category.category_id)
```

### `get_parent_categories`

```python
def get_parent_categories(self, use_cache=True, **kwargs) -> List[model_Category]:
    """Получает все доступные родительские категории.

    Args:
        use_cache (bool, optional): Использовать кэшированные категории, чтобы избежать повторных запросов к API. По умолчанию True.

    Returns:
        list[model_Category]: Список родительских категорий.

    Raises:
        CategoriesNotFoudException: Если категории не найдены.
        ApiRequestException: Если произошла ошибка при выполнении запроса к API.
        ApiRequestResponseException: Если получен некорректный ответ от API.
    """
```

**Параметры**:
- `use_cache` (bool, optional): Использовать кэш категорий. По умолчанию `True`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `list[model_Category]`: Список родительских категорий.

**Вызывает исключения**:
- `CategoriesNotFoudException`: Если категории не найдены.
- `ApiRequestException`: При ошибке запроса к API.
- `ApiRequestResponseException`: При ошибке ответа от API.

**Как работает функция**:
- Функция выполняет получение списка родительских категорий товаров.
- Если `use_cache` имеет значение `True` и категории уже загружены, функция использует кэшированные категории.
- В противном случае функция вызывает метод `get_categories` для получения списка всех категорий.
- Фильтрует список категорий и возвращает только родительские категории.

**Примеры**:

```python
api = AliexpressApi(
    key="your_api_key",
    secret="your_api_secret",
    language=model_Language.RU,
    currency=model_Currency.RUB,
    tracking_id="your_tracking_id",
)
parent_categories = api.get_parent_categories(use_cache=True)
if parent_categories:
    for category in parent_categories:
        print(category.category_name, category.category_id)
```

### `get_child_categories`

```python
def get_child_categories(self, parent_category_id: int, use_cache=True, **kwargs) -> List[model_ChildCategory]:
    """Получает все доступные дочерние категории для указанной родительской категории.

    Args:
        parent_category_id (int): ID родительской категории.
        use_cache (bool, optional): Использовать кэшированные категории, чтобы избежать повторных запросов к API. По умолчанию True.

    Returns:
        list[model_ChildCategory]: Список дочерних категорий.

    Raises:
        CategoriesNotFoudException: Если категории не найдены.
        ApiRequestException: Если произошла ошибка при выполнении запроса к API.
        ApiRequestResponseException: Если получен некорректный ответ от API.
    """
```

**Параметры**:
- `parent_category_id` (int): ID родительской категории.
- `use_cache` (bool, optional): Использовать кэш категорий. По умолчанию `True`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `list[model_ChildCategory]`: Список дочерних категорий.

**Вызывает исключения**:
- `CategoriesNotFoudException`: Если категории не найдены.
- `ApiRequestException`: При ошибке запроса к API.
- `ApiRequestResponseException`: При ошибке ответа от API.

**Как работает функция**:
- Функция выполняет получение списка дочерних категорий для указанной родительской категории.
- Если `use_cache` имеет значение `True` и категории уже загружены, функция использует кэшированные категории.
- В противном случае функция вызывает метод `get_categories` для получения списка всех категорий.
- Фильтрует список категорий и возвращает только дочерние категории, соответствующие указанной родительской категории.

**Примеры**:

```python
api = AliexpressApi(
    key="your_api_key",
    secret="your_api_secret",
    language=model_Language.RU,
    currency=model_Currency.RUB,
    tracking_id="your_tracking_id",
)
child_categories = api.get_child_categories(parent_category_id=200003402, use_cache=True)
if child_categories:
    for category in child_categories:
        print(category.category_name, category.category_id)