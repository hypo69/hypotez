# Модуль визуального сбора данных VisualDG

## Обзор

Модуль `src.suppliers.visualdg.graber.py` - это класс для сбора значений полей на странице товара `visualdg.co.il`.  

## Подробней

Класс `Graber` - это класс для работы с сайтом `visualdg.co.il`. Он наследует функциональность от `Graber` и имеет несколько переопределенных функций для работы с данным поставщиком.  

- Для каждого поля страницы товара определена функция обработки. 
- **Декоратор** позволяет выполнять предварительные действия перед отправкой запроса к вебдрайверу.  

## Классы

### `Graber`

**Описание**: Класс для операций захвата Morlevi.

**Наследует**: `Graber` (Родительский класс с общими функциями для сбора данных)

**Атрибуты**:

- `supplier_prefix`: Строковый префикс для поставщика,  в данном случае `visualdg`.

**Методы**:

- `__init__`: Инициализация класса. Устанавливает префикс поставщика и наследует инициализацию от родительского класса. 

## Функции

### `close_pop_up`

**Назначение**: Декоратор для закрытия всплывающих окон перед выполнением основной логики функции.

**Параметры**:

- `value`: Дополнительное значение для декоратора (не используется).

**Возвращает**: 

- `Callable`: Декоратор, оборачивающий функцию. 

**Пример**:
```python
# Предположим, что  есть функция 'process_data', которую мы хотим обернуть декоратором:
from src.webdriver.driver import Driver
from src.logger.logger import logger
from src.suppliers.graber import Graber as Grbr, Config, close_pop_up

class Graber(Grbr):
    # ...

    @close_pop_up
    def process_data(self, some_value: Any) -> None:
        """Обработка данных."""
        # ... 
```

**Как работает**: 

- Декоратор `@close_pop_up`  оборачивает функцию `process_data`. 
- Перед выполнением `process_data`, декоратор пытается выполнить `close_pop_up` (`Context.locator.close_pop_up`). 
- Если при этом возникнет ошибка (`ExecuteLocatorException`), то она логируется через `logger.debug`.
- После закрытия pop-up окна, запускается функция `process_data`.


**Примеры**: 
```python
# Примеры использования декоратора:
from src.webdriver.driver import Driver
from src.logger.logger import logger
from src.suppliers.graber import Graber as Grbr, Config, close_pop_up

# ... 

    @close_pop_up
    def get_title(self, data: Any) -> str:
        """Функция для получения заголовка страницы. """
        # ...

    @close_pop_up
    def get_price(self, data: Any) -> str:
        """Функция для получения цены. """
        # ... 

    @close_pop_up
    def get_description(self, data: Any) -> str:
        """Функция для получения описания. """
        # ... 

```


## Параметры 

### `Config.locator_for_decorator`

**Описание**: Локатор для закрытия всплывающих окон. Если значение установлено, то декоратор `@close_pop_up`  будет выполнять его перед запуском целевой функции.


## Примеры

```python
# Создание инстанса драйвера (пример с Chrome):
driver = Driver(Chrome)

# Создание инстанса Graber:
graber = Graber(driver)

# Вызов функции для сбора данных:
graber.get_title(data)