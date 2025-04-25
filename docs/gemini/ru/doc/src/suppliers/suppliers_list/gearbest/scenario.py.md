# Модуль сбора товаров со страницы категорий поставщика bangood.co.il

## Обзор

Модуль `scenario.py` содержит функции для сбора товаров со страниц категорий поставщика bangood.co.il. 

## Подробнее

Этот модуль работает следующим образом:

- Сначала он собирает список категорий со страниц продавца с помощью функции `get_list_categories_from_site()`.
- Затем он перебирает категории и собирает список товаров со страниц категорий с помощью функции `get_list_products_in_category()`.
- После этого он перебирает полученные товары и передает управление функции `grab_product_page()`, которая обрабатывает поля товара и передает управление классу `Product`.

## Функции

### `get_list_products_in_category`

**Назначение**: Функция собирает список товаров со страницы категории.

**Параметры**:

- `s`: Объект `Supplier`, представляющий поставщика bangood.

**Возвращает**:

- `list[str, str, None]`: Список ссылок на товары или `None`, если товаров не найдено.

**Как работает**:

1. Извлекает локатор категории из объекта `Supplier`.
2. Выполняет локатор `close_banner`, чтобы закрыть всплывающее окно, если оно есть.
3. Проверяет наличие локатора категории. Если локатора нет, выводит ошибку и возвращает `None`.
4. Выполняет прокрутку страницы.
5. Извлекает ссылки на товары с помощью локатора `product_links`.
6. Проверяет, найдено ли хотя бы одно значение.
7. Если найдено несколько значений - сохраняет их в список. Если найдено одно значение - сохраняет его в список, состоящий из одного элемента.
8. Выводит сообщение о количестве найденных товаров.

**Пример**:

```python
from src.suppliers.bangood.scenario import get_list_products_in_category
from src.suppliers import Supplier
# Создайте объект Supplier
supplier = Supplier(...)
# Вызовите функцию
products = get_list_products_in_category(supplier)
# Выведите результат
print(products)
```

### `get_list_categories_from_site`

**Назначение**: Функция собирает список категорий со страниц продавца.

**Параметры**:

- `s`: Объект `Supplier`, представляющий поставщика bangood.

**Возвращает**:

- `...`: Возвращаемое значение не указано.

**Как работает**:

Функция `get_list_categories_from_site()` собирает список категорий со страниц продавца. Она использует вебдрайвер для навигации по страницам продавца и извлечения ссылок на категории. 
**Пример**:

```python
from src.suppliers.bangood.scenario import get_list_categories_from_site
from src.suppliers import Supplier
# Создайте объект Supplier
supplier = Supplier(...)
# Вызовите функцию
categories = get_list_categories_from_site(supplier)
# Выведите результат
print(categories)
```

## Примеры

```python
from src.suppliers.bangood.scenario import get_list_products_in_category, get_list_categories_from_site
from src.suppliers import Supplier
# Создайте объект Supplier
supplier = Supplier(...)
# Вызовите функцию get_list_categories_from_site()
categories = get_list_categories_from_site(supplier)
# Выведите результат
print(categories)
# Вызовите функцию get_list_products_in_category() для каждой категории
for category in categories:
    products = get_list_products_in_category(supplier, category)
    # Выведите результат
    print(products)