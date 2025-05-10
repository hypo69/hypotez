# Модуль `aliapi.py`

## Обзор

Модуль `aliapi.py` предназначен для работы с API AliExpress. Он предоставляет класс `AliApi`, который расширяет функциональность класса `AliexpressApi` и предоставляет методы для получения информации о товарах и партнерских ссылок.

## Подробнее

Модуль предоставляет кастомный класс `AliApi` для выполнения операций с AliExpress API. Он включает методы для извлечения деталей товара в формате словаря и получения партнерских ссылок. Расположение файла в проекте указывает на его роль в качестве поставщика данных из AliExpress.

## Классы

### `AliApi`

**Описание**:
Класс `AliApi` представляет собой пользовательский API для операций с AliExpress.

**Наследует**:

*   `AliexpressApi`: Класс `AliApi` наследует функциональность от класса `AliexpressApi`, расширяя его возможности для работы с API AliExpress.

**Атрибуты**:

*   Нет дополнительных атрибутов, кроме тех, что наследуются от `AliexpressApi`.

**Методы**:

*   `__init__`: Инициализирует экземпляр класса `AliApi`.
*   `retrieve_product_details_as_dict`: Отправляет список ID товаров в AliExpress и получает список объектов `SimpleNamespace` с описаниями товаров.
*   `get_affiliate_links`: Получает партнерские ссылки для указанных товаров.

**Принцип работы**:

Класс `AliApi` инициализируется с параметрами языка и валюты, а также с учетными данными для доступа к API AliExpress. Он использует методы родительского класса `AliexpressApi` для выполнения запросов к API и предоставляет дополнительные методы для преобразования данных и получения партнерских ссылок.

### `__init__`

```python
def __init__(self, language: str = 'en', currency: str = 'usd', *args, **kwargs):
    """Инициализирует экземпляр класса AliApi.

    Args:
        language (str): Язык для использования в API-запросах. По умолчанию 'en'.
        currency (str): Валюта для использования в API-запросах. По умолчанию 'usd'.
    """
    credentials = gs.credentials.aliexpress
    api_key = credentials.api_key
    secret = credentials.secret
    tracking_id = credentials.tracking_id
    super().__init__(api_key, secret, language, currency, tracking_id)
    ...
```

**Назначение**:
Инициализация экземпляра класса `AliApi` с заданными параметрами языка и валюты, а также с учетными данными для доступа к API AliExpress.

**Параметры**:

*   `language` (str): Язык для использования в API-запросах. По умолчанию `'en'`.
*   `currency` (str): Валюта для использования в API-запросах. По умолчанию `'usd'`.
*   `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса.
*   `**kwargs`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса.

**Как работает функция**:

1.  Извлекает учетные данные AliExpress API из `gs.credentials.aliexpress`.
2.  Инициализирует родительский класс `AliexpressApi` с учетными данными, языком, валютой и идентификатором отслеживания.

**Примеры**:

```python
ali_api = AliApi(language='ru', currency='rub')
```

### `retrieve_product_details_as_dict`

```python
def retrieve_product_details_as_dict(self, product_ids: list) -> dict | dict | None:
    """Отправляет список ID товаров в AliExpress и получает список объектов SimpleNamespace с описаниями товаров.

    Args:
        product_ids (list): Список ID товаров.

    Returns:
        dict | None: Список данных о товарах в виде словарей.

    Example:
        # Convert from SimpleNamespace format to dict
        namespace_list = [
            SimpleNamespace(a=1, b=2, c=3),
            SimpleNamespace(d=4, e=5, f=6),
            SimpleNamespace(g=7, h=8, i=9)
        ]

        # Convert each SimpleNamespace object to a dictionary
        dict_list = [vars(ns) for ns in namespace_list]

        # Alternatively, use the __dict__ method:
        dict_list = [ns.__dict__ for ns in namespace_list]

        # Print the list of dictionaries
        print(dict_list)
    """
    prod_details_ns = self.retrieve_product_details(product_ids)
    prod_details_dict = [vars(ns) for ns in prod_details_ns]
    return prod_details_dict
```

**Назначение**:
Получение деталей товаров AliExpress в формате словаря на основе списка их идентификаторов.

**Параметры**:

*   `product_ids` (list): Список идентификаторов товаров, для которых требуется получить детали.

**Возвращает**:

*   `dict | None`: Список данных о товарах в виде словарей. Возвращает `None`, если произошла ошибка при получении данных.

**Как работает функция**:

1.  Вызывает метод `retrieve_product_details` для получения списка объектов `SimpleNamespace` с деталями товаров.
2.  Преобразует каждый объект `SimpleNamespace` в словарь с использованием функции `vars()`.
3.  Возвращает список словарей с деталями товаров.

**Примеры**:

```python
product_ids = ['1234567890', '0987654321']
product_details = ali_api.retrieve_product_details_as_dict(product_ids)
if product_details:
    pprint(product_details)
```

### `get_affiliate_links`

```python
def get_affiliate_links(self, links: str | list, link_type: int = 0, **kwargs) -> List[SimpleNamespace]:
    """
    Retrieves affiliate links for the specified products.

    Args:
        links (str | list): The product links to be processed.
        link_type (int, optional): The type of affiliate link to be generated. Defaults to 0.

    Returns:
        List[SimpleNamespace]: A list of SimpleNamespace objects containing affiliate links.
    """
    return super().get_affiliate_links(links, link_type, **kwargs)
```

**Назначение**:
Получение партнерских ссылок для указанных товаров.

**Параметры**:

*   `links` (str | list): Ссылка или список ссылок на товары, для которых требуется получить партнерские ссылки.
*   `link_type` (int, optional): Тип партнерской ссылки для генерации. По умолчанию `0`.
*   `**kwargs`: Произвольные именованные аргументы, передаваемые в метод родительского класса.

**Возвращает**:

*   `List[SimpleNamespace]`: Список объектов `SimpleNamespace`, содержащих партнерские ссылки.

**Как работает функция**:

1.  Вызывает метод `get_affiliate_links` родительского класса `AliexpressApi` с переданными параметрами.
2.  Возвращает список объектов `SimpleNamespace` с партнерскими ссылками.

**Примеры**:

```python
product_links = ['https://example.com/product1', 'https://example.com/product2']
affiliate_links = ali_api.get_affiliate_links(product_links, link_type=1)
pprint(affiliate_links)