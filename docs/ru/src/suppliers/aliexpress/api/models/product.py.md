# Модуль `product`

## Обзор

Модуль `product` содержит класс `Product`, который представляет модель данных товара с AliExpress. Эта модель включает в себя различные атрибуты, такие как цены, валюты, ссылки, идентификаторы и другую информацию о продукте. Модуль предназначен для организации и структурирования данных о товарах, получаемых через API AliExpress.

## Подробней

Этот модуль определяет структуру данных для представления информации о товаре, полученной через API AliExpress. Класс `Product` служит контейнером для хранения различных атрибутов товара, таких как цены, валюты, URL-адреса и идентификаторы. Он помогает стандартизировать способ обработки данных о товарах в проекте `hypotez`.

## Классы

### `Product`

**Описание**: Класс `Product` предназначен для хранения информации о товаре с AliExpress.

**Наследует**:

Нет наследования.

**Атрибуты**:

- `app_sale_price` (str): Цена товара в приложении со скидкой.
- `app_sale_price_currency` (str): Валюта цены товара в приложении со скидкой.
- `commission_rate` (str): Комиссионные отчисления.
- `discount` (str): Размер скидки на товар.
- `evaluate_rate` (str): Рейтинг товара.
- `first_level_category_id` (int): Идентификатор категории первого уровня.
- `first_level_category_name` (str): Название категории первого уровня.
- `lastest_volume` (int): Последний объем продаж товара.
- `hot_product_commission_rate` (str): Комиссионные отчисления для горячих товаров.
- `original_price` (str): Оригинальная цена товара.
- `original_price_currency` (str): Валюта оригинальной цены товара.
- `product_detail_url` (str): URL-адрес страницы с подробным описанием товара.
- `product_id` (int): Идентификатор товара.
- `product_main_image_url` (str): URL-адрес основного изображения товара.
- `product_small_image_urls` (List[str]): Список URL-адресов маленьких изображений товара.
- `product_title` (str): Заголовок товара.
- `product_video_url` (str): URL-адрес видео товара.
- `promotion_link` (str): Ссылка на промоакцию товара.
- `relevant_market_commission_rate` (str): Комиссионные отчисления для конкретного рынка.
- `sale_price` (str): Цена товара со скидкой.
- `sale_price_currency` (str): Валюта цены товара со скидкой.
- `second_level_category_id` (int): Идентификатор категории второго уровня.
- `second_level_category_name` (str): Название категории второго уровня.
- `shop_id` (int): Идентификатор магазина.
- `shop_url` (str): URL-адрес магазина.
- `target_app_sale_price` (str): Целевая цена товара в приложении со скидкой.
- `target_app_sale_price_currency` (str): Валюта целевой цены товара в приложении со скидкой.
- `target_original_price` (str): Целевая оригинальная цена товара.
- `target_original_price_currency` (str): Валюта целевой оригинальной цены товара.
- `target_sale_price` (str): Целевая цена товара со скидкой.
- `target_sale_price_currency` (str): Валюта целевой цены товара со скидкой.

**Принцип работы**:

Класс `Product` служит контейнером для хранения данных о товаре. Каждый атрибут класса представляет собой характеристику товара, полученную из API AliExpress.

## Методы класса

В классе `Product` отсутствуют методы. Он используется только для хранения данных.

## Параметры класса

- `app_sale_price` (str): Цена товара в приложении со скидкой.
- `app_sale_price_currency` (str): Валюта цены товара в приложении со скидкой.
- `commission_rate` (str): Комиссионные отчисления.
- `discount` (str): Размер скидки на товар.
- `evaluate_rate` (str): Рейтинг товара.
- `first_level_category_id` (int): Идентификатор категории первого уровня.
- `first_level_category_name` (str): Название категории первого уровня.
- `lastest_volume` (int): Последний объем продаж товара.
- `hot_product_commission_rate` (str): Комиссионные отчисления для горячих товаров.
- `original_price` (str): Оригинальная цена товара.
- `original_price_currency` (str): Валюта оригинальной цены товара.
- `product_detail_url` (str): URL-адрес страницы с подробным описанием товара.
- `product_id` (int): Идентификатор товара.
- `product_main_image_url` (str): URL-адрес основного изображения товара.
- `product_small_image_urls` (List[str]): Список URL-адресов маленьких изображений товара.
- `product_title` (str): Заголовок товара.
- `product_video_url` (str): URL-адрес видео товара.
- `promotion_link` (str): Ссылка на промоакцию товара.
- `relevant_market_commission_rate` (str): Комиссионные отчисления для конкретного рынка.
- `sale_price` (str): Цена товара со скидкой.
- `sale_price_currency` (str): Валюта цены товара со скидкой.
- `second_level_category_id` (int): Идентификатор категории второго уровня.
- `second_level_category_name` (str): Название категории второго уровня.
- `shop_id` (int): Идентификатор магазина.
- `shop_url` (str): URL-адрес магазина.
- `target_app_sale_price` (str): Целевая цена товара в приложении со скидкой.
- `target_app_sale_price_currency` (str): Валюта целевой цены товара в приложении со скидкой.
- `target_original_price` (str): Целевая оригинальная цена товара.
- `target_original_price_currency` (str): Валюта целевой оригинальной цены товара.
- `target_sale_price` (str): Целевая цена товара со скидкой.
- `target_sale_price_currency` (str): Валюта целевой цены товара со скидкой.

**Примеры**:

```python
product = Product()
product.product_id = 123456789
product.product_title = "Example Product"
product.sale_price = "19.99"
product.sale_price_currency = "USD"