# Модуль `src.suppliers.wallmart.graber`

## Обзор

Модуль содержит класс `Graber`, который используется для сбора данных о товарах с сайта `wallmart.com`. 
Класс наследует от базового класса `Graber` (из модуля `src.suppliers.graber`) и предоставляет специфическую реализацию 
функций для работы с сайтом `wallmart.com`.

## Детали

### Класс `Graber`

**Описание**: Класс для сбора данных о товарах с сайта `wallmart.com`.
**Наследует**: Класс наследует от `src.suppliers.graber.Graber`.

**Атрибуты**:

 - `supplier_prefix`: Строка, определяющая префикс поставщика (`"wallmart"`).
 - `driver`: Объект драйвера, используемого для взаимодействия с веб-страницами.
 - `lang_index`: Индекс языка.

**Методы**:

 - `__init__(self, driver: Driver, lang_index: int)`: Инициализирует экземпляр класса `Graber`.

### Принцип работы

Класс `Graber` работает следующим образом:
1. Инициализируется экземпляр класса `Graber` с указанием драйвера и индекса языка.
2. В конструкторе класса `Graber` устанавливается префикс поставщика (`supplier_prefix = "wallmart"`).
3. Вызывается конструктор родительского класса `Graber` с передачей префикса поставщика, драйвера и индекса языка.
4. Устанавливаются глобальные настройки через `Config.locator_for_decorator`.

#### Внутренние функции

 - `close_pop_up`: Декоратор для закрытия всплывающих окон перед выполнением основной логики функции.
   - **Описание**: Декоратор создает функцию-обертку для закрытия всплывающих окон перед выполнением основной логики.
   - **Параметры**:
     - `value (Any)`: Дополнительное значение для декоратора.
   - **Возвращает**:
     - `Callable`: Декоратор, оборачивающий функцию.
   - **Пример**:
     ```python
     @close_pop_up
     def my_function(param1: str) -> str:
         """Функция, которая выполняет определенное действие.
         """
         return f"Результат: {param1}"
     ```

## Параметры

 - `driver`: Объект драйвера, используемого для взаимодействия с веб-страницами.
 - `lang_index`: Индекс языка.

## Примеры

```python
from src.suppliers.wallmart.graber import Graber
from src.webdriver.driver import Driver
from src.webdriver.driver import Chrome

# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)
# Создание инстанса Graber
graber = Graber(driver, lang_index=0)