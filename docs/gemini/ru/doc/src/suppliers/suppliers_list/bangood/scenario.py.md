# Модуль сбора товаров со страницы категорий поставщика bangood.co.il через вебдрайвер

## Обзор

Модуль `scenario.py`  предназначен для сбора товаров со страниц категорий поставщика `bangood.co.il` с использованием вебдрайвера. В нем определены функции, которые:

- Собирают список категорий со страниц продавца `get_list_categories_from_site()`.
- Собирают список товаров со страницы категории `get_list_products_in_category()`. 
- Обрабатывают информацию о товаре `grab_product_page()` и передают ее в класс `Product`.

## Подробнее

**Модуль работает следующим образом:**

1.  **Сбор категорий:** 
    - Функция `get_list_categories_from_site()` собирает список категорий со страниц продавца.
    - Она использует вебдрайвер (`s.driver`) для получения HTML-кода страницы категорий.
    - Выполняет парсинг HTML-кода с помощью локатора `s.locators['category']` и извлекает список ссылок на категории.
2.  **Сбор товаров:**
    - Функция `get_list_products_in_category()` собирает список товаров со страницы категории.
    - Она использует вебдрайвер (`s.driver`) для получения HTML-кода страницы категории.
    - Выполняет парсинг HTML-кода с помощью локатора `s.locators['product_links']` и извлекает список ссылок на товары.
3.  **Обработка товаров:**
    - Функция `grab_product_page()` обрабатывает информацию о товаре, полученную со страницы товара.
    - Она использует вебдрайвер (`s.driver`) для получения HTML-кода страницы товара.
    - Выполняет парсинг HTML-кода с помощью локаторов `s.locators['product']` и извлекает информацию о товаре.
    - Передает обработанные данные в класс `Product`.

## Функции

### `get_list_products_in_category`

**Назначение**: Получение списка товаров со страницы категории.

**Параметры**:

- `s` (Supplier): Экземпляр класса `Supplier`, содержащий информацию о поставщике.

**Возвращает**:

- list[str, str, None]: Список URL-адресов товаров на странице категории, либо None, если не найдены товары.

**Вызывает исключения**:

- `None`: В случае возникновения ошибки логгирует предупреждение в `logger.warning()`.

**Как работает функция**:

1.  Получает доступ к вебдрайверу (`s.driver`).
2.  Выполняет локатор `s.locators['product']['close_banner']` для закрытия рекламных баннеров.
3.  Проверяет наличие локаторов `s.locators['category']`. Если локаторы отсутствуют, выводит ошибку в лог.
4.  Выполняет прокрутку страницы вниз (`d.scroll()`). 
5.  Получает ссылки на товары с помощью локатора `l['product_links']`.
6.  Логгирует количество найденных товаров.

**Примеры**:

```python
# Пример вызова функции с передачей экземпляра класса Supplier:
supplier = Supplier(...)  # Инициализация экземпляра класса Supplier
products_urls = get_list_products_in_category(supplier)

# Проверка на наличие списка товаров:
if products_urls:
    print(f"Найдено товаров: {len(products_urls)}")
else:
    print("Товаров не найдено.")
```

### `get_list_categories_from_site`

**Назначение**: Получение списка категорий со страниц продавца.

**Параметры**:

- `s` (Supplier): Экземпляр класса `Supplier`, содержащий информацию о поставщике.

**Возвращает**:

- list: Список ссылок на категории, либо None, если не найдено категорий.

**Вызывает исключения**:

- `None`: В случае возникновения ошибки логгирует предупреждение в `logger.warning()`.

**Как работает функция**:

1.  Получает доступ к вебдрайверу (`s.driver`).
2.  Выполняет локатор `s.locators['category']` для получения списка категорий.
3.  Выполняет парсинг HTML-кода и извлекает ссылки на категории.
4.  Проверяет наличие категорий. Если категории отсутствуют, выводит ошибку в лог.
5.  Логгирует количество найденных категорий.

**Примеры**:

```python
# Пример вызова функции с передачей экземпляра класса Supplier:
supplier = Supplier(...)  # Инициализация экземпляра класса Supplier
categories_urls = get_list_categories_from_site(supplier)

# Проверка на наличие списка категорий:
if categories_urls:
    print(f"Найдено категорий: {len(categories_urls)}")
else:
    print("Категорий не найдено.")
```


## Внутренние функции:

В текущей реализации `scenario.py` нет внутренних функций.

## Параметры класса:

- `s.locators['product']['close_banner']`: Локатор для закрытия рекламных баннеров на странице товара.
- `s.locators['product_links']`: Локатор для получения ссылок на товары.
- `s.locators['category']`: Локатор для получения списка категорий.

## Примеры:

**Примеры вызова функции `get_list_products_in_category`:**

```python
# Пример вызова функции с передачей экземпляра класса Supplier:
from src.suppliers.suppliers_list.bangood.scenario import get_list_products_in_category
from src.suppliers.suppliers_list.bangood.supplier import Supplier

# Инициализация экземпляра класса Supplier (может потребоваться дополнительная настройка)
supplier = Supplier(
    name="Bangood",
    driver_type=Chrome,
    site_url="https://www.bangood.com/en",
    currency="ILS",
    locators={"product": {"close_banner": {"by": "XPATH", "selector": "//button[@id = 'closeXButton']", "event": "click()"}, "product_links": {"by": "XPATH", "selector": "//div[@class = 'product-box']//a/@href"}}, "category": {"by": "XPATH", "selector": "//div[@class = 'product-list']//a/@href"}},
    )

# Получение списка товаров со страницы категории
products_urls = get_list_products_in_category(supplier)

# Вывод результатов
if products_urls:
    print(f"Найдено товаров: {len(products_urls)}")
    print("Список товаров:", products_urls)
else:
    print("Товаров не найдено.")

```

**Примеры вызова функции `get_list_categories_from_site`:**

```python
# Пример вызова функции с передачей экземпляра класса Supplier:
from src.suppliers.suppliers_list.bangood.scenario import get_list_categories_from_site
from src.suppliers.suppliers_list.bangood.supplier import Supplier

# Инициализация экземпляра класса Supplier (может потребоваться дополнительная настройка)
supplier = Supplier(
    name="Bangood",
    driver_type=Chrome,
    site_url="https://www.bangood.com/en",
    currency="ILS",
    locators={"product": {"close_banner": {"by": "XPATH", "selector": "//button[@id = 'closeXButton']", "event": "click()"}, "product_links": {"by": "XPATH", "selector": "//div[@class = 'product-box']//a/@href"}}, "category": {"by": "XPATH", "selector": "//div[@class = 'product-list']//a/@href"}},
    )

# Получение списка категорий со страниц продавца
categories_urls = get_list_categories_from_site(supplier)

# Вывод результатов
if categories_urls:
    print(f"Найдено категорий: {len(categories_urls)}")
    print("Список категорий:", categories_urls)
else:
    print("Категорий не найдено.")
```