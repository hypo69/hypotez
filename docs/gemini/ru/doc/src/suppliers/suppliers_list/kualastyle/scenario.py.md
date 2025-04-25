# Модуль сбора товаров со страницы категорий поставщика kualastyle.il через вебдрайвер

## Обзор

Модуль `hypotez/src/suppliers/suppliers_list/kualastyle/scenario.py`  предназначен для сбора информации о товарах с сайта поставщика `kualastyle.il` с помощью `Webdriver` и  `Selenium`. 

## Подробнее

Модуль предоставляет набор функций для:

- Получения списка категорий с сайта `kualastyle.il` (`get_list_categories_from_site()`).
- Извлечения ссылок на товары с  страниц категории (`get_list_products_in_category()`).
-  Перехода на страницу товара, сбора данных и передачи информации  классу `Product` (`grab_product_page()`). 

## Классы

### `Supplier`

**Описание**:  Класс `Supplier`  предоставляет  методы для работы с  данными поставщика,  включая  сбор категорий, товаров и обработку  страниц продуктов.

**Атрибуты**:

- `driver`:  Экземпляр класса `Driver` ( `src.webdriver.driver`), представляющий `Webdriver` для работы с сайтом.
- `locators`:  Словарь, содержащий `locators`  для  идентификации  веб-элементов на сайте  поставщика. 
- `current_scenario`: Словарь,  содержащий  информацию  о  текущем сценарии.

**Методы**:

- `get_list_categories_from_site()`:  Получение  актуальных категорий с сайта поставщика.
- `get_list_products_in_category()`:  Получение  списка  ссылок на товары  с  страницы категории. 
- `grab_product_page()`:  Обработка страницы продукта и  передача данных  в  класс  `Product`.


## Функции

### `get_list_products_in_category`

**Назначение**: Извлечение  списка ссылок на товары с  страницы категории. 

**Параметры**:

- `s` (`Supplier`): Экземпляр класса `Supplier`,  представляющий  поставщика.

**Возвращает**:

- `list` или  `None`: Список  ссылок на товары  с  страницы категории  или  `None`,  если  ссылки  не найдены. 

**Как работает функция**:

1. Извлекает  `Driver` и `locators`  из  объекта  `Supplier`.
2. Ожидает  загрузку  страницы  в  течение  1 секунды.
3. Закрывает  рекламный  баннер  на  странице.
4. Прокручивает  страницу  вниз, чтобы  отобразить  все  товары.
5. Извлекает  ссылки  на  товары  с  помощью  `locator`  `product_links`.
6. Если  ссылки  не  найдены,  выводит  предупреждение  в  лог  и  возвращает  `None`.
7. Если  на  странице  есть  пагинация,  проверяет  наличие  следующей  страницы  и  добавляет  ссылки  с  этой  страницы  в  список,  пока  текущий  URL  не  совпадает  с  предыдущим.
8. Возвращает  список  ссылок  на  товары.

**Примеры**:

```python
# Пример вызова функции с объектом Supplier
supplier = Supplier(driver=Driver(Chrome), locators={'category': {'product_links': {'by': 'XPATH', 'selector': '//a[@class="product-link"]'}}}, current_scenario={'name': 'Категория 1'})
product_urls = get_list_products_in_category(supplier)
```

### `paginator`

**Назначение**:  Проверка  наличия  следующей  страницы  в  пагинации. 

**Параметры**:

- `d` (`Driver`): Экземпляр класса `Driver`. 
- `locator` (`dict`): Локатор  для  кнопки  "Следующая страница".
- `list_products_in_category` (`list`):  Список  ссылок  на  товары,  полученный  ранее.

**Возвращает**:

- `bool`: `True`,  если  следующая  страница  найдена,  `None`  в  противном  случае.

**Как работает функция**:

1. Использует `Driver` для поиска элемента, соответствующего локатору `locator`.
2. Проверяет, найден ли элемент. Если  не  найден,  возвращает  `None`.
3. Если элемент найден,  переходит  на  следующую  страницу  и  возвращает  `True`.

**Примеры**:

```python
# Пример вызова функции с объектом Driver и локатором
driver = Driver(Chrome)
locator = {'pagination': {'<->': {'by': 'XPATH', 'selector': '//a[@rel="next"]'}}}
product_urls = []  # Список ссылок на товары
has_next_page = paginator(driver, locator, product_urls) 
```

### `get_list_categories_from_site`

**Назначение**:  Сбор  актуальных  категорий  с  сайта  поставщика.

**Параметры**:

- `s` (`Supplier`): Экземпляр  класса  `Supplier`.

**Возвращает**:

- `list`:  Список  категорий. 

**Как работает функция**: 

1.  Использует  `Driver` и `locators`  из  объекта  `Supplier`.
2.  Находит  список  категорий на сайте.
3.  Извлекает  название  и  ссылку  на  каждую  категорию.
4.  Возвращает  список  категорий. 

**Примеры**:

```python
# Пример вызова функции с объектом Supplier
supplier = Supplier(driver=Driver(Chrome), locators={'category': {'product_links': {'by': 'XPATH', 'selector': '//a[@class="product-link"]'}}}, current_scenario={'name': 'Категория 1'})
categories = get_list_categories_from_site(supplier)
```

## Внутренние функции

#### `grab_product_page`
**Назначение**:   Обработка страницы товара. 

**Параметры**:

- `url` (`str`): URL-адрес страницы  товара.

**Возвращает**:

- `dict`:  Словарь,  содержащий  данные  товара  или  `None`.

**Как работает функция**:

1.  Создает  экземпляр  класса `Product`  с  помощью  `url`  страницы.
2.  Извлекает  необходимые  данные  с  помощью  `Driver`  и  `locators`  из  объекта  `Supplier`.
3.  Добавляет  извлеченные  данные  в  объект  `Product`.
4.  Возвращает  `Product`.

**Примеры**:

```python
# Пример вызова функции с URL-адресом страницы товара
product_url = 'https://kualastyle.il/product/4352421482'
product_data = grab_product_page(product_url)
```

## Параметры класса `Supplier`

- `driver`:  Экземпляр класса `Driver` ( `src.webdriver.driver`), представляющий `Webdriver` для работы с сайтом.
- `locators`:  Словарь, содержащий `locators`  для  идентификации  веб-элементов на сайте  поставщика. 
- `current_scenario`: Словарь,  содержащий  информацию  о  текущем сценарии.


## Примеры

### Примеры использования модуля `scenario.py`

```python
# Создание инстанса драйвера
driver = Driver(Chrome)

# Создание инстанса поставщика
supplier = Supplier(driver=driver, locators={'category': {'product_links': {'by': 'XPATH', 'selector': '//a[@class="product-link"]'}}}, current_scenario={'name': 'Категория 1'})

# Получение списка категорий
categories = get_list_categories_from_site(supplier)

# Итерация по категориям
for category in categories:
    # Получение списка товаров
    product_urls = get_list_products_in_category(supplier)
    
    # Итерация по товарам
    for product_url in product_urls:
        # Получение данных товара
        product_data = grab_product_page(product_url)

        # Обработка данных товара (сохранение в базу данных, отправка на обработку и т.д.)
        ...

```

### Примеры вызова функции `get_list_products_in_category`

```python
# Вызов функции с объектом Supplier
supplier = Supplier(driver=Driver(Chrome), locators={'category': {'product_links': {'by': 'XPATH', 'selector': '//a[@class="product-link"]'}}}, current_scenario={'name': 'Категория 1'})
product_urls = get_list_products_in_category(supplier)

# Вызов функции с объектом Supplier и категорией
category_name = 'Категория 1'
supplier = Supplier(driver=Driver(Chrome), locators={'category': {'product_links': {'by': 'XPATH', 'selector': '//a[@class="product-link"]'}}}, current_scenario={'name': category_name})
product_urls = get_list_products_in_category(supplier)
```

### Примеры вызова функции `paginator`

```python
# Вызов функции с объектом Driver и локатором
driver = Driver(Chrome)
locator = {'pagination': {'<->': {'by': 'XPATH', 'selector': '//a[@rel="next"]'}}}
product_urls = []  # Список ссылок на товары
has_next_page = paginator(driver, locator, product_urls) 

# Вызов функции с объектом Driver, локатором и списком товаров
driver = Driver(Chrome)
locator = {'pagination': {'<->': {'by': 'XPATH', 'selector': '//a[@rel="next"]'}}}
product_urls = ['https://kualastyle.il/product/4352421482', 'https://kualastyle.il/product/4352421483']
has_next_page = paginator(driver, locator, product_urls) 
```

### Примеры вызова функции `get_list_categories_from_site`

```python
# Вызов функции с объектом Supplier
supplier = Supplier(driver=Driver(Chrome), locators={'category': {'product_links': {'by': 'XPATH', 'selector': '//a[@class="product-link"]'}}}, current_scenario={'name': 'Категория 1'})
categories = get_list_categories_from_site(supplier)

# Вызов функции с объектом Supplier и списком категорий
categories = ['Категория 1', 'Категория 2', 'Категория 3']
supplier = Supplier(driver=Driver(Chrome), locators={'category': {'product_links': {'by': 'XPATH', 'selector': '//a[@class="product-link"]'}}}, current_scenario={'name': 'Категория 1'})
categories = get_list_categories_from_site(supplier)
```

### Примеры вызова функции `grab_product_page`

```python
# Вызов функции с URL-адресом страницы товара
product_url = 'https://kualastyle.il/product/4352421482'
product_data = grab_product_page(product_url)

# Вызов функции с URL-адресом страницы товара и объектом Supplier
product_url = 'https://kualastyle.il/product/4352421482'
supplier = Supplier(driver=Driver(Chrome), locators={'category': {'product_links': {'by': 'XPATH', 'selector': '//a[@class="product-link"]'}}}, current_scenario={'name': 'Категория 1'})
product_data = grab_product_page(product_url, supplier)
```

##  Внутренние функции
**Внутренние функции**:
-  `grab_product_page`:  обработка страницы товара,  получение  данных  товара  с  страницы  и  заполнение  объекта  `Product`.
-  `paginator`:  проверка  наличия  следующей  страницы  в  пагинации,  позволяет  пролистать  все  страницы  категории.