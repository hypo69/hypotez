## Как использовать класс `PrestaCustomer`
=========================================================================================

Описание
-------------------------
Класс `PrestaCustomer` предоставляет набор методов для работы с клиентами в системе PrestaShop. 

Шаги выполнения
-------------------------
1. **Инициализация объекта `PrestaCustomer`**: 
    - Передайте необходимые параметры в конструктор класса:
        - `credentials` (Optional[dict | SimpleNamespace]): Словарь или объект SimpleNamespace с параметрами `api_domain` и `api_key`. 
        - `api_domain` (Optional[str]): Домен API.
        - `api_key` (Optional[str]): Ключ API. 
    - Если переданы `credentials`, класс автоматически извлечёт значения `api_domain` и `api_key` из них.
    - Если `credentials` не передан, то необходимо передать `api_domain` и `api_key` отдельно.
    - Если ни один из параметров не передан, то будет вызвана ошибка `ValueError`
2. **Использование методов**:
    - Класс `PrestaCustomer` предоставляет следующие методы:
        - `add_customer_PrestaShop(customer_name: str, customer_email: str)`: Добавляет нового клиента в PrestaShop.
        - `delete_customer_PrestaShop(customer_id: int)`: Удаляет клиента из PrestaShop по его ID.
        - `update_customer_PrestaShop(customer_id: int, customer_name: str)`: Обновляет имя клиента в PrestaShop по его ID.
        - `get_customer_details_PrestaShop(customer_id: int)`: Возвращает информацию о клиенте в виде словаря.
   
Пример использования
-------------------------

```python
from src.endpoints.prestashop.customer import PrestaCustomer

# Пример 1: Использование credentials
credentials = {
    'api_domain': 'example.com',
    'api_key': 'your_api_key'
}
prestacustomer = PrestaCustomer(credentials=credentials)

# Пример 2: Использование api_domain и api_key
prestacustomer = PrestaCustomer(api_domain='example.com', api_key='your_api_key')

# Добавление нового клиента
prestacustomer.add_customer_PrestaShop('John Doe', 'johndoe@example.com')

# Удаление клиента по ID
prestacustomer.delete_customer_PrestaShop(3)

# Обновление имени клиента по ID
prestacustomer.update_customer_PrestaShop(4, 'Updated Customer Name')

# Получение информации о клиенте по ID
customer_details = prestacustomer.get_customer_details_PrestaShop(5)
print(customer_details)
```