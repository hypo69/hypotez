# Модуль `pricelist`

## Обзор

Модуль `pricelist` предназначен для работы с запросами списка цен в PrestaShop. Он включает в себя класс `PriceListRequester`, который позволяет запрашивать цены на товары, обновлять источник данных и изменять цены товаров. Модуль использует API PrestaShop для взаимодействия с данными.

## Подробнее

Этот модуль является частью системы `hypotez` и используется для интеграции с PrestaShop. Он предоставляет функциональность для автоматизированного получения и изменения цен товаров в PrestaShop, что может быть полезно для автоматизации процессов ценообразования и синхронизации данных о товарах.

## Классы

### `PriceListRequester`

**Описание**: Класс `PriceListRequester` предназначен для запроса списка цен в PrestaShop. Он наследуется от класса `PrestaShop` и предоставляет методы для запроса цен на товары, обновления источника данных и изменения цен товаров.

**Наследует**:
- `PrestaShop`: Базовый класс для работы с API PrestaShop.

**Атрибуты**:
- Отсутствуют явно объявленные атрибуты, но класс использует атрибуты, унаследованные от `PrestaShop`, такие как `api_domain` и `api_key`.

**Принцип работы**:
1.  Класс инициализируется с учетными данными API PrestaShop.
2.  Метод `request_prices` используется для получения цен на товары.
3.  Метод `update_source` используется для обновления источника данных.
4.  Метод `modify_product_price` используется для изменения цен товаров.

**Методы**:

*   `__init__(self, api_credentials: Dict[str, str]) -> None`
*   `request_prices(self, products: List[str]) -> Dict[str, float]`
*   `update_source(self, new_source: str) -> None`
*   `modify_product_price(self, product: str, new_price: float) -> None`

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
```

**Описание**: Инициализирует объект класса `PriceListRequester`.

**Параметры**:
- `api_credentials` (Dict[str, str]): Словарь с учетными данными для API, включающий `'api_domain'` и `'api_key'`.

**Пример**:

```python
api_credentials = {'api_domain': 'example.com', 'api_key': 'your_api_key'}
price_requester = PriceListRequester(api_credentials)
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
```

**Описание**: Запрашивает список цен для указанных товаров.

**Параметры**:
- `products` (List[str]): Список товаров, для которых требуется получить цены.

**Возвращает**:
- `Dict[str, float]`: Словарь, где ключами являются товары, а значениями - их цены. Например: `{'product1': 10.99, 'product2': 5.99}`.

**Пример**:

```python
api_credentials = {'api_domain': 'example.com', 'api_key': 'your_api_key'}
price_requester = PriceListRequester(api_credentials)
products = ['product1', 'product2']
prices = price_requester.request_prices(products)
print(prices)
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
```

**Описание**: Обновляет источник данных для запроса цен.

**Параметры**:
- `new_source` (str): Новый источник данных.

**Пример**:

```python
api_credentials = {'api_domain': 'example.com', 'api_key': 'your_api_key'}
price_requester = PriceListRequester(api_credentials)
new_source = 'new_data_source'
price_requester.update_source(new_source)
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
```

**Описание**: Модифицирует цену указанного товара.

**Параметры**:
- `product` (str): Название товара.
- `new_price` (float): Новая цена товара.

**Пример**:

```python
api_credentials = {'api_domain': 'example.com', 'api_key': 'your_api_key'}
price_requester = PriceListRequester(api_credentials)
product = 'product1'
new_price = 12.99
price_requester.modify_product_price(product, new_price)
```