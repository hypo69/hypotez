### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода определяет класс `Graber`, который наследуется от класса `Graber` (под псевдонимом `Grbr`) из модуля `src.suppliers.graber`. Класс `Graber` предназначен для сбора информации о товарах с сайта `wallashop.co.il`. Он инициализируется с использованием веб-драйвера и индекса языка. Класс также включает функциональность для закрытия всплывающих окон с использованием декоратора.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `typing`, `SimpleNamespace`, `header`, `Graber` (под псевдонимом `Grbr`), `Config`, `close_pop_up`, `Driver` и `logger`.
2. **Определение класса `Graber`**:
   - Класс `Graber` наследуется от класса `Grbr`.
   - Определяется атрибут класса `supplier_prefix` со значением `'wallashop'`.
3. **Инициализация класса `Graber` в методе `__init__`**:
   - Метод `__init__` принимает аргументы `driver` (экземпляр веб-драйвера) и `lang_index` (индекс языка).
   - Вызывается конструктор родительского класса `Grbr` с передачей `supplier_prefix`, `driver` и `lang_index`.
   - Устанавливается `Config.locator_for_decorator` в `None`, что отключает выполнение декоратора `@close_pop_up`.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.wallashop.graber import Graber
from src.webdriver.driver import Driver
from src.webdriver.drivers.firefox import Firefox

# Инициализация веб-драйвера (например, Firefox)
driver = Driver(Firefox)

# Создание экземпляра класса Graber для Wallashop
wallashop_graber = Graber(driver=driver, lang_index=0)

# Теперь можно использовать методы класса wallashop_graber для сбора информации о товарах с сайта wallashop.co.il
# Например, можно вызвать методы для получения названия товара, цены и т.д.
# product_data = wallashop_graber.get_product_data()

# Закрытие веб-драйвера после завершения работы
# driver.close()
```
```python
from typing import Optional, Any
from types import SimpleNamespace

from src.suppliers.graber import Graber as Grbr, Config, close_pop_up
from src.webdriver.driver import Driver
from src.logger.logger import logger


class Graber(Grbr):
    """Класс для операций захвата Wallashop."""
    supplier_prefix: str

    def __init__(self, driver: Driver, lang_index:int):
        """Инициализация класса сбора полей товара.

        Args:
            driver (Driver): Экземпляр веб-драйвера.
            lang_index (int): Индекс языка.
        """
        # Функция устанавливает префикс поставщика
        self.supplier_prefix = 'wallashop'
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)

        # Закрыватель поп ап `@close_pop_up`
        # если будет уастановлено значение - то оно выполнится в декораторе `@close_pop_up`
        Config.locator_for_decorator = None