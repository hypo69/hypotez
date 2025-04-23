### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода представляет собой тестовый сценарий для работы с поставщиком AliExpress, включая инициализацию поставщика, настройку параметров продукта и добавление товара в базу данных PrestaShop.

Шаги выполнения
-------------------------
1. **Инициализация поставщика**:
   - Определяется функция `start_supplier`, которая принимает префикс поставщика (`supplier_prefix`) и инициализирует класс `Supplier` с этим префиксом.
   - Задается префикс поставщика `supplier_prefix = 'aliexpress'`.
   - Создается экземпляр класса `Supplier` с помощью `s = start_supplier(supplier_prefix)`.

2. **Настройка тестового сценария**:
   - Определяется словарь `test_scenario`, содержащий данные для тестового товара "iPhone 13 & 13 MINI", такие как ID категории на сайте, бренд, URL, активность, состояние, категории PrestaShop и комбинации продуктов.
   - Определяется список `test_products_list`, содержащий URL тестовых товаров.

3. **Инициализация продукта**:
   - Определяется функция `start_product`, которая инициализирует класс `Product` с параметрами, необходимыми для работы с товаром.
   - Параметры включают: экземпляр класса `Supplier` (`s`), локаторы веб-элементов (`webelements_locators`), категории товара (`product_categories`).
   - Создается экземпляр класса `Product` с помощью `p = start_product()`.

4. **Работа с WebDriver**:
   - Получается экземпляр `WebDriver` из класса `Supplier` (`d = s.driver`).
   - Определяются сокращения для функций и атрибутов: `_ = d.execute_locator`, `f = p.fields`, `l = p.webelements_locators`.

5. **Получение данных о продукте**:
   - Открывается URL первого товара из списка `test_products_list` с помощью `d.get_url(test_products_list[0])`.
   - Извлекается артикул товара из URL и присваивается полю `reference` объекта `f` (поля продукта).
   - Извлекается цена товара с использованием локатора `l['price']` и присваивается полю `price` объекта `f`.

6. **Добавление товара в PrestaShop**:
   - Проверяется, существует ли товар с данным артикулом в базе данных PrestaShop с помощью `p.check_if_product_in_presta_db(f.reference)`.
   - Если товара нет в базе данных, он добавляется с помощью `p.add_2_PrestaShop(f)`.

Пример использования
-------------------------

```python
import sys
import os
path = os.getcwd()[:os.getcwd().rfind(r'hypotez')+7]
sys.path.append(path)  # Добавляю корневую папку в sys.path
# ----------------
from pathlib import Path

# ----------------
from src import gs

from src.product import Product
from categories import Category
from src.logger.logger import logger


def start_supplier(supplier_prefix):
    params: dict = {
        'supplier_prefix': supplier_prefix
    }
    
    return Supplier(**params)


supplier_prefix = 'aliexpress'
s = start_supplier(supplier_prefix)
""" s - на протяжении всего кода означает класс `Supplier` """


print(" Можно продолжать ")


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


test_products_list: list = ['https://s.click.aliexpress.com/e/_oFLpkfz', 
                            'https://s.click.aliexpress.com/e/_oE5V3d9', 
                            'https://s.click.aliexpress.com/e/_oDnvttN', 
                            'https://s.click.aliexpress.com/e/_olWWQCP', 
                            'https://s.click.aliexpress.com/e/_ok0xeMn']

def start_product():
    """ и категории и локаторы и product_fields нужны при инициализации класса Product для наглядности тестов 
    по умолачанию локаторы и так содержатся к классе `Supplier`
    """
    
    params: dict = {
        'supplier':s,
        'webelements_locators':s.locators.get('product'),
        'product_categories':test_scenario['iPhone 13 & 13 MINI']['presta_categories'],
        #'product_fields':product_fields,
    }
    
    return Product(**params)

p = start_product()

d = s.driver
_ = d.execute_locator
f = p.fields
l = p.webelements_locators

d.get_url(test_products_list[0])

f.reference = d.current_url.split('/')[
    -1].split('.')[0]  # Извлекает reference (артикул) из URL
f.price = _(l['price'])

if not p.check_if_product_in_presta_db(f.reference):
    p.add_2_PrestaShop(f)