# Модуль для сбора данных о товарах с Gearbest

## Обзор

Модуль содержит класс `Graber`, предназначенный для сбора информации о товарах с веб-сайта `gearbest.com`. Он наследуется от базового класса `src.suppliers.graber.Graber` и предоставляет методы для обработки различных полей товара на странице. В случае необходимости нестандартной обработки поля, метод может быть переопределен.

## Подробнее

Этот модуль является частью системы для сбора данных о товарах от различных поставщиков. Он специализируется на парсинге данных с сайта `gearbest.com`. Класс `Graber` содержит логику для извлечения информации о товарах, такую как наименование, цена, описание и характеристики.

## Классы

### `Graber`

**Описание**: Класс для сбора данных о товарах с веб-сайта `gearbest.com`.

**Наследует**:
- `src.suppliers.graber.Graber`: Базовый класс для сбора данных о товарах с веб-сайтов поставщиков.

**Атрибуты**:
- `supplier_prefix` (str): Префикс поставщика, используется для идентификации поставщика в системе.

**Методы**:
- `__init__(driver: Optional['Driver']]=None, lang_index:Optional[int] = None)`: Инициализирует экземпляр класса `Graber`.

### `__init__`

```python
 def __init__(self, driver: Optional['Driver'] = None, lang_index:Optional[int] = None):
        """Инициализация класса сбора полей товара.
        Args:
            driver (Optional['Driver'], optional): Экземпляр веб-драйвера для управления браузером. По умолчанию `None`.
            lang_index (Optional[int], optional): Индекс языка. По умолчанию `None`.

        """
```
**Назначение**: Инициализация класса `Graber`.

**Параметры**:
- `driver` (Optional['Driver'], optional): Экземпляр веб-драйвера для управления браузером. По умолчанию `None`.
- `lang_index` (Optional[int], optional): Индекс языка. По умолчанию `None`.

**Как работает функция**:
- Функция инициализирует класс `Graber`, устанавливая префикс поставщика (`supplier_prefix`) как `etzmaleh`.
- Вызывает конструктор родительского класса `Grbr` с указанным префиксом поставщика, драйвером и индексом языка.
- Устанавливает `Config.locator_for_decorator` в `None`, что отключает выполнение декоратора `@close_pop_up`.

**Примеры**:
```python
# Пример инициализации класса Graber с использованием веб-драйвера Firefox
from src.webdriver.driver import Driver, Firefox
driver = Driver(Firefox)
graber = Graber(driver=driver)

# Пример инициализации класса Graber без веб-драйвера
graber = Graber()
```
```python

#     DECORATOR TEMPLATE. 
#
# def close_pop_up(value: Any = None) -> Callable:
#     """Создает декоратор для закрытия всплывающих окон перед выполнением основной логики функции.
#     Args:
#         value (Any): Дополнительное значение для декоратора.
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
**Описание**: Шаблон декоратора для закрытия всплывающих окон перед выполнением основной логики функции.

**Параметры**:
- `value` (Any): Дополнительное значение для декоратора.

**Возвращает**:
- `Callable`: Декоратор, оборачивающий функцию.

**Как работает функция**:
- Функция создает декоратор, который пытается закрыть всплывающее окно перед выполнением основной логики функции.
- Если выполнение локатора завершается с ошибкой, в лог записывается отладочное сообщение.
- Возвращает результат выполнения основной функции.

**Примеры**:
```python
# Пример использования декоратора
# @close_pop_up()
# async def my_function():
#     ...
```
```python
    def __init__(self, driver: Optional['Driver'] = None, lang_index:Optional[int] = None):
        """Инициализация класса сбора полей товара."""
        self.supplier_prefix = 'etzmaleh'
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)
        # Устанавливаем глобальные настройки через Context
        
        Config.locator_for_decorator = None # <- если будет уастановлено значение - то оно выполнится в декораторе `@close_pop_up`
```
## Параметры класса

- `driver` (Optional['Driver'], optional): Экземпляр веб-драйвера для управления браузером. По умолчанию `None`.
- `lang_index` (Optional[int], optional): Индекс языка. По умолчанию `None`.