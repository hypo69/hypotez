# Модуль для работы со складами PrestaShop

## Обзор

Модуль `src/endpoints/prestashop/warehouse.py` предоставляет класс `PrestaWarehouse`, который расширяет функциональность `PrestaShop` для работы с данными о складах в PrestaShop.

## Классы

### `PrestaWarehouse`

**Описание**: Класс `PrestaWarehouse` расширяет функциональность `PrestaShop` для работы с данными о складах в PrestaShop.

**Наследует**:
    - `PrestaShop`

**Атрибуты**: 
    - `warehouse_id`: идентификатор склада

**Методы**:
    - `get_warehouses()`: Возвращает список всех складов.
    - `get_warehouse_by_id(warehouse_id: int) -> dict`: Возвращает информацию о складе по его идентификатору.
    - `create_warehouse(name: str, address: str, zipcode: str, city: str, country_id: int, phone: str) -> int`: Создает новый склад.
    - `update_warehouse(warehouse_id: int, name: str = None, address: str = None, zipcode: str = None, city: str = None, country_id: int = None, phone: str = None) -> bool`: Обновляет информацию о складе.
    - `delete_warehouse(warehouse_id: int) -> bool`: Удаляет склад.

## Функции

### `get_warehouse_by_id`

**Назначение**: Возвращает информацию о складе по его идентификатору.

**Параметры**:
    - `warehouse_id` (int): Идентификатор склада.

**Возвращает**:
    - `dict`: Словарь с информацией о складе.

**Примеры**:

```python
from src.endpoints.prestashop.warehouse import PrestaWarehouse

# Создание инстанса класса PrestaWarehouse
warehouse = PrestaWarehouse()

# Получение информации о складе с идентификатором 1
warehouse_data = warehouse.get_warehouse_by_id(1)

# Вывод информации о складе
pprint(warehouse_data)
```

## Методы класса

### `get_warehouses`

```python
    def get_warehouses(self) -> list:
        """
        Возвращает список всех складов.

        Args:
            None

        Returns:
            list: Список словарей с информацией о складах.

        Raises:
            Exception: Если возникла ошибка при получении данных.
        """
        ...
```

### `get_warehouse_by_id`

```python
    def get_warehouse_by_id(self, warehouse_id: int) -> dict:
        """
        Возвращает информацию о складе по его идентификатору.

        Args:
            warehouse_id (int): Идентификатор склада.

        Returns:
            dict: Словарь с информацией о складе.

        Raises:
            Exception: Если возникла ошибка при получении данных.
        """
        ...
```

### `create_warehouse`

```python
    def create_warehouse(self, name: str, address: str, zipcode: str, city: str, country_id: int, phone: str) -> int:
        """
        Создает новый склад.

        Args:
            name (str): Название склада.
            address (str): Адрес склада.
            zipcode (str): Почтовый индекс склада.
            city (str): Город склада.
            country_id (int): Идентификатор страны склада.
            phone (str): Телефон склада.

        Returns:
            int: Идентификатор созданного склада.

        Raises:
            Exception: Если возникла ошибка при создании склада.
        """
        ...
```

### `update_warehouse`

```python
    def update_warehouse(self, warehouse_id: int, name: str = None, address: str = None, zipcode: str = None, city: str = None, country_id: int = None, phone: str = None) -> bool:
        """
        Обновляет информацию о складе.

        Args:
            warehouse_id (int): Идентификатор склада.
            name (str, optional): Новое название склада. По умолчанию None.
            address (str, optional): Новый адрес склада. По умолчанию None.
            zipcode (str, optional): Новый почтовый индекс склада. По умолчанию None.
            city (str, optional): Новый город склада. По умолчанию None.
            country_id (int, optional): Новый идентификатор страны склада. По умолчанию None.
            phone (str, optional): Новый телефон склада. По умолчанию None.

        Returns:
            bool: True, если обновление прошло успешно, False в противном случае.

        Raises:
            Exception: Если возникла ошибка при обновлении склада.
        """
        ...
```

### `delete_warehouse`

```python
    def delete_warehouse(self, warehouse_id: int) -> bool:
        """
        Удаляет склад.

        Args:
            warehouse_id (int): Идентификатор склада.

        Returns:
            bool: True, если удаление прошло успешно, False в противном случае.

        Raises:
            Exception: Если возникла ошибка при удалении склада.
        """
        ...
```

## Примеры

```python
from src.endpoints.prestashop.warehouse import PrestaWarehouse

# Создание инстанса класса PrestaWarehouse
warehouse = PrestaWarehouse()

# Получение списка всех складов
warehouses = warehouse.get_warehouses()

# Вывод информации о складах
pprint(warehouses)

# Создание нового склада
new_warehouse_id = warehouse.create_warehouse(
    name='Новый склад',
    address='Адрес склада',
    zipcode='Почтовый индекс',
    city='Город',
    country_id=1,
    phone='+7(999)999-99-99',
)

# Получение информации о созданном складе
new_warehouse_data = warehouse.get_warehouse_by_id(new_warehouse_id)

# Вывод информации о созданном складе
pprint(new_warehouse_data)

# Обновление информации о складе
warehouse.update_warehouse(
    warehouse_id=new_warehouse_id,
    name='Обновленное название склада',
)

# Удаление склада
warehouse.delete_warehouse(new_warehouse_id)
```