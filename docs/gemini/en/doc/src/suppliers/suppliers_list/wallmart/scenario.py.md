# Модуль сбора товаров со страницы категорий поставщика kualastyle.il через вебдрайвер
=================================================================================================

## Обзор

Модуль сбора товаров со страницы категорий поставщика kualastyle.il через вебдрайвер. У каждого поставщика свой сценарий обработки категорий. 

## Детали

- Модуль собирает список категорий со страниц продавца (`get_list_categories_from_site()`).
  @todo Сделать проверку на изменение категорий на страницах продавца. Продавец может добавлять новые категории, переименовывать или удалять/прятать уже существующие. По большому счету надо держать таблицу категории `PrestaShop.categories <-> aliexpress.shop.categoies`
- Собирает список товаров со страницы категории (`get_list_products_in_category()`).
- Итерируясь по списку передает управление в `grab_product_page()` отсылая функции текущий url страницы.
`grab_product_page()` обрабатывает поля товара и передает управление классу `Product`.

## Функции

### `get_list_products_in_category`

**Описание**: Функция возвращает список URL-адресов товаров со страницы категории.

**Параметры**:

- `s` (Supplier): объект Supplier, содержащий информацию о поставщике.

**Возвращает**:

- `list[str, str, None]`: список URL-адресов товаров или `None`, если товаров не найдено.

**Пример**:

```python
>>> from src.suppliers.suppliers_list.kualastyle.scenario import get_list_products_in_category
>>> from src.suppliers.suppliers_list.kualastyle.supplier import Supplier
>>> supplier = Supplier(...)
>>> products_urls = get_list_products_in_category(supplier)
>>> if products_urls:
...     print(f"Found {len(products_urls)} products in category {supplier.current_scenario['name']}")
... else:
...     print(f"No products found in category {supplier.current_scenario['name']}")
```

### `paginator`

**Описание**: Функция реализует пролистывание страниц категории.

**Параметры**:

- `d` (Driver): объект Driver, представляющий вебдрайвер.
- `locator` (dict): словарь с локаторами для элементов на странице.
- `list_products_in_category` (list): список URL-адресов товаров.

**Возвращает**:

- `bool`: `True`, если удалось пролистнуть страницу, `False` в противном случае.

**Пример**:

```python
>>> from src.suppliers.suppliers_list.kualastyle.scenario import paginator
>>> from src.webdriver.driver import Driver
>>> driver = Driver(...)
>>> locator = {'pagination': {'<-' : ...}}
>>> products_urls = [...]
>>> paginator(driver, locator, products_urls)
```

### `get_list_categories_from_site`

**Описание**: Функция собирает список актуальных категорий с сайта поставщика.

**Параметры**:

- `s` (Supplier): объект Supplier, содержащий информацию о поставщике.

**Возвращает**:

- `list`: список категорий с сайта.


## Принцип работы

**`get_list_products_in_category`**

1. Получает вебдрайвер `d` и локаторы `l` для страницы категории из объекта Supplier `s`.
2. Ждет 1 секунду (`d.wait(1)`).
3. Закрывает всплывающее окно (`d.execute_locator (s.locators [\'product\'][\'close_banner\'] )`).
4. Прокручивает страницу (`d.scroll()`).
5. Получает список URL-адресов товаров с помощью локатора `l[\'product_links\']`.
6. Если товаров не найдено, выводит предупреждение в лог (`logger.warning`).
7. Пока текущий URL-адрес `d.current_url` не равен предыдущему URL-адресу `d.previous_url`:
    - Вызывает функцию `paginator` для пролистывания страницы.
    - Если удалось пролистнуть, добавляет найденные URL-адресы товаров в список `list_products_in_category`.
    - Если пролистывание невозможно, прерывает цикл.
8. Преобразует `list_products_in_category` в список, если он был строкой.
9. Выводит в лог количество найденных товаров (`logger.debug`).
10. Возвращает список URL-адресов товаров.

**`paginator`**

1. Получает локатор для кнопки "предыдущая страница" из словаря локаторов.
2. Получает элемент по локатору.
3. Если элемент не найден или список элементов пустой, возвращает `None`.
4. Если элемент найден, пролистывает страницу и возвращает `True`.

**`get_list_categories_from_site`**

1. Получает вебдрайвер `d` и локаторы `l` для страницы категории из объекта Supplier `s`.
2. Получает список категорий с помощью локатора `l['category_links']`.
3. Возвращает список категорий.

## Примеры

```python
# Пример использования get_list_products_in_category
from src.suppliers.suppliers_list.kualastyle.scenario import get_list_products_in_category
from src.suppliers.suppliers_list.kualastyle.supplier import Supplier
supplier = Supplier(...)
products_urls = get_list_products_in_category(supplier)
if products_urls:
    print(f"Found {len(products_urls)} products in category {supplier.current_scenario['name']}")
else:
    print(f"No products found in category {supplier.current_scenario['name']}")

# Пример использования paginator
from src.suppliers.suppliers_list.kualastyle.scenario import paginator
from src.webdriver.driver import Driver
driver = Driver(...)
locator = {'pagination': {'<-' : ...}}
products_urls = [...]
paginator(driver, locator, products_urls)

# Пример использования get_list_categories_from_site
from src.suppliers.suppliers_list.kualastyle.scenario import get_list_categories_from_site
from src.suppliers.suppliers_list.kualastyle.supplier import Supplier
supplier = Supplier(...)
categories = get_list_categories_from_site(supplier)
print(f"Found {len(categories)} categories on the site")
```

## Дополнительные сведения

- В функциях `get_list_products_in_category` и `paginator` используются локаторы для элементов на странице. Локаторы определены в объекте `Supplier`.
- Для логгирования используется модуль `logger` из `src.logger.logger`.
- В коде используется вебдрайвер `Driver`, который наследует от `Chrome`, `Firefox`, `Playwright`.
- Основная команда, используемая в коде: `driver.execute_locator(l:dict)`.

## Изменения

- Добавлены комментарии с объяснением принципа работы функций.
- Добавлено описание параметров и возвращаемых значений функций.
- Добавлены примеры использования функций.
- Добавлены комментарии с описанием используемых локаторов.
- Добавлены комментарии с описанием используемого вебдрайвера.
- Добавлены комментарии с описанием используемого модуля логгирования.
- Исправлены грамматические ошибки в документации.
- Изменен формат документации в соответствии с требованиями.
- Обновлено описание функции `get_list_categories_from_site`.