# Модуль graber.py

## Обзор

Модуль `graber.py` предназначен для сбора информации о товарах с веб-страниц поставщиков. Он содержит базовый класс `Graber`, который использует веб-драйвер (класс `Driver`) для извлечения целевых полей, таких как название, описание, спецификация, артикул и цена, со страниц HTML. Расположение полей определяется локаторами, хранящимися в JSON-файлах в директории `locators` каждого поставщика.
Для нестандартной обработки полей товара можно переопределить функцию в своем классе.

## Оглавление

- [Классы](#классы)
  - [Context](#context)
  - [Graber](#graber)
- [Функции](#функции)
  - [close_pop_up](#close_pop_up)

## Подробнее

Модуль предоставляет базовый класс для сбора данных с веб-страниц поставщиков. Он использует веб-драйвер для сбора информации о товаре, определяя местоположение полей с помощью локаторов, хранящихся в JSON-файлах.

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
    ...
```

**Назначение**: Создает декоратор для закрытия всплывающих окон перед выполнением основной логики декорируемой функции.

**Параметры**:
- `value` (\'Driver\'): Дополнительное значение для декоратора.

**Возвращает**:
- `Callable`: Декоратор, оборачивающий функцию.

**Как работает функция**:
Функция `close_pop_up` является декоратором, который оборачивает другую функцию. Перед выполнением обернутой функции, декоратор проверяет, установлен ли `Context.locator_for_decorator`. Если он установлен, декоратор пытается выполнить локатор, чтобы закрыть всплывающее окно. После этого `Context.locator_for_decorator` сбрасывается, чтобы декоратор не срабатывал повторно.

## Классы

### `Context`

```python
class Context:
    """
    Класс для хранения глобальных настроек.

    Attributes:
        driver (Optional[\'Driver\']): Объект драйвера, используется для управления браузером или другим интерфейсом.
        locator_for_decorator (Optional[SimpleNamespace]): Если будет установлен - выполнится декоратор `@close_pop_up`.
            Устанавливается при инициализации поставщика, например: `Context.locator = self.locator.close_pop_up`.
        supplier_prefix (Optional[str]): Префикс поставщика.

    Example:
        >>> context = Context()
        >>> context.supplier_prefix = \'prefix\'
        >>> print(context.supplier_prefix)
        prefix
    """

    # Аттрибуты класса
    driver: Optional[\'Driver\'] = None
    locator_for_decorator: Optional[SimpleNamespace] = None  # <- Если будет установлен - выполнится декоратор `@close_pop_up`. Устанавливается при инициализации поставщика, например: `Context.locator = self.locator.close_pop_up`
    supplier_prefix: Optional[str] = None
```

**Описание**: Класс `Context` используется для хранения глобальных настроек, таких как драйвер, локатор для декоратора `@close_pop_up` и префикс поставщика.

**Атрибуты**:
- `driver` (Optional['Driver']): Объект драйвера для управления браузером.
- `locator_for_decorator` (Optional[SimpleNamespace]): Локатор для декоратора `@close_pop_up`.
- `supplier_prefix` (Optional[str]): Префикс поставщика.

**Принцип работы**:
Класс `Context` предоставляет централизованное место для хранения глобальных настроек, которые могут использоваться различными частями приложения. Это позволяет избежать передачи одних и тех же параметров между функциями и классами.

### `Graber`

```python
class Graber:
    """Базовый класс сбора данных со страницы для всех поставщиков."""
    
    def __init__(self, supplier_prefix: str, lang_index:int, driver: 'Driver'):
        """Инициализация класса Graber.

        Args:
            supplier_prefix (str): Префикс поставщика.
            driver (\'Driver\'): Экземпляр класса Driver.
        """
        self.supplier_prefix = supplier_prefix
        self.locator: SimpleNamespace = j_loads_ns(gs.path.src / \'suppliers\' / supplier_prefix / \'locators\' / \'product.json\')
        self.driver = driver
        self.fields: ProductFields = ProductFields(lang_index) # <- установка базового языка. Тип - `int`
        Context.driver = self.driver
        Context.supplier_prefix = None
        Context.locator_for_decorator = None
        """Если будет установлен локатор в Context.locator_for_decorator - выполнится декоратор `@close_pop_up`"""
```

**Описание**: Базовый класс `Graber` предназначен для сбора данных о товарах с веб-страниц поставщиков.

**Атрибуты**:
- `supplier_prefix` (str): Префикс поставщика.
- `locator` (SimpleNamespace): Локаторы элементов страницы.
- `driver` ('Driver'): Экземпляр класса `Driver` для управления браузером.
- `fields` (ProductFields): Объект для хранения полей продукта.

**Параметры**:
- `supplier_prefix` (str): Префикс поставщика.
- `driver` ('Driver'): Экземпляр класса `Driver`.

**Принцип работы**:
Класс `Graber` инициализируется с префиксом поставщика и экземпляром драйвера. Он загружает локаторы элементов страницы из JSON-файла и создает объект `ProductFields` для хранения данных о товаре.

**Методы**:

- `error(self, field: str)`: Обработчик ошибок для полей.
- `set_field_value(self, value: Any, locator_func: Callable[[], Any], field_name: str, default: Any = '') -> Any`: Универсальная функция для установки значений полей с обработкой ошибок.
- `grab_page(self, *args, **kwards) -> ProductFields`: Синхронная функция для сбора полей продукта.
- `grab_page_async(self, *args, **kwards) -> ProductFields`: Асинхронная функция для сбора полей продукта.
- `additional_shipping_cost(self, value: Optional[Any] = None)`: Извлекает и устанавливает дополнительную стоимость доставки.
- `delivery_in_stock(self, value: Optional[Any] = None)`: Извлекает и устанавливает статус доставки в наличии.
- `active(self, value: Optional[Any] = None)`: Извлекает и устанавливает статус активности.
- `additional_delivery_times(self, value: Optional[Any] = None)`: Извлекает и устанавливает дополнительное время доставки.
- `advanced_stock_management(self, value: Optional[Any] = None)`: Извлекает и устанавливает статус расширенного управления запасами.
- `affiliate_short_link(self, value: Optional[Any] = None)`: Извлекает и устанавливает короткую ссылку аффилиата.
- `affiliate_summary(self, value: Optional[Any] = None)`: Извлекает и устанавливает сводку аффилиата.
- `affiliate_summary_2(self, value: Optional[Any] = None)`: Извлекает и устанавливает сводку аффилиата 2.
- `affiliate_text(self, value: Optional[Any] = None)`: Извлекает и устанавливает текст аффилиата.
- `affiliate_image_large(self, value: Optional[Any] = None)`: Извлекает и устанавливает большое изображение аффилиата.
- `affiliate_image_medium(self, value: Optional[Any] = None)`: Извлекает и устанавливает среднее изображение аффилиата.
- `affiliate_image_small(self, value: Optional[Any] = None)`: Извлекает и устанавливает маленькое изображение аффилиата.
- `available_date(self, value: Optional[Any] = None)`: Извлекает и устанавливает доступную дату.
- `available_for_order(self, value: Optional[Any] = None)`: Извлекает и устанавливает статус доступности для заказа.
- `available_later(self, value: Optional[Any] = None)`: Извлекает и устанавливает статус доступности позже.
- `available_now(self, value: Optional[Any] = None)`: Извлекает и устанавливает статус доступности сейчас.
- `additional_categories(self, value: str | list = None) -> dict`: Устанавливает дополнительные категории.
- `cache_default_attribute(self, value: Optional[Any] = None)`: Извлекает и устанавливает атрибут кэша по умолчанию.
- `cache_has_attachments(self, value: Optional[Any] = None)`: Извлекает и устанавливает статус наличия вложений в кэше.
- `cache_is_pack(self, value: Optional[Any] = None)`: Извлекает и устанавливает статус упаковки в кэше.
- `condition(self, value: Optional[Any] = None)`: Извлекает и устанавливает условие продукта.
- `customizable(self, value: Optional[Any] = None)`: Извлекает и устанавливает статус настройки.
- `date_add(self, value: Optional[str  |  datetime.date] = None)`: Извлекает и устанавливает дату добавления.
- `date_upd(self, value: Optional[Any] = None)`: Извлекает и устанавливает дату обновления.
- `delivery_out_stock(self, value: Optional[Any] = None)`: Извлекает и устанавливает доставку вне склада.
- `depth(self, value: Optional[Any] = None)`: Извлекает и устанавливает глубину.
- `description(self, value: Optional[Any] = None)`: Извлекает и устанавливает описание.
- `description_short(self, value: Optional[Any] = None)`: Извлекает и устанавливает краткое описание.
- `id_category_default(self, value: Optional[Any] = None)`: Извлекает и устанавливает ID категории по умолчанию.
- `id_default_combination(self, value: Optional[Any] = None)`: Извлекает и устанавливает ID комбинации по умолчанию.
- `id_product(self, value: Optional[Any] = None)`: Извлекает и устанавливает ID продукта.
- `locale(self, value: Optional[Any] = None)`: Извлекает и устанавливает локаль.
- `id_default_image(self, value: Optional[Any] = None)`: Извлекает и устанавливает ID изображения по умолчанию.
- `ean13(self, value: Optional[Any] = None)`: Извлекает и устанавливает код EAN13.
- `ecotax(self, value: Optional[Any] = None)`: Извлекает и устанавливает ecotax.
- `height(self, value: Optional[Any] = None)`: Извлекает и устанавливает высоту.
- `how_to_use(self, value: Optional[Any] = None)`: Извлекает и устанавливает "как использовать".
- `id_manufacturer(self, value: Optional[Any] = None)`: Извлекает и устанавливает ID производителя.
- `id_supplier(self, value: Optional[Any] = None)`: Извлекает и устанавливает ID поставщика.
- `id_tax(self, value: Optional[Any] = None)`: Извлекает и устанавливает ID налога.
- `id_type_redirected(self, value: Optional[Any] = None)`: Извлекает и устанавливает ID перенаправленного типа.
- `images_urls(self, value: Optional[Any] = None)`: Извлекает и устанавливает URL-адреса изображений.
- `indexed(self, value: Optional[Any] = None)`: Извлекает и устанавливает статус индексации.
- `ingredients(self, value: Optional[Any] = None)`: Извлекает и устанавливает ингредиенты.
- `meta_description(self, value: Optional[Any] = None)`: Извлекает и устанавливает мета-описание.
- `meta_keywords(self, value: Optional[Any] = None)`: Извлекает и устанавливает мета-ключевые слова.
- `meta_title(self, value: Optional[Any] = None)`: Извлекает и устанавливает мета-заголовок.
- `is_virtual(self, value: Optional[Any] = None)`: Извлекает и устанавливает виртуальный статус.
- `isbn(self, value: Optional[Any] = None)`: Извлекает и устанавливает ISBN.
- `link_rewrite(self, value: Optional[Any] = None)`: Извлекает и устанавливает перезапись ссылки.
- `location(self, value: Optional[Any] = None)`: Извлекает и устанавливает местоположение.
- `low_stock_alert(self, value: Optional[Any] = None)`: Извлекает и устанавливает оповещение о низком запасе.
- `low_stock_threshold(self, value: Optional[Any] = None)`: Извлекает и устанавливает порог низкого запаса.
- `minimal_quantity(self, value: Optional[Any] = None)`: Извлекает и устанавливает минимальное количество.
- `mpn(self, value: Optional[Any] = None)`: Извлекает и устанавливает MPN (номер детали производителя).
- `name(self, value: Optional[Any] = None)`: Извлекает и устанавливает название продукта.
- `online_only(self, value: Optional[Any] = None)`: Извлекает и устанавливает статус "только онлайн".
- `on_sale(self, value: Optional[Any] = None)`: Извлекает и устанавливает статус "в продаже".
- `out_of_stock(self, value: Optional[Any] = None)`: Извлекает и устанавливает статус "нет в наличии".
- `pack_stock_type(self, value: Optional[Any] = None)`: Извлекает и устанавливает тип запаса пакета.
- `price(self, value: Optional[Any] = None)`: Извлекает и устанавливает цену.
- `product_type(self, value: Optional[Any] = None)`: Извлекает и устанавливает тип продукта.
- `quantity(self, value: Optional[Any] = None)`: Извлекает и устанавливает количество.
- `quantity_discount(self, value: Optional[Any] = None)`: Извлекает и устанавливает скидку за количество.
- `redirect_type(self, value: Optional[Any] = None)`: Извлекает и устанавливает тип перенаправления.
- `reference(self, value: Optional[Any] = None)`: Извлекает и устанавливает ссылку.
- `show_condition(self, value: Optional[int] = None)`: Извлекает и устанавливает отображение условия.
- `show_price(self, value: Optional[int] = None)`: Извлекает и устанавливает отображение цены.
- `state(self, value: Optional[Any] = None)`: Извлекает и устанавливает состояние.
- `text_fields(self, value: Optional[Any] = None)`: Извлекает и устанавливает текстовые поля.
- `unit_price_ratio(self, value: Optional[Any] = None)`: Извлекает и устанавливает коэффициент цены за единицу.
- `unity(self, value: Optional[str] = None)`: Извлекает и устанавливает единство.
- `upc(self, value: Optional[str] = None)`: Извлекает и устанавливает UPC.
- `uploadable_files(self, value: Optional[Any] = None)`: Извлекает и устанавливает загружаемые файлы.
- `default_image_url(self, value: Optional[Any] = None)`: Извлекает и устанавливает URL изображения по умолчанию.
- `visibility(self, value: Optional[str] = None)`: Извлекает и устанавливает видимость.
- `weight(self, value: Optional[float] = None)`: Извлекает и устанавливает вес.
- `wholesale_price(self, value: Optional[float] = None)`: Извлекает и устанавливает оптовую цену.
- `width(self, value: Optional[float] = None)`: Извлекает и устанавливает ширину.
- `specification(self, value: Optional[str | list] = None)`: Извлекает и устанавливает спецификацию.
- `link(self, value: Optional[str] = None)`: Извлекает и устанавливает ссылку.
- `byer_protection(self, value: Optional[str | list] = None)`: Извлекает и устанавливает защиту покупателя.
- `customer_reviews(self, value: Optional[Any] = None)`: Извлекает и устанавливает отзывы клиентов.
- `link_to_video(self, value: Optional[Any] = None)`: Извлекает и устанавливает ссылку на видео.
- `local_image_path(self, value: Optional[str] = None)`: Извлекает и сохраняет изображение локально.
- `local_video_path(self, value: Optional[Any] = None)`: Извлекает и сохраняет видео локально.

### `__init__`

```python
def __init__(self, supplier_prefix: str, lang_index:int, driver: 'Driver'):
    """Инициализация класса Graber.

    Args:
        supplier_prefix (str): Префикс поставщика.
        driver (\'Driver\'): Экземпляр класса Driver.
    """
    self.supplier_prefix = supplier_prefix
    self.locator: SimpleNamespace = j_loads_ns(gs.path.src / 'suppliers' / supplier_prefix / 'locators' / 'product.json')
    self.driver = driver
    self.fields: ProductFields = ProductFields(lang_index) # <- установка базового языка. Тип - `int`
    Context.driver = self.driver
    Context.supplier_prefix = None
    Context.locator_for_decorator = None
    """Если будет установлен локатор в Context.locator_for_decorator - выполнится декоратор `@close_pop_up`"""
```

**Назначение**: Инициализация экземпляра класса `Graber`.

**Параметры**:
- `supplier_prefix` (str): Префикс поставщика.
- `lang_index` (int): Индекс языка.
- `driver` ('Driver'): Экземпляр класса `Driver`.

**Как работает функция**:
Конструктор класса `Graber` принимает префикс поставщика, индекс языка и экземпляр драйвера. Он загружает локаторы элементов страницы из JSON-файла, создает объект `ProductFields` для хранения данных о товаре и устанавливает глобальные настройки в классе `Context`.

### `error`

```python
async def error(self, field: str):
    """Обработчик ошибок для полей."""
    logger.debug(f"Ошибка заполнения поля {field}")
```

**Назначение**: Обработчик ошибок для полей.

**Параметры**:
- `field` (str): Название поля, для которого произошла ошибка.

**Как работает функция**:
Функция `error` записывает сообщение об ошибке в лог с указанием названия поля, для которого произошла ошибка.

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
    locator_result = await asyncio.to_thread(locator_func)
    if value:
        return value
    if locator_result:
        return locator_result
    await self.error(field_name)
    return default
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
Функция `set_field_value` пытается установить значение поля, используя переданные параметры. Если передано значение `value`, оно устанавливается. В противном случае, функция пытается получить значение из локатора с помощью функции `locator_func`. Если значение получено, оно устанавливается. Если ни значение `value`, ни значение из локатора не получены, записывается сообщение об ошибке в лог и устанавливается значение по умолчанию.

### `grab_page`

```python
def grab_page(self, *args, **kwards) -> ProductFields:
    return asyncio.run(self.grab_page_async(*args, **kwards))
```

**Назначение**: Синхронная функция для сбора полей продукта.

**Параметры**:
- `*args`: Аргументы, передаваемые в `grab_page_async`.
- `**kwargs`: Ключевые аргументы, передаваемые в `grab_page_async`.

**Возвращает**:
- `ProductFields`: Объект `ProductFields` с собранными данными.

**Как работает функция**:
Функция `grab_page` является синхронной оберткой для асинхронной функции `grab_page_async`. Она запускает асинхронную функцию и возвращает результат.

### `grab_page_async`

```python
async def grab_page_async(self, *args, **kwards) -> ProductFields:
    """Асинхронная функция для сбора полей продукта."""
    async def fetch_all_data(*args, **kwards):
        # Динамическое вызовы функций для каждого поля из args
        if not args: # по какой то причини не были переданы имена полей для сбора информации
            args:list = ['id_product', 'name', 'description_short', 'description', 'specification', 'local_image_path']
        for filed_name in args:
            function = getattr(self, filed_name, None)
            if function:
                await function(kwards.get(filed_name, '')) # Просто вызываем с await, так как все функции асинхронные

    await fetch_all_data(*args, **kwards)
    return self.fields
```

**Назначение**: Асинхронная функция для сбора полей продукта.

**Параметры**:
- `*args`: Список полей, которые необходимо собрать. Если не переданы, используются значения по умолчанию (`id_product`, `name`, `description_short`, `description`, `specification`, `local_image_path`).
- `**kwargs`: Ключевые аргументы, содержащие значения для установки полей.

**Возвращает**:
- `ProductFields`: Объект `ProductFields` с собранными данными.

**Как работает функция**:
Функция `grab_page_async` выполняет сбор данных о продукте асинхронно. Она динамически вызывает функции для каждого поля, указанного в `args`, и устанавливает значения полей, используя данные из `kwargs`.

**Внутренние функции**:
- `fetch_all_data(*args, **kwards)`: Асинхронная функция, которая динамически вызывает функции для каждого поля из `args`. Если `args` пустой, то устанавливаются значения по умолчанию.

### `additional_shipping_cost`

```python
@close_pop_up()
async def additional_shipping_cost(self, value:Optional[Any] = None):
    """Fetch and set additional shipping cost.
    Args:
    value (Any): это значение можно передать в словаре kwards чеез ключ {additional_shipping_cost = `value`} при определении класса
    если `value` был передан - его значение подставляется в поле `ProductFields.additional_shipping_cost
    """
    try:
        # Получаем значение через execute_locator
        self.fields.additional_shipping_cost = normalize_string(value or  await self.driver.execute_locator(self.locator.additional_shipping_cost) or '')
        if not  self.fields.additional_shipping_cost:
            logger.error(f"Поле `additional_shipping_cost` не получиле значения")
            return

        return True
    except Exception as ex:
        logger.error(f"Ошибка получения значения в поле `additional_shipping_cost`", ex)
        ...
        return
```

**Назначение**: Извлечение и установка дополнительной стоимости доставки.

**Параметры**:
- `value` (Any, optional): Значение, которое можно передать через словарь `kwargs` с ключом `additional_shipping_cost`.

**Как работает функция**:
Функция `additional_shipping_cost` пытается получить и установить значение дополнительной стоимости доставки. Если `value` передан, то нормализуется и присваивается полю `ProductFields.additional_shipping_cost`. Если `value` не передан, то пытается получить значение через `execute_locator` из `self.locator.additional_shipping_cost`, нормализует его и присваивает полю `ProductFields.additional_shipping_cost`.

### `delivery_in_stock`

```python
@close_pop_up()
async def delivery_in_stock(self, value:Optional[Any] = None):
    """Fetch and set delivery in stock status.
    
    Args:
    value (Any): это значение можно передать в словаре kwargs через ключ {delivery_in_stock = `value`} при определении класса.
    Если `value` был передан, его значение подставляется в поле `ProductFields.delivery_in_stock`.\n
    """
    try:
        # Получаем значение через execute_locator
        self.fields.delivery_in_stock = normalize_string( value or  await self.driver.execute_locator(self.locator.delivery_in_stock) or '' )
        if not  self.fields.delivery_in_stock:
            logger.error(f"Поле `delivery_in_stock` не получиле значения")
            return
        return True
    except Exception as ex:
        logger.error(f"Ошибка получения значения в поле `delivery_in_stock`", ex)
        ...
        return
```

**Назначение**: Извлечение и установка статуса доставки в наличии.

**Параметры**:
- `value` (Any, optional): Значение, которое можно передать через словарь `kwargs` с ключом `delivery_in_stock`.

**Как работает функция**:
Функция `delivery_in_stock` пытается получить и установить статус доставки в наличии. Если `value` передан, то нормализуется и присваивается полю `ProductFields.delivery_in_stock`. Если `value` не передан, то пытается получить значение через `execute_locator` из `self.locator.delivery_in_stock`, нормализует его и присваивает полю `ProductFields.delivery_in_stock`.

### `active`

```python
@close_pop_up()
async def active(self, value:Optional[Any] = None):
    """Fetch and set active status.
    
    Args:
    value (Any): это значение можно передать в словаре kwargs через ключ {active = `value`} при определении класса.
    Если `value` был передан, его значение подставляется в поле `ProductFields.active`.
    Принимаемое значениеЬ 1/0\n
    """
    try:
        # Получаем значение через execute_locator
        self.fields.active = normalize_int( value or  await self.driver.execute_locator(self.locator.active) or 1)
        if not self.fields.active:
            return
    except Exception as ex:
        logger.error(f"Ошибка получения значения в поле `active`", ex)
        ...
        return
    
    # Проверка валидности `value`
    if not value:
        logger.debug(f"Невалидный результат {value=}\\nлокатор {self.locator.active}")
        ...
        return

    # Записываем результат в поле `active` объекта `ProductFields`
    self.fields.active = value
    return True
```

**Назначение**: Извлечение и установка статуса активности товара.

**Параметры**:
- `value` (Any, optional): Значение, которое можно передать через словарь `kwargs` с ключом `active`.

**Как работает функция**:
Функция `active` пытается получить и установить статус активности товара. Если `value` передан, то нормализуется как целое число и присваивается полю `ProductFields.active`. Если `value` не передан, то пытается получить значение через `execute_locator` из `self.locator.active`, нормализует его как целое число и присваивает полю `ProductFields.active`.

### `additional_delivery_times`

```python
@close_pop_up()
async def additional_delivery_times(self, value:Optional[Any] = None):
    """Fetch and set additional delivery times.
    
    Args:
    value (Any): это значение можно передать в словаре kwargs через ключ {additional_delivery_times = `value`} при определении класса.
    Если `value` был передан, его значение подставляется в поле `ProductFields.additional_delivery_times`.\n
    """
    try:
        # Получаем значение через execute_locator
        value = value or  await self.driver.execute_locator(self.locator.additional_delivery_times) or ''
    except Exception as ex:
        logger.error(f"Ошибка получения значения в поле `additional_delivery_times`", ex)
        ...
        return
    
    # Проверка валидности `value`
    if not value:
        logger.debug(f"Невалидный результат {value=}\\nлокатор {self.locator.additional_delivery_times}")
        ...
        return

    # Записываем результат в поле `additional_delivery_times` объекта `ProductFields`
    self.fields.additional_delivery_times = value
    return True
```

**Назначение**: Извлечение и установка дополнительного времени доставки.

**Параметры**:
- `value` (Any, optional): Значение, которое можно передать через словарь `kwargs` с ключом `additional_delivery_times`.

**Как работает функция**:
Функция `additional_delivery_times` пытается получить и установить дополнительное время доставки. Если `value` передан, то присваивается полю `ProductFields.additional_delivery_times`. Если `value` не передан, то пытается получить значение через `execute_locator` из `self.locator.additional_delivery_times` и присваивает полю `ProductFields.additional_delivery_times`.

### `advanced_stock_management`

```python
@close_pop_up()
async def advanced_stock_management(self, value:Optional[Any] = None):
    """Fetch and set advanced stock management status.
    
    Args:
    value (Any): это значение можно передать в словаре kwargs через ключ {advanced_stock_management = `value`} при определении класса.
    Если `value` был передан, его значение подставляется в поле `ProductFields.advanced_stock_management`.\n
    """
    try:
        # Получаем значение через execute_locator
        value = value or  await self.driver.execute_locator(self.locator.advanced_stock_management) or ''
    except Exception as ex:
        logger.error(f"Ошибка получения значения в поле `advanced_stock_management`", ex)
        ...
        return
    
    # Проверка валидности `value`
    if not value:
        logger.debug(f"Невалидный результат {value=}\\nлокатор {self.locator.advanced_stock_management}")
        ...
        return

    # Записываем результат в поле `advanced_stock_management` объекта `ProductFields`
    self.fields.advanced_stock_management = value
    return True
```

**Назначение**: Извлечение и установка статуса расширенного управления запасами.

**Параметры**:
- `value` (Any, optional): Значение, которое можно передать через словарь `kwargs` с ключом `advanced_stock_management`.

**Как работает функция**:
Функция `advanced_stock_management` пытается получить и установить статус расширенного управления запасами. Если `value` передан, то присваивается полю `ProductFields.advanced_stock_management`. Если `value` не передан, то пытается получить значение через `execute_locator` из `self.locator.advanced_stock_management` и присваивает полю `ProductFields.advanced_stock_management`.

### `affiliate_short_link`

```python
@close_pop_up()
async def affiliate_short_link(self, value:Optional[Any] = None):
    """Fetch and set affiliate short link.
    
    Args:
    value (Any): это значение можно передать в словаре kwargs через ключ {affiliate_short_link = `value`} при определении класса.
    Если `value` был передан, его значение подставляется в поле `ProductFields.affiliate_short_link`.\n
    """
    try:
        # Получаем значение через execute_locator
        self.fields.affiliate_short_link = value or  await self.driver.execute_locator(self.locator.affiliate_short_link) or ''
        return True
    except Exception as ex:
        logger.error(f"Ошибка получения значения в поле `affiliate_short_link`", ex)
        ...
        return
```

**Назначение**: Извлечение и установка короткой ссылки аффилиата.

**Параметры**:
- `value` (Any, optional): Значение, которое можно передать через словарь `kwargs` с ключом `affiliate_short_link`.

**Как работает функция**:
Функция `aff