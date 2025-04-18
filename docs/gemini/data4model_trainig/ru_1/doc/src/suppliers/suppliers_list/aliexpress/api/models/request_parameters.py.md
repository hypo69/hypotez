# Модуль: src.suppliers.suppliers_list.aliexpress.api.models

## Обзор

Модуль содержит классы, определяющие типы продуктов, способы сортировки и типы ссылок, используемые в API для работы с AliExpress.

## Подробнее

Этот модуль предоставляет набор констант, которые используются для формирования запросов к API AliExpress. Он определяет возможные значения для фильтрации и сортировки результатов поиска товаров.
Эти константы позволяют разработчикам единообразно и безошибочно указывать параметры запроса, избегая опечаток и несовместимости.
Модуль предназначен для использования внутри проекта `hypotez` для обеспечения взаимодействия с API AliExpress.

## Классы

### `ProductType`

**Описание**: Класс, определяющий типы продуктов, которые могут быть запрошены через API AliExpress.

**Атрибуты**:
- `ALL` (str):  Представляет все типы продуктов.
- `PLAZA` (str):  Представляет продукты, доступные на AliExpress Plaza.
- `TMALL` (str):  Представляет продукты, доступные на Tmall.

**Принцип работы**:
Класс `ProductType` предоставляет константы, которые могут быть использованы при формировании запросов к API AliExpress для фильтрации товаров по типу. Например, можно запросить только товары из Tmall, установив параметр `ProductType.TMALL`.

### `SortBy`

**Описание**: Класс, определяющий способы сортировки результатов поиска товаров.

**Атрибуты**:
- `SALE_PRICE_ASC` (str):  Сортировка по возрастанию цены товара.
- `SALE_PRICE_DESC` (str): Сортировка по убыванию цены товара.
- `LAST_VOLUME_ASC` (str): Сортировка по возрастанию объема продаж.
- `LAST_VOLUME_DESC` (str): Сортировка по убыванию объема продаж.

**Принцип работы**:
Класс `SortBy` предоставляет константы, которые могут быть использованы при формировании запросов к API AliExpress для сортировки результатов поиска товаров. Например, можно отсортировать товары по убыванию цены, установив параметр `SortBy.SALE_PRICE_DESC`.

### `LinkType`

**Описание**: Класс, определяющий типы ссылок, используемые в API AliExpress.

**Атрибуты**:
- `NORMAL` (int):  Представляет обычную ссылку.
- `HOTLINK` (int):  Представляет партнерскую ссылку.

**Принцип работы**:
Класс `LinkType` предоставляет константы, которые могут быть использованы при формировании запросов к API AliExpress для указания типа ссылки, которую необходимо получить. Например, можно запросить партнерскую ссылку, установив параметр `LinkType.HOTLINK`.