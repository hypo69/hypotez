# Модуль для работы с поставщиком Morlevi

## Обзор

Модуль `__morlevi__.py` предназначен для автоматизации взаимодействия с веб-сайтом поставщика Morlevi. Он включает в себя функции для входа в систему, сбора информации о товарах и навигации по категориям товаров.

## Подробней

Этот модуль является частью системы автоматизации сбора данных о товарах от различных поставщиков для проекта `hypotez`. Он использует библиотеки `selenium` для управления браузером, `requests` для отправки HTTP-запросов и `pandas` для работы с данными. Модуль содержит функции для авторизации на сайте поставщика, сбора информации о товарах со страниц категорий и отдельных страниц товаров, а также для обработки различных сценариев, возникающих в процессе работы.

## Функции

### `login`

```python
def login(supplier):
    """
    Осуществляет вход на сайт поставщика.

    Args:
        supplier: Объект поставщика, содержащий параметры подключения и драйвер веб-браузера.

    Returns:
        bool: `True`, если вход выполнен успешно, иначе `False`.
    
    """
```

**Как работает функция**:
- Функция пытается войти на сайт поставщика, используя предоставленные учетные данные.
- Если вход не удался с первой попытки, функция пытается закрыть возможные всплывающие окна, которые могут блокировать процесс входа.
- В случае неудачи логирует ошибку.

### `_login`

```python
def _login(_s):
    """
    Выполняет фактический процесс входа на сайт Morlevi.

    Args:
        _s: Объект поставщика, содержащий параметры подключения и драйвер веб-браузера.

    Returns:
        bool: `True`, если вход выполнен успешно, иначе `False`.

    """
```

**Как работает функция**:
- Обновляет страницу.
- Использует локаторы для нахождения элементов ввода email, пароля и кнопки входа.
- Заполняет поля и нажимает на кнопку входа.
- Логирует успешный вход или ошибку в случае неудачи.

### `grab_product_page`

```python
def grab_product_page(s):
    """
    Собирает информацию со страницы товара.

    Args:
        s: Объект поставщика, содержащий параметры подключения и драйвер веб-браузера.

    Returns:
        Product: Объект `Product`, содержащий собранную информацию о товаре.

    """
```

**Как работает функция**:
- Создает экземпляр класса `Product`.
- Определяет внутренние функции для установки различных полей продукта, таких как ID, SKU, название, описание, цена и изображения.
- Вызывает эти внутренние функции для заполнения полей продукта.
- Возвращает объект `Product` с заполненными данными.

**Внутренние функции**:
- `set_id`: Извлекает идентификатор товара.
- `set_sku_suppl`: Устанавливает артикул поставщика.
- `set_sku_prod`: Формирует SKU товара.
- `set_title`: Устанавливает заголовок товара, беря его из заголовка страницы.
- `set_summary`: Извлекает краткое описание товара.
- `set_description`: Извлекает полное описание товара.
- `set_cost_price`: Извлекает и очищает цену товара, применяет правило ценообразования.
- `set_before_tax_price`: Устанавливает цену без налога.
- `set_delivery`: <TODO  перенести в комбинации >
- `set_images`: Извлекает URL изображений товара.
- `set_combinations`: ...
- `set_qty`: ...
- `set_specification`: Извлекает спецификацию товара.
- `set_customer_reviews`: ...
- `set_supplier`: Устанавливает идентификатор поставщика.
- `set_rewritted_URL`: ...

### `list_products_in_category_from_pagination`

```python
def list_products_in_category_from_pagination(supplier):
    """
    Собирает список ссылок на товары в категории, переходя по страницам пагинации.

    Args:
        supplier: Объект поставщика, содержащий параметры подключения и драйвер веб-браузера.

    Returns:
        list: Список URL-адресов товаров в категории.

    """
```

**Как работает функция**:

- Получает список товаров на странице.
- Проверяет, является ли возвращенный список адресов `None` или пустым. Если да, возвращает пустой список.
- Если список не пустой, расширяет список `list_products_in_category` полученными значениями.
- Находит элементы пагинации и переходит по страницам, собирая ссылки на товары с каждой страницы.
- Удаляет дубликаты из списка ссылок.
- Возвращает список URL-адресов товаров в категории.

### `get_list_products_in_category`

```python
def get_list_products_in_category(s, scenario, presath):
    """
    s:Supplier
    scenario:JSON
    presath:PrestaShopWebServiceDict
    """
```

**Как работает функция**:
-   Вызывает `list_products_in_category_from_pagination` для получения списка товаров
-   ...

### `get_list_categories_from_site`

```python
def get_list_categories_from_site(s,scenario_file,brand=''):
    """
    ...
    """
```
## Оглавление

1.  [Обзор](#обзор)
2.  [Подробней](#подробней)
3.  [Функции](#функции)
    *   [login](#login)
    *   [_login](#_login)
    *   [grab_product_page](#grab_product_page)
        *   [set_id](#set_id)
        *   [set_sku_suppl](#set_sku_suppl)
        *   [set_sku_prod](#set_sku_prod)
        *   [set_title](#set_title)
        *   [set_summary](#set_summary)
        *   [set_description](#set_description)
        *   [set_cost_price](#set_cost_price)
        *   [set_before_tax_price](#set_before_tax_price)
        *   [set_delivery](#set_delivery)
        *   [set_images](#set_images)
        *   [set_combinations](#set_combinations)
        *   [set_qty](#set_qty)
        *   [set_specification](#set_specification)
        *   [set_customer_reviews](#set_customer_reviews)
        *   [set_supplier](#set_supplier)
        *   [set_rewritted_URL](#set_rewritted_URL)
    *   [list_products_in_category_from_pagination](#list_products_in_category_from_pagination)
    *   [get_list_products_in_category](#get_list_products_in_category)
    *   [get_list_categories_from_site](#get_list_categories_from_site)