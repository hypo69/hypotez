### **Как использовать этот блок кода**

=========================================================================================

Описание
-------------------------
Этот блок кода определяет набор пользовательских исключений для работы с AliExpress API.
Он включает базовый класс `AliexpressException` и несколько подклассов, каждый из которых представляет конкретную ошибку,
которая может возникнуть при взаимодействии с API AliExpress.

Шаги выполнения
-------------------------
1. **Определение базового класса `AliexpressException`**:
   - Создается класс `AliexpressException`, который наследуется от стандартного класса `Exception`.
   - Конструктор `__init__` принимает аргумент `reason: str`, который сохраняется в атрибуте `self.reason`.
   - Метод `__str__` переопределен для возврата строки с описанием причины исключения.

2. **Определение подклассов исключений**:
   - `InvalidArgumentException`: Вызывается, когда аргументы, переданные в API, некорректны.
   - `ProductIdNotFoundException`: Вызывается, если ID товара не найден.
   - `ApiRequestException`: Вызывается, если запрос к AliExpress API завершается неудачей.
   - `ApiRequestResponseException`: Вызывается, если ответ на запрос к AliExpress API невалиден.
   - `ProductsNotFoudException`: Вызывается, если товары не найдены.
   - `CategoriesNotFoudException`: Вызывается, если категории не найдены.
   - `InvalidTrackingIdException`: Вызывается, если ID отслеживания отсутствует или невалиден.

3. **Использование исключений в коде**:
   - Для каждой конкретной ситуации, когда может возникнуть ошибка, вызывается соответствующее исключение.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.api.errors.exceptions import (
    AliexpressException,
    InvalidArgumentException,
    ProductIdNotFoundException,
    ApiRequestException,
    ApiRequestResponseException,
    ProductsNotFoudException,
    CategoriesNotFoudException,
    InvalidTrackingIdException
)

def get_product_details(product_id: str) -> dict:
    """
    Функция пытается получить детали товара по его ID.

    Args:
        product_id (str): ID товара.

    Returns:
        dict: Детали товара, если товар найден.

    Raises:
        ProductIdNotFoundException: Если товар с указанным ID не найден.
        ApiRequestException: Если запрос к API завершается неудачей.
    """
    if not product_id:
        raise InvalidArgumentException("Product ID cannot be empty.")

    try:
        # Имитация запроса к API
        if product_id == "12345":
            product_details = {"id": "12345", "name": "Example Product"}
        else:
            raise ProductIdNotFoundException(f"Product with ID {product_id} not found.")
        return product_details
    except ProductIdNotFoundException as e:
        raise e
    except Exception as e:
        raise ApiRequestException(f"Failed to get product details: {e}")

try:
    product = get_product_details("123")
    print(product)
except ProductIdNotFoundException as e:
    print(f"Error: {e}")
except ApiRequestException as e:
    print(f"Error: {e}")
except InvalidArgumentException as e:
    print(f"Error: {e}")
```