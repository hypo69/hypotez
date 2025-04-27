# Module for collecting data about goods from Bangood
=========================================================================================

This module contains the :class:`Graber` class, which is used for collecting data about goods from the `bangood.com` website. It inherits from the base class :class:`src.suppliers.graber.Graber`.

The `Graber` class provides methods for processing various fields of a product on the page. If non-standard processing of a field is required, the method can be overridden.

For each field of the product page, a field processing function is made in the parent `Graber`. If non-standard processing is needed, you can override the method here, in this class.
------------------
Before sending a request to the webdriver, you can perform preliminary actions through the decorator. 
The decorator is by default in the parent class. To make the decorator work, you need to pass a value 
to `Context.locator`. If you need to implement your own decorator, uncomment the lines with the decorator and override its behavior.
You can also implement your own decorator by uncommenting the corresponding lines of code

```rst
.. module:: src.suppliers.suppliers_list.bangood 
```

## Table of Contents

### Classes
- :class:`Graber`

### Functions
- :func:`close_pop_up` (Decorator Template)


## Classes

### `Graber`

**Description**: Class for Morlevi capture operations.

**Inherits**:
- `src.suppliers.graber.Graber`

**Attributes**:
- `supplier_prefix`: String, prefix for the supplier.

**Methods**:
- `__init__(driver: Driver, lang_index: int)`: Initializes the class for collecting product fields.
- `close_pop_up(value: Any = None)` (Decorator Template): Creates a decorator for closing pop-up windows before executing the main function logic.

```python
class Graber(Grbr):
    """Класс для операций захвата Morlevi."""
    supplier_prefix: str

    def __init__(self, driver: Driver, lang_index:int):
        """Инициализация класса сбора полей товара."""
        self.supplier_prefix = 'bangood'
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)
        # Устанавливаем глобальные настройки через Context
        
        Config.locator_for_decorator = None # <- если будет уастановлено значение - то оно выполнится в декораторе `@close_pop_up`

        
        
                ```

## Functions

### `close_pop_up` (Decorator Template)

**Purpose**: Creates a decorator for closing pop-up windows before executing the main function logic.

**Parameters**:
- `value` (Any, optional): Additional value for the decorator. Defaults to `None`.

**Returns**:
- `Callable`: Decorator wrapping the function.

**Raises**:
- `ExecuteLocatorException`: If an error occurs while executing the locator.

**How the Function Works**:
- The decorator first tries to execute the locator specified in `Context.locator.close_pop_up` to close the pop-up window.
- If successful, it then executes the main function (`func`).
- If an `ExecuteLocatorException` is caught, it logs a debug message and continues with the main function execution.

**Examples**:

```python
def close_pop_up(value: Any = None) -> Callable:
    """Создает декоратор для закрытия всплывающих окон перед выполнением основной логики функции.

    Args:
        value (Any): Дополнительное значение для декоратора.

    Returns:
        Callable: Декоратор, оборачивающий функцию.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # await Context.driver.execute_locator(Context.locator.close_pop_up)  # Await async pop-up close  
                ... 
            except ExecuteLocatorException as e:
                logger.debug(f'Ошибка выполнения локатора: {e}')
            return await func(*args, **kwargs)  # Await the main function
        return wrapper
    return decorator
```