# Модуль: `test_1_murano_glass_scenario.py`

## Обзор

Модуль `test_1_murano_glass_scenario.py` предназначен для экспериментов со сценариями получения данных о товарах "Муранское стекло" с сайта Amazon и их последующей загрузки или обновления в базе данных PrestaShop. Он включает в себя определение сценария для конкретного товара, получение данных о товаре со страницы Amazon и взаимодействие с API PrestaShop для добавления или обновления информации о товаре.

## Подробнее

Модуль выполняет следующие основные шаги:

1.  **Инициализация**: Запускает поставщика (supplier) с префиксом `'amazon'` и определяет текущий сценарий, включающий URL товара на Amazon, условия (состояние товара), категории PrestaShop и правило цены.
2.  **Получение данных со страницы товара**: Использует локаторы для извлечения данных о товаре, таких как ASIN, название и URL изображений.
3.  **Проверка наличия товара в базе данных PrestaShop**: Проверяет, существует ли товар с данным reference (комбинация supplier_id и ASIN) в базе данных PrestaShop.
4.  **Загрузка или обновление товара**: Если товар уже существует в базе данных, обновляет его изображение. Если товар отсутствует, собирает все необходимые данные о товаре и добавляет его в базу данных PrestaShop.

## Классы

### `header.Product`

**Описание**: Класс для работы с товарами.

**Методы**:

*   `check_if_product_in_presta_db(product_reference)`: Проверяет, существует ли товар с заданным reference в базе данных PrestaShop.
*   `upload_image2presta(image_url, product_id)`: Загружает изображение товара в PrestaShop.
*   `grab_product_page(s)`: Собирает все необходимые данные о товаре со страницы Amazon.

### `header.Supplier`

**Описание**: Класс, представляющий поставщика товаров.

**Атрибуты**:

*   `supplier_id` (str): Идентификатор поставщика (в данном случае, 'amazon').
*   `current_scenario` (dict): Словарь, содержащий информацию о текущем сценарии, такую как URL товара, условия и категории PrestaShop.
*   `locators` (dict): Локаторы элементов на странице товара Amazon.
*   `driver`: Инстанс веб-драйвера для взаимодействия с веб-страницей.

## Функции

### `start_supplier(supplier_prefix: str) -> Supplier`

**Назначение**: Функция для инициализации и запуска поставщика товаров.

**Параметры**:

*   `supplier_prefix` (str): Префикс поставщика (например, 'amazon').

**Возвращает**:

*   `Supplier`: Объект класса `Supplier`, представляющий запущенного поставщика.

**Как работает функция**:

Функция `start_supplier` инициализирует поставщика на основе переданного префикса. Она создает экземпляр класса `Supplier`, выполняет необходимые настройки и возвращает этот экземпляр для дальнейшего использования в коде.

### `_()`

```python
_ = d.execute_locator
```

**Назначение**: Функция для выполнения локатора с использованием веб-драйвера.

**Параметры**:

*   `l` (dict): Словарь с параметрами локатора.

**Возвращает**:

*   `WebElement`: Найденный веб-элемент или `None`, если элемент не найден.

**Как работает функция**:

Функция `_` является сокращением для `d.execute_locator`, где `d` - это инстанс веб-драйвера. Она выполняет поиск элемента на веб-странице с использованием заданного локатора и возвращает найденный веб-элемент. Если элемент не найден, возвращается `None`.

### Основная часть скрипта

**Назначение**: Выполнение основного сценария получения данных о товаре и их загрузки или обновления в базе данных PrestaShop.

**Как работает**:

1.  **Получение URL товара**: Извлекается URL товара из текущего сценария (`s.current_scenario['url']`).
2.  **Получение ASIN товара**: Извлекается ASIN товара с использованием локатора `'ASIN'`.
3.  **Формирование reference товара**: Формируется reference товара как комбинация `supplier_id` и `ASIN`.
4.  **Проверка наличия товара в базе данных**: Вызывается метод `Product.check_if_product_in_presta_db` для проверки наличия товара в базе данных PrestaShop.
5.  **Обработка товара**:
    *   Если товар уже существует в базе данных (возвращается `product_id`):
        *   Обновляется изображение товара в PrestaShop с использованием `Product.upload_image2presta`.
    *   Если товар отсутствует в базе данных (возвращается `False`):
        *   Собираются данные о товаре с использованием `Product.grab_product_page`.
        *   Формируется словарь `product_dict` с данными о товаре.
        *   Извлекается название товара и очищается от лишних символов.
        *   Выводится словарь `product_dict` (закомментировано добавление товара в PrestaShop).

```python
if not isinstance(product_id, bool):
    """ Если не вернулся False, значит товар уже в бд, я полуну его id_product
    здесь обработка product_update
    """
    Product.upload_image2presta(image_url = default_image_url, product_id = product_id)
    ...

else:
    product_fields: ProductFields = Product.grab_product_page(s)

   
    product_dict: dict = {}
    product_dict['product']: dict = dict(product_fields.fields)
    #product_dict['product']['wholesale_price'] = product_dict['product']['price'] = float(product_dict['product']['wholesale_price'] )
    #
    product_name = _(l['name'])[0]
    
    res_product_name = ''
    for n in product_name:
        res_product_name += n
    product_dict['product']['name'] = res_product_name.strip("\'").strip('"').strip('\n')
    pprint(product_dict)
    #pprint(PrestaProduct.add(product_dict))
```

**Примеры**:

Пример использования:

```python
from header import start_supplier, Product

supplier_prefix = 'amazon'
s = start_supplier(supplier_prefix)

s.current_scenario = {
      "url": "https://amzn.to/3OhRz2g",
      "condition": "new",
      "presta_categories": {
        "default_category": { "11209": "MURANO GLASS" },
        "additional_categories": [ "" ]
      },
      "price_rule": 1
    }
l = s.locators.get('product')
d = s.driver
_ = d.execute_locator

ASIN = _(l['ASIN'])

product_reference = f"{s.supplier_id}-{ASIN}"
product_id = Product.check_if_product_in_presta_db(product_reference)
print(f' Если товар в бд получу id_product, иначе False. Получил: {product_id}')

default_image_url = _(l['additional_images_urls'])[0]

if not isinstance(product_id, bool):
    """ Если не вернулся False, значит товар уже в бд, я полуну его id_product
    здесь обработка product_update
    """
    Product.upload_image2presta(image_url = default_image_url, product_id = product_id)
    print("Изображение товара обновлено в PrestaShop")

else:
    product_fields = Product.grab_product_page(s)
    product_dict = {}
    product_dict['product'] = dict(product_fields.fields)
    product_name = _(l['name'])[0]
    res_product_name = ''
    for n in product_name:
        res_product_name += n
    product_dict['product']['name'] = res_product_name.strip("\'").strip('"').strip('\n')
    print(product_dict)
    #pprint(PrestaProduct.add(product_dict))