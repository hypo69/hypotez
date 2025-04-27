# PrestaShop Warehouse Endpoint

## Overview

This module defines the `PrestaWarehouse` class, which is responsible for managing warehouse operations within the PrestaShop e-commerce platform. It extends the `PrestaShop` class to provide specific functionality related to warehouses.

## Details

The `PrestaWarehouse` class inherits from the `PrestaShop` class, providing access to the PrestaShop API and implementing warehouse-related operations. It utilizes the `src.logger.logger` module for logging information and errors during execution.

## Classes

### `PrestaWarehouse`

**Description**: This class represents a PrestaShop warehouse and provides methods for interacting with warehouse-related data and operations.

**Inherits**: `PrestaShop`

**Attributes**: 

**Methods**: 

    - `get_warehouse_id(product_id: int, warehouse_name: str) -> Optional[int]`: This method retrieves the warehouse ID associated with a given product ID and warehouse name.

    - `product_has_warehouse(product_id: int, warehouse_id: int) -> bool`: This method checks if a product is assigned to a specific warehouse.

    - `product_assign_to_warehouse(product_id: int, warehouse_id: int) -> bool`: This method assigns a product to a specific warehouse.

    - `update_warehouse_id(product_id: int, warehouse_id: int) -> bool`: This method updates the warehouse ID for a given product.

    - `get_warehouse_name(warehouse_id: int) -> str`: This method retrieves the name of the warehouse based on its ID.

    - `get_warehouse_data(warehouse_id: int) -> dict`: This method retrieves warehouse data for the specified warehouse ID.

    - `get_warehouse_ids(product_id: int) -> list`: This method retrieves a list of warehouse IDs associated with a product.

    - `get_warehouses() -> list`: This method retrieves a list of all warehouses available in the PrestaShop store.

    - `get_stock_available(product_id: int) -> Optional[int]`: This method retrieves the stock availability of a product.


## Class Methods

### `get_warehouse_id`

```python
def get_warehouse_id(self, product_id: int, warehouse_name: str) -> Optional[int]:
    """
    Получает ID склада, связанного с продуктом.

    Args:
        product_id (int): ID продукта.
        warehouse_name (str): Название склада.

    Returns:
        Optional[int]: ID склада, если он найден.
    """
    warehouse = self.get_warehouses(product_id=product_id)
    if not warehouse:
        logger.error(f'Product {product_id} is not assigned to any warehouse')
        return None

    for w in warehouse:
        if w.get('name') == warehouse_name:
            return w.get('id')

    logger.error(f'Product {product_id} is not assigned to warehouse {warehouse_name}')
    return None

```

### `product_has_warehouse`

```python
    def product_has_warehouse(self, product_id: int, warehouse_id: int) -> bool:
        """
        Проверяет, назначен ли продукт на склад.

        Args:
            product_id (int): ID продукта.
            warehouse_id (int): ID склада.

        Returns:
            bool: True, если продукт назначен на склад, False в противном случае.
        """
        warehouses = self.get_warehouse_ids(product_id)
        if warehouses:
            return warehouse_id in warehouses
        return False
```

### `product_assign_to_warehouse`

```python
    def product_assign_to_warehouse(self, product_id: int, warehouse_id: int) -> bool:
        """
        Назначает продукт на склад.

        Args:
            product_id (int): ID продукта.
            warehouse_id (int): ID склада.

        Returns:
            bool: True, если продукт назначен на склад, False в противном случае.
        """
        data = {
            "product_id": product_id,
            "warehouse_id": warehouse_id,
        }
        try:
            res = self.post(endpoint='products/{product_id}/warehouses', data=data, product_id=product_id)
            if res.status_code == 201:
                logger.info(f'Product {product_id} assigned to warehouse {warehouse_id}')
                return True
            else:
                logger.error(f'Error assigning product {product_id} to warehouse {warehouse_id}. Response: {res.text}')
                return False
        except Exception as ex:
            logger.error(f'Error assigning product {product_id} to warehouse {warehouse_id}. Exception: {ex}')
            return False
```

### `update_warehouse_id`

```python
    def update_warehouse_id(self, product_id: int, warehouse_id: int) -> bool:
        """
        Обновляет ID склада для продукта.

        Args:
            product_id (int): ID продукта.
            warehouse_id (int): ID склада.

        Returns:
            bool: True, если ID склада обновлен, False в противном случае.
        """
        data = {
            "warehouse_id": warehouse_id,
        }
        try:
            res = self.put(endpoint='products/{product_id}/warehouses', data=data, product_id=product_id)
            if res.status_code == 200:
                logger.info(f'Warehouse ID for product {product_id} updated to {warehouse_id}')
                return True
            else:
                logger.error(f'Error updating warehouse ID for product {product_id}. Response: {res.text}')
                return False
        except Exception as ex:
            logger.error(f'Error updating warehouse ID for product {product_id}. Exception: {ex}')
            return False
```

### `get_warehouse_name`

```python
    def get_warehouse_name(self, warehouse_id: int) -> str:
        """
        Получает название склада по ID.

        Args:
            warehouse_id (int): ID склада.

        Returns:
            str: Название склада.
        """
        warehouse = self.get_warehouse_data(warehouse_id)
        if warehouse:
            return warehouse.get('name')
        return ''
```

### `get_warehouse_data`

```python
    def get_warehouse_data(self, warehouse_id: int) -> dict:
        """
        Получает данные о складе.

        Args:
            warehouse_id (int): ID склада.

        Returns:
            dict: Данные о складе, если он найден.
        """
        try:
            res = self.get(endpoint='warehouses/{warehouse_id}', warehouse_id=warehouse_id)
            if res.status_code == 200:
                return res.json()
            else:
                logger.error(f'Error getting warehouse data. Response: {res.text}')
                return {}
        except Exception as ex:
            logger.error(f'Error getting warehouse data. Exception: {ex}')
            return {}
```

### `get_warehouse_ids`

```python
    def get_warehouse_ids(self, product_id: int) -> list:
        """
        Получает список ID складов, связанных с продуктом.

        Args:
            product_id (int): ID продукта.

        Returns:
            list: Список ID складов.
        """
        try:
            res = self.get(endpoint='products/{product_id}/warehouses', product_id=product_id)
            if res.status_code == 200:
                return [w.get('id') for w in res.json()]
            else:
                logger.error(f'Error getting warehouse IDs for product {product_id}. Response: {res.text}')
                return []
        except Exception as ex:
            logger.error(f'Error getting warehouse IDs for product {product_id}. Exception: {ex}')
            return []
```

### `get_warehouses`

```python
    def get_warehouses(self, product_id: int = None) -> list:
        """
        Получает список всех складов.

        Args:
            product_id (int, optional): ID продукта. Defaults to None.

        Returns:
            list: Список всех складов.
        """
        if product_id:
            try:
                res = self.get(endpoint='products/{product_id}/warehouses', product_id=product_id)
                if res.status_code == 200:
                    return res.json()
                else:
                    logger.error(f'Error getting warehouses for product {product_id}. Response: {res.text}')
                    return []
            except Exception as ex:
                logger.error(f'Error getting warehouses for product {product_id}. Exception: {ex}')
                return []
        else:
            try:
                res = self.get(endpoint='warehouses')
                if res.status_code == 200:
                    return res.json()
                else:
                    logger.error(f'Error getting warehouses. Response: {res.text}')
                    return []
            except Exception as ex:
                logger.error(f'Error getting warehouses. Exception: {ex}')
                return []
```

### `get_stock_available`

```python
    def get_stock_available(self, product_id: int) -> Optional[int]:
        """
        Получает количество доступных на складе товаров.

        Args:
            product_id (int): ID продукта.

        Returns:
            Optional[int]: Количество доступных товаров.
        """
        product = self.get_product_data(product_id=product_id)
        if product:
            return product.get('quantity')
        return None
```

## Parameter Details

- `product_id` (int): ID продукта в PrestaShop.
- `warehouse_id` (int): ID склада в PrestaShop.
- `warehouse_name` (str): Название склада.

## Examples

```python
# Создание экземпляра класса PrestaWarehouse
warehouse = PrestaWarehouse()

# Получение ID склада по имени
warehouse_id = warehouse.get_warehouse_id(product_id=123, warehouse_name='Main Warehouse')

# Проверка, назначен ли продукт на склад
is_assigned = warehouse.product_has_warehouse(product_id=123, warehouse_id=warehouse_id)

# Назначение продукта на склад
success = warehouse.product_assign_to_warehouse(product_id=123, warehouse_id=warehouse_id)

# Обновление ID склада для продукта
success = warehouse.update_warehouse_id(product_id=123, warehouse_id=warehouse_id)

# Получение названия склада по ID
warehouse_name = warehouse.get_warehouse_name(warehouse_id=warehouse_id)

# Получение данных о складе
warehouse_data = warehouse.get_warehouse_data(warehouse_id=warehouse_id)

# Получение списка ID складов, связанных с продуктом
warehouse_ids = warehouse.get_warehouse_ids(product_id=123)

# Получение списка всех складов
warehouses = warehouse.get_warehouses()

# Получение количества доступных товаров на складе
stock_available = warehouse.get_stock_available(product_id=123)
```

## How the Function Works

This module provides the necessary functions to interact with PrestaShop's warehouse data.  You can retrieve information about a warehouse by its ID or name, assign products to specific warehouses, and update product assignments. The module also provides methods for fetching stock availability information for products. 

The `PrestaWarehouse` class extends the `PrestaShop` class, which provides a base for interacting with the PrestaShop API. This allows `PrestaWarehouse` to utilize API calls to retrieve and update warehouse data.