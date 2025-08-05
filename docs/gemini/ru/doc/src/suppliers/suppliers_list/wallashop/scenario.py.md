# Модуль сбора товаров со страницы категорий поставщика kualastyle.il через вебдрайвер

## Обзор

Модуль `sceanrio.py` предназначен для сбора товаров со страниц категорий поставщика `kualastyle.il` с помощью вебдрайвера. Он состоит из следующих частей:

- **Сбор списка категорий:** Функция `get_list_categories_from_site()` собирает актуальный список категорий с сайта.
- **Сбор списка товаров в категории:** Функция `get_list_products_in_category()` извлекает ссылки на товары со страницы категории, включая пролистывание страниц пагинации.
- **Обработка страницы товара:** Функция `grab_product_page()` обрабатывает поля товара с текущей страницы, используя класс `Product` для сохранения информации.

## Подробнее

Модуль `sceanrio.py` работает по следующему принципу:

1. **Сбор списка категорий:** Функция `get_list_categories_from_site()` получает список категорий с сайта поставщика.
2. **Сбор списка товаров в категории:** Для каждой категории выполняется функция `get_list_products_in_category()`.
3. **Обработка страницы товара:** Для каждой ссылки на товар, полученной из `get_list_products_in_category()`, выполняется функция `grab_product_page()`, которая извлекает информацию о товаре и передает ее классу `Product`.

## Классы

### `class Supplier`

**Описание**: Класс `Supplier` предоставляет набор методов для работы с поставщиком.
**Наследует**: 
**Атрибуты**:
    - `locators`: Словарь локаторов для веб-элементов на сайте поставщика.
    - `driver`: Объект вебдрайвера `Driver`.
    - `current_scenario`: Текущий сценарий (категория) для обработки.

**Методы**: 
    - `get_list_categories_from_site()`: Собирает актуальные категории с сайта.
    - `get_list_products_in_category()`: Извлекает ссылки на товары из текущей категории.
    - `grab_product_page()`: Обрабатывает страницу товара и передает данные в класс `Product`.


## Функции

### `get_list_products_in_category`

**Назначение**: Функция `get_list_products_in_category()` извлекает ссылки на товары со страницы категории.

**Параметры**:
    - `s` (Supplier): Объект класса `Supplier`, представляющий поставщика.

**Возвращает**:
    - `list[str, str, None]`: Список ссылок на товары, полученных со страницы категории.

**Вызывает исключения**:
    - `Exception`: Возникает, если происходит ошибка при извлечении данных.

**Как работает функция**:

1. Получение драйвера и локаторов из объекта `Supplier`.
2. Использование метода `execute_locator()` для получения списка ссылок на товары.
3. Проверка наличия ссылок и вывод сообщения, если ссылок нет.
4. Пролистывание страниц категории с помощью пагинации.
5. Дополнительная обработка полученного списка ссылок.

**Примеры**:

```python
from src.suppliers.suppliers_list.kualastyle.scenario import get_list_products_in_category
from src.suppliers.suppliers_list.kualastyle.supplier import Supplier

# Создание объекта Supplier
supplier = Supplier()

# Получение списка товаров из категории
products = get_list_products_in_category(supplier)

# Вывод результатов
print(f"Найдено товаров: {len(products)}")
for product_url in products:
    print(product_url)
```

### `paginator`

**Назначение**: Функция `paginator()` выполняет пролистывание страниц категории.

**Параметры**:
    - `d` (Driver): Объект вебдрайвера.
    - `locator` (dict): Локатор для элемента пагинации.
    - `list_products_in_category` (list): Список ссылок на товары.

**Возвращает**:
    - `bool`: Возвращает `True`, если пролистывание выполнено успешно, иначе `False`.

**Вызывает исключения**:
    - `Exception`: Возникает, если происходит ошибка при обработке пагинации.

**Как работает функция**:

1. Использование метода `execute_locator()` для поиска элемента пагинации.
2. Проверка наличия элемента пагинации.
3. Выполнение пролистывания, если элемент пагинации найден.
4. Обновление списка ссылок на товары после пролистывания.

**Примеры**:

```python
# Нет примеров, так как функция используется внутри другой функции.
```

### `get_list_categories_from_site`

**Назначение**: Функция `get_list_categories_from_site()` собирает актуальные категории с сайта.

**Параметры**:
    - `s` (Supplier): Объект класса `Supplier`, представляющий поставщика.

**Возвращает**:
    - `list[str, str, None]`: Список категорий, полученных с сайта.

**Вызывает исключения**:
    - `Exception`: Возникает, если происходит ошибка при получении данных.

**Как работает функция**:

1. Извлечение локаторов для элементов списка категорий.
2. Использование метода `execute_locator()` для получения списка категорий.
3. Проверка наличия категорий и вывод сообщения, если категорий нет.

**Примеры**:

```python
from src.suppliers.suppliers_list.kualastyle.scenario import get_list_categories_from_site
from src.suppliers.suppliers_list.kualastyle.supplier import Supplier

# Создание объекта Supplier
supplier = Supplier()

# Получение списка категорий
categories = get_list_categories_from_site(supplier)

# Вывод результатов
print(f"Найдено категорий: {len(categories)}")
for category_name in categories:
    print(category_name)
```

## Параметры класса `Supplier`

- `locators`: Словарь локаторов для веб-элементов на сайте поставщика. Содержит локаторы для элементов списка категорий, ссылок на товары и других элементов, необходимых для работы сценария.
- `driver`: Объект вебдрайвера `Driver`, который используется для взаимодействия с сайтом поставщика.
- `current_scenario`: Текущий сценарий (категория) для обработки.

**Примеры**:

```python
from src.suppliers.suppliers_list.kualastyle.supplier import Supplier

# Создание объекта Supplier
supplier = Supplier()

# Доступ к локаторам
print(supplier.locators['category'])  # Локатор для элементов списка категорий

# Доступ к драйверу
print(supplier.driver)  # Объект вебдрайвера

# Доступ к текущему сценарию
print(supplier.current_scenario)  # Текущая категория
```

## Примеры

```python
from src.suppliers.suppliers_list.kualastyle.scenario import get_list_categories_from_site, get_list_products_in_category, grab_product_page
from src.suppliers.suppliers_list.kualastyle.supplier import Supplier

# Создание объекта Supplier
supplier = Supplier()

# Получение списка категорий
categories = get_list_categories_from_site(supplier)

# Итерация по категориям
for category_name in categories:
    print(f"Обработка категории: {category_name}")
    supplier.current_scenario = {
        "name": category_name
    }
    # Получение списка товаров из категории
    products = get_list_products_in_category(supplier)
    # Итерация по товарам
    for product_url in products:
        print(f"Обработка товара: {product_url}")
        # Обработка страницы товара
        grab_product_page(supplier, product_url)
```
```markdown