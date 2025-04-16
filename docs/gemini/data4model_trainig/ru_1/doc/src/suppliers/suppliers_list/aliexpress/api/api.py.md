# Модуль для работы с API AliExpress
=================================================

Модуль предоставляет класс `AliexpressApi`, который позволяет получать информацию о товарах и партнерских ссылках с AliExpress, используя официальный API.

## Обзор

Модуль `api.py` является частью проекта `hypotez` и предназначен для упрощения взаимодействия с API AliExpress. Он предоставляет удобный интерфейс для получения информации о товарах, генерации партнерских ссылок и поиска популярных товаров. Модуль включает в себя модели данных, обработку ошибок и вспомогательные функции для работы с API AliExpress.

## Подробнее

Модуль содержит класс `AliexpressApi`, который инициализируется с использованием ключа API, секрета, языка и валюты. Он предоставляет методы для получения информации о продуктах, создания партнерских ссылок и получения списка популярных товаров. Этот модуль использует другие модули в проекте `hypotez` для регистрации, печати и обработки ответов API.

## Классы

### `AliexpressApi`

**Описание**: Предоставляет методы для получения информации с AliExpress с использованием учетных данных API.
**Атрибуты**:
- `_key` (str): Ключ API.
- `_secret` (str): Секрет API.
- `_tracking_id` (str): Идентификатор отслеживания для генерации ссылок.
- `_language` (str): Языковой код.
- `_currency` (str): Код валюты.
- `_app_signature` (str): Подпись приложения.
- `categories` (List[model_Category | model_ChildCategory]): Список категорий.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `AliexpressApi`.
- `retrieve_product_details`: Получает информацию о товарах.
- `get_affiliate_links`: Преобразует список ссылок в партнерские ссылки.
- `get_hotproducts`: Поиск партнерских товаров с высокой комиссией.
- `get_categories`: Получает все доступные категории, как родительские, так и дочерние.
- `get_parent_categories`: Получает все доступные родительские категории.
- `get_child_categories`: Получает все доступные дочерние категории для конкретной родительской категории.

#### `__init__`

```python
def __init__(self, key: str, secret: str, language: model_Language, currency: model_Currency, tracking_id: str = None, app_signature: str = None, **kwargs)
```

**Назначение**: Инициализирует экземпляр класса `AliexpressApi`.

**Параметры**:
- `key` (str): Ваш ключ API.
- `secret` (str): Ваш секрет API.
- `language` (str): Код языка. По умолчанию EN.
- `currency` (str): Код валюты. По умолчанию USD.
- `tracking_id` (str): Идентификатор отслеживания для генератора ссылок. По умолчанию `None`.
- `app_signature` (str): Подпись приложения.

**Как работает функция**:
- Функция инициализирует экземпляр класса `AliexpressApi`, сохраняя переданные параметры (ключ API, секрет, идентификатор отслеживания, язык, валюта и подпись приложения) в атрибуты экземпляра.
- Устанавливает значения по умолчанию для языка и валюты, если они не указаны.
- Вызывает функцию `setDefaultAppInfo` из модуля `skd` для установки ключа и секрета API по умолчанию.
- Инициализирует атрибут `categories` значением `None`.

**Примеры**:

```python
api = AliexpressApi(key='your_api_key', secret='your_api_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
```

#### `retrieve_product_details`

```python
def retrieve_product_details(self, product_ids: str | list, fields: str | list = None, country: str = None, **kwargs) -> List[model_Product]
```

**Назначение**: Получает информацию о товарах.

**Параметры**:
- `product_ids` (str | list): Одна или несколько ссылок или идентификаторов продуктов.
- `fields` (str | list): Поля для включения в результаты. По умолчанию все.
- `country` (str): Фильтр продуктов, которые могут быть отправлены в эту страну. Возвращает цену в соответствии с налоговой политикой страны.

**Возвращает**:
- `list[model_Product]`: Список продуктов.

**Вызывает исключения**:
- `ProductsNotFoudException`: Если продукты не найдены.
- `InvalidArgumentException`: Если передан неверный аргумент.
- `ApiRequestException`: Если произошла ошибка при запросе к API.
- `ApiRequestResponseException`: Если произошла ошибка в ответе API.

**Как работает функция**:
- Функция `retrieve_product_details` извлекает детали продукта(ов) из AliExpress API.
- Сначала она обрабатывает входные `product_ids`, преобразуя их в список, если это строка, и извлекая идентификаторы продуктов из ссылок, если это необходимо.
- Затем она создает запрос к API AliExpress, используя метод `AliexpressAffiliateProductdetailGetRequest()`.
- В запрос добавляются необходимые параметры, такие как идентификаторы продуктов, поля для включения в результаты, страна доставки, валюта и язык.
- После получения ответа от API, функция проверяет, были ли найдены продукты.
- Если продукты найдены, функция вызывает `parse_products()` для преобразования ответа в список объектов `model_Product`.
- Если продукты не найдены, функция регистрирует предупреждение и возвращает `None`.
- В случае возникновения каких-либо исключений в процессе, функция регистрирует ошибку и также возвращает `None`.

**Примеры**:

```python
product_ids = ['1234567890', '0987654321']
products = api.retrieve_product_details(product_ids=product_ids, fields=['product_title', 'product_price'], country='US')
if products:
    for product in products:
        print(product.product_title, product.product_price)
```

#### `get_affiliate_links`

```python
def get_affiliate_links(self, links: str | list, link_type: model_LinkType = model_LinkType.NORMAL, **kwargs) -> List[model_AffiliateLink]
```

**Назначение**: Преобразует список ссылок в партнерские ссылки.

**Параметры**:
- `links` (str | list): Одна или несколько ссылок для преобразования.
- `link_type` (model_LinkType): Выберите между обычной ссылкой со стандартной комиссией или горячей ссылкой с высокой комиссией. По умолчанию `NORMAL`.

**Возвращает**:
- `list[model_AffiliateLink]`: Список, содержащий партнерские ссылки.

**Вызывает исключения**:
- `InvalidArgumentException`: Если передан неверный аргумент.
- `InvalidTrackingIdException`: Если идентификатор отслеживания недействителен.
- `ProductsNotFoudException`: Если продукты не найдены.
- `ApiRequestException`: Если произошла ошибка при запросе к API.
- `ApiRequestResponseException`: Если произошла ошибка в ответе API.

**Как работает функция**:
- Функция `get_affiliate_links` преобразует список обычных ссылок AliExpress в партнерские ссылки, используя API AliExpress.
- Сначала она проверяет, установлен ли идентификатор отслеживания (`tracking_id`). Если он не установлен, функция регистрирует ошибку и возвращает `None`, так как `tracking_id` необходим для создания партнерских ссылок.
- Затем функция преобразует входные ссылки в строковый формат, если они представлены в виде списка.
- После этого создается запрос к API AliExpress с использованием метода `AliexpressAffiliateLinkGenerateRequest()`.
- В запрос добавляются необходимые параметры, такие как ссылки, тип ссылки (обычная или горячая) и идентификатор отслеживания.
- После получения ответа от API, функция проверяет, были ли успешно созданы партнерские ссылки.
- Если ссылки созданы, функция возвращает список партнерских ссылок.
- Если ссылки не созданы, функция регистрирует предупреждение и возвращает `None`.
- В случае возникновения каких-либо исключений в процессе, функция перехватывает их и обрабатывает, регистрируя информацию об ошибке.

**Примеры**:

```python
links = ['https://www.aliexpress.com/item/1234567890.html', 'https://www.aliexpress.com/item/0987654321.html']
affiliate_links = api.get_affiliate_links(links=links, link_type=model_LinkType.HOTLINK)
if affiliate_links:
    for link in affiliate_links:
        print(link)
```

#### `get_hotproducts`

```python
def get_hotproducts(self, category_ids: str | list = None, delivery_days: int = None, fields: str | list = None, keywords: str = None, max_sale_price: int = None, min_sale_price: int = None, page_no: int = None, page_size: int = None, platform_product_type: model_ProductType = None, ship_to_country: str = None, sort: model_SortBy = None, **kwargs) -> model_HotProductsResponse
```

**Назначение**: Поиск партнерских товаров с высокой комиссией.

**Параметры**:
- `category_ids` (str | list): Один или несколько идентификаторов категорий.
- `delivery_days` (int): Предполагаемое количество дней доставки.
- `fields` (str | list): Поля для включения в список результатов. По умолчанию все.
- `keywords` (str): Поиск товаров на основе ключевых слов.
- `max_sale_price` (int): Фильтрует товары с ценой ниже указанного значения. Цены указываются в наименьшем номинале валюты. Так, $31.41 следует указывать как 3141.
- `min_sale_price` (int): Фильтрует товары с ценой выше указанного значения. Цены указываются в наименьшем номинале валюты. Так, $31.41 следует указывать как 3141.
- `page_no` (int): Номер страницы.
- `page_size` (int): Количество товаров на странице. Должно быть между 1 и 50.
- `platform_product_type` (model_ProductType): Укажите тип товара платформы.
- `ship_to_country` (str): Фильтр товаров, которые могут быть отправлены в эту страну. Возвращает цену в соответствии с налоговой политикой страны.
- `sort` (model_SortBy): Указывает метод сортировки.

**Возвращает**:
- `model_HotProductsResponse`: Содержит информацию об ответе и список продуктов.

**Вызывает исключения**:
- `ProductsNotFoudException`: Если продукты не найдены.
- `ApiRequestException`: Если произошла ошибка при запросе к API.
- `ApiRequestResponseException`: Если произошла ошибка в ответе API.

**Как работает функция**:
- Функция `get_hotproducts` выполняет поиск популярных товаров с высокой комиссией на AliExpress, используя API AliExpress.
- Она принимает различные параметры для фильтрации и сортировки результатов, такие как идентификаторы категорий, количество дней доставки, ключевые слова, минимальная и максимальная цена, номер страницы, размер страницы, тип товара платформы, страна доставки и метод сортировки.
- Функция создает запрос к API AliExpress с использованием метода `AliexpressAffiliateHotproductQueryRequest()`.
- В запрос добавляются все переданные параметры.
- После получения ответа от API, функция проверяет, были ли найдены продукты.
- Если продукты найдены, функция вызывает `parse_products()` для преобразования ответа в список объектов `model_Product`.
- Если продукты не найдены, функция вызывает исключение `ProductsNotFoudException`.
- Функция возвращает объект `model_HotProductsResponse`, содержащий информацию об ответе и список продуктов.

**Примеры**:

```python
hot_products = api.get_hotproducts(category_ids=['123', '456'], keywords='shoes', min_sale_price=1000, max_sale_price=5000, ship_to_country='US')
if hot_products:
    for product in hot_products.products:
        print(product.product_title, product.product_price)
```

#### `get_categories`

```python
def get_categories(self, **kwargs) -> List[model_Category | model_ChildCategory]
```

**Назначение**: Получает все доступные категории, как родительские, так и дочерние.

**Возвращает**:
- `list[model_Category | model_ChildCategory]`: Список категорий.

**Вызывает исключения**:
- `CategoriesNotFoudException`: Если категории не найдены.
- `ApiRequestException`: Если произошла ошибка при запросе к API.
- `ApiRequestResponseException`: Если произошла ошибка в ответе API.

**Как работает функция**:
- Функция `get_categories` получает список всех доступных категорий (родительских и дочерних) из API AliExpress.
- Она создает запрос к API AliExpress с использованием метода `AliexpressAffiliateCategoryGetRequest()`.
- После получения ответа от API, функция проверяет, были ли найдены категории.
- Если категории найдены, функция сохраняет их в атрибуте `categories` экземпляра класса и возвращает их.
- Если категории не найдены, функция вызывает исключение `CategoriesNotFoudException`.

**Примеры**:

```python
categories = api.get_categories()
if categories:
    for category in categories:
        print(category.category_name, category.category_id)
```

#### `get_parent_categories`

```python
def get_parent_categories(self, use_cache=True, **kwargs) -> List[model_Category]
```

**Назначение**: Получает все доступные родительские категории.

**Параметры**:
- `use_cache` (bool): Использует кэшированные категории для уменьшения количества запросов к API.

**Возвращает**:
- `list[model_Category]`: Список родительских категорий.

**Вызывает исключения**:
- `CategoriesNotFoudException`: Если категории не найдены.
- `ApiRequestException`: Если произошла ошибка при запросе к API.
- `ApiRequestResponseException`: Если произошла ошибка в ответе API.

**Как работает функция**:
- Функция `get_parent_categories` получает список всех доступных родительских категорий из API AliExpress.
- Она принимает параметр `use_cache`, который определяет, следует ли использовать кэшированные категории для уменьшения количества запросов к API.
- Если `use_cache` имеет значение `True` и категории уже были загружены ранее, функция использует кэшированные категории.
- В противном случае функция вызывает метод `get_categories()` для загрузки категорий из API.
- Затем функция вызывает функцию `filter_parent_categories()` из модуля `categories` для фильтрации списка категорий и получения только родительских категорий.
- Функция возвращает список родительских категорий.

**Примеры**:

```python
parent_categories = api.get_parent_categories(use_cache=True)
if parent_categories:
    for category in parent_categories:
        print(category.category_name, category.category_id)
```

#### `get_child_categories`

```python
def get_child_categories(self, parent_category_id: int, use_cache=True, **kwargs) -> List[model_ChildCategory]
```

**Назначение**: Получает все доступные дочерние категории для конкретной родительской категории.

**Параметры**:
- `parent_category_id` (int): Идентификатор родительской категории.
- `use_cache` (bool): Использует кэшированные категории для уменьшения количества запросов к API.

**Возвращает**:
- `list[model_ChildCategory]`: Список дочерних категорий.

**Вызывает исключения**:
- `CategoriesNotFoudException`: Если категории не найдены.
- `ApiRequestException`: Если произошла ошибка при запросе к API.
- `ApiRequestResponseException`: Если произошла ошибка в ответе API.

**Как работает функция**:
- Функция `get_child_categories` получает список всех доступных дочерних категорий для указанной родительской категории из API AliExpress.
- Она принимает параметры `parent_category_id` (идентификатор родительской категории) и `use_cache` (указывать, использовать ли кэшированные категории для уменьшения количества запросов к API).
- Если `use_cache` имеет значение `True` и категории уже были загружены ранее, функция использует кэшированные категории.
- В противном случае функция вызывает метод `get_categories()` для загрузки категорий из API.
- Затем функция вызывает функцию `filter_child_categories()` из модуля `categories` для фильтрации списка категорий и получения только дочерних категорий, связанных с указанной родительской категорией.
- Функция возвращает список дочерних категорий.

**Примеры**:

```python
child_categories = api.get_child_categories(parent_category_id=12345, use_cache=True)
if child_categories:
    for category in child_categories:
        print(category.category_name, category.category_id)