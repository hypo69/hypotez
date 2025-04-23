### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода содержит функции для обработки аргументов, используемых в API AliExpress. Он включает функции для преобразования списков в строки и извлечения ID товаров из различных типов входных данных.

Шаги выполнения
-------------------------
1. **`get_list_as_string(value)`**:
   - Функция `get_list_as_string` преобразует входное значение в строку, если это возможно.
   - Если значение `None`, функция возвращает `None`.
   - Если значение является строкой (`str`), функция возвращает эту строку без изменений.
   - Если значение является списком (`list`), функция объединяет элементы списка в строку, разделяя их запятыми.
   - Если значение не является ни строкой, ни списком, функция вызывает исключение `InvalidArgumentException`.

2. **`get_product_ids(values)`**:
   - Функция `get_product_ids` извлекает и возвращает список ID товаров из входных значений.
   - Если входное значение является строкой (`str`), функция разделяет строку на список ID товаров, используя запятую в качестве разделителя.
   - Если входное значение не является ни строкой, ни списком, функция вызывает исключение `InvalidArgumentException`.
   - Затем функция итерируется по каждому значению в списке и использует функцию `get_product_id` для извлечения ID товара.
   - Все извлеченные ID товаров добавляются в список `product_ids`, который возвращается в конце функции.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.api.helpers.arguments import get_list_as_string, get_product_ids
from src.suppliers.suppliers_list.aliexpress.api.errors.exceptions import InvalidArgumentException

# Пример использования get_list_as_string
list_value = ['товар1', 'товар2', 'товар3']
string_value = get_list_as_string(list_value)
print(f"Строка из списка: {string_value}")  # Вывод: Строка из списка: товар1,товар2,товар3

string_value = get_list_as_string("товар4")
print(f"Строка из строки: {string_value}")  # Вывод: Строка из строки: товар4

none_value = get_list_as_string(None)
print(f"Строка из None: {none_value}")  # Вывод: Строка из None: None

try:
    invalid_value = get_list_as_string(123)
except InvalidArgumentException as e:
    print(f"Ошибка: {e}")  # Вывод: Ошибка: Argument should be a list or string: 123

# Пример использования get_product_ids
product_ids_string = "12345,67890,11223"
product_ids_list = get_product_ids(product_ids_string)
print(f"ID товаров из строки: {product_ids_list}")

product_ids_list = ['12345', '67890', '11223']
product_ids_list = get_product_ids(product_ids_list)
print(f"ID товаров из списка: {product_ids_list}")

try:
    invalid_value = get_product_ids(123)
except InvalidArgumentException as e:
    print(f"Ошибка: {e}")  # Вывод: Ошибка: Argument product_ids should be a list or string