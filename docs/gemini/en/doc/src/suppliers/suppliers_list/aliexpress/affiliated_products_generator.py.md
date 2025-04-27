# Алиэкспресс Affiliated Products Generator

## Обзор

Этот модуль содержит класс `AliAffiliatedProducts`, который позволяет собирать полные данные о товарах с Алиэкспресс, используя URL-адреса или ID товаров. Модуль также генерирует HTML-шаблоны для рекламных кампаний, используя информацию о продуктах.

## Подробности

Этот модуль является частью проекта `hypotez` и используется для сбора данных о товарах с Алиэкспресс. 

### Использование

`AliAffiliatedProducts` - это класс, который наследует от класса `AliApi`. Этот класс предоставляет функциональность для работы с API AliExpress, извлечения аффилированных ссылок и сохранения данных о товарах.

## Классы

### `AliAffiliatedProducts`

**Описание**: Класс для сбора полных данных о продуктах с Алиэкспресс, используя URLs или ID продуктов. 
    Для получения более подробной информации о том, как создавать шаблоны для рекламных кампаний, смотрите раздел `Managing Aliexpress Ad Campaigns`.

**Inherits**: `AliApi` 

**Attributes**:
- `language` (str): Язык для кампании (по умолчанию `'EN'`).
- `currency` (str): Валюта для кампании (по умолчанию `'USD'`).

**Methods**:

- `__init__(language: str | dict = 'EN', currency: str = 'USD', *args, **kwargs)`: Инициализирует класс `AliAffiliatedProducts`.

- `process_affiliate_products(prod_ids: list[str], category_root: Path | str) -> list[SimpleNamespace]`:
    Обрабатывает список ID продуктов или URLs и возвращает список продуктов с аффилированными ссылками и сохраненными изображениями.

    **Purpose**: Эта функция собирает информацию о товарах с Алиэкспресс, используя список URLs или ID товаров. 
        Она обрабатывает каждый URL или ID товара, получая аффилированную ссылку, а затем извлекает полные данные о товаре с помощью API AliExpress. 
        Функция сохраняет изображения товара и видео (если есть) в локальный каталог, а также генерирует HTML-шаблоны для рекламной кампании.

    **Parameters**:
    - `prod_ids` (list[str]): Список URLs или ID продуктов.
    - `category_root` (Path | str): Путь к каталогу, в котором будут сохранены данные о товарах.

    **Returns**:
    - `list[SimpleNamespace]`: Список обработанных продуктов с аффилированными ссылками и сохраненными изображениями.

    **Raises Exceptions**:
    - `Exception`: Если имя категории не найдено в кампании.

    **Examples**:
    ```python
    >>> campaign = SimpleNamespace(category={})\n
    >>> category_name = "electronics"\n
    >>> prod_ids = ["http://example.com/product1", "http://example.com/product2"]\n
    >>> products = campaign.process_affiliate_products(category_name, prod_ids)\n
    >>> for product in products:\n
    ...     print(product.product_title)\n
    "Product 1 Title"\n
    "Product 2 Title"\n
    ```

    **How the Function Works**:
    - Функция сначала получает список ID продуктов или URLs и нормализует их к виду `https://aliexpress.com/item/<product_id>.html`.
    - Для каждого ID товара или URL функция проверяет наличие аффилированной ссылки.
    - Если аффилированная ссылка найдена, функция извлекает полные данные о товаре с помощью API AliExpress.
    - Функция сохраняет изображения товара и видео (если есть) в локальный каталог, а также генерирует HTML-шаблоны для рекламной кампании.

    **Inner Functions**:
    - `get_affiliate_links(prod_url: str) -> list[dict | None]`: 
        Извлекает аффилированные ссылки для данного ID товара или URL.
        **Purpose**: Функция извлекает аффилированную ссылку для товара с Алиэкспресс, используя URL или ID товара.
            Она использует API AliExpress, чтобы получить список всех аффилированных ссылок для товара.
        **Parameters**:
        - `prod_url` (str): URL или ID товара.
        **Returns**:
        - `list[dict | None]`: Список аффилированных ссылок для товара или `None`, если аффилированных ссылок не найдено.
    - `retrieve_product_details(prod_urls: list[str]) -> list[SimpleNamespace]`:
        Извлекает полные данные о товарах по списку аффилированных URLs.
        **Purpose**: Функция извлекает полные данные о товарах с Алиэкспресс, используя список аффилированных ссылок.
            Она использует API AliExpress, чтобы получить детальную информацию о каждом товаре, такую как название, описание, цена, изображения и видео.
        **Parameters**:
        - `prod_urls` (list[str]): Список аффилированных URLs.
        **Returns**:
        - `list[SimpleNamespace]`: Список объектов `SimpleNamespace` с информацией о товарах.

## Примеры

### Создание экземпляра класса `AliAffiliatedProducts`:

```python
from src.suppliers.suppliers_list.aliexpress.affiliated_products_generator import AliAffiliatedProducts

aliexpress_products = AliAffiliatedProducts(language='RU', currency='RUB')
```

### Обработка списка ID товаров:

```python
prod_ids = ['1234567890', '9876543210']
category_root = Path('/path/to/category/data')
products = await aliexpress_products.process_affiliate_products(prod_ids, category_root)

for product in products:
    print(product.product_title)
    print(product.promotion_link)
```

## Параметры

- `language` (str): Язык для кампании (по умолчанию `'EN'`). Может принимать значение `'EN'` (английский), `'RU'` (русский) или другой поддерживаемый язык.
- `currency` (str): Валюта для кампании (по умолчанию `'USD'`). Может принимать значение `'USD'`, `'RUB'`, `'EUR'` или другую поддерживаемую валюту.

## Примеры

### Создание экземпляра класса `AliAffiliatedProducts` с использованием различных языков и валют:

```python
from src.suppliers.suppliers_list.aliexpress.affiliated_products_generator import AliAffiliatedProducts

aliexpress_products_en_usd = AliAffiliatedProducts(language='EN', currency='USD')
aliexpress_products_ru_rub = AliAffiliatedProducts(language='RU', currency='RUB')
aliexpress_products_de_eur = AliAffiliatedProducts(language='DE', currency='EUR')
```

### Обработка списка ID товаров с использованием разных языков и валют:

```python
prod_ids = ['1234567890', '9876543210']
category_root = Path('/path/to/category/data')

products_en_usd = await aliexpress_products_en_usd.process_affiliate_products(prod_ids, category_root)
products_ru_rub = await aliexpress_products_ru_rub.process_affiliate_products(prod_ids, category_root)
products_de_eur = await aliexpress_products_de_eur.process_affiliate_products(prod_ids, category_root)
```