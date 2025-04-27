# Модуль сбора товаров со страницы категорий поставщика bangood.co.il через вебдрайвер

## Обзор

Модуль сбора товаров со страницы категорий поставщика bangood.co.il через вебдрайвер. 

## Детали

- Модуль собирает список категорий со страниц продавца. `get_list_categories_from_site()`
- Собирает список товаров со страницы категории `get_list_products_in_category()`
- Итерируясь по списку, передает управление в `grab_product_page()`, отсылая функции текущий url страницы.
- `grab_product_page()` обрабатывает поля товара и передает управление классу `Product`

##  Функции

### `get_list_products_in_category` 

**Описание**: Возвращает список url товаров со страницы категории. 

**Параметры**:
- `s` (Supplier): Поставщик.

**Возвращаемое значение**: 
- `list[str, str, None]`: Список url товаров или `None`, если на странице не найдено товаров.

**Исключения**: 
- `Exception`: Если возникла ошибка при обработке страницы.

**Пример**:
```python
# Пример вызова функции:
supplier = Supplier(
    driver=Driver(Chrome),
    locators={'category': {'product_links': {'attribute': 'href', 'by': 'XPATH', 'selector': '//a[contains(@href, "/product/")]', 'if_list': 'all', 'use_mouse': False, 'mandatory': False, 'timeout': 0, 'timeout_for_event': 'presence_of_element_located', 'event': None, 'locator_description': 'Сбор ссылок на товары с категории'}},
    'product': {'close_banner': {'attribute': null, 'by': 'XPATH', 'selector': "//button[@id = 'closeXButton']", 'if_list': 'first', 'use_mouse': False, 'mandatory': False, 'timeout': 0, 'timeout_for_event': 'presence_of_element_located', 'event': 'click()', 'locator_description': 'Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)'}}
)
products_urls = get_list_products_in_category(supplier)
```

**Как работает функция**:

1. Извлекает данные о локаторах для страницы категории из объекта `Supplier`.
2. Использует `d.execute_locator` для получения списка ссылок на товары со страницы.
3. Возвращает полученный список ссылок.

### `get_list_categories_from_site`

**Описание**: Собирает список категорий со страниц продавца. 

**Параметры**:
- `s` (Supplier): Поставщик.

**Возвращаемое значение**: 
- `list[str, str, None]`: Список url категорий или `None`, если на странице не найдено категорий.

**Исключения**: 
- `Exception`: Если возникла ошибка при обработке страницы.

**Пример**:
```python
# Пример вызова функции:
supplier = Supplier(
    driver=Driver(Chrome),
    locators={'category': {'product_links': {'attribute': 'href', 'by': 'XPATH', 'selector': '//a[contains(@href, "/product/")]', 'if_list': 'all', 'use_mouse': False, 'mandatory': False, 'timeout': 0, 'timeout_for_event': 'presence_of_element_located', 'event': None, 'locator_description': 'Сбор ссылок на товары с категории'}},
    'product': {'close_banner': {'attribute': null, 'by': 'XPATH', 'selector': "//button[@id = 'closeXButton']", 'if_list': 'first', 'use_mouse': False, 'mandatory': False, 'timeout': 0, 'timeout_for_event': 'presence_of_element_located', 'event': 'click()', 'locator_description': 'Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)'}}
)
categories_urls = get_list_categories_from_site(supplier)
```

**Как работает функция**:

1. Извлекает данные о локаторах для страницы категорий из объекта `Supplier`.
2. Использует `d.execute_locator` для получения списка ссылок на категории со страницы.
3. Возвращает полученный список ссылок.