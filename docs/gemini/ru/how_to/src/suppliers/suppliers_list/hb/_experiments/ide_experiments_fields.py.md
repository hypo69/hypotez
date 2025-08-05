## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода представляет собой набор функций, которые собирают информацию о товаре с веб-страницы поставщика HB и преобразуют её в формат, совместимый с базой данных PrestaShop. 

Шаги выполнения
-------------------------
1. **Инициализация**: 
    - Создается объект `Supplier` с именем `s` (используется префикс `hb` для идентификации поставщика).
    - Создается объект `Product` с именем `p` (используется объект `Supplier` `s` для получения необходимой информации).
    - Создается объект `ProductFields` с именем `f` (используется объект `Supplier` `s` для получения необходимой информации).
    - Инициализируется словарь `s.current_scenario` с информацией о текущем сценарии (например, URL категории, имя категории и т. д.).
    - Используется веб-драйвер `d` для перехода на указанный в `s.current_scenario` URL.

2. **Сбор данных о товаре**:
    - Вызывается функция `grab_product_page(s)`, которая собирает значения с веб-элементов на странице товара и преобразует их в поля объекта `ProductFields`.
    - Функция `grab_product_page(s)` включает множество подфункций, каждая из которых отвечает за заполнение определенного поля `ProductFields`. 
    - Например, функция `product_reference_and_volume_and_price_for_100()` извлекает информацию о `volume`, `supplier_reference` и цене за единицу товара (за 100 мл).
    - Функция `set_references()` устанавливает значения `id_supplier`, `supplier_reference` и `reference` для товара.
    -  Функция `field_available_for_order()` определяет доступность товара для заказа, устанавливая `available_for_order` и `active` в `ProductFields`.
    -  Функция `field_description()`  извлекает полное описание товара с веб-страницы и сохраняет его в поле `description_short` объекта `ProductFields`.
    -  Функция `field_id_category_default()` получает значение  "default_category" из `s.current_scenario`  и сохраняет его в поле `id_category_default`.
    -  Функция `field_name()` очищает название товара от лишних символов и записывает в поле `name`  используя `StringNormalizer.normalize_product_name()`.
    -  Функция `field_price()` извлекает цену товара с веб-страницы, нормализует ее используя `StringNormalizer.normalize_price()`  и записывает в поле `price` объекта `ProductFields`. 
    -  Функция `field_link_rewrite()` генерирует значение поля `link_rewrite`  на основе названия товара (поле `name`) используя `StringNormalizer.normalize_link_rewrite()`.
    -  Функция `field_visibility()` получает информацию о видимости товара на веб-странице и записывает ее в поле `visibility` объекта `ProductFields`.

3. **Обработка полученных данных**:
    - В блоке кода создается объект `product_fields` из  `grab_product_page(s)`. 
    -  Создается словарь `presta_fields_dict`, в который передаются  `presta_fields_dict` из объекта `product_fields`.  
    - Удаляется ключ `quantity` из `presta_fields_dict` (запрещено при добавлении нового товара).
    - Создается словарь `assist_fields_dict`  из объекта `product_fields`.
    - Создается переменная `reference` из `presta_fields_dict`  и используется для создания `search_filter_dict`  -  словаря для поиска  товара в PrestaShop.

4. **Добавление товара в PrestaShop**:
    - Используется `Product`  `p`  для поиска товара по `search_filter_dict` в PrestaShop (версия API  `V3`). 
    - Если товар не найден,  то используется функция `p.add()`  для добавления нового товара в PrestaShop.
    -  В случае добавления нового товара передается  `presta_fields_dict`   в JSON-формате (версия API  `V3`). 
    - В случае успеха (или ошибки)  код `...` -  продолжение обработки.

Пример использования
-------------------------

```python
# Инициализация объекта `Supplier`
s: Supplier = Supplier(supplier_prefix='hb')

# Вызов функции `grab_product_page` для сбора данных
product_fields = grab_product_page(s)

# Получение словаря с полями PrestaShop
presta_fields_dict: Dict = product_fields.presta_fields_dict

# Добавление товара в PrestaShop
p.add(presta_fields_dict, 'JSON', 'V3')
```