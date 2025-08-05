# Модуль: src.endpoints.prestashop.pricelist

## Обзор

Модуль `pricelist` предназначен для работы с запросами списка цен в PrestaShop. Он предоставляет функциональность для запроса цен на товары и обновления источника данных.

## Подробнее

Модуль содержит класс `PriceListRequester`, который наследует от `PrestaShop` и предоставляет методы для запроса цен на товары, обновления источника данных и модификации цен товаров.

## Классы

### `PriceListRequester(PrestaShop)`

**Описание**: Класс для запроса списка цен PrestaShop.

**Наследует**:
- `PrestaShop`: Базовый класс для работы с API PrestaShop.

**Атрибуты**:
- Нет специфических атрибутов, кроме унаследованных от `PrestaShop`.

**Методы**:
- `__init__(api_credentials: Dict[str, str]) -> None`
- `request_prices(products: List[str]) -> Dict[str, float]`
- `update_source(new_source: str) -> None`
- `modify_product_price(product: str, new_price: float) -> None`

### `__init__(api_credentials: Dict[str, str]) -> None`

**Назначение**: Инициализирует объект класса `PriceListRequester`.

**Параметры**:
- `api_credentials` (Dict[str, str]): Словарь с учетными данными для API, включающий `'api_domain'` и `'api_key'`.

**Возвращает**:
- `None`

**Как работает функция**:
- Функция инициализирует объект класса `PriceListRequester`, вызывая конструктор базового класса `PrestaShop` с учетными данными API (`api_domain` и `api_key`).

**Примеры**:

```python
api_credentials = {'api_domain': 'your_api_domain', 'api_key': 'your_api_key'}
pricelist_requester = PriceListRequester(api_credentials)
```

### `request_prices(products: List[str]) -> Dict[str, float]`

**Назначение**: Запрашивает список цен для указанных товаров.

**Параметры**:
- `products` (List[str]): Список товаров, для которых требуется получить цены.

**Возвращает**:
- `Dict[str, float]`: Словарь, где ключами являются товары, а значениями - их цены. Например: `{'product1': 10.99, 'product2': 5.99}`

**Как работает функция**:
- Функция отправляет запрос на получение цен из источника данных для каждого товара в списке `products`. Возвращает словарь с ценами товаров.
- В текущей реализации функция возвращает пустой словарь `{}`.

**Примеры**:

```python
products = ['product1', 'product2', 'product3']
prices = pricelist_requester.request_prices(products)
print(prices)  # Output: {}
```

### `update_source(new_source: str) -> None`

**Назначение**: Обновляет источник данных для запроса цен.

**Параметры**:
- `new_source` (str): Новый источник данных.

**Возвращает**:
- `None`

**Как работает функция**:
- Функция обновляет атрибут `source` объекта `PriceListRequester` новым источником данных `new_source`.

**Примеры**:

```python
pricelist_requester.update_source('new_data_source')
```

### `modify_product_price(product: str, new_price: float) -> None`

**Назначение**: Модифицирует цену указанного товара.

**Параметры**:
- `product` (str): Название товара.
- `new_price` (float): Новая цена товара.

**Возвращает**:
- `None`

**Как работает функция**:
- Функция изменяет цену товара в источнике данных на новое значение `new_price`.
- В текущей реализации функция содержит заготовку `...`, указывающую на отсутствие реализации.

**Примеры**:

```python
pricelist_requester.modify_product_price('product1', 12.99)