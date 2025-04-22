# Модуль сбора категорий и товаров со страниц поставщика hb.co.il

## Обзор

Модуль предназначен для сбора информации о товарах и категориях с сайта поставщика hb.co.il. Он использует веб-драйвер для взаимодействия со страницами сайта, извлечения данных и формирования списков товаров и категорий.

## Подробнее

Этот модуль играет важную роль в процессе автоматизированного сбора данных о товарах с сайта поставщика. Он обеспечивает следующие функции:

- Сбор списка категорий со страниц продавца (`get_list_categories_from_site()`).
- Сбор списка товаров со страницы категории (`get_list_products_in_category()`).
- Передача управления в функцию `grab_product_page()` для обработки полей товара и передачи данных классу `Product`.

## Функции

### `get_list_products_in_category`

```python
def get_list_products_in_category (s: Supplier) -> list[str, str, None]:
    """ Функция возвращает список URL товаров со страницы категории.

    Args:
        s (Supplier): Объект поставщика.

    Returns:
        list[str, str, None]: Список URL товаров или None.
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

**Назначение**: Функция извлекает список URL товаров со страницы категории. Если необходимо, пролистывает страницы категорий.

**Параметры**:
- `s` (Supplier): Объект поставщика, содержащий информацию о текущем поставщике, включая веб-драйвер и локаторы элементов.

**Возвращает**:
- `list[str, str, None]`: Список URL товаров, найденных на странице категории. Возвращает `None`, если список товаров не найден.

**Как работает функция**:

1. **Инициализация**:
   - Извлекает драйвер и локаторы из объекта поставщика `s`.

2. **Ожидание и закрытие баннера**:
   - Ожидает 1 секунду.
   - Выполняет локатор для закрытия баннера, если он есть.
   - Прокручивает страницу вниз.

3. **Извлечение ссылок на товары**:
   - Выполняет локатор для получения списка ссылок на товары.

4. **Обработка отсутствия ссылок**:
   - Если список ссылок пуст, записывает предупреждение в лог и возвращает `None`.

5. **Пагинация**:
   - Если текущий URL отличается от предыдущего, вызывает функцию `paginator` для перелистывания страниц.
   - Добавляет новые ссылки на товары в общий список.

6. **Преобразование списка**:
   - Преобразует список товаров, если он является строкой.

7. **Логирование и возврат**:
   - Записывает отладочное сообщение в лог с количеством найденных товаров.
   - Возвращает список URL товаров.

**Внутренние функции**:
   - `paginator`: Функция, обеспечивающая перелистывание страниц.

**Примеры**:
```python
# Пример вызова функции
supplier = Supplier(...)
product_links = get_list_products_in_category(supplier)
if product_links:
    print(f"Found {len(product_links)} product links")
else:
    print("No product links found")
```

### `paginator`

```python
def paginator(d:Driver, locator: dict, list_products_in_category: list):
    """ Функция перелистывания страниц. """
    response = d.execute_locator(locator['pagination']['<-'])
    if not response or (isinstance(response, list) and len(response) == 0): 
        ...
        return
    return True
```

**Назначение**: Функция осуществляет перелистывание страниц на сайте.

**Параметры**:
- `d` (Driver): Объект веб-драйвера.
- `locator` (dict): Словарь с локаторами элементов для пагинации.
- `list_products_in_category` (list): Список текущих товаров в категории.

**Возвращает**:
- `True`: Если перелистывание выполнено успешно.
- `None`: Если перелистывание не удалось.

**Как работает функция**:

1. **Выполнение локатора для кнопки пагинации**:
   - Пытается выполнить локатор для кнопки "назад" или "влево" (`<-`) на странице.

2. **Проверка ответа**:
   - Если ответ отсутствует или является пустым списком, функция считает, что перелистывание не удалось, и возвращает `None`.

3. **Возврат значения True**:
   - Если локатор выполнен успешно, функция возвращает `True`, указывая на успешное перелистывание.

**Примеры**:
```python
# Пример вызова функции
driver = Driver(...)
category_locator = {...}
products = [...]
success = paginator(driver, category_locator, products)
if success:
    print("Page flipped successfully")
else:
    print("Page flipping failed")
```

### `get_list_categories_from_site`

```python
def get_list_categories_from_site(s):
    """ Функция сбора актуальных категорий с сайта. """
    ...
```

**Назначение**: Функция собирает актуальные категории с сайта.

**Параметры**:
- `s` (Supplier): Объект поставщика.

**Возвращает**:
- `list`: Список категорий, найденных на сайте.

**Как работает функция**:
   -  <Описание логики функции будет добавлено после реализации>

**Примеры**:
```python
# Пример вызова функции
supplier = Supplier(...)
categories = get_list_categories_from_site(supplier)
if categories:
    print(f"Found {len(categories)} categories")
else:
    print("No categories found")