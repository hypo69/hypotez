### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет класс `PrestaCustomer`, который предоставляет интерфейс для взаимодействия с API PrestaShop для управления клиентами. Класс позволяет добавлять, удалять, обновлять и получать информацию о клиентах в PrestaShop.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются необходимые модули, включая `sys`, `os`, `attr`, `Path`, `typing`, `SimpleNamespace`, `header`, `gs`, `logger`, `j_loads`, `PrestaShop`, `PrestaShopException` и `Optional`.
2. **Определение класса `PrestaCustomer`**: Создается класс `PrestaCustomer`, который наследуется от класса `PrestaShop`.
3. **Инициализация класса**: В методе `__init__` происходит инициализация клиента PrestaShop. Проверяется наличие параметров `api_domain` и `api_key`, которые могут быть переданы как отдельные аргументы или через словарь `credentials`. Если параметры отсутствуют, вызывается исключение `ValueError`.
4. **Инициализация родительского класса**: Вызывается метод `__init__` родительского класса `PrestaShop` с передачей параметров `api_domain` и `api_key`.

Пример использования
-------------------------

```python
from src.endpoints.prestashop.customer import PrestaCustomer
from types import SimpleNamespace

# Пример использования с передачей параметров через SimpleNamespace
credentials = SimpleNamespace(api_domain='your_api_domain', api_key='your_api_key')
prestacustomer = PrestaCustomer(credentials=credentials)

# или с передачей параметров напрямую
prestacustomer = PrestaCustomer(api_domain='your_api_domain', api_key='your_api_key')

# Добавление нового клиента
#prestacustomer.add_customer_PrestaShop('John Doe', 'johndoe@example.com')

# Удаление клиента
#prestacustomer.delete_customer_PrestaShop(3)

# Обновление информации о клиенте
#prestacustomer.update_customer_PrestaShop(4, 'Updated Customer Name')

# Получение информации о клиенте
#print(prestacustomer.get_customer_details_PrestaShop(5))