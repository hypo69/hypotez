# Модуль для проверки наполнения полей HB -> product_fields

## Обзор

Данный модуль предназначен для сбора и обработки данных о товарах с сайта поставщика HB (hbdeadsea.co.il) и приведения их к формату, необходимому для добавления или обновления информации о товарах в PrestaShop. Он использует Selenium WebDriver для взаимодействия с веб-страницами, извлечения данных и нормализации полученных значений.

## Подробнее

Модуль выполняет следующие основные задачи:

1.  **Сбор данных**: Извлекает информацию о товарах со страниц категорий и отдельных страниц товаров на сайте HB.
2.  **Нормализация данных**: Приводит полученные значения к стандартному формату, необходимому для полей товаров в PrestaShop.
3.  **Идентификация товаров**: Определяет, является ли товар новым или уже существует в системе, на основе артикула поставщика.
4.  **Добавление/Обновление товаров**: Добавляет новые товары или обновляет информацию о существующих товарах в PrestaShop через API.
5.  **Обработка изображений**: Сохраняет и отправляет изображения товаров на сервер FTP.

Модуль состоит из нескольких функций, каждая из которых отвечает за определенный этап сбора и обработки данных. Основная функция `grab_product_page` координирует работу остальных функций и возвращает объект `ProductFields`, содержащий всю необходимую информацию о товаре.

## Классы

В данном коде используются следующие классы:

### `Supplier`

**Описание**: Класс, представляющий поставщика товаров.

**Атрибуты**:

*   `supplier_prefix` (str): Префикс поставщика (например, 'hb').

### `Product`

**Описание**: Класс, представляющий товар.

**Атрибуты**:

*   `s` (Supplier): Объект класса `Supplier`, представляющий поставщика товара.

### `ProductFields`

**Описание**: Класс, содержащий поля товара, необходимые для добавления или обновления информации о товаре в PrestaShop.

**Атрибуты**:

*   `s` (Supplier): Объект класса `Supplier`, представляющий поставщика товара.

### `Driver`

**Описание**: Класс, представляющий драйвер для управления браузером.

**Методы**:

*   `execute_locator(l: dict)`: Выполняет поиск веб-элемента на странице по заданному локатору.
*   `get_url(url: str)`: Открывает указанный URL в браузере.
*   `wait(seconds: int)`: Ожидает заданное количество секунд.
*   `scroll()`: Прокручивает страницу вниз.

## Функции

### `grab_product_page`

```python
def grab_product_page(supplier: Supplier, async_run: bool = True) -> ProductFields:
    """Собираю со страницы товара значения вебэлементов и привожу их к полям ProductFields

    Args:
        supplier (Supplier): Класс поставщика. Вебдрайвер должен быть установлен на странице товара.
        async_run (bool, optional): Флаг асинхронного запуска. По умолчанию True.

    Returns:
        ProductFields: Объект класса ProductFields, содержащий собранные и нормализованные данные о товаре.
    """
    ...
```

**Назначение**: Собирает со страницы товара значения веб-элементов и преобразует их в поля `ProductFields`.

**Параметры**:

*   `supplier` (Supplier): Класс поставщика. Веб-драйвер должен быть установлен на странице товара.
*   `async_run` (bool, optional): Флаг асинхронного запуска. По умолчанию `True`.

**Возвращает**:

*   `ProductFields`: Объект класса `ProductFields`, содержащий собранные и нормализованные данные о товаре.

**Как работает функция**:

1.  Инициализирует глобальные переменные `s` (Supplier), `p` (Product), `f` (ProductFields), `d` (Driver) и `l` (locator).
2.  Закрывает баннер на странице.
3.  Прокручивает страницу товара, чтобы загрузить все элементы, подгружаемые через AJAX.
4.  Вызывает внутренние функции, специфичные для данного поставщика (`product_reference_and_volume_and_price_for_100`, `set_references`).
5.  Вызывает функции для заполнения различных полей товара (`field_additional_shipping_cost`, `field_affiliate_short_link` и т.д.).
6.  Извлекает URL изображений товара.
7.  Возвращает объект `ProductFields`, содержащий собранные данные.

**Внутренние функции**:

#### `product_reference_and_volume_and_price_for_100`

```python
def product_reference_and_volume_and_price_for_100():
    """Функция вытаскивает 3 поля:
    - volume,
    - supplier_reference,
    - цена за единицу товара
    @todo Реализовать поле `цена за единицу товара`
    """
    ...
```

**Назначение**: Извлекает объем, артикул поставщика и цену за единицу товара из веб-элементов на странице товара.

**Как работает функция**:

1.  Извлекает список веб-элементов, содержащих информацию об объеме, артикуле поставщика и цене за единицу товара.
2.  Перебирает веб-элементы и извлекает соответствующие значения на основе анализа текста веб-элемента.
3.  Присваивает извлеченные значения полям объекта `f` (ProductFields).

#### `set_references`

```python
def set_references(f: ProductFields, s: Supplier):
    """все, что касается id товара"""
    ...
```

**Назначение**: Устанавливает значения полей, связанных с идентификацией товара.

**Параметры**:

*   `f` (ProductFields): Объект класса `ProductFields`, в который необходимо установить значения полей.
*   `s` (Supplier): Объект класса `Supplier`, содержащий информацию о поставщике.

**Как работает функция**:

1.  Устанавливает `id_supplier` равным `s.supplier_id`.
2.  Формирует значение поля `reference` как комбинацию `s.supplier_id` и `f.supplier_reference`.

### `field_additional_shipping_cost`

```python
def field_additional_shipping_cost():
    """
    стоимость доставки
    @details
    """
    ...
```

**Назначение**: Извлекает стоимость доставки товара.

**Возвращает**:

*   Стоимость доставки, извлеченная из веб-элемента.

### `field_delivery_in_stock`

```python
def field_delivery_in_stock():
    """
    Доставка, когда товар в наличии
    @details
    """
    ...
```

**Назначение**: Извлекает информацию о доставке, когда товар в наличии.

**Возвращает**:

*   Текст, содержащий информацию о доставке, когда товар в наличии.

### `field_active`

```python
def field_active():
    """

    @details
    """
    ...
```

**Назначение**: Определяет, активен ли товар.

**Возвращает**:

*   Значение поля `f.active`.

### `field_additional_delivery_times`

```python
def field_additional_delivery_times():
    """

    @details
    """
    ...
```

**Назначение**: Извлекает информацию о дополнительном времени доставки.

**Возвращает**:

*   Информация о дополнительном времени доставки, извлеченная из веб-элемента.

### `field_advanced_stock_management`

```python
def field_advanced_stock_management():
    """

    @details
    """
    ...
```

**Назначение**: Возвращает значение расширенного управления запасами.

**Возвращает**:

*   Значение поля `f.advanced_stock_management`.

### `field_affiliate_short_link`

```python
def field_affiliate_short_link():
    """

    @details
    """
    ...
```

**Назначение**: Получает текущий URL страницы.

**Возвращает**:

*   Текущий URL страницы.

### `field_affiliate_summary`

```python
def field_affiliate_summary():
    """

    @details
    """
    ...
```

**Назначение**: Возвращает сводку об аффилиате.

**Возвращает**:

*   Значение поля `f.affiliate_summary`.

### `field_affiliate_summary_2`

```python
def field_affiliate_summary_2():
    """

    @details
    """
    ...
```

**Назначение**: Возвращает дополнительную сводку об аффилиате.

**Возвращает**:

*   Значение поля `f.affiliate_summary_2`.

### `field_affiliate_text`

```python
def field_affiliate_text():
    """

    @details
    """
    ...
```

**Назначение**: Возвращает текст аффилиата.

**Возвращает**:

*   Значение поля `f.affiliate_text`.

### `field_affiliate_image_large`

```python
def field_affiliate_image_large():
    """

    @details
    """
    ...
```

**Назначение**:  Не реализовано, возвращает значение `f.affiliate_image_large`.

### `field_affiliate_image_medium`

```python
def field_affiliate_image_medium():
    """

    @details
    """
    ...
```

**Назначение**: Не реализовано, возвращает значение `f.affiliate_image_medium`.

### `field_affiliate_image_small`

```python
def field_affiliate_image_small():
    """

    @details
    """
    ...
```

**Назначение**: Извлекает URL маленького изображения аффилиата.

**Возвращает**:

*   URL маленького изображения аффилиата.

### `field_available_date`

```python
def field_available_date():
    """

    @details
    """
    ...
```

**Назначение**: Возвращает дату доступности товара.

**Возвращает**:

*   Значение поля `f.available_date`.

### `field_available_for_order`

```python
def field_available_for_order():
    """Если вернулся вебэлемент, это флаг, что товара нет в наличии, а вернулся <p>המלאי אזל
    """
    ...
```

**Назначение**: Определяет, доступен ли товар для заказа.

**Как работает функция**:

1.  Пытается извлечь веб-элемент, указывающий на доступность товара для заказа.
2.  Если веб-элемент не найден, устанавливает `f.available_for_order` в 1 (товар доступен) и `f.active` в 1 (товар активен).
3.  Если веб-элемент найден, устанавливает `f.available_for_order` в 0 (товар не доступен) и `f.active` в 0 (товар не активен).

### `field_available_later`

```python
def field_available_later():
    """

    @details
    """
    ...
```

**Назначение**: Возвращает текст "Доступно позже".

**Возвращает**:

*   Значение поля `f.available_later`.

### `field_available_now`

```python
def field_available_now():
    """

    @details
    """
    ...
```

**Назначение**: Возвращает текст "Доступно сейчас".

**Возвращает**:

*   Значение поля `f.available_now`.

### `field_category_ids`

```python
def field_category_ids():
	"""  
	
	@details
	"""
	return f.category_ids
	...
```

**Назначение**: Не реализовано, возвращает значение `f.category_ids`.

### `field_category_ids_append`

```python
def field_category_ids_append():
	"""  
	
	@details
	"""
	#return f.category_ids_append
	...
```

**Назначение**: Не реализовано, возвращает значение `f.category_ids_append`.

### `field_cache_default_attribute`

```python
def field_cache_default_attribute():
    """

    @details
    """
    ...
```

**Назначение**: Возвращает атрибут кэша по умолчанию.

**Возвращает**:

*   Значение поля `f.cache_default_attribute`.

### `field_cache_has_attachments`

```python
def field_cache_has_attachments():
    """

    @details
    """
    ...
```

**Назначение**: Возвращает значение, указывающее, есть ли в кэше вложения.

**Возвращает**:

*   Значение поля `f.cache_has_attachments`.

### `field_cache_is_pack`

```python
def field_cache_is_pack():
	"""  
	
	@details
	"""
	return f.cache_is_pack
	...
```

**Назначение**: Не реализовано, возвращает значение `f.cache_is_pack`.

### `field_condition`

```python
def field_condition():
	"""  
	
	@details
	"""
	return d.execute_locator(l.condition)
        
```

**Назначение**: Не реализовано, возвращает состояние товара.

### `field_customizable`

```python
def field_customizable():
	"""  
	
	@details
	"""
	return f.customizable
	...
```

**Назначение**: Не реализовано, возвращает значение `f.customizable`.

### `field_date_add`

```python
def field_date_add():
	"""  
	
	@details
	"""
	return f.date_add
	...
	
```

**Назначение**: Не реализовано, возвращает дату добавления товара.

### `field_date_upd`

```python
def field_date_upd():
	"""  
	
	@details
	"""
	return f.date_upd
	...
	
```

**Назначение**: Не реализовано, возвращает дату обновления товара.

### `field_delivery_out_stock`

```python
def field_delivery_out_stock():
	"""  
	 Заметка о доставке, когда товара нет в наличии
	"""
	return f.delivery_out_stock
	...
	
```

**Назначение**: Не реализовано, возвращает заметку о доставке, когда товара нет в наличии.

### `field_depth`

```python
def field_depth():
	"""  
	@details
	"""
	return d.execute_locator ( l ["depth"] )
	...
	
```

**Назначение**: Не реализовано, возвращает глубину товара.

### `field_description`

```python
def field_description():
	"""  поле полного описания товара 
	@details
	"""
	return d.execute_locator (l["description"] )[0].text
	...
```

**Назначение**: Не реализовано, возвращает описание товара.

### `field_id_category_default`

```python
def field_id_category_default():
	"""  Главная категория товара. Берется из сценария	"""
	return s.current_scenario["presta_categories"]["default_category"]
	...
	
```

**Назначение**: Не реализовано, возвращает ID главной категории товара.

### `field_ean13`

```python
def field_ean13():
	"""  
	
	@details
	"""
	return d.execute_locator ( l ["ean13"] )
	...
```

**Назначение**: Не реализовано, возвращает код EAN13.

### `field_ecotax`

```python
def field_ecotax():
	"""  
	
	@details
	"""
	return f.ecotax
	...
	
        	
                
```

**Назначение**: Не реализовано, возвращает ecotax.

### `field_height`

```python
def field_height():
	"""  
	
	@details
	"""
	return d.execute_locator ( l ["height"] )
	...
	
```

**Назначение**: Не реализовано, возвращает высоту товара.

### `field_how_to_use`

```python
def field_how_to_use():
	"""  
	
	@details
	"""
	return d.execute_locator ( l ["how_to_use"] ) [0].text
	...
	
                	
```

**Назначение**: Не реализовано, возвращает инструкцию как использовать товар.

### `field_id_default_combination`

```python
def field_id_default_combination():
	"""  
	
	@details
	"""
	return f.id_default_combination
	...
	
```

**Назначение**: Не реализовано, возвращает ID комбинации по умолчанию.

### `field_id_default_image`

```python
def field_id_default_image():
	"""  
	
	@details
	"""
	return f.id_default_image
	...
	
```

**Назначение**: Не реализовано, возвращает ID картинки по умолчанию.

### `field_id_lang`

```python
def field_id_lang():
	"""  
	
	@details
	"""
	return f.id_lang
	...
	
```

**Назначение**: Не реализовано, возвращает ID языка.

### `field_id_manufacturer`

```python
def field_id_manufacturer():
	"""  ID бренда. Может быть и названием бренда - престашоп сам разберется """
	
	return d.execute_locator(l["id_manufacturer"])
	...
	
```

**Назначение**: Не реализовано, возвращает ID производителя.

### `field_id_product`

```python
def field_id_product():
	"""  
	
	@details
	"""
	return f.id_product
	...
```

**Назначение**: Не реализовано, возвращает ID продукта.

### `field_id_shop_default`

```python
def field_id_shop_default():
	"""  
	
	@details
	"""
	return f.id_shop_default
	...
```

**Назначение**: Не реализовано, возвращает ID магазина по умолчанию.

### `field_id_supplier`

```python
def field_id_supplier():
	"""  
	
	@details
	"""
	return d.execute_locator(l["id_supplier"])
	...
	
```

**Назначение**: Не реализовано, возвращает ID поставщика.

### `field_id_tax`

```python
def field_id_tax():
	"""  
	
	@details
	"""
	return f.id_tax
	...
	
```

**Назначение**: Не реализовано, возвращает ID налога.

### `field_id_type_redirected`

```python
def field_id_type_redirected():
	"""  
	
	@details
	"""
	return f.id_type_redirected
	...
```

**Назначение**: Не реализовано, возвращает ID типа редиректа.

### `field_images_urls`

```python
def field_images_urls():
	"""  
	 Вначале я загружу дефолтную картинку
	@details
	"""
	return d.execute_locator(l["additional_images_urls"])
	...
	
```

**Назначение**: Не реализовано, возвращает список URL дополнительных картинок.

### `field_indexed`

```python
def field_indexed():
	"""  
	
	@details
	"""
	return f.indexed
	...
	
        
```

**Назначение**: Не реализовано, возвращает проиндексирован ли продукт.

### `field_ingredients`

```python
def field_ingredients():
	"""  Состав. Забираю с сайта HTML с картинками ингридиентов """
	
	return d.execute_locator ( l["ingredients"] )[0].text
	...
	
```

**Назначение**: Не реализовано, возвращает список ингридиентов.

### `field_meta_description`

```python
def field_meta_description():
	"""  
	
	@details
	"""
	d.execute_locator ( l[\'meta_description\'] )
	...
	
```

**Назначение**: Не реализовано, возвращает мета описание.

### `field_meta_keywords`

```python
def field_meta_keywords():
	"""  
	
	@details
	"""
	return d.execute_locator ( l[\'meta_keywords\'] )
	...
	
        
```

**Назначение**: Не реализовано, возвращает мета ключевые слова.

### `field_meta_title`

```python
def field_meta_title():
	"""  
	
	@details
	"""
	return d.execute_locator ( l[\'meta_title\'] )
	...
	
```

**Назначение**: Не реализовано, возвращает мета заголовок.

### `field_is_virtual`

```python
def field_is_virtual():
	"""  
	
	@details
	"""
	return f.is_virtual
	...
```

**Назначение**: Не реализовано, возвращает виртуальный ли продукт.

### `field_isbn`

```python
def field_isbn():
	"""  
	
	@details
	"""
	return f.isbn
	...
	
```

**Назначение**: Не реализовано, возвращает ISBN.

### `field_link_rewrite`

```python
def field_link_rewrite(product_name: str) -> str:
	"""  Создается из переменной `product_name` которая содержит значение локатора l["name"] 	"""	
	return StringNormalizer.normalize_link_rewrite ( product_name )
	...
	
```

**Назначение**: Не реализовано, генерирует ссылку перезаписи.

### `field_location`

```python
def field_location():
	"""  
	
	@details
	"""
	return f.location
	...
	
```

**Назначение**: Не реализовано, возвращает местоположение.

### `field_low_stock_alert`

```python
def field_low_stock_alert():
	"""  
	
	@details
	"""
	return f.low_stock_alert
	...
	
    
```

**Назначение**: Не реализовано, возвращает оповещение о низком стоке.

### `field_low_stock_threshold`

```python
def field_low_stock_threshold():
	"""  
	
	@details
	"""
	return f.low_stock_threshold
	...
	
```

**Назначение**: Не реализовано, возвращает порог низкого стока.

### `field_minimal_quantity`

```python
def field_minimal_quantity():
	"""  
	
	@details
	"""
	return f.minimal_quantity
	...
```

**Назначение**: Не реализовано, возвращает минимальное количество.

### `field_mpn`

```python
def field_mpn():
	"""  
	
	@details
	"""
	return f.mpn
	...
	
```

**Назначение**: Не реализовано, возвращает MPN.

### `field_name`

```python
def field_name(name: str):
	"""  Название товара 
	Очищаю поля от лишних параметров, которые не проходят в престашоп 
	"""
	return StringNormalizer.normalize_product_name(name)
	...
```

**Назначение**: Не реализовано, возвращает название товара.

### `field_online_only`

```python
def field_online_only():
	""" 	товар только в интернет магазине
	
	@details
	"""
	return d.execute_locator ( l[\'online_only\'] )
	...
	
```

**Назначение**: Не реализовано, возвращает продукт только в онлайн магазине.

### `field_on_sale`

```python
def field_on_sale():
	""" 	Распродажа	"""
	return d.execute_locator ( l[\'on_sale\'] )
	...
	
```

**Назначение**: Не реализовано, возвращает находится ли продукт на распродаже.

### `field_out_of_stock`

```python
def field_out_of_stock():
	"""  Товара нет в наличии """
	return d.execute_locator ( l["out_of_stock"]) 
	...
	
```

**Назначение**: Не реализовано, возвращает находится ли продукт в стоке.

### `field_pack_stock_type`

```python
def field_pack_stock_type():
	"""  
	
	@details
	"""
	return f.pack_stock_type
	...
	
```

**Назначение**: Не реализовано, возвращает тип стока пака.

### `field_position_in_category`

```python
def field_position_in_category():
	"""  
	
	@details
	"""
	return f.position_in_category
	...
	
```

**Назначение**: Не реализовано, возвращает позицию в категории.

### `field_price`

```python
def field_price():
	"""  
	
	@details
	"""
	return StringNormalizer.normalize_price (d.execute_locator (l["price"])[0] ) 
	
	
```

**Назначение**: Не реализовано, возвращает цену товара.

### `field_product_type`

```python
def field_product_type():
	"""  
	
	@details
	"""
	return f.product_type
	...
	
```

**Назначение**: Не реализовано, возвращает тип продукта.

### `field_quantity_discount`

```python
def field_quantity_discount():
	"""  
	
	@details
	"""
	return f.quantity_discount
	...
	
```

**Назначение**: Не реализовано, возвращает скидку на количество.

### `field_redirect_type`

```python
def field_redirect_type():
	"""  
	
	@details
	"""
	return f.redirect_type
	...
	
```

**Назначение**: Не реализовано, возвращает тип редиректа.

### `field_reference`

```python
def field_reference():
	"""  supplier's SKU """
	return f\'{s.supplier_id}-{f.supplier_reference}\' 
	...
	
```

**Назначение**: Не реализовано, возвращает SKU поставщика.

### `field_show_condition`

```python
def field_show_condition():
	"""  
	
	@details
	"""
	return f.show_condition
	
```

**Назначение**: Не реализовано, возвращает показівать ли условия.

### `field_show_price`

```python
def field_show_price():
	"""  
	
	@details
	"""
	return f.show_price
	...
```

**Назначение**: Не реализовано, возвращает показівать ли цену.

### `field_state`

```python
def field_state():
	"""  
	
	@details
	"""
	return f.state
	...
```

**Назначение**: Не реализовано, возвращает состояние.

### `field_text_fields`

```python
def field_text_fields():
	"""  
	
	@details
	"""
	return f.text_fields
	...
	
```

**Назначение**: Не реализовано, возвращает текстовые поля.

### `field_unit_price_ratio`

```python
def field_unit_price_ratio():
	"""  
	
	@details
	"""
	return f.unit_price_ratio
	...
	
```

**Назначение**: Не реализовано, возвращает соотнешение цены за еденицу.

### `field_unity`

```python
def field_unity():
	"""  
	
	@details
	"""
	return f.unity
	...
	
        
```

**Назначение**: Не реализовано, возвращает единство.

### `field_upc`

```python
def field_upc():
	"""  
	
	@details
	"""
	return f.upc
	...
	
```

**Назначение**: Не реализовано, возвращает UPC.

### `field_uploadable_files`

```python
def field_uploadable_files():
	"""  
	
	@details
	"""
	return f.uploadable_files
	...
	
```

**Назначение**: Не реализовано, возвращает список файлов для загрузки.

### `field_default_image_url`

```python
def field_default_image_url():
	"""  
	
	@details
	"""
	return f.default_image_url
	...
        
```

**Назначение**: Не реализовано, возвращает URL картинки по умолчанию.

### `field_visibility`

```python
def field_visibility():
	"""  
	
	@details
	"""
	return d.execute_locator(l["visibility"])
	...
	
```

**Назначение**: Не реализовано, возвращает видимость.

### `field_weight`

```python
def field_weight():
	"""  
	
	@details
	"""
	return f.weight
	...
	
```

**Назначение**: Не реализовано, возвращает вес.

### `field_wholesale_price`

```python
def field_wholesale_price():
	"""  
	
	@details
	"""
	return f.wholesale_price
	...
	
```

**Назначение**: Не реализовано, возвращает оптовую цену.

### `field_width`

```python
def field_width():
	"""  
	
	@details
	"""
	return f.width
	...
	
        
                
```

**Назначение**: Не реализовано, возвращает ширину.

### `get_price`

```python
async def get_price(_d: Driver, _l: dict) -> str | float:
    """Привожу денюшку через флаг `format`
    @details к:
    - [ ] float
    - [v] str
    """
    ...
```

**Назначение**: Приводит цену к нужному формату.

**Параметры**:

*   `_d` (Driver): Драйвер.
*   `_l` (dict): Локаторы.

**Возвращает**:

*   `str | float`: Преобразованная цена.

**Как работает функция**:

1.  Извлекает цену с помощью локатора `_l["price"]["new"]`.
2.  Разделяет строку цены по символу новой строки (`\n`) и берет первую часть.
3.  Нормализует цену с помощью `StringNormalizer.normalize_price`.
4.  В случае ошибки логирует исключение и возвращает `None`.

### `specification`

```python
def specification():
    #f["product_specification"] = _d.execute_locator(_l["specification_locator"])
    f["product_specification"] = f["description"]
def summary():
    f["summary"] = f["description"]
def delivery():

    #__ = _l["dynamic_shipping_block"]
    #_d.execute_locator(__l["product_shippihg_locator_button"])
    #\'\'\' Открываю панель способов доставки \'\'\'
    #shipping_price = _d.execute_locator(__l["dynamic_shipping_titleLayout"])
    #dynamic_shipping_estimated = _d.execute_locator(__l["dynamic_shipping_estimated"])
    #dynamic_tracking_available = _d.execute_locator(__l["dynamic_tracking_available"])
    #close = _d.execute_locator(__l["close"])

    shipping_price = _d.execute_locator(_l["shipping_price_locator"])
    if \'Free Shipping\' in shipping_price:\n        f["shipping price"] = 0\n        return True\n    f["shipping price"] = StringFormatter.clear_price(shipping_price)\n    return True
def link():
    f["link_to_product"]= _d.current_url.split(\'?\')[0]\n

```

**Назначение**: Не реализовано, содержит код для извлечения спецификации продукта.

### `images`

```python
def images():

    _http_server = f\'\'\'http://davidka.esy.es/supplier_imgs/{s.supplier_prefix}\'\'\'
    _img_name = f\'\'\'{f["sku"]}.png\'\'\'
    f["img url"] =f\'\'\'{_http_server}/{_img_name}\'\'\'
    screenshot = _d.execute_locator(_l["main_image_locator"])
    s.save_and_send_viaftp({_img_name:screenshot})

```

**Назначение**: Не реализовано, содержит код для обработки картинок.

### `qty`

```python
def qty():
    try:
        _qty = _d.execute_locator(_l["qty_locator"])[0]
        f["qty"] = StringFormatter.clear_price(_qty)\n        f["tavit im bemlay"] = f["qty"]\n        return True\n    except Exception as ex: \n        #field["qty"] = None\n        logger.error(ex)\n        return

```

**Назначение**: Не реализовано, содержит код для получения количества.

### `byer_protection`

```python
def byer_protection():
    try:
        f["product_byer_protection"] = str(_d.execute_locator(_l["byer_protection_locator"]))\n        return True\n    except Exception as ex: \n        f["product_byer_protection"] = None\n        logger.error(ex)\n        return

```

**Назначение**: Не реализовано