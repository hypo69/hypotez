# Модуль: src.suppliers.aliexpress.api.models.product

## Обзор

Модуль содержит класс `Product`, который представляет собой модель товара с AliExpress. Класс предоставляет информацию о товаре, такую как название, цена, категория, изображения, ссылки и т.д.

## Классы

### `Product`

**Описание**: Класс модели товара с AliExpress.

**Атрибуты**:

- `app_sale_price` (str): Цена продажи в приложении.
- `app_sale_price_currency` (str): Валюта цены продажи в приложении.
- `commission_rate` (str): Комиссия за продажу.
- `discount` (str): Скидка.
- `evaluate_rate` (str): Оценка товара.
- `first_level_category_id` (int): Идентификатор категории первого уровня.
- `first_level_category_name` (str): Название категории первого уровня.
- `lastest_volume` (int): Последний объем продаж.
- `hot_product_commission_rate` (str): Комиссия за продажу популярного товара.
- `lastest_volume` (int): Последний объем продаж.
- `original_price` (str): Оригинальная цена.
- `original_price_currency` (str): Валюта оригинальной цены.
- `product_detail_url` (str): Ссылка на страницу товара.
- `product_id` (int): Идентификатор товара.
- `product_main_image_url` (str): URL главной картинки товара.
- `product_small_image_urls` (List[str]): Список URL картинок товара.
- `product_title` (str): Название товара.
- `product_video_url` (str): Ссылка на видео товара.
- `promotion_link` (str): Ссылка на промоакцию товара.
- `relevant_market_commission_rate` (str): Комиссия за продажу на релевантном рынке.
- `sale_price` (str): Цена продажи.
- `sale_price_currency` (str): Валюта цены продажи.
- `second_level_category_id` (int): Идентификатор категории второго уровня.
- `second_level_category_name` (str): Название категории второго уровня.
- `shop_id` (int): Идентификатор магазина.
- `shop_url` (str): Ссылка на магазин.
- `target_app_sale_price` (str): Целевая цена продажи в приложении.
- `target_app_sale_price_currency` (str): Валюта целевой цены продажи в приложении.
- `target_original_price` (str): Целевая оригинальная цена.
- `target_original_price_currency` (str): Валюта целевой оригинальной цены.
- `target_sale_price` (str): Целевая цена продажи.
- `target_sale_price_currency` (str): Валюта целевой цены продажи.

**Примеры**:

```python
from src.suppliers.aliexpress.api.models.product import Product

product = Product(
    app_sale_price='10.00',
    app_sale_price_currency='USD',
    commission_rate='0.1',
    discount='10%',
    evaluate_rate='4.5',
    first_level_category_id=12345,
    first_level_category_name='Electronics',
    lastest_volume=100,
    hot_product_commission_rate='0.2',
    lastest_volume=100,
    original_price='15.00',
    original_price_currency='USD',
    product_detail_url='https://www.aliexpress.com/item/1234567890.html',
    product_id=1234567890,
    product_main_image_url='https://img.alicdn.com/imgextra/i4/6000000000000/O1CN01H36N8F2s4015c.jpg',
    product_small_image_urls=['https://img.alicdn.com/imgextra/i4/6000000000000/O1CN01H36N8F2s4015c.jpg'],
    product_title='Smartphone',
    product_video_url='https://www.youtube.com/watch?v=1234567890',
    promotion_link='https://www.aliexpress.com/promotion/1234567890.html',
    relevant_market_commission_rate='0.15',
    sale_price='12.00',
    sale_price_currency='USD',
    second_level_category_id=567890,
    second_level_category_name='Phones & Telecommunications',
    shop_id=9876543210,
    shop_url='https://www.aliexpress.com/store/9876543210',
    target_app_sale_price='11.00',
    target_app_sale_price_currency='USD',
    target_original_price='16.00',
    target_original_price_currency='USD',
    target_sale_price='13.00',
    target_sale_price_currency='USD',
)

print(product.product_title)
print(product.sale_price)