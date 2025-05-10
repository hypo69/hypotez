# Модуль грабера

## Обзор

Модуль `graber.py` предназначен для сбора информации о товарах с веб-страниц поставщиков. Он содержит базовый класс `Graber`, который использует веб-драйвер для извлечения целевых полей, таких как название, описание, спецификация, артикул и цена. Расположение этих полей определяется локаторами, хранящимися в JSON-файлах в директории `locators` каждого поставщика.

## Подробнее

Этот модуль предоставляет основу для создания граберов для различных поставщиков, позволяя стандартизировать процесс сбора данных и упростить интеграцию с другими частями проекта. Для нестандартной обработки полей товара можно переопределить соответствующие функции в классах-наследниках.

## Содержание

1.  [Общие сведения](#общие-сведения)
2.  [Классы](#классы)
    *   [Config](#класс-config)
    *   [Graber](#класс-graber)
3.  [Функции](#функции)
    *   [close_pop_up](#функция-close_pop_up)

## Общие сведения

-   Модуль предоставляет базовый класс `Graber` для сбора данных о товарах с веб-страниц поставщиков.
-   Использует веб-драйвер для извлечения информации о товарах.
-   Поддерживает конфигурацию через JSON-файлы с локаторами элементов на страницах товаров.

## Классы

### `Config`

Класс для хранения глобальных настроек.

**Описание**:
Класс `Config` предназначен для хранения глобальных настроек, используемых граберами.

**Атрибуты**:

*   `locator_for_decorator` (`Optional[SimpleNamespace]`): Локатор для декоратора `@close_pop_up`. Если установлен, декоратор будет выполнен.
*   `supplier_prefix` (`Optional[str]`): Префикс поставщика.
*   `driver` (`'Driver'`): Экземпляр класса `Driver`. Если не передан, создается новый экземпляр класса `Driver(Firefox)` по умолчанию.

**Пример**:

```python
Config = Config()
Config.supplier_prefix = 'prefix'
print(Config.supplier_prefix)
```

### `Graber`

Базовый класс сбора данных со страницы для всех поставщиков.

**Описание**:
Класс `Graber` является базовым классом для сбора данных о товарах с веб-страниц поставщиков. Он предоставляет функциональность для инициализации, загрузки локаторов, управления драйвером и сбора данных о товарах.

**Методы**:

*   `__init__(supplier_prefix: str, driver: Optional['Driver'] = None, lang_index: Optional[int] = 2)`: Инициализация класса `Graber`.
*   `yield_scenarios_for_supplier(supplier_prefix: str, input_scenarios: Optional[List[Dict[str, Any]] | Dict[str, Any]] = None) -> Generator[Dict[str, Any], None, None]`: Генератор, который выдает словари сценариев для поставщика.
*   `process_supplier_scenarios_async(supplier_prefix: str, input_scenarios=None, id_lang: Optional[int] = 1) -> bool`: Метод, использующий генератор `yield_scenarios_for_supplier` и вызывающий `run_scenario` для каждого сценария.
*   `process_scenarios(supplier_prefix: str, input_scenarios: List[Dict[str, Any]] | Dict[str, Any], id_lang: Optional[int] = 1) -> Optional[List[Any]]`: Выполняет один или несколько сценариев для указанного поставщика.
*   `set_field_value(value: Any, locator_func: Callable[[], Any], field_name: str, default: Any = '') -> Any`: Универсальная функция для установки значений полей с обработкой ошибок.
*   `grab_page(self, *args, **kwargs) -> ProductFields`: Функция для сбора полей товара.
*   `grab_page_async(self, *args, **kwargs) -> ProductFields`: Асинхронная функция для сбора полей товара.
*   `error(field: str)`: Обработчик ошибок для полей.
*   `additional_shipping_cost(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает дополнительную стоимость доставки.
*   `delivery_in_stock(value: Optional[str] = None) -> bool`: Извлекает и устанавливает статус доставки в наличии.
*   `active(value: bool = True) -> bool`: Извлекает и устанавливает статус активности.
*   `additional_delivery_times(value: Optional[str] = None) -> bool`: Извлекает и устанавливает дополнительное время доставки.
*   `advanced_stock_management(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает статус расширенного управления запасами (DEPRECATED FIELD!).
*   `affiliate_short_link(value: Optional[str] = None) -> bool`: Извлекает и устанавливает короткую партнерскую ссылку.
*   `affiliate_summary(value: Optional[str] = None) -> bool`: Извлекает и устанавливает партнерский обзор.
*   `affiliate_summary_2(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает партнерский обзор 2.
*   `affiliate_text(value: Optional[str] = None) -> bool`: Извлекает и устанавливает партнерский текст.
*   `affiliate_image_large(value: Optional[str] = None) -> bool`: Извлекает и устанавливает большое партнерское изображение.
*   `affiliate_image_medium(value: Optional[str] = None) -> bool`: Извлекает и устанавливает среднее партнерское изображение.
*   `affiliate_image_small(value: Optional[str] = None) -> bool`: Извлекает и устанавливает маленькое партнерское изображение.
*   `available_date(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает доступную дату.
*   `available_for_order(value: Optional[str] = None) -> bool`: Извлекает и устанавливает статус "доступно для заказа".
*   `available_later(value: Optional[str] = None) -> bool`: Извлекает и устанавливает статус "доступно позже".
*   `available_now(value: Optional[str] = None) -> bool`: Извлекает и устанавливает статус "доступно сейчас".
*   `additional_categories(value: str | list = None) -> dict`: Устанавливает дополнительные категории.
*   `cache_default_attribute(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает кэш атрибута по умолчанию.
*   `cache_has_attachments(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает статус кэша "имеются вложения".
*   `cache_is_pack(value: Optional[str] = None) -> bool`: Извлекает и устанавливает статус кэша "является набором".
*   `condition(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает условие товара.
*   `customizable(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает статус "настраиваемый".
*   `date_add(value: Optional[str | datetime.date] = None) -> bool`: Извлекает и устанавливает дату добавления.
*   `date_upd(value: Optional[str | datetime.date] = None) -> bool`: Извлекает и устанавливает дату обновления.
*   `delivery_out_stock(value: Optional[str] = None) -> bool`: Извлекает и устанавливает доставку при отсутствии на складе.
*   `depth(value: Optional[float] = None) -> bool`: Извлекает и устанавливает глубину.
*   `description(value: Optional[str] = None) -> bool`: Извлекает и устанавливает описание.
*   `description_short(value: Optional[str] = '') -> bool`: Извлекает и устанавливает краткое описание.
*   `id_category_default(value: int) -> bool`: Извлекает и устанавливает ID категории по умолчанию.
*   `id_default_combination(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает ID комбинации по умолчанию.
*   `id_product(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает ID товара.
*   `locale(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает локаль.
*   `id_default_image(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает ID изображения по умолчанию.
*   `ean13(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает код EAN13.
*   `ecotax(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает ecotax.
*   `height(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает высоту.
*   `how_to_use(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает "как использовать".
*   `id_manufacturer(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает ID производителя.
*   `id_supplier(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает ID поставщика.
*   `id_tax_rules_group(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает ID налога.
*   `id_type_redirected(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает ID перенаправленного типа.
*   `images_urls(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает URL изображений.
*   `indexed(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает статус "индексировано".
*   `ingredients(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает ингредиенты.
*   `meta_description(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает meta-описание.
*   `meta_keywords(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает meta-ключевые слова.
*   `meta_title(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает meta-заголовок.
*   `is_virtual(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает статус "виртуальный".
*   `isbn(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает ISBN.
*   `link_rewrite(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает перезапись ссылки.
*   `location(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает местоположение.
*   `low_stock_alert(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает оповещение о низком запасе.
*   `low_stock_threshold(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает порог низкого запаса.
*   `minimal_quantity(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает минимальное количество.
*   `mpn(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает MPN (Manufacturer Part Number).
*   `name(value: Optional[str] = '') -> bool`: Извлекает и устанавливает наименование товара.
*   `online_only(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает статус "только онлайн".
*   `on_sale(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает статус "в продаже".
*   `out_of_stock(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает статус "нет в наличии".
*   `pack_stock_type(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает тип запаса упаковки.
*   `price(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает цену.
*   `product_type(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает тип товара.
*   `quantity(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает количество.
*   `quantity_discount(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает скидку за количество.
*   `redirect_type(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает тип перенаправления.
*   `reference(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает ссылку.
*   `show_condition(value: Optional[int] = None) -> bool`: Извлекает и устанавливает "показывать условие".
*   `show_price(value: Optional[int] = None) -> bool`: Извлекает и устанавливает "показывать цену".
*   `state(value: Optional[str] = None) -> bool`: Извлекает и устанавливает состояние.
*   `text_fields(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает текстовые поля.
*   `unit_price_ratio(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает коэффициент цены за единицу.
*   `unity(value: Optional[str] = None) -> bool`: Извлекает и устанавливает "единство".
*   `upc(value: Optional[str] = None) -> bool`: Извлекает и устанавливает UPC.
*   `uploadable_files(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает загружаемые файлы.
*   `default_image_url(value: Optional[str] = None) -> bool`: Извлекает и устанавливает URL изображения по умолчанию.
*   `visibility(value: Optional[str] = None) -> bool`: Извлекает и устанавливает видимость.
*   `weight(value: Optional[float] = None) -> bool`: Извлекает и устанавливает вес.
*   `wholesale_price(value: Optional[float] = None) -> bool`: Извлекает и устанавливает оптовую цену.
*   `width(value: Optional[float] = None) -> bool`: Извлекает и устанавливает ширину.
*   `specification(value: Optional[str | list] = None) -> bool`: Извлекает и устанавливает спецификацию.
*   `link(value: Optional[str] = None) -> bool`: Извлекает и устанавливает ссылку.
*   `byer_protection(value: Optional[str] = None) -> bool`: Извлекает и устанавливает защиту покупателя.
*   `customer_reviews(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает отзывы клиентов.
*   `link_to_video(value: Optional[Any] = None) -> bool`: Извлекает и устанавливает ссылку на видео.
*   `local_image_path(value: Optional[str] = None) -> bool`: Извлекает и сохраняет изображение локально.
*   `local_video_path(value: Optional[Any] = None) -> bool`: Извлекает и сохраняет видео локально.

## Функции

### `close_pop_up`

Создает декоратор для закрытия всплывающих окон перед выполнением основной логики функции.

**Описание**:
Функция `close_pop_up` создает декоратор, который закрывает всплывающие окна перед выполнением основной логики декорируемой функции.

**Аргументы**:

*   `value` (`'Driver'`): Дополнительное значение для декоратора.

**Возвращает**:

*   `Callable`: Декоратор, оборачивающий функцию.

**Принцип работы**:

1.  Определяет внутреннюю функцию `decorator`, которая принимает функцию `func` в качестве аргумента.
2.  Внутри `decorator` определяется асинхронная функция `wrapper`, которая выполняет следующие действия:
    *   Проверяет, установлен ли `Config.locator_for_decorator`. Если да, то пытается выполнить локатор для закрытия всплывающего окна с помощью `Config.driver.execute_locator()`.
    *   В случае ошибки выполнения локатора, логирует отладочное сообщение.
    *   После выполнения локатора или при его отсутствии, вызывает основную функцию `func` с переданными аргументами и возвращает результат.
3.  Возвращает функцию `wrapper`.

**Пример**:

```python
@close_pop_up()
async def my_function():
    # Здесь логика вашей функции
    pass