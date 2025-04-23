# Модуль грабера

## Обзор

Модуль `graber.py` предназначен для сбора информации о товарах с веб-страниц поставщиков. Он содержит базовый класс `Graber`, который использует веб-драйвер для извлечения целевых полей, таких как название, описание, спецификация, артикул и цена, с HTML-страниц. Локаторы для определения местоположения полей хранятся в JSON-файлах в директории `locators` каждого поставщика.

## Подробней

Этот модуль предоставляет базовый класс для сбора данных о товарах с веб-страниц поставщиков. Он использует веб-драйвер для навигации по страницам и извлечения информации о товарах. Для нестандартной обработки полей товара можно переопределить соответствующие функции в классах, наследующих `Graber`.

## Классы

### `Config`

**Описание**: Класс для хранения глобальных настроек, таких как объект драйвера, локатор для декоратора `@close_pop_up` и префикс поставщика.

**Аттрибуты**:

- `locator_for_decorator` (Optional[SimpleNamespace]): Локатор для декоратора `@close_pop_up`.
- `supplier_prefix` (Optional[str]): Префикс поставщика.
- `driver` (Optional['Driver']): Объект драйвера для управления браузером.

**Принцип работы**:

Класс `Config` используется для хранения глобальных настроек, которые могут быть использованы в различных частях модуля. Он предоставляет удобный способ доступа к этим настройкам через атрибуты класса.

### `Graber`

**Описание**: Базовый класс для сбора данных со страницы для всех поставщиков.

**Атрибуты**:

- `supplier_prefix` (str): Префикс поставщика.
- `product_locator` (SimpleNamespace): Локаторы для полей продукта.
- `category_locator` (SimpleNamespace): Локаторы для полей категорий.
- `driver` (Driver): Экземпляр класса Driver.
- `fields` (ProductFields): Объект для хранения полей продукта.

**Принцип работы**:

Класс `Graber` является базовым классом для сбора данных о товарах с веб-страниц поставщиков. Он инициализируется с префиксом поставщика и объектом драйвера. Класс использует локаторы, загруженные из JSON-файлов, для определения местоположения полей на странице.

**Методы**:

- `__init__`: Инициализация класса Graber.
- `yield_scenarios_for_supplier`: Генератор, который выдает словари сценариев для поставщика.
- `process_supplier_scenarios_async`: Метод, который использует генератор yield_scenarios_for_supplier и вызывает run_scenario для каждого сценария.
- `process_scenarios`: Выполняет один или несколько сценариев для указанного поставщика.
- `set_field_value`: Универсальная функция для установки значений полей с обработкой ошибок.
- `grab_page`: Функция для сбора полей продукта.
- `grab_page_async`: Асинхронная функция для сбора полей продукта.
- `error`: Обработчик ошибок для полей.
- `additional_shipping_cost`: Функция для получения и установки дополнительной стоимости доставки.
- `delivery_in_stock`: Функция для получения и установки статуса доставки в наличии.
- `active`: Функция для получения и установки статуса активности.
- `additional_delivery_times`: Функция для получения и установки дополнительного времени доставки.
- `advanced_stock_management`: Функция для получения и установки статуса расширенного управления запасами (DEPRECATED).
- `affiliate_short_link`: Функция для получения и установки короткой ссылки аффилиата.
- `affiliate_summary`: Функция для получения и установки сводки аффилиата.
- `affiliate_summary_2`: Функция для получения и установки сводки аффилиата 2.
- `affiliate_text`: Функция для получения и установки текста аффилиата.
- `affiliate_image_large`: Функция для получения и установки большого изображения аффилиата.
- `affiliate_image_medium`: Функция для получения и установки среднего изображения аффилиата.
- `affiliate_image_small`: Функция для получения и установки маленького изображения аффилиата.
- `available_date`: Функция для получения и установки доступной даты.
- `available_for_order`: Функция для получения и установки статуса доступности для заказа.
- `available_later`: Функция для получения и установки статуса доступности позже.
- `available_now`: Функция для получения и установки статуса доступности сейчас.
- `additional_categories`: Функция для установки дополнительных категорий.
- `cache_default_attribute`: Функция для получения и установки атрибута кэша по умолчанию.
- `cache_has_attachments`: Функция для получения и установки статуса кэша с вложениями.
- `cache_is_pack`: Функция для получения и установки статуса кэша как набора.
- `condition`: Функция для получения и установки условия продукта.
- `customizable`: Функция для получения и установки статуса настраиваемости.
- `date_add`: Функция для получения и установки даты добавления.
- `date_upd`: Функция для получения и установки даты обновления.
- `delivery_out_stock`: Функция для получения и установки статуса доставки вне склада.
- `depth`: Функция для получения и установки глубины.
- `description`: Функция для получения и установки описания.
- `description_short`: Функция для получения и установки короткого описания.
- `id_category_default`: Функция для получения и установки идентификатора категории по умолчанию.
- `id_default_combination`: Функция для получения и установки идентификатора комбинации по умолчанию.
- `id_product`: Функция для получения и установки идентификатора продукта.
- `locale`: Функция для получения и установки локали.
- `id_default_image`: Функция для получения и установки идентификатора изображения по умолчанию.
- `ean13`: Функция для получения и установки кода EAN13.
- `ecotax`: Функция для получения и установки ecotax.
- `height`: Функция для получения и установки высоты.
- `how_to_use`: Функция для получения и установки инструкции по использованию.
- `id_manufacturer`: Функция для получения и установки идентификатора производителя.
- `id_supplier`: Функция для получения и установки идентификатора поставщика.
- `id_tax_rules_group`: Функция для получения и установки идентификатора налога.
- `id_type_redirected`: Функция для получения и установки идентификатора перенаправленного типа.
- `images_urls`: Функция для получения и установки URL изображений.
- `indexed`: Функция для получения и установки статуса индексации.
- `ingredients`: Функция для получения и установки ингредиентов.
- `meta_description`: Функция для получения и установки мета-описания.
- `meta_keywords`: Функция для получения и установки мета-ключевых слов.
- `meta_title`: Функция для получения и установки мета-заголовка.
- `is_virtual`: Функция для получения и установки виртуального статуса.
- `isbn`: Функция для получения и установки ISBN.
- `link_rewrite`: Функция для получения и установки перезаписи ссылки.
- `location`: Функция для получения и установки местоположения.
- `low_stock_alert`: Функция для получения и установки оповещения о низком уровне запасов.
- `low_stock_threshold`: Функция для получения и установки порога низкого уровня запасов.
- `minimal_quantity`: Функция для получения и установки минимального количества.
- `mpn`: Функция для получения и установки MPN (Manufacturer Part Number).
- `name`: Функция для получения и установки названия продукта.
- `online_only`: Функция для получения и установки статуса "только онлайн".
- `on_sale`: Функция для получения и установки статуса "в продаже".
- `out_of_stock`: Функция для получения и установки статуса "нет в наличии".
- `pack_stock_type`: Функция для получения и установки типа запаса упаковки.
- `price`: Функция для получения и установки цены.
- `product_type`: Функция для получения и установки типа продукта.
- `quantity`: Функция для получения и установки количества.
- `quantity_discount`: Функция для получения и установки скидки на количество.
- `redirect_type`: Функция для получения и установки типа перенаправления.
- `reference`: Функция для получения и установки ссылки.
- `show_condition`: Функция для получения и установки отображения условия.
- `show_price`: Функция для получения и установки отображения цены.
- `state`: Функция для получения и установки состояния.
- `text_fields`: Функция для получения и установки текстовых полей.
- `unit_price_ratio`: Функция для получения и установки коэффициента цены за единицу.
- `unity`: Функция для получения и установки единицы измерения.
- `upc`: Функция для получения и установки UPC.
- `uploadable_files`: Функция для получения и установки загружаемых файлов.
- `default_image_url`: Функция для получения и установки URL изображения по умолчанию.
- `visibility`: Функция для получения и установки видимости.
- `weight`: Функция для получения и установки веса.
- `wholesale_price`: Функция для получения и установки оптовой цены.
- `width`: Функция для получения и установки ширины.
- `specification`: Функция для получения и установки спецификации.
- `link`: Функция для получения и установки ссылки.
- `byer_protection`: Функция для получения и установки защиты покупателя.
- `customer_reviews`: Функция для получения и установки отзывов клиентов.
- `link_to_video`: Функция для получения и установки ссылки на видео.
- `local_image_path`: Функция для получения и сохранения изображения локально.
- `local_video_path`: Функция для получения и сохранения видео локально.

## Функции

### `close_pop_up`

**Назначение**: Создает декоратор для закрытия всплывающих окон перед выполнением основной логики функции.

**Параметры**:

- `value` ('Driver'): Дополнительное значение для декоратора.

**Возвращает**:

- `Callable`: Декоратор, оборачивающий функцию.

**Как работает функция**:

Функция создает декоратор, который закрывает всплывающее окно, если `Config.locator_for_decorator` установлен. Декоратор оборачивает функцию и выполняет закрытие всплывающего окна перед выполнением основной логики функции.

```python
@close_pop_up()
async def some_function(self, value: str):
    # Some code here
    pass
```

## Методы класса

### `__init__`

```python
def __init__(self, supplier_prefix: str,  driver: Optional['Driver'] = None,  lang_index:Optional[int] = 2, ):
```

**Назначение**: Инициализация класса Graber.

**Параметры**:

- `supplier_prefix` (str): Префикс поставщика.
- `driver` ('Driver'): Экземпляр класса Driver.
- `lang_index` (Optional[int]): Индекс языка. По умолчанию 2.

**Как работает функция**:

Функция инициализирует класс `Graber`, устанавливает префикс поставщика, загружает локаторы для продукта и категории, создает экземпляр драйвера, устанавливает язык и настраивает декоратор `@close_pop_up`.

**Примеры**:

```python
graber = Graber(supplier_prefix='some_supplier', driver=Driver(Firefox))
```

### `yield_scenarios_for_supplier`

```python
def yield_scenarios_for_supplier(self, supplier_prefix: str, input_scenarios: Optional[List[Dict[str, Any]] | Dict[str, Any]] = None) -> Generator[Dict[str, Any], None, None]:
```

**Назначение**: Генератор, который выдает (yields) словари сценариев для поставщика.

**Параметры**:

- `supplier_prefix` (str): Префикс (идентификатор) поставщика.
- `input_scenarios` (Optional[List[Dict] | Dict]): Непосредственно переданные сценарии (один словарь или список словарей).

**Возвращает**:

- `Generator[Dict[str, Any], None, None]`: Генератор, возвращающий словари сценариев по одному.

**Как работает функция**:

Функция сначала обрабатывает сценарии, переданные в `input_scenarios`. Если `input_scenarios` пуст или None, функция ищет и загружает .json файлы из директории сценариев поставщика.

**Примеры**:

```python
for scenario in grabber.yield_scenarios_for_supplier(supplier_prefix='some_supplier', input_scenarios=[{'url': 'http://example.com'}])
    print(scenario)
```

### `process_supplier_scenarios_async`

```python
async def process_supplier_scenarios_async(self, supplier_prefix: str, input_scenarios=None, id_lang:Optional[int]=1) -> bool:
```

**Назначение**: Метод, который использует генератор `yield_scenarios_for_supplier` и вызывает `run_scenario` для каждого сценария.

**Параметры**:

- `supplier_prefix` (str): Префикс (идентификатор) поставщика.
- `input_scenarios` (Optional[List[Dict] | Dict]): Непосредственно переданные сценарии (один словарь или список словарей).
- `id_lang` (Optional[int]): Идентификатор языка. По умолчанию 1.

**Возвращает**:

- `bool`: Список результатов выполнения каждого сценария или None в случае критической ошибки.

**Как работает функция**:

Функция получает генератор сценариев с помощью `yield_scenarios_for_supplier`, итерируется по сценариям и вызывает `self.process_scenarios` для каждого сценария.

**Примеры**:

```python
result = await grabber.process_supplier_scenarios_async(supplier_prefix='some_supplier', input_scenarios=[{'url': 'http://example.com'}])
print(result)
```

### `process_scenarios`

```python
async def process_scenarios(self, supplier_prefix: str, input_scenarios: List[Dict[str, Any]] | Dict[str, Any], id_lang:Optional[int]=1) -> Optional[List[Any]]:
```

**Назначение**: Выполняет один или несколько сценариев для указанного поставщика.

**Параметры**:

- `supplier_prefix` (str): Префикс (идентификатор) поставщика.
- `input_scenarios` (List[Dict[str, Any]] | Dict[str, Any]): Данные сценариев: либо список словарей сценариев, либо словарь вида {'scenarios': {'name': dict, ...}}.
- `id_lang` (Optional[int]): Идентификатор языка. По умолчанию 1.

**Возвращает**:

- `Optional[List[Any]]]`: Список результатов выполнения каждого сценария (например, списки обработанных URL товаров) или None в случае критической ошибки.

**Как работает функция**:

Функция нормализует входные данные, динамически импортирует модуль сценария, итерируется по сценариям, переходит по URL сценария, вызывает функцию для получения списка товаров и обрабатывает каждый товар.

**Примеры**:

```python
result = await grabber.process_scenarios(supplier_prefix='some_supplier', input_scenarios=[{'url': 'http://example.com'}])
print(result)
```

### `set_field_value`

```python
async def set_field_value(
        self,
        value: Any,
        locator_func: Callable[[], Any],
        field_name: str,
        default: Any = ''
    ) -> Any:
```

**Назначение**: Универсальная функция для установки значений полей с обработкой ошибок.

**Параметры**:

- `value` (Any): Значение для установки.
- `locator_func` (Callable[[], Any]): Функция для получения значения из локатора.
- `field_name` (str): Название поля.
- `default` (Any): Значение по умолчанию. По умолчанию пустая строка.

**Возвращает**:

- `Any`: Установленное значение.

**Как работает функция**:

Функция устанавливает значение поля, используя значение, переданное в параметре `value`, или значение, полученное из локатора с помощью функции `locator_func`. Если значение не получено, устанавливается значение по умолчанию.

**Примеры**:

```python
value = await grabber.set_field_value(value='some_value', locator_func=lambda: 'locator_value', field_name='some_field', default='default_value')
print(value)
```

### `grab_page`

```python
def grab_page(self, *args, **kwargs) -> ProductFields:
```

**Назначение**: Функция для сбора полей продукта.

**Параметры**:

- `*args`: Список полей для сбора.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:

- `ProductFields`: Объект ProductFields с собранными данными.

**Как работает функция**:

Функция запускает асинхронную функцию `grab_page_async` и возвращает результат.

**Примеры**:

```python
product_fields = grabber.grab_page(id_product='some_id', name='some_name')
print(product_fields)
```

### `grab_page_async`

```python
async def grab_page_async(self, *args, **kwargs) -> ProductFields:
```

**Назначение**: Асинхронная функция для сбора полей продукта.

**Параметры**:

- `*args`: Список полей для сбора.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:

- `ProductFields`: Объект ProductFields с собранными данными.

**Как работает функция**:

Функция динамически вызывает функции для каждого поля из `args` и собирает данные в объект `ProductFields`.

**Примеры**:

```python
product_fields = await grabber.grab_page_async(id_product='some_id', name='some_name')
print(product_fields)
```

### `error`

```python
async def error(self, field: str):
```

**Назначение**: Обработчик ошибок для полей.

**Параметры**:

- `field` (str): Название поля.

**Как работает функция**:

Функция логирует отладочное сообщение об ошибке заполнения поля.

**Примеры**:

```python
await grabber.error(field='some_field')
```

### `additional_shipping_cost`

```python
@close_pop_up()
async def additional_shipping_cost(self, value:Optional[Any] = None) -> bool:
```

**Назначение**: Функция для получения и установки дополнительной стоимости доставки.

**Параметры**:

- `value` (Any): Значение дополнительной стоимости доставки.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить значение дополнительной стоимости доставки из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.additional_shipping_cost(value='10.00')
print(result)
```

### `delivery_in_stock`

```python
@close_pop_up()
async def delivery_in_stock(self, value:Optional[str] = None) -> bool:
```

**Назначение**: Функция для получения и установки статуса доставки в наличии.

**Параметры**:

- `value` (str): Статус доставки в наличии.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить статус доставки в наличии из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.delivery_in_stock(value='In Stock')
print(result)
```

### `active`

```python
@close_pop_up()
async def active(self, value:bool = True) -> bool:
```

**Назначение**: Функция для получения и установки статуса активности.

**Параметры**:

- `value` (bool): Статус активности.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить статус активности из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.active(value=True)
print(result)
```

### `additional_delivery_times`

```python
@close_pop_up()
async def additional_delivery_times(self, value:Optional[str] = None) -> bool:
```

**Назначение**: Функция для получения и установки дополнительного времени доставки.

**Параметры**:

- `value` (str): Дополнительное время доставки.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить дополнительное время доставки из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.additional_delivery_times(value='3-5 days')
print(result)
```

### `advanced_stock_management`

```python
@close_pop_up()
async def advanced_stock_management(self, value:Optional[Any] = None) -> bool:
```

**Назначение**: Функция для получения и установки статуса расширенного управления запасами (DEPRECATED).

**Параметры**:

- `value` (Any): Статус расширенного управления запасами.

**Возвращает**:

- `bool`: Всегда True.

**Как работает функция**:

Функция всегда возвращает True.

**Примеры**:

```python
result = await grabber.advanced_stock_management(value=True)
print(result)
```

### `affiliate_short_link`

```python
@close_pop_up()
async def affiliate_short_link(self, value:Optional[str] = None) -> bool:
```

**Назначение**: Функция для получения и установки короткой ссылки аффилиата.

**Параметры**:

- `value` (str): Короткая ссылка аффилиата.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить короткую ссылку аффилиата из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.affiliate_short_link(value='http://short.link')
print(result)
```

### `affiliate_summary`

```python
@close_pop_up()
async def affiliate_summary(self, value:Optional[str] = None) -> bool:
```

**Назначение**: Функция для получения и установки сводки аффилиата.

**Параметры**:

- `value` (str): Сводка аффилиата.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить сводку аффилиата из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.affiliate_summary(value='Some summary')
print(result)
```

### `affiliate_summary_2`

```python
@close_pop_up()
async def affiliate_summary_2(self, value:Optional[Any] = None) -> bool:
```

**Назначение**: Функция для получения и установки сводки аффилиата 2.

**Параметры**:

- `value` (Any): Сводка аффилиата 2.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить сводку аффилиата 2 из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.affiliate_summary_2(value='Some summary 2')
print(result)
```

### `affiliate_text`

```python
@close_pop_up()
async def affiliate_text(self, value:Optional[str] = None) -> bool:
```

**Назначение**: Функция для получения и установки текста аффилиата.

**Параметры**:

- `value` (Any): Текст аффилиата.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить текст аффилиата из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.affiliate_text(value='Some text')
print(result)
```

### `affiliate_image_large`

```python
@close_pop_up()
async def affiliate_image_large(self, value:Optional[str] = None) -> bool:
```

**Назначение**: Функция для получения и установки большого изображения аффилиата.

**Параметры**:

- `value` (str): URL большого изображения аффилиата.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить URL большого изображения аффилиата из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.affiliate_image_large(value='http://example.com/image.jpg')
print(result)
```

### `affiliate_image_medium`

```python
@close_pop_up()
async def affiliate_image_medium(self, value:Optional[str] = None) -> bool:
```

**Назначение**: Функция для получения и установки среднего изображения аффилиата.

**Параметры**:

- `value` (str): URL среднего изображения аффилиата.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить URL среднего изображения аффилиата из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.affiliate_image_medium(value='http://example.com/image.jpg')
print(result)
```

### `affiliate_image_small`

```python
@close_pop_up()
async def affiliate_image_small(self, value:Optional[str] = None) -> bool:
```

**Назначение**: Функция для получения и установки маленького изображения аффилиата.

**Параметры**:

- `value` (str): URL маленького изображения аффилиата.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить URL маленького изображения аффилиата из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.affiliate_image_small(value='http://example.com/image.jpg')
print(result)
```

### `available_date`

```python
@close_pop_up()
async def available_date(self, value:Optional[Any] = None) -> bool:
```

**Назначение**: Функция для получения и установки доступной даты.

**Параметры**:

- `value` (Any): Доступная дата.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить доступную дату из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.available_date(value='2024-01-01')
print(result)
```

### `available_for_order`

```python
@close_pop_up()
async def available_for_order(self, value:Optional[str] = None) -> bool:
```

**Назначение**: Функция для получения и установки статуса доступности для заказа.

**Параметры**:

- `value` (str): Статус доступности для заказа.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить статус доступности для заказа из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.available_for_order(value='Yes')
print(result)
```

### `available_later`

```python
@close_pop_up()
async def available_later(self, value:Optional[str] = None) -> bool:
```

**Назначение**: Функция для получения и установки статуса доступности позже.

**Параметры**:

- `value` (str): Статус доступности позже.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить статус доступности позже из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.available_later(value='Available Later')
print(result)
```

### `available_now`

```python
@close_pop_up()
async def available_now(self, value:Optional[str] = None) -> bool:
```

**Назначение**: Функция для получения и установки статуса доступности сейчас.

**Параметры**:

- `value` (Any): Статус доступности сейчас.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить статус доступности сейчас из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.available_now(value='Available Now')
print(result)
```

### `additional_categories`

```python
@close_pop_up()
async def additional_categories(self, value: str | list = None) -> dict:
```

**Назначение**: Функция для установки дополнительных категорий.

**Параметры**:

- `value` (str | list, optional): Строка или список категорий. Если не передано, используется пустое значение.

**Возвращает**:

- `dict`: Словарь с ID категорий.

**Как работает функция**:

Функция устанавливает дополнительные категории в поле `additional_categories` объекта `ProductFields`.

**Примеры**:

```python
result = await grabber.additional_categories(value=['Category1', 'Category2'])
print(result)
```

### `cache_default_attribute`

```python
@close_pop_up()
async def cache_default_attribute(self, value:Optional[Any] = None) -> bool:
```

**Назначение**: Функция для получения и установки атрибута кэша по умолчанию.

**Параметры**:

- `value` (Any): Атрибут кэша по умолчанию.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить атрибут кэша по умолчанию из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.cache_default_attribute(value='SomeAttribute')
print(result)
```

### `cache_has_attachments`

```python
@close_pop_up()
async def cache_has_attachments(self, value:Optional[Any] = None) -> bool:
```

**Назначение**: Функция для получения и установки статуса кэша с вложениями.

**Параметры**:

- `value` (Any): Статус кэша с вложениями.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить статус кэша с вложениями из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.cache_has_attachments(value=True)
print(result)
```

### `cache_is_pack`

```python
@close_pop_up()
async def cache_is_pack(self, value:Optional[str] = None) -> bool:
```

**Назначение**: Функция для получения и установки статуса кэша как набора.

**Параметры**:

- `value` (str): Статус кэша как набора.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить статус кэша как набора из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.cache_is_pack(value='Yes')
print(result)
```

### `condition`

```python
@close_pop_up()
async def condition(self, value:Optional[Any] = None) -> bool:
```

**Назначение**: Функция для получения и установки условия продукта.

**Параметры**:

- `value` (Any): Условие продукта.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить условие продукта из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.condition(value='new')
print(result)
```

### `customizable`

```python
@close_pop_up()
async def customizable(self, value:Optional[Any] = None) -> bool:
```

**Назначение**: Функция для получения и установки статуса настраиваемости.

**Параметры**:

- `value` (Any): Статус настраиваемости.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить статус настраиваемости из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.customizable(value=True)
print(result)
```

### `date_add`

```python
@close_pop_up()
async def date_add(self, value:Optional[str | datetime.date] = None) -> bool:
```

**Назначение**: Функция для получения и установки даты добавления.

**Параметры**:

- `value` (Any): Дата добавления.

**Возвращает**:

- `bool`: True в случае успеха, None в случае ошибки.

**Как работает функция**:

Функция пытается получить дату добавления из локатора или использовать переданное значение.

**Примеры**:

```python
result = await grabber.date_add(value='2024-01-01')
print(result)
```

### `date_upd`

```python
@close_pop_up()
async def date_upd(self, value