# Модуль: src.suppliers.hb.graber

## Обзор

Модуль `graber.py` предназначен для сбора информации о товарах с сайта `hb.co.il`. Он содержит класс `Graber`, который наследует функциональность от базового класса `Graber` (`Grbr`) и переопределяет методы для специфической обработки данных, характерной для данного поставщика. Модуль использует веб-драйвер для взаимодействия с сайтом и извлечения необходимых данных.

## Подробней

Этот модуль является частью системы сбора данных о товарах от различных поставщиков в проекте `hypotez`. Он специализируется на сборе данных с сайта `hb.co.il`. Для каждого поля товара на сайте создается функция обработки. Если стандартной обработки недостаточно, функция перегружается в этом классе.

Перед отправкой запроса к веб-драйверу можно выполнить предварительные действия через декоратор. Декоратор по умолчанию находится в родительском классе. Чтобы декоратор сработал, необходимо передать значение в `Context.locator`. Если требуется реализовать собственный декоратор, можно раскомментировать соответствующие строки кода и переопределить его поведение.

## Классы

### `Graber`

**Описание**: Класс `Graber` предназначен для сбора данных о товарах с сайта `hb.co.il`. Он наследует функциональность от базового класса `Graber` (`Grbr`) и переопределяет методы для специфической обработки данных, характерной для данного поставщика.

**Наследует**:

- `Grbr` (src.suppliers.graber.Graber): Базовый класс для сбора данных о товарах.

**Атрибуты**:

- `supplier_prefix` (str): Префикс поставщика, устанавливается в значение `'hb'`.

**Методы**:

- `__init__`: Инициализирует экземпляр класса `Graber`, устанавливает префикс поставщика и вызывает конструктор родительского класса.
- `default_image_url`: Метод-заглушка для получения URL изображения товара по умолчанию.
- `price`: Метод-заглушка для получения цены товара.

## Методы класса

### `__init__`

```python
def __init__(self, driver: Optional['Driver'] = None, lang_index: Optional[int] = None) -> None
```

**Назначение**: Инициализирует экземпляр класса `Graber`, устанавливает префикс поставщика и вызывает конструктор родительского класса.

**Параметры**:

- `driver` (Optional['Driver'], optional): Экземпляр веб-драйвера для взаимодействия с сайтом. По умолчанию `None`.
- `lang_index` (Optional[int], optional): Индекс языка. По умолчанию `None`.

**Как работает функция**:

1. Устанавливает атрибут `supplier_prefix` в значение `'hb'`.
2. Вызывает конструктор родительского класса `Grbr` с установленным префиксом поставщика, драйвером и индексом языка.
3. Устанавливает `Config.locator_for_decorator` в `None`, чтобы декоратор `@close_pop_up` не выполнялся по умолчанию.

**Примеры**:

```python
from src.webdriver.driver import Driver
from src.webdriver.chrome import Chrome
driver = Driver(Chrome)
graber = Graber(driver=driver, lang_index=0)
print(graber.supplier_prefix)  # Вывод: hb
```

### `default_image_url`

```python
async def default_image_url(self, value: Optional[Any] = None) -> bool
```

**Назначение**: Метод-заглушка для получения URL изображения товара по умолчанию.

**Параметры**:

- `value` (Optional[Any], optional): Дополнительное значение, которое может быть передано. По умолчанию `None`.

**Возвращает**:

- `bool`: Всегда возвращает `True`.

**Как работает функция**:

Просто возвращает `True` без каких-либо действий.

**Примеры**:

```python
from src.webdriver.driver import Driver
from src.webdriver.chrome import Chrome
driver = Driver(Chrome)
import asyncio
async def main():
    graber = Graber(driver=driver, lang_index=0)
    result = await graber.default_image_url()
    print(result)  # Вывод: True
asyncio.run(main())
```

### `price`

```python
async def price(self, value: Optional[Any] = None) -> bool
```

**Назначение**: Метод-заглушка для получения цены товара.

**Параметры**:

- `value` (Optional[Any], optional): Дополнительное значение, которое может быть передано. По умолчанию `None`.

**Возвращает**:

- `bool`: Всегда возвращает `True`.

**Как работает функция**:

1. Устанавливает атрибут `self.fields.price` в значение `150.00`.
2. Возвращает `True`.

**Примеры**:

```python
from src.webdriver.driver import Driver
from src.webdriver.chrome import Chrome
driver = Driver(Chrome)
import asyncio

async def main():
    graber = Graber(driver=driver, lang_index=0)
    await graber.price()
    print(graber.fields.price)
asyncio.run(main()) # Вывод: 150.0