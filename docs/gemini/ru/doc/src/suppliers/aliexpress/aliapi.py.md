# Модуль `aliapi`

## Обзор

Модуль `aliapi` представляет собой часть проекта `hypotez` и предназначен для работы с API AliExpress. Он содержит класс `AliApi`, который расширяет функциональность базового класса `AliexpressApi` и предоставляет методы для получения информации о товарах, категориях и акциях на AliExpress.

## Подробней

Модуль `aliapi` предоставляет инструменты для взаимодействия с API AliExpress, включая получение информации о товарах, категориях и акциях. Он использует классы `CategoryManager` и `ProductCampaignsManager` для управления данными о категориях и акциях, соответственно. Этот модуль позволяет получать детали о продуктах, аффилиатные ссылки и другую информацию, необходимую для работы с AliExpress.

## Классы

### `AliApi`

**Описание**:
Класс `AliApi` является пользовательским классом API для операций с AliExpress. Он наследует класс `AliexpressApi` и добавляет дополнительную функциональность, такую как управление категориями и кампаниями продуктов.

**Наследует**:
- `AliexpressApi`: Базовый класс для взаимодействия с API AliExpress.

**Атрибуты**:
- `manager_categories` (CategoryManager): Менеджер категорий AliExpress.
- `manager_campaigns` (ProductCampaignsManager): Менеджер кампаний продуктов.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `AliApi`.
- `retrieve_product_details_as_dict`: Получает детали продукта в виде словаря.
- `get_affiliate_links`: Получает партнерские ссылки для указанных товаров.

### `__init__`

```python
def __init__(self, language: str = 'en', currency: str = 'usd', *args, **kwargs):
    """ Инициализирует экземпляр класса AliApi.

    Args:
        language (str): Язык для использования в API-запросах. По умолчанию 'en'.
        currency (str): Валюта для использования в API-запросах. По умолчанию 'usd'.
    """
    ...
```

**Назначение**:
Инициализирует экземпляр класса `AliApi`, устанавливая язык и валюту для API-запросов, а также инициализируя менеджеры категорий и кампаний.

**Параметры**:
- `language` (str): Язык для использования в API-запросах. По умолчанию `'en'`.
- `currency` (str): Валюта для использования в API-запросах. По умолчанию `'usd'`.
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса.
- `**kwargs`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса.

**Как работает функция**:
- Извлекает учетные данные AliExpress из объекта `gs.credentials.aliexpress`.
- Инициализирует менеджеры категорий и кампаний продуктов.
- Вызывает конструктор родительского класса `AliexpressApi` с переданными параметрами.

**Примеры**:

```python
api = AliApi(language='ru', currency='rub')
```

### `retrieve_product_details_as_dict`

```python
def retrieve_product_details_as_dict(self, product_ids: list) -> dict | dict | None:
    """ Отправляет список идентификаторов продуктов в AliExpress и получает список объектов SimpleNamespace с описаниями продуктов.

    Args:
        product_ids (list): Список идентификаторов продуктов.

    Returns:
        dict | None: Список данных о продуктах в виде словарей.

    Example:
        # Преобразование из формата SimpleNamespace в dict
        namespace_list = [
            SimpleNamespace(a=1, b=2, c=3),
            SimpleNamespace(d=4, e=5, f=6),
            SimpleNamespace(g=7, h=8, i=9)
        ]

        # Преобразование каждого объекта SimpleNamespace в словарь
        dict_list = [vars(ns) for ns in namespace_list]

        # Или используйте метод __dict__:
        dict_list = [ns.__dict__ for ns in namespace_list]

        # Вывод списка словарей
        print(dict_list)
    """
    ...
```

**Назначение**:
Преобразует данные о продуктах, полученные из AliExpress, в формат словаря.

**Параметры**:
- `product_ids` (list): Список идентификаторов продуктов.

**Возвращает**:
- `dict | None`: Список данных о продуктах в виде словарей.

**Как работает функция**:
- Вызывает метод `retrieve_product_details` для получения данных о продуктах в формате `SimpleNamespace`.
- Преобразует каждый объект `SimpleNamespace` в словарь с использованием функции `vars()`.
- Возвращает список словарей с данными о продуктах.

**Примеры**:

```python
product_ids = ['1234567890', '0987654321']
product_details = api.retrieve_product_details_as_dict(product_ids)
print(product_details)
```

### `get_affiliate_links`

```python
def get_affiliate_links(self, links: str | list, link_type: int = 0, **kwargs) -> List[SimpleNamespace]:
    """
    Получает партнерские ссылки для указанных продуктов.

    Args:
        links (str | list): Ссылки на продукты, для которых необходимо получить партнерские ссылки.
        link_type (int, optional): Тип партнерской ссылки для генерации. По умолчанию 0.

    Returns:
        List[SimpleNamespace]: Список объектов SimpleNamespace, содержащих партнерские ссылки.
    """
    ...
```

**Назначение**:
Получает партнерские ссылки для указанных товаров.

**Параметры**:
- `links` (str | list): Ссылки на продукты, для которых необходимо получить партнерские ссылки.
- `link_type` (int, optional): Тип партнерской ссылки для генерации. По умолчанию `0`.
- `**kwargs`: Дополнительные именованные аргументы, передаваемые в метод `get_affiliate_links` родительского класса.

**Возвращает**:
- `List[SimpleNamespace]`: Список объектов `SimpleNamespace`, содержащих партнерские ссылки.

**Как работает функция**:
- Вызывает метод `get_affiliate_links` родительского класса `AliexpressApi` с переданными параметрами.
- Возвращает список объектов `SimpleNamespace`, содержащих партнерские ссылки.

**Примеры**:

```python
links = ['https://aliexpress.com/item/1234567890.html', 'https://aliexpress.com/item/0987654321.html']
affiliate_links = api.get_affiliate_links(links)
print(affiliate_links)