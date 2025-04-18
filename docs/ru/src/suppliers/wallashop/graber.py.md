# Модуль graber.py для сбора данных с сайта Wallashop

## Обзор

Модуль `graber.py` предназначен для сбора информации о товарах с сайта `wallashop.co.il`. Он содержит класс `Graber`, который наследует функциональность от родительского класса `Graber` (Grbr) и переопределяет методы для специфичной обработки данных с сайта Wallashop.

## Подробней

Основная задача модуля - извлечение данных о товарах с сайта `wallashop.co.il` и их последующая обработка. Он использует веб-драйвер для взаимодействия с сайтом и извлечения необходимой информации. Класс `Graber` содержит методы для работы с отдельными полями товаров, которые могут быть переопределены для нестандартной обработки. Перед отправкой запроса к веб-драйверу, модуль позволяет выполнять предварительные действия через декораторы.

## Классы

### `Graber`

**Описание**: Класс `Graber` предназначен для сбора данных о товарах с сайта `wallashop.co.il`. Он наследует функциональность от родительского класса `Graber` (Grbr) и предоставляет возможность переопределять методы для специфичной обработки данных.

**Наследует**:
- `Graber` (Grbr) из модуля `src.suppliers.graber`

**Атрибуты**:
- `supplier_prefix` (str): Префикс поставщика, в данном случае 'wallashop'.

**Методы**:
- `__init__(driver: Driver, lang_index: int)`: Инициализирует класс `Graber` с указанным драйвером и индексом языка.

#### `__init__`

```python
def __init__(self, driver: Driver, lang_index:int):
    """Инициализация класса сбора полей товара."""
    ...
```

**Назначение**: Инициализирует экземпляр класса `Graber`.

**Параметры**:
- `driver` (Driver): Экземпляр веб-драйвера для взаимодействия с сайтом.
- `lang_index` (int): Индекс языка, используемый при сборе данных.

**Как работает функция**:
- Устанавливает префикс поставщика `supplier_prefix` равным `'wallashop'`.
- Вызывает конструктор родительского класса `Graber` (Grbr) с указанным префиксом поставщика, драйвером и индексом языка.
- Устанавливает `Context.locator_for_decorator` в `None`, что позволяет выполнять предварительные действия через декораторы.

**Примеры**:

```python
from src.webdriver.driver import Driver, Chrome
from src.suppliers.wallashop.graber import Graber

# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)

# Пример инициализации класса Graber
graber = Graber(driver, lang_index=0)
```
```python
# Создание инстанса драйвера (пример с Firefox)
from src.webdirver import Driver, Firefox
driver = Driver(Firefox)

# Пример инициализации класса Graber
graber = Graber(driver, lang_index=0)