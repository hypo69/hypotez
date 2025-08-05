# Модуль сбора товаров со страницы категорий поставщика kualastyle.il через вебдрайвер

## Обзор

Модуль собирает товары со страницы категорий поставщика `kualastyle.il` через вебдрайвер.

## Подробнее

Модуль выполняет следующие задачи:

- Собирает список категорий со страниц продавца.
- Собирает список товаров со страницы категории.
- Передает управление в `grab_product_page()` для обработки полей товара.
- Итерируется по списку товаров, вызывая `grab_product_page()`.

## Классы

### `Supplier`

**Описание**: Класс `Supplier` содержит информацию о поставщике, необходимую для сбора данных.

**Атрибуты**:

- `driver` (Driver): Вебдрайвер для взаимодействия с сайтом.
- `locators` (dict): Словарь локаторов для элементов на странице.
- `current_scenario` (dict): Информация о текущем сценарии сбора.
- `site_settings` (dict): Настройки сайта.

**Принцип работы**:

Класс `Supplier` предоставляет информацию о поставщике, необходимую для работы модуля.

## Функции

### `get_list_products_in_category`

**Назначение**: Функция извлекает список URL-адресов товаров со страницы категории.

**Параметры**:

- `s` (Supplier): Объект класса `Supplier`, содержащий информацию о поставщике.

**Возвращает**:

- `list[str, str, None]`: Список URL-адресов товаров или `None` в случае ошибки.

**Как работает функция**:

1. Инициализирует вебдрайвер.
2. Извлекает список локаторов из `s.locators`.
3. Проверяет наличие баннера и, если он есть, закрывает его.
4. Прокручивает страницу до конца.
5. Получает список URL-адресов товаров.
6. Проверяет наличие пагинации и, если она есть, листает страницы категории, собирая дополнительные URL-адреса товаров.
7. Возвращает список URL-адресов товаров.

**Примеры**:

```python
from src.suppliers.suppliers_list.kualastyle.scenario import get_list_products_in_category
from src.suppliers.suppliers_list.kualastyle.supplier import Supplier

# Создание инстанса класса Supplier
s = Supplier()

# Получение списка URL-адресов товаров
list_products_in_category = get_list_products_in_category(s)

# Вывод списка URL-адресов товаров
print(list_products_in_category)
```

### `paginator`

**Назначение**: Функция реализует пагинацию на странице категории.

**Параметры**:

- `d` (Driver): Вебдрайвер для взаимодействия с сайтом.
- `locator` (dict): Словарь локаторов для элементов на странице.
- `list_products_in_category` (list): Список URL-адресов товаров.

**Возвращает**:

- `bool`: `True`, если страница пролистана, иначе `False`.

**Как работает функция**:

1. Проверяет наличие кнопки пагинации.
2. Если кнопка пагинации есть, кликает по ней.
3. Обновляет список URL-адресов товаров.
4. Возвращает `True`, если страница пролистана, иначе `False`.

**Примеры**:

```python
from src.suppliers.suppliers_list.kualastyle.scenario import paginator
from src.webdriver.driver import Driver

# Создание инстанса класса Driver
d = Driver(Chrome)

# Локатор кнопки пагинации
locator = {'pagination': {'<-' : {'attribute': null, 'by': 'XPATH', 'selector': "//button[@id = 'closeXButton']", 'if_list': 'first', 'use_mouse': false, 'mandatory': false, 'timeout': 0, 'timeout_for_event': 'presence_of_element_located', 'event': 'click()', 'locator_description': 'Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)'}}}

# Список URL-адресов товаров
list_products_in_category = []

# Вызов функции paginator
paginator(d, locator, list_products_in_category)
```

### `get_list_categories_from_site`

**Назначение**: Функция собирает актуальные категории с сайта.

**Параметры**:

- `s` (Supplier): Объект класса `Supplier`, содержащий информацию о поставщике.

**Возвращает**:

- `None`: Функция не возвращает значение.

**Как работает функция**:

1. Получает список локаторов из `s.locators`.
2. Собирает список URL-адресов категорий.
3. Возвращает список URL-адресов категорий.

**Примеры**:

```python
from src.suppliers.suppliers_list.kualastyle.scenario import get_list_categories_from_site
from src.suppliers.suppliers_list.kualastyle.supplier import Supplier

# Создание инстанса класса Supplier
s = Supplier()

# Вызов функции get_list_categories_from_site
get_list_categories_from_site(s)
```

## Параметры класса `Supplier`

- `driver` (Driver): Вебдрайвер для взаимодействия с сайтом.
- `locators` (dict): Словарь локаторов для элементов на странице.
- `current_scenario` (dict): Информация о текущем сценарии сбора.
- `site_settings` (dict): Настройки сайта.

**Примеры**:

```python
from src.suppliers.suppliers_list.kualastyle.supplier import Supplier
from src.webdriver.driver import Driver, Chrome

# Создание инстанса класса Driver
driver = Driver(Chrome)

# Создание инстанса класса Supplier
s = Supplier(driver=driver, locators={'category': {'product_links': {'attribute': null, 'by': 'XPATH', 'selector': "//button[@id = 'closeXButton']", 'if_list': 'first', 'use_mouse': false, 'mandatory': false, 'timeout': 0, 'timeout_for_event': 'presence_of_element_located', 'event': 'click()', 'locator_description': 'Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)'}}, 'product': {'close_banner': {'attribute': null, 'by': 'XPATH', 'selector': "//button[@id = 'closeXButton']", 'if_list': 'first', 'use_mouse': false, 'mandatory': false, 'timeout': 0, 'timeout_for_event': 'presence_of_element_located', 'event': 'click()', 'locator_description': 'Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)'}}}, current_scenario={'name': 'kualastyle.il'}, site_settings={'url': 'https://kualastyle.il'})

# Вывод информации о Supplier
print(s)