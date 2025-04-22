# Модуль `aliapi.py`

## Обзор

Модуль `aliapi.py` предоставляет класс `AliApi`, который является кастомным API-клиентом для взаимодействия с AliExpress. Он расширяет функциональность базового класса `AliexpressApi` и предоставляет методы для получения информации о товарах и генерации партнерских ссылок.

## Подробнее

Этот модуль предназначен для упрощения работы с API AliExpress, предоставляя удобные методы для выполнения типичных задач, таких как получение информации о товарах по их идентификаторам и создание партнерских ссылок. Он использует модуль `AliexpressApi` из той же директории для выполнения низкоуровневых запросов к API.

## Классы

### `AliApi`

**Описание**: Кастомный API класс для операций с AliExpress.

**Наследует**:
- `AliexpressApi`: Базовый класс для взаимодействия с API AliExpress.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `AliApi`.
- `retrieve_product_details_as_dict`: Получает детали продуктов в формате словаря.
- `get_affiliate_links`: Получает партнерские ссылки для указанных продуктов.

## Методы класса

### `__init__`

```python
def __init__(self, language: str = 'en', currency: str = 'usd', *args, **kwargs):
    """ Инициализирует экземпляр класса AliApi.

    Args:
        language (str): Язык для API запросов. По умолчанию 'en'.
        currency (str): Валюта для API запросов. По умолчанию 'usd'.
    """
```

**Назначение**: Инициализирует экземпляр класса `AliApi`, устанавливая язык и валюту для API-запросов, а также передает учетные данные в базовый класс `AliexpressApi`.

**Параметры**:
- `language` (str): Язык для API запросов. По умолчанию 'en'.
- `currency` (str): Валюта для API запросов. По умолчанию 'usd'.
- `*args`: Произвольные позиционные аргументы, передаваемые в базовый класс.
- `**kwargs`: Произвольные именованные аргументы, передаваемые в базовый класс.

**Как работает функция**:
1. Извлекает учетные данные AliExpress (ключ API, секрет и идентификатор отслеживания) из объекта `gs.credentials.aliexpress`.
2. Вызывает конструктор базового класса `AliexpressApi`, передавая учетные данные, язык и валюту.

**Примеры**:

```python
from src.suppliers.suppliers_list.aliexpress.aliapi import AliApi
# Пример инициализации AliApi с параметрами по умолчанию
ali_api = AliApi()

# Пример инициализации AliApi с указанием языка и валюты
ali_api_custom = AliApi(language='ru', currency='rub')
```

### `retrieve_product_details_as_dict`

```python
def retrieve_product_details_as_dict(self, product_ids: list) -> dict | dict | None:
    """ Отправляет список ID продуктов в AliExpress и получает список объектов SimpleNamespace с описаниями продуктов.

    Args:
        product_ids (list): Список ID продуктов.

    Returns:
        dict | None: Список данных продуктов в виде словарей.
    """
```

**Назначение**: Получает детали продуктов с AliExpress по списку их идентификаторов и возвращает их в виде списка словарей.

**Параметры**:
- `product_ids` (list): Список идентификаторов продуктов.

**Возвращает**:
- `dict | None`: Список данных продуктов в виде словарей. Возвращает `None` в случае ошибки.

**Как работает функция**:
1. Вызывает метод `retrieve_product_details` базового класса `AliexpressApi`, чтобы получить детали продуктов в виде списка объектов `SimpleNamespace`.
2. Преобразует каждый объект `SimpleNamespace` в словарь с использованием `vars(ns)` для каждого элемента в списке.
3. Возвращает список словарей с деталями продуктов.

**Примеры**:

```python
from src.suppliers.suppliers_list.aliexpress.aliapi import AliApi

# Пример получения деталей продуктов по их ID
ali_api = AliApi()
product_ids = ['1234567890', '0987654321']
product_details = ali_api.retrieve_product_details_as_dict(product_ids)

if product_details:
    for product in product_details:
        print(product)
```

### `get_affiliate_links`

```python
def get_affiliate_links(self, links: str | list, link_type: int = 0, **kwargs) -> List[SimpleNamespace]:
    """
    Извлекает партнерские ссылки для указанных продуктов.

    Args:
        links (str | list): Ссылки на продукты, для которых требуется получить партнерские ссылки.
        link_type (int, optional): Тип партнерской ссылки для генерации. По умолчанию 0.

    Returns:
        List[SimpleNamespace]: Список объектов SimpleNamespace, содержащих партнерские ссылки.
    """
```

**Назначение**: Получает партнерские ссылки для указанных продуктов, используя API AliExpress.

**Параметры**:
- `links` (str | list): Ссылка или список ссылок на продукты.
- `link_type` (int, optional): Тип партнерской ссылки. По умолчанию 0.
- `**kwargs`: Дополнительные параметры, передаваемые в базовый класс.

**Возвращает**:
- `List[SimpleNamespace]`: Список объектов `SimpleNamespace`, содержащих партнерские ссылки.

**Как работает функция**:
1. Вызывает метод `get_affiliate_links` базового класса `AliexpressApi`, передавая ссылки, тип ссылки и дополнительные параметры.
2. Возвращает список объектов `SimpleNamespace` с партнерскими ссылками.

**Примеры**:

```python
from src.suppliers.suppliers_list.aliexpress.aliapi import AliApi

# Пример получения партнерских ссылок для списка продуктов
ali_api = AliApi()
product_links = ['https://example.com/product1', 'https://example.com/product2']
affiliate_links = ali_api.get_affiliate_links(product_links, link_type=1)

if affiliate_links:
    for link in affiliate_links:
        print(link)