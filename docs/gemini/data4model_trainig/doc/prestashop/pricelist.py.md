# Модуль для работы со списком цен PrestaShop

## Обзор

Модуль `src.endpoints.prestashop.pricelist` предназначен для работы с запросами списка цен PrestaShop.

## Подробней

Модуль предоставляет класс `PriceListRequester` для запроса и обновления цен товаров в PrestaShop.

## Классы

### `PriceListRequester`

**Описание**: Класс для запроса списка цен.

**Наследует**:

*   `PrestaShop`: Предоставляет базовые методы для работы с API PrestaShop.

**Атрибуты**:

*   Нет явно определенных атрибутов, но наследует атрибуты от класса `PrestaShop`, такие как `api_key` и `api_domain`.

**Методы**:

*   `__init__(self, api_credentials: Dict[str, str]) -> None`: Инициализирует объект класса `PriceListRequester`.
*   `request_prices(self, products: List[str]) -> Dict[str, float]`: Запрашивает список цен для указанных товаров.
*   `update_source(self, new_source: str) -> None`: Обновляет источник данных для запроса цен.
*   `modify_product_price(self, product: str, new_price: float) -> None`: Модифицирует цену указанного товара.

## Методы класса `PriceListRequester`

### `__init__`

```python
def __init__(self, api_credentials: Dict[str, str]) -> None:
```

**Назначение**: Инициализирует объект класса `PriceListRequester`.

**Параметры**:

*   `api_credentials` (Dict[str, str]): Словарь с учетными данными для API, включающий `'api_domain'` и `'api_key'`.

**Как работает функция**:

1.  Вызывает конструктор родительского класса `PrestaShop` с переданными учетными данными API.

### `request_prices`

```python
def request_prices(self, products: List[str]) -> Dict[str, float]:
```

**Назначение**: Запрашивает список цен для указанных товаров.

**Параметры**:

*   `products` (List[str]): Список товаров, для которых требуется получить цены.

**Возвращает**:

*   `Dict[str, float]`: Словарь, где ключами являются товары, а значениями - их цены. Например: `{'product1': 10.99, 'product2': 5.99}`

**Как работает функция**:

1.  В настоящее время содержит только заглушку `...` и возвращает пустой словарь. В реальной реализации должен отправлять запрос на получение цен из источника данных и возвращать полученные цены в виде словаря.

### `update_source`

```python
def update_source(self, new_source: str) -> None:
```

**Назначение**: Обновляет источник данных для запроса цен.

**Параметры**:

*   `new_source` (str): Новый источник данных.

**Как работает функция**:

1.  Обновляет значение атрибута `source` объекта класса `PriceListRequester` новым источником данных.

### `modify_product_price`

```python
def modify_product_price(self, product: str, new_price: float) -> None:
```

**Назначение**: Модифицирует цену указанного товара.

**Параметры**:

*   `product` (str): Название товара.
*   `new_price` (float): Новая цена товара.

**Как работает функция**:

1.  В настоящее время содержит только заглушку `...`. В реальной реализации должен изменять цену товара в источнике данных.