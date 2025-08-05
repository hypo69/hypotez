# Модуль PrestaShop Product
## Обзор
Модуль `src/endpoints/prestashop/product.py` предназначен для работы с товарами в PrestaShop. Он содержит классы и функции для взаимодействия с товарами через API PrestaShop, включая добавление новых товаров, получение информации о товарах, управление категориями и загрузку изображений.

## Детали
Модуль `src/endpoints/prestashop/product.py` реализует взаимодействие с товарами в PrestaShop. Он использует API PrestaShop для добавления новых товаров, обновления информации о товарах, получения данных о товарах и загрузки изображений. Модуль интегрирован с другими модулями проекта `hypotez` для обработки данных, вызова API и логирования.

##  Классы
### `Config`
**Описание**: Класс конфигурации для настроек товаров в PrestaShop.

**Атрибуты**:
- `MODE` (str): Режим работы.
- `API_DOMAIN` (str): Домен API PrestaShop.
- `API_KEY` (str): Ключ API PrestaShop.

**Принцип работы**:
- Класс `Config` содержит конфигурационные параметры для подключения к API PrestaShop. 
- Значения для `API_DOMAIN` и `API_KEY` могут быть установлены из переменных окружения или из конфигурационного файла `keepass`.

### `PrestaProduct`
**Описание**: Класс, отвечающий за взаимодействие с товарами в PrestaShop.

**Наследует**: `PrestaShop`

**Атрибуты**: 
- `api_key` (Optional[str]): Ключ API PrestaShop.
- `api_domain` (Optional[str]): Домен API PrestaShop.

**Принцип работы**:
- Класс `PrestaProduct` наследует от класса `PrestaShop` и предоставляет дополнительные методы для работы с товарами.
- Класс использует `Config` для получения ключа и домена API.
- При создании экземпляра класса `PrestaProduct`, он автоматически подключается к API PrestaShop с помощью ключа и домена, полученных из `Config`.


**Методы**:
- `get_product_schema`: Возвращает схему для ресурса товара из PrestaShop.
- `get_parent_category`: Получает родительские категории из PrestaShop для заданной категории рекурсивно.
- `_add_parent_categories`: Добавляет все родительские категории в объект `ProductFields`.
- `get_product`: Возвращает словарь полей товара из магазина Prestashop.
- `add_new_product`: Добавляет новый товар в PrestaShop.

**Как работает**:
- `get_product_schema`: Этот метод использует `self.get_schema`, чтобы получить схему ресурса товара из PrestaShop. 
- `get_parent_category`: Метод использует `self.read` для получения данных о категории из PrestaShop и возвращает ID родительской категории.
- `_add_parent_categories`: Метод вычисляет и добавляет все уникальные родительские категории в объект `ProductFields`. 
- `get_product`: Этот метод использует `self.read` для получения данных о товаре из PrestaShop и возвращает словарь полей товара.
- `add_new_product`: Этот метод преобразовывает объект `ProductFields` в словарь формата PrestaShop, преобразует словарь в XML, отправляет XML-данные в API PrestaShop и возвращает ID добавленного товара.

**Примеры**:
```python
# Создание экземпляра класса PrestaProduct
p = PrestaProduct()

# Получение схемы для товара с ID 24
schema = p.get_product_schema(resource_id=24)

# Получение ID родительской категории для категории с ID 123
parent_category_id = p.get_parent_category(id_category=123)

# Получение данных о товаре с ID 456
product_data = p.get_product(id_product=456)

# Добавление нового товара
f = ProductFields(...) # Заполнить объект ProductFields данными о товаре
new_product_id = p.add_new_product(f)
```

##  Функции
### `example_add_new_product`
**Цель**: Пример для добавления товара в Prestashop

**Пример**:
```python
def example_add_new_product() -> None:
    """Пример для добавления товара в Prestashop"""
    p = PrestaProduct(API_KEY=Config.API_KEY, API_DOMAIN=Config.API_DOMAIN)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEBUG ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # resource_id = 2191
    # schema = p.get_product_schema(resource_id = resource_id)
    # j_dumps(schema, gs.path.endpoints / 'emil' / '_experiments' / f'product_schema.{resource_id}_{gs.now}.json')
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    example_data: dict = j_loads(
        gs.path.endpoints / 'emil' / '_experiments' / 'product_schema.2191_250319224027026.json'
    )  # <- XML like
    """"""
    if not example_data:
        logger.error(f'Файл не существует или неправильный формат файла')
        ...
        return

    presta_product_xml = dict2xml(example_data)  # <- XML
    save_xml(presta_product_xml, gs.path.endpoints / 'emil' / '_experiments' / f'{gs.now}_presta_product.xml')

    # 1. JSON | XML
    kwargs: dict = {
        'io_format': 'JSON',
    }

    response = p._exec(
        resource='products',
        method='POST',
        data=example_data if kwargs['io_format'] == 'JSON' else presta_product_xml,
        **kwargs,
    )
    # response = p.create('products', data=presta_product_dict  if kwargs['io_format'] == 'JSON' else presta_product_xml, **kwargs)
    # j_dumps(response if kwargs['io_format'] == 'JSON' else xml2dict(response), gs.path.endpoints / 'emil' / '_experiments' / f"{gs.now}_presta_response_new_product_added.json")

    print(response)
    ...
```

### `example_get_product`
**Цель**: Пример для получения информации о товаре по ID.

**Пример**:
```python
def example_get_product(id_product: int, **kwargs) -> None:
    """"""

    p = PrestaProduct(API_KEY=Config.API_KEY, API_DOMAIN=Config.API_DOMAIN)
    # kwargs: dict = {
    #     'data_format': 'JSON',
    #     'display': 'full',
    #     'schema': 'blank',
    # }
    presta_product = p.get_product(id_product, **kwargs)
    presta_product = presta_product[0] if isinstance(presta_product, list) else presta_product
    ...
    j_dumps(
        presta_product, gs.path.endpoints / 'emil' / '_experiments' / f'presta_response_product_{id_product}.json'
    )
    ...
```

## Детали параметров
- `id_product` (int): ID товара в PrestaShop.

##  Примеры
```python
# Пример получения информации о товаре с ID 2191
example_get_product(id_product=2191)