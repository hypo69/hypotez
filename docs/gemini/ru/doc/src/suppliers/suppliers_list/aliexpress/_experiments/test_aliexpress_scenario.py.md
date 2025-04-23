# Документация для модуля `test_aliexpress_scenario.py`

## Обзор

Модуль `test_aliexpress_scenario.py` предназначен для проведения экспериментов и тестирования сценариев работы с поставщиком AliExpress в рамках проекта `hypotez`. Он включает в себя функции для инициализации поставщика, настройки тестовых сценариев и создания объектов товаров для тестирования.

## Подробней

Модуль содержит функции для эмуляции запуска поставщика (`Supplier`) и инициализации объектов `Product` с тестовыми данными, такими как категории и локаторы веб-элементов. Он также содержит примеры тестовых сценариев и списки URL товаров для тестирования. Код предназначен для проверки взаимодействия с AliExpress, включая получение данных о товарах и добавление их в PrestaShop.

## Классы

В данном модуле классы отсутствуют.

## Функции

### `start_supplier`

```python
def start_supplier(supplier_prefix):
    """
    Инициализирует и возвращает объект класса `Supplier` с заданным префиксом.

    Args:
        supplier_prefix (str): Префикс поставщика, используемый для настройки объекта `Supplier`.

    Returns:
        Supplier: Объект класса `Supplier`, созданный с указанным префиксом.

    """
```

**Назначение**: Инициализация объекта поставщика `Supplier`.

**Параметры**:

-   `supplier_prefix` (str): Префикс поставщика, используемый для настройки объекта `Supplier`.

**Возвращает**:

-   `Supplier`: Объект класса `Supplier`, созданный с указанным префиксом.

**Как работает функция**:

Функция принимает префикс поставщика (`supplier_prefix`) в качестве аргумента, создает словарь `params` с этим префиксом, а затем возвращает экземпляр класса `Supplier`, инициализированный с использованием этих параметров.

**Примеры**:

```python
supplier_prefix = 'aliexpress'
s = start_supplier(supplier_prefix)
```

### `start_product`

```python
def start_product():
    """
    Инициализирует и возвращает объект класса `Product` с заданными параметрами, включая информацию о поставщике,
    категориях и локаторах веб-элементов.

    Returns:
        Product: Объект класса `Product`, созданный с указанными параметрами.

    """
```

**Назначение**: Инициализация объекта товара `Product`.

**Возвращает**:

-   `Product`: Объект класса `Product`, созданный с указанными параметрами.

**Как работает функция**:

Функция создает словарь `params`, содержащий информацию о поставщике (`s`), локаторах веб-элементов (`s.locators.get('product')`), категориях товара (`test_scenario['iPhone 13 & 13 MINI']['presta_categories']`). Затем возвращает экземпляр класса `Product`, инициализированный с использованием этих параметров.

**Примеры**:

```python
p = start_product()
```

## Переменные модуля

### `supplier_prefix`

```python
supplier_prefix = 'aliexpress'
```

**Назначение**: Префикс поставщика, используемый для инициализации объекта `Supplier`.

### `s`

```python
s = start_supplier(supplier_prefix)
```

**Назначение**: Объект класса `Supplier`, созданный с префиксом `aliexpress`.

### `test_scenario`

```python
test_scenario: dict = {
    "iPhone 13 & 13 MINI": {
        "category ID on site": 40000002781737,
        "brand": "APPLE",
        "url": "https://hi5group.aliexpress.com/store/group/iPhone-13-13-mini/1053035_40000002781737.html",
        "active": True,
        "condition": "new",
        "presta_categories": {
            "template": {
                "apple": "iPhone 13"
            }
        },
        "product combinations": [
            "bundle",
            "color"
        ]
    }
}
```

**Назначение**: Словарь, содержащий тестовые сценарии для товаров, включая информацию о категории, бренде, URL, и категориях PrestaShop.

### `test_products_list`

```python
test_products_list: list = [
    'https://s.click.aliexpress.com/e/_oFLpkfz',
    'https://s.click.aliexpress.com/e/_oE5V3d9',
    'https://s.click.aliexpress.com/e/_oDnvttN',
    'https://s.click.aliexpress.com/e/_olWWQCP',
    'https://s.click.aliexpress.com/e/_ok0xeMn'
]
```

**Назначение**: Список URL товаров, используемых для тестирования.

### `p`

```python
p = start_product()
```

**Назначение**: Объект класса `Product`, созданный с тестовыми параметрами.

### `d`

```python
d = s.driver
```

**Назначение**: Драйвер веб-браузера, используемый для взаимодействия с веб-сайтом AliExpress.

### `_`

```python
_ = d.execute_locator
```

**Назначение**: Ссылка на функцию `execute_locator` драйвера, используемая для поиска веб-элементов на странице.

### `f`

```python
f = p.fields
```

**Назначение**: Объект, содержащий поля товара, такие как reference и price.

### `l`

```python
l = p.webelements_locators
```

**Назначение**: Локаторы веб-элементов, используемые для поиска элементов на странице товара.