# Модуль PrestaShop Endpoint

## Обзор

Этот модуль предоставляет функциональность для работы с PrestaShop API. Он содержит набор функций для обработки различных задач, таких как загрузка описаний товаров в PrestaShop. 

## Детали

Модуль `src.endpoints.emil.presta` предназначен для взаимодействия с PrestaShop API, предоставляя функции для выполнения операций с товарами. 

## Классы

### `class PrestaShopEndpoint`

**Описание**: Класс `PrestaShopEndpoint` представляет собой точку входа для работы с PrestaShop API. Он предоставляет методы для выполнения операций с товарами, такие как получение списка товаров, создание новых товаров и обновление существующих.

**Атрибуты**:

- `config (dict)`: Словарь конфигурации для PrestaShop API, включая такие параметры, как `api_key`, `shop_url` и `language`.

**Методы**:

- `get_products(page: int = 1, limit: int = 100) -> list`: Метод для получения списка товаров из PrestaShop.

    **Параметры**:

    - `page (int, optional)`: Номер страницы для получения товаров. По умолчанию `1`.
    - `limit (int, optional)`: Количество товаров на странице. По умолчанию `100`.

    **Возвращает**:

    - `list`: Список товаров в формате JSON.


- `create_product(product_data: dict) -> dict`: Метод для создания нового товара в PrestaShop.

    **Параметры**:

    - `product_data (dict)`: Словарь данных о новом товаре. Должен содержать все необходимые поля для создания товара в PrestaShop. 

    **Возвращает**:

    - `dict`: Словарь данных о созданном товаре, включая его ID.


- `update_product(product_id: int, product_data: dict) -> dict`: Метод для обновления данных существующего товара.

    **Параметры**:

    - `product_id (int)`: ID товара, который нужно обновить.
    - `product_data (dict)`: Словарь данных, которые нужно обновить для товара.

    **Возвращает**:

    - `dict`: Словарь данных об обновленном товаре.

- `delete_product(product_id: int) -> bool`: Метод для удаления товара из PrestaShop.

    **Параметры**:

    - `product_id (int)`: ID товара, который нужно удалить.

    **Возвращает**:

    - `bool`: `True`, если товар успешно удален, `False` в противном случае.

## Функции

### `function load_product_descriptions(product_ids: list) -> dict`:

**Описание**: Функция `load_product_descriptions` загружает описания товаров из PrestaShop API.

**Параметры**:

- `product_ids (list)`: Список ID товаров, описания которых нужно загрузить.

**Возвращает**:

- `dict`: Словарь, содержащий описания товаров, где ключи - это ID товаров, а значения - это описания.


**Принцип работы**:

- Функция получает список ID товаров.
- Для каждого ID она выполняет запрос к PrestaShop API, чтобы получить описание товара.
- Затем она добавляет описание товара в словарь, где ключ - это ID товара, а значение - описание.

**Примеры**:

```python
# Загрузка описаний товаров с ID 1, 2, 3
product_descriptions = load_product_descriptions([1, 2, 3])
print(product_descriptions)
```


### `function load_all_product_descriptions() -> dict`:

**Описание**: Функция `load_all_product_descriptions` загружает описания всех товаров из PrestaShop.

**Параметры**:

- Нет.

**Возвращает**:

- `dict`: Словарь, содержащий описания товаров, где ключи - это ID товаров, а значения - это описания.


**Принцип работы**:

- Функция использует метод `get_products` для получения списка всех товаров.
- Она перебирает полученный список товаров и для каждого товара выполняет запрос к PrestaShop API, чтобы получить его описание.
- Затем она добавляет описание товара в словарь, где ключ - это ID товара, а значение - описание.

**Примеры**:

```python
# Загрузка описаний всех товаров
all_product_descriptions = load_all_product_descriptions()
print(all_product_descriptions)
```

## Внутренние функции:

### `function _get_product_description(product_id: int) -> str`:

**Описание**: Внутренняя функция `_get_product_description` получает описание товара из PrestaShop API.

**Параметры**:

- `product_id (int)`: ID товара, описание которого нужно получить.

**Возвращает**:

- `str`: Описание товара.


**Принцип работы**:

- Функция отправляет запрос к PrestaShop API с указанным ID товара.
- Она извлекает описание товара из ответа API и возвращает его.

**Примеры**:

```python
# Получение описания товара с ID 1
product_description = _get_product_description(1)
print(product_description)
```

## Параметры

- `product_id (int)`: ID товара в PrestaShop.
- `product_data (dict)`: Словарь с данными о товаре.
- `page (int, optional)`: Номер страницы для получения товаров. По умолчанию `1`.
- `limit (int, optional)`: Количество товаров на странице. По умолчанию `100`.

## Примеры

```python
# Создание экземпляра класса PrestaShopEndpoint
prestashop = PrestaShopEndpoint(config={
    'api_key': '<your_api_key>', 
    'shop_url': '<your_shop_url>',
    'language': '<your_language_code>'
})

# Получение списка товаров
products = prestashop.get_products(page=2, limit=50)
print(products)

# Создание нового товара
new_product_data = {
    'name': '<product_name>',
    'description': '<product_description>',
    # ... другие данные о товаре
}
new_product = prestashop.create_product(new_product_data)
print(new_product)

# Обновление товара
product_id = 123
updated_product_data = {
    'name': '<updated_product_name>',
    # ... другие данные для обновления
}
updated_product = prestashop.update_product(product_id, updated_product_data)
print(updated_product)

# Удаление товара
product_id = 123
success = prestashop.delete_product(product_id)
print(f'Товар {product_id} успешно удален: {success}')

# Загрузка описаний товаров
product_ids = [1, 2, 3]
product_descriptions = load_product_descriptions(product_ids)
print(product_descriptions)

# Загрузка описаний всех товаров
all_product_descriptions = load_all_product_descriptions()
print(all_product_descriptions)
```

## Дополнительная информация

- Для работы с этим модулем требуется наличие API-ключа и URL-адреса вашего магазина PrestaShop.
- Модуль использует библиотеку `requests` для отправки запросов к PrestaShop API. 
-  Если  используется  webdriver,  в  модуле  PrestaShopEndpoint  необходимо  использовать  классы `Driver`, `Chrome`, `Firefox` или `Playwright`  из модуля `webdriver`. 
-  Рекомендуется  использовать  `logger`  из  модуля `src.logger.logger`  для  логгирования  информации и ошибок.