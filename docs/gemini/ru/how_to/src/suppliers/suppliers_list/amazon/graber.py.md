### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода определяет класс `Graber`, предназначенный для сбора данных о товарах с веб-сайта Amazon. Он наследуется от базового класса `Graber` из модуля `src.suppliers.graber` и предоставляет методы для обработки различных полей товара на странице Amazon. В классе `Graber` можно переопределять методы для нестандартной обработки полей товара.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `typing`, `SimpleNamespace`, `header`, `Graber` из `src.suppliers.graber`, `Driver` из `src.webdriver.driver` и `logger` из `src.logger.logger`.

2. **Определение класса `Graber`**:
   - Класс `Graber` наследуется от `Grbr` (родительский класс Graber) и предназначен для сбора данных о товарах с Amazon.
   - Определяется атрибут класса `supplier_prefix`, который указывает на префикс поставщика (в данном случае 'amazon').

3. **Инициализация класса `Graber`**:
   - Метод `__init__` инициализирует класс `Graber`, принимая экземпляр `Driver` и `lang_index` в качестве аргументов.
   - Вызывается конструктор родительского класса `Grbr` с указанием префикса поставщика, драйвера и индекса языка.
   - Устанавливается значение `Config.locator_for_decorator` в `None`, чтобы отключить выполнение декоратора `@close_pop_up` по умолчанию. Если необходимо выполнение декоратора, нужно установить значение `Config.locator_for_decorator` на нужный локатор.

Пример использования
-------------------------

```python
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
from src.suppliers.suppliers_list.amazon.graber import Graber

# Инициализация драйвера (например, Firefox)
driver = Driver(Firefox)

# Создание экземпляра класса Graber для Amazon
amazon_graber = Graber(driver=driver, lang_index=1)

# Теперь можно использовать методы amazon_graber для сбора данных о товарах с Amazon
# Например:
# product_data = amazon_graber.get_product_data(url="https://www.amazon.com/...")
```