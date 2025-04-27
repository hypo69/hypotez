# Обеспечение HTTPS-префикса для URL-адресов

## Обзор

Модуль `ensure_https.py` предназначен для обеспечения того, чтобы все предоставленные URL-строки содержали префикс `https://`. Если на входе указан идентификатор товара, то он строит полный URL с префиксом `https://`.

## Подробности

Модуль используется для проверки URL-адресов на наличие HTTPS-префикса и добавления его, если он отсутствует. Он также обрабатывает идентификаторы товаров, преобразуя их в полные URL с HTTPS-префиксом.

## Функции

### `ensure_https`

**Назначение**: Обеспечивает наличие HTTPS-префикса в URL-строке или списке URL-строк. Если на входе указан идентификатор товара, то он строит полный URL с HTTPS-префиксом.

**Параметры**:

- `prod_ids` (str | list[str]): URL-строка или список URL-строк для проверки и изменения (если необходимо).

**Возвращает**:

- str | list[str]: URL-строка или список URL-строк с префиксом `https://`.

**Возможные исключения**:

- `ValueError`: Если `prod_ids` является экземпляром `WindowsPath`.

**Примеры**:

```python
>>> ensure_https("example_product_id")
'https://www.aliexpress.com/item/example_product_id.html'

>>> ensure_https(["example_product_id1", "https://www.aliexpress.com/item/example_product_id2.html"])
['https://www.aliexpress.com/item/example_product_id1.html', 'https://www.aliexpress.com/item/example_product_id2.html']

>>> ensure_https("https://www.example.com/item/example_product_id")
'https://www.example.com/item/example_product_id'
```

**Внутренние функции**:

#### `ensure_https_single`

**Назначение**: Обеспечивает наличие HTTPS-префикса в единственной URL-строке или строке идентификатора товара.

**Параметры**:

- `prod_id` (str): URL-строка или строка идентификатора товара.

**Возвращает**:

- str: URL-строка с префиксом `https://`.

**Возможные исключения**:

- `ValueError`: Если `prod_id` является экземпляром `WindowsPath`.

**Примеры**:

```python
>>> ensure_https_single("example_product_id")
'https://www.aliexpress.com/item/example_product_id.html'

>>> ensure_https_single("https://www.example.com/item/example_product_id")
'https://www.example.com/item/example_product_id'
```

**Как работает функция**:

1. Вызывается функция `extract_prod_ids`, чтобы получить идентификатор товара из предоставленной строки.
2. Если идентификатор товара найден, то функция строит полный URL с префиксом `https://` и возвращает его.
3. Если идентификатор товара не найден, то функция возвращает исходную строку.

**Примеры**:

```python
>>> ensure_https("example_product_id")
'https://www.aliexpress.com/item/example_product_id.html'
```

В этом случае функция `extract_prod_ids` извлекает идентификатор товара `example_product_id` из исходной строки. Затем функция `ensure_https_single` строит полный URL с префиксом `https://` и возвращает его.

```python
>>> ensure_https("https://www.example.com/item/example_product_id")
'https://www.example.com/item/example_product_id'
```

В этом случае функция `extract_prod_ids` не находит идентификатора товара, так как исходная строка уже является полным URL. Поэтому функция `ensure_https_single` просто возвращает исходную строку.

## Примеры

```python
# Пример использования
url = "example_product_id"
url_with_https = ensure_https(url)
print(url_with_https)  # Вывод: https://www.aliexpress.com/item/example_product_id.html

urls = ["example_product_id1", "https://www.aliexpress.com/item/example_product_id2.html"]
urls_with_https = ensure_https(urls)
print(urls_with_https)  # Вывод: ['https://www.aliexpress.com/item/example_product_id1.html', 'https://www.aliexpress.com/item/example_product_id2.html']
```

## Дополнительная информация

- Модуль использует функцию `extract_prod_ids` из модуля `extract_product_id`.
- Модуль использует модуль `logger` для вывода сообщений об ошибках.

## Использование Webdriver

В модуле `ensure_https.py` не используется `webdriver`.