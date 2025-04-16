# Модуль для работы с клиентами PrestaShop

## Обзор

Модуль `customer.py` предназначен для взаимодействия с API PrestaShop для управления клиентами. Он содержит класс `PrestaCustomer`, который предоставляет методы для добавления, удаления, обновления и получения информации о клиентах в магазине PrestaShop.

## Подробней

Этот модуль обеспечивает удобный интерфейс для работы с клиентами PrestaShop, абстрагируя детали API и упрощая выполнение типичных операций, таких как добавление нового клиента, удаление существующего клиента, обновление информации о клиенте и получение детальной информации о конкретном клиенте.

## Классы

### `PrestaCustomer`

**Описание**: Класс для работы с клиентами в PrestaShop.

**Наследует**: `PrestaShop`

**Атрибуты**:
- Нет специфических атрибутов, кроме тех, что наследуются от `PrestaShop`.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `PrestaCustomer`.
- `add_customer_PrestaShop`: Добавляет нового клиента в PrestaShop.
- `delete_customer_PrestaShop`: Удаляет клиента из PrestaShop.
- `update_customer_PrestaShop`: Обновляет информацию о клиенте в PrestaShop.
- `get_customer_details_PrestaShop`: Получает детальную информацию о клиенте из PrestaShop.

**Принцип работы**:

Класс `PrestaCustomer` наследует функциональность от класса `PrestaShop`, который предоставляет базовые методы для взаимодействия с API PrestaShop. При инициализации класса `PrestaCustomer` требуется передать учетные данные API (домен и ключ), которые используются для аутентификации при выполнении запросов к API PrestaShop.

### `__init__`

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
    ...
```

**Назначение**: Инициализация экземпляра класса `PrestaCustomer`.

**Параметры**:
- `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или объект `SimpleNamespace`, содержащий параметры `api_domain` и `api_key`. По умолчанию `None`.
- `api_domain` (Optional[str], optional): Домен API PrestaShop. По умолчанию `None`.
- `api_key` (Optional[str], optional): Ключ API PrestaShop. По умолчанию `None`.

**Возвращает**:
- `None`

**Вызывает исключения**:
- `ValueError`: Если не предоставлены `api_domain` и `api_key`.

**Как работает функция**:

Функция инициализирует класс `PrestaCustomer`, принимая учетные данные для доступа к API PrestaShop. Учетные данные могут быть переданы либо как словарь/SimpleNamespace в параметре `credentials`, либо как отдельные параметры `api_domain` и `api_key`. Если учетные данные не предоставлены, вызывается исключение `ValueError`. Функция также вызывает конструктор родительского класса `PrestaShop` для инициализации базовых параметров API.

**Примеры**:

```python
# Пример 1: Инициализация с использованием отдельных параметров
prestacustomer = PrestaCustomer(api_domain='your_api_domain', api_key='your_api_key')

# Пример 2: Инициализация с использованием словаря credentials
credentials = {'api_domain': 'your_api_domain', 'api_key': 'your_api_key'}
prestacustomer = PrestaCustomer(credentials=credentials)

# Пример 3: Инициализация с использованием SimpleNamespace credentials
credentials = SimpleNamespace(api_domain='your_api_domain', api_key='your_api_key')
prestacustomer = PrestaCustomer(credentials=credentials)