# Модуль для работы с API AliExpress
======================================

Модуль предоставляет класс `AliexpressApi`, который упрощает взаимодействие с API AliExpress для получения информации о продуктах и создания партнерских ссылок.

## Оглавление
- [Обзор](#обзор)
- [Подробнее](#подробнее)
- [Классы](#классы)
  - [AliexpressApi](#aliexpressapi)
- [Функции](#функции)
  - [retrieve_product_details](#retrieve_product_details)
  - [get_affiliate_links](#get_affiliate_links)
  - [get_hotproducts](#get_hotproducts)
  - [get_categories](#get_categories)
  - [get_parent_categories](#get_parent_categories)
  - [get_child_categories](#get_child_categories)

## Обзор

Модуль `src.suppliers.aliexpress.api` предоставляет интерфейс для взаимодействия с API AliExpress. Он включает в себя класс `AliexpressApi`, который содержит методы для получения информации о товарах, создания партнерских ссылок и получения категорий товаров. Модуль использует другие модули и модели для обработки данных и выполнения запросов к API AliExpress.

## Подробнее

Этот модуль разработан для упрощения работы с API AliExpress. Он предоставляет удобные методы для выполнения различных операций, таких как поиск товаров, получение информации о товарах, создание партнерских ссылок и получение списка категорий. Модуль использует классы моделей данных для представления информации о товарах и категориях, что упрощает работу с данными, полученными из API AliExpress.

## Классы

### `AliexpressApi`

**Описание**: Класс `AliexpressApi` предоставляет методы для получения информации из AliExpress с использованием API credentials.

**Принцип работы**:
Класс инициализируется с использованием ключа API, секретного ключа, языка и валюты. Он также может включать идентификатор отслеживания. Класс предоставляет методы для получения сведений о продукте, получения партнерских ссылок, получения популярных продуктов и получения категорий.

**Аттрибуты**:
- `_key` (str): API ключ.
- `_secret` (str): API секрет.
- `_tracking_id` (str): Идентификатор отслеживания для генерации ссылок.
- `_language` (model_Language): Код языка.
- `_currency` (model_Currency): Код валюты.
- `_app_signature` (str): Подпись приложения.
- `categories` (List[model_Category | model_ChildCategory]): Кэшированный список категорий.

**Методы**:
- `retrieve_product_details`: Получает информацию о продуктах.
- `get_affiliate_links`: Преобразует список ссылок в партнерские ссылки.
- `get_hotproducts`: Поиск партнерских продуктов с высокой комиссией.
- `get_categories`: Получает все доступные категории, как родительские, так и дочерние.
- `get_parent_categories`: Получает все доступные родительские категории.
- `get_child_categories`: Получает все доступные дочерние категории для указанной родительской категории.

## Функции

### `retrieve_product_details`

```python
def retrieve_product_details(
        product_ids: str | list,
        fields: str | list = None,
        country: str = None,
        **kwargs) -> List[model_Product]:
    """ Функция получает информацию о продуктах из AliExpress API.

    Args:
        product_ids (str | list): Один или несколько идентификаторов продуктов или ссылок на продукты.
        fields (str | list, optional): Список полей, которые необходимо включить в результаты. По умолчанию включает все поля.
        country (str, optional): Страна, для которой необходимо отфильтровать продукты.
            Возвращает цену с учетом налоговой политики страны. По умолчанию `None`.

    Returns:
        list[model_Product]: Список объектов `model_Product`, содержащих информацию о продуктах.

    Raises:
        ProductsNotFoudException: Если продукты не найдены.
        InvalidArgumentException: Если переданы неверные аргументы.
        ApiRequestException: Если произошла ошибка при выполнении запроса к API.
        ApiRequestResponseException: Если получен некорректный ответ от API.
    """
```

**Назначение**: Получение детальной информации о продуктах из AliExpress.

**Параметры**:
- `product_ids` (str | list): Идентификаторы продуктов или список идентификаторов.
- `fields` (str | list, optional): Список полей для включения в ответ. По умолчанию `None`.
- `country` (str, optional): Страна доставки. По умолчанию `None`.

**Возвращает**:
- `List[model_Product]`: Список продуктов.

**Вызывает исключения**:
- `ProductsNotFoudException`: Если продукты не найдены.
- `InvalidArgumentException`: Если переданы некорректные аргументы.
- `ApiRequestException`: Если произошла ошибка при выполнении запроса к API.
- `ApiRequestResponseException`: Если получен некорректный ответ от API.

**Как работает функция**:

1.  **Подготовка идентификаторов продуктов**:
    - Функция `get_product_ids` преобразует входной параметр `product_ids` (который может быть строкой или списком) в список идентификаторов продуктов.
    - Затем `get_list_as_string` преобразует полученный список в строку, разделенную запятыми, для передачи в API запрос.

2.  **Формирование API запроса**:
    - Создается объект запроса `AliexpressAffiliateProductdetailGetRequest` из библиотеки `aliapi.rest`.
    - Устанавливаются параметры запроса, такие как подпись приложения, поля для включения в ответ, идентификаторы продуктов, страна доставки, валюта и язык.

3.  **Выполнение API запроса**:
    - Функция `api_request` выполняет запрос к API AliExpress с использованием сформированного объекта запроса и типа ответа.

4.  **Обработка ответа**:
    - Если количество записей в ответе больше 0, функция `parse_products` преобразует полученные данные в список объектов `model_Product`.
    - Если продукты не найдены, регистрируется предупреждение с использованием `logger.warning`.

5.  **Обработка ошибок**:
    - Если в процессе выполнения запроса или обработки ответа возникает исключение, оно логируется с использованием `logger.error`.

```
   Начало
      ↓
   Преобразование product_ids в список строк
      ↓
   Формирование API запроса
      ↓
   Выполнение API запроса через api_request
      ↓
   Проверка количества записей в ответе > 0?
   ├── Да →  Преобразование ответа в список объектов model_Product
   │       ↓
   │       Возврат списка model_Product
   │
   └── Нет → Логирование предупреждения
           ↓
           Возврат None
```

**Примеры**:

```python
from src.suppliers.aliexpress.api.api import AliexpressApi
from src.suppliers.aliexpress.api.models import Language, Currency

# Инициализация API
api = AliexpressApi(key='your_key', secret='your_secret', language=Language.RU, currency=Currency.RUB, tracking_id='your_tracking_id')

# Пример 1: Получение информации о продукте по ID
product_id = '1234567890'
product_details = api.retrieve_product_details(product_ids=product_id)
if product_details:
    print(f'Product details: {product_details[0].title}')
else:
    print('Product not found')

# Пример 2: Получение информации о нескольких продуктах с указанием полей
product_ids = ['1234567890', '0987654321']
fields = ['product_title', 'product_price']
product_details = api.retrieve_product_details(product_ids=product_ids, fields=fields)
if product_details:
    print(f'Product details: {product_details[0].title}, {product_details[0].price}')
else:
    print('Products not found')

# Пример 3: Получение информации о продукте с фильтрацией по стране
product_id = '1234567890'
country = 'US'
product_details = api.retrieve_product_details(product_ids=product_id, country=country)
if product_details:
    print(f'Product price in US: {product_details[0].price}')
else:
    print('Product not found')
```

### `get_affiliate_links`

```python
def get_affiliate_links(
        links: str | list,
        link_type: model_LinkType = model_LinkType.NORMAL,
        **kwargs) -> List[model_AffiliateLink]:
    """ Преобразует список ссылок в партнерские ссылки AliExpress.

    Args:
        links (str | list): Одна или несколько ссылок для конвертации.
        link_type (model_LinkType, optional): Тип ссылки: `NORMAL` (стандартная комиссия) или `HOTLINK` (высокая комиссия).
            По умолчанию `NORMAL`.

    Returns:
        list[model_AffiliateLink]: Список партнерских ссылок.

    Raises:
        InvalidArgumentException: Если переданы неверные аргументы.
        InvalidTrackingIdException: Если не указан tracking_id.
        ProductsNotFoudException: Если партнерские ссылки не доступны.
        ApiRequestException: Если произошла ошибка при выполнении запроса к API.
        ApiRequestResponseException: Если получен некорректный ответ от API.
    """
```

**Назначение**: Преобразование списка ссылок в партнерские ссылки AliExpress.

**Параметры**:
- `links` (str | list): Список ссылок для конвертации.
- `link_type` (model_LinkType, optional): Тип партнерской ссылки. По умолчанию `model_LinkType.NORMAL`.

**Возвращает**:
- `List[model_AffiliateLink]`: Список партнерских ссылок.

**Вызывает исключения**:
- `InvalidArgumentException`: Если переданы неверные аргументы.
- `InvalidTrackingIdException`: Если не указан `tracking_id`.
- `ProductsNotFoudException`: Если партнерские ссылки не доступны.
- `ApiRequestException`: Если произошла ошибка при выполнении запроса к API.
- `ApiRequestResponseException`: Если получен некорректный ответ от API.

**Как работает функция**:

1.  **Проверка наличия tracking_id**:
    - Функция проверяет, установлен ли идентификатор отслеживания (`self._tracking_id`). Если `tracking_id` не установлен, функция регистрирует ошибку с использованием `logger.error` и возвращает `None`.

2.  **Преобразование списка ссылок**:
    - Функция `get_list_as_string` преобразует входной параметр `links` (который может быть строкой или списком) в строку, разделенную запятыми, для передачи в API запрос.

3.  **Формирование API запроса**:
    - Создается объект запроса `AliexpressAffiliateLinkGenerateRequest` из библиотеки `aliapi.rest`.
    - Устанавливаются параметры запроса, такие как подпись приложения, исходные значения (ссылки), тип ссылки и идентификатор отслеживания.

4.  **Выполнение API запроса**:
    - Функция `api_request` выполняет запрос к API AliExpress с использованием сформированного объекта запроса и типа ответа.

5.  **Обработка ответа**:
    - Если ответ от API не получен, функция возвращает `None`.
    - Если количество результатов в ответе больше 0, функция возвращает список партнерских ссылок из ответа (`response.promotion_links.promotion_link`).
    - Если партнерские ссылки не доступны, регистрируется предупреждение с использованием `logger.warning` и функция возвращает `None`.

```
   Начало
      ↓
   Проверка наличия tracking_id
   ├── Нет → Логирование ошибки
   │       ↓
   │       Возврат None
   │
   └── Да → Преобразование links в строку
           ↓
           Формирование API запроса
           ↓
           Выполнение API запроса через api_request
           ↓
           Проверка наличия ответа
           ├── Нет → Возврат None
           │
           └── Да → Проверка total_result_count > 0?
                   ├── Да → Возврат списка партнерских ссылок
                   │
                   └── Нет → Логирование предупреждения
                           ↓
                           Возврат None
```

**Примеры**:

```python
from src.suppliers.aliexpress.api.api import AliexpressApi
from src.suppliers.aliexpress.api.models import Language, Currency, LinkType

# Инициализация API
api = AliexpressApi(key='your_key', secret='your_secret', language=Language.RU, currency=Currency.RUB, tracking_id='your_tracking_id')

# Пример 1: Получение партнерских ссылок для одной ссылки
link = 'https://www.aliexpress.com/item/1234567890.html'
affiliate_links = api.get_affiliate_links(links=link)
if affiliate_links:
    print(f'Affiliate link: {affiliate_links[0].promotion_url}')
else:
    print('Affiliate links not available')

# Пример 2: Получение партнерских ссылок для нескольких ссылок с указанием типа ссылки
links = ['https://www.aliexpress.com/item/1234567890.html', 'https://www.aliexpress.com/item/0987654321.html']
affiliate_links = api.get_affiliate_links(links=links, link_type=LinkType.HOTLINK)
if affiliate_links:
    print(f'Affiliate link: {affiliate_links[0].promotion_url}')
else:
    print('Affiliate links not available')
```

### `get_hotproducts`

```python
def get_hotproducts(
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
    """ Функция выполняет поиск партнерских продуктов с высокой комиссией на AliExpress.

    Args:
        category_ids (str | list, optional): Один или несколько идентификаторов категорий. По умолчанию `None`.
        delivery_days (int, optional): Предполагаемое количество дней доставки. По умолчанию `None`.
        fields (str | list, optional): Список полей, которые необходимо включить в результаты. По умолчанию включает все поля.
        keywords (str, optional): Ключевые слова для поиска продуктов. По умолчанию `None`.
        max_sale_price (int, optional): Максимальная цена продукта (в минимальной валютной единице, например, центах). По умолчанию `None`.
        min_sale_price (int, optional): Минимальная цена продукта (в минимальной валютной единице). По умолчанию `None`.
        page_no (int, optional): Номер страницы результатов. По умолчанию `None`.
        page_size (int, optional): Количество продуктов на странице (от 1 до 50). По умолчанию `None`.
        platform_product_type (model_ProductType, optional): Тип продукта платформы. По умолчанию `None`.
        ship_to_country (str, optional): Страна, в которую возможна доставка. По умолчанию `None`.
        sort (model_SortBy, optional): Метод сортировки результатов. По умолчанию `None`.

    Returns:
        model_HotProductsResponse: Объект `model_HotProductsResponse`, содержащий информацию об ответе и список продуктов.

    Raises:
        ProductsNotFoudException: Если продукты не найдены.
        ApiRequestException: Если произошла ошибка при выполнении запроса к API.
        ApiRequestResponseException: Если получен некорректный ответ от API.
    """
```

**Назначение**: Поиск партнерских продуктов с высокой комиссией.

**Параметры**:
- `category_ids` (str | list, optional): Список идентификаторов категорий. По умолчанию `None`.
- `delivery_days` (int, optional): Количество дней доставки. По умолчанию `None`.
- `fields` (str | list, optional): Список полей для включения в ответ. По умолчанию `None`.
- `keywords` (str, optional): Ключевые слова для поиска. По умолчанию `None`.
- `max_sale_price` (int, optional): Максимальная цена. По умолчанию `None`.
- `min_sale_price` (int, optional): Минимальная цена. По умолчанию `None`.
- `page_no` (int, optional): Номер страницы. По умолчанию `None`.
- `page_size` (int, optional): Размер страницы. По умолчанию `None`.
- `platform_product_type` (model_ProductType, optional): Тип продукта платформы. По умолчанию `None`.
- `ship_to_country` (str, optional): Страна доставки. По умолчанию `None`.
- `sort` (model_SortBy, optional): Метод сортировки. По умолчанию `None`.

**Возвращает**:
- `model_HotProductsResponse`: Ответ с списком продуктов.

**Вызывает исключения**:
- `ProductsNotFoudException`: Если продукты не найдены.
- `ApiRequestException`: Если произошла ошибка при выполнении запроса к API.
- `ApiRequestResponseException`: Если получен некорректный ответ от API.

**Как работает функция**:

1.  **Формирование API запроса**:
    - Создается объект запроса `AliexpressAffiliateHotproductQueryRequest` из библиотеки `aliapi.rest`.
    - Устанавливаются параметры запроса, такие как подпись приложения, идентификаторы категорий, количество дней доставки, поля для включения в ответ, ключевые слова, максимальная и минимальная цена, номер страницы, размер страницы, тип продукта платформы, страна доставки и метод сортировки.

2.  **Выполнение API запроса**:
    - Функция `api_request` выполняет запрос к API AliExpress с использованием сформированного объекта запроса и типа ответа.

3.  **Обработка ответа**:
    - Если количество записей в ответе больше 0, функция `parse_products` преобразует полученные данные в список объектов `model_Product` и присваивает его атрибуту `products` объекта `response`.
    - Если продукты не найдены, вызывается исключение `ProductsNotFoudException`.

```
   Начало
      ↓
   Формирование API запроса
      ↓
   Выполнение API запроса через api_request
      ↓
   Проверка количества записей в ответе > 0?
   ├── Да →  Преобразование ответа в список объектов model_Product
   │       ↓
   │       Возврат объекта model_HotProductsResponse
   │
   └── Нет → Вызов исключения ProductsNotFoudException
```

**Примеры**:

```python
from src.suppliers.aliexpress.api.api import AliexpressApi
from src.suppliers.aliexpress.api.models import Language, Currency, SortBy

# Инициализация API
api = AliexpressApi(key='your_key', secret='your_secret', language=Language.RU, currency=Currency.RUB, tracking_id='your_tracking_id')

# Пример 1: Получение популярных продуктов без фильтров
hot_products = api.get_hotproducts()
if hot_products.products:
    print(f'Hot product: {hot_products.products[0].title}')
else:
    print('Hot products not found')

# Пример 2: Получение популярных продуктов с фильтрацией по категории и сортировкой
category_ids = ['123', '456']
hot_products = api.get_hotproducts(category_ids=category_ids, sort=SortBy.AVG_USER_RATING_DSR)
if hot_products.products:
    print(f'Hot product: {hot_products.products[0].title}')
else:
    print('Hot products not found')
```

### `get_categories`

```python
def get_categories(self, **kwargs) -> List[model_Category | model_ChildCategory]:
    """ Получает все доступные категории товаров AliExpress, как родительские, так и дочерние.

    Returns:
        list[model_Category | model_ChildCategory]: Список категорий.

    Raises:
        CategoriesNotFoudException: Если категории не найдены.
        ApiRequestException: Если произошла ошибка при выполнении запроса к API.
        ApiRequestResponseException: Если получен некорректный ответ от API.
    """
```

**Назначение**: Получение списка категорий товаров.

**Возвращает**:
- `List[model_Category | model_ChildCategory]`: Список категорий.

**Вызывает исключения**:
- `CategoriesNotFoudException`: Если категории не найдены.
- `ApiRequestException`: Если произошла ошибка при выполнении запроса к API.
- `ApiRequestResponseException`: Если получен некорректный ответ от API.

**Как работает функция**:

1.  **Формирование API запроса**:
    - Создается объект запроса `AliexpressAffiliateCategoryGetRequest` из библиотеки `aliapi.rest`.
    - Устанавливается подпись приложения.

2.  **Выполнение API запроса**:
    - Функция `api_request` выполняет запрос к API AliExpress с использованием сформированного объекта запроса и типа ответа.

3.  **Обработка ответа**:
    - Если количество результатов в ответе больше 0, функция сохраняет категории в атрибуте `categories` объекта `self` и возвращает список категорий из ответа (`response.categories.category`).
    - Если категории не найдены, вызывается исключение `CategoriesNotFoudException`.

```
   Начало
      ↓
   Формирование API запроса
      ↓
   Выполнение API запроса через api_request
      ↓
   Проверка количества записей в ответе > 0?
   ├── Да →  Сохранение категорий в self.categories
   │       ↓
   │       Возврат списка категорий
   │
   └── Нет → Вызов исключения CategoriesNotFoudException
```

**Примеры**:

```python
from src.suppliers.aliexpress.api.api import AliexpressApi
from src.suppliers.aliexpress.api.models import Language, Currency

# Инициализация API
api = AliexpressApi(key='your_key', secret='your_secret', language=Language.RU, currency=Currency.RUB, tracking_id='your_tracking_id')

# Получение категорий
categories = api.get_categories()
if categories:
    print(f'Category: {categories[0].name}')
else:
    print('Categories not found')
```

### `get_parent_categories`

```python
def get_parent_categories(self, use_cache=True, **kwargs) -> List[model_Category]:
    """ Получает все доступные родительские категории товаров AliExpress.

    Args:
        use_cache (bool, optional): Использовать кэшированные категории для уменьшения количества запросов к API. По умолчанию `True`.

    Returns:
        list[model_Category]: Список родительских категорий.

    Raises:
        CategoriesNotFoudException: Если категории не найдены.
        ApiRequestException: Если произошла ошибка при выполнении запроса к API.
        ApiRequestResponseException: Если получен некорректный ответ от API.
    """
```

**Назначение**: Получение списка родительских категорий товаров.

**Параметры**:
- `use_cache` (bool, optional): Использовать кэш. По умолчанию `True`.

**Возвращает**:
- `List[model_Category]`: Список родительских категорий.

**Вызывает исключения**:
- `CategoriesNotFoudException`: Если категории не найдены.
- `ApiRequestException`: Если произошла ошибка при выполнении запроса к API.
- `ApiRequestResponseException`: Если получен некорректный ответ от API.

**Как работает функция**:

1.  **Проверка наличия кэша**:
    - Функция проверяет, нужно ли использовать кэшированные категории (`use_cache`) и есть ли они в атрибуте `categories` объекта `self`.
    - Если кэш не используется или категории не найдены в кэше, функция вызывает метод `get_categories` для получения категорий с API.

2.  **Фильтрация родительских категорий**:
    - Функция `filter_parent_categories` фильтрует список категорий и возвращает только родительские категории.

```
   Начало
      ↓
   Проверка use_cache и self.categories
   ├── use_cache == True и self.categories != None →  Фильтрация родительских категорий
   │       ↓
   │       Возврат списка родительских категорий
   │
   └── Иначе →  Вызов self.get_categories()
           ↓
           Фильтрация родительских категорий
           ↓
           Возврат списка родительских категорий
```

**Примеры**:

```python
from src.suppliers.aliexpress.api.api import AliexpressApi
from src.suppliers.aliexpress.api.models import Language, Currency

# Инициализация API
api = AliexpressApi(key='your_key', secret='your_secret', language=Language.RU, currency=Currency.RUB, tracking_id='your_tracking_id')

# Получение родительских категорий
parent_categories = api.get_parent_categories()
if parent_categories:
    print(f'Parent category: {parent_categories[0].name}')
else:
    print('Parent categories not found')
```

### `get_child_categories`

```python
def get_child_categories(self, parent_category_id: int, use_cache=True, **kwargs) -> List[model_ChildCategory]:
    """ Получает все доступные дочерние категории товаров AliExpress для указанной родительской категории.

    Args:
        parent_category_id (int): Идентификатор родительской категории.
        use_cache (bool, optional): Использовать кэшированные категории для уменьшения количества запросов к API. По умолчанию `True`.

    Returns:
        list[model_ChildCategory]: Список дочерних категорий.

    Raises:
        CategoriesNotFoudException: Если категории не найдены.
        ApiRequestException: Если произошла ошибка при выполнении запроса к API.
        ApiRequestResponseException: Если получен некорректный ответ от API.
    """
```

**Назначение**: Получение списка дочерних категорий товаров для указанной родительской категории.

**Параметры**:
- `parent_category_id` (int): Идентификатор родительской категории.
- `use_cache` (bool, optional): Использовать кэш. По умолчанию `True`.

**Возвращает**:
- `List[model_ChildCategory]`: Список дочерних категорий.

**Вызывает исключения**:
- `CategoriesNotFoudException`: Если категории не найдены.
- `ApiRequestException`: Если произошла ошибка при выполнении запроса к API.
- `ApiRequestResponseException`: Если получен некорректный ответ от API.

**Как работает функция**:

1.  **Проверка наличия кэша**:
    - Функция проверяет, нужно ли использовать кэшированные категории (`use_cache`) и есть ли они в атрибуте `categories` объекта `self`.
    - Если кэш не используется или категории не найдены в кэше, функция вызывает метод `get_categories` для получения категорий с API.

2.  **Фильтрация дочерних категорий**:
    - Функция `filter_child_categories` фильтрует список категорий и возвращает только дочерние категории для указанного `parent_category_id`.

```
   Начало
      ↓
   Проверка use_cache и self.categories
   ├── use_cache == True и self.categories != None →  Фильтрация дочерних категорий
   │       ↓
   │       Возврат списка дочерних категорий
   │
   └── Иначе →  Вызов self.get_categories()
           ↓
           Фильтрация дочерних категорий
           ↓
           Возврат списка дочерних категорий
```

**Примеры**:

```python
from src.suppliers.aliexpress.api.api import AliexpressApi
from src.suppliers.aliexpress.api.models import Language, Currency

# Инициализация API
api = AliexpressApi(key='your_key', secret='your_secret', language=Language.RU, currency=Currency.RUB, tracking_id='your_tracking_id')

# Получение дочерних категорий для родительской категории с ID 100
parent_category_id = 100
child_categories = api.get_child_categories(parent_category_id=parent_category_id)
if child_categories:
    print(f'Child category: {child_categories[0].name}')
else:
    print('Child categories not found')