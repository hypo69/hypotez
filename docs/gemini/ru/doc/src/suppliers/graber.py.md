# Модуль грабера

## Обзор

Модуль `graber.py` предназначен для сбора информации о товарах с веб-страниц поставщиков. Он содержит базовый класс `Graber`, который использует веб-драйвер (класс `Driver`) для извлечения целевых полей, таких как название, описание, спецификация, артикул и цена. Локаторы для этих полей хранятся в JSON-файлах в директории `locators` каждого поставщика.

## Подробней

Этот модуль играет важную роль в процессе сбора данных о товарах из различных источников (веб-страниц поставщиков) для дальнейшей обработки и интеграции в систему `hypotez`. Он предоставляет гибкий и расширяемый способ определения и извлечения информации о товарах, позволяя адаптироваться к различным структурам веб-страниц и требованиям поставщиков.

## Классы

### `Context`

**Описание**: Класс для хранения глобальных настроек, таких как объект драйвера, локатор для декоратора `@close_pop_up` и префикс поставщика.

**Атрибуты**:

- `driver` (Optional['Driver']): Объект драйвера, используемый для управления браузером или другим интерфейсом.
- `locator_for_decorator` (Optional[SimpleNamespace]): Локатор для декоратора `@close_pop_up`, устанавливается при инициализации поставщика.
- `supplier_prefix` (Optional[str]): Префикс поставщика.

**Принцип работы**:
Класс `Context` используется для хранения глобальных настроек, которые могут быть доступны и изменены в разных частях кода. Это позволяет избежать передачи одних и тех же параметров в разные функции и классы, а также обеспечивает централизованное управление настройками.

**Примеры**:

```python
context = Context()
context.supplier_prefix = 'prefix'
print(context.supplier_prefix)
```

### `Graber`

**Описание**: Базовый класс для сбора данных со страницы для всех поставщиков.

**Атрибуты**:

- `supplier_prefix` (str): Префикс поставщика.
- `locator` (SimpleNamespace): Объект, содержащий локаторы для элементов на странице продукта.
- `driver` ('Driver'): Экземпляр класса `Driver` для управления браузером.
- `fields` (ProductFields): Объект класса `ProductFields` для хранения собранных данных о продукте.

**Принцип работы**:

Класс `Graber` инициализируется с префиксом поставщика и экземпляром драйвера. Он загружает локаторы из JSON-файла и создает объект `ProductFields` для хранения данных. Основная задача класса - сбор данных о продукте со страницы поставщика с использованием веб-драйвера и локаторов.

**Методы**:
- `__init__`: Инициализация класса Graber.
- `error`: Обработчик ошибок для полей.
- `set_field_value`: Универсальная функция для установки значений полей с обработкой ошибок.
- `grab_page`: Асинхронная функция для сбора полей продукта.
- `grab_page_async`: Асинхронная функция для сбора полей продукта.
- `additional_shipping_cost`: Получение и установка дополнительной стоимости доставки.
- `delivery_in_stock`: Получение и установка статуса доставки в наличии.
- `active`: Получение и установка статуса активности.
- `additional_delivery_times`: Получение и установка дополнительного времени доставки.
- `advanced_stock_management`: Получение и установка статуса расширенного управления запасами.
- `affiliate_short_link`: Получение и установка короткой партнерской ссылки.
- `affiliate_summary`: Получение и установка партнерского резюме.
- `affiliate_summary_2`: Получение и установка партнерского резюме 2.
- `affiliate_text`: Получение и установка партнерского текста.
- `affiliate_image_large`: Получение и установка большого партнерского изображения.
- `affiliate_image_medium`: Получение и установка среднего партнерского изображения.
- `affiliate_image_small`: Получение и установка маленького партнерского изображения.
- `available_date`: Получение и установка доступной даты.
- `available_for_order`: Получение и установка статуса доступности для заказа.
- `available_later`: Получение и установка статуса доступности позже.
- `available_now`: Получение и установка статуса доступности сейчас.
- `additional_categories`: Установка дополнительных категорий.
- `cache_default_attribute`: Получение и установка кэшированного атрибута по умолчанию.
- `cache_has_attachments`: Получение и установка статуса наличия вложений в кэше.
- `cache_is_pack`: Получение и установка статуса является ли кэш пакетом.
- `condition`: Получение и установка условия продукта.
- `customizable`: Получение и установка статуса настраиваемости.
- `date_add`: Получение и установка даты добавления.
- `date_upd`: Получение и установка даты обновления.
- `delivery_out_stock`: Получение и установка доставки вне склада.
- `depth`: Получение и установка глубины.
- `description`: Получение и установка описания.
- `description_short`: Получение и установка короткого описания.
- `id_category_default`: Получение и установка ID категории по умолчанию.
- `id_default_combination`: Получение и установка ID комбинации по умолчанию.
- `id_product`: Получение и установка ID продукта.
- `locale`: Получение и установка локали.
- `id_default_image`: Получение и установка ID изображения по умолчанию.
- `ean13`: Получение и установка кода EAN13.
- `ecotax`: Получение и установка ecotax.
- `height`: Получение и установка высоты.
- `how_to_use`: Получение и установка инструкции по использованию.
- `id_manufacturer`: Получение и установка ID производителя.
- `id_supplier`: Получение и установка ID поставщика.
- `id_tax`: Получение и установка ID налога.
- `id_type_redirected`: Получение и установка ID перенаправленного типа.
- `images_urls`: Получение и установка URL изображений.
- `indexed`: Получение и установка статуса индексации.
- `ingredients`: Получение и установка ингредиентов.
- `meta_description`: Получение и установка мета-описания.
- `meta_keywords`: Получение и установка мета-ключевых слов.
- `meta_title`: Получение и установка мета-заголовка.
- `is_virtual`: Получение и установка виртуального статуса.
- `isbn`: Получение и установка ISBN.
- `link_rewrite`: Получение и установка перезаписи ссылки.
- `location`: Получение и установка местоположения.
- `low_stock_alert`: Получение и установка оповещения о низком запасе.
- `low_stock_threshold`: Получение и установка порога низкого запаса.
- `minimal_quantity`: Получение и установка минимального количества.
- `mpn`: Получение и установка MPN (Manufacturer Part Number).
- `name`: Получение и установка названия продукта.
- `online_only`: Получение и установка статуса "только онлайн".
- `on_sale`: Получение и установка статуса "в продаже".
- `out_of_stock`: Получение и установка статуса "нет в наличии".
- `pack_stock_type`: Получение и установка типа запаса пакета.
- `price`: Получение и установка цены.
- `product_type`: Получение и установка типа продукта.
- `quantity`: Получение и установка количества.
- `quantity_discount`: Получение и установка скидки на количество.
- `redirect_type`: Получение и установка типа перенаправления.
- `reference`: Получение и установка ссылки.
- `show_condition`: Получение и установка условия показа.
- `show_price`: Получение и установка показа цены.
- `state`: Получение и установка состояния.
- `text_fields`: Получение и установка текстовых полей.
- `unit_price_ratio`: Получение и установка коэффициента цены за единицу.
- `unity`: Получение и установка единства.
- `upc`: Получение и установка UPC.
- `uploadable_files`: Получение и установка загружаемых файлов.
- `default_image_url`: Получение и установка URL изображения по умолчанию.
- `visibility`: Получение и установка видимости.
- `weight`: Получение и установка веса.
- `wholesale_price`: Получение и установка оптовой цены.
- `width`: Получение и установка ширины.
- `specification`: Получение и установка спецификации.
- `link`: Получение и установка ссылки.
- `byer_protection`: Получение и установка защиты покупателя.
- `customer_reviews`: Получение и установка отзывов клиентов.
- `link_to_video`: Получение и установка ссылки на видео.
- `local_image_path`: Получение и сохранение изображения локально.
- `local_video_path`: Получение и сохранение видео локально.

## Функции

### `close_pop_up`

```python
def close_pop_up() -> Callable:
    """Создает декоратор для закрытия всплывающих окон перед выполнением основной логики функции.
    Функция `driver.execute_locator()` будет вызвана только если был указан `Context.locator_for_decorator` при инициализации экземляра класса.

    Args:
        value (\'Driver\'): Дополнительное значение для декоратора.

    Returns:
        Callable: Декоратор, оборачивающий функцию.
    """
```

**Назначение**: Функция создает декоратор `@close_pop_up`, который предназначен для закрытия всплывающих окон перед выполнением основной логики декорируемой функции.

**Как работает функция**:

1. Определяется внутренняя функция `decorator`, которая принимает функцию `func` в качестве аргумента и возвращает обертку `wrapper`.
2. Внутри функции `wrapper` проверяется, установлен ли `Context.locator_for_decorator`. Если да, то выполняется попытка закрытия всплывающего окна с помощью `Context.driver.execute_locator(Context.locator_for_decorator)`.
3. После выполнения (или попытки выполнения) закрытия всплывающего окна, `Context.locator_for_decorator` сбрасывается в `None`, чтобы декоратор не срабатывал повторно.
4. В конце функция `wrapper` вызывает и возвращает результат выполнения исходной функции `func`.

**Примеры**:

```python
@close_pop_up()
async def my_function():
    # Основная логика функции
    pass
```

## Методы класса `Graber`

### `__init__`

```python
def __init__(self, supplier_prefix: str, lang_index:int, driver: 'Driver'):
    """Инициализация класса Graber.

    Args:
        supplier_prefix (str): Префикс поставщика.
        driver (\'Driver\'): Экземпляр класса Driver.
    """
```

**Назначение**: Инициализирует экземпляр класса `Graber` с префиксом поставщика, индексом языка и экземпляром драйвера.

**Параметры**:

- `supplier_prefix` (str): Префикс поставщика.
- `lang_index` (int): Индекс языка.
- `driver` ('Driver'): Экземпляр класса `Driver`.

**Как работает функция**:

1. Устанавливает атрибуты `supplier_prefix`, `driver` и `fields` на основе переданных аргументов.
2. Загружает локаторы из JSON-файла с использованием `j_loads_ns` и сохраняет их в атрибуте `locator`.
3. Создает экземпляр класса `ProductFields` с указанным индексом языка и сохраняет его в атрибуте `fields`.
4. Устанавливает атрибуты класса `Context` для `driver`, `supplier_prefix` и `locator_for_decorator`.

**Примеры**:

```python
graber = Graber(supplier_prefix='some_supplier', lang_index=0, driver=driver)
```

### `error`

```python
async def error(self, field: str):
    """Обработчик ошибок для полей."""
```

**Назначение**: Обработчик ошибок для полей.

**Параметры**:

- `field` (str): Название поля, для которого произошла ошибка.

**Как работает функция**:

1. Логирует отладочное сообщение с указанием поля, для которого произошла ошибка.

**Примеры**:

```python
await graber.error('name')
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
    """Универсальная функция для установки значений полей с обработкой ошибок.

    Args:
        value (Any): Значение для установки.
        locator_func (Callable[[], Any]): Функция для получения значения из локатора.
        field_name (str): Название поля.
        default (Any): Значение по умолчанию. По умолчанию пустая строка.

    Returns:
        Any: Установленное значение.
    """
```

**Назначение**: Универсальная функция для установки значений полей с обработкой ошибок.

**Параметры**:

- `value` (Any): Значение для установки.
- `locator_func` (Callable[[], Any]): Функция для получения значения из локатора.
- `field_name` (str): Название поля.
- `default` (Any, optional): Значение по умолчанию. По умолчанию ''.

**Как работает функция**:

1. Асинхронно выполняет функцию `locator_func` для получения значения из локатора.
2. Если передано значение `value`, возвращает его.
3. Если получено значение из локатора (`locator_result`), возвращает его.
4. В противном случае логирует ошибку и возвращает значение по умолчанию.

**Примеры**:

```python
async def get_name_from_locator():
    return await self.driver.execute_locator(self.locator.name)

name = await self.set_field_value(
    value=None,
    locator_func=get_name_from_locator,
    field_name='name',
    default='Unknown'
)
```

### `grab_page`

```python
def grab_page(self, *args, **kwards) -> ProductFields:
    return asyncio.run(self.grab_page_async(*args, **kwards))
```

**Назначение**: Синхронная функция для запуска асинхронной функции сбора полей продукта.

**Параметры**:

- `*args`: Произвольные позиционные аргументы, передаваемые в `grab_page_async`.
- `**kwards`: Произвольные именованные аргументы, передаваемые в `grab_page_async`.

**Возвращает**:

- `ProductFields`: Объект `ProductFields` с собранными данными.

**Как работает функция**:

1. Использует `asyncio.run` для запуска асинхронной функции `grab_page_async` в синхронном контексте.
2. Передает все аргументы, полученные функцией `grab_page` в `grab_page_async`

**Примеры**:

```python
product_fields = graber.grab_page(id_product='123', name='Test Product')
```

### `grab_page_async`

```python
async def grab_page_async(self, *args, **kwards) -> ProductFields:
    """Асинхронная функция для сбора полей продукта."""
```

**Назначение**: Асинхронная функция для сбора полей продукта.

**Параметры**:

- `*args`: Список полей для сбора информации.
- `**kwards`: Словарь с дополнительными параметрами.

**Возвращает**:

- `ProductFields`: Объект `ProductFields` с собранными данными.

**Как работает функция**:

1. Определяет внутреннюю асинхронную функцию `fetch_all_data`, которая динамически вызывает функции для каждого поля из `args`.
2. Если `args` пустой, то по какой-то причине не были переданы имена полей для сбора информации, в таком случае  `args` определяется как `['id_product', 'name', 'description_short', 'description', 'specification', 'local_image_path']`
3. Для каждого имени поля функция пытается получить атрибут с этим именем из экземпляра класса (self).
4. Если атрибут является вызываемым (функцией), она вызывает его с помощью `await function(kwards.get(filed_name, ''))`.
5. После сбора всех полей возвращает объект `self.fields`.

**Примеры**:

```python
product_fields = await graber.grab_page_async(id_product='123', name='Test Product')
```

### `additional_shipping_cost`

```python
    @close_pop_up()
    async def additional_shipping_cost(self, value:Optional[Any] = None):
        """Fetch and set additional shipping cost.
        Args:
        value (Any): это значение можно передать в словаре kwards чеез ключ {additional_shipping_cost = `value`} при определении класса
        если `value` был передан - его значение подставляется в поле `ProductFields.additional_shipping_cost
        """
```

**Назначение**: Асинхронная функция для получения и установки дополнительной стоимости доставки.

**Параметры**:

- `value` (Any, optional): Значение, которое можно передать в словаре `kwargs` через ключ `additional_shipping_cost`. Если `value` передано, его значение будет установлено в поле `ProductFields.additional_shipping_cost`.

**Как работает функция**:

1. Пытается получить значение дополнительной стоимости доставки через `execute_locator`.
2. Если значение получено, оно нормализуется и устанавливается в поле `ProductFields.additional_shipping_cost`.
3. Если поле не заполнено, логируется ошибка.

**Примеры**:

```python
await graber.additional_shipping_cost(value='10.00')
```

### `delivery_in_stock`

```python
    @close_pop_up()
    async def delivery_in_stock(self, value:Optional[Any] = None):
        """Fetch and set delivery in stock status.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {delivery_in_stock = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.delivery_in_stock`.\n        """
```

**Назначение**: Асинхронная функция для получения и установки статуса доставки в наличии.

**Параметры**:

- `value` (Any, optional): Значение, которое можно передать в словаре `kwargs` через ключ `delivery_in_stock`. Если `value` передано, его значение будет установлено в поле `ProductFields.delivery_in_stock`.

**Как работает функция**:

1. Пытается получить значение статуса доставки в наличии через `execute_locator`.
2. Если значение получено, оно нормализуется и устанавливается в поле `ProductFields.delivery_in_stock`.
3. Если поле не заполнено, логируется ошибка.

**Примеры**:

```python
await graber.delivery_in_stock(value='В наличии')
```

### `active`

```python
    @close_pop_up()
    async def active(self, value:Optional[Any] = None):
        """Fetch and set active status.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {active = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.active`.
        Принимаемое значениеЬ 1/0
        """
```

**Назначение**: Асинхронная функция для получения и установки статуса активности.

**Параметры**:

- `value` (Any, optional): Значение, которое можно передать в словаре `kwargs` через ключ `active`. Если `value` передано, его значение будет установлено в поле `ProductFields.active`. Принимаемые значения: 1 или 0.

**Как работает функция**:

1. Пытается получить значение статуса активности через `execute_locator`.
2. Если значение получено, оно нормализуется и устанавливается в поле `ProductFields.active`.
3. Если поле не заполнено, логируется ошибка.

**Примеры**:

```python
await graber.active(value=1)
```

### `additional_delivery_times`

```python
    @close_pop_up()
    async def additional_delivery_times(self, value:Optional[Any] = None):
        """Fetch and set additional delivery times.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {additional_delivery_times = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.additional_delivery_times`.\n        """
```

**Назначение**: Асинхронная функция для получения и установки дополнительного времени доставки.

**Параметры**:

- `value` (Any, optional): Значение, которое можно передать в словаре `kwargs` через ключ `additional_delivery_times`. Если `value` передано, его значение будет установлено в поле `ProductFields.additional_delivery_times`.

**Как работает функция**:

1. Пытается получить значение дополнительного времени доставки через `execute_locator`.
2. Если значение получено, оно устанавливается в поле `ProductFields.additional_delivery_times`.
3. Если поле не заполнено, логируется ошибка.

**Примеры**:

```python
await graber.additional_delivery_times(value='3-5 дней')
```

### `advanced_stock_management`

```python
    @close_pop_up()
    async def advanced_stock_management(self, value:Optional[Any] = None):
        """Fetch and set advanced stock management status.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {advanced_stock_management = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.advanced_stock_management`.\n        """
```

**Назначение**: Асинхронная функция для получения и установки статуса расширенного управления запасами.

**Параметры**:

- `value` (Any, optional): Значение, которое можно передать в словаре `kwargs` через ключ `advanced_stock_management`. Если `value` передано, его значение будет установлено в поле `ProductFields.advanced_stock_management`.

**Как работает функция**:

1. Пытается получить значение статуса расширенного управления запасами через `execute_locator`.
2. Если значение получено, оно устанавливается в поле `ProductFields.advanced_stock_management`.
3. Если поле не заполнено, логируется ошибка.

**Примеры**:

```python
await graber.advanced_stock_management(value='1')
```

### `affiliate_short_link`

```python
    @close_pop_up()
    async def affiliate_short_link(self, value:Optional[Any] = None):
        """Fetch and set affiliate short link.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {affiliate_short_link = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.affiliate_short_link`.\n        """
```

**Назначение**: Асинхронная функция для получения и установки короткой партнерской ссылки.

**Параметры**:

- `value` (Any, optional): Значение, которое можно передать в словаре `kwargs` через ключ `affiliate_short_link`. Если `value` передано, его значение будет установлено в поле `ProductFields.affiliate_short_link`.

**Как работает функция**:

1. Пытается получить значение короткой партнерской ссылки через `execute_locator`.
2. Если значение получено, оно устанавливается в поле `ProductFields.affiliate_short_link`.

**Примеры**:

```python
await graber.affiliate_short_link(value='https://short.link')
```

### `affiliate_summary`

```python
    @close_pop_up()
    async def affiliate_summary(self, value:Optional[Any] = None):
        """Fetch and set affiliate summary.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {affiliate_summary = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.affiliate_summary`.\n        """
```

**Назначение**: Асинхронная функция для получения и установки партнерского резюме.

**Параметры**:

- `value` (Any, optional): Значение, которое можно передать в словаре `kwargs` через ключ `affiliate_summary`. Если `value` передано, его значение будет установлено в поле `ProductFields.affiliate_summary`.

**Как работает функция**:

1. Пытается получить значение партнерского резюме через `execute_locator`.
2. Если значение получено, оно нормализуется и устанавливается в поле `ProductFields.affiliate_summary`.

**Примеры**:

```python
await graber.affiliate_summary(value='Краткое описание партнерской программы')
```

### `affiliate_summary_2`

```python
    @close_pop_up()
    async def affiliate_summary_2(self, value:Optional[Any] = None):
        """Fetch and set affiliate summary 2.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {affiliate_summary_2 = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.affiliate_summary_2`.\n        """
```

**Назначение**: Асинхронная функция для получения и установки второго партнерского резюме.

**Параметры**:

- `value` (Any, optional): Значение, которое можно передать в словаре `kwargs` через ключ `affiliate_summary_2`. Если `value` передано, его значение будет установлено в поле `ProductFields.affiliate_summary_2`.

**Как работает функция**:

1. Пытается получить значение второго партнерского резюме через `execute_locator`.
2. Если значение получено, оно устанавливается в поле `ProductFields.affiliate_summary_2`.
3. Если поле не заполнено, логируется ошибка.

**Примеры**:

```python
await graber.affiliate_summary_2(value='Дополнительное описание партнерской программы')
```

### `affiliate_text`

```python
    @close_pop_up()
    async def affiliate_text(self, value:Optional[Any] = None):
        """Fetch and set affiliate text.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {affiliate_text = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.affiliate_text`.\n        """
```

**Назначение**: Асинхронная функция для получения и установки партнерского текста.

**Параметры**:

- `value` (Any, optional): Значение, которое можно передать в словаре `kwargs` через ключ `affiliate_text`. Если `value` передано, его значение будет установлено в поле `ProductFields.affiliate_text`.

**Как работает функция**:

1. Пытается получить значение партнерского текста через `execute_locator`.
2. Если значение получено, оно устанавливается в поле `ProductFields.affiliate_text`.
3. Если поле не заполнено, логируется ошибка.

**Примеры**:

```python
await graber.affiliate_text(value='Текст партнерской программы')
```

### `affiliate_image_large`

```python
    @close_pop_up()
    async def affiliate_image_large(self, value:Optional[Any] = None):
        """Fetch and set affiliate large image.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {affiliate_image_large = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.affiliate_image_large`.\n        """
```

**Назначение**: Асинхронная функция для получения и установки большого партнерского изображения.

**Параметры**:

- `value` (Any, optional): Значение, которое можно передать в словаре `kwargs` через ключ `affiliate_image_large`. Если `value` передано, его значение будет установлено в поле `ProductFields.affiliate_image_large`.

**Как работает функция**:

1. Пытается получить значение большого партнерского изображения через `execute_locator`.
2. Если значение получено, оно устанавливается в поле `ProductFields.affiliate_image_large`.

**Примеры**:

```python
await graber.affiliate_image_large(value='https://example.com/large_image.jpg')
```

### `affiliate_image_medium`

```python
    @close_pop_up()
    async def affiliate_image_medium(self, value:Optional[Any] = None):
        """Fetch and set affiliate medium image.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {affiliate_image_medium = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.affiliate_image_medium`.\n        """
```

**Назначение**: Асинхронная функция для получения и установки среднего партнерского изображения.

**Параметры**:

- `value` (Any, optional): Значение, которое можно передать в словаре `kwargs` через ключ `affiliate_image_medium`. Если `value` передано, его значение будет установлено в поле `ProductFields.affiliate_image_medium`.

**Как работает функция**:

1. Пытается получить значение среднего партнерского изображения через `execute_locator`.
2. Если значение получено, оно устанавливается в поле `ProductFields.affiliate_image_medium`.
3. Если поле не заполнено, логируется ошибка.

**Примеры**:

```python
await graber.affiliate_image_medium(value='https://example.com/medium_image.jpg')
```

### `affiliate_image_small`

```python
    @close_pop_up()
    async def affiliate_image_small(self, value:Optional[Any] = None):
        """Fetch and set affiliate small image.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {affiliate_image_small = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.affiliate_image_small`.\n        """
```

**Назначение**: Асинхронная функция для получения и установки маленького партнерского изображения.

**Параметры**:

- `value` (Any, optional): Значение, которое можно передать в словаре `kwargs` через ключ `affiliate_image_small`. Если `value` передано, его значение будет установлено в поле `ProductFields.affiliate_image_small`.

**Как работает функция**:

1. Пытается получить значение маленького партнерского изображения через `execute_locator`.
2. Если значение получено, оно устанавливается в поле `ProductFields.affiliate_image_small`.
3. Если поле не заполнено, логируется ошибка.

**Примеры**:

```python
await graber.affiliate_image_small(value='https://example.com/small_image.jpg')
```

### `available_date`

```python
    @close_pop_up()
    async def available_date(self, value:Optional[Any] = None):
        """Fetch and set available date.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {available_date = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.available_date`.\n        """
```

**Назначение**: Асинхронная функция для получения и установки доступной даты.

**Параметры**:

- `value` (Any, optional): Значение, которое можно передать в словаре `kwargs` через ключ `available_date`. Если `value` передано, его значение будет установлено в поле `ProductFields.available_date`.

**Как работает функция**:

1. Пытается получить значение доступной даты через `execute_locator`.
2. Если значение получено, оно устанавливается в поле `ProductFields.available_date`.
3. Если поле не заполнено, логируется ошибка.

**Примеры**:

```python
await graber.available_date(value='2024-12-31')
```

### `available_for_order`

```python
    @close_pop_up()
    async def available_for_order(self, value:Optional[Any] = None):
        """Fetch and set available for order status.

        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {available_for_order = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.available_for_order`.\n        """
```

**Назначение**: Асинхронная функция для получения и установки статуса "доступно для заказа".

**Параметры**:

- `value` (Any, optional): Значение, которое можно передать в словаре `kwargs` через ключ `available_for_order`. Если `value` передано, его значение будет установлено в поле `ProductFields.available_for_order`.

**Как работает функция**:

1. Пытается получить значение статуса "доступно для заказа" через `execute_locator`.
2. Если значение получено, оно устанавливается в поле `ProductFields.available_for_order`.
3. Если поле не заполнено, логируется ошибка.

**Примеры**:

```python
await graber.available_for_order(value='1')
```

### `available_later`

```python
    @close_pop_up()
    async def available_later(self, value:Optional[Any] = None):
        """Fetch and set available later status.

        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {available_later = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле