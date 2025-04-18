# Модуль для сбора данных о товарах с Cdata

## Обзор

Модуль предназначен для сбора информации о товарах с веб-сайта Cdata. Он содержит класс `Graber`, который наследуется от базового класса `src.suppliers.graber.Graber` и предоставляет методы для обработки и извлечения данных о товарах с сайта Cdata.

## Подробней

Этот модуль является частью системы сбора данных о товарах от различных поставщиков в проекте `hypotez`. Он специализируется на извлечении информации с сайта Cdata.

Класс `Graber` переопределяет или использует методы из родительского класса для обработки полей товара. Если для какого-либо поля требуется нестандартная обработка, соответствующий метод переопределяется в этом классе.

Перед отправкой запроса к веб-драйверу, можно выполнить предварительные действия, используя декоратор `@close_pop_up`. Если необходимо реализовать собственный декоратор, раскомментируйте соответствующие строки кода и переопределите его поведение.

## Классы

### `Graber`

**Описание**: Класс для сбора данных о товарах с сайта Cdata.

**Наследует**: `src.suppliers.graber.Graber`

**Атрибуты**:
- `supplier_prefix` (str): Префикс поставщика, используется для идентификации поставщика 'cdata'.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `Graber`.

#### `__init__`

```python
def __init__(self, driver: Driver, lang_index:int):
    """Инициализация класса сбора полей товара."""
    ...
```

**Назначение**: Инициализирует класс `Graber`, устанавливает префикс поставщика и вызывает конструктор родительского класса.

**Параметры**:
- `driver` (Driver): Экземпляр веб-драйвера, используемый для взаимодействия с веб-сайтом.
- `lang_index` (int): Индекс языка, используемый для выбора языка на веб-сайте.

**Как работает функция**:
1. Устанавливает атрибут `supplier_prefix` равным 'cdata', чтобы указать, что этот граббер предназначен для Cdata.
2. Вызывает конструктор родительского класса `Graber` (`super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)`) для инициализации общих параметров и настроек граббера.
3. Устанавливает `Context.locator_for_decorator` в `None`. Если установить другое значение, оно выполнится в декораторе `@close_pop_up`.

**Примеры**:
```python
from src.webdriver.driver import Driver, Firefox

driver = Driver(Firefox)
graber = Graber(driver, lang_index=0)