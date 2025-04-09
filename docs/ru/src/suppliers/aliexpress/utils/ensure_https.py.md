# Модуль `ensure_https`

## Обзор

Модуль `ensure_https` предназначен для обеспечения наличия префикса `https://` в предоставленных URL или идентификаторах продуктов. Если входные данные являются идентификатором продукта, модуль создает полный URL с префиксом `https://`.

## Подробнее

Модуль содержит функцию `ensure_https`, которая принимает на вход строку URL или список строк URL и возвращает строку URL или список строк URL с добавленным префиксом `https://`, если он отсутствует. Если передан идентификатор продукта, функция формирует полный URL для товара на AliExpress.

## Функции

### `ensure_https`

```python
def ensure_https(prod_ids: str | list[str]) -> str | list[str]:
    """ Ensures that the provided URL string(s) contain the https:// prefix.
    If the input is a product ID, it constructs a full URL with https:// prefix.

    Args:
        prod_ids (str | list[str]): A URL string or a list of URL strings to check and modify if necessary.

    Returns:
        str | list[str]: The URL string or list of URL strings with the https:// prefix.

    Raises:
        ValueError: If `prod_ids` is an instance of `WindowsPath`.

    Examples:
        >>> ensure_https("example_product_id")
        'https://www.aliexpress.com/item/example_product_id.html'

        >>> ensure_https(["example_product_id1", "https://www.aliexpress.com/item/example_product_id2.html"])
        ['https://www.aliexpress.com/item/example_product_id1.html', 'https://www.aliexpress.com/item/example_product_id2.html']

        >>> ensure_https("https://www.example.com/item/example_product_id")
        'https://www.example.com/item/example_product_id'
    """
```

**Назначение**: Обеспечивает, чтобы предоставленные URL-адреса или идентификаторы продуктов содержали префикс `https://`. Если входные данные - идентификатор продукта, создает полный URL с префиксом `https://`.

**Параметры**:

- `prod_ids` (str | list[str]): URL-адрес в виде строки или список URL-адресов для проверки и изменения при необходимости.

**Возвращает**:

- `str | list[str]`: URL-адрес в виде строки или список URL-адресов с префиксом `https://`.

**Вызывает исключения**:

- `ValueError`: Если `prod_ids` является экземпляром `WindowsPath`.

**Внутренние функции**:

#### `ensure_https_single`

```python
def ensure_https_single(prod_id: str) -> str:
    """ Ensures a single URL or product ID string has the https:// prefix.

    Args:
        prod_id (str): The URL or product ID string.

    Returns:
        str: The URL string with the https:// prefix.

    Raises:
        ValueError: If `prod_id` is an instance of `WindowsPath`.

    Examples:
        >>> ensure_https_single("example_product_id")
        'https://www.aliexpress.com/item/example_product_id.html'

        >>> ensure_https_single("https://www.example.com/item/example_product_id")
        'https://www.example.com/item/example_product_id'
    """
```

**Назначение**: Обеспечивает, чтобы одиночный URL или идентификатор продукта содержал префикс `https://`.

**Параметры**:

- `prod_id` (str): URL-адрес или идентификатор продукта в виде строки.

**Возвращает**:

- `str`: URL-адрес в виде строки с префиксом `https://`.

**Вызывает исключения**:

- `ValueError`: Если `prod_id` является экземпляром `WindowsPath`.

**Как работает функция `ensure_https_single`**:

1. **Извлекает идентификатор продукта**: Извлекает идентификатор продукта из предоставленного `prod_id` с использованием функции `extract_prod_ids`.
2. **Проверяет и формирует URL**: Если идентификатор продукта извлечен успешно, формирует URL-адрес товара на AliExpress, объединяя `https://www.aliexpress.com/item/` с идентификатором продукта и добавляя `.html`.
3. **Обрабатывает ошибку**: Если `prod_id` не является допустимым идентификатором продукта или URL, логирует ошибку с использованием `logger.error` и возвращает исходный `prod_id`.

```
   Начало
   │
   │ prod_id
   │
   │ Извлечение идентификатора продукта с помощью extract_prod_ids
   │
   │ Идентификатор?
   ├── Да: Формирование URL-адреса товара на AliExpress
   │   │
   │   └── Возврат URL-адреса
   │
   └── Нет: Логирование ошибки и возврат исходного prod_id
   │
   Конец
```

**Как работает функция `ensure_https`**:

1. **Проверяет тип входных данных**: Проверяет, является ли `prod_ids` списком или строкой.
2. **Обрабатывает список URL**: Если `prod_ids` - это список, применяет функцию `ensure_https_single` к каждому элементу списка и возвращает новый список с обработанными URL.
3. **Обрабатывает строку URL**: Если `prod_ids` - это строка, применяет функцию `ensure_https_single` к строке и возвращает обработанный URL.

```
   Начало
   │
   │ prod_ids
   │
   │ Проверка типа prod_ids
   ├── Список: Применение ensure_https_single к каждому элементу
   │   │
   │   └── Возврат списка URL-адресов
   │
   └── Строка: Применение ensure_https_single к строке
   │
   └── Возврат URL-адреса
   │
   Конец
```

**Примеры**:

```python
ensure_https("example_product_id")
# Результат: 'https://www.aliexpress.com/item/example_product_id.html'

ensure_https(["example_product_id1", "https://www.aliexpress.com/item/example_product_id2.html"])
# Результат: ['https://www.aliexpress.com/item/example_product_id1.html', 'https://www.aliexpress.com/item/example_product_id2.html']

ensure_https("https://www.example.com/item/example_product_id")
# Результат: 'https://www.example.com/item/example_product_id'