# Модуль сбора товаров со страницы категорий поставщика bangood.co.il

## Overview

Модуль сбора товаров со страницы категорий поставщика bangood.co.il через вебдрайвер. 

## Details

Этот модуль предоставляет функциональность для сбора списка категорий и товаров с сайта bangood.co.il. Он включает в себя функции для:

- **Сбора списка категорий:** `get_list_categories_from_site()`.
- **Сбора списка товаров с конкретной категории:** `get_list_products_in_category()`.

## Table of Contents

- [Функции](#функции)
    - [`get_list_products_in_category()`](#get_list_products_in_category)
    - [`get_list_categories_from_site()`](#get_list_categories_from_site)

## Функции

### `get_list_products_in_category()`

```python
def get_list_products_in_category (s) -> list[str, str, None]:    
    """ Returns list of products urls from category page
    Если надо пролистстать - страницы категорий - листаю ??????

    Attrs:
        s - Supplier
    @returns
        list or one of products urls or None
    """
    d = s.driver
    
    
    l: dict = s.locators['category']
    
    d.execute_locator (s.locators ['product']['close_banner'] )
    
    if not l:
        """ Много проверок, потому, что код можно запускать от лица разных ихполнителей: Supplier, Product, Scenario """
        logger.error(f"А где локаторы? {l}")
        return
    d.scroll()

    #TODO: Нет листалки

    list_products_in_category = d.execute_locator(l['product_links'])
    """ Собирал ссылки на товары.  """
    
    if not list_products_in_category:
        logger.warning('Нет ссылок на товары. Так бывает')
        return
    
    list_products_in_category = [list_products_in_category] if isinstance(list_products_in_category, str) else list_products_in_category

    logger.info(f""" Найдено {len(list_products_in_category)} товаров """)
    
    
    return list_products_in_category
```

**Purpose**: Эта функция собирает список URL-адресов товаров с заданной страницы категории.

**Parameters**:

- `s` (`Supplier`): Объект `Supplier`, содержащий информацию о поставщике (например, локаторы элементов, драйвер браузера).

**Returns**:

- `list[str, str, None]`: Возвращает список URL-адресов товаров, или `None`, если возникла ошибка или на странице не найдено товаров.

**How the Function Works**:

1. Функция получает объект `Supplier` в качестве аргумента.
2. Получает локаторы для элементов страницы категории из объекта `Supplier`.
3. Использует `driver.execute_locator()` для поиска и взаимодействия с элементами, например, закрытия баннера.
4. Использует `d.scroll()` для прокрутки страницы.
5. Выполняет поиск элементов с локатором `product_links` и извлекает список URL-адресов товаров.
6. Логирует количество найденных товаров.
7. Возвращает список URL-адресов товаров или `None`, если не удалось найти товары.

**Examples**:

```python
# Пример использования функции:
supplier = Supplier(...) # Создание объекта Supplier
product_urls = get_list_products_in_category(supplier)

# Обработка полученного списка URL-адресов товаров:
if product_urls:
    for product_url in product_urls:
        # Обработка каждой ссылки на товар (получение данных о товаре, сохранение информации)
        ...
else:
    # Обработка ситуации, когда не удалось найти товары на странице категории.
    ...
```

### `get_list_categories_from_site()`

```python
def get_list_categories_from_site(s):
    ...
```

**Purpose**:  Эта функция собирает список категорий с сайта.

**Parameters**:

- `s` (`Supplier`): Объект `Supplier`, содержащий информацию о поставщике (например, локаторы элементов, драйвер браузера).

**Returns**:

- ...:  Возвращает список категорий с сайта, или `None`, если возникла ошибка.

**How the Function Works**:

1. Функция получает объект `Supplier` в качестве аргумента.
2. Получает локаторы для элементов страницы категории из объекта `Supplier`.
3. Использует `driver.execute_locator()` для поиска и взаимодействия с элементами, например, закрытия баннера.
4. Использует `d.scroll()` для прокрутки страницы.
5. Выполняет поиск элементов с локатором `product_links` и извлекает список URL-адресов товаров.
6. Логирует количество найденных товаров.
7. Возвращает список URL-адресов товаров или `None`, если не удалось найти товары.

**Examples**:

```python
# Пример использования функции:
supplier = Supplier(...) # Создание объекта Supplier
category_urls = get_list_categories_from_site(supplier)

# Обработка полученного списка URL-адресов категорий:
if category_urls:
    for category_url in category_urls:
        # Обработка каждой ссылки на категорию (например, сбор товаров с этой категории)
        ...
else:
    # Обработка ситуации, когда не удалось найти категории на сайте.
    ...
```