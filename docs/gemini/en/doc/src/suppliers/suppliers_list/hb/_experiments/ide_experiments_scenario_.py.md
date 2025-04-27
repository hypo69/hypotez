# Модуль проверки наполнения полей HB -> product_fields 
===================================================================

## Overview

Модуль предназначен для проверки наполнения полей в продуктах на сайте HB. 
В модуле используется `Supplier` объект для работы с сайтом HB. 
Функции модуля позволяют получить информацию о продуктах, проверить наличие обязательных полей, 
сравнить данные с данными на сайте PrestaShop. 
Также, в модуле используется `Driver` объект, который представляет собой WebDriver (Selenium) для работы с веб-страницами. 
В модуле используются функции из `src.scenario` и `src.logger` для управления сценариями тестирования и логгирования. 

## Table of Contents

- [Classes](#classes)
  - [`Supplier`](#supplier)
  - [`Product`](#product)
  - [`ProductFields`](#productfields)
- [Functions](#functions)
  - [`run_scenarios`](#run_scenarios)

## Classes

### `Supplier`

**Description**: Класс для работы с поставщиком HB.

**Inherits**:

**Attributes**:

- `supplier_prefix` (str): Префикс поставщика (например, 'hb').
- `locators` (dict): Словарь с локаторами для элементов на странице.
- `driver` (Driver): Объект WebDriver для работы с сайтом.
- `current_scenario` (dict): Словарь с текущим сценарием тестирования.

**Methods**:

- `get_product_data()`: Возвращает данные о продукте с текущей страницы.
- `get_product_fields()`: Возвращает список доступных полей продукта.
- `check_product_fields()`: Проверяет, заполнены ли обязательные поля продукта.
- `compare_product_data()`: Сравнивает данные о продукте с данными на сайте PrestaShop.

### `Product`

**Description**: Класс для работы с продуктом.

**Inherits**:

**Attributes**:

- `supplier` (Supplier): Объект Supplier, которому принадлежит продукт.
- `data` (dict): Словарь с данными о продукте.

**Methods**:

- `get_data()`: Возвращает данные о продукте.
- `get_fields()`: Возвращает список доступных полей продукта.
- `get_field_value(field_name: str) -> str | None`: Возвращает значение поля продукта.

### `ProductFields`

**Description**: Класс для работы с полями продукта.

**Inherits**:

**Attributes**:

- `supplier` (Supplier): Объект Supplier, которому принадлежит продукт.

**Methods**:

- `get_fields()`: Возвращает список доступных полей продукта.

## Functions

### `run_scenarios`

**Purpose**: Функция для запуска сценариев тестирования.

**Parameters**:

- `s` (Supplier): Объект Supplier.
- `scenario` (dict): Словарь с описанием сценария.

**Returns**:

- `None`:

**Raises Exceptions**:

- `ExecuteLocatorException`: Если возникла ошибка при выполнении локатора.

**How the Function Works**:

- Получает данные о продукте с текущей страницы.
- Проверяет, заполнены ли обязательные поля продукта.
- Сравнивает данные о продукте с данными на сайте PrestaShop.
- Записывает результаты в лог.

**Examples**:

```python
# Запуск сценария с заданными параметрами
ret = run_scenarios(s, s.current_scenario)
```

## Parameter Details

- `s` (Supplier): Объект `Supplier`, который содержит информацию о текущем поставщике. 
    - `supplier_prefix` (str): Префикс поставщика (например, `'hb'`).
    - `locators` (dict): Словарь с локаторами для элементов на странице.
    - `driver` (Driver): Объект `Driver` для работы с сайтом.
    - `current_scenario` (dict): Словарь с текущим сценарием тестирования.
- `scenario` (dict): Словарь с описанием сценария тестирования. 
    - `url` (str): URL страницы, с которой начинается сценарий.
    - `name` (str): Название сценария.
    - `condition` (str): Условие, которое должно быть выполнено для успешного завершения сценария.
    - `presta_categories` (dict): Словарь с категориями в PrestaShop. 
        - `default_category` (int): ID дефолтной категории в PrestaShop.
        - `additional_categories` (list): Список ID дополнительных категорий в PrestaShop.

**Examples**:

```python
# Создание объекта Supplier с префиксом 'hb'
s: Supplier = Supplier(supplier_prefix = 'hb')

# Определение локаторов для элементов на странице
l: dict = s.locators['product']

# Создание объекта Driver для работы с сайтом
d: Driver = s.driver

# Создание объекта ProductFields
f: ProductFields = ProductFields(s)

# Задание текущего сценария
s.current_scenario: dict =  {
    "url": "https://hbdeadsea.co.il/product-category/bodyspa/feet-hand-treatment/",
    "name": "טיפוח כפות ידיים ורגליים",
    "condition": "new",
    "presta_categories": {
        "default_category": 11259,
        "additional_categories": []
    }
}

# Запуск сценария
ret = run_scenarios(s, s.current_scenario)
```