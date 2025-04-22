# Модуль graber.py

## Обзор

Модуль `graber.py` предназначен для сбора информации о товарах с веб-страниц поставщиков. Он содержит базовый класс `Graber`, который использует веб-драйвер для извлечения целевых полей, таких как название, описание, спецификация, артикул и цена. Расположение полей определяется локаторами, хранящимися в JSON-файлах в директории `locators` каждого поставщика. Модуль предоставляет возможность переопределения функций для нестандартной обработки полей товара.

## Подробней

Модуль предназначен для автоматизации процесса сбора данных о товарах с веб-страниц различных поставщиков. Он использует веб-драйвер для навигации по страницам и извлечения необходимой информации на основе локаторов, определенных в JSON-файлах.

## Классы

### `Config`

**Описание**: Класс для хранения глобальных настроек, таких как объект драйвера, локатор для декоратора и префикс поставщика.

**Атрибуты**:

-   `locator_for_decorator` (Optional[`SimpleNamespace`]): Локатор для декоратора `@close_pop_up`.
-   `supplier_prefix` (Optional[str]): Префикс поставщика.
-   `driver` (\`Driver\`): Экземпляр класса `Driver`.

### `Graber`

**Описание**: Базовый класс для сбора данных со страницы для всех поставщиков.

**Методы**:

-   `__init__(supplier_prefix: str, driver: Optional['Driver'] = None, lang_index: Optional[int] = 2)`: Инициализация класса `Graber`.
-   `yield_scenarios_for_supplier(supplier_prefix: str, input_scenarios: Optional[List[Dict[str, Any]] | Dict[str, Any]] = None) -> Generator[Dict[str, Any], None, None]`: Генератор сценариев для поставщика.
-   `process_supplier_scenarios_async(supplier_prefix: str, input_scenarios=None, id_lang: Optional[int] = 1) -> bool`: Метод для обработки сценариев поставщика.
-   `process_scenarios(supplier_prefix: str, input_scenarios: List[Dict[str, Any]] | Dict[str, Any], id_lang: Optional[int] = 1) -> Optional[List[Any]]`: Выполняет один или несколько сценариев для указанного поставщика.
-   `set_field_value(value: Any, locator_func: Callable[[], Any], field_name: str, default: Any = '') -> Any`: Универсальная функция для установки значений полей с обработкой ошибок.
-   `grab_page(self, *args, **kwards) -> ProductFields`: Запускает асинхронную функцию `grab_page_async`.
-   `grab_page_async(self, *args, **kwards) -> ProductFields`: Асинхронная функция для сбора полей товара.
-   `error(self, field: str)`: Обработчик ошибок для полей.
-   `additional_shipping_cost(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает дополнительную стоимость доставки.
-   `delivery_in_stock(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает статус наличия на складе.
-   `active(self, value:bool = True) -> bool`: Извлекает и устанавливает статус активности.
-   `additional_delivery_times(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает дополнительное время доставки.
-   `advanced_stock_management(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает статус расширенного управления запасами (DEPRECATED).
-   `affiliate_short_link(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает короткую ссылку филиала.
-   `affiliate_summary(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает сводку филиала.
-   `affiliate_summary_2(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает сводку филиала 2.
-   `affiliate_text(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает текст филиала.
-   `affiliate_image_large(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает большое изображение филиала.
-   `affiliate_image_medium(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает среднее изображение филиала.
-   `affiliate_image_small(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает маленькое изображение филиала.
-   `available_date(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает доступную дату.
-   `available_for_order(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает статус доступности для заказа.
-   `available_later(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает статус доступности позже.
-   `available_now(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает статус доступности сейчас.
-   `additional_categories(self, value: str | list = None) -> dict`: Устанавливает дополнительные категории.
-   `cache_default_attribute(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает атрибут кэша по умолчанию.
-   `cache_has_attachments(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает статус наличия вложений в кэше.
-   `cache_is_pack(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает статус кэша (является ли пакетом).
-   `condition(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает условие товара.
-   `customizable(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает статус настраиваемости.
-   `date_add(self, value:Optional[str | datetime.date] = None) -> bool`: Извлекает и устанавливает дату добавления.
-   `date_upd(self, value:Optional[str | datetime.date] = None) -> bool`: Извлекает и устанавливает дату обновления.
-   `delivery_out_stock(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает доставку вне склада.
-   `depth(self, value:Optional[float] = None) -> bool`: Извлекает и устанавливает глубину.
-   `description(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает описание.
-   `description_short(self, value:Optional[str] = '') -> bool`: Извлекает и устанавливает краткое описание.
-   `id_category_default(self, value:int) -> bool`: Извлекает и устанавливает ID категории по умолчанию.
-   `id_default_combination(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает ID комбинации по умолчанию.
-   `id_product(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает ID товара.
-   `locale(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает локаль.
-   `id_default_image(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает ID изображения по умолчанию.
-   `ean13(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает код EAN13.
-   `ecotax(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает ecotax.
-   `height(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает высоту.
-   `how_to_use(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает как использовать.
-   `id_manufacturer(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает ID производителя.
-   `id_supplier(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает ID поставщика.
-   `id_tax_rules_group(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает ID налога.
-   `id_type_redirected(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает ID перенаправленного типа.
-   `images_urls(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает URL изображений.
-   `indexed(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает статус индексации.
-   `ingredients(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает ингредиенты.
-   `meta_description(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает мета-описание.
-   `meta_keywords(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает мета-ключевые слова.
-   `meta_title(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает мета-заголовок.
-   `is_virtual(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает виртуальный статус.
-   `isbn(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает ISBN.
-   `link_rewrite(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает перезапись ссылки.
-   `location(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает местоположение.
-   `low_stock_alert(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает оповещение о низком уровне запасов.
-   `low_stock_threshold(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает порог низкого уровня запасов.
-   `minimal_quantity(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает минимальное количество.
-   `mpn(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает MPN (номер детали производителя).
-   `name(self, value:Optional[str] = '') -> bool`: Извлекает и устанавливает наименование товара.
-   `online_only(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает статус "только онлайн".
-   `on_sale(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает статус "в продаже".
-   `out_of_stock(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает статус "нет в наличии".
-   `pack_stock_type(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает тип запаса пакета.
-   `price(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает цену.
-   `product_type(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает тип товара.
-   `quantity(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает количество.
-   `quantity_discount(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает скидку за количество.
-   `redirect_type(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает тип перенаправления.
-   `reference(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает ссылку.
-   `show_condition(self, value:Optional[int] = None) -> bool`: Извлекает и устанавливает условие отображения.
-   `show_price(self, value:Optional[int] = None) -> bool`: Извлекает и устанавливает отображение цены.
-   `state(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает состояние.
-   `text_fields(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает текстовые поля.
-   `unit_price_ratio(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает коэффициент цены за единицу.
-   `unity(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает единство.
-   `upc(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает UPC.
-   `uploadable_files(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает загружаемые файлы.
-   `default_image_url(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает URL изображения по умолчанию.
-   `visibility(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает видимость.
-   `weight(self, value:Optional[float] = None) -> bool`: Извлекает и устанавливает вес.
-   `wholesale_price(self, value:Optional[float] = None) -> bool`: Извлекает и устанавливает оптовую цену.
-   `width(self, value:Optional[float] = None) -> bool`: Извлекает и устанавливает ширину.
-   `specification(self, value:Optional[str|list] = None) -> bool`: Извлекает и устанавливает спецификацию.
-   `link(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает ссылку.
    `byer_protection(self, value:Optional[str] = None) -> bool`: Извлекает и устанавливает защиту покупателя.
-   `customer_reviews(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает отзывы клиентов.
-   `link_to_video(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает ссылку на видео.
-   `local_image_path(self, value: Optional[str] = None) -> bool`: Сохраняет изображение локально и устанавливает путь.
-   `local_video_path(self, value:Optional[Any] = None) -> bool`: Извлекает и устанавливает локальный путь к видео.

## Функции

### `close_pop_up()`

**Назначение**: Создает декоратор для закрытия всплывающих окон перед выполнением основной логики функции.

**Параметры**:

-   `value` (\`Driver\`): Дополнительное значение для декоратора.

**Возвращает**:

-   `Callable`: Декоратор, оборачивающий функцию.

**Как работает функция**:

Функция `close_pop_up()` создает декоратор, который закрывает всплывающие окна перед выполнением основной логики декорируемой функции. Декоратор проверяет, установлен ли локатор для закрытия всплывающего окна в `Config.locator_for_decorator`. Если локатор установлен, декоратор пытается выполнить локатор с помощью `Config.driver.execute_locator()`. В случае успеха, всплывающее окно закрывается, и выполняется основная логика функции. Если локатор не установлен, основная логика функции выполняется без закрытия всплывающего окна.

**Примеры**:

```python
@close_pop_up()
async def some_function(self, param: str) -> bool:
    ...
```

### `Graber.__init__`

**Назначение**: Инициализация класса `Graber`.

**Параметры**:

-   `supplier_prefix` (str): Префикс поставщика.
-   `driver` (\`Driver\`, optional): Экземпляр класса `Driver`. По умолчанию `None`.
-   `lang_index` (Optional[int], optional): Индекс языка. По умолчанию `2`.

**Как работает функция**:

Функция инициализирует экземпляр класса `Graber`, устанавливая префикс поставщика, загружая локаторы для товаров и категорий из JSON-файлов, создавая экземпляр класса `Driver` (если не передан) и устанавливая базовый язык для полей товара. Также устанавливает конфигурацию для декоратора `@close_pop_up`.

**Примеры**:

```python
graber = Graber(supplier_prefix='some_supplier', driver=Driver(Chrome))
```

### `Graber.yield_scenarios_for_supplier`

**Назначение**: Генератор, который выдает (yields) словари сценариев для поставщика.

**Параметры**:

-   `supplier_prefix` (str): Префикс (идентификатор) поставщика.
-   `input_scenarios` (Optional[List[Dict[str, Any]] | Dict[str, Any]]): Непосредственно переданные сценарии (один словарь или список словарей).

**Возвращает**:

-   `Generator[Dict[str, Any], None, None]`: Генератор, возвращающий словари сценариев по одному.

**Как работает функция**:

Сначала функция обрабатывает сценарии, переданные в `input_scenarios`. Если `input_scenarios` пуст или `None`, функция ищет и загружает `.json` файлы из директории сценариев поставщика.

**Примеры**:

```python
for scenario in grabber.yield_scenarios_for_supplier(supplier_prefix='some_supplier', input_scenarios=[{'url': 'http://example.com'}])
    ...
```

### `Graber.process_supplier_scenarios_async`

**Назначение**: Метод для обработки сценариев поставщика.

**Параметры**:

-   `supplier_prefix` (str): Префикс (идентификатор) поставщика.
-   `input_scenarios`: Сценарии, переданные для обработки.
-    `id_lang` (Optional[int], optional): ID языка. По умолчанию `1`.

**Возвращает**:

-   `bool`: Результат выполнения сценариев.

**Как работает функция**:

Функция использует генератор `yield_scenarios_for_supplier` для получения сценариев и вызывает `process_scenarios` для каждого сценария.

**Примеры**:

```python
result = await grabber.process_supplier_scenarios_async(supplier_prefix='some_supplier', input_scenarios=[{'url': 'http://example.com'}])
```

### `Graber.process_scenarios`

**Назначение**: Выполняет один или несколько сценариев для указанного поставщика.

**Параметры**:

-   `supplier_prefix` (str): Префикс (идентификатор) поставщика.
-   `input_scenarios` (List[Dict[str, Any]] | Dict[str, Any]): Данные сценариев: либо список словарей сценариев, либо словарь вида `{'scenarios': {'name': dict, ...}}`.
-    `id_lang` (Optional[int], optional): ID языка. По умолчанию `1`.

**Возвращает**:

-   `Optional[List[Any]]`: Список результатов выполнения каждого сценария (например, списки обработанных URL товаров) или `None` в случае критической ошибки.

**Как работает функция**:

Функция нормализует входные данные, динамически импортирует модуль сценария и выполняет сценарии, извлекая URL товаров и собирая данные о товарах.

**Примеры**:

```python
result = await grabber.process_scenarios(supplier_prefix='some_supplier', input_scenarios=[{'url': 'http://example.com'}])
```

### `Graber.set_field_value`

**Назначение**: Универсальная функция для установки значений полей с обработкой ошибок.

**Параметры**:

-   `value` (Any): Значение для установки.
-   `locator_func` (Callable[[], Any]): Функция для получения значения из локатора.
-   `field_name` (str): Название поля.
-   `default` (Any, optional): Значение по умолчанию. По умолчанию пустая строка.

**Возвращает**:

-   `Any`: Установленное значение.

**Как работает функция**:

Функция пытается получить значение из локатора с помощью `locator_func`. Если `value` передано, возвращается `value`. Если `locator_result` получено, возвращается `locator_result`. В противном случае вызывается `self.error` и возвращается `default`.

**Примеры**:

```python
value = await grabber.set_field_value(value='some_value', locator_func=lambda: 'locator_value', field_name='some_field', default='default_value')
```

### `Graber.grab_page`

**Назначение**: Запускает асинхронную функцию `grab_page_async`.

**Параметры**:

-   `*args`: Аргументы, передаваемые в `grab_page_async`.
-   `**kwards`: Ключевые аргументы, передаваемые в `grab_page_async`.

**Возвращает**:

-   `ProductFields`: Результат выполнения `grab_page_async`.

**Как работает функция**:

Функция запускает асинхронную функцию `grab_page_async` и возвращает результат ее выполнения.

**Примеры**:

```python
product_fields = grabber.grab_page(id_product='123', name='some_name')
```

### `Graber.grab_page_async`

**Назначение**: Асинхронная функция для сбора полей товара.

**Параметры**:

-   `*args`: Список полей для сбора.
-   `**kwards`: Ключевые аргументы.

**Возвращает**:

-   `ProductFields`: Объект `ProductFields` с собранными данными.

**Как работает функция**:

Функция динамически вызывает функции для каждого поля из `args` и собирает данные о товаре.

**Примеры**:

```python
product_fields = await grabber.grab_page_async(id_product='123', name='some_name')
```

### `Graber.error`

**Назначение**: Обработчик ошибок для полей.

**Параметры**:

-   `field` (str): Название поля.

**Как работает функция**:

Функция логирует ошибку заполнения поля.

**Примеры**:

```python
grabber.error(field='some_field')
```

### `Graber.additional_shipping_cost`

**Назначение**: Извлекает и устанавливает дополнительную стоимость доставки.

**Параметры**:

-   `value` (Any, optional): Значение, передаваемое через kwargs. По умолчанию `None`.

**Возвращает**:

-   `bool`: `True` в случае успеха, `None` в случае ошибки.

**Как работает функция**:

Функция пытается получить значение дополнительной стоимости доставки из локатора и нормализовать его. Если значение передано через `value`, используется оно.

**Примеры**:

```python
result = await grabber.additional_shipping_cost(value='10.00')
```

### `Graber.delivery_in_stock`

**Назначение**: Извлекает и устанавливает статус наличия на складе.

**Параметры**:

-   `value` (str, optional): Значение, передаваемое через kwargs. По умолчанию `None`.

**Возвращает**:

-   `bool`: `True` в случае успеха, `None` в случае ошибки.

**Как работает функция**:

Функция пытается получить статус наличия на складе из локатора и нормализовать его. Если значение передано через `value`, используется оно.

**Примеры**:

```python
result = await grabber.delivery_in_stock(value='В наличии')
```

### `Graber.active`

**Назначение**: Извлекает и устанавливает статус активности.

**Параметры**:

-   `value` (bool, optional): Значение, передаваемое через kwargs. По умолчанию `True`.

**Возвращает**:

-   `bool`: `True` в случае успеха, `None` в случае ошибки.

**Как работает функция**:

Функция пытается получить статус активности из локатора и нормализовать его. Если значение передано через `value`, используется оно.

**Примеры**:

```python
result = await grabber.active(value=False)
```

### `Graber.additional_delivery_times`

**Назначение**: Извлекает и устанавливает дополнительное время доставки.

**Параметры**:

-   `value` (str, optional): Значение, передаваемое через kwargs. По умолчанию `None`.

**Возвращает**:

-   `bool`: `True` в случае успеха, `None` в случае ошибки.

**Как работает функция**:

Функция пытается получить дополнительное время доставки из локатора. Если значение передано через `value`, используется оно.

**Примеры**:

```python
result = await grabber.additional_delivery_times(value='3-5 дней')
```

### `Graber.advanced_stock_management`

**Назначение**: Извлекает и устанавливает статус расширенного управления запасами (DEPRECATED).

**Параметры**:

-   `value` (Any, optional): Значение, передаваемое через kwargs. По умолчанию `None`.

**Возвращает**:

-   `bool`: Всегда `True`.

**Как работает функция**:

Функция всегда возвращает `True` и устанавливает значение в поле `advanced_stock_management`.

**Примеры**:

```python
result = await grabber.advanced_stock_management(value=True)
```

### `Graber.affiliate_short_link`

**Назначение**: Извлекает и устанавливает короткую ссылку филиала.

**Параметры**:

-   `value` (str, optional): Значение, передаваемое через kwargs. По умолчанию `None`.

**Возвращает**:

-   `bool`: `True` в случае успеха, `None` в случае ошибки.

**Как работает функция**:

Функция пытается получить короткую ссылку филиала из локатора. Если значение передано через `value`, используется оно.

**Примеры**:

```python
result = await grabber.affiliate_short_link(value='http://short.link')
```

### `Graber.affiliate_summary`

**Назначение**: Извлекает и устанавливает сводку филиала.

**Параметры**:

-   `value` (str, optional): Значение, передаваемое через kwargs. По умолчанию `None`.

**Возвращает**:

-   `bool`: `True` в случае успеха, `None` в случае ошибки.

**Как работает функция**:

Функция пытается получить сводку филиала из локатора и нормализовать ее. Если значение передано через `value`, используется оно.

**Примеры**:

```python
result = await grabber.affiliate_summary(value='Some summary')
```

### `Graber.affiliate_summary_2`

**Назначение**: Извлекает и устанавливает сводку филиала 2.

**Параметры**:

-   `value` (Any, optional): Значение, передаваемое через kwargs. По умолчанию `None`.

**Возвращает**:

-   `bool`: `True` в случае успеха, `None` в случае ошибки.

**Как работает функция**:

Функция пытается получить сводку филиала 2 из локатора и нормализовать ее. Если значение передано через `value`, используется оно.

**Примеры**:

```python
result = await grabber.affiliate_summary_2(value='Some summary 2')
```

### `Graber.affiliate_text`

**Назначение**: Извлекает и устанавливает текст филиала.

**Параметры**:

-   `value` (str, optional): Значение, передаваемое через kwargs. По умолчанию `None`.

**Возвращает**:

-   `bool`: `True` в случае успеха, `None` в случае ошибки.

**Как работает функция**:

Функция пытается получить текст филиала из локатора и нормализовать его. Если значение передано через `value`, используется оно.

**Примеры**:

```python
result = await grabber.affiliate_text(value='Some text')
```

### `Graber.affiliate_image_large`

**Назначение**: Извлекает и устанавливает большое изображение филиала.

**Параметры**:

-   `value` (str, optional): Значение, передаваемое через kwargs. По умолчанию `None`.

**Возвращает**:

-   `bool`: `True` в случае успеха, `None` в случае ошибки.

**Как работает функция**:

Функция пытается получить большое изображение филиала из локатора. Если значение передано через `value`, используется оно.

**Примеры**:

```python
result = await grabber.affiliate_image_large(value='http://example.com/image.jpg')
```

### `Graber.affiliate_image_medium`

**Назначение**: Извлекает и устанавливает среднее изображение филиала.

**Параметры**:

-   `value` (str, optional): Значение, передаваемое через kwargs. По умолчанию `None`.

**Возвращает**:

-   `bool`: `True` в случае успеха, `None` в случае ошибки.

**Как работает функция**:

Функция пытается получить среднее изображение филиала из локатора. Если значение передано через `value`, используется оно.

**Примеры**:

```python
result = await grabber.affiliate_image_medium(value='http://example.com/image.jpg')
```

### `Graber.affiliate_image_small`

**Назначение**: Извлекает и устанавливает маленькое изображение филиала.

**Параметры**:

-   `value` (str, optional): Значение, передаваемое через kwargs. По умолчанию `None`.

**Возвращает**:

-   `bool`: `True` в случае успеха, `None` в случае ошибки.

**Как работает функция**:

Функция пытается получить маленькое изображение филиала из локатора. Если значение передано через `value`, используется оно.

**Примеры**:

```python
result = await grabber.affiliate_image_small(value='http://example.com/image.jpg')
```

### `Graber.available_date`

**Назначение**: Извлекает и устанавливает доступную дату.

**Параметры**:

-   `value` (Any, optional): Значение, передаваемое через kwargs. По умолчанию `None`.

**Возвращает**:

-   `bool`: `True` в случае успеха, `None` в случае ошибки.

**Как работает функция**:

Функция пытается получить доступную дату из локатора. Если значение передано через `value`, используется оно.

**Примеры**:

```python
result = await grabber.available_date(value='2024-12-31')
```

### `Graber.available_for_order`

**Назначение**: Извлекает и устанавливает статус доступности для заказа.

**Параметры**:

-   `value` (str, optional): Значение, передаваемое через kwargs. По умолчанию `None`.

**Возвращает**:

-   `bool`: `True` в случае успеха, `None` в случае ошибки.

**Как работает функция**:

Функция пытается получить статус доступности для заказа из локатора. Если значение передано через `value`, используется оно.

**Примеры**:

```python
result = await grabber.available_for_order(value='true')
```

### `Graber.available_later`

**Назначение**: Извлекает и устанавливает статус доступности позже.

**Параметры**:

-   `value` (str, optional): Значение, передаваемое через kwargs. По умолчанию `None`.

**Возвращает**:

-   `bool`: `True` в случае успеха, `None` в случае ошибки.

**Как работает функция**:

Функция пытается получить статус доступности позже из локатора. Если значение передано через `value`, используется оно.

**Примеры**:

```python
result = await grabber.available_later(value='Будет доступно позже')
```

### `Graber.available_now`

**Назначение**: Извлекает и устанавливает статус доступности сейчас.

**Параметры**:

-   `value` (Any, optional): Значение, передаваемое через kwargs. По умолчанию `None`.

**Возвращает**:

-   `bool`: `True` в случае успеха, `None` в случае ошибки.

**Как работает функция**:

Функция пытается получить статус доступности сейчас из локатора. Если значение передано через `value`, используется оно.

**Примеры**:

```python
result = await grabber.available_now(value='В наличии')
```

### `Graber.additional_categories`

**Назначение**: Устанавливает дополнительные категории.

**Параметры**:

-   `value` (str | list, optional): Строка или список категорий. Если не передано, используется пустое значение.

**Возвращает**:

-   `dict`: Словарь с ID категорий.

**Как работает функция**:

Функция устанавливает дополнительные категории в поле `additional_categories` объекта `ProductFields`. Если `value` не передано, устанавливается пустая строка. Возвращает словарь с ID категорий.

**Примеры**:

```python
result = await grabber.additional_categories(value=['1', '2', '3'])
```

### `Graber.cache_default_attribute`

**Назначение**: Извлекает и устанавливает атрибут кэша по умолчанию.

**Параметры**:

-   `value` (Any, optional): Значение, передаваемое через kwargs. По умолчанию `None`.

**Возвращает**:

-   `bool`: `True` в случае успеха, `None` в случае ошибки.

**Как работает функция**:

Функция пытается получить атрибут кэша по умолчанию из локатора. Если значение передано через `value`, используется оно.

**Примеры**:

```python
result = await grabber.cache_default_attribute(value='some_attribute')
```

### `Graber.cache_has_attachments`

**Назначение**: Извлекает и устанавливает статус наличия вложений в кэше.

**Параметры**:

-   `value` (Any, optional): Значение, передаваемое через