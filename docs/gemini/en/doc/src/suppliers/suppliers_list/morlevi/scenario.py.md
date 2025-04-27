# Модуль сбора товаров со страницы категорий поставщика kualastyle.il через вебдрайвер

## Обзор

Модуль собирает товары со страниц категорий поставщика kualastyle.il, используя вебдрайвер. Он предоставляет набор функций для:

- Получения списка категорий со страниц продавца. `get_list_categories_from_site()`
- Собирает список товаров со страницы категории `get_list_products_in_category()`
- Итерируясь по списку, передает управление в `grab_product_page()`, отправляя функции текущий URL страницы. `grab_product_page()` обрабатывает поля товара и передает управление классу `Product`.

## Детали

Этот модуль реализует логику сбора товаров с сайта поставщика. 

- `get_list_categories_from_site()`: извлекает список категорий с сайта.
- `get_list_products_in_category()`: извлекает список URL-адресов товаров с выбранной страницы категории.
- `paginator()`: реализует логику перехода к следующей странице товаров в категории.
- `grab_product_page()`: обрабатывает данные о товаре на странице товара.

## Таблица Содержания

- [Функции](#функции)
    - [`get_list_products_in_category`](#get_list_products_in_category)
    - [`paginator`](#paginator)
    - [`get_list_categories_from_site`](#get_list_categories_from_site)

## Функции

### `get_list_products_in_category`

```python
def get_list_products_in_category (s: Supplier) -> list[str, str, None]:    
    """ Возвращает список URL-адресов товаров со страницы категории.
    Если надо пролистать страницы категорий - листаю ??????
    
    Attrs:
        s - Supplier
    @returns
        list or one of products urls or None
    """
    ...
    d:Driver = s.driver
    l: dict = s.locators['category']
    ...
    d.wait(1)
    d.execute_locator (s.locators ['product']['close_banner'] )
    d.scroll()
    ...
    
    list_products_in_category: List = d.execute_locator(l['product_links'])
    
    if not list_products_in_category:
        logger.warning('Нет ссылок на товары. Так бывает')
        ...
        return
    ...
    while d.current_url != d.previous_url:
        if paginator(d,l,list_products_in_category):
            list_products_in_category.append(d.execute_locator(l['product_links']))
        else:
            break
        
    list_products_in_category = [list_products_in_category] if isinstance(list_products_in_category, str) else list_products_in_category
    
    logger.debug(f""" Found {len(list_products_in_category)} items in category {s.current_scenario['name']} """)
    
    return list_products_in_category
```

**Назначение**: Функция извлекает список URL-адресов товаров со страницы категории. 

**Параметры**:
- `s` (Supplier): Объект поставщика, содержащий информацию о текущей категории и настройках вебдрайвера.

**Возвращает**:
- `list[str, str, None]`: Список URL-адресов товаров, найденных на странице категории. Если товаров нет, возвращает `None`.

**Как работает**:
- Получает объект `Driver` из объекта `Supplier`.
- Выполняет поиск ссылок на товары на странице категории.
- Проверяет, есть ли ссылки на товары, если нет, выводит сообщение в лог.
- Проверяет, есть ли кнопка "Далее" на странице, если да, то переходит на следующую страницу и повторяет процесс поиска товаров.
- Возвращает список URL-адресов найденных товаров.

### `paginator`

```python
def paginator(d:Driver, locator: dict, list_products_in_category: list):
    """ Листалка """
    response = d.execute_locator(locator['pagination']['<-\'] )
    if not response or (isinstance(response, list) and len(response) == 0): 
        ...
        return
    return True
```

**Назначение**: Функция реализует логику перехода к следующей странице товаров в категории. 

**Параметры**:
- `d` (Driver): Объект вебдрайвера.
- `locator` (dict): Словарь локаторов, используемых для поиска элементов на странице.
- `list_products_in_category` (list): Список URL-адресов товаров, найденных на текущей странице.

**Возвращает**:
- `True` если перешли на следующую страницу, `None` если не смогли перейти на следующую страницу. 

**Как работает**:
- Поиск элемента с локатором `locator['pagination']['<-\']`
- Проверяет, найден ли элемент, если нет, то возвращает `None`
- Если элемент найден, то переходит на следующую страницу
- Возвращает `True`

### `get_list_categories_from_site`

```python
def get_list_categories_from_site(s):
    """ сборщик актуальных категорий с сайта """
    ...
```

**Назначение**: Функция собирает список категорий с сайта.

**Параметры**:
- `s` (Supplier): Объект поставщика, содержащий информацию о текущей категории и настройках вебдрайвера.

**Возвращает**:
- ...

**Как работает**:
- ...

**Примеры**:
- ...