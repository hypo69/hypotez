# Модуль `affiliated_products_generator`

## Обзор

Модуль `affiliated_products_generator` - это часть проекта `hypotez`, которая используется для сбора данных о товарах AliExpress с партнерскими ссылками. Модуль содержит класс `AliAffiliatedProducts`, который наследует класс `AliApi` и предоставляет функциональность для сбора и обработки информации о товарах. 

## Подробней

Модуль `affiliated_products_generator` используется для создания рекламных кампаний в интернет-магазинах, таких как PrestaShop. Он позволяет собирать данные о товарах AliExpress, включая названия, описания, изображения, видео и партнерские ссылки. 

## Классы

### `AliAffiliatedProducts`

**Описание**: Класс `AliAffiliatedProducts` наследует класс `AliApi` и предоставляет функциональность для сбора и обработки информации о товарах AliExpress с партнерскими ссылками.

**Наследует**: `AliApi`

**Атрибуты**:

- `language` (str): Язык кампании (по умолчанию `EN`).
- `currency` (str): Валюта кампании (по умолчанию `USD`).

**Методы**:

- `__init__(self, language: str | dict = 'EN', currency: str = 'USD', *args, **kwargs)`: Инициализирует класс `AliAffiliatedProducts`.
- `async def process_affiliate_products(self, prod_ids: list[str], category_root: Path | str) -> list[SimpleNamespace]`:  Обрабатывает список идентификаторов товаров или URL-адресов и возвращает список товаров с партнерскими ссылками и сохраненными изображениями.

**Принцип работы**:

Класс `AliAffiliatedProducts` работает следующим образом:

1. **Получение партнерских ссылок**:
   - Метод `process_affiliate_products` принимает список идентификаторов товаров или URL-адресов (`prod_ids`) и корневую директорию для сохранения данных (`category_root`).
   - Он использует метод `get_affiliate_links` из родительского класса `AliApi` для получения партнерских ссылок для каждого товара.
   - Если партнерские ссылки найдены, они добавляются в список `_promotion_links`, а URL-адреса товаров - в список `_prod_urls`.

2. **Извлечение деталей товаров**:
   - Метод `retrieve_product_details` используется для извлечения подробной информации о товарах по полученным URL-адресам.
   - Полученная информация о товарах сохраняется в список `_affiliated_products`.

3. **Обработка и сохранение данных**:
   - Для каждого товара из списка `_affiliated_products` выполняются следующие действия:
     - Сохраняются изображения товаров с использованием метода `save_image_from_url`.
     - Сохраняются видео товаров с использованием метода `save_video_from_url`.
     - Сохраняются данные о товарах в формате JSON.
     - Дополнительно сохраняются названия товаров в текстовый файл.

4. **Возврат результатов**:
   - В результате обработки метод `process_affiliate_products` возвращает список товаров (`affiliated_products_list`) с партнерскими ссылками и сохраненными изображениями/видео.

**Примеры**:

```python
from src.suppliers.suppliers_list.aliexpress.affiliated_products_generator import AliAffiliatedProducts

# Создание экземпляра класса AliAffiliatedProducts
aliexpress_products = AliAffiliatedProducts(language='RU', currency='RUB')

# Список идентификаторов товаров
prod_ids = ['1234567890', '9876543210']

# Корневая директория для сохранения данных
category_root = Path('/path/to/category')

# Вызов метода process_affiliate_products для получения информации о товарах
products = asyncio.run(aliexpress_products.process_affiliate_products(prod_ids, category_root))

# Печать информации о товарах
for product in products:
    print(f"Название товара: {product.product_title}")
    print(f"Партнерская ссылка: {product.promotion_link}")
    print(f"Путь к изображению: {product.local_image_path}")
    print(f"Путь к видео: {product.local_video_path}")
```

## Методы класса

### `process_affiliate_products`

```python
    async def process_affiliate_products(self, prod_ids: list[str], category_root: Path | str) -> list[SimpleNamespace]:
        """
        Обрабатывает список идентификаторов товаров или URL-адресов и возвращает список товаров с партнерскими ссылками и сохраненными изображениями.

        Args:
            prod_ids (list[str]): Список URL-адресов или идентификаторов товаров.
            category_root (Path | str): Корневая директория для сохранения данных.

        Returns:
            list[SimpleNamespace]: Список обработанных товаров с партнерскими ссылками и сохраненными изображениями.

        Example:
            >>> campaign = SimpleNamespace(category={})
            >>> category_name = "electronics"
            >>> prod_ids = ["http://example.com/product1", "http://example.com/product2"]
            >>> products = campaign.process_affiliate_products(category_name, prod_ids)
            >>> for product in products:
            ...     print(product.product_title)
            "Product 1 Title"
            "Product 2 Title"

        Raises:
            Exception: Если имя категории не найдено в кампании.

        Notes:
            - Извлекает содержимое страниц с URL-адресов.
            - Обрабатывает партнерские ссылки и сохраняет изображения/видео.
            - Генерирует и сохраняет данные кампании и выходные файлы.

        Flowchart:
        ┌───────────────────────────────────────────────┐
        │ Start                                         │
        └───────────────────────────────────────────────┘
                            │
                            ▼
        ┌─────────────────────────────────────────────────────────┐
        │ Try to get category from campaign using `category_name` │
        └─────────────────────────────────────────────────────────┘
                            │
                            ┴───────────────────────────────────────────┐
                            │                                           │
                            ▼                                           ▼
        ┌──────────────────────────────────────────────────────┐
        │ Campaign Category found: Initialize paths,           │
        │ set promotional URLs, and process products           │
        └──────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────────────┐
        │ No category found: Create default category    │
        │ and initialize paths, set promotional URLs,   │
        │ and process products                          │
        └───────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────────────┐
        │ Initialize paths and prepare data structures  │
        └───────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────────────┐
        │ Process products URLs to get affiliate links  │
        └───────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────────────────────┐
                │                                       │
                ▼                                       ▼
        ┌─────────────────────────────────────────────┐
        │ No affiliate links found: Log warning       │
        └─────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────────────┐
        │ Retrieve product details for affiliate URLs   │
        └───────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────────────┐
        │ Process each product and save images/videos   │
        └───────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────────────┐
        │ Prepare and save final output data            │
        └───────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────────────┐
        │ Return list of affiliated products            │    
        └───────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────────────┐
        │ End                                           │
        └───────────────────────────────────────────────┘

        """
```

### **Внутренние функции**:

**Функции**:

- `ensure_https(prod_ids: list[str]) -> list[str]`: Преобразует URL-адреса в список с протоколом `https` 

**Пример**:

```python
>>> urls = ['http://aliexpress.com/item/1234567890.html', 'aliexpress.com/item/9876543210.html']
>>> ensure_https(urls)
['https://aliexpress.com/item/1234567890.html', 'https://aliexpress.com/item/9876543210.html']
```

**Описание**:

Функция `ensure_https` используется для проверки URL-адресов и приведения их к протоколу `https`, если это необходимо.

**Принцип работы**:

Функция `ensure_https` перебирает список URL-адресов и проверяет их протокол. Если протокол не `https`, он заменяется на `https`.

**Пример**:

```python
>>> urls = ['http://aliexpress.com/item/1234567890.html', 'aliexpress.com/item/9876543210.html']
>>> ensure_https(urls)
['https://aliexpress.com/item/1234567890.html', 'https://aliexpress.com/item/9876543210.html']