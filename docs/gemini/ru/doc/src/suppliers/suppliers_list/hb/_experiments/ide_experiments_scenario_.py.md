# Модуль: src.suppliers.hb._experiments.ide_experiments_scenario_.py

## Обзор

Модуль предназначен для экспериментов с наполнением полей товара (product_fields) данными, полученными от поставщика HB.

## Подробней

Этот файл содержит код, предназначенный для проверки и экспериментов с процессом заполнения данных о товарах на основе информации, предоставляемой поставщиком HB. Он включает в себя настройку путей, импорт необходимых модулей и классов, а также создание экземпляров основных объектов, таких как поставщик, товар, локаторы и драйвер.

## Классы

### `Supplier`

**Описание**: Класс, представляющий поставщика товаров.

**Атрибуты**:

-   `supplier_prefix` (str): Префикс поставщика (например, 'hb').

### `Product`

**Описание**: Класс, представляющий товар.

**Атрибуты**:

-   `s` (Supplier): Экземпляр класса `Supplier`, связанный с товаром.

### `ProductFields`

**Описание**: Класс, представляющий поля товара.

**Атрибуты**:

-   `s` (Supplier): Экземпляр класса `Supplier`, связанный с полями товара.

## Переменные

-   `dir_root` (Path): Корневая директория проекта `hypotez`.
-   `dir_src` (Path): Директория `src` внутри корневой директории проекта.
-   `s` (Supplier): Экземпляр класса `Supplier` с префиксом 'hb'.
-   `p` (Product): Экземпляр класса `Product`, связанный с поставщиком `s`.
-   `l` (dict): Локаторы элементов продукта, полученные из атрибута `locators['product']` поставщика `s`.
-   `d` (Driver): Драйвер, связанный с поставщиком `s`.
-   `f` (ProductFields): Экземпляр класса `ProductFields`, связанный с поставщиком `s`.
-   `s.current_scenario` (dict): Словарь, представляющий текущий сценарий, включающий URL, название, состояние и категории PrestaShop.

## Функции

### `run_scenarios(s: Supplier, current_scenario: dict) -> Any`

**Назначение**: Выполняет сценарии для заданного поставщика и текущего сценария.

**Параметры**:

-   `s` (Supplier): Экземпляр класса `Supplier`.
-   `current_scenario` (dict): Словарь, представляющий текущий сценарий.

**Возвращает**:

-   `Any`: Результат выполнения сценариев.

**Как работает функция**:

Функция вызывает `run_scenarios` с текущим сценарием и поставщиком, чтобы запустить процесс сбора и обработки данных о товарах.

**Примеры**:

```python
from src.suppliers.hb._experiments.ide_experiments_scenario_ import Supplier, Product, ProductFields
from src.webdriver.driver import Driver
from pathlib import Path
import os, sys

dir_root: Path = Path(os.getcwd()[:os.getcwd().rfind('hypotez') + 7])
sys.path.append(str(dir_root))  # Adding the root folder to sys.path

s: Supplier = Supplier(supplier_prefix = 'hb')
p: Product = Product(s)
l: dict = s.locators['product']
d: Driver = s.driver
f: ProductFields = ProductFields(s)

s.current_scenario: dict =  {
      "url": "https://hbdeadsea.co.il/product-category/bodyspa/feet-hand-treatment/",
      "name": "טיפוח כפות ידיים ורגליים",
      "condition": "new",
      "presta_categories": {
        "default_category": 11259,
        "additional_categories": []
      }
    }

# Пример вызова функции run_scenarios
#ret = run_scenarios(s, s.current_scenario)