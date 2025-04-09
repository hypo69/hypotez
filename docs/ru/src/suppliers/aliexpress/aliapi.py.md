# Модуль `aliapi.py`

## Обзор

Модуль `aliapi.py` предоставляет класс `AliApi`, который является пользовательским API для работы с AliExpress. Он расширяет функциональность базового класса `AliexpressApi` и включает методы для получения информации о продуктах, категорий и управления кампаниями.

## Подробней

Модуль предназначен для упрощения взаимодействия с API AliExpress, предоставляя удобные методы для выполнения различных операций, таких как получение деталей продуктов и создание партнерских ссылок. Класс `AliApi` использует учетные данные, хранящиеся в `gs.credentials.aliexpress`, для аутентификации запросов к API.

## Классы

### `AliApi`

**Описание**: Пользовательский класс API для операций с AliExpress.

**Наследует**:

- `AliexpressApi`: Расширяет базовый класс `AliexpressApi`, добавляя функциональность для работы с категориями, кампаниями и деталями продуктов.

**Атрибуты**:

- `manager_categories` (CategoryManager): Менеджер категорий для работы с категориями AliExpress.
- `manager_campaigns` (ProductCampaignsManager): Менеджер кампаний для работы с кампаниями продуктов AliExpress.

**Методы**:

- `__init__(self, language: str = 'en', currency: str = 'usd', *args, **kwargs)`: Инициализирует экземпляр класса `AliApi`.
- `retrieve_product_details_as_dict(self, product_ids: list) -> dict | dict | None`: Получает детали продуктов в формате словаря.
- `get_affiliate_links(self, links: str | list, link_type: int = 0, **kwargs) -> List[SimpleNamespace]`: Получает партнерские ссылки для указанных продуктов.

### `__init__`

```python
def __init__(self, language: str = 'en', currency: str = 'usd', *args, **kwargs):
    """ Инициализирует экземпляр класса AliApi.
    
    Args:
        language (str): Язык для API запросов. По умолчанию 'en'.
        currency (str): Валюта для API запросов. По умолчанию 'usd'.
    """
```

**Как работает функция**:

1.  Получает учетные данные AliExpress из `gs.credentials.aliexpress`.
2.  Инициализирует базовый класс `AliexpressApi` с полученными учетными данными, языком и валютой.
3.  Инициализирует менеджеры базы данных для категорий и кампаний (закомментировано в текущей версии).

**Примеры**:

```python
api = AliApi(language='ru', currency='rub')
```

### `retrieve_product_details_as_dict`

```python
def retrieve_product_details_as_dict(self, product_ids: list) -> dict | dict | None:
    """ Отправляет список ID продуктов в AliExpress и получает список объектов SimpleNamespace с описаниями продуктов.
    
    Args:
        product_ids (list): Список ID продуктов.
    
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
        
        # Альтернативно, использование метода __dict__:
        dict_list = [ns.__dict__ for ns in namespace_list]
        
        # Вывод списка словарей
        print(dict_list)
    """
```

**Как работает функция**:

1.  Вызывает метод `retrieve_product_details` базового класса `AliexpressApi` для получения деталей продуктов в формате `SimpleNamespace`.
2.  Преобразует каждый объект `SimpleNamespace` в словарь с использованием функции `vars()`.
3.  Возвращает список словарей с деталями продуктов.

```
A: Получение деталей продуктов в формате SimpleNamespace
|
B: Преобразование SimpleNamespace в dict
|
C: Возврат списка словарей
```

**Примеры**:

```python
product_ids = ['1234567890', '0987654321']
product_details = api.retrieve_product_details_as_dict(product_ids)
if product_details:
    for product in product_details:
        print(product['title'])
```

### `get_affiliate_links`

```python
def get_affiliate_links(self, links: str | list, link_type: int = 0, **kwargs) -> List[SimpleNamespace]:
    """ 
    Получает партнерские ссылки для указанных продуктов.
    
    Args:
        links (str | list): Ссылки на продукты, для которых требуется получить партнерские ссылки.
        link_type (int, optional): Тип партнерской ссылки для генерации. По умолчанию 0.
    
    Returns:
        List[SimpleNamespace]: Список объектов SimpleNamespace, содержащих партнерские ссылки.
    """
```

**Как работает функция**:

1.  Вызывает метод `get_affiliate_links` базового класса `AliexpressApi` для получения партнерских ссылок.
2.  Возвращает список объектов `SimpleNamespace`, содержащих партнерские ссылки.

```
A: Вызов метода получения партнерских ссылок из базового класса
|
B: Возврат списка SimpleNamespace с партнерскими ссылками
```

**Примеры**:

```python
links = ['https://example.com/product1', 'https://example.com/product2']
affiliate_links = api.get_affiliate_links(links)
for link in affiliate_links:
    print(link.affiliate_url)