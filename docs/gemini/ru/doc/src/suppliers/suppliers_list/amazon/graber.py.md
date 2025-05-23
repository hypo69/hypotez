# Модуль для сбора данных о товарах с Amazon
=========================================================================================

Модуль содержит класс :class:`Graber`, который используется для сбора данных о товарах
с веб-сайта `amazon.com`. Он наследуется от базового класса :class:`src.suppliers.graber.Graber`.

Класс `Graber` предоставляет методы для обработки различных полей товара на странице.
В случае необходимости нестандартной обработки поля, метод может быть переопределен.

Для каждого поля страницы товара сделана функция обработки поля в родительском `Graber`.
Если нужна нестандертная обработка, можно перегрузить метод здесь, в этом классе.
------------------
Перед отправкой запроса к вебдрайверу можно совершить предварительные действия через декоратор. 
Декоратор по умолчанию находится в родительском классе. Для того, чтобы декоратор сработал надо передать значение 
в `Context.locator`, Если надо реализовать свой декоратор - раскоментируйте строки с декоратором и переопределите его поведение.
Вы также можете реализовать свой собственный декоратор, раскомментировав соответствующие строки кода

```rst
.. module:: src.suppliers.suppliers_list.amazon
```

## Оглавление
* [Класс `Graber`](#класс-graber)
  * [Инициализация класса `Graber`](#инициализация-класса-graber)
  * [Декоратор `close_pop_up`](#декоратор-close_pop_up)


## Класс `Graber`
### Описание
Класс для операций захвата данных с Amazon.

**Наследует**: `src.suppliers.graber.Graber`


### Инициализация класса `Graber`

```python
    def __init__(self, driver: Driver, lang_index:int):
        """Инициализация класса сбора полей товара."""
        self.supplier_prefix = 'amazon'
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)
        # Устанавливаем глобальные настройки через Context
        
        Config.locator_for_decorator = None # <- если будет уастановлено значение - то оно выполнится в декораторе `@close_pop_up`
```
**Назначение**: Инициализирует класс `Graber`. Устанавливает префикс поставщика, вызывает конструктор родительского класса `Graber` и устанавливает глобальные настройки.

**Параметры**:
- `driver` (Driver): Объект драйвера веб-браузера.
- `lang_index` (int): Индекс языка для выбора.

**Возвращает**: `None`

**Как работает функция**:
1. Устанавливает префикс поставщика в `self.supplier_prefix` со значением `'amazon'`.
2. Вызывает конструктор родительского класса `Graber` с параметрами `supplier_prefix`, `driver` и `lang_index`.
3. Устанавливает глобальную настройку `Config.locator_for_decorator` в `None`. Если эта настройка будет установлена в декоратор `@close_pop_up`, то он выполнится.

### Декоратор `close_pop_up`

```python
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

**Назначение**: Создает декоратор для закрытия всплывающих окон перед выполнением основной логики функции.

**Параметры**:
- `value` (Any): Дополнительное значение для декоратора.

**Возвращает**: `Callable`: Декоратор, оборачивающий функцию.

**Как работает функция**:
1. Декоратор `decorator` оборачивает функцию `func`, которая передается в качестве параметра.
2. Внутри декоратора создается асинхронная обертка `wrapper`, которая выполняет следующие действия:
   - Пытается выполнить локатор `Context.locator.close_pop_up` для закрытия всплывающих окон.
   - Если возникает ошибка `ExecuteLocatorException`, то записывает сообщение об ошибке в лог.
   - Выполняет исходную функцию `func` и возвращает результат.
3. Возвращает `wrapper` в качестве декоратора.
4. Декоратор `close_pop_up` возвращает `decorator`.

**Пример использования**:

```python
@close_pop_up()
async def my_function():
    # Логика функции
    ...
```

В этом примере декоратор `@close_pop_up()` будет вызываться перед выполнением функции `my_function`. Декоратор попытается закрыть всплывающие окна, а затем выполнит исходную функцию `my_function`.