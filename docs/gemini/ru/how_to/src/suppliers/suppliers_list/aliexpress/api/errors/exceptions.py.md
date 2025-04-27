## Как использовать модуль `src.suppliers.aliexpress.api.errors.exceptions`
=========================================================================================

### Описание
-------------------------
Модуль `src.suppliers.aliexpress.api.errors.exceptions` определяет набор пользовательских исключений для обработки ошибок, возникающих при работе с AliExpress API. Эти исключения расширяют базовый класс `AliexpressException` и предоставляют более конкретную информацию об ошибке.

### Шаги выполнения
-------------------------
1. **Импорт модуля:** Импортируйте модуль `src.suppliers.aliexpress.api.errors.exceptions` в ваш код:

   ```python
   from src.suppliers.aliexpress.api.errors.exceptions import AliexpressException, InvalidArgumentException, ProductIdNotFoundException, ApiRequestException, ApiRequestResponseException, ProductsNotFoudException, CategoriesNotFoudException, InvalidTrackingIdException
   ```

2. **Использование исключений:** В вашем коде используйте соответствующие исключения для обработки ошибок:

   * **InvalidArgumentException**: Используйте это исключение, если аргументы функции некорректны.

   * **ProductIdNotFoundException**: Используйте это исключение, если не найден идентификатор продукта.

   * **ApiRequestException**: Используйте это исключение, если запрос к AliExpress API не удался.

   * **ApiRequestResponseException**: Используйте это исключение, если ответ API не соответствует ожидаемому формату.

   * **ProductsNotFoudException**: Используйте это исключение, если не найдены продукты.

   * **CategoriesNotFoudException**: Используйте это исключение, если не найдены категории.

   * **InvalidTrackingIdException**: Используйте это исключение, если идентификатор отслеживания отсутствует или неверен.

3. **Обработка исключений:** Используйте оператор `try-except` для обработки исключений, возникающих во время работы с AliExpress API:

   ```python
   try:
       # Вызов функции, которая может вызвать исключение
       product_details = get_product_details(product_id)
   except ProductIdNotFoundException:
       print("Идентификатор продукта не найден.")
   except ApiRequestException:
       print("Произошла ошибка при запросе к API.")
   except InvalidArgumentException:
       print("Неверные аргументы для функции.")
   except Exception as ex:
       print(f"Произошла непредвиденная ошибка: {ex}")
   ```

### Пример использования
-------------------------

```python
from src.suppliers.aliexpress.api.errors.exceptions import AliexpressException, InvalidArgumentException, ProductIdNotFoundException, ApiRequestException, ApiRequestResponseException, ProductsNotFoudException, CategoriesNotFoudException, InvalidTrackingIdException

def get_product_details(product_id: str):
    """Функция для получения деталей продукта по его ID."""
    try:
        # ... логика получения данных о продукте из AliExpress API ...
        return product_details
    except ProductIdNotFoundException:
        # Обработка ошибки, если идентификатор продукта не найден
        print("Идентификатор продукта не найден.")
        raise
    except ApiRequestException:
        # Обработка ошибки, если запрос к API не удался
        print("Произошла ошибка при запросе к API.")
        raise
    except InvalidArgumentException:
        # Обработка ошибки, если аргументы функции некорректны
        print("Неверные аргументы для функции.")
        raise
    except Exception as ex:
        # Обработка непредвиденных ошибок
        print(f"Произошла непредвиденная ошибка: {ex}")
        raise

try:
    product_details = get_product_details("1234567890")
    print(product_details)
except Exception as ex:
    print(f"Ошибка: {ex}")
```