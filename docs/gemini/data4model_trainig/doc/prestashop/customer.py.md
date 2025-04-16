# Модуль для работы с клиентами в PrestaShop

## Обзор

Модуль `src.endpoints.prestashop.customer` предназначен для управления клиентами в PrestaShop. Он содержит класс `PrestaCustomer`, который позволяет добавлять, удалять, обновлять и получать информацию о клиентах.

## Подробней

Модуль предоставляет удобный интерфейс для выполнения операций с клиентами в PrestaShop, используя API PrestaShop.

## Классы

### `PrestaCustomer`

**Описание**: Класс для работы с клиентами в PrestaShop.

**Наследует**:

*   `PrestaShop`: Предоставляет базовые методы для взаимодействия с API PrestaShop.

**Атрибуты**:

*   Нет явно определенных атрибутов, но наследует атрибуты от класса `PrestaShop`, такие как `api_key` и `api_domain`.

**Методы**:

*   `__init__(self, credentials: Optional[dict | SimpleNamespace] = None, api_domain: Optional[str] = None, api_key: Optional[str] = None, *args, **kwards)`: Инициализирует объект `PrestaCustomer`.

## Методы класса `PrestaCustomer`

### `__init__`

```python
def __init__(self, 
             credentials: Optional[dict | SimpleNamespace] = None, 
             api_domain: Optional[str] = None, 
             api_key: Optional[str] = None, 
             *args, **kwards):
```

**Назначение**: Инициализирует объект `PrestaCustomer`.

**Параметры**:

*   `credentials` (Optional[dict | SimpleNamespace]], optional): Словарь или объект SimpleNamespace с параметрами `api_domain` и `api_key`. Defaults to None.
*   `api_domain` (Optional[str], optional): Домен API. Defaults to None.
*   `api_key` (Optional[str], optional): Ключ API. Defaults to None.

**Вызывает исключения**:

*   `ValueError`: Если не предоставлены `api_domain` и `api_key`.

**Как работает функция**:

1.  Если предоставлены `credentials`, извлекает `api_domain` и `api_key` из них.
2.  Проверяет, предоставлены ли `api_domain` и `api_key`. Если нет, вызывает исключение `ValueError`.
3.  Вызывает конструктор родительского класса `PrestaShop` с переданными параметрами.

**Примеры**:

```python
from src.endpoints.prestashop.customer import PrestaCustomer

# Пример инициализации с использованием параметров
customer = PrestaCustomer(api_domain='your_api_domain', api_key='your_api_key')

# Пример инициализации с использованием credentials
credentials = {'api_domain': 'your_api_domain', 'api_key': 'your_api_key'}
customer = PrestaCustomer(credentials=credentials)