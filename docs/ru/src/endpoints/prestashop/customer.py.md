# Модуль: src.endpoints.prestashop.customer

## Обзор

Модуль `customer.py` предназначен для работы с клиентами в PrestaShop. Он включает в себя класс `PrestaCustomer`, который позволяет добавлять, удалять, обновлять и получать информацию о клиентах через API PrestaShop.

## Подробнее

Модуль предоставляет удобный интерфейс для взаимодействия с API PrestaShop, упрощая процесс управления данными клиентов. Он использует классы `PrestaShop` из модуля `api.py` для выполнения HTTP-запросов к API PrestaShop.

## Классы

### `PrestaCustomer`

**Описание**: Класс для работы с клиентами в PrestaShop. Он позволяет добавлять, удалять, обновлять и получать информацию о клиентах через API PrestaShop.

**Наследует**:

-   `PrestaShop`: Класс для взаимодействия с API PrestaShop.

**Атрибуты**: Отсутствуют

**Методы**:

-   `__init__`: Инициализация клиента PrestaShop.

#### `__init__`

```python
def __init__(self,
             credentials: Optional[dict | SimpleNamespace] = None,
             api_domain: Optional[str] = None,
             api_key: Optional[str] = None,
             *args, **kwards):
    """Инициализация клиента PrestaShop.

    Args:
        credentials (Optional[dict | SimpleNamespace], optional): Словарь или объект SimpleNamespace с параметрами `api_domain` и `api_key`. Defaults to None.
        api_domain (Optional[str], optional): Домен API. Defaults to None.
        api_key (Optional[str], optional): Ключ API. Defaults to None.
    """
```

**Назначение**: Инициализирует экземпляр класса `PrestaCustomer`.

**Параметры**:

-   `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или объект `SimpleNamespace` с параметрами `api_domain` и `api_key`. По умолчанию `None`.
-   `api_domain` (Optional[str], optional): Домен API. По умолчанию `None`.
-   `api_key` (Optional[str], optional): Ключ API. По умолчанию `None`.
-   `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса.
-   `**kwards`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса.

**Как работает функция**:

1.  Проверяет, переданы ли параметры `credentials`. Если да, извлекает значения `api_domain` и `api_key` из словаря `credentials`, если они там есть.
2.  Проверяет, что `api_domain` и `api_key` не `None`. Если хотя бы один из них `None`, вызывает исключение `ValueError`.
3.  Вызывает конструктор родительского класса `PrestaShop` с переданными параметрами.

**Примеры**:

```python
# Пример 1: Инициализация с использованием api_domain и api_key
prestacustomer = PrestaCustomer(api_domain='your_api_domain', api_key='your_api_key')

# Пример 2: Инициализация с использованием credentials
credentials = {'api_domain': 'your_api_domain', 'api_key': 'your_api_key'}
prestacustomer = PrestaCustomer(credentials=credentials)

# Пример 3: Инициализация с использованием SimpleNamespace
credentials = SimpleNamespace(api_domain='your_api_domain', api_key='your_api_key')
prestacustomer = PrestaCustomer(credentials=credentials)