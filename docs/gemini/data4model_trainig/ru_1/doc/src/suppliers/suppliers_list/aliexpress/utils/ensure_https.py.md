# Модуль `ensure_https`

## Обзор

Модуль `ensure_https` предназначен для работы с URL-адресами и идентификаторами продуктов, обеспечивая наличие префикса `https://`. Если на вход подается идентификатор продукта, модуль формирует полный URL-адрес с использованием этого идентификатора и префикса `https://`.

## Подробнее

Этот модуль предоставляет функцию `ensure_https`, которая принимает строку URL или список строк URL и гарантирует, что все они начинаются с `https://`. Если строка не является URL-адресом, она интерпретируется как идентификатор продукта AliExpress, и функция преобразует его в полный URL-адрес. Модуль использует `logger` для регистрации ошибок и `extract_prod_ids` для извлечения идентификаторов продуктов из URL-адресов.

## Функции

### `ensure_https`

**Назначение**: Обеспечивает наличие префикса `https://` в предоставленной строке URL или списке строк URL. Если входные данные являются идентификатором продукта, функция создает полный URL-адрес с префиксом `https://`.

**Параметры**:

-   `prod_ids` (str | list[str]): Строка URL или список строк URL для проверки и изменения, если это необходимо.

**Возвращает**:

-   `str | list[str]`: Строка URL или список строк URL с префиксом `https://`.

**Вызывает исключения**:

-   `ValueError`: Если `prod_ids` является экземпляром `WindowsPath`.

**Внутренние функции**:

-   `ensure_https_single`: Обеспечивает наличие префикса `https://` в одной строке URL или идентификаторе продукта.

**Как работает функция**:

Функция `ensure_https` проверяет, является ли входной параметр `prod_ids` списком или строкой. Если это список, она применяет внутреннюю функцию `ensure_https_single` к каждому элементу списка и возвращает новый список с измененными URL-адресами. Если это строка, она напрямую передается в `ensure_https_single` и возвращается результат.

**Примеры**:

```python
>>> ensure_https("example_product_id")
'https://www.aliexpress.com/item/example_product_id.html'

>>> ensure_https(["example_product_id1", "https://www.aliexpress.com/item/example_product_id2.html"])
['https://www.aliexpress.com/item/example_product_id1.html', 'https://www.aliexpress.com/item/example_product_id2.html']

>>> ensure_https("https://www.example.com/item/example_product_id")
'https://www.example.com/item/example_product_id'
```

### `ensure_https_single`

**Назначение**: Обеспечивает, чтобы одна строка URL или идентификатор продукта имели префикс `https://`.

**Параметры**:

-   `prod_id` (str): Строка URL или идентификатор продукта.

**Возвращает**:

-   `str`: Строка URL с префиксом `https://`.

**Вызывает исключения**:

-   `ValueError`: Если `prod_id` является экземпляром `WindowsPath`.

**Как работает функция**:

Внутренняя функция `ensure_https_single` принимает строку `prod_id`, извлекает идентификатор продукта с помощью функции `extract_prod_ids`. Если идентификатор успешно извлечен, функция возвращает полный URL-адрес с префиксом `https://` и идентификатором продукта. В случае ошибки извлечения идентификатора, функция логирует ошибку и возвращает исходный `prod_id`.

**Примеры**:

```python
>>> ensure_https_single("example_product_id")
'https://www.aliexpress.com/item/example_product_id.html'

>>> ensure_https_single("https://www.example.com/item/example_product_id")
'https://www.example.com/item/example_product_id'
```