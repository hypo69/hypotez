# Модуль для экспериментов по извлечению данных с сайта HB

## Обзор

Этот модуль предназначен для экспериментов по извлечению данных о товарах с сайта поставщика HB (hbdeadsea.co.il). Он включает в себя получение информации о товарах и отправку ее на сервер. Модуль использует Selenium для автоматизации действий в браузере, а также другие модули проекта `hypotez` для работы с поставщиками, товарами, сценариями и логированием.

## Подробней

Модуль предназначен для тестирования и экспериментов, связанных с процессом сбора данных о товарах с сайта HB. Он позволяет автоматизировать навигацию по сайту, извлечение необходимой информации и отправку её на сервер. В коде задаются параметры для подключения к сайту, сценарий работы с сайтом, а также основные объекты, необходимые для работы (поставщик, продукт, локаторы, драйвер и поля продукта).

## Классы

В данном коде классы явно не определены. Используются объекты классов, импортированные из других модулей:

- `Supplier` (из `src.suppliers`): Представляет поставщика товаров.
- `Product` (из `src.product`): Представляет товар.
- `ProductFields` (из `src.product`): Представляет поля товара.
- `Driver` (из `src.webdriver.driver`): Представляет веб-драйвер для управления браузером.

## Функции

В явном виде функции не определены. Используются функции из других модулей:

- `run_scenarios` (из `src.scenario`): Запускает сценарии для поставщика.
- `s.related_modules.grab_product_page(s)`:  Извлекает информацию о товаре со страницы продукта.

## Переменные

- `dir_root` (Path): Корневая директория проекта `hypotez`.
- `sys.path` (List[str]): Список путей для поиска модулей Python.
- `dir_src` (Path): Путь к директории `src` внутри проекта `hypotez`.
- `s` (Supplier): Объект класса `Supplier` с префиксом 'hb'.
- `p` (Product): Объект класса `Product`, связанный с поставщиком `s`.
- `l` (Dict): Словарь локаторов для продукта, полученный из `s.locators["product"]`.
- `d` (Driver): Объект класса `Driver`, представляющий веб-драйвер, полученный из `s.driver`.
- `f` (ProductFields): Объект класса `ProductFields`, связанный с поставщиком `s`.
- `s.current_scenario` (Dict): Словарь, содержащий информацию о текущем сценарии, включая URL, название, условие и категории PrestaShop.
- `ret`: Результат выполнения сценариев `run_scenarios`.

## Работа с кодом

1.  **Импорт модулей и настройка путей**:

    *   Импортируются необходимые модули и классы из других частей проекта, такие как `Supplier`, `Product`, `Driver` и другие.
    *   Определяются пути к корневой директории проекта и директории `src`, чтобы обеспечить возможность импорта модулей из этих директорий.

2.  **Инициализация объектов**:

    *   Создаются экземпляры классов `Supplier`, `Product`, `ProductFields` и `Driver` с необходимыми параметрами.
    *   Объект `Supplier` инициализируется с префиксом 'hb', что указывает на поставщика HB.
    *   Объект `Product` создается на основе объекта `Supplier`.
    *   Объект `Driver` получается из объекта `Supplier` и представляет собой драйвер для управления браузером.
    *   Объект `ProductFields` создается на основе объекта `Supplier` и предназначен для работы с полями продукта.

3.  **Определение текущего сценария**:

    *   Определяется словарь `s.current_scenario`, содержащий информацию о текущем сценарии, включая URL страницы, название, условие и категории PrestaShop.

4.  **Выполнение сценария**:

    *   Выполняется сценарий с использованием функции `run_scenarios`, которой передаются объекты `s` (поставщик) и `s.current_scenario` (текущий сценарий).

5.  **Извлечение информации о товаре**:

    *   Вызывается метод `s.related_modules.grab_product_page(s)` для извлечения информации о товаре со страницы продукта.

```python
#from math import prod
import os, sys
from pathlib import Path
from typing import List, Union, Dict
from selenium.webdriver.remote.webelement import WebElement

################# добавление корневой директории позволяет мне плясать от печки ###################
dir_root: Path = Path(os.getcwd()[:os.getcwd().rfind('hypotez') + 7])
sys.path.append(str(dir_root))  # Adding the root folder to sys.path
dir_src = Path(dir_root, 'src')
sys.path.append(str(dir_root))
from src.webdriver import executor
"""  добавление корневой директории позволяет мне плясать от печки. """
####################################################################################################


from src import gs
from src.suppliers import Supplier
from src.product import Product, ProductFields
from src.scenario import run_scenarios

from src.logger.logger import logger, ExecuteLocatorException
from src.webdriver.driver import Driver
from src.utils import StringFormatter, StringNormalizer


s: Supplier = Supplier(supplier_prefix = 'hb')
p: Product = Product(s)
l: Dict = s.locators["product"]
d: Driver = s.driver
f: ProductFields = ProductFields(s)

s.current_scenario: Dict =  {
      "url": "https://hbdeadsea.co.il/product-category/bodyspa/feet-hand-treatment/",
      "name": "טיפוח כפות ידיים ורגליים",
      "condition": "new",
      "presta_categories": {
        "default_category": 11259,
        "additional_categories": []
      }
    }

d.get_url(s.current_scenario['url'])
ret = run_scenarios(s, s.current_scenario)
s.related_modules.grab_product_page(s)
```