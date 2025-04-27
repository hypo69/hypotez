## Как использовать функцию `ensure_https`
=========================================================================================

Описание
-------------------------
Функция `ensure_https` проверяет, содержит ли строка URL(ы) префикс `https://`. Если ввод — это идентификатор товара, она формирует полный URL с префиксом `https://`.

Шаги выполнения
-------------------------
1. **Проверка типа входных данных:** 
    - Если `prod_ids` — это строка, то она передается в функцию `ensure_https_single` для обработки.
    - Если `prod_ids` — это список, то функция итерирует по каждому элементу списка и применяет `ensure_https_single` к каждому из них. 
2. **Обработка отдельной строки URL:** 
    - Функция `ensure_https_single` проверяет, начинается ли строка `prod_id` с `https://`.
    - Если строка начинается с `https://`, то возвращается оригинальная строка.
    - Если строка не начинается с `https://`, то функция пытается извлечь идентификатор товара из строки с помощью функции `extract_prod_ids`. 
    - Если извлечение идентификатора товара успешно, то формируется полный URL с префиксом `https://` и возвращается.
    - Если извлечение идентификатора товара не удалось, то функция выводит сообщение об ошибке в лог и возвращается оригинальная строка. 
3. **Формирование выходных данных:**
    - Если `prod_ids` — это список, то функция возвращает новый список, содержащий строки URL с префиксом `https://`.
    - Если `prod_ids` — это строка, то функция возвращает строку URL с префиксом `https://`.

Пример использования
-------------------------

```python
    # Пример 1: Обработка одиночного идентификатора товара
    product_id = "example_product_id"
    url_with_https = ensure_https(product_id)
    print(url_with_https)  # Вывод: https://www.aliexpress.com/item/example_product_id.html

    # Пример 2: Обработка списка идентификаторов товаров
    product_ids = ["example_product_id1", "example_product_id2"]
    urls_with_https = ensure_https(product_ids)
    print(urls_with_https)  # Вывод: ['https://www.aliexpress.com/item/example_product_id1.html', 'https://www.aliexpress.com/item/example_product_id2.html']

    # Пример 3: Обработка списка, содержащего URL с префиксом https://
    product_ids = ["example_product_id1", "https://www.aliexpress.com/item/example_product_id2.html"]
    urls_with_https = ensure_https(product_ids)
    print(urls_with_https)  # Вывод: ['https://www.aliexpress.com/item/example_product_id1.html', 'https://www.aliexpress.com/item/example_product_id2.html']
```