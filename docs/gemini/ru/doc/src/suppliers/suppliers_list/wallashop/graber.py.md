# Модуль `src.suppliers.suppliers_list.wallashop.graber`

## Обзор

Модуль содержит класс `Graber`, предназначенный для сбора информации о товарах с сайта `wallashop.co.il`. Он наследует функциональность основного класса `Graber` и переопределяет методы для специфической обработки данных с этого сайта. Модуль предоставляет механизм для выполнения предварительных действий перед отправкой запросов к веб-драйверу через декораторы.

## Подробнее

Этот модуль является частью системы для сбора данных о товарах с различных онлайн-магазинов. Он специализируется на сайте `wallashop.co.il`, адаптируя общие механизмы сбора данных под особенности структуры и контента этого сайта. Важной особенностью является возможность предварительной обработки данных с использованием декораторов, что позволяет выполнять дополнительные действия перед извлечением информации.

## Классы

### `Graber`

**Описание**: Класс `Graber` предназначен для захвата данных о товарах с сайта `wallashop.co.il`.

**Наследует**:
- `Graber` (как `Grbr`) из модуля `src.suppliers.graber`: Предоставляет базовую функциональность для сбора данных о товарах.

**Атрибуты**:
- `supplier_prefix` (str): Префикс поставщика, устанавливается как `wallashop`.

**Методы**:
- `__init__(driver: Driver, lang_index: int)`: Инициализирует экземпляр класса, устанавливает префикс поставщика и вызывает конструктор родительского класса.

### `__init__`

**Назначение**: Инициализация экземпляра класса `Graber`.

**Параметры**:
- `driver` (Driver): Экземпляр веб-драйвера для взаимодействия с сайтом.
- `lang_index` (int): Индекс языка, используемый при сборе данных.

**Как работает функция**:
- Устанавливает атрибут `supplier_prefix` в значение `wallashop`.
- Вызывает конструктор родительского класса `Graber` (как `Grbr`) с установленным префиксом поставщика, драйвером и индексом языка.
- Инициализирует `Config.locator_for_decorator` значением `None`, что указывает на отсутствие необходимости выполнять какие-либо действия в декораторе `@close_pop_up`.

**Примеры**:
```python
from src.webdriver.driver import Driver, Chrome
# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)
graber = Graber(driver, 0)
```
```python
from src.webdriver.driver import Driver, Firefox
# Создание инстанса драйвера (пример с Firefox)
driver = Driver(Firefox)
graber = Graber(driver, 1)
```
```python
from src.webdriver.driver import Driver, Playwright
# Создание инстанса драйвера (пример с Playwright)
driver = Driver(Playwright)
graber = Graber(driver, 2)
```
```python
from src.webdriver.driver import Driver
from src.webdriver import Chrome
# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)
graber = Graber(driver, 0)
```
```python
from src.webdriver.driver import Driver
from src.webdriver import Firefox
# Создание инстанса драйвера (пример с Firefox)
driver = Driver(Firefox)
graber = Graber(driver, 1)
```
```python
from src.webdriver.driver import Driver
from src.webdriver import Playwright
# Создание инстанса драйвера (пример с Playwright)
driver = Driver(Playwright)
graber = Graber(driver, 2)
```
```python
from src.webdriver.driver import Driver
from src.webdriver import Chrome
# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)
graber = Graber(driver, 0)
```
```python
from src.webdriver.driver import Driver
from src.webdriver import Firefox
# Создание инстанса драйвера (пример с Firefox)
driver = Driver(Firefox)
graber = Graber(driver, 1)
```
```python
from src.webdriver.driver import Driver
from src.webdriver import Playwright
# Создание инстанса драйвера (пример с Playwright)
driver = Driver(Playwright)
graber = Graber(driver, 2)