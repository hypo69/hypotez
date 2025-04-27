# Module for collecting product data from Ebay
=========================================================================================

This module contains the `Graber` class, which is used for collecting product data from the `ebay.com` website. It inherits from the base class `src.suppliers.graber.Graber`.

The `Graber` class provides methods for processing different product fields on the page. If non-standard field processing is required, the method can be overridden.

For each field on the product page, there is a field processing function in the parent `Graber`. If non-standard processing is needed, you can override the method here, in this class.
------------------
Before sending a request to the web driver, you can perform preliminary actions through a decorator.
The default decorator is in the parent class. In order for the decorator to work, you need to pass a value to `Context.locator`. If you need to implement your own decorator, uncomment the lines with the decorator and redefine its behavior.
You can also implement your own decorator by uncommenting the corresponding lines of code

```rst
.. module:: src.suppliers.suppliers_list.ebay
```

## Table of Contents

- [Classes](#classes)
    - [`Graber`](#graber)

## Classes

### `Graber`

```python
class Graber(Grbr):
    """Класс для операций захвата Morlevi."""
    supplier_prefix: str

    def __init__(self, driver: Optional['Driver'] = None, lang_index:Optional[int] = None):
        """Инициализация класса сбора полей товара."""
        self.supplier_prefix = 'ebay'
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)
        # Устанавливаем глобальные настройки через Context
        
        Config.locator_for_decorator = None # <- если будет уастановлено значение - то оно выполнится в декораторе `@close_pop_up`

                ```

**Description**: The `Graber` class is responsible for collecting product data from the `ebay.com` website. 
It inherits from the base class `src.suppliers.graber.Graber`.

**Inherits**: `src.suppliers.graber.Graber`

**Attributes**:

- `supplier_prefix` (str): Prefix for the supplier. Set to 'ebay'.

**Methods**:

- `__init__`(self, driver: Optional['Driver'] = None, lang_index:Optional[int] = None): 
    - Initializes the class.
    - Sets the `supplier_prefix` attribute to 'ebay'.
    - Calls the `__init__` method of the parent class `Grbr` with the `supplier_prefix`, `driver`, and `lang_index` arguments.
    - Sets the `Config.locator_for_decorator` attribute to `None`. This attribute is used by the `@close_pop_up` decorator to determine whether a pop-up window should be closed before the main function is executed.

## Decorator Template

```python
#           DECORATOR TEMPLATE. 
#
# def close_pop_up(value: Any = None) -> Callable:
#     """Создает декоратор для закрытия всплывающих окон перед выполнением основной логики функции.
#
#     Args:
#         value (Any): Дополнительное значение для декоратора.
#
#     Returns:
#         Callable: Декоратор, оборачивающий функцию.
#     """
#     def decorator(func: Callable) -> Callable:
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             try:
#                 # await Context.driver.execute_locator(Context.locator.close_pop_up)  # Await async pop-up close  
#                 ... 
#             except ExecuteLocatorException as e:
#                 logger.debug(f'Ошибка выполнения локатора: {e}')
#             return await func(*args, **kwargs)  # Await the main function
#         return wrapper
#     return decorator

```

**Description**: This code provides a template for a decorator function. The decorator function can be used to perform pre-execution actions, such as closing pop-up windows, before the main function is executed. 

**Parameters**:

- `value` (Any): This parameter can be used to pass additional values to the decorator.

**Returns**:

- `Callable`: This function returns a decorator function that can be used to wrap other functions.

**How the Decorator Works**:

- The `decorator` function is defined within the `close_pop_up` function. It takes a function `func` as input.
- The `wrapper` function is defined within the `decorator` function. It is an asynchronous function that is used to wrap the input function `func`.
- The `wrapper` function first tries to execute the `Context.driver.execute_locator(Context.locator.close_pop_up)` command to close a pop-up window. 
- If the command execution fails, an `ExecuteLocatorException` is caught and logged.
- Finally, the `wrapper` function calls the original function `func` and returns the result.

**Examples**:

```python
# This is an example of how to use the decorator:
@close_pop_up()
def my_function():
    # Do something
    pass
```

In this example, the `my_function` function is decorated with the `close_pop_up` decorator. This means that before the `my_function` is executed, the `close_pop_up` decorator will be called and the pop-up window will be closed.