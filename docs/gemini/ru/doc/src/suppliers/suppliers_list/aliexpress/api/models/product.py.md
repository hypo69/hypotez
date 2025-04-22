# Модуль `product.py`

## Обзор

Модуль определяет структуру данных для представления информации о товаре с платформы AliExpress. Он содержит класс `Product`, который включает в себя различные атрибуты, такие как цена, валюта, рейтинг, URL и другие детали, характеризующие товар.

## Подробней

Модуль предназначен для унификации данных о товарах, получаемых через API AliExpress, и предоставляет удобный способ доступа к этим данным. Он определяет структуру данных, которая используется для хранения и передачи информации о товарах между различными компонентами системы.

## Классы

### `Product`

**Описание**: Класс представляет собой модель данных для хранения информации о товаре с AliExpress.

**Атрибуты**:
- `app_sale_price` (str): Цена товара в приложении.
- `app_sale_price_currency` (str): Валюта цены товара в приложении.
- `commission_rate` (str): Комиссионные отчисления.
- `discount` (str): Размер скидки на товар.
- `evaluate_rate` (str): Рейтинг товара.
- `first_level_category_id` (int): ID категории первого уровня.
- `first_level_category_name` (str): Название категории первого уровня.
- `lastest_volume` (int): Объем продаж за последнее время.
- `hot_product_commission_rate` (str): Комиссионные отчисления для популярных товаров.
- `original_price` (str): Оригинальная цена товара.
- `original_price_currency` (str): Валюта оригинальной цены товара.
- `product_detail_url` (str): URL страницы с детальным описанием товара.
- `product_id` (int): ID товара.
- `product_main_image_url` (str): URL главного изображения товара.
- `product_small_image_urls` (List[str]): Список URL маленьких изображений товара.
- `product_title` (str): Название товара.
- `product_video_url` (str): URL видео товара.
- `promotion_link` (str): Ссылка на промоакцию товара.
- `relevant_market_commission_rate` (str): Комиссионные отчисления для соответствующего рынка.
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

**Принцип работы**:
Класс `Product` служит контейнером для хранения информации о товаре. Он не содержит методов для обработки данных, а только атрибуты, представляющие различные характеристики товара.

**Примеры**:
Пример создания экземпляра класса `Product` и доступа к его атрибутам:

```python
from src.suppliers.suppliers_list.aliexpress.api.models import Product

product = Product()
product.product_title = "Example Product"
product.sale_price = "10.00"
print(product.product_title, product.sale_price)  # Вывод: Example Product 10.00