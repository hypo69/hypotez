# Генератор HTML контента рекламной кампании
## Overview

Модуль содержит классы для генерации HTML-контента для товаров, категорий и рекламной кампании. 

## Details

Модуль `html_generators.py` предназначен для создания HTML-файлов для товаров, категорий и рекламной кампании.  Он использует стандартные HTML-теги и CSS для оформления и включает в себя ссылки на Bootstrap, CSS-файл (`styles.css`) и JavaScript-файл для улучшенной функциональности. 

## Classes

### `ProductHTMLGenerator`

**Description**: Класс для генерации HTML для отдельных товаров.

**Attributes**: 
- None

**Methods**:
- `set_product_html(product: SimpleNamespace, category_path: str | Path)`: Создает HTML-файл для отдельного товара.

### `set_product_html(product: SimpleNamespace, category_path: str | Path)`

**Purpose**: Создает HTML-файл для отдельного товара.

**Parameters**:

- `product (SimpleNamespace)`: Данные товара, которые нужно включить в HTML.
- `category_path (str | Path)`: Путь для сохранения HTML-файла.

**Returns**: 
- None

**Raises Exceptions**:
- None

**How the Function Works**:
- Получает данные о товаре (`product`) и путь к категории (`category_path`).
- Создает полный путь к HTML-файлу товара (`html_path`).
- Формирует HTML-код с использованием данных товара:
    - Вставляет заголовок (`<title>`) с названием товара.
    - Добавляет изображение товара (`<img src=...>`) по пути `product.local_image_path`.
    - Указывает цену и валюту (`<span class="product-price">`).
    - Вставляет оригинальную цену (`<span class="product-original-price">`).
    - Отображает категорию товара (`<span class="product-category">`).
    - Добавляет ссылку на товар ("Buy Now" - `<a href=...>`) с `product.promotion_link`.
- Сохраняет сформированный HTML-код в файл (`html_path`) с помощью функции `save_text_file()`.


### `CategoryHTMLGenerator`

**Description**: Класс для генерации HTML для категорий товаров.

**Attributes**: 
- None

**Methods**:
- `set_category_html(products_list: list[SimpleNamespace] | SimpleNamespace, category_path: str | Path)`: Создает HTML-файл для категории.

### `set_category_html(products_list: list[SimpleNamespace] | SimpleNamespace, category_path: str | Path)`

**Purpose**: Создает HTML-файл для категории, включающий список товаров.

**Parameters**:

- `products_list (list[SimpleNamespace] | SimpleNamespace)`: Список товаров, которые нужно включить в HTML.
- `category_path (str | Path)`: Путь для сохранения HTML-файла.

**Returns**: 
- None

**Raises Exceptions**:
- None

**How the Function Works**:
- Получает список товаров (`products_list`) и путь к категории (`category_path`).
- Создает полный путь к HTML-файлу категории (`html_path`).
- Формирует HTML-код для страницы категории:
    - Вставляет заголовок (`<title>`) с названием категории.
    - Создает сетку товаров (`<div class="row product-grid">`) с использованием Bootstrap.
    - В цикле перебирает каждый товар из `products_list`:
        - Вставляет изображение товара (`<img src=...>`) по пути `product.local_image_path`.
        - Добавляет название товара (`<h5 class="card-title">`).
        - Отображает цену, валюту и оригинальную цену.
        - Вставляет категорию товара (`<span class="product-category">`).
        - Добавляет ссылку на товар ("Buy Now" - `<a href=...>`) с `product.promotion_link`.
- Сохраняет сформированный HTML-код в файл (`html_path`) с помощью функции `save_text_file()`.


### `CampaignHTMLGenerator`

**Description**: Класс для генерации HTML для рекламной кампании.

**Attributes**: 
- None

**Methods**:
- `set_campaign_html(categories: list[str], campaign_path: str | Path)`: Создает HTML-файл для кампании, перечисляя все категории.

### `set_campaign_html(categories: list[str], campaign_path: str | Path)`

**Purpose**: Создает HTML-файл для рекламной кампании, перечисляя все категории.

**Parameters**:

- `categories (list[str])`: Список названий категорий.
- `campaign_path (str | Path)`: Путь для сохранения HTML-файла.

**Returns**: 
- None

**Raises Exceptions**:
- None

**How the Function Works**:
- Получает список категорий (`categories`) и путь к кампании (`campaign_path`).
- Создает полный путь к HTML-файлу кампании (`html_path`).
- Формирует HTML-код для страницы кампании:
    - Вставляет заголовок (`<title>`) "Campaign Overview".
    - Создает список категорий (`<ul class="list-group">`).
    - В цикле перебирает каждую категорию из `categories`:
        - Добавляет ссылку на страницу категории (`<a href=...>`).
- Сохраняет сформированный HTML-код в файл (`html_path`) с помощью функции `save_text_file()`.

## Parameter Details

- `product (SimpleNamespace)`: Объект с данными о товаре.
- `category_path (str | Path)`: Путь к директории категории.
- `products_list (list[SimpleNamespace] | SimpleNamespace)`: Список объектов с данными о товарах или один объект с данными о товаре.
- `categories (list[str])`: Список названий категорий.
- `campaign_path (str | Path)`: Путь к директории кампании.

## Examples

### Generating HTML for a Product

```python
from src.suppliers.aliexpress.campaign.html_generators import ProductHTMLGenerator

product = SimpleNamespace(
    product_id="1234567890",
    product_title="Awesome Product",
    local_image_path="path/to/product/image.jpg",
    target_sale_price="10.00",
    target_sale_price_currency="USD",
    target_original_price="15.00",
    target_original_price_currency="USD",
    second_level_category_name="Electronics",
    promotion_link="https://aliexpress.com/product/1234567890"
)

category_path = "/path/to/category"

ProductHTMLGenerator.set_product_html(product, category_path)
```

### Generating HTML for a Category

```python
from src.suppliers.aliexpress.campaign.html_generators import CategoryHTMLGenerator

products_list = [
    SimpleNamespace(
        product_id="1234567890",
        product_title="Awesome Product 1",
        local_image_path="path/to/product/image1.jpg",
        target_sale_price="10.00",
        target_sale_price_currency="USD",
        target_original_price="15.00",
        target_original_price_currency="USD",
        second_level_category_name="Electronics",
        promotion_link="https://aliexpress.com/product/1234567890"
    ),
    SimpleNamespace(
        product_id="9876543210",
        product_title="Cool Product 2",
        local_image_path="path/to/product/image2.jpg",
        target_sale_price="12.00",
        target_sale_price_currency="USD",
        target_original_price="18.00",
        target_original_price_currency="USD",
        second_level_category_name="Electronics",
        promotion_link="https://aliexpress.com/product/9876543210"
    )
]

category_path = "/path/to/category"

CategoryHTMLGenerator.set_category_html(products_list, category_path)
```

### Generating HTML for a Campaign

```python
from src.suppliers.aliexpress.campaign.html_generators import CampaignHTMLGenerator

categories = ["Electronics", "Fashion", "Home"]
campaign_path = "/path/to/campaign"

CampaignHTMLGenerator.set_campaign_html(categories, campaign_path)
```