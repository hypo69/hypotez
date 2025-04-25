# Модуль для работы с клиентами PrestaShop

## Обзор

Этот модуль предоставляет класс `PrestaCustomer`, который используется для взаимодействия с API PrestaShop и выполнения операций с клиентами, таких как добавление, удаление, обновление и получение информации о клиентах.

## Подробности

Модуль `PrestaCustomer` реализует интерфейс для взаимодействия с API PrestaShop и предоставляет удобные методы для работы с клиентами. 

- **Пример использования**:

  ```python
  prestacustomer = PrestaCustomer(API_DOMAIN=API_DOMAIN, API_KEY=API_KEY)
  prestacustomer.add_customer_PrestaShop('John Doe', 'johndoe@example.com')
  prestacustomer.delete_customer_PrestaShop(3)
  prestacustomer.update_customer_PrestaShop(4, 'Updated Customer Name')
  print(prestacustomer.get_customer_details_PrestaShop(5))
  ```

## Классы

### `PrestaCustomer`

**Описание**: Класс для работы с клиентами в PrestaShop.

**Наследует**: `PrestaShop`

**Атрибуты**:

- `api_domain` (str): Домен API.
- `api_key` (str): Ключ API.

**Методы**:

- `__init__(self, credentials: Optional[dict | SimpleNamespace] = None, api_domain: Optional[str] = None, api_key: Optional[str] = None, *args, **kwargs)`: Инициализация клиента PrestaShop.

  **Параметры**:

  - `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или объект SimpleNamespace с параметрами `api_domain` и `api_key`. По умолчанию `None`.
  - `api_domain` (Optional[str], optional): Домен API. По умолчанию `None`.
  - `api_key` (Optional[str], optional): Ключ API. По умолчанию `None`.

  **Возвращает**: `None`

  **Вызывает исключения**:

  - `ValueError`: Если не заданы оба параметра: `api_domain` и `api_key`.

  **Как работает метод**:

  - Метод инициализирует экземпляр класса `PrestaCustomer` с помощью предоставленных учетных данных или параметров `api_domain` и `api_key`.
  - Если предоставлены учетные данные, метод извлекает значения `api_domain` и `api_key` из них.
  - Если не заданы оба параметра, метод вызывает исключение `ValueError`.
  - После успешной инициализации метод вызывает родительский класс `PrestaShop` для завершения инициализации.


  **Примеры**:

  ```python
  # Инициализация с помощью словаря
  credentials = {'api_domain': 'https://example.com', 'api_key': 'your_api_key'}
  prestacustomer = PrestaCustomer(credentials=credentials)

  # Инициализация с помощью объекта SimpleNamespace
  credentials = SimpleNamespace(api_domain='https://example.com', api_key='your_api_key')
  prestacustomer = PrestaCustomer(credentials=credentials)

  # Инициализация с помощью параметров api_domain и api_key
  prestacustomer = PrestaCustomer(api_domain='https://example.com', api_key='your_api_key')
  ```

## Методы класса

### `add_customer_PrestaShop(self, firstname: str, lastname: str, email: str, password: Optional[str] = None, **kwargs) -> dict | None`

**Назначение**: Добавляет нового клиента в PrestaShop.

**Параметры**:

- `firstname` (str): Имя клиента.
- `lastname` (str): Фамилия клиента.
- `email` (str): Email клиента.
- `password` (Optional[str], optional): Пароль клиента. По умолчанию `None`.

**Возвращает**:

- `dict | None`: Словарь с информацией о новом клиенте или `None` в случае ошибки.

**Вызывает исключения**:

- `PrestaShopException`: Если возникает ошибка при взаимодействии с API PrestaShop.

**Как работает метод**:

- Метод отправляет запрос на API PrestaShop для создания нового клиента с помощью метода `POST`.
- В запросе передаются параметры `firstname`, `lastname`, `email` и `password` (если задан).
- Если запрос выполнен успешно, метод возвращает словарь с информацией о новом клиенте.
- Если возникает ошибка, метод вызывает исключение `PrestaShopException`.

**Примеры**:

```python
# Создание нового клиента
new_customer_data = prestacustomer.add_customer_PrestaShop(
    firstname='John',
    lastname='Doe',
    email='johndoe@example.com',
    password='your_password'
)

# Вывод информации о новом клиенте
if new_customer_data:
    print(f'Новый клиент создан: {new_customer_data}')
else:
    print('Ошибка при создании клиента')
```

### `delete_customer_PrestaShop(self, customer_id: int) -> bool`

**Назначение**: Удаляет клиента из PrestaShop.

**Параметры**:

- `customer_id` (int): ID клиента для удаления.

**Возвращает**:

- `bool`: `True`, если клиент удален успешно, `False` в случае ошибки.

**Вызывает исключения**:

- `PrestaShopException`: Если возникает ошибка при взаимодействии с API PrestaShop.

**Как работает метод**:

- Метод отправляет запрос на API PrestaShop для удаления клиента с помощью метода `DELETE`.
- В запросе передается параметр `customer_id`.
- Если запрос выполнен успешно, метод возвращает `True`.
- Если возникает ошибка, метод вызывает исключение `PrestaShopException`.

**Примеры**:

```python
# Удаление клиента с ID 3
result = prestacustomer.delete_customer_PrestaShop(customer_id=3)

if result:
    print('Клиент удален успешно.')
else:
    print('Ошибка при удалении клиента.')
```

### `update_customer_PrestaShop(self, customer_id: int, firstname: Optional[str] = None, lastname: Optional[str] = None, email: Optional[str] = None, **kwargs) -> dict | None`

**Назначение**: Обновляет информацию о клиенте в PrestaShop.

**Параметры**:

- `customer_id` (int): ID клиента для обновления.
- `firstname` (Optional[str], optional): Новое имя клиента. По умолчанию `None`.
- `lastname` (Optional[str], optional): Новая фамилия клиента. По умолчанию `None`.
- `email` (Optional[str], optional): Новый email клиента. По умолчанию `None`.

**Возвращает**:

- `dict | None`: Словарь с обновленной информацией о клиенте или `None` в случае ошибки.

**Вызывает исключения**:

- `PrestaShopException`: Если возникает ошибка при взаимодействии с API PrestaShop.

**Как работает метод**:

- Метод отправляет запрос на API PrestaShop для обновления информации о клиенте с помощью метода `PUT`.
- В запросе передаются параметры `customer_id`, `firstname`, `lastname` и `email` (если заданы).
- Если запрос выполнен успешно, метод возвращает словарь с обновленной информацией о клиенте.
- Если возникает ошибка, метод вызывает исключение `PrestaShopException`.

**Примеры**:

```python
# Обновление имени и фамилии клиента с ID 4
updated_customer_data = prestacustomer.update_customer_PrestaShop(
    customer_id=4,
    firstname='Updated',
    lastname='Customer'
)

# Вывод информации об обновленном клиенте
if updated_customer_data:
    print(f'Клиент обновлен: {updated_customer_data}')
else:
    print('Ошибка при обновлении клиента.')
```

### `get_customer_details_PrestaShop(self, customer_id: int) -> dict | None`

**Назначение**: Получает подробную информацию о клиенте из PrestaShop.

**Параметры**:

- `customer_id` (int): ID клиента.

**Возвращает**:

- `dict | None`: Словарь с информацией о клиенте или `None` в случае ошибки.

**Вызывает исключения**:

- `PrestaShopException`: Если возникает ошибка при взаимодействии с API PrestaShop.

**Как работает метод**:

- Метод отправляет запрос на API PrestaShop для получения информации о клиенте с помощью метода `GET`.
- В запросе передается параметр `customer_id`.
- Если запрос выполнен успешно, метод возвращает словарь с информацией о клиенте.
- Если возникает ошибка, метод вызывает исключение `PrestaShopException`.

**Примеры**:

```python
# Получение информации о клиенте с ID 5
customer_details = prestacustomer.get_customer_details_PrestaShop(customer_id=5)

# Вывод информации о клиенте
if customer_details:
    print(f'Информация о клиенте: {customer_details}')
else:
    print('Ошибка при получении информации о клиенте.')
```

## Параметры класса

- `api_domain` (str): Домен API PrestaShop.
- `api_key` (str): Ключ API PrestaShop.

## Примеры

```python
# Импорт необходимых модулей
from src.endpoints.prestashop.customer import PrestaCustomer

# Задание учетных данных для API PrestaShop
API_DOMAIN = 'https://example.com'
API_KEY = 'your_api_key'

# Создание экземпляра класса PrestaCustomer
prestacustomer = PrestaCustomer(API_DOMAIN=API_DOMAIN, API_KEY=API_KEY)

# Добавление нового клиента
new_customer_data = prestacustomer.add_customer_PrestaShop(
    firstname='John',
    lastname='Doe',
    email='johndoe@example.com',
    password='your_password'
)

# Вывод информации о новом клиенте
if new_customer_data:
    print(f'Новый клиент создан: {new_customer_data}')
else:
    print('Ошибка при создании клиента')

# Получение информации о клиенте с ID 5
customer_details = prestacustomer.get_customer_details_PrestaShop(customer_id=5)

# Вывод информации о клиенте
if customer_details:
    print(f'Информация о клиенте: {customer_details}')
else:
    print('Ошибка при получении информации о клиенте.')
```