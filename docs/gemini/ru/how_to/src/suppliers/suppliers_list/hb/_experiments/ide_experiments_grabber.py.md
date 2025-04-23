### Как использовать этот блок кода

=========================================================================================

Описание
-------------------------
Данный блок кода инициализирует основные объекты и переменные, необходимые для выполнения сценариев парсинга и обработки данных о товарах с веб-сайта поставщика HB. Он включает в себя настройку пути к корневой директории проекта, импорт необходимых модулей и создание экземпляров классов для работы с поставщиком, товарами, локаторами и веб-драйвером. Также устанавливается текущий сценарий для парсинга определенной страницы сайта.

Шаги выполнения
-------------------------
1. **Инициализация путей и добавление в `sys.path`**:
   - Определяется корневая директория проекта `hypotez`.
   - Добавляет корневую директорию и директорию `src` в `sys.path`, что позволяет импортировать модули из этих директорий.

2. **Импорт необходимых модулей и классов**:
   - Импортируются классы и модули, такие как `Supplier`, `Product`, `ProductFields`, `Driver`, `logger`, `run_scenarios`, `StringFormatter`, `StringNormalizer` и другие, необходимые для работы скрипта.

3. **Создание экземпляров классов**:
   - Создается экземпляр класса `Supplier` с префиксом `'hb'`.
   - Создается экземпляр класса `Product`, принимающий экземпляр `Supplier`.
   - Извлекаются локаторы продукта из `s.locators["product"]` в словарь `l`.
   - Создается экземпляр класса `Driver`, используемый `s.driver`.
   - Создается экземпляр класса `ProductFields`, принимающий экземпляр `Supplier`.

4. **Установка текущего сценария**:
   - Определяется словарь `s.current_scenario`, содержащий информацию о URL, имени, состоянии и категориях PrestaShop для текущего сценария парсинга.

5. **Выполнение сценария**:
   - Открывается URL, указанный в `s.current_scenario['url']`, с использованием `d.get_url()`.
   - Запускаются сценарии парсинга с использованием функции `run_scenarios()`.
   - Вызывается функция `s.related_modules.grab_product_page(s)` для обработки страницы продукта.

Пример использования
-------------------------

```python
import os, sys
from pathlib import Path
from typing import List, Union, Dict
from selenium.webdriver.remote.webelement import WebElement

# добавление корневой директории позволяет мне плясать от печки
dir_root: Path = Path(os.getcwd()[:os.getcwd().rfind('hypotez') + 7])
sys.path.append(str(dir_root))  # Adding the root folder to sys.path
dir_src = Path(dir_root, 'src')
sys.path.append(str(dir_root))
from src.webdriver import executor
"""  добавление корневой директории позволяет мне плясать от печки. """
####################################################################################################

from src import gs
from src.product import Product, ProductFields
from src.scenario import run_scenarios
from src.logger.logger import logger, ExecuteLocatorException
from src.webdriver.driver import Driver
from src.utils import StringFormatter, StringNormalizer
from src.suppliers import Supplier

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