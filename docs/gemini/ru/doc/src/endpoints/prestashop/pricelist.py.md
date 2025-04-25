# Модуль для работы с запросами списка цен PrestaShop

## Обзор

Модуль предоставляет функциональность для взаимодействия с API PrestaShop с целью получения и обновления информации о ценах товаров. 

## Подробнее

Модуль `pricelist.py` содержит класс `PriceListRequester`, который наследует от базового класса `PrestaShop`. `PriceListRequester` используется для отправки запросов на получение списка цен для товаров, а также для изменения цен товаров в источнике данных. 

## Классы

### `PriceListRequester`

**Описание**: Класс для запроса списка цен. 

**Наследует**:  `PrestaShop` 

**Атрибуты**:

- `api_domain` (str): Домен API PrestaShop.
- `api_key` (str): Ключ API PrestaShop.
- `source` (str): Источник данных для запроса цен.

**Методы**:

- `__init__(self, api_credentials: Dict[str, str]) -> None`: Инициализирует объект класса `PriceListRequester`.
- `request_prices(self, products: List[str]) -> Dict[str, float]`: Запрашивает список цен для указанных товаров.
- `update_source(self, new_source: str) -> None`: Обновляет источник данных для запроса цен.
- `modify_product_price(self, product: str, new_price: float) -> None`: Модифицирует цену указанного товара.

**Принцип работы**:

Класс `PriceListRequester` использует методы базового класса `PrestaShop` для взаимодействия с API PrestaShop. 
- Метод `request_prices()` отправляет запрос на получение цен для указанных товаров.
- Метод `update_source()` обновляет источник данных для запроса цен.
- Метод `modify_product_price()` изменяет цену указанного товара в источнике данных. 

**Примеры**:

```python
# Создание объекта класса PriceListRequester
api_credentials = {'api_domain': 'your_prestashop_domain.com', 'api_key': 'your_api_key'}
price_list_requester = PriceListRequester(api_credentials)

# Запрос списка цен для товаров
products = ['product1', 'product2', 'product3']
prices = price_list_requester.request_prices(products)
print(prices)  # Вывод: {'product1': 10.99, 'product2': 5.99, 'product3': 19.99}

# Обновление источника данных
price_list_requester.update_source('new_source')

# Изменение цены товара
price_list_requester.modify_product_price('product1', 12.99)
```

## Методы класса

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
        # Здесь код для отправки запроса на получение цен из источника данных
        ...
        return {}
```

**Назначение**: Метод отправляет запрос на получение цен для указанных товаров.

**Параметры**:

- `products` (List[str]): Список товаров, для которых требуется получить цены.

**Возвращает**:

- `Dict[str, float]`: Словарь, где ключами являются товары, а значениями - их цены.

**Как работает функция**:

- Метод отправляет запрос на получение цен для указанных товаров из источника данных.
- Он использует методы базового класса `PrestaShop` для взаимодействия с API PrestaShop. 
- В текущем варианте функция возвращает пустой словарь, поскольку код для отправки запроса не указан. 

**Примеры**:

```python
products = ['product1', 'product2', 'product3']
prices = price_list_requester.request_prices(products)
print(prices)  # Вывод: {'product1': 10.99, 'product2': 5.99, 'product3': 19.99}
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
        self.source = new_source
```

**Назначение**: Метод обновляет источник данных для запроса цен.

**Параметры**:

- `new_source` (str): Новый источник данных.

**Возвращает**:

- `None`

**Как работает функция**:

- Метод устанавливает новое значение для атрибута `source`, которое указывает на новый источник данных.

**Примеры**:

```python
price_list_requester.update_source('new_source')
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
        # Здесь код для изменения цены товара в источнике данных
        ...
```

**Назначение**: Метод изменяет цену указанного товара в источнике данных.

**Параметры**:

- `product` (str): Название товара.
- `new_price` (float): Новая цена товара.

**Возвращает**:

- `None`

**Как работает функция**:

- Метод использует код для изменения цены товара в источнике данных.
- В текущем варианте код не указан, поэтому функция не выполняет никаких действий.

**Примеры**:

```python
price_list_requester.modify_product_price('product1', 12.99)
```

## Параметры класса

- `api_credentials` (Dict[str, str]): Словарь с учетными данными для API, включая `api_domain` и `api_key`.
- `source` (str): Источник данных для запроса цен.

## Примеры

```python
# Создание объекта класса PriceListRequester
api_credentials = {'api_domain': 'your_prestashop_domain.com', 'api_key': 'your_api_key'}
price_list_requester = PriceListRequester(api_credentials)

# Запрос списка цен для товаров
products = ['product1', 'product2', 'product3']
prices = price_list_requester.request_prices(products)
print(prices)  # Вывод: {'product1': 10.99, 'product2': 5.99, 'product3': 19.99}

# Обновление источника данных
price_list_requester.update_source('new_source')

# Изменение цены товара
price_list_requester.modify_product_price('product1', 12.99)
```

## Примечания

- Модуль использует библиотеку `requests` для отправки HTTP-запросов.
- Модуль использует библиотеку `attr` для определения атрибутов класса.
- Модуль использует библиотеку `json` для обработки JSON-данных.
- Модуль использует библиотеку `logger` из проекта `hypotez` для вывода логов.

## Изменения

- 2023-12-01: Добавлены комментарии и документация.