# src.suppliers.hb._experiments.ide_experiments_fields

## Обзор

Данный модуль предназначен для экспериментов с полями товаров от поставщика HB (hbdeadsea.co.il) и их сопоставления с полями в PrestaShop. Он содержит функции для сбора данных о товарах со страниц HB, нормализации этих данных и их последующей загрузки или обновления в PrestaShop.

## Подробней

Этот модуль является частью процесса интеграции данных о товарах от поставщика HB в систему PrestaShop. Он включает в себя функции для парсинга веб-страниц с использованием Selenium, извлечения информации о товарах, преобразования этой информации в формат, совместимый с PrestaShop, и выполнения операций добавления или обновления товаров через API PrestaShop. Модуль также содержит логику для обработки изображений товаров и управления различными атрибутами товаров, такими как цена, описание, наличие на складе и т.д.

## Классы

В данном коде классы не объявлены.

## Функции

### `grab_product_page`

```python
def grab_product_page(supplier: Supplier, async_run = True) -> ProductFields:
    """ Собираю со страницы товара значения вебэлементов и привожу их к полям ProductFields

    Args:
        supplier (Supplier): класс поставщика. Вебдрайвер должен быть установлен на странице товара.
        async_run (bool, optional): Флаг для асинхронного выполнения. По умолчанию `True`.

    Returns:
        ProductFields: Объект, содержащий извлеченные и преобразованные поля товара.
    
    Принцип работы:
    - Функция принимает объект `Supplier`, представляющий поставщика, и флаг `async_run`, указывающий, следует ли выполнять код асинхронно.
    - Инициализирует глобальные переменные `s` (Supplier), `p` (Product), `f` (ProductFields) и `l` (locators).
    - Закрывает баннер на странице, если он есть.
    - Прокручивает страницу товара, чтобы загрузить все элементы, отображаемые через AJAX.
    - Вызывает внутренние функции для извлечения конкретных полей товара, таких как `product_reference_and_volume_and_price_for_100` и `set_references`.
    - Вызывает функции для заполнения различных полей товара, таких как `field_additional_shipping_cost`, `field_affiliate_short_link`, `field_available_for_order`, `field_condition` и другие.
    - Извлекает URL изображений товара.
    - Извлекает название товара и создает на его основе `link_rewrite`.
    - Возвращает объект `ProductFields`, содержащий все извлеченные и обработанные поля товара.

    """
    ...
```

### Внутренние функции `grab_product_page`

#### `product_reference_and_volume_and_price_for_100`

```python
def product_reference_and_volume_and_price_for_100():
    """ Функция вытаскивает 3 поля:
    - volume,
    - supplier_reference,
    - цена за единицу товара
    @todo Реализовать поле `цена за единицу товара`"""
    ...
```

Функция извлекает объем товара, артикул поставщика и цену за единицу товара (цену за 100 мл). 
Извлекает веб-элементы, содержащие информацию об объеме, цене за единицу товара и артикуле, и сохраняет их в соответствующие поля объекта `f` (ProductFields).

#### `set_references`

```python
def set_references(f, s):
    """ все, что касается id товара """
    ...
```

Функция устанавливает значения для полей, связанных с идентификаторами товара, таких как `id_supplier` и `reference`.

### `field_additional_shipping_cost`

```python
def field_additional_shipping_cost():
    """
    стоимость доставки
    @details
    """
    ...
```

Извлекает стоимость доставки товара.

### `field_delivery_in_stock`

```python
def field_delivery_in_stock():
    """
    Доставка, когда товар в наличии
    @details
    """
    ...
```

Извлекает информацию о доставке, когда товар есть в наличии.

### `field_active`

```python
def field_active():
    """

    @details
    """
    ...
```

Определяет, активен ли товар.

### `field_additional_delivery_times`

```python
def field_additional_delivery_times():
    """

    @details
    """
    ...
```

Извлекает информацию о дополнительном времени доставки.

### `field_advanced_stock_management`

```python
def field_advanced_stock_management():
    """

    @details
    """
    ...
```

Определяет, используется ли расширенное управление запасами.

### `field_affiliate_short_link`

```python
def field_affiliate_short_link():
    """

    @details
    """
    ...
```

Возвращает короткую партнерскую ссылку на товар.

### `field_affiliate_summary`

```python
def field_affiliate_summary():
    """

    @details
    """
    ...
```

Возвращает краткое описание партнерской программы.

### `field_affiliate_summary_2`

```python
def field_affiliate_summary_2():
    """

    @details
    """
    ...
```

Возвращает дополнительное краткое описание партнерской программы.

### `field_affiliate_text`

```python
def field_affiliate_text():
    """

    @details
    """
    ...
```

Возвращает текст партнерской программы.

### `field_affiliate_image_large`

```python
def field_affiliate_image_large():
    """

    @details
    """
    ...
```

### `field_affiliate_image_medium`

```python
def field_affiliate_image_medium():
    """

    @details
    """
    ...
```

### `field_affiliate_image_small`

```python
def field_affiliate_image_small():
    """

    @details
    """
    ...
```

Извлекает URL маленького изображения партнерской программы.

### `field_available_date`

```python
def field_available_date():
    """

    @details
    """
    ...
```

Возвращает дату, когда товар станет доступен.

### `field_available_for_order`

```python
def field_available_for_order():
    """ Если вернулся вебэлемент, это флаг, что товара нет в наличии, а вернулся <p>המלאי אזל
    """
    ...
```

Определяет, доступен ли товар для заказа.

### `field_available_later`

```python
def field_available_later():
    """

    @details
    """
    ...
```

Возвращает текст о доступности товара позже.

### `field_available_now`

```python
def field_available_now():
    """

    @details
    """
    ...
```

Возвращает текст о доступности товара сейчас.

### `field_category_ids`

```python
def field_category_ids():
    """

    @details
    """
    ...
```

### `field_category_ids_append`

```python
def field_category_ids_append():
    """

    @details
    """
    ...
```

### `field_cache_default_attribute`

```python
def field_cache_default_attribute():
    """

    @details
    """
    ...
```

### `field_cache_has_attachments`

```python
def field_cache_has_attachments():
    """

    @details
    """
    ...
```

### `field_cache_is_pack`

```python
def field_cache_is_pack():
    """

    @details
    """
    ...
```

### `field_condition`

```python
def field_condition():
    """

    @details
    """
    ...
```

Извлекает условие товара (например, новый, б/у).

### `field_customizable`

```python
def field_customizable():
    """

    @details
    """
    ...
```

Определяет, можно ли настраивать товар.

### `field_date_add`

```python
def field_date_add():
    """

    @details
    """
    ...
```

### `field_date_upd`

```python
def field_date_upd():
    """

    @details
    """
    ...
```

### `field_delivery_out_stock`

```python
def field_delivery_out_stock():
    """
    Заметка о доставке, когда товара нет в наличии
    """
    ...
```

Возвращает заметку о доставке, когда товара нет в наличии.

### `field_depth`

```python
def field_depth():
    """
    @details
    """
    ...
```

Извлекает глубину товара.

### `field_description`

```python
def field_description():
    """ поле полного описания товара
    @details
    """
    ...
```

Извлекает полное описание товара.

### `field_id_category_default`

```python
def field_id_category_default():
    """ Главная категория товара. Берется из сценария """
    ...
```

Возвращает идентификатор главной категории товара, взятый из сценария.

### `field_ean13`

```python
def field_ean13():
    """

    @details
    """
    ...
```

Извлекает EAN13 код товара.

### `field_ecotax`

```python
def field_ecotax():
    """

    @details
    """
    ...
```

### `field_height`

```python
def field_height():
    """

    @details
    """
    ...
```

Извлекает высоту товара.

### `field_how_to_use`

```python
def field_how_to_use():
    """

    @details
    """
    ...
```

Извлекает инструкцию по использованию товара.

### `field_id_default_combination`

```python
def field_id_default_combination():
    """

    @details
    """
    ...
```

### `field_id_default_image`

```python
def field_id_default_image():
    """

    @details
    """
    ...
```

### `field_id_lang`

```python
def field_id_lang():
    """

    @details
    """
    ...
```

### `field_id_manufacturer`

```python
def field_id_manufacturer():
    """ ID бренда. Может быть и названием бренда - престашоп сам разберется """
    ...
```

Извлекает ID производителя товара.

### `field_id_product`

```python
def field_id_product():
    """

    @details
    """
    ...
```

### `field_id_shop_default`

```python
def field_id_shop_default():
    """

    @details
    """
    ...
```

### `field_id_supplier`

```python
def field_id_supplier():
    """

    @details
    """
    ...
```

### `field_id_tax`

```python
def field_id_tax():
    """

    @details
    """
    ...
```

### `field_id_type_redirected`

```python
def field_id_type_redirected():
    """

    @details
    """
    ...
```

### `field_images_urls`

```python
def field_images_urls():
    """
    Вначале я загружу дефолтную картинку
    @details
    """
    ...
```

Извлекает URL дополнительных изображений товара.

### `field_indexed`

```python
def field_indexed():
    """

    @details
    """
    ...
```

### `field_ingredients`

```python
def field_ingredients():
    """ Состав. Забираю с сайта HTML с картинками ингридиентов """
    ...
```

Извлекает состав товара.

### `field_meta_description`

```python
def field_meta_description():
    """

    @details
    """
    ...
```

Извлекает мета-описание товара.

### `field_meta_keywords`

```python
def field_meta_keywords():
    """

    @details
    """
    ...
```

### `field_meta_title`

```python
def field_meta_title():
    """

    @details
    """
    ...
```

### `field_is_virtual`

```python
def field_is_virtual():
    """

    @details
    """
    ...
```

### `field_isbn`

```python
def field_isbn():
    """

    @details
    """
    ...
```

### `field_link_rewrite`

```python
def field_link_rewrite(product_name: str) -> str:
    """ Создается из переменной `product_name` которая содержит значение локатора l["name"] """
    ...
```

Создает `link_rewrite` на основе названия товара.

### `field_location`

```python
def field_location():
    """

    @details
    """
    ...
```

### `field_low_stock_alert`

```python
def field_low_stock_alert():
    """

    @details
    """
    ...
```

### `field_low_stock_threshold`

```python
def field_low_stock_threshold():
    """

    @details
    """
    ...
```

### `field_name`

```python
def field_name(name: str):
    """ Название товара
    Очищаю поля от лишних параметров, которые не проходят в престашоп
    """
    ...
```

Извлекает и нормализует название товара.

### `field_online_only`

```python
def field_online_only():
    """ товар только в интернет магазине

    @details
    """
    ...
```

### `field_on_sale`

```python
def field_on_sale():
    """ Распродажа """
    ...
```

Определяет, находится ли товар на распродаже.

### `field_out_of_stock`

```python
def field_out_of_stock():
    """ Товара нет в наличии """
    ...
```

Определяет, есть ли товар в наличии.

### `field_pack_stock_type`

```python
def field_pack_stock_type():
    """

    @details
    """
    ...
```

### `field_position_in_category`

```python
def field_position_in_category():
    """

    @details
    """
    ...
```

### `field_price`

```python
def field_price():
    """

    @details
    """
    ...
```

Извлекает и нормализует цену товара.

### `field_product_type`

```python
def field_product_type():
    """

    @details
    """
    ...
```

### `field_quantity_discount`

```python
def field_quantity_discount():
    """

    @details
    """
    ...
```

### `field_redirect_type`

```python
def field_redirect_type():
    """

    @details
    """
    ...
```

### `field_reference`

```python
def field_reference():
    """ supplier's SKU """
    ...
```

### `field_show_condition`

```python
def field_show_condition():
    """

    @details
    """
    ...
```

### `field_show_price`

```python
def field_show_price():
    """

    @details
    """
    ...
```

### `field_state`

```python
def field_state():
    """

    @details
    """
    ...
```

### `field_text_fields`

```python
def field_text_fields():
    """

    @details
    """
    ...
```

### `field_unit_price_ratio`

```python
def field_unit_price_ratio():
    """

    @details
    """
    ...
```

### `field_unity`

```python
def field_unity():
    """

    @details
    """
    ...
```

### `field_upc`

```python
def field_upc():
    """

    @details
    """
    ...
```

### `field_uploadable_files`

```python
def field_uploadable_files():
    """

    @details
    """
    ...
```

### `field_default_image_url`

```python
def field_default_image_url():
    """

    @details
    """
    ...
```

### `field_visibility`

```python
def field_visibility():
    """

    @details
    """
    ...
```

Извлекает видимость товара.

### `field_weight`

```python
def field_weight():
    """

    @details
    """
    ...
```

### `field_wholesale_price`

```python
def field_wholesale_price():
    """

    @details
    """
    ...
```

### `field_width`

```python
def field_width():
    """

    @details
    """
    ...
```

### `get_price`

```python
async def get_price(_d, _l) -> str | float:
    """ Привожу денюшку через флаг `format`
    @details к:
    - [ ] float
    - [v] str
    """
    ...
```

Асинхронная функция для извлечения и нормализации цены товара.
Аргументы:
    - `_d`: вебдрайвер
    - `_l`: локатор

### `specification`

```python
def specification():
    #f["product_specification"] = _d.execute_locator(_l["specification_locator"])
    f["product_specification"] = f["description"]
```

### `summary`

```python
def summary():
    f["summary"] = f["description"]
```

### `delivery`

```python
def delivery():
    ...
```

### `link`

```python
def link():
    f["link_to_product"]= _d.current_url.split('?')[0]
```

### `images`

```python
def images():
    ...
```

### `qty`

```python
def qty():
    try:
        _qty = _d.execute_locator(_l["qty_locator"])[0]
        f["qty"] = StringFormatter.clear_price(_qty)
        f["tavit im bemlay"] = f["qty"]
        return True
    except Exception as ex:
        #field["qty"] = None
        logger.error(ex)
        return
```

### `byer_protection`

```python
def byer_protection():
    try:
        f["product_byer_protection"] = str(_d.execute_locator(_l["byer_protection_locator"]))
        return True
    except Exception as ex:
        f["product_byer_protection"] = None
        logger.error(ex)
        return
```

### `customer_reviews`

```python
def customer_reviews():
    try:
        f["product_customer_reviews"] = _d.execute_locator(_l["customer_reviews_locator"])
    except Exception as ex:
        f["product_customer_reviews"] = None
        logger.error(ex)
        return
```

### `rewritted_URL`

```python
def rewritted_URL():
    """
    TODO
    получается длинные
    f["Rewritten URL"] = StringFormatter.rewritted_URL(f["title"])
    """
    f["Rewritten URL"] = f["id"]
```

## Переменные

### `product_fields`

```python
product_fields = grab_product_page (s)
```

### `presta_fields_dict`

```python
presta_fields_dict: Dict = {key: value for key, value in product_fields.presta_fields_dict.items() if value}
```

### `assist_fields_dict`

```python
assist_fields_dict: Dict = product_fields.assist_fields_dict
```