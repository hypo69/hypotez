# Модуль `product_fields`

## Обзор

Модуль `product_fields` предназначен для работы с полями товаров в PrestaShop. Он предоставляет класс `ProductFields`, который позволяет удобно управлять атрибутами товара, как основными, так и мультиязычными.

## Подробней

Этот модуль предназначен для упрощения взаимодействия с API PrestaShop при управлении полями товаров. Он содержит класс `ProductFields`, который инкапсулирует логику установки и получения значений различных полей товара, включая мультиязычные поля.

## Классы

### `ProductFields`

**Описание**: Класс, описывающий поля товара в формате API PrestaShop.

**Атрибуты**:

-   `presta_fields` (SimpleNamespace): Объект, содержащий поля товара. Инициализируется в методе `_payload` значениями из файлов `fields_list.txt` и `product_fields_default_values.json`.
-   `id_lang` (int): ID языка, используемый по умолчанию для мультиязычных полей. По умолчанию равен 1.

**Методы**:

-   `__post_init__()`: Вызывается после инициализации экземпляра класса. Вызывает метод `_payload()` для загрузки дефолтных значений полей.
-   `_payload()`: Загружает дефолтные значения полей товара из файлов `fields_list.txt` и `product_fields_default_values.json`.
-   `_set_multilang_value()`: Устанавливает мультиязычное значение для заданного поля.
-   `to_dict()`: Преобразует объект `ProductFields` в словарь, пригодный для отправки в API PrestaShop.
-   `_format_multilang_value()`: Форматирует мультиязычные значения в список словарей для PrestaShop API.
-   `_ensure_associations()`: Убеждается, что структура `associations` существует в `presta_fields`.
-   `additional_category_append()`: Добавляет связь с категорией, если ее еще нет.
-   `additional_categories_clear()`: Очищает все связи с категориями.
-   `product_image_append()`: Добавляет связь с изображением.
-   `product_images_clear()`: Очищает все связи с изображениями.
-   `images_urls_append()`: Устанавливает список URL, откуда скачать дополнительные изображения.
-   `product_combination_append()`: Добавляет связь с комбинацией.
-   `product_combinations_clear()`: Очищает все связи с комбинациями.
-   `product_options_append()`: Добавляет связь со значением опции продукта.
-   `product_options_clear()`: Очищает все связи со значениями опций продукта.
-   `product_features_append()`: Добавляет связь с характеристикой продукта.
-   `product_features_clear()`: Очищает все связи с характеристиками продукта.
-   `product_tag_append()`: Добавляет связь с тегом.
-   `product_tags_clear()`: Очищает все связи с тегами.
-   `product_stock_available_append()`: Добавляет связь с доступностью на складе.
-   `product_stock_availables_clear()`: Очищает все связи с доступностью на складе.
-   `product_attachment_append()`: Добавляет связь с вложением.
-   `product_attachments_clear()`: Очищает все связи с вложениями.
-   `product_accessory_append()`: Добавляет связь с аксессуаром.
-   `product_accessories_clear()`: Очищает все связи с аксессуарами.
-   `product_bundle_append()`: Добавляет связь с бандлом продукта.
-   `product_bundle_clear()`: Очищает все связи с бандлами продуктов.

### `EnumRedirect`

**Описание**: Перечисление для типов редиректов.

**Элементы**:

-   `ERROR_404`
-   `REDIRECT_301_PRODUCT`
-   `REDIRECT_302_PRODUCT`
-   `REDIRECT_301_CATEGORY`
-   `REDIRECT_302_CATEGORY`

### `EnumCondition`

**Описание**: Перечисление для состояний товара.

**Элементы**:

-   `NEW`
-   `USED`
-   `REFURBISHED`

### `EnumVisibity`

**Описание**: Перечисление для видимости товара.

**Элементы**:

-   `BOTH`
-   `CATALOG`
-   `SEARCH`
-   `NONE`

### `EnumProductType`

**Описание**: Перечисление для типов товаров.

**Элементы**:

-   `STANDARD`
-   `PACK`
-   `VIRTUAL`
-   `COMBINATIONS`
-   `EMPTY`

## Функции

### `__post_init__`

```python
def __post_init__(self):
    """"""
    self._payload()
```

**Назначение**: Метод, вызываемый после инициализации экземпляра класса.

**Как работает функция**:

-   Вызывает метод `_payload()`, который загружает дефолтные значения полей товара.

**Примеры**:

```python
product_fields = ProductFields()
```

### `_payload`

```python
def _payload(self) -> bool:
    """
    Загрузка дефолтных значений полей.
    Returns:
        bool: True, если загрузка прошла успешно, иначе False.
    """
    ...
```

**Назначение**: Загружает дефолтные значения полей товара из файлов `fields_list.txt` и `product_fields_default_values.json`.

**Параметры**:

-   Нет

**Возвращает**:

-   `bool`: `True`, если загрузка прошла успешно, `False` в случае ошибки.

**Как работает функция**:

1.  Определяет базовый путь к файлам конфигурации.
2.  Считывает список полей из файла `fields_list.txt`.
3.  Создает объект `SimpleNamespace` с атрибутами, соответствующими полям товара, и инициализирует их значениями `None`.
4.  Загружает значения по умолчанию из файла `product_fields_default_values.json`.
5.  Устанавливает значения атрибутов `self.presta_fields` на основе загруженных данных.
6.  В случае возникновения исключений логирует ошибки и возвращает `False`.

**Примеры**:

```python
product_fields = ProductFields()
result = product_fields._payload()
print(result)  # Выведет True или False в зависимости от успешности загрузки
```

### `_set_multilang_value`

```python
def _set_multilang_value(self, field_name: str, value: str, id_lang: Optional[int | str] = None) -> bool:
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
    ...
```

**Назначение**: Устанавливает мультиязычное значение для заданного поля.

**Параметры**:

-   `field_name` (str): Имя поля (например, `'name'`, `'description'`).
-   `value` (str): Значение для установки.
-   `id_lang` (Optional[int | str], optional): ID языка. Если не указан, используется `self.id_lang`. По умолчанию `None`.

**Возвращает**:

-   `bool`: `True`, если значение успешно установлено, `False` в случае ошибки.

**Как работает функция**:

1.  Определяет ID языка, используя переданный `id_lang` или значение по умолчанию `self.id_lang`.
2.  Формирует структуру данных для хранения значения языка.
3.  Проверяет, существует ли поле `field_name` в `self.presta_fields`.
4.  Если поле не существует, создает его и устанавливает значение для указанного языка.
5.  Если поле существует, проверяет его структуру. Если структура не соответствует ожидаемой, поле перезаписывается.
6.  Если поле существует и имеет правильную структуру, пытается обновить значение для указанного языка. Если язык уже существует в списке, его значение обновляется. Если язык не существует, добавляется новая запись в список.
7.  В случае возникновения исключений логирует ошибки и возвращает `False`.

**Внутренние функции**:

### `escape_and_strip`

```python
def escape_and_strip(text: str) -> str:
    """
    Очищает и экранирует строку, заменяя символы "\'" и \'"\' на "\\\'" и \'\\"\',
    удаляя пробелы в начале и конце.
    """
    ...
```

**Назначение**: Очищает и экранирует строку, заменяя символы `\'` и `\"` на `\\\'` и `\\"`, удаляя пробелы в начале и конце.

**Параметры**:

-   `text` (str): Строка для обработки.

**Возвращает**:

-   `str`: Очищенная и экранированная строка.

**Как работает функция**:

1.  Проверяет, является ли входной текст пустым. Если да, возвращает пустую строку.
2.  Экранирует символы `'` и `"` с помощью обратного слеша.
3.  Заменяет символы `;` на `<br>`.
4.  Удаляет пробелы в начале и конце строки.

**Примеры**:

```python
product_fields = ProductFields()
result = product_fields._set_multilang_value('name', 'Example Product', id_lang=2)
print(result)  # Выведет True или False в зависимости от успешности установки
```

### `to_dict`

```python
def to_dict(self) -> Dict[str, Any]:
    """
    Преобразует объект ProductFields в словарь для PrestaShop API,
    исключая ключи, значения которых равны None или пустой строке,
    и формирует мультиязычные поля в нужном формате. Все поля должны быть представлены как строки.

    Returns:
        Dict[str, Any]: Словарь с полями, готовый для PrestaShop API.
    """
    ...
```

**Назначение**: Преобразует объект `ProductFields` в словарь для PrestaShop API.

**Параметры**:

-   Нет

**Возвращает**:

-   `Dict[str, Any]`: Словарь с полями, готовый для PrestaShop API.

**Как работает функция**:

1.  Создает пустой словарь `product_dict`.
2.  Проходит по всем атрибутам объекта `ProductFields` и добавляет их в словарь, если они не равны `None` и не являются пустой строкой.
3.  Для мультиязычных полей вызывает метод `_format_multilang_value()` для форматирования значений.
4.  Формирует словарь `associations_dict` с ассоциациями (категории, изображения и т.д.).
5.  Добавляет словарь `associations_dict` в `product_dict`, если он не пустой.
6.  Возвращает словарь `product_dict`.

**Внутренние функции**:

### `str_val`

```python
def str_val(value: Any) -> Optional[str]:
    """Helper function to convert values to strings, handling None."""
    return str(value) if value is not None else None
```

**Назначение**: Вспомогательная функция для преобразования значений в строки, обрабатывающая `None`.

**Параметры**:

-   `value` (Any): Значение для преобразования.

**Возвращает**:

-   `Optional[str]`: Строковое представление значения или `None`, если значение равно `None`.

**Как работает функция**:

1.  Проверяет, является ли входное значение `None`.
2.  Если значение не `None`, преобразует его в строку с помощью `str(value)`.
3.  Если значение `None`, возвращает `None`.

**Примеры**:

```python
product_fields = ProductFields()
product_fields.name = 'Example Product'
product_fields.price = 19.99
product_dict = product_fields.to_dict()
print(product_dict)
```

### `_format_multilang_value`

```python
def _format_multilang_value(self, data: Any) -> List[Dict[str, str]]:
    """
    Форматирует мультиязычные значения в список словарей для PrestaShop API. Все значения представляются как строки.

    Args:
        data (Any): Значение поля. Если это словарь, ожидается структура {'language': [{'attrs': {'id': lang_id}, 'value': value}]}

    Returns:
        List[Dict[str, str]]: Список словарей, где каждый словарь содержит 'id' и 'value' (все как строки) для каждого языка.
    """
    ...
```

**Назначение**: Форматирует мультиязычные значения в список словарей для PrestaShop API.

**Параметры**:

-   `data` (Any): Значение поля.

**Возвращает**:

-   `List[Dict[str, str]]`: Список словарей, где каждый словарь содержит `'id'` и `'value'` для каждого языка.

**Как работает функция**:

Функция возвращает исходные данные `data` без изменений. <инструкция для модели gemini:Возможно, требуется доработка этой функции для правильного форматирования мультиязычных значений.>

**Примеры**:

```python
product_fields = ProductFields()
product_fields.name = {'language': [{'attrs': {'id': 1}, 'value': 'Example Product'}]}
formatted_name = product_fields._format_multilang_value(product_fields.name)
print(formatted_name)
```

## Методы класса

### `id_product`

```python
@property
def id_product(self) -> Optional[int]:
    """ property `ps_product.id_product: int(10) unsigned` """
    return self.presta_fields.id_product
```

**Назначение**: Получает значение `id_product` из `presta_fields`.

**Возвращает**:

-   `Optional[int]`: Значение `id_product` или `None`, если оно не установлено.

```python
@id_product.setter
def id_product(self, value: int = None):
    """ setter `ID` товара. Для нового товара id назначается из `PrestaShop`. """
    try:
        self.presta_fields.id_product = value
    except Exception as ex:
        logger.error(f"Ошибка при установке id_product:",ex)
```

**Назначение**: Устанавливает значение `id_product` в `presta_fields`.

**Параметры**:

-   `value` (int, optional): Значение `id_product`. По умолчанию `None`.

**Как работает функция**:

1.  Пытается установить значение `value` в `self.presta_fields.id_product`.
2.  В случае возникновения исключения логирует ошибку.

**Примеры**:

```python
product_fields = ProductFields()
product_fields.id_product = 123
print(product_fields.id_product)  # Выведет 123
```

### `id_supplier`

```python
@property
def id_supplier(self) -> Optional[int]:
    """ property `ps_product.id_supplier: int(10) unsigned` """
    return self.presta_fields.id_supplier
```

**Назначение**: Получает значение `id_supplier` из `presta_fields`.

**Возвращает**:

-   `Optional[int]`: Значение `id_supplier` или `None`, если оно не установлено.

```python
@id_supplier.setter
def id_supplier(self, value: int = None):
    """ setter `ID` поставщика."""
    try:
        self.presta_fields.id_supplier = value
    except Exception as ex:
       logger.error(f"Ошибка при установке id_supplier:",ex)
```

**Назначение**: Устанавливает значение `id_supplier` в `presta_fields`.

**Параметры**:

-   `value` (int, optional): Значение `id_supplier`. По умолчанию `None`.

**Как работает функция**:

1.  Пытается установить значение `value` в `self.presta_fields.id_supplier`.
2.  В случае возникновения исключения логирует ошибку.

**Примеры**:

```python
product_fields = ProductFields()
product_fields.id_supplier = 456
print(product_fields.id_supplier)  # Выведет 456
```

### `id_manufacturer`

```python
@property
def id_manufacturer(self) -> Optional[int]:
    """ property `ps_product.id_manufacturer: int(10) unsigned` """
    return self.presta_fields.id_manufacturer
```

**Назначение**: Получает значение `id_manufacturer` из `presta_fields`.

**Возвращает**:

-   `Optional[int]`: Значение `id_manufacturer` или `None`, если оно не установлено.

```python
@id_manufacturer.setter
def id_manufacturer(self, value: int = None):
    """ setter `ID` бренда."""
    try:
         self.presta_fields.id_manufacturer = value
    except Exception as ex:
         logger.error(f"Ошибка при установке id_manufacturer:",ex)
```

**Назначение**: Устанавливает значение `id_manufacturer` в `presta_fields`.

**Параметры**:

-   `value` (int, optional): Значение `id_manufacturer`. По умолчанию `None`.

**Как работает функция**:

1.  Пытается установить значение `value` в `self.presta_fields.id_manufacturer`.
2.  В случае возникновения исключения логирует ошибку.

**Примеры**:

```python
product_fields = ProductFields()
product_fields.id_manufacturer = 789
print(product_fields.id_manufacturer)  # Выведет 789
```

### `id_category_default`

```python
@property
def id_category_default(self) -> Optional[int]:
    """ property `ps_product.id_category_default: int(10) unsigned` """
    return self.presta_fields.id_category_default
```

**Назначение**: Получает значение `id_category_default` из `presta_fields`.

**Возвращает**:

-   `Optional[int]`: Значение `id_category_default` или `None`, если оно не установлено.

```python
@id_category_default.setter
def id_category_default(self, value: int):
    """ setter `ID` главной категории товара."""
    try:
        self.presta_fields.id_category_default = value
    except Exception as ex:
        logger.error(f"Ошибка при установке id_shop_default:",ex)
```

**Назначение**: Устанавливает значение `id_category_default` в `presta_fields`.

**Параметры**:

-   `value` (int): Значение `id_category_default`.

**Как работает функция**:

1.  Пытается установить значение `value` в `self.presta_fields.id_category_default`.
2.  В случае возникновения исключения логирует ошибку.

**Примеры**:

```python
product_fields = ProductFields()
product_fields.id_category_default = 10
print(product_fields.id_category_default)  # Выведет 10
```

### `id_shop_default`

```python
@property
def id_shop_default(self) -> Optional[int]:
    """ property `ps_product.id_shop_default: int(10) unsigned` """
    return self.presta_fields.id_shop_default
```

**Назначение**: Получает значение `id_shop_default` из `presta_fields`.

**Возвращает**:

-   `Optional[int]`: Значение `id_shop_default` или `None`, если оно не установлено.

```python
@id_shop_default.setter
def id_shop_default(self, value: int ):
    """ setter `ID` магазина по умолчанию."""
    try:
        self.presta_fields.id_shop_default = normalize_int(value or 1)
    except Exception as ex:
        logger.error(f"Ошибка при установке id_shop_default:",ex)
```

**Назначение**: Устанавливает значение `id_shop_default` в `presta_fields`.

**Параметры**:

-   `value` (int): Значение `id_shop_default`.

**Как работает функция**:

1.  Нормализует значение `value` с помощью `normalize_int`, используя значение `1` по умолчанию, если `value` равно `None`.
2.  Пытается установить нормализованное значение в `self.presta_fields.id_shop_default`.
3.  В случае возникновения исключения логирует ошибку.

**Примеры**:

```python
product_fields = ProductFields()
product_fields.id_shop_default = 1
print(product_fields.id_shop_default)
```

### `id_shop`

```python
@property
def id_shop(self) -> Optional[int]:
    """ property `ps_product.id_shop: int(10) unsigned` """
    return self.presta_fields.id_shop
```

**Назначение**: Получает значение `id_shop` из `presta_fields`.

**Возвращает**:

-   `Optional[int]`: Значение `id_shop` или `None`, если оно не установлено.

```python
@id_shop.setter
def id_shop(self, value: int):
    """ setter `ID` магазина (для multishop)."""
    try:
        self.presta_fields.id_shop = normalize_int(value or 1)
    except Exception as ex:
         logger.error(f"Ошибка при установке id_shop:",ex)
```

**Назначение**: Устанавливает значение `id_shop` в `presta_fields`.

**Параметры**:

-   `value` (int): Значение `id_shop`.

**Как работает функция**:

1.  Нормализует значение `value` с помощью `normalize_int`, используя значение `1` по умолчанию, если `value` равно `None`.
2.  Пытается установить нормализованное значение в `self.presta_fields.id_shop`.
3.  В случае возникновения исключения логирует ошибку.

**Примеры**:

```python
product_fields = ProductFields()
product_fields.id_shop = 1
print(product_fields.id_shop)
```

### `id_tax`

```python
@property
def id_tax(self) -> Optional[int]:
    """ property `ps_product.id_tax: int(11) unsigned` """
    return self.presta_fields.id_tax
```

**Назначение**: Получает значение `id_tax` из `presta_fields`.

**Возвращает**:

-   `Optional[int]`: Значение `id_tax` или `None`, если оно не установлено.

```python
@id_tax.setter
def id_tax(self, value: int):
     """ setter `ID` налога."""
    
     try:
        self.presta_fields.id_tax = normalize_int(value)
     except Exception as ex:
        logger.error(f"Ошибка при установке id_tax:",ex)
```

**Назначение**: Устанавливает значение `id_tax` в `presta_fields`.

**Параметры**:

-   `value` (int): Значение `id_tax`.

**Как работает функция**:

1.  Нормализует значение `value` с помощью `normalize_int`.
2.  Пытается установить нормализованное значение в `self.presta_fields.id_tax`.
3.  В случае возникновения исключения логирует ошибку.

**Примеры**:

```python
product_fields = ProductFields()
product_fields.id_tax = 5
print(product_fields.id_tax)
```

### `position_in_category`

```python
@property
def position_in_category(self) -> Optional[int]:
     """ property `ps_category_product.position: int(10) unsigned` """
     return self.presta_fields.position_in_category
```

**Назначение**: Получает значение `position_in_category` из `presta_fields`.

**Возвращает**:

-   `Optional[int]`: Значение `position_in_category` или `None`, если оно не установлено.

```python
@position_in_category.setter
def position_in_category(self, value:int = None):
    """ setter  Позиция товара в категории."""
    try:
        self.presta_fields.position_in_category = normalize_int(value)
    except Exception as ex:
       logger.error(f'Ошибка при установке `position_in_category` {value} : ',ex)
```

**Назначение**: Устанавливает значение `position_in_category` в `presta_fields`.

**Параметры**:

-   `value` (int, optional): Значение `position_in_category`. По умолчанию `None`.

**Как работает функция**:

1.  Нормализует значение `value` с помощью `normalize_int`.
2.  Пытается установить нормализованное значение в `self.presta_fields.position_in_category`.
3.  В случае возникновения исключения логирует ошибку.

**Примеры**:

```python
product_fields = ProductFields()
product_fields.position_in_category = 1
print(product_fields.position_in_category)
```

### `on_sale`

```python
@property
def on_sale(self) -> int:
    """ property `ps_product.on_sale: tinyint(1) unsigned` """
    return self.presta_fields.on_sale
```

**Назначение**: Получает значение `on_sale` из `presta_fields`.

**Возвращает**:

-   `int`: Значение `on_sale`.

```python
@on_sale.setter
def on_sale(self, value: int ):
    """ setter Флаг распродажи."""
    self.presta_fields.on_sale = normalize_int(value)
```

**Назначение**: Устанавливает значение `on_sale` в `presta_fields`.

**Параметры**:

-   `value` (int): Значение `on_sale`.

**Как работает функция**:

1.  Нормализует значение `value` с помощью `normalize_int`.
2.  Устанавливает нормализованное значение в `self.presta_fields.on_sale`.

**Примеры**:

```python
product_fields = ProductFields()
product_fields.on_sale = 1
print(product_fields.on_sale)
```

### `online_only`

```python
@property
def online_only(self) -> int:
    """ property `ps_product.online_only: tinyint(1) unsigned` """
    return self.presta_fields.online_only
```

**Назначение**: Получает значение `online_only` из `presta_fields`.

**Возвращает**:

-   `int`: Значение `online_only`.

```python
@online_only.setter
def online_only(self, value: int|bool ):
    """ setter Флаг "только онлайн". """
    self.presta_fields.online_only = normalize_int(value)
```

**Назначение**: Устанавливает значение `online_only` в `presta_fields`.

**Параметры**:

-   `value` (int | bool): Значение `online_only`.

**Как работает функция**:

1.  Нормализует значение `value` с помощью `normalize_int`.
2.  Устанавливает нормализованное значение в `self.presta_fields.online_only`.

**Примеры**:

```python
product_fields = ProductFields()
product_fields.online_only = 1
print(product_fields.online_only)
```

### `ean13`

```python
@property
def ean13(self) -> Optional[str]:
    """ property `ps_product.ean13: varchar(13)` """
    return self.presta_fields.ean13
```

**Назначение**: Получает значение `ean13` из `presta_fields`.

**Возвращает**:

-   `Optional[str]`: Значение `ean13` или `None`, если оно не установлено.

```python
@ean13.setter
def ean13(self, value: str):
    """ setter EAN13 код товара."""
    self.presta_fields.ean13 = normalize_string(value)
```

**Назначение**: Устанавливает значение `ean13` в `presta_fields`.

**Параметры**:

-   `value` (str): Значение `ean13`.

**Как работает функция**:

1.  Нормализует значение `value` с помощью `normalize_string`.
2.  Устанавливает нормализованное значение в `self.presta_fields.ean13`.

**Примеры**:

```python
product_fields = ProductFields()
product_fields.ean13 = '1234567890123'
print(product_fields.ean13)
```

### `isbn`

```python
@property
def isbn(self) -> Optional[str]:
    """ property `ps_product.isbn: varchar(32)` """
    return self.presta_fields.isbn
```

**Назначение**: Получает значение `isbn` из `presta_fields`.

**Возвращает**:

-   `Optional[str]`: Значение `isbn` или `None`, если оно не установлено.

```python
@isbn.setter
def isbn(self, value: str):
    """ setter ISBN код товара."""
    self.presta_fields.isbn = normalize_string(value)
```

**Назначение**: Устанавливает значение `isbn` в `presta_fields`.

**Параметры**:

-   `value` (str): Значение `isbn`.

**Как работает функция**:

1.  Нормализует значение `value` с помощью `normalize_string`.
2.  Устанавливает нормализованное значение в `self.presta_fields.isbn`.

**Примеры**:

```python
product_fields = ProductFields()
product_fields.isbn = '978-0-321-76572-3'
print(product_fields.isbn)
```

### `upc`

```python
@property
def upc(self) -> Optional[str]:
    """ property `ps_product.upc: varchar(12)` """
    return self.presta_fields.upc
```

**Назначение**: Получает значение `upc` из `presta_fields`.

**Возвращает**:

-   `Optional[str]`: Значение `upc` или `None`, если оно не установлено.

```python
@upc.setter
def upc(self, value: str):
    """ setter UPC код товара."""
    self.presta_fields.upc = normalize_string(value)
```

**Назначение**: Устанавливает значение `upc` в `presta_fields`.

**Параметры**:

-   `value` (str): Значение `upc`.

**Как работает функция**:

1.  Нормализует значение `value` с помощью `normalize_string`.
2.  Устанавливает нормализованное значение в `self.presta_fields.upc`.

**Примеры**:

```python
product_fields = ProductFields()
product_fields.upc = '012345678905'
print(product_fields.upc)
```

### `mpn`

```python
@property
def mpn(self) -> Optional[str]:
    """ property `ps_product.mpn: varchar(40)` """
    return self.presta_fields.mpn
```

**Назначение**: Получает значение `mpn` из `presta_fields`.

**Возвращает**:

-   `Optional[str]`: Значение `mpn` или `None`, если оно не установлено.

```python
@mpn.setter
def mpn(self, value: str):
    """ setter MPN код товара."""
    self.presta_fields.mpn = normalize_string(value)
```

**Назначение**: Устанавливает значение `mpn` в `presta_fields`.

**Параметры**:

-   `value` (str): Значение `mpn`.

**Как