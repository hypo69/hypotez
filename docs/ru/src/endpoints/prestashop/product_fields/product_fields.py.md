# Модуль `product_fields`

## Обзор

Модуль `product_fields` предназначен для работы с полями товаров в PrestaShop. Он предоставляет класс `ProductFields`, который позволяет удобно управлять атрибутами товара, как основными, так и мультиязычными.

## Подробнее

Модуль предоставляет функциональность для работы с полями товаров в PrestaShop.
В классе `ProductFields` реализована логика для загрузки значений полей по умолчанию, установки мультиязычных значений и преобразования объекта в словарь для PrestaShop API.

## Классы

### `ProductFields`

**Описание**: Класс, описывающий поля товара в формате API PrestaShop.

**Атрибуты**:
- `presta_fields` (SimpleNamespace): Объект, хранящий поля товара. Инициализируется в методе `__post_init__`.
- `id_lang` (int): ID языка, используемый по умолчанию для мультиязычных полей.

**Методы**:
- `__post_init__()`: Вызывается после инициализации экземпляра класса.
- `_payload()`: Загружает значения полей товара по умолчанию.
- `_set_multilang_value(field_name: str, value: str, id_lang: Optional[int | str] = 1) -> bool`: Устанавливает мультиязычное значение для заданного поля.
- `id_product`: property `ps_product.id_product: int(10) unsigned`
- `id_supplier`: property `ps_product.id_supplier: int(10) unsigned`
- `id_manufacturer`: property `ps_product.id_manufacturer: int(10) unsigned`
- `id_category_default`: property `ps_product.id_category_default: int(10) unsigned`
- `id_shop_default`: property `ps_product.id_shop_default: int(10) unsigned`
- `id_shop`: property `ps_product.id_shop: int(10) unsigned`
- `id_tax_rules_group`: property `ps_product.id_tax_rules_group: int(11) unsigned`
- `position_in_category`: property `ps_category_product.position: int(10) unsigned`
- `on_sale`: property `ps_product.on_sale: tinyint(1) unsigned`
- `online_only`: property `ps_product.online_only: tinyint(1) unsigned`
- `ean13`: property `ps_product.ean13: varchar(13)`
- `isbn`: property `ps_product.isbn: varchar(32)`
- `upc`: property `ps_product.upc: varchar(12)`
- `mpn`: property `ps_product.mpn: varchar(40)`
- `ecotax`: property `ps_product.ecotax: decimal(17,6)`
- `minimal_quantity`: property `ps_product.minimal_quantity: int(10) unsigned`
- `low_stock_threshold`: property `ps_product.low_stock_threshold: int(10)`
- `low_stock_alert`: property `ps_product.low_stock_alert: tinyint(1)`
- `price`: property `ps_product.price: decimal(20,6)`
- `wholesale_price`: property `ps_product.wholesale_price: decimal(20,6)`
- `unity`: property `ps_product.unity: varchar(255)`
- `unit_price_ratio`: property `ps_product.unit_price_ratio: decimal(20,6)`
- `additional_shipping_cost`: property `ps_product.additional_shipping_cost: decimal(20,6)`
- `reference`: property `ps_product.reference: varchar(64)`
- `supplier_reference`: property `ps_product.supplier_reference: varchar(64)`
- `location`: property `ps_product.location: varchar(255)`
- `width`: property `ps_product.width: decimal(20,6)`
- `height`: property `ps_product.height: decimal(20,6)`
- `depth`: property `ps_product.depth: decimal(20,6)`
- `weight`: property `ps_product.weight: decimal(20,6)`
- `volume`: property `ps_product.volume: varchar(100)`
- `out_of_stock`: property `ps_product.out_of_stock: int(10) unsigned`
- `additional_delivery_times`: property `ps_product.additional_delivery_times: tinyint(1) unsigned`
- `quantity_discount`: property `ps_product.quantity_discount: tinyint(1)`
- `customizable`: property `ps_product.customizable: tinyint(2)`
- `uploadable_files`: property `ps_product.uploadable_files: tinyint(4)`
- `text_fields`: property `ps_product.text_fields: tinyint(4)`
- `active`: property `ps_product.active: tinyint(1) unsigned`
- `redirect_type`: property `ps_product.redirect_type: enum('404','301-product','302-product','301-category','302-category')`
- `id_type_redirected`: property `ps_product.id_type_redirected: int(10) unsigned`
- `available_for_order`: property `ps_product.available_for_order: tinyint(1)`
- `available_date`: property `ps_product.available_date: date`
- `show_condition`: property `ps_product.show_condition: tinyint(1)`
- `condition`: property `ps_product.condition: enum('new','used','refurbished')`
- `show_price`: property `ps_product.show_price: tinyint(1)`
- `indexed`: property `ps_product.indexed: tinyint(1)`
- `visibility`: property `ps_product.visibility: enum('both','catalog','search','none')`
- `cache_is_pack`: property `ps_product.cache_is_pack: tinyint(1)`
- `cache_has_attachments`: property `ps_product.cache_has_attachments: tinyint(1)`
- `is_virtual`: property `ps_product.is_virtual: tinyint(1)`
- `cache_default_attribute`: property `ps_product.cache_default_attribute: int(10) unsigned`
- `date_add`: property `ps_product.date_add: datetime`
- `date_upd`: property `ps_product.date_upd: datetime`
- `advanced_stock_management`: property `ps_product.advanced_stock_management: tinyint(1)`
- `pack_stock_type`: property `ps_product.pack_stock_type: int(11) unsigned`
- `state`: property `ps_product.state: int(11) unsigned`
- `product_type`: property `ps_product.product_type: enum('standard', 'pack', 'virtual', 'combinations', '')`
- `name`: property `ps_product_lang.name: varchar(128)`
- `description`: property `ps_product_lang.description: text`
- `description_short`: property `ps_product_lang.description_short: text`
- `link_rewrite`: property `ps_product_lang.link_rewrite: varchar(128)`
- `meta_description`: property `ps_product_lang.meta_description: varchar(512)`
- `meta_keywords`: property `ps_product_lang.meta_keywords: varchar(255)`
- `meta_title`: property `ps_product_lang.meta_title: varchar(128)`
- `available_now`: property `ps_product_lang.available_now: varchar(255)`
- `available_later`: property `ps_product_lang.available_later: varchar(255)`
- `delivery_in_stock`: property `ps_product_lang.delivery_in_stock: varchar(255)`
- `delivery_out_stock`: property `ps_product_lang.delivery_out_stock: varchar(255)`
- `delivery_additional_message`: property `ps_product_lang.delivery_additional_message: tinytext`
- `affiliate_short_link`: property `ps_product_lang.affiliate_short_link: tinytext`
- `affiliate_text`: property `ps_product_lang.affiliate_text: tinytext`
- `affiliate_summary`: property `ps_product_lang.affiliate_summary: tinytext`
- `affiliate_summary_2`: property `ps_product_lang.affiliate_summary_2: tinytext`
- `affiliate_image_small`: property `ps_product_lang.affiliate_image_small: varchar(512)`
- `affiliate_image_medium`: property `ps_product_lang.affiliate_image_medium: varchar(512)`
- `affiliate_image_large`: property `ps_product_lang.affiliate_image_large: varchar(512)`
- `ingredients`: property `ps_product_lang.ingredients: tinytext`
- `specification`: property `ps_product_lang.specification: tinytext`
- `how_to_use`: property `ps_product_lang.how_to_use: tinytext`
- `id_default_image`: property `ps_product.id_default_image: int(10) unsigned`
- `link_to_video`: property `ps_product.link_to_video: varchar(255)`
- `local_image_path`: property Путь к локальному изображению.
- `local_video_path`: property Путь к локальному видео.
- `additional_categories`:
- `product_images`:
- `images_urls`: property Список URL дополнительных изображений.
- `product_combinations`:
- `product_options`:
- `product_product_features`:
- `product_product_tags`: Возвращает список тегов для поисковиков
- `product_stock_availables`:
- `product_attachments`:
- `product_accessories`:
- `product_bundle`:
- `to_dict() -> Dict[str, Any]`: Преобразует объект `ProductFields` в словарь, пригодный для отправки в PrestaShop API.

#### `__post_init__`

```python
def __post_init__(self):
    """"""
    self._payload()
```

**Назначение**: Метод, вызываемый после инициализации экземпляра класса.

**Как работает функция**:
- Вызывает метод `self._payload()` для загрузки дефолтных значений полей.

#### `_payload`

```python
def _payload(self) -> bool:
    """
    Загрузка дефолтных значений полей.
    Returns:
        bool: True, если загрузка прошла успешно, иначе False.
    """
```

**Назначение**: Метод загружает дефолтные значения полей товара из файлов `fields_list.txt` и `product_fields_default_values.json`.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `bool`: Возвращает `True`, если загрузка прошла успешно, и `False` в случае ошибки.

**Как работает функция**:
1. Формирует путь к файлам `fields_list.txt` и `product_fields_default_values.json`.
2. Считывает список полей из файла `fields_list.txt` с помощью функции `read_text_file`.
3. Если список полей не был загружен, то логирует ошибку и возвращает `False`.
4. Инициализирует атрибут `presta_fields` как `SimpleNamespace` с ключами из списка полей.
5. Загружает словарь с данными из файла `product_fields_default_values.json` с помощью функции `j_loads`.
6. Если словарь не был загружен, логирует отладочное сообщение и возвращает `False`.
7. Перебирает элементы словаря и устанавливает соответствующие атрибуты в `self.presta_fields`.
8. В случае возникновения исключений в процессе загрузки или конвертации данных, логирует ошибки и возвращает `False`.

**Примеры**:
```python
product_fields = ProductFields()
success = product_fields._payload()
print(success)  # Выведет True, если загрузка прошла успешно, иначе False
```

#### `_set_multilang_value`

```python
def _set_multilang_value(self, field_name: str, value: str, id_lang: Optional[int | str] = 1) -> bool:
    """
    Устанавливает мультиязычное значение для заданного поля.

    Args:
        field_name (str): Имя поля (например, 'name', 'description').
        value (str): Значение для установки.
        id_lang (Optional[Union[int, str]]): ID языка. Если не указан, используется self.id_lan.

    Описание:
        Функция устанавливает мультиязычное значение для указанного поля объекта.  
        Поле может хранить значения для разных языков.  Значения хранятся в виде списка словарей,
        где каждый словарь представляет собой значение для определенного языка и имеет структуру:

        {'attrs': {'id': 'language_id'}, 'value': 'language_value'}
         {'id': 'language_id'}, 'value': 'language_value'}

        - 'attrs': Словарь, содержащий атрибуты значения.  В данном случае, обязательным атрибутом является 'id',
                   который представляет собой идентификатор языка.
        - 'value': Значение поля для указанного языка.

        Если поле с указанным именем не существует, оно создается. Если поле существует, но не имеет
        ожидаемой структуры (словарь с ключом 'language', содержащим список), поле перезаписывается.
        Если поле существует и имеет правильную структуру, функция пытается обновить значение для
        указанного языка. Если язык уже существует в списке, его значение обновляется. Если язык
        не существует, добавляется новая запись в список.

    Returns:
        bool: True, если значение успешно установлено, False в случае ошибки.
    """
```

**Назначение**: Устанавливает мультиязычное значение для указанного поля объекта `presta_fields`.

**Параметры**:
- `field_name` (str): Имя поля (например, `'name'`, `'description'`).
- `value` (str): Значение для установки.
- `id_lang` (Optional[int  |  str], optional): ID языка. Если не указан, используется `self.id_lang`. По умолчанию `1`.

**Возвращает**:
- `bool`: Возвращает `True`, если значение успешно установлено, и `False` в случае ошибки.

**Как работает функция**:
1.  Определяет ID языка, используя `self.id_lang`, если `id_lang` не указан.
2.  Экранирует специальные символы в значении, чтобы избежать ошибок при сохранении в базу данных.
3.  Создает словарь `lang_data`, содержащий информацию о языке и значении.
4.  Пытается получить текущее значение поля из `self.presta_fields`.
5.  Если поле не существует, создает новое поле в формате `{'language': [lang_data]}`.
6.  Если поле существует, проверяет его структуру. Если структура неправильная, перезаписывает поле в правильном формате.
7.  Если структура поля правильная, ищет запись для указанного языка в списке.
8.  Если запись для языка найдена, обновляет значение. Если нет, добавляет новую запись в список.
9.  В случае возникновения исключений, логирует ошибку и возвращает `False`.

**Внутренние функции**:
*   `escape_and_strip(text: str) -> str`:
    *   **Назначение**: Очищает и экранирует строку, заменяя символы `\'` и `\"` на `\\\'` и `\\"`, удаляя пробелы в начале и конце.
    *   **Параметры**:
        *   `text` (str): Входная строка для очистки и экранирования.
    *   **Возвращает**:
        *   `str`: Очищенная и экранированная строка.
    *   **Как работает функция**:
        1.  Проверяет, является ли входная строка пустой. Если да, возвращает пустую строку.
        2.  Экранирует символы `\'` и `\"`, заменяет `;` на `<br>`, и удаляет лишние пробелы с помощью регулярного выражения и методов `strip()` и `replace()`.
        3.  Возвращает полученную строку.

**Примеры**:

```python
product_fields = ProductFields()
success = product_fields._set_multilang_value('name', 'Новое название товара', id_lang=2)
print(success)  # Выведет True, если значение успешно установлено, иначе False
```

#### `id_product`

```python
@property
def id_product(self) -> Optional[int]:
    """ property `ps_product.id_product: int(10) unsigned` """
    return self.presta_fields.id_product
```

**Назначение**: Получение значения `id_product` из `presta_fields`.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `Optional[int]`: Значение `id_product` или `None`, если оно не установлено.

#### `id_product.setter`

```python
@id_product.setter
def id_product(self, value: int = None):
    """ setter `ID` товара. Для нового товара id назначается из `PrestaShop`. """
    try:
        self.presta_fields.id_product = value
    except Exception as ex:
        logger.error(f"Ошибка при установке id_product:",ex)
```

**Назначение**: Установка значения `id_product` в `presta_fields`.

**Параметры**:
- `value` (int, optional): Значение для установки. По умолчанию `None`.

**Как работает функция**:
- Пытается установить значение `id_product` в `presta_fields`.
- В случае ошибки логирует ее.

**Примеры**:
```python
product_fields = ProductFields()
product_fields.id_product = 123
print(product_fields.id_product)  # Выведет 123
```

#### `id_supplier`

```python
@property
def id_supplier(self) -> Optional[int]:
    """ property `ps_product.id_supplier: int(10) unsigned` """
    return self.presta_fields.id_supplier
```

**Назначение**: Получение значения `id_supplier` из `presta_fields`.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `Optional[int]`: Значение `id_supplier` или `None`, если оно не установлено.

#### `id_supplier.setter`

```python
@id_supplier.setter
def id_supplier(self, value: int = None):
    """ setter `ID` поставщика."""
    try:
        self.presta_fields.id_supplier = value
    except Exception as ex:
       logger.error(f"Ошибка при установке id_supplier:",ex)
```

**Назначение**: Установка значения `id_supplier` в `presta_fields`.

**Параметры**:
- `value` (int, optional): Значение для установки. По умолчанию `None`.

**Как работает функция**:
- Пытается установить значение `id_supplier` в `presta_fields`.
- В случае ошибки логирует ее.

#### `id_manufacturer`

```python
@property
def id_manufacturer(self) -> Optional[int]:
    """ property `ps_product.id_manufacturer: int(10) unsigned` """
    return self.presta_fields.id_manufacturer
```

**Назначение**: Получение значения `id_manufacturer` из `presta_fields`.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `Optional[int]`: Значение `id_manufacturer` или `None`, если оно не установлено.

#### `id_manufacturer.setter`

```python
@id_manufacturer.setter
def id_manufacturer(self, value: int = None):
    """ setter `ID` бренда."""
    try:
         self.presta_fields.id_manufacturer = value
    except Exception as ex:
         logger.error(f"Ошибка при установке id_manufacturer:",ex)
```

**Назначение**: Установка значения `id_manufacturer` в `presta_fields`.

**Параметры**:
- `value` (int, optional): Значение для установки. По умолчанию `None`.

**Как работает функция**:
- Пытается установить значение `id_manufacturer` в `presta_fields`.
- В случае ошибки логирует ее.

#### `id_category_default`

```python
@property
def id_category_default(self) -> Optional[int]:
    """ property `ps_product.id_category_default: int(10) unsigned` """
    return self.presta_fields.id_category_default
```

**Назначение**: Получение значения `id_category_default` из `presta_fields`.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `Optional[int]`: Значение `id_category_default` или `None`, если оно не установлено.

#### `id_category_default.setter`

```python
@id_category_default.setter
def id_category_default(self, value: int):
    """ setter `ID` главной категории товара."""
    try:
        self.presta_fields.id_category_default = value
    except Exception as ex:
        logger.error(f"Ошибка при установке id_shop_default:",ex)
```

**Назначение**: Установка значения `id_category_default` в `presta_fields`.

**Параметры**:
- `value` (int): Значение для установки.

**Как работает функция**:
- Пытается установить значение `id_category_default` в `presta_fields`.
- В случае ошибки логирует ее.

#### `id_shop_default`

```python
@property
def id_shop_default(self) -> Optional[int]:
    """ property `ps_product.id_shop_default: int(10) unsigned` """
    return self.presta_fields.id_shop_default
```

**Назначение**: Получение значения `id_shop_default` из `presta_fields`.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `Optional[int]`: Значение `id_shop_default` или `None`, если оно не установлено.

#### `id_shop_default.setter`

```python
@id_shop_default.setter
def id_shop_default(self, value: int ):
    """ setter `ID` магазина по умолчанию."""
    try:
        self.presta_fields.id_shop_default = normalize_int(value or 1)
    except Exception as ex:
        logger.error(f"Ошибка при установке id_shop_default:",ex)
```

**Назначение**: Установка значения `id_shop_default` в `presta_fields`.

**Параметры**:
- `value` (int): Значение для установки.

**Как работает функция**:
- Пытается установить значение `id_shop_default` в `presta_fields`, используя функцию `normalize_int` для нормализации значения.
- В случае ошибки логирует ее.

#### `id_shop`

```python
@property
def id_shop(self) -> Optional[int]:
    """ property `ps_product.id_shop: int(10) unsigned` """
    return self.presta_fields.id_shop
```

**Назначение**: Получение значения `id_shop` из `presta_fields`.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `Optional[int]`: Значение `id_shop` или `None`, если оно не установлено.

#### `id_shop.setter`

```python
@id_shop.setter
def id_shop(self, value: int):
    """ setter `ID` магазина (для multishop)."""
    try:
        self.presta_fields.id_shop = normalize_int(value or 1)
    except Exception as ex:
         logger.error(f"Ошибка при установке id_shop:",ex)
```

**Назначение**: Установка значения `id_shop` в `presta_fields`.

**Параметры**:
- `value` (int): Значение для установки.

**Как работает функция**:
- Пытается установить значение `id_shop` в `presta_fields`, используя функцию `normalize_int` для нормализации значения.
- В случае ошибки логирует ее.

#### `id_tax_rules_group`

```python
@property
def id_tax_rules_group (self) -> Optional[int]:
    """ property `ps_product.id_tax_rules_group: int(11) unsigned` """
    return self.presta_fields.id_tax_rules_group 
```

**Назначение**: Получение значения `id_tax_rules_group` из `presta_fields`.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `Optional[int]`: Значение `id_tax_rules_group` или `None`, если оно не установлено.

#### `id_tax_rules_group.setter`

```python
@id_tax_rules_group.setter
def id_tax_rules_group (self, value: int):
     """ setter `ID` налога."""
    
     try:
        self.presta_fields.id_tax_rules_group  = normalize_int(value)
     except Exception as ex:
        logger.error(f"Ошибка при установке id_tax_rules_group:",ex)
```

**Назначение**: Установка значения `id_tax_rules_group` в `presta_fields`.

**Параметры**:
- `value` (int): Значение для установки.

**Как работает функция**:
- Пытается установить значение `id_tax_rules_group` в `presta_fields`, используя функцию `normalize_int` для нормализации значения.
- В случае ошибки логирует ее.

#### `position_in_category`

```python
@property
def position_in_category(self) -> Optional[int]:
     """ property `ps_category_product.position: int(10) unsigned` """
     return self.presta_fields.position_in_category
```

**Назначение**: Получение значения `position_in_category` из `presta_fields`.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `Optional[int]`: Значение `position_in_category` или `None`, если оно не установлено.

#### `position_in_category.setter`

```python
@position_in_category.setter
def position_in_category(self, value:int = None):
    """ setter  Позиция товара в категории."""
    try:
        self.presta_fields.position_in_category = normalize_int(value)
    except Exception as ex:
       logger.error(f'Ошибка при установке `position_in_category` {value} : ',ex)
```

**Назначение**: Установка значения `position_in_category` в `presta_fields`.

**Параметры**:
- `value` (int, optional): Значение для установки. По умолчанию `None`.

**Как работает функция**:
- Пытается установить значение `position_in_category` в `presta_fields`, используя функцию `normalize_int` для нормализации значения.
- В случае ошибки логирует ее.

#### `on_sale`

```python
@property
def on_sale(self) -> int:
    """ property `ps_product.on_sale: tinyint(1) unsigned` """
    return self.presta_fields.on_sale
```

**Назначение**: Получение значения `on_sale` из `presta_fields`.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `int`: Значение `on_sale`.

#### `on_sale.setter`

```python
@on_sale.setter
def on_sale(self, value: int ):
    """ setter Флаг распродажи."""
    self.presta_fields.on_sale = normalize_int(value)
```

**Назначение**: Установка значения `on_sale` в `presta_fields`.

**Параметры**:
- `value` (int): Значение для установки.

**Как работает функция**:
- Устанавливает значение `on_sale` в `presta_fields`, используя функцию `normalize_int` для нормализации значения.

#### `online_only`

```python
@property
def online_only(self) -> int:
    """ property `ps_product.online_only: tinyint(1) unsigned` """
    return self.presta_fields.online_only
```

**Назначение**: Получение значения `online_only` из `presta_fields`.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `int`: Значение `online_only`.

#### `online_only.setter`

```python
@online_only.setter
def online_only(self, value: int|bool ):
    """ setter Флаг "только онлайн". """
    self.presta_fields.online_only = normalize_int(value)
```

**Назначение**: Установка значения `online_only` в `presta_fields`.

**Параметры**:
- `value` (int | bool): Значение для установки.

**Как работает функция**:
- Устанавливает значение `online_only` в `presta_fields`, используя функцию `normalize_int` для нормализации значения.

#### `ean13`

```python
@property
def ean13(self) -> Optional[str]:
    """ property `ps_product.ean13: varchar(13)` """
    return self.presta_fields.ean13
```

**Назначение**: Получение значения `ean13` из `presta_fields`.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `Optional[str]`: Значение `ean13` или `None`, если оно не установлено.

#### `ean13.setter`

```python
@ean13.setter
def ean13(self, value: str):
    """ setter EAN13 код товара."""
    self.presta_fields.ean13 = normalize_string(value)
```

**Назначение**: Установка значения `ean13` в `presta_fields`.

**Параметры**:
- `value` (str): Значение для установки.

**Как работает функция**:
- Устанавливает значение `ean13` в `presta_fields`, используя функцию `normalize_string` для нормализации значения.

#### `isbn`

```python
@property
def isbn(self) -> Optional[str]:
    """ property `ps_product.isbn: varchar(32)` """
    return self.presta_fields.isbn
```

**Назначение**: Получение значения `isbn` из `presta_fields`.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `Optional[str]`: Значение `isbn` или `None`, если оно не установлено.

#### `isbn.setter`

```python
@isbn.setter
def isbn(self, value: str):
    """ setter ISBN код товара."""
    self.presta_fields.isbn = normalize_string(value)
```

**Назначение**: Установка значения `isbn` в `presta_fields`.

**Параметры**:
- `value` (str): Значение для установки.

**Как работает функция**:
- Устанавливает значение `isbn` в `presta_fields`, используя функцию `normalize_string` для нормализации значения.

#### `upc`

```python
@property
def upc(self) -> Optional[str]:
    """ property `ps_product.upc: varchar(12)` """
    return self.presta_fields.upc
```

**Назначение**: Получение значения `upc` из `presta_fields`.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `Optional[str]`: Значение `upc` или `None`, если оно не установлено.

#### `upc.setter`

```python
@upc.setter
def upc(self, value: str):
    """ setter UPC код товара."""
    self.presta_fields.upc = normalize_string(value)
```

**Назначение**: Установка значения `upc` в `presta_fields`.

**Параметры**:
- `value` (str): Значение для установки.

**Как работает функция**:
- Устанавливает значение `upc` в `presta_fields`, используя функцию `normalize_string` для нормализации значения.

#### `mpn`

```python
@property
def mpn(self) -> Optional[str]:
    """ property `ps_product.mpn: varchar(40)` """
    return self.presta_fields.mpn
```

**Назначение**: Получение значения `mpn` из `presta_fields`.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `Optional[str]`: Значение `mpn` или `None`, если оно не установлено.

#### `mpn.setter`

```python
@mpn.setter
def mpn(self, value: str):
    """ setter MPN код товара."""
    self.presta_fields.mpn = normalize_string(value)
```

**Назначение**: Установка значения `mpn` в `presta_fields`.

**Параметры**:
- `value` (str): Значение для установки.

**Как работает функция**:
- Устанавливает значение `mpn` в `presta_fields`, используя функцию `normalize_string` для нормализации значения.

#### `ecotax`

```python
@property
def ecotax(self) -> Optional[float]:
    """ property `ps_product.ecotax: decimal(17,6)` """
    return self.presta_fields