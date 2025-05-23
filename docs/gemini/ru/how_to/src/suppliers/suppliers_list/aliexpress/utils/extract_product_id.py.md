## Как использовать функцию `extract_prod_ids`
=========================================================================================

Описание
-------------------------
Функция `extract_prod_ids` извлекает идентификаторы товаров (`product_id`) из списка URL-адресов или из отдельных URL-адресов. 
Если в качестве аргумента переданы непосредственно идентификаторы товаров, функция возвращает их без изменений.

Шаги выполнения
-------------------------
1. **Проверка типа входных данных**:  
    - Если функция получает список URL-адресов (`list[str]`), то она перебирает каждый URL и извлекает идентификатор.
    - Если функция получает отдельный URL (`str`), она извлекает идентификатор из него.
    - Если функция получает `product_id` в виде строки (`str`), она возвращает его без изменений.
2. **Извлечение идентификатора**: 
    - Функция использует регулярное выражение (`pattern = re.compile(r"(?:item/|/)?(\\d+)\\.html)`) для поиска идентификатора товара в URL-адресе.
    - Если идентификатор найден, функция возвращает его. 
    - Если идентификатор не найден, функция возвращает `None`.
3. **Обработка списка**: 
    - Если функция получает список URL-адресов (`list[str]`), она возвращает новый список, содержащий только найденные идентификаторы.
    - Если в списке нет найденных идентификаторов, функция возвращает `None`.

Пример использования
-------------------------

```python
    # Извлечение идентификатора из одного URL-адреса
    url = "https://www.aliexpress.com/item/123456.html"
    product_id = extract_prod_ids(url)
    print(f"Product ID: {product_id}")  # Output: Product ID: 123456

    # Извлечение идентификаторов из списка URL-адресов
    urls = ["https://www.aliexpress.com/item/123456.html", "https://www.aliexpress.com/item/7891011.html"]
    product_ids = extract_prod_ids(urls)
    print(f"Product IDs: {product_ids}") # Output: Product IDs: ['123456', '7891011']

    # Передача идентификатора товара напрямую
    product_id = "7891011"
    extracted_id = extract_prod_ids(product_id)
    print(f"Extracted ID: {extracted_id}")  # Output: Extracted ID: 7891011

    # URL, из которого нельзя извлечь идентификатор
    url = "https://www.example.com/item/abcdef.html"
    product_id = extract_prod_ids(url)
    print(f"Product ID: {product_id}")  # Output: Product ID: None
```