### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код определяет асинхронный класс `PrestaCategoryAsync` для управления категориями в PrestaShop, а также функцию `get_parent_categories_list_async`, которая асинхронно извлекает родительские категории для заданной категории.

Шаги выполнения
-------------------------
1. **Инициализация класса `PrestaCategoryAsync`**:
   - При создании экземпляра класса `PrestaCategoryAsync` необходимо передать либо словарь `credentials`, содержащий `api_domain` и `api_key`, либо отдельные параметры `api_domain` и `api_key`.
   - Выполняется проверка наличия `api_domain` и `api_key`. Если они отсутствуют, выбрасывается исключение `ValueError`.
   - Инициализируется родительский класс `PrestaShopAsync` с переданными `api_domain` и `api_key`.

2. **Вызов метода `get_parent_categories_list_async`**:
   - Метод принимает `id_category` (идентификатор категории) и опциональный список `additional_categories_list` (дополнительные категории для обработки).
   - `id_category` преобразуется в целое число. Если преобразование не удаётся, регистрируется ошибка и выполнение продолжается.
   - `additional_categories_list` преобразуется в список, если это не список. `id_category` добавляется в этот список.
   - Создаётся пустой список `out_categories_list` для хранения родительских категорий.
   - Итерируемся по списку `additional_categories_list`. Для каждой категории:
     - Асинхронно вызывается метод `read` родительского класса `PrestaShopAsync` для получения информации о категории. Если происходит ошибка, она регистрируется, и происходит переход к следующей итерации.
     - Если полученный `parent` меньше или равен 2, функция возвращает накопленный список `out_categories_list` (так как дерево категорий начинается с 2, это означает, что достигнута корневая категория).
     - `parent` добавляется в `out_categories_list`.

3. **Завершение работы функции `get_parent_categories_list_async`**:
   - После обработки всех категорий из `additional_categories_list`, функция возвращает список `out_categories_list`, содержащий идентификаторы родительских категорий.

Пример использования
-------------------------

```python
import asyncio
from types import SimpleNamespace
from src.endpoints.prestashop.category_async import PrestaCategoryAsync
from src.logger.logger import logger

async def main():
    # Пример использования класса PrestaCategoryAsync и его методов
    credentials = SimpleNamespace(api_domain="your_api_domain", api_key="your_api_key")
    category_manager = PrestaCategoryAsync(credentials=credentials)

    try:
        # Пример получения родительских категорий для категории с ID 3
        parent_categories = await category_manager.get_parent_categories_list_async(id_category=3)
        logger.info(f"Родительские категории: {parent_categories}")
    except ValueError as ve:
        logger.error(f"Ошибка инициализации: {ve}")
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())