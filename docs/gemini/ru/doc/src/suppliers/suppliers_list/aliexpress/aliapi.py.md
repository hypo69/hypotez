# Модуль AliApi

## Обзор

Модуль `aliapi.py` предоставляет API для взаимодействия с AliExpress. 
Он основан на классе `AliexpressApi`, реализует методы для получения данных о товарах, 
генерации партнёрских ссылок и других операций с AliExpress.

## Подробнее

Модуль содержит класс `AliApi`, который наследует класс `AliexpressApi`. 
`AliApi` расширяет функциональность базового класса и добавляет методы для работы с данными о товарах. 
Он также использует API-ключи для аутентификации и работы с сервисом. 

## Классы

### `AliApi`

**Описание**: Класс для работы с AliExpress. 
**Наследует**: `AliexpressApi`

**Атрибуты**: 
- `language` (str): Язык, который используется для запросов к API. По умолчанию `en`.
- `currency` (str): Валюта, которая используется для запросов к API. По умолчанию `usd`.
- `api_key` (str): Ключ API, который используется для аутентификации запросов к API.
- `secret` (str): Секретный ключ API, который используется для аутентификации запросов к API.
- `tracking_id` (str): Идентификатор отслеживания, который используется для отслеживания результатов запросов к API.

**Методы**:

- `__init__(self, language: str = 'en', currency: str = 'usd', *args, **kwargs)`: Инициализирует экземпляр класса `AliApi`.
- `retrieve_product_details_as_dict(self, product_ids: list) -> dict | dict | None`: Отправляет список идентификаторов товаров на AliExpress и получает список объектов `SimpleNamespace` с описанием товаров.
- `get_affiliate_links(self, links: str | list, link_type: int = 0, **kwargs) -> List[SimpleNamespace]`: Возвращает партнёрские ссылки для указанных товаров.

#### `__init__(self, language: str = 'en', currency: str = 'usd', *args, **kwargs)`

**Назначение**: Инициализирует экземпляр класса `AliApi`.

**Параметры**:
- `language` (str, optional): Язык, который используется для запросов к API. По умолчанию `en`.
- `currency` (str, optional): Валюта, которая используется для запросов к API. По умолчанию `usd`.
- `*args`: Дополнительные аргументы, которые передаются в конструктор базового класса `AliexpressApi`.
- `**kwargs`: Дополнительные именованные аргументы, которые передаются в конструктор базового класса `AliexpressApi`.

**Возвращает**:
- None

**Примеры**:

```python
# Инициализация экземпляра класса AliApi
aliapi = AliApi(language='ru', currency='rub')
```

#### `retrieve_product_details_as_dict(self, product_ids: list) -> dict | dict | None`

**Назначение**: Отправляет список идентификаторов товаров на AliExpress и получает список объектов `SimpleNamespace` с описанием товаров.

**Параметры**:
- `product_ids` (list): Список идентификаторов товаров.

**Возвращает**:
- `dict | None`: Список данных о товарах в виде словарей.

**Примеры**:

```python
# Получение данных о товарах
product_ids = ['1234567890', '9876543210']
product_details = aliapi.retrieve_product_details_as_dict(product_ids)
pprint(product_details) # Вывод данных о товарах на экран
```

**Как работает функция**:
- Функция вызывает метод `retrieve_product_details` базового класса `AliexpressApi`, который отправляет запрос на AliExpress с указанными идентификаторами товаров.
- Ответ от API преобразуется из списка объектов `SimpleNamespace` в список словарей.
- Функция возвращает список словарей с данными о товарах.

#### `get_affiliate_links(self, links: str | list, link_type: int = 0, **kwargs) -> List[SimpleNamespace]`

**Назначение**: Возвращает партнёрские ссылки для указанных товаров.

**Параметры**:
- `links` (str | list): Ссылка или список ссылок на товары.
- `link_type` (int, optional): Тип партнёрской ссылки, который нужно сгенерировать. По умолчанию `0`.
- `**kwargs`: Дополнительные именованные аргументы, которые передаются в метод `get_affiliate_links` базового класса `AliexpressApi`.

**Возвращает**:
- `List[SimpleNamespace]`: Список объектов `SimpleNamespace` с партнёрскими ссылками.

**Примеры**:

```python
# Получение партнёрских ссылок
links = 'https://aliexpress.com/item/1234567890.html'
affiliate_links = aliapi.get_affiliate_links(links, link_type=1)
pprint(affiliate_links) # Вывод партнёрских ссылок на экран
```

**Как работает функция**:
- Функция вызывает метод `get_affiliate_links` базового класса `AliexpressApi`, который отправляет запрос на AliExpress с указанными ссылками на товары.
- Ответ от API преобразуется в список объектов `SimpleNamespace`.
- Функция возвращает список объектов `SimpleNamespace` с партнёрскими ссылками.

## Примеры

### Пример работы с классом `AliApi`

```python
# Импорт необходимых модулей
from src.suppliers.suppliers_list.aliexpress.aliapi import AliApi

# Инициализация экземпляра класса AliApi
aliapi = AliApi(language='ru', currency='rub')

# Получение данных о товарах
product_ids = ['1234567890', '9876543210']
product_details = aliapi.retrieve_product_details_as_dict(product_ids)

# Вывод данных о товарах на экран
pprint(product_details)

# Получение партнёрских ссылок
links = ['https://aliexpress.com/item/1234567890.html']
affiliate_links = aliapi.get_affiliate_links(links, link_type=1)

# Вывод партнёрских ссылок на экран
pprint(affiliate_links)
```