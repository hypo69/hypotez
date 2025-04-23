# Модуль для сбора данных о товарах с AliExpress

## Обзор

Модуль предназначен для сбора данных о товарах с веб-сайта AliExpress. Он содержит класс `Graber`, который наследуется от базового класса `src.suppliers.graber.Graber` и предоставляет методы для обработки различных полей товара на странице.

## Подробней

Модуль предназначен для сбора данных о товарах с Amazon.
Класс `Graber` предоставляет методы для обработки различных полей товара на странице. В случае необходимости нестандартной обработки поля, метод может быть переопределен.

Перед отправкой запроса к веб-драйверу могут быть выполнены предварительные действия с использованием декоратора. Декоратор по умолчанию находится в родительском классе. Для активации декоратора необходимо передать значение в `Context.locator`. Также возможно реализовать свой собственный декоратор, раскомментировав соответствующие строки кода и переопределив его поведение.

## Классы

### `Graber`

**Описание**: Класс для сбора данных о товарах с AliExpress.

**Наследует**: `src.suppliers.graber.Graber`

**Атрибуты**:
- `supplier_prefix` (str): Префикс поставщика, устанавливается как `'aliexpress'`.

**Методы**:
- `__init__(self, driver: Driver, lang_index: int)`: Инициализирует класс `Graber`.

#### `__init__(self, driver: Driver, lang_index: int)`

**Назначение**: Инициализация класса сбора полей товара.

**Параметры**:
- `driver` (Driver): Экземпляр веб-драйвера для взаимодействия с браузером.
- `lang_index` (int): Индекс языка.

**Как работает функция**:

1. Устанавливает `supplier_prefix` в значение `'aliexpress'`.
2. Вызывает конструктор родительского класса `Graber` из модуля `src.suppliers.graber` с переданными параметрами `supplier_prefix`, `driver` и `lang_index`.
3. Устанавливает значение `Config.locator_for_decorator` в `None`. Это необходимо для отключения декоратора `@close_pop_up`, если он не нужен.

**Примеры**:
```python
from src.webdriver.driver import Driver, Chrome
from src.suppliers.suppliers_list.aliexpress.graber import Graber

# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)
# Создание инстанса класса Graber
graber = Graber(driver=driver, lang_index=0)
```
```python
from src.webdriver.driver import Driver, Firefox
from src.suppliers.suppliers_list.aliexpress.graber import Graber

# Создание инстанса драйвера (пример с Firefox)
driver = Driver(Firefox)

# Создание инстанса класса Graber
graber = Graber(driver=driver, lang_index=1)
```
```python
from src.webdriver.driver import Driver
from src.suppliers.suppliers_list.aliexpress.graber import Graber

# Создание инстанса класса Graber
# driver не определен
# будет ошибка
#graber = Graber(driver=driver, lang_index=1)
```
```python
from src.webdriver.driver import Driver, Chrome
from src.suppliers.suppliers_list.aliexpress.graber import Graber

# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)

# Создание инстанса класса Graber
# lang_index не определен
# будет ошибка
#graber = Graber(driver=driver)
```
```python
from src.webdriver.driver import Driver, Chrome
from src.suppliers.suppliers_list.aliexpress.graber import Graber

# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)

# Создание инстанса класса Graber
# driver.close()
# Ошибка - драйвер уже закрыт
graber = Graber(driver=driver, lang_index=1)
```
```python
from src.webdriver.driver import Driver, Chrome
from src.suppliers.suppliers_list.aliexpress.graber import Graber

# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)

# Создание инстанса класса Graber
# driver.quit()
# Ошибка - драйвер уже закрыт
graber = Graber(driver=driver, lang_index=1)