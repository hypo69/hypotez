# Модуль `pricelist`

## Обзор

Модуль `pricelist` предназначен для работы с запросами списка цен PrestaShop. Он предоставляет класс `PriceListRequester`, который позволяет запрашивать цены для указанных товаров, обновлять источник данных для запроса цен и изменять цену товара.

## Подробней

Модуль содержит класс `PriceListRequester`, который наследует класс `PrestaShop` из модуля `api`. `PriceListRequester` использует учетные данные API (домен и ключ) для взаимодействия с PrestaShop. Он позволяет запрашивать цены товаров, обновлять источник данных и изменять цены товаров.

## Классы

### `PriceListRequester`

**Описание**: Класс для запроса списка цен из PrestaShop.

**Наследует**:
- `PrestaShop`: Базовый класс для работы с API PrestaShop.

**Атрибуты**:
- Нет явных атрибутов, кроме тех, что наследуются от `PrestaShop`.

**Методы**:
- `__init__`: Инициализирует объект класса.
- `request_prices`: Запрашивает список цен для указанных товаров.
- `update_source`: Обновляет источник данных для запроса цен.
- `modify_product_price`: Модифицирует цену указанного товара.

**Принцип работы**:
Класс `PriceListRequester` предназначен для получения и изменения цен товаров в PrestaShop. Он инициализируется с использованием учетных данных API, после чего можно запрашивать цены, обновлять источник данных и модифицировать цены товаров.

## Методы класса

### `__init__`

```python
def __init__(self, api_credentials: Dict[str, str]) -> None:
    """
    Инициализирует объект класса PriceListRequester.

    Args:
        api_credentials (Dict[str, str]): Словарь с учетными данными для API,
            включая 'api_domain' и 'api_key'.

    Returns:
        None
    """
    ...
```

**Назначение**: Инициализирует объект класса `PriceListRequester`.

**Параметры**:
- `api_credentials` (Dict[str, str]): Словарь с учетными данными API, содержащий ключи `'api_domain'` и `'api_key'`.

**Возвращает**:
- `None`

**Как работает функция**:
Функция `__init__` инициализирует объект `PriceListRequester`, вызывая конструктор базового класса `PrestaShop` с переданными учетными данными API. Это позволяет установить соединение с API PrestaShop для дальнейших операций.

**Примеры**:
```python
api_credentials = {'api_domain': 'example.com', 'api_key': 'your_api_key'}
pricelist_requester = PriceListRequester(api_credentials)
```

### `request_prices`

```python
def request_prices(self, products: List[str]) -> Dict[str, float]:
    """
    Запрашивает список цен для указанных товаров.

    Args:
        products (List[str]): Список товаров, для которых требуется получить цены.

    Returns:
        Dict[str, float]: Словарь, где ключами являются товары, а значениями - их цены.
            Например: {'product1': 10.99, 'product2': 5.99}
    """
    ...
```

**Назначение**: Запрашивает список цен для указанных товаров.

**Параметры**:
- `products` (List[str]): Список товаров, для которых требуется получить цены.

**Возвращает**:
- `Dict[str, float]`: Словарь, где ключами являются товары, а значениями - их цены.

**Как работает функция**:
Функция `request_prices` отправляет запрос на получение цен из источника данных для каждого товара в списке `products`. Возвращает словарь, содержащий цены для каждого товара. В текущей реализации возвращает пустой словарь.

**Примеры**:
```python
api_credentials = {'api_domain': 'example.com', 'api_key': 'your_api_key'}
pricelist_requester = PriceListRequester(api_credentials)
products = ['product1', 'product2', 'product3']
prices = pricelist_requester.request_prices(products)
print(prices)  # Output: {}
```

### `update_source`

```python
def update_source(self, new_source: str) -> None:
    """
    Обновляет источник данных для запроса цен.

    Args:
        new_source (str): Новый источник данных.

    Returns:
        None
    """
    ...
```

**Назначение**: Обновляет источник данных для запроса цен.

**Параметры**:
- `new_source` (str): Новый источник данных.

**Возвращает**:
- `None`

**Как работает функция**:
Функция `update_source` устанавливает новое значение атрибута `source` объекта `PriceListRequester` на переданный `new_source`. Это позволяет изменить источник данных, из которого запрашиваются цены.

**Примеры**:
```python
api_credentials = {'api_domain': 'example.com', 'api_key': 'your_api_key'}
pricelist_requester = PriceListRequester(api_credentials)
new_source = 'new_data_source'
pricelist_requester.update_source(new_source)
```

### `modify_product_price`

```python
def modify_product_price(self, product: str, new_price: float) -> None:
    """
    Модифицирует цену указанного товара.

    Args:
        product (str): Название товара.
        new_price (float): Новая цена товара.

    Returns:
        None
    """
    ...
```

**Назначение**: Модифицирует цену указанного товара.

**Параметры**:
- `product` (str): Название товара.
- `new_price` (float): Новая цена товара.

**Возвращает**:
- `None`

**Как работает функция**:
Функция `modify_product_price` изменяет цену товара в источнике данных. В текущей реализации функция ничего не делает (`...`).

**Примеры**:
```python
api_credentials = {'api_domain': 'example.com', 'api_key': 'your_api_key'}
pricelist_requester = PriceListRequester(api_credentials)
product = 'product1'
new_price = 12.99
pricelist_requester.modify_product_price(product, new_price)
```