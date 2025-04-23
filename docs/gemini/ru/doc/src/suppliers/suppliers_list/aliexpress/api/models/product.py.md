# Модуль `product`

## Обзор

Модуль `product` содержит класс `Product`, предназначенный для представления информации о товаре, полученной из API AliExpress. Класс содержит атрибуты, описывающие различные характеристики товара, такие как цены, скидки, ссылки, изображения и категории.

## Подробней

Этот модуль определяет структуру данных для хранения информации о товаре, полученной от API AliExpress. Он используется для унификации представления данных о товарах и облегчения доступа к различным параметрам товара. Данные включают в себя цены (обычные и акционные, в разных валютах), информацию о скидках, ссылки на изображения и детали товара, категории, а также информацию о магазине.

## Классы

### `Product`

**Описание**: Класс `Product` предназначен для хранения информации о товаре, полученной из API AliExpress.

**Атрибуты**:
- `app_sale_price` (str): Цена товара со скидкой для мобильного приложения.
- `app_sale_price_currency` (str): Валюта цены товара со скидкой для мобильного приложения.
- `commission_rate` (str): Комиссионные отчисления.
- `discount` (str): Размер скидки.
- `evaluate_rate` (str): Рейтинг товара.
- `first_level_category_id` (int): ID категории первого уровня.
- `first_level_category_name` (str): Название категории первого уровня.
- `lastest_volume` (int): Объем продаж за последнее время.
- `hot_product_commission_rate` (str): Комиссионные отчисления для "горячих" товаров.
- `original_price` (str): Оригинальная цена товара.
- `original_price_currency` (str): Валюта оригинальной цены товара.
- `product_detail_url` (str): URL страницы с детальным описанием товара.
- `product_id` (int): ID товара.
- `product_main_image_url` (str): URL главного изображения товара.
- `product_small_image_urls` (List[str]): Список URL маленьких изображений товара.
- `product_title` (str): Название товара.
- `product_video_url` (str): URL видео товара.
- `promotion_link` (str): Ссылка на промо-акцию товара.
- `relevant_market_commission_rate` (str): Комиссионные отчисления для релевантного рынка.
- `sale_price` (str): Цена товара со скидкой.
- `sale_price_currency` (str): Валюта цены товара со скидкой.
- `second_level_category_id` (int): ID категории второго уровня.
- `second_level_category_name` (str): Название категории второго уровня.
- `shop_id` (int): ID магазина.
- `shop_url` (str): URL магазина.
- `target_app_sale_price` (str): Целевая цена товара со скидкой для мобильного приложения.
- `target_app_sale_price_currency` (str): Валюта целевой цены товара со скидкой для мобильного приложения.
- `target_original_price` (str): Целевая оригинальная цена товара.
- `target_original_price_currency` (str): Валюта целевой оригинальной цены товара.
- `target_sale_price` (str): Целевая цена товара со скидкой.
- `target_sale_price_currency` (str): Валюта целевой цены товара со скидкой.

**Принцип работы**:

Класс `Product` служит контейнером для хранения данных о товаре. Он не содержит методов для обработки или изменения данных, а лишь предоставляет структуру для их хранения.

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