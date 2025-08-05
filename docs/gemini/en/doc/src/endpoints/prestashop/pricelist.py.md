# Модуль для работы с запросами списка цен PrestaShop
===============================================================

Модуль содержит класс `PriceListRequester`, который используется для взаимодействия с API PrestaShop и запроса цен для товаров.

## Содержание

- [Описание](#описание)
- [Классы](#классы)
    - [PriceListRequester](#pricelistequester)
- [Функции](#функции)

## Описание

Этот модуль обеспечивает функциональность для получения и обновления цен на товары с использованием API PrestaShop. Он включает в себя класс `PriceListRequester`, который инкапсулирует логику запросов цен и управления источником данных.

## Классы

### `PriceListRequester`

**Описание**: Класс для запроса списка цен.

**Наследуется от**: `PrestaShop` (базовый класс для работы с API PrestaShop)

**Атрибуты**:

- `api_credentials` (Dict[str, str]): Словарь с учетными данными для API, включая `api_domain` и `api_key`.

**Методы**:

- `__init__(self, api_credentials: Dict[str, str]) -> None`: Инициализирует объект класса `PriceListRequester`.
- `request_prices(self, products: List[str]) -> Dict[str, float]`: Запрашивает список цен для указанных товаров.
- `update_source(self, new_source: str) -> None`: Обновляет источник данных для запроса цен.
- `modify_product_price(self, product: str, new_price: float) -> None`: Модифицирует цену указанного товара.

#### `__init__(self, api_credentials: Dict[str, str]) -> None`

**Описание**: Инициализирует объект класса `PriceListRequester`.

**Параметры**:

- `api_credentials` (Dict[str, str]): Словарь с учетными данными для API, включая `api_domain` и `api_key`.

**Возвращает**:

- `None`

#### `request_prices(self, products: List[str]) -> Dict[str, float]`

**Описание**: Запрашивает список цен для указанных товаров.

**Параметры**:

- `products` (List[str]): Список товаров, для которых требуется получить цены.

**Возвращает**:

- `Dict[str, float]`: Словарь, где ключами являются товары, а значениями - их цены. 
    Например: `{'product1': 10.99, 'product2': 5.99}`

#### `update_source(self, new_source: str) -> None`

**Описание**: Обновляет источник данных для запроса цен.

**Параметры**:

- `new_source` (str): Новый источник данных.

**Возвращает**:

- `None`

#### `modify_product_price(self, product: str, new_price: float) -> None`

**Описание**: Модифицирует цену указанного товара.

**Параметры**:

- `product` (str): Название товара.
- `new_price` (float): Новая цена товара.

**Возвращает**:

- `None`

## Функции

В этом модуле нет дополнительных функций.