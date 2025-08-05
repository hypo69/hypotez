# Модуль сбора товаров со страницы категорий поставщика bangood.co.il через вебдрайвер

## Обзор

Модуль `scenario.py` предназначен для сбора товаров со страниц категорий поставщика `bangood.co.il` с использованием вебдрайвера. 

## Подробнее

Модуль реализует следующие функции:

- `get_list_categories_from_site(s)`: собирает список категорий со страниц продавца.
- `get_list_products_in_category(s)`: собирает список товаров со страницы категории. 
- `grab_product_page(s)`: обрабатывает поля товара и передает управление классу `Product`.

##  Функции

### `get_list_products_in_category(s)`

**Назначение**: Функция собирает список товаров со страницы категории.

**Параметры**:
- `s` (Supplier): объект класса `Supplier`, содержащий информацию о поставщике, включая вебдрайвер, локаторы и другие настройки.

**Возвращает**:
- `list[str, str, None]`: список ссылок на товары, либо `None` в случае ошибки.

**Как работает функция**:

- Функция извлекает объект вебдрайвера `d` из объекта `s` (Supplier). 
- Выполняет `d.execute_locator(s.locators['product']['close_banner'])`, чтобы закрыть баннер, если он есть на странице.
- Проверяет наличие локаторов в объекте `s.locators['category']`.
- Выполняет прокрутку страницы с помощью `d.scroll()`.
- Извлекает ссылки на товары с помощью `d.execute_locator(l['product_links'])`. 
- Проверяет наличие ссылок на товары. Если ссылок нет, выводит предупреждение в лог с помощью `logger.warning`.
- Возвращает список ссылок на товары или `None`, если ссылок не найдено.

**Примеры**:
```python
from src.suppliers.suppliers_list.grandadvance import scenario
from src.suppliers.suppliers_list.grandadvance.supplier import GrandAdvance

# Создание объекта класса GrandAdvance
grandadvance = GrandAdvance()

# Вызов функции get_list_products_in_category
product_urls = scenario.get_list_products_in_category(grandadvance)

# Вывод полученного списка ссылок на товары
print(f'Product URLs: {product_urls}')

# Пример с ошибкой (отсутствующие локаторы)
grandadvance.locators['category'] = None
product_urls = scenario.get_list_products_in_category(grandadvance)
print(f'Product URLs: {product_urls}')
```


### `get_list_categories_from_site(s)`

**Назначение**: Функция собирает список категорий со страниц продавца.

**Параметры**:
- `s` (Supplier): объект класса `Supplier`, содержащий информацию о поставщике, включая вебдрайвер, локаторы и другие настройки.

**Возвращает**:
- `list[str]`: список категорий, либо `None` в случае ошибки.

**Как работает функция**:

- Извлекает вебдрайвер `d` из объекта `s` (Supplier).
- Выполняет `d.execute_locator(s.locators['product']['close_banner'])`, чтобы закрыть баннер, если он есть на странице.
- Проверяет наличие локатора `s.locators['categories_list']`.
- Выполняет `d.execute_locator(s.locators['categories_list'])`, чтобы получить список категорий.
- Возвращает список категорий, либо `None`, если ссылок не найдено.

**Примеры**:
```python
from src.suppliers.suppliers_list.grandadvance import scenario
from src.suppliers.suppliers_list.grandadvance.supplier import GrandAdvance

# Создание объекта класса GrandAdvance
grandadvance = GrandAdvance()

# Вызов функции get_list_categories_from_site
categories = scenario.get_list_categories_from_site(grandadvance)

# Вывод полученного списка категорий
print(f'Categories: {categories}')

# Пример с ошибкой (отсутствующие локаторы)
grandadvance.locators['categories_list'] = None
categories = scenario.get_list_categories_from_site(grandadvance)
print(f'Categories: {categories}')
```

### `grab_product_page(s)`

**Назначение**: Функция обрабатывает поля товара и передает управление классу `Product`.

**Параметры**:
- `s` (Supplier): объект класса `Supplier`, содержащий информацию о поставщике, включая вебдрайвер, локаторы и другие настройки.

**Возвращает**:
- `None`:  Функция не возвращает значение. 

**Как работает функция**:

- Извлекает вебдрайвер `d` из объекта `s` (Supplier).
- Выполняет `d.execute_locator(s.locators['product']['close_banner'])`, чтобы закрыть баннер, если он есть на странице.
- Выполняет прокрутку страницы с помощью `d.scroll()`.
- Извлекает значения полей товара с помощью `d.execute_locator(s.locators['product'])`.
- Создает объект класса `Product` с полученными значениями полей.
- Вызывает методы класса `Product` для обработки полученных данных.

**Примеры**:
```python
from src.suppliers.suppliers_list.grandadvance import scenario
from src.suppliers.suppliers_list.grandadvance.supplier import GrandAdvance
from src.suppliers.suppliers_list.grandadvance.product import Product

# Создание объекта класса GrandAdvance
grandadvance = GrandAdvance()

# Вызов функции grab_product_page
scenario.grab_product_page(grandadvance)

# Пример с ошибкой (отсутствующие локаторы)
grandadvance.locators['product'] = None
scenario.grab_product_page(grandadvance)