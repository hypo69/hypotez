### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода определяет класс `Graber`, который используется для сбора данных о товарах с веб-сайта Banggood. Он наследуется от базового класса `Graber` из модуля `src.suppliers.graber`. Класс `Graber` предоставляет методы для обработки различных полей товара на странице.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей и классов**:
   - Импортируются модули `typing`, `SimpleNamespace`, `header`, `src.suppliers.graber`, `src.webdriver.driver` и `src.logger.logger`.
2. **Определение класса `Graber`**:
   - Класс `Graber` наследуется от `Graber` (переименованного как `Grbr`) из модуля `src.suppliers.graber`.
   - Определяется атрибут класса `supplier_prefix`, который указывает на префикс поставщика (в данном случае, 'bangood').
3. **Инициализация класса `Graber`**:
   - В методе `__init__` устанавливается значение `supplier_prefix` равным 'bangood'.
   - Вызывается конструктор родительского класса `Grbr` с передачей `supplier_prefix`, объекта `driver` и `lang_index`.
   - Устанавливается `Config.locator_for_decorator = None`, что отключает выполнение декоратора `@close_pop_up`.

Пример использования
-------------------------

```python
from src.webdriver.driver import Driver
from src.suppliers.suppliers_list.bangood.graber import Graber

# Пример использования класса Graber
driver = Driver("chrome")  # Инициализация веб-драйвера (например, Chrome)
lang_index = 0  # Индекс языка (например, 0 для первого языка)
graber = Graber(driver, lang_index)  # Создание экземпляра класса Graber

# Теперь можно использовать методы graber для сбора данных о товарах с Banggood
# graber.grab_product_data()
```