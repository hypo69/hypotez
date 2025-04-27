# Модуль для работы с продуктами AliExpress
## Overview

Модуль предоставляет класс `Product` для работы с данными о товарах из AliExpress API.

## Details

Этот модуль используется для обработки информации о товарах, получаемой из API AliExpress. Класс `Product`  представляет собой структуру данных, содержащую различные атрибуты, описывающие характеристики товара. 

## Classes

### `Product`

**Description**: Класс `Product` представляет структуру данных для хранения информации о товарах из API AliExpress.

**Attributes**:

- `app_sale_price` (str): Цена продажи в приложении.
- `app_sale_price_currency` (str): Валюта цены продажи в приложении.
- `commission_rate` (str): Комиссия.
- `discount` (str): Скидка.
- `evaluate_rate` (str): Оценка товара.
- `first_level_category_id` (int): ID первой категории.
- `first_level_category_name` (str): Название первой категории.
- `lastest_volume` (int): Последний объем продаж.
- `hot_product_commission_rate` (str): Комиссия за горячие товары.
- `lastest_volume` (int): Последний объем продаж.
- `original_price` (str): Оригинальная цена.
- `original_price_currency` (str): Валюта оригинальной цены.
- `product_detail_url` (str): URL страницы товара.
- `product_id` (int): ID товара.
- `product_main_image_url` (str): URL главной картинки товара.
- `product_small_image_urls` (List[str]): Список URL картинок товара.
- `product_title` (str): Название товара.
- `product_video_url` (str): URL видео товара.
- `promotion_link` (str): URL промо-акции.
- `relevant_market_commission_rate` (str): Комиссия для целевого рынка.
- `sale_price` (str): Цена продажи.
- `sale_price_currency` (str): Валюта цены продажи.
- `second_level_category_id` (int): ID второй категории.
- `second_level_category_name` (str): Название второй категории.
- `shop_id` (int): ID магазина.
- `shop_url` (str): URL магазина.
- `target_app_sale_price` (str): Целевая цена продажи в приложении.
- `target_app_sale_price_currency` (str): Целевая валюта цены продажи в приложении.
- `target_original_price` (str): Целевая оригинальная цена.
- `target_original_price_currency` (str): Целевая валюта оригинальной цены.
- `target_sale_price` (str): Целевая цена продажи.
- `target_sale_price_currency` (str): Целевая валюта цены продажи.

## Example

```python
from src.suppliers.aliexpress.api.models.product import Product

product = Product()
product.product_title = "Новое платье"
product.product_id = 12345
product.product_detail_url = "https://aliexpress.com/item/12345"
```