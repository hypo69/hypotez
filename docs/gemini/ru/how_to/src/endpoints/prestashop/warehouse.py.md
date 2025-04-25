## Как использовать класс PrestaWarehouse
=========================================================================================

Описание
-------------------------
Класс `PrestaWarehouse`  расширяет класс `PrestaShop` и предоставляет функциональность для работы со складами в PrestaShop. 

Шаги выполнения
-------------------------
1. **Инициализация**:  Создайте экземпляр класса `PrestaWarehouse` с помощью аргументов,  определенных в базовом классе `PrestaShop`.
2. **Использование методов**: Используйте доступные методы класса `PrestaWarehouse` для работы со складами в PrestaShop.

Пример использования
-------------------------

```python
from src.endpoints.prestashop.warehouse import PrestaWarehouse

# Инициализация класса
warehouse = PrestaWarehouse(
    api_url='http://your-prestashop-domain.com/api/',
    api_key='your-api-key',
)

# Пример вызова метода: получить список складов 
warehouses = warehouse.get_warehouses()

# Вывод результатов
pprint(warehouses)
```

**Важно**: Замените  `'http://your-prestashop-domain.com/api/'` и `'your-api-key'` на свои действительные значения.