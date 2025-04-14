# Модуль `category.py`

## Обзор

Модуль `category.py` предназначен для сбора информации о категориях и товарах с сайта поставщика hb.co.il. Он использует веб-драйвер для навигации по сайту и извлечения необходимых данных. Модуль включает функции для получения списка категорий, списка товаров в каждой категории и итерации по страницам товаров.

## Подробней

Этот модуль играет ключевую роль в процессе сбора данных с сайта поставщика. Он отвечает за получение актуального списка категорий товаров, а также за сбор ссылок на отдельные товары внутри каждой категории. Полученные данные используются для дальнейшей обработки и сохранения информации о товарах.

## Функции

### `get_list_products_in_category`

```python
def get_list_products_in_category(s: Supplier) -> list[str, str, None]:
    """
    Возвращает список URL товаров со страницы категории.

    Args:
        s (Supplier): Объект поставщика.

    Returns:
        list[str, str, None]: Список URL товаров или None.
    """
    ...
    d: Driver = s.driver
    l: dict = s.locators['category']
    ...
    d.wait(1)
    d.execute_locator(s.locators['product']['close_banner'])
    d.scroll()
    ...

    list_products_in_category: List = d.execute_locator(l['product_links'])

    if not list_products_in_category:
        logger.warning('Нет ссылок на товары. Так бывает')
        ...
        return
    ...
    while d.current_url != d.previous_url:
        if paginator(d, l, list_products_in_category):
            list_products_in_category.append(d.execute_locator(l['product_links']))
        else:
            break

    list_products_in_category = [list_products_in_category] if isinstance(list_products_in_category, str) else list_products_in_category

    logger.debug(f""" Found {len(list_products_in_category)} items in category {s.current_scenario['name']} """)

    return list_products_in_category
```

**Назначение**: Функция `get_list_products_in_category` извлекает список URL-адресов товаров из текущей категории на сайте поставщика. Она использует объект `Supplier` для доступа к драйверу веб-браузера и локаторам элементов на странице.

**Параметры**:
- `s` (Supplier): Объект поставщика, содержащий информацию о текущем поставщике, включая драйвер веб-браузера и локаторы элементов на странице.

**Возвращает**:
- `list[str, str, None]`: Список URL-адресов товаров в текущей категории. Если товары не найдены, возвращает `None`.

**Как работает функция**:
1.  Извлекает драйвер веб-браузера и локаторы элементов категории из объекта поставщика `s`.
2.  Ожидает 1 секунду, чтобы элементы страницы успели загрузиться.
3.  Выполняет локатор для закрытия баннера (если он есть) с помощью `d.execute_locator`.
4.  Прокручивает страницу вниз, чтобы подгрузить все элементы, с помощью `d.scroll()`.
5.  Извлекает список URL-адресов товаров с использованием локатора `l['product_links']` и сохраняет его в `list_products_in_category`.
6.  Если список URL-адресов товаров пуст, регистрирует предупреждение в лог и возвращает `None`.
7.  Организует пагинацию по страницам категории.
8.  В цикле проверяет, изменился ли текущий URL страницы. Если URL не изменился, завершает цикл.
9.  Если URL изменился, вызывает функцию `paginator` для перехода на следующую страницу.
10. Если `paginator` возвращает `True`, добавляет URL-адреса товаров со следующей страницы в `list_products_in_category`.
11. Преобразует `list_products_in_category` в список, если он является строкой.
12. Регистрирует отладочное сообщение в лог с количеством найденных товаров и названием текущей категории.
13. Возвращает список URL-адресов товаров.

**Внутренние функции**:
- `paginator(d:Driver, locator: dict, list_products_in_category: list)`: Выполняет пагинацию по страницам категории.

**Примеры**:

```python
from src.suppliers import Supplier
from src.webdriver.driver import Driver, Chrome

# Создаем фиктивный объект поставщика
class MockSupplier(Supplier):
    def __init__(self):
        self.driver = Driver(Chrome)  # Инициализация драйвера Chrome
        self.locators = {
            'category': {
                'product_links': {
                    'by': 'CSS_SELECTOR',
                    'selector': '.product-item a',
                    'attribute': 'href'
                },
                'pagination': {
                    '<-': {
                        'by': 'CSS_SELECTOR',
                        'selector': '.pagination-next',
                        'attribute': 'href'
                    }
                }
            },
            'product': {
                'close_banner': {
                    'by': 'XPATH',
                    'selector': "//button[@id = 'closeXButton']",
                    'if_list': 'first',
                    'use_mouse': False,
                    'mandatory': False,
                    'timeout': 0,
                    'timeout_for_event': 'presence_of_element_located',
                    'event': 'click()',
                    'locator_description': "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
                }
            }
        }
        self.current_scenario = {'name': 'Test Category'}
        self.driver.current_url = 'https://example.com/category/page1'  # Установите начальный URL
        self.driver.previous_url = None

# Создаем экземпляр фиктивного поставщика
s = MockSupplier()

# Получаем список товаров (предполагается, что драйвер настроен и возвращает данные)
product_list = get_list_products_in_category(s)

if product_list:
    print(f"Found {len(product_list)} products in category")
else:
    print("No products found in category")

```

### `paginator`

```python
def paginator(d: Driver, locator: dict, list_products_in_category: list):
    """ Листалка """
    response = d.execute_locator(locator['pagination']['<-'])
    if not response or (isinstance(response, list) and len(response) == 0):
        ...
        return
    return True
```

**Назначение**: Функция `paginator` осуществляет переход на следующую страницу категории, используя локатор кнопки пагинации.

**Параметры**:
- `d` (Driver): Объект драйвера веб-браузера.
- `locator` (dict): Словарь с локаторами элементов страницы.
- `list_products_in_category` (list): Список URL-адресов товаров в текущей категории.

**Возвращает**:
- `True`: Если переход на следующую страницу выполнен успешно.
- `None`: Если переход на следующую страницу невозможен.

**Как работает функция**:
1.  Извлекает локатор кнопки пагинации из словаря `locator['pagination']['<-']`.
2.  Выполняет локатор для кнопки пагинации с помощью `d.execute_locator`.
3.  Если результат выполнения локатора равен `None` или является пустым списком, возвращает `None`.
4.  В противном случае возвращает `True`, что означает успешный переход на следующую страницу.

**Примеры**:

```python
from src.webdriver.driver import Driver, Chrome

# Создаем фиктивный объект драйвера
driver = Driver(Chrome)

# Создаем фиктивный локатор
locator = {
    'pagination': {
        '<-': {
            'by': 'CSS_SELECTOR',
            'selector': '.pagination-next',
            'attribute': 'href'
        }
    }
}

# Создаем фиктивный список товаров
product_list = ['https://example.com/product1', 'https://example.com/product2']

# Вызываем функцию paginator
result = paginator(driver, locator, product_list)

if result:
    print("Переход на следующую страницу выполнен")
else:
    print("Переход на следующую страницу невозможен")
```

### `get_list_categories_from_site`

```python
def get_list_categories_from_site(s):
    """ сборщик актуальных категорий с сайта """
    ...
```

**Назначение**: Функция `get_list_categories_from_site` отвечает за сбор актуальных категорий с сайта.

**Параметры**:
- `s`: Параметр, который представляет собой объект, содержащий необходимую информацию для сбора категорий с сайта.

**Как работает функция**:
1.  Выполняет действия, необходимые для сбора актуальных категорий с сайта.
2.  Использует драйвер веб-браузера для навигации по сайту.
3.  Извлекает список категорий с использованием заданных локаторов элементов.
4.  Обрабатывает полученные данные и возвращает список категорий.