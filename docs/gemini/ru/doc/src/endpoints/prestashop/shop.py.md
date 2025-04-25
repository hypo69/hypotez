# Модуль PrestaShop Shop

## Обзор

Этот модуль предоставляет класс `PrestaShopShop`, который предназначен для взаимодействия с магазинами PrestaShop через API. Он наследует класс `PrestaShop`, который предоставляет основные методы для работы с API PrestaShop. 

## Подробнее

Модуль `shop.py` является частью проекта `hypotez`. Он обеспечивает функциональность для взаимодействия с магазинами PrestaShop, используя API PrestaShop. Класс `PrestaShopShop` наследует базовый класс `PrestaShop`, расширяя его функциональность для специфических задач работы с магазинами.

## Классы

### `PrestaShopShop`

**Описание**: Класс `PrestaShopShop` обеспечивает доступ к функциональности работы с магазинами PrestaShop, используя API. Он наследует базовый класс `PrestaShop`, расширяя его функциональность для специфических задач работы с магазинами.

**Наследует**: `PrestaShop`

**Атрибуты**:

* **api_domain** (str): Домен API PrestaShop.
* **api_key** (str): Ключ API PrestaShop.

**Методы**:

* **__init__(self, credentials: Optional[dict | SimpleNamespace] = None, api_domain: Optional[str] = None, api_key: Optional[str] = None, *args, **kwargs)**: Инициализирует экземпляр класса `PrestaShopShop`. 

    **Параметры**:

    * **credentials** (Optional[dict | SimpleNamespace], optional): Словарь или объект SimpleNamespace с параметрами `api_domain` и `api_key`. По умолчанию `None`.
    * **api_domain** (Optional[str], optional): Домен API. По умолчанию `None`.
    * **api_key** (Optional[str], optional): Ключ API. По умолчанию `None`.
 
    **Как работает метод**:

    1. Метод инициализации `__init__` класса `PrestaShopShop` получает параметры `credentials`, `api_domain`, `api_key`, а также дополнительные параметры `*args` и `**kwargs`.
    2. Если передаются `credentials`, метод извлекает из них `api_domain` и `api_key`.
    3. Если `api_domain` и `api_key` не переданы, метод выдает исключение `ValueError`.
    4. Метод вызывает родительский метод `__init__` класса `PrestaShop`, передавая ему `api_domain`, `api_key` и дополнительные параметры. 

    **Примеры**:

    ```python
    # Инициализация с использованием словаря credentials
    credentials = {'api_domain': 'example.com', 'api_key': 'your_api_key'}
    shop = PrestaShopShop(credentials=credentials)

    # Инициализация с использованием объекта SimpleNamespace
    credentials = SimpleNamespace(api_domain='example.com', api_key='your_api_key')
    shop = PrestaShopShop(credentials=credentials)

    # Инициализация с прямым указанием api_domain и api_key
    shop = PrestaShopShop(api_domain='example.com', api_key='your_api_key')
    ```


## Параметры класса

* **credentials** (Optional[dict | SimpleNamespace], optional): Словарь или объект SimpleNamespace с параметрами `api_domain` и `api_key`. По умолчанию `None`.
* **api_domain** (Optional[str], optional): Домен API. По умолчанию `None`.
* **api_key** (Optional[str], optional): Ключ API. По умолчанию `None`. 

## Примеры

```python
from src.endpoints.prestashop.shop import PrestaShopShop

# Инициализация с использованием словаря credentials
credentials = {'api_domain': 'example.com', 'api_key': 'your_api_key'}
shop = PrestaShopShop(credentials=credentials)

# Инициализация с прямым указанием api_domain и api_key
shop = PrestaShopShop(api_domain='example.com', api_key='your_api_key')
```