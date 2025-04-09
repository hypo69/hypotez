# Модуль для генерации аффилированных продуктов AliExpress

## Обзор

Модуль предназначен для сбора данных о товарах с AliExpress, получения аффилированных ссылок, сохранения изображений и видео, а также для генерации HTML-кода для рекламных кампаний.

## Подробнее

Этот модуль предоставляет класс `AliAffiliatedProducts`, который позволяет получать полную информацию о продуктах с AliExpress по URL-адресам или идентификаторам продуктов. Он также включает функциональность для создания шаблонов рекламных кампаний. Модуль использует различные утилиты для работы с файлами, изображениями, видео и JSON.

## Классы

### `AliAffiliatedProducts`

**Описание**: Класс для сбора полных данных о продуктах по URL-адресам или идентификаторам продуктов.  Для получения более подробной информации о создании шаблонов рекламных кампаний см. раздел `Managing Aliexpress Ad Campaigns`.

**Наследует**: `AliApi`

**Атрибуты**:
- `language` (str): Язык для рекламной кампании (по умолчанию `None`).
- `currency` (str): Валюта для рекламной кампании (по умолчанию `None`).

**Методы**:
- `__init__`: Инициализирует класс `AliAffiliatedProducts`.
- `process_affiliate_products`: Обрабатывает список идентификаторов или URL-адресов продуктов и возвращает список продуктов с партнерскими ссылками и сохраненными изображениями.

## Методы класса

### `__init__`

```python
def __init__(self,
             language: str | dict = 'EN',
             currency: str = 'USD',
             *args, **kwargs):
    """
    Initializes the AliAffiliatedProducts class.
    Args:
        language: Language for the campaign (default 'EN').
        currency: Currency for the campaign (default 'USD').
    """
    ...
```

**Назначение**: Инициализирует экземпляр класса `AliAffiliatedProducts`.

**Параметры**:
- `language` (str | dict): Язык для рекламной кампании (по умолчанию `'EN'`).
- `currency` (str): Валюта для рекламной кампании (по умолчанию `'USD'`).
- `*args`: Произвольные позиционные аргументы.
- `**kwargs`: Произвольные именованные аргументы.

**Как работает функция**:
- Проверяет, что указаны язык и валюта. Если нет, то записывает критическую ошибку в лог и завершает работу.
- Вызывает конструктор родительского класса `AliApi` с указанными языком и валютой.
- Устанавливает атрибуты `language` и `currency` экземпляра класса.

**Примеры**:
```python
affiliated_products = AliAffiliatedProducts(language='RU', currency='RUB')
affiliated_products = AliAffiliatedProducts(language='EN', currency='USD')
```

### `process_affiliate_products`

```python
async def process_affiliate_products(self, prod_ids: list[str], category_root: Path | str) -> list[SimpleNamespace]:
    """
    Processes a list of product IDs or URLs and returns a list of products with affiliate links and saved images.

    Args:
        campaign (SimpleNamespace): The promotional campaign data.
        category_name (str): The name of the category to process.
        prod_ids (list[str]): List of product URLs or IDs.

    Returns:
        list[SimpleNamespace]: A list of processed products with affiliate links and saved images.

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
        Exception: If the category name is not found in the campaign.

    Notes:
        - Fetches page content from URLs.
        - Handles affiliate links and image/video saving.
        - Generates and saves campaign data and output files.

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
    ...
```

**Назначение**: Обрабатывает список идентификаторов или URL-адресов продуктов, чтобы получить партнерские ссылки и сохранить изображения.

**Параметры**:
- `prod_ids` (list[str]): Список URL-адресов или идентификаторов продуктов.
- `category_root` (Path | str): Путь к корневой директории категории.

**Возвращает**:
- `list[SimpleNamespace]`: Список обработанных продуктов с партнерскими ссылками и сохраненными изображениями.

**Как работает функция**:
1.  **Нормализация URL-адресов**:
    *   Преобразует все URL-адреса продуктов в HTTPS формат с помощью функции `ensure_https`.
2.  **Получение партнерских ссылок**:
    *   Для каждого нормализованного URL-адреса продукта пытается получить партнерские ссылки с помощью метода `super().get_affiliate_links(prod_url)`.
    *   Если партнерская ссылка найдена, извлекает `promotion_link` и добавляет её в список `_promotion_links`, а URL продукта — в список `_prod_urls`.
    *   Если партнерская ссылка не найдена, переходит к следующему URL-адресу продукта.
3.  **Обработка отсутствующих партнерских ссылок**:
    *   Если не найдено ни одной партнерской ссылки, в лог записывается предупреждение.
    *   Функция возвращает `None`.
4.  **Получение деталей продукта**:
    *   Извлекает детали продукта для каждого URL-адреса из списка `_prod_urls` с помощью метода `self.retrieve_product_details`.
    *   Если не удалось получить детали продукта, функция возвращает `None`.
5.  **Сохранение данных о продукте**:
    *   Создает пустой список `affiliated_products_list` для хранения обработанных продуктов.
    *   Создает пустой список `product_titles` для хранения заголовков продуктов.
    *   Перебирает продукты и соответствующие партнерские ссылки:
        *   Добавляет заголовок продукта в список `product_titles`.
        *   Устанавливает атрибуты `language` и `promotion_link` для каждого продукта.
        *   Определяет путь для сохранения изображения продукта.
        *   Асинхронно сохраняет изображение продукта, используя URL-адрес основного изображения продукта и определенный путь.
        *   Устанавливает локальный путь к изображению продукта.
        *   Если у продукта есть URL-адрес видео:
            *   Извлекает суффикс (расширение) из URL-адреса видео.
            *   Определяет путь для сохранения видео продукта.
            *   Асинхронно сохраняет видео продукта, используя URL-адрес видео продукта и определенный путь.
            *   Устанавливает локальный путь к видео продукта.
        *   Сохраняет данные продукта в формате JSON в файл.
        *   Добавляет продукт в список `affiliated_products_list`.
6.  **Сохранение заголовков продуктов**:
    *   Определяет путь для сохранения заголовков продуктов.
    *   Сохраняет список заголовков продуктов в текстовый файл.
7.  **Возврат обработанных продуктов**:
    *   Возвращает список `affiliated_products_list`, содержащий все обработанные продукты.

**Внутренние переменные**:
- `_promotion_links` (list): Список партнерских ссылок.
- `_prod_urls` (list): Список URL-адресов продуктов.
- `normilized_prod_urls` (list): Список нормализованных URL-адресов продуктов (HTTPS).
- `print_flag` (str): Флаг для переключения печати в одну строку.
- `_affiliated_products` (List[SimpleNamespace]): Список деталей продуктов, полученных по партнерским ссылкам.
- `affiliated_products_list` (list[SimpleNamespace]): Список обработанных продуктов.
- `product_titles` (list): Список заголовков продуктов.
- `image_path` (Path): Путь для сохранения изображения продукта.
- `parsed_url` (Path): Объект `ParseResult`, содержащий компоненты URL-адреса видео.
- `suffix` (str): Суффикс (расширение) видеофайла.
- `video_path` (Path): Путь для сохранения видео продукта.
- `product_titles_path` (Path): Путь для сохранения файла с заголовками продуктов.

**Примеры**:

```python
import asyncio
from pathlib import Path
from types import SimpleNamespace

# Пример вызова функции
async def main():
    ali_products = AliAffiliatedProducts(language='EN', currency='USD')
    product_ids = ['https://aliexpress.com/item/1234567890.html', 'https://aliexpress.com/item/0987654321.html']
    category_root = Path('./output')
    
    products = await ali_products.process_affiliate_products(product_ids, category_root)
    
    if products:
        for product in products:
            print(f"Product Title: {product.product_title}")
            print(f"Affiliate Link: {product.promotion_link}")
            print(f"Local Image Path: {product.local_image_path}")
            if hasattr(product, 'local_video_path'):
                print(f"Local Video Path: {product.local_video_path}")

if __name__ == "__main__":
    asyncio.run(main())