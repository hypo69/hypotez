# Модуль для извлечения идентификатора продукта из текста
## Обзор

Модуль `get_product_id.py` предназначен для извлечения идентификатора продукта из предоставленной строки. Он использует функцию `extract_prod_ids` для поиска и возврата идентификатора продукта. В случае, если идентификатор не найден, выбрасывается исключение `ProductIdNotFoundException`.

## Подробней

Этот модуль является частью системы для работы с AliExpress API и предназначен для стандартизации и упрощения процесса получения идентификаторов продуктов из различных форматов входных данных, таких как URL или просто текст.

## Функции

### `get_product_id`

```python
def get_product_id(raw_product_id: str) -> str:
    """Returns the product ID from a given text. Raises ProductIdNotFoundException on fail."""
    return extract_prod_ids(raw_product_id)
```

**Назначение**:
Извлекает и возвращает идентификатор продукта из предоставленной строки.

**Параметры**:
- `raw_product_id` (str): Строка, содержащая идентификатор продукта или информацию, из которой можно извлечь идентификатор.

**Возвращает**:
- `str`: Идентификатор продукта.

**Вызывает исключения**:
- `ProductIdNotFoundException`: Если идентификатор продукта не найден в предоставленной строке.

**Как работает функция**:
1. Функция принимает строку `raw_product_id` в качестве входных данных.
2. Вызывает функцию `extract_prod_ids` с переданной строкой.
3. Возвращает результат, полученный от `extract_prod_ids`, который должен быть идентификатором продукта.

**Примеры**:

```python
from src.suppliers.aliexpress.api.tools.get_product_id import get_product_id
from src.suppliers.aliexpress.api.errors import ProductIdNotFoundException

# Пример 1: Успешное извлечение идентификатора продукта
product_id = get_product_id("1234567890")
print(product_id)  # Вывод: 1234567890

# Пример 2: Извлечение идентификатора продукта из URL
product_id = get_product_id("https://aliexpress.com/item/1234567890.html")
print(product_id)  # Вывод: 1234567890

# Пример 3: Ошибка, если идентификатор продукта не найден
try:
    product_id = get_product_id("No product ID here")
    print(product_id)
except ProductIdNotFoundException as ex:
    print(f"Ошибка: {ex}")  # Вывод: Ошибка: Product id not found: No product ID here