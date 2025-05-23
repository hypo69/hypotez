## Как использовать функцию `get_product_id`
=========================================================================================

Описание
-------------------------
Функция `get_product_id` предназначена для извлечения идентификатора товара из текстовой строки. Она использует функцию `extract_prod_ids` для поиска и возврата идентификатора товара.

Шаги выполнения
-------------------------
1. Функция принимает текстовую строку `raw_product_id`, которая может содержать идентификатор товара.
2. Функция `extract_prod_ids` анализирует строку `raw_product_id` с использованием регулярных выражений для поиска и извлечения идентификатора товара.
3.  Функция `get_product_id` возвращает найденный идентификатор товара, если он был найден.
4. Если идентификатор товара не найден, функция `get_product_id` выдает исключение `ProductIdNotFoundException`.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.api.tools.get_product_id import get_product_id

# Пример текста с идентификатором товара
raw_product_id = "https://www.aliexpress.com/item/10000000000000.html"

# Вызов функции для получения идентификатора товара
product_id = get_product_id(raw_product_id)

# Печать результата
print(f"Идентификатор товара: {product_id}")
```

**Важно**: 
-  В примере `product_id` - это строка с найденным идентификатором.
-  Функция `get_product_id` должна использоваться только для извлечения идентификаторов товаров. 
-  Если идентификатор товара не найден, то функция выдает исключение.