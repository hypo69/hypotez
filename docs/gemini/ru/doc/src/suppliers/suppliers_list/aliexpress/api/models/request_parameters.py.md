# Модуль `request_parameters`

## Обзор

Модуль `request_parameters` содержит классы, определяющие типы параметров запросов к API AliExpress.

## Подробнее

Данный модуль используется для управления типом продукта, сортировкой и типом ссылки в запросах к API AliExpress. Он предоставляет набор классов, каждый из которых определяет константы, представляющие различные варианты параметров запроса.

## Классы

### `ProductType`

**Описание**: Класс `ProductType` определяет типы продуктов для запросов к API AliExpress.

**Атрибуты**:

- `ALL` (str): Все типы продуктов.
- `PLAZA` (str): Продукты с площадки PLAZA.
- `TMALL` (str): Продукты с площадки TMALL.

### `SortBy`

**Описание**: Класс `SortBy` определяет типы сортировки результатов запросов к API AliExpress.

**Атрибуты**:

- `SALE_PRICE_ASC` (str): Сортировка по цене продажи по возрастанию.
- `SALE_PRICE_DESC` (str): Сортировка по цене продажи по убыванию.
- `LAST_VOLUME_ASC` (str): Сортировка по объему продаж по возрастанию.
- `LAST_VOLUME_DESC` (str): Сортировка по объему продаж по убыванию.

### `LinkType`

**Описание**: Класс `LinkType` определяет типы ссылок, которые могут быть получены в результатах запросов к API AliExpress.

**Атрибуты**:

- `NORMAL` (int): Обычная ссылка.
- `HOTLINK` (int): "Горячая" ссылка.

## Примеры

**Пример использования классов:**

```python
from src.suppliers.aliexpress.api.models.request_parameters import ProductType, SortBy, LinkType

product_type = ProductType.ALL
sort_by = SortBy.SALE_PRICE_DESC
link_type = LinkType.NORMAL
```