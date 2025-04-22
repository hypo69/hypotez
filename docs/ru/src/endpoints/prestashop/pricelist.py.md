# Модуль: src.endpoints.prestashop.pricelist

## Обзор

Модуль `src.endpoints.prestashop.pricelist` предназначен для работы с запросами списка цен PrestaShop. Он предоставляет класс `PriceListRequester`, который позволяет запрашивать и обновлять цены товаров через API PrestaShop.

## Подробней

Этот модуль обеспечивает функциональность для взаимодействия с API PrestaShop с целью получения актуальной информации о ценах товаров. Он включает в себя возможность инициализации с учетными данными API, запроса цен для списка товаров, обновления источника данных и модификации цен отдельных товаров.

## Классы

### `PriceListRequester(PrestaShop)`

**Описание**: Класс `PriceListRequester` предназначен для запроса списка цен товаров из PrestaShop. Он наследует функциональность базового класса `PrestaShop` для упрощения взаимодействия с API PrestaShop.

**Наследует**:
- `PrestaShop`: Базовый класс, предоставляющий общую функциональность для работы с API PrestaShop.

**Атрибуты**:
- Отсутствуют явно определенные атрибуты, но используются атрибуты, унаследованные от класса `PrestaShop`, такие как `api_domain` и `api_key`.

**Методы**:
- `__init__(api_credentials: Dict[str, str]) -> None`: Инициализирует объект класса `PriceListRequester`.
- `request_prices(products: List[str]) -> Dict[str, float]`: Запрашивает список цен для указанных товаров.
- `update_source(new_source: str) -> None`: Обновляет источник данных для запроса цен.
- `modify_product_price(product: str, new_price: float) -> None`: Модифицирует цену указанного товара.

### `__init__(api_credentials: Dict[str, str]) -> None`

**Назначение**: Инициализация объекта класса `PriceListRequester` с передачей учетных данных API.

**Параметры**:
- `api_credentials` (Dict[str, str]): Словарь, содержащий учетные данные для доступа к API PrestaShop, включая `api_domain` (домен API) и `api_key` (ключ API).

**Возвращает**:
- `None`

**Как работает функция**:
- Функция вызывает конструктор базового класса `PrestaShop`, передавая ему домен и ключ API из предоставленного словаря `api_credentials`. Это необходимо для настройки аутентификации и соединения с API PrestaShop.

**Примеры**:
```python
api_credentials = {'api_domain': 'your_prestashop_domain.com', 'api_key': 'your_api_key'}
pricelist_requester = PriceListRequester(api_credentials)
```

### `request_prices(products: List[str]) -> Dict[str, float]`

**Назначение**: Запрашивает цены для списка товаров из API PrestaShop.

**Параметры**:
- `products` (List[str]): Список названий товаров, для которых требуется получить цены.

**Возвращает**:
- `Dict[str, float]`: Словарь, где ключами являются названия товаров, а значениями - соответствующие цены. Возвращает пустой словарь, если цены не были получены.

**Как работает функция**:
-  Функция отправляет запрос к API PrestaShop для получения цен на товары, указанные в списке `products`. Возвращает словарь, где каждому товару сопоставлена его цена. В текущей реализации возвращается пустой словарь.

**Примеры**:
```python
products = ['product1', 'product2', 'product3']
prices = pricelist_requester.request_prices(products)
print(prices)  # Output: {}
```

### `update_source(new_source: str) -> None`

**Назначение**: Обновляет источник данных, из которого запрашиваются цены.

**Параметры**:
- `new_source` (str): Новый источник данных для получения цен.

**Возвращает**:
- `None`

**Как работает функция**:
- Функция изменяет значение атрибута `source` объекта `PriceListRequester` на `new_source`. Это позволяет переключиться на другой источник данных для получения цен, например, другой API endpoint или базу данных.

**Примеры**:
```python
pricelist_requester.update_source('new_data_source')
```

### `modify_product_price(product: str, new_price: float) -> None`

**Назначение**: Изменяет цену указанного товара в источнике данных.

**Параметры**:
- `product` (str): Название товара, цену которого необходимо изменить.
- `new_price` (float): Новая цена товара.

**Возвращает**:
- `None`

**Как работает функция**:
- Функция отправляет запрос к API PrestaShop для изменения цены товара `product` на значение `new_price`. В текущей реализации функция не выполняет никаких действий.

**Примеры**:
```python
pricelist_requester.modify_product_price('product1', 19.99)