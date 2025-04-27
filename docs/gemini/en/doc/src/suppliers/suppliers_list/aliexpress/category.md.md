# AliExpress Category Management Module

## Overview

This module provides functionality for managing categories on AliExpress. It allows for retrieving product URLs, updating category lists, and interacting with the AliExpress platform for category synchronization.

## Table of Contents

- [Functions](#functions)
    - [`get_list_products_in_category(s: Supplier) -> list[str, str]`](#get_list_products_in_category-s-supplier--liststr-str)
    - [`get_prod_urls_from_pagination(s: Supplier) -> list[str]`](#get_prod_urls_from_pagination-s-supplier--liststr)
    - [`update_categories_in_scenario_file(s: Supplier, scenario_filename: str) -> bool`](#update_categories_in_scenario_file-s-supplier-scenario_filename-str--bool)
    - [`get_list_categories_from_site(s: Supplier, scenario_file: str, brand: str = '') -> list`](#get_list_categories_from_site-s-supplier-scenario_file-str-brand-str--list)
- [Classes](#classes)
    - [`DBAdaptor`](#dbadaptor)
- [Dependencies](#dependencies)
- [Usage Example](#usage-example)
- [License](#license)

## Functions

### `get_list_products_in_category(s: Supplier) -> list[str, str]`

Извлекает список URL-адресов товаров со страницы категории, включая пагинацию.

#### Parameters:

- `s` (`Supplier`): Экземпляр поставщика с драйвером браузера и локаторами.

#### Returns:

- Список URL-адресов товаров со страницы категории.

---

### `get_prod_urls_from_pagination(s: Supplier) -> list[str]`

Извлекает URL-адреса товаров со страниц категории, обрабатывая пагинацию.

#### Parameters:

- `s` (`Supplier`): Экземпляр поставщика с драйвером браузера и локаторами.

#### Returns:

- Список URL-адресов товаров.

---

### `update_categories_in_scenario_file(s: Supplier, scenario_filename: str) -> bool`

Сравнивает категории на сайте с теми, что есть в предоставленном файле сценария, и обновляет файл изменениями.

#### Parameters:

- `s` (`Supplier`): Экземпляр поставщика с драйвером браузера и локаторами.
- `scenario_filename` (`str`): Название файла сценария, который нужно обновить.

#### Returns:

- `True`, если категории были успешно обновлены, `False` в противном случае.

---

### `get_list_categories_from_site(s: Supplier, scenario_file: str, brand: str = '') -> list`

Извлекает список категорий с сайта AliExpress, исходя из предоставленного файла сценария.

#### Parameters:

- `s` (`Supplier`): Экземпляр поставщика с драйвером браузера и локаторами.
- `scenario_file` (`str`): Файл сценария, содержащий информацию о категориях.
- `brand` (`str`, optional): Фильтр по бренду для категорий.

#### Returns:

- Список категорий с сайта.

---

## Classes

### `DBAdaptor`

Предоставляет методы для взаимодействия с базой данных, позволяющие выполнять стандартные операции, такие как `SELECT`, `INSERT`, `UPDATE` и `DELETE` над записями `AliexpressCategory`.

#### Methods:

- `select`: Извлекает записи из таблицы `AliexpressCategory`.
- `insert`: Вставляет новую запись в таблицу `AliexpressCategory`.
- `update`: Обновляет существующую запись в таблице `AliexpressCategory`.
- `delete`: Удаляет запись из таблицы `AliexpressCategory`.

---

## Dependencies

Этот модуль использует несколько других модулей для различных функциональных возможностей:

- `src.db.manager_categories.suppliers_categories`: Для управления категориями в базе данных.
- `src.utils.jjson`: Для работы с JSON-данными.
- `src.logger`: Для регистрации ошибок и сообщений.
- `requests`: Для отправки HTTP-запросов для получения данных о категориях с сайта AliExpress.

---

## Usage Example

```python
from src.suppliers.suppliers_list.aliexpress.category import get_list_products_in_category, update_categories_in_scenario_file

# Example usage
supplier_instance = Supplier()
category_urls = get_list_products_in_category(supplier_instance)
update_categories_in_scenario_file(supplier_instance, 'example_scenario.json')
```

---

## License

Этот модуль лицензирован под лицензией MIT.