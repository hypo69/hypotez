# Модуль: src.endpoints.prestashop.customer

## Обзор

Модуль `src.endpoints.prestashop.customer` предоставляет класс `PrestaCustomer` для работы с клиентами в PrestaShop. Он включает в себя методы для добавления, удаления, обновления и получения информации о клиентах через API PrestaShop.

## Подробней

Модуль предназначен для упрощения взаимодействия с API PrestaShop при работе с клиентами. Класс `PrestaCustomer` наследует функциональность из класса `PrestaShop` и предоставляет удобные методы для выполнения стандартных операций с клиентами. Расположение файла в проекте указывает на то, что он является частью подсистемы, отвечающей за интеграцию с PrestaShop.

## Классы

### `PrestaCustomer`

**Описание**: Класс для работы с клиентами в PrestaShop.

**Наследует**: `PrestaShop`

**Атрибуты**:
- Нет явных атрибутов, кроме тех, что наследуются от `PrestaShop`.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `PrestaCustomer`.
- `add_customer_PrestaShop`: Добавляет нового клиента в PrestaShop.
- `delete_customer_PrestaShop`: Удаляет клиента из PrestaShop.
- `update_customer_PrestaShop`: Обновляет информацию о клиенте в PrestaShop.
- `get_customer_details_PrestaShop`: Получает детали клиента из PrestaShop.

**Принцип работы**:
Класс инициализируется с использованием домена API и ключа API PrestaShop. Он предоставляет методы для выполнения операций CRUD (Create, Read, Update, Delete) над клиентами через API PrestaShop.

## Методы класса

### `__init__`

```python
def __init__(self, 
                 credentials: Optional[dict | SimpleNamespace] = None, 
                 api_domain: Optional[str] = None, 
                 api_key: Optional[str] = None, 
                 *args, **kwargs):
    """Инициализация клиента PrestaShop.

    Args:
        credentials (Optional[dict | SimpleNamespace], optional): Словарь или объект SimpleNamespace с параметрами `api_domain` и `api_key`. Defaults to None.
        api_domain (Optional[str], optional): Домен API. Defaults to None.
        api_key (Optional[str], optional): Ключ API. Defaults to None.
    """
```

**Назначение**: Инициализирует экземпляр класса `PrestaCustomer`, устанавливая домен API и ключ API.

**Параметры**:
- `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или объект `SimpleNamespace`, содержащий `api_domain` и `api_key`. По умолчанию `None`.
- `api_domain` (Optional[str], optional): Домен API PrestaShop. По умолчанию `None`.
- `api_key` (Optional[str], optional): Ключ API PrestaShop. По умолчанию `None`.

**Возвращает**:
- Ничего (None).

**Вызывает исключения**:
- `ValueError`: Если `api_domain` или `api_key` не предоставлены.

**Как работает функция**:
Функция `__init__` инициализирует класс `PrestaCustomer`. Она проверяет, переданы ли домен API и ключ API через аргументы или через словарь `credentials`. Если ни один из этих параметров не предоставлен, функция выдает исключение `ValueError`. В противном случае функция вызывает метод `__init__` родительского класса `PrestaShop`.

**Примеры**:

```python
# Пример 1: Инициализация с использованием api_domain и api_key
prestacustomer = PrestaCustomer(api_domain='https://yourdomain.com/api', api_key='your_api_key')

# Пример 2: Инициализация с использованием словаря credentials
credentials = {'api_domain': 'https://yourdomain.com/api', 'api_key': 'your_api_key'}
prestacustomer = PrestaCustomer(credentials=credentials)