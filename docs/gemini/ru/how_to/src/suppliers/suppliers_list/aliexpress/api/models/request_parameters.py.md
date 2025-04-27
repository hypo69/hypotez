## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет три класса, которые используются для хранения типов данных для запросов к API AliExpress: `ProductType`, `SortBy` и `LinkType`.

Шаги выполнения
-------------------------
1. Класс `ProductType` определяет типы товаров, которые можно получить с помощью API AliExpress.
   - `ALL`: возвращает все товары.
   - `PLAZA`: возвращает товары с AliExpress Plaza.
   - `TMALL`: возвращает товары с AliExpress TMALL.
2. Класс `SortBy` определяет способы сортировки результатов запроса.
   - `SALE_PRICE_ASC`: сортирует товары по возрастанию цены.
   - `SALE_PRICE_DESC`: сортирует товары по убыванию цены.
   - `LAST_VOLUME_ASC`: сортирует товары по возрастанию последнего объема продаж.
   - `LAST_VOLUME_DESC`: сортирует товары по убыванию последнего объема продаж.
3. Класс `LinkType` определяет тип ссылки на товар.
   - `NORMAL`: обычная ссылка на товар.
   - `HOTLINK`: "горячая" ссылка на товар, которая может быть использована для отслеживания кликов.

Пример использования
-------------------------

```python
from src.suppliers.aliexpress.api.models.request_parameters import ProductType, SortBy, LinkType

# Устанавливаем тип товара как "TMALL"
product_type = ProductType.TMALL

# Устанавливаем способ сортировки как "SALE_PRICE_DESC"
sort_by = SortBy.SALE_PRICE_DESC

# Устанавливаем тип ссылки как "HOTLINK"
link_type = LinkType.HOTLINK

# Передаем эти параметры в функцию запроса API AliExpress
response = get_aliexpress_products(product_type=product_type, sort_by=sort_by, link_type=link_type)
```