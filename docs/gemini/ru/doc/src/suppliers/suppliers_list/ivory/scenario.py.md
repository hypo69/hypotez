# Модуль сбора товаров со страницы категорий поставщика hb.co.il

## Обзор

Модуль `category.py` предназначен для сбора товаров со страниц категорий поставщика `hb.co.il` с использованием вебдрайвера. Он включает в себя функции для извлечения списка категорий, сбора товаров из каждой категории и обработки данных о товарах.

## Подробнее

Данный модуль использует объект `Driver` из модуля `src.webdriver` для взаимодействия с веб-сайтом `hb.co.il`. 
Он использует локаторы (XPath-выражения) для поиска элементов на странице, чтобы извлечь список категорий и товары. 
При сборке товаров из каждой категории,  функция `get_list_products_in_category()` использует `driver.execute_locator()` для поиска ссылок на товары. 
Если на странице категории присутствует пагинация, то используется функция `paginator()` для перехода к следующей странице и продолжения сбора товаров.

## Функции

### `get_list_products_in_category(s: Supplier) -> list[str, str, None]`

**Назначение**: Извлечение списка ссылок на товары со страницы категории.

**Параметры**:

- `s` (`Supplier`): Объект `Supplier`, содержащий информацию о поставщике, включая драйвер, локаторы и текущий сценарий.

**Возвращает**:

- `list[str, str, None]`: Список ссылок на товары, либо `None`, если не удалось получить ссылки. 

**Как работает функция**:

- Получает объект `Driver` и локаторы из объекта `Supplier`.
- Выполняет локатор `'product'` (`'close_banner'`) для закрытия баннера на странице.
- Прокручивает страницу вниз с помощью `d.scroll()`.
- Использует `d.execute_locator()` для поиска ссылок на товары с помощью локатора `'product_links'`.
- Если ссылок на товары не найдено, выводит предупреждение в логгер и возвращает `None`.
- Если на странице присутствует пагинация, то запускается функция `paginator()` для перехода к следующей странице и добавления новых ссылок в список.
- Преобразует список ссылок в список `list` и выводит информацию в логгер о количестве найденных товаров.
- Возвращает список ссылок на товары.

### `paginator(d: Driver, locator: dict, list_products_in_category: list) -> bool`

**Назначение**: Переход к следующей странице пагинации.

**Параметры**:

- `d` (`Driver`): Объект `Driver` для работы с браузером.
- `locator` (`dict`): Словарь с локаторами для поиска элементов на странице пагинации.
- `list_products_in_category` (`list`): Список ссылок на товары.

**Возвращает**:

- `bool`: `True`, если перешёл к следующей странице, `False` - если нет.

**Как работает функция**:

- Использует `d.execute_locator()` для поиска элемента "Следующая страница" с помощью локатора `'pagination'`.
- Если элемент не найден или список пуст, выводит информацию в логгер и возвращает `None`.
- Если элемент найден, то переходит к следующей странице и возвращает `True`.

### `get_list_categories_from_site(s)`

**Назначение**: Извлечение списка категорий с сайта.

**Параметры**:

- `s` (`Supplier`): Объект `Supplier`, содержащий информацию о поставщике.

**Возвращает**:

- `list`: Список категорий с сайта.

**Как работает функция**:

- **Недостаточно информации**: Документация не содержит информации о том, как именно работает эта функция. 

## Примеры

**Пример вызова функции `get_list_products_in_category()`**:

```python
from src.suppliers.hb.category import get_list_products_in_category
from src.suppliers.suppliers_list.ivory.supplier import Supplier

# Создание объекта Supplier
s = Supplier()

# Получение списка товаров из категории
products = get_list_products_in_category(s)

# Вывод списка товаров
print(products)
```

**Пример вызова функции `paginator()`**:

```python
from src.suppliers.hb.category import paginator
from src.webdriver.driver import Driver

# Создание объекта Driver
driver = Driver()

# Локаторы для пагинации
locator = {'pagination': {'<-' : {'attribute': null, 'by': 'XPATH', 'selector': "//button[@id = 'closeXButton']", 'if_list': 'first', 'use_mouse': False, 'mandatory': False, 'timeout': 0, 'timeout_for_event': 'presence_of_element_located', 'event': 'click()', 'locator_description': 'Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)'}}}

# Список товаров 
list_products_in_category = []

# Переход к следующей странице
success = paginator(driver, locator, list_products_in_category)

# Вывод результата
print(f'Успешно перешёл к следующей странице: {success}')
```

**Пример вызова функции `get_list_categories_from_site()`**:

```python
from src.suppliers.hb.category import get_list_categories_from_site
from src.suppliers.suppliers_list.ivory.supplier import Supplier

# Создание объекта Supplier
s = Supplier()

# Получение списка категорий
categories = get_list_categories_from_site(s)

# Вывод списка категорий
print(categories)
```

**Пример определения объекта `Supplier`**:

```python
from src.suppliers.suppliers_list.ivory.supplier import Supplier

# Создание объекта Supplier
s = Supplier()

# Настройка драйвера
s.driver = Driver(Chrome)

# Настройка локаторов
s.locators = {
    'category': {
        'product_links': {
            'attribute': 'href',
            'by': 'XPATH',
            'selector': "//a[@class='product-item__link']",
            'if_list': 'all',
            'use_mouse': False,
            'mandatory': False,
            'timeout': 0,
            'timeout_for_event': 'presence_of_element_located',
            'event': None,
            'locator_description': 'Нахожу все ссылки на товары на странице',
        },
        'pagination': {
            '<-': {
                'attribute': null,
                'by': 'XPATH',
                'selector': "//button[@id = 'closeXButton']",
                'if_list': 'first',
                'use_mouse': False,
                'mandatory': False,
                'timeout': 0,
                'timeout_for_event': 'presence_of_element_located',
                'event': 'click()',
                'locator_description': 'Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)',
            },
        },
    },
}

# Настройка текущего сценария
s.current_scenario = {
    'name': 'Category_Name'
}