# Модуль сбора товаров со страницы категорий поставщика hb.co.il через вебдрайвер

## Обзор

Модуль предназначен для сбора информации о товарах с сайта поставщика hb.co.il. Он включает в себя функции для получения списка категорий товаров и списка товаров в каждой категории, используя веб-драйвер. Собранные данные затем используются для дальнейшей обработки и сохранения.

## Подробней

Этот модуль является частью системы для автоматизированного сбора данных о товарах с сайтов поставщиков. Он разработан с учетом особенностей структуры сайта hb.co.il и использует веб-драйвер для навигации по сайту и извлечения необходимой информации.

Модуль выполняет следующие основные задачи:

1.  **Сбор списка категорий**: Функция `get_list_categories_from_site()` собирает список категорий товаров с сайта поставщика.
2.  **Сбор списка товаров в категории**: Функция `get_list_products_in_category()` собирает список URL товаров, представленных на странице категории.
3.  **Обработка пагинации**: Если в категории есть несколько страниц с товарами, функция `paginator()` осуществляет переход по страницам и собирает ссылки на все товары в категории.
4.  **Извлечение информации о товаре**: Функция `grab_product_page()` (не представлена в данном коде) отвечает за извлечение конкретных данных о каждом товаре (наименование, описание, цена и т.д.).

## Функции

### `get_list_products_in_category`

```python
async def get_list_products_in_category (d: Driver, l:'SimpleNamespace') -> list[str, str, None]:
    """
    Извлекает список URL товаров со страницы категории.

    Args:
        d (Driver): Инстанс веб-драйвера для взаимодействия с сайтом.
        l (SimpleNamespace): Объект, содержащий локаторы элементов на странице.

    Returns:
        list[str, str, None]: Список URL товаров или None, если список не найден.

    
    - Ожидает загрузки страницы.
    - Выполняет прокрутку страницы для загрузки динамического контента.
    - Извлекает список URL товаров, используя локатор `l.product_links`.
    - Если список не найден, регистрирует предупреждение.
    - Если URL текущей страницы не отличается от предыдущего, осуществляет пагинацию с помощью функции `paginator`.
    - Возвращает список URL товаров.

    Примеры:
    ```
    # Пример вызова функции (требуется инициализация веб-драйвера и объекта с локаторами)
    # list_products = await get_list_products_in_category(driver, locators)
    # if list_products:
    #     print(f"Найдено {len(list_products)} товаров в категории")
    # else:
    #     print("Товары в категории не найдены")
    ```
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
    """ Листалка
    Осуществляет переход на следующую страницу категории, если это возможно.

    Args:
        d (Driver): Инстанс веб-драйвера для взаимодействия с сайтом.
        locator (dict): Объект, содержащий локаторы элементов на странице, включая кнопку пагинации.
        list_products_in_category (list): Текущий список URL товаров в категории.

    Returns:
        bool: True, если переход на следующую страницу выполнен успешно, иначе - None.

    
    - Пытается выполнить нажатие на кнопку пагинации, используя локатор `locator.pagination['<-']`.
    - Если кнопка не найдена или не активна, возвращает None.
    - В случае успешного нажатия возвращает True.
    ```
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
    """ сборщик актуальных категорий с сайта
    Собирает актуальный список категорий с сайта поставщика.

    Args:
        s: Объект поставщика (описание структуры объекта отсутствует в предоставленном коде).

    Returns:
        None: Данные возвращаются через объект поставщика (не указано явно в коде).
    """
    ...
```