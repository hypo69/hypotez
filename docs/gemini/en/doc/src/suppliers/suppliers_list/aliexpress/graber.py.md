# Module for Collecting Product Information from AliExpress
## Overview

This module contains the `Graber` class, used to collect product information from the `aliexpress.com` website. It inherits from the base class `src.suppliers.graber.Graber`.

The `Graber` class provides methods for handling different product fields on the page. If a field requires non-standard processing, its method can be overridden.

Before sending a request to the web driver, preliminary actions can be performed using a decorator. The default decorator is located in the parent class. To activate the decorator, you need to pass a value to `Context.locator`. It is also possible to implement your own decorator by uncommenting the corresponding lines of code and overriding its behavior.


## Details
This module implements the `Graber` class which is responsible for scraping product data from AliExpress. The class inherits from the base `Graber` class, providing a framework for common scraping operations.

## Classes

### `Graber`
**Description**: Класс для сбора данных о товарах с AliExpress.


**Inherits**:
    - `src.suppliers.graber.Graber`
    - Базовый класс для сбора данных о товарах с различных платформ.

**Attributes**:
    - `supplier_prefix` (str): Префикс поставщика, в данном случае "aliexpress".

**Methods**:
    - `__init__(self, driver: Driver, lang_index: int)`: Инициализирует класс `Graber`, устанавливает префикс поставщика и инициализирует родительский класс.

## Functions

### `close_pop_up`
**Purpose**: Создает декоратор для закрытия всплывающих окон перед выполнением основной логики функции.

**Parameters**:
    - `value`: Дополнительное значение для декоратора.
    - `func`: Функция, которую нужно обернуть декоратором.

**Returns**:
    - `Callable`: Декоратор, оборачивающий функцию.

**Raises Exceptions**:
    - `ExecuteLocatorException`: Возникает при ошибке выполнения локатора.

**How the Function Works**:
    - Декоратор проверяет наличие локатора для закрытия всплывающего окна в `Config.locator_for_decorator`.
    - Если локатор найден, декоратор выполняет его с помощью `Context.driver.execute_locator`.
    - После успешного закрытия всплывающего окна декоратор вызывает основную функцию.
    - В случае ошибки выполнения локатора, декоратор логирует ошибку и продолжает выполнение основной функции.

**Examples**:
    ```python
    # Пример использования декоратора
    @close_pop_up()
    async def my_function():
        # Выполнение основной логики функции
        pass

    # Вызов функции
    await my_function()
    ```

## Parameter Details

- `driver` (`Driver`): Экземпляр веб-драйвера для взаимодействия с браузером.
- `lang_index` (`int`): Индекс языка, используемый для сбора данных.

## Examples

```python
# Создание экземпляра класса Graber
driver = Driver(Chrome)  # Создаем экземпляр веб-драйвера (в данном случае Chrome)
graber = Graber(driver, lang_index=0)  # Инициализируем Graber с веб-драйвером и индексом языка

# Вызов метода для получения информации о товаре
product_data = graber.get_product_info(product_url='https://www.aliexpress.com/item/10050012345678.html')

# Обработка полученных данных
print(product_data)  # Вывод данных о товаре
```