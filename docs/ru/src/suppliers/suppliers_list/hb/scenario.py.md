# Модуль сбора товаров со страницы категорий поставщика hb.co.il через вебдрайвер

## Обзор

Модуль предназначен для сбора информации о товарах с сайта поставщика hb.co.il. Он включает в себя функции для получения списка категорий товаров, списка товаров в каждой категории и последующей обработки информации о товарах. Модуль использует веб-драйвер для взаимодействия с сайтом и сбора данных.

## Подробнее

Модуль предоставляет следующий функционал:

- Сбор списка категорий товаров с сайта поставщика.
- Сбор списка товаров в каждой категории.
- Итерация по списку товаров и передача управления в функцию `grab_product_page()` для обработки информации о каждом товаре.
- Обработка полей товара и передача управления классу `Product`.

## Функции

### `get_list_products_in_category`

```python
async def get_list_products_in_category (d: Driver, l:'SimpleNamespace') -> list[str, str, None]:
    """ Функция возвращает список URL товаров со страницы категории.

    Args:
        d (Driver): Инстанс веб-драйвера.
        l (SimpleNamespace): Объект, содержащий локаторы элементов страницы.

    Returns:
        list[str, str, None]: Список URL товаров или None, если список товаров не найден.

    Как работает функция:
    - Функция ожидает загрузки страницы в течение 1 секунды.
    - Прокручивает страницу вниз.
    - Извлекает ссылки на товары с использованием локатора `l.product_links`.
    - Если ссылки на товары не найдены, логирует предупреждение и возвращает None.
    - Организует пагинацию по страницам категории, если это необходимо.
    - Возвращает список URL товаров.
    """
    ...
    d.wait(1)
    d.scroll()
    ...

    list_products_in_category: List = await d.execute_locator(l.product_links)

    if not list_products_in_category:
        logger.warning('Нет ссылок на товары. Так бывает')
        ...
        return
    ...
    while d.current_url != d.previous_url:
        if await paginator(d,l,list_products_in_category):
            list_products_in_category.append(await d.execute_locator(l.product_links))
        else:
            break
        
    list_products_in_category:list = [list_products_in_category] if isinstance(list_products_in_category, str) else list_products_in_category

    logger.debug(f""" Found {len(list_products_in_category)} items in  """)
    
    return list_products_in_category
```

### `paginator`

```python
async def paginator(d:Driver, locator: dict, list_products_in_category: list):
    """ Функция осуществляет пагинацию по страницам категории.

    Args:
        d (Driver): Инстанс веб-драйвера.
        locator (dict): Объект, содержащий локаторы элементов страницы.
        list_products_in_category (list): Список URL товаров в текущей категории.

    Returns:
        bool: True, если пагинация прошла успешно, иначе None.

    Как работает функция:
    - Функция пытается выполнить клик по локатору следующей страницы `locator.pagination.__dict__['<-']`.
    - Если клик не удался или список результатов пуст, функция завершает работу и возвращает None.
    - В случае успешного клика возвращает True.
    """
    response = await d.execute_locator(locator.pagination.__dict__['<-'])
    if not response or (isinstance(response, list) and len(response) == 0): 
        ...
        return
    return True
```

### `build_list_categories_from_site`

```python
def build_list_categories_from_site(s):
    """ Функция сборки актуальных категорий с сайта.

    Args:
        s: Объект, содержащий информацию о поставщике.

    Как работает функция:
        -   Извлекает категории с сайта поставщика.

    """
    ...