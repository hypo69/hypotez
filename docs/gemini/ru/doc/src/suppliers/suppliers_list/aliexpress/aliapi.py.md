# Модуль для работы с API AliExpress
## Обзор

Модуль `aliapi.py` предоставляет класс `AliApi`, который расширяет функциональность класса `AliexpressApi` для работы с API AliExpress. Он включает методы для получения деталей продукта и партнерских ссылок, адаптированные для использования в проекте `hypotez`.

## Подробней

Этот модуль предназначен для упрощения взаимодействия с API AliExpress, предоставляя удобные методы для получения информации о продуктах и генерации партнерских ссылок. Он использует классы и функции из других модулей проекта, таких как `src.gs`, `src.utils.jjson`, `src.utils.printer`, `src.utils.convertors.json` и `src.logger.logger`.

## Классы

### `AliApi`

**Описание**: Пользовательский класс API для операций с AliExpress.

**Наследует**: `AliexpressApi`

**Методы**:
- `__init__`: Инициализирует экземпляр класса `AliApi`.
- `retrieve_product_details_as_dict`: Получает детали продукта в виде словаря.
- `get_affiliate_links`: Получает партнерские ссылки для указанных продуктов.

## Методы класса

### `__init__`

```python
def __init__(self, language: str = 'en', currency: str = 'usd', *args, **kwargs):
    """
    Инициализирует экземпляр класса AliApi.

    Args:
        language (str): Язык для использования в API-запросах. По умолчанию 'en'.
        currency (str): Валюта для использования в API-запросах. По умолчанию 'usd'.

    """
    ...
```

**Назначение**: Инициализирует экземпляр класса `AliApi`, устанавливая язык и валюту для API-запросов, а также извлекая учетные данные из конфигурации.

**Параметры**:
- `language` (str): Язык для использования в API-запросах. По умолчанию `'en'`.
- `currency` (str): Валюта для использования в API-запросах. По умолчанию `'usd'`.
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса.
- `**kwargs`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса.

**Как работает функция**:
- Извлекает учетные данные (api_key, secret, tracking_id) из конфигурации `gs.credentials.aliexpress`.
- Вызывает конструктор родительского класса `AliexpressApi` с переданными учетными данными, языком и валютой.
- ...

**Примеры**:
```python
ali_api = AliApi(language='ru', currency='rub')
```

### `retrieve_product_details_as_dict`

```python
def retrieve_product_details_as_dict(self, product_ids: list) -> dict | dict | None:
    """
    Отправляет список идентификаторов продуктов в AliExpress и получает список объектов SimpleNamespace с описаниями продуктов.

    Args:
        product_ids (list): Список идентификаторов продуктов.

    Returns:
        dict | None: Список данных продукта в виде словарей.

    Example:
        # Преобразование из формата SimpleNamespace в dict
        namespace_list = [
            SimpleNamespace(a=1, b=2, c=3),
            SimpleNamespace(d=4, e=5, f=6),
            SimpleNamespace(g=7, h=8, i=9)
        ]

        # Преобразование каждого объекта SimpleNamespace в словарь
        dict_list = [vars(ns) for ns in namespace_list]

        # Альтернативно, используйте метод __dict__:
        dict_list = [ns.__dict__ for ns in namespace_list]

        # Вывод списка словарей
        print(dict_list)
    """
    ...
```

**Назначение**: Получает детали продукта в виде словаря, отправляя список идентификаторов продуктов в AliExpress.

**Параметры**:
- `product_ids` (list): Список идентификаторов продуктов.

**Возвращает**:
- `dict | None`: Список данных продукта в виде словарей.

**Как работает функция**:
- Вызывает метод `retrieve_product_details` для получения деталей продукта в формате `SimpleNamespace`.
- Преобразует каждый объект `SimpleNamespace` в словарь с помощью `vars(ns)`.
- Возвращает список словарей с деталями продуктов.

**Примеры**:
```python
product_ids = ['1234567890', '0987654321']
product_details = ali_api.retrieve_product_details_as_dict(product_ids)
if product_details:
    print(product_details)
```

### `get_affiliate_links`

```python
def get_affiliate_links(self, links: str | list, link_type: int = 0, **kwargs) -> List[SimpleNamespace]:
    """
    Получает партнерские ссылки для указанных продуктов.

    Args:
        links (str | list): Ссылки на продукты, для которых требуется получить партнерские ссылки.
        link_type (int, optional): Тип партнерской ссылки, которую необходимо сгенерировать. По умолчанию 0.

    Returns:
        List[SimpleNamespace]: Список объектов SimpleNamespace, содержащих партнерские ссылки.
    """
    ...
```

**Назначение**: Получает партнерские ссылки для указанных продуктов.

**Параметры**:
- `links` (str | list): Ссылки на продукты, для которых требуется получить партнерские ссылки.
- `link_type` (int, optional): Тип партнерской ссылки, которую необходимо сгенерировать. По умолчанию `0`.
- `**kwargs`: Дополнительные именованные аргументы, передаваемые в метод `get_affiliate_links` родительского класса.

**Возвращает**:
- `List[SimpleNamespace]`: Список объектов `SimpleNamespace`, содержащих партнерские ссылки.

**Как работает функция**:
- Вызывает метод `get_affiliate_links` родительского класса `AliexpressApi` с переданными параметрами.
- Возвращает список объектов `SimpleNamespace`, содержащих партнерские ссылки.

**Примеры**:
```python
links = ['https://example.com/product1', 'https://example.com/product2']
affiliate_links = ali_api.get_affiliate_links(links)
if affiliate_links:
    print(affiliate_links)