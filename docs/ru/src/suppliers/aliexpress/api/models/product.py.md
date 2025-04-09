# Модуль `product`

## Обзор

Модуль содержит класс `Product`, который представляет собой модель данных для хранения информации о продукте с AliExpress. Он определяет структуру данных продукта, включая цену, валюту, рейтинг, изображения, URL-адреса и другие детали.

## Подробнее

Этот модуль предназначен для структурированного хранения данных о товарах, полученных из API AliExpress. Класс `Product` используется для представления информации об отдельном товаре и содержит атрибуты, соответствующие различным характеристикам продукта. Этот класс может быть использован для дальнейшей обработки данных о продуктах, например, для анализа, сравнения или отображения информации о товарах.

## Классы

### `Product`

**Описание**: Класс `Product` представляет собой модель данных для хранения информации о продукте с AliExpress.

**Принцип работы**:
Класс `Product` служит контейнером для хранения данных о продукте. Каждый атрибут класса соответствует определенному свойству продукта, такому как цена, название, URL изображения и т.д.
При создании экземпляра класса `Product`, атрибуты заполняются данными, полученными из API AliExpress.

**Атрибуты**:
- `app_sale_price` (str): Цена товара в приложении.
- `app_sale_price_currency` (str): Валюта цены товара в приложении.
- `commission_rate` (str): Комиссионный процент.
- `discount` (str): Скидка на товар.
- `evaluate_rate` (str): Рейтинг товара.
- `first_level_category_id` (int): ID категории первого уровня.
- `first_level_category_name` (str): Название категории первого уровня.
- `lastest_volume` (int): Последний объем продаж.
- `hot_product_commission_rate` (str): Комиссионный процент для популярных товаров.
- `original_price` (str): Оригинальная цена товара.
- `original_price_currency` (str): Валюта оригинальной цены товара.
- `product_detail_url` (str): URL страницы с детальным описанием товара.
- `product_id` (int): ID товара.
- `product_main_image_url` (str): URL главного изображения товара.
- `product_small_image_urls` (List[str]): Список URL маленьких изображений товара.
- `product_title` (str): Название товара.
- `product_video_url` (str): URL видео товара.
- `promotion_link` (str): Ссылка на промоакцию товара.
- `relevant_market_commission_rate` (str): Комиссионный процент на релевантном рынке.
- `sale_price` (str): Цена товара со скидкой.
- `sale_price_currency` (str): Валюта цены товара со скидкой.
- `second_level_category_id` (int): ID категории второго уровня.
- `second_level_category_name` (str): Название категории второго уровня.
- `shop_id` (int): ID магазина.
- `shop_url` (str): URL магазина.
- `target_app_sale_price` (str): Целевая цена товара в приложении.
- `target_app_sale_price_currency` (str): Валюта целевой цены товара в приложении.
- `target_original_price` (str): Целевая оригинальная цена товара.
- `target_original_price_currency` (str): Валюта целевой оригинальной цены товара.
- `target_sale_price` (str): Целевая цена товара со скидкой.
- `target_sale_price_currency` (str): Валюта целевой цены товара со скидкой.

**Примеры**:

```python
from typing import List

class Product:
    app_sale_price: str
    app_sale_price_currency: str
    commission_rate: str
    discount: str
    evaluate_rate: str
    first_level_category_id: int
    first_level_category_name: str
    lastest_volume: int
    hot_product_commission_rate: str
    lastest_volume: int
    original_price: str
    original_price_currency: str
    product_detail_url: str
    product_id: int
    product_main_image_url: str
    product_small_image_urls: List[str]
    product_title: str
    product_video_url: str
    promotion_link: str
    relevant_market_commission_rate: str
    sale_price: str
    sale_price_currency: str
    second_level_category_id: int
    second_level_category_name: str
    shop_id: int
    shop_url: str
    target_app_sale_price: str
    target_app_sale_price_currency: str
    target_original_price: str
    target_original_price_currency: str
    target_sale_price: str
    target_sale_price_currency: str

# Пример создания экземпляра класса Product
product = Product()
product.product_title = "Example Product"
product.sale_price = "10.00"
product.sale_price_currency = "USD"
print(product.product_title, product.sale_price, product.sale_price_currency)
# > Example Product 10.00 USD
```