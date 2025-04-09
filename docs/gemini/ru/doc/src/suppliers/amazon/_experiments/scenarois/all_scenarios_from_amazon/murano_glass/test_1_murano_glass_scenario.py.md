# Модуль для тестирования сценария Murano Glass на Amazon

## Обзор

Модуль предназначен для тестирования сценариев работы с товарами Murano Glass на платформе Amazon. Он включает в себя функциональность для извлечения информации о товарах, проверки их наличия в базе данных PrestaShop, а также загрузки изображений товаров.

## Подробней

Этот модуль является частью процесса тестирования и автоматизации работы с поставщиками Amazon. Он использует различные классы и функции из других модулей (`header`), таких как `Supplier`, `Product`, `Driver` и `PrestaAPIV2`, для взаимодействия с Amazon и PrestaShop.
В данном сценарии основное внимание уделяется товарам категории Murano Glass. Модуль определяет локаторы элементов на странице товара, извлекает необходимые данные и выполняет соответствующие действия, такие как добавление товара в PrestaShop или обновление информации о нем.

## Классы

### `Supplier`

**Описание**: Класс `Supplier` представляет поставщика товаров, в данном случае Amazon.
**Наследует**:
**Атрибуты**:
- `supplier_id` (str): Идентификатор поставщика (`amazon`).
- `current_scenario` (dict): Словарь, содержащий информацию о текущем сценарии, включая URL, условие, категории PrestaShop и правило цены.
- `locators` (dict): Локаторы элементов на странице товара.
- `driver` (webdriver): Инстанс веб-драйвера для взаимодействия с веб-страницей.
**Принцип работы**:
Класс `Supplier` инициализируется с префиксом поставщика (`amazon`). Он содержит информацию о текущем сценарии, локаторы элементов на странице товара и инстанс веб-драйвера. Этот класс используется для управления процессом извлечения и обработки данных о товарах.

### `Product`

**Описание**: Класс `Product` представляет товар.
**Наследует**:
**Атрибуты**:
- Отсутствуют атрибуты, специфичные для данного примера кода.
**Методы**:
- `check_if_product_in_presta_db(product_reference: str) -> Union[int, bool]`: Проверяет наличие товара в базе данных PrestaShop по reference.
- `upload_image2presta(image_url: str, product_id: int)`: Загружает изображение товара в PrestaShop.
- `grab_product_page(s: Supplier) -> ProductFields`: Извлекает информацию о товаре со страницы товара на Amazon.

### `Driver`

**Описание**: Класс `Driver` представляет веб-драйвер для взаимодействия с веб-страницами.
**Наследует**:
**Атрибуты**:
- Отсутствуют атрибуты, специфичные для данного примера кода.
**Методы**:
- `execute_locator(l: dict) -> str`: Выполняет локатор и возвращает значение веб-элемента.
- `get_url(url: str)`: Открывает URL в веб-драйвере.

## Методы класса

### `check_if_product_in_presta_db`

```python
def check_if_product_in_presta_db(product_reference: str) -> Union[int, bool]:
    """ Проверяет, существует ли продукт в базе данных PrestaShop.
    Args:
        product_reference (str): Артикул товара, используемый для поиска в базе данных.

    Returns:
        Union[int, bool]: Если товар найден, возвращает его ID (id_product). Если товар не найден, возвращает `False`.

    Raises:
        Не вызывает исключений напрямую, но может столкнуться с исключениями при взаимодействии с базой данных.

    Example:
        >>> product_id = Product.check_if_product_in_presta_db("amazon-B09N53XSQB")
        >>> if product_id:
        ...     print(f"Товар с ID {product_id} найден в базе данных.")
        ... else:
        ...     print("Товар не найден в базе данных.")
    """
    ...
```

### `upload_image2presta`

```python
def upload_image2presta(image_url: str, product_id: int):
    """ Загружает изображение товара в PrestaShop.

    Args:
        image_url (str): URL изображения для загрузки.
        product_id (int): ID товара в PrestaShop, к которому нужно привязать изображение.

    Returns:
        None

    Raises:
        Может вызывать исключения при неудачной загрузке или обработке изображения.

    Example:
        >>> Product.upload_image2presta("https://example.com/image.jpg", 123)
    """
    ...
```

### `grab_product_page`

```python
def grab_product_page(s: Supplier) -> ProductFields:
    """ Извлекает информацию о товаре со страницы товара на Amazon.

    Args:
        s (Supplier): Инстанс класса `Supplier`, содержащий информацию о поставщике и текущем сценарии.

    Returns:
        ProductFields: Объект `ProductFields`, содержащий извлеченные данные о товаре.

    Raises:
        Возможны исключения при невозможности извлечь какие-либо данные со страницы.

    Example:
        >>> supplier = Supplier("amazon")
        >>> product_fields = Product.grab_product_page(supplier)
        >>> print(product_fields.fields["name"])
    """
    ...
```

## Параметры класса

- `supplier_prefix` (str): Префикс поставщика (в данном случае `'amazon'`).
- `s` (Supplier): Инстанс класса `Supplier`, созданный с префиксом поставщика.
- `s.current_scenario` (dict): Словарь, содержащий информацию о текущем сценарии, включая URL, условие, категории PrestaShop и правило цены.
- `l` (dict): Локаторы элементов на странице товара, полученные из `s.locators.get('product')`.
- `d` (Driver): Инстанс веб-драйвера, полученный из `s.driver`.
- `ASIN` (str): Значение ASIN (Amazon Standard Identification Number) товара, полученное с использованием локатора `l['ASIN']`.
- `product_reference` (str): Артикул товара, сформированный как `f"{s.supplier_id}-{ASIN}"`.
- `product_id` (Union[int, bool]): ID товара в базе данных PrestaShop, полученный с помощью `Product.check_if_product_in_presta_db(product_reference)`.
- `default_image_url` (str): URL первого изображения товара, полученный из списка `_(l['additional_images_urls'])`.
- `product_fields` (ProductFields): Объект `ProductFields`, содержащий извлеченные данные о товаре.
- `product_dict` (dict): Словарь, содержащий данные о товаре, подготовленные для добавления в PrestaShop.
- `product_name` (list): Список частей названия товара, полученный с использованием локатора `l['name']`.
- `res_product_name` (str): Объединенное название товара из списка `product_name`.

## Примеры

```python
# Пример создания инстанса класса Supplier
supplier_prefix = 'amazon'
s = start_supplier(supplier_prefix)

# Пример определения текущего сценария
s.current_scenario: dict = {
    "url": "https://amzn.to/3OhRz2g",
    "condition": "new",
    "presta_categories": {
        "default_category": {"11209": "MURANO GLASS"},
        "additional_categories": [""]
    },
    "price_rule": 1
}

# Пример получения локаторов и драйвера
l = s.locators.get('product')
d = s.driver

# Пример получения ASIN товара
ASIN = _(l['ASIN'])

# Пример формирования артикула товара
product_reference = f"{s.supplier_id}-{ASIN}"

# Пример проверки наличия товара в базе данных PrestaShop
product_id = Product.check_if_product_in_presta_db(product_reference)
print(f' Если товар в бд получу id_product, иначе False. Получил: {product_id}')

# Пример получения URL первого изображения товара
default_image_url = _(l['additional_images_urls'])[0]