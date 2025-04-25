## Как использовать класс `PrestaSupplier`
=========================================================================================

Описание
-------------------------
Класс `PrestaSupplier`  предназначен для взаимодействия с API платформы PrestaShop, предоставляя  функциональность  для управления данными поставщиков.

Шаги выполнения
-------------------------
1. **Инициализация:**
   - Создайте экземпляр класса `PrestaSupplier`, передав необходимые параметры:
     - `credentials` (необязательно): Словарь или объект `SimpleNamespace` с ключами `api_domain` и `api_key`, содержащими  домен и ключ API PrestaShop.
     - `api_domain` (необязательно): Домен API PrestaShop.
     - `api_key` (необязательно): Ключ API PrestaShop.
     -  Если  `credentials`  не указан, должны быть заданы `api_domain` и `api_key` как отдельные аргументы.

2. **Использование методов:**
   -  После инициализации вы можете использовать  методы класса `PrestaSupplier` для взаимодействия с API. 
   - Доступные методы зависят от конкретной реализации класса.

Пример использования
-------------------------

```python
from src.endpoints.prestashop.supplier import PrestaSupplier

# Используйте объект `credentials` с доменом и ключом API
credentials = {
    'api_domain': 'https://your-prestashop-domain.com',
    'api_key': 'your-api-key'
}

# Инициализация класса `PrestaSupplier` с помощью объекта `credentials`
supplier = PrestaSupplier(credentials=credentials)

# Или инициализация  с  `api_domain`  и  `api_key`  как отдельные аргументы
supplier = PrestaSupplier(api_domain='https://your-prestashop-domain.com', api_key='your-api-key')

# Пример вызова метода для получения информации о поставщике
# (метод должен быть реализован в классе)
supplier_info = supplier.get_supplier_info(supplier_id=123)
```