# Модуль `ensure_https`

## Обзор

Модуль `ensure_https` обеспечивает добавление префикса `https://` к предоставленному URL-адресу или списку URL-адресов. 
Если в качестве входных данных используется ID товара, то он строит полный URL с префиксом `https://`.

## Подробнее

Этот модуль используется в системе для обработки URL-адресов, поступающих из различных источников. 
Он гарантирует, что все URL-адреса имеют правильный протокол (`https`) перед обработкой. 
Это необходимо для обеспечения безопасности и правильной работы системы.

## Функции

### `ensure_https`

**Назначение**: Обеспечивает наличие префикса `https://` в предоставленной строке URL или списке строк URL.
Если в качестве входных данных используется ID товара, то он строит полный URL с префиксом `https://`.

**Параметры**:

- `prod_ids` (str | list[str]): Строка URL или список строк URL для проверки и, при необходимости, изменения.

**Возвращает**:

- `str | list[str]`: Строка URL или список строк URL с префиксом `https://`.

**Вызывает исключения**:

- `ValueError`: Если `prod_ids` является экземпляром `WindowsPath`.

**Как работает функция**:

- Функция `ensure_https` принимает на вход строку URL или список строк URL.
- Она проверяет, содержит ли URL префикс `https://`.
- Если URL не содержит префикс `https://`, функция добавляет его.
- Если в качестве входных данных используется ID товара, функция `ensure_https` строит полный URL с префиксом `https://`, используя ID товара.
- Для обработки списка строк URL функция `ensure_https` использует функцию `ensure_https_single` для каждой строки в списке.

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

**Назначение**: Обеспечивает, чтобы строка URL или ID товара имела префикс `https://`.

**Параметры**:

- `prod_id` (str): Строка URL или ID товара.

**Возвращает**:

- `str`: Строка URL с префиксом `https://`.

**Вызывает исключения**:

- `ValueError`: Если `prod_id` является экземпляром `WindowsPath`.

**Как работает функция**:

- Функция `ensure_https_single` принимает на вход строку URL или ID товара.
- Она проверяет, содержит ли URL префикс `https://`.
- Если URL не содержит префикс `https://`, функция добавляет его.
- Если в качестве входных данных используется ID товара, функция `ensure_https_single` строит полный URL с префиксом `https://`, используя ID товара.

**Примеры**:

```python
>>> ensure_https_single("example_product_id")
'https://www.aliexpress.com/item/example_product_id.html'

>>> ensure_https_single("https://www.example.com/item/example_product_id")
'https://www.example.com/item/example_product_id'
```

## Параметры класса

- `prod_id` (str): ID товара.
- `prod_ids` (str | list[str]): Строка URL или список строк URL.

**Примеры**:

```python
# Пример использования ID товара
prod_id = "example_product_id"
url_with_https = ensure_https(prod_id)
print(url_with_https)  # Вывод: https://www.aliexpress.com/item/example_product_id.html

# Пример использования списка URL-адресов
urls = ["example_product_id1", "https://www.aliexpress.com/item/example_product_id2.html"]
urls_with_https = ensure_https(urls)
print(urls_with_https)  # Вывод: ['https://www.aliexpress.com/item/example_product_id1.html', 'https://www.aliexpress.com/item/example_product_id2.html']
```