# Модуль для сбора данных о товарах с Gearbest
## Обзор

Модуль содержит класс `Graber`, предназначенный для сбора информации о товарах с веб-сайта `gearbest.com`. Он наследует базовый класс `Graber` из модуля `src.suppliers.graber`.

## Подробней

Этот модуль предоставляет класс `Graber`, который специализируется на извлечении данных о товарах с сайта `gearbest.com`. Он расширяет функциональность базового класса `Graber`, предоставляя возможность переопределять методы обработки полей товара для соответствия уникальной структуре страниц `gearbest.com`. В случае необходимости нестандартной обработки какого-либо поля товара, соответствующий метод может быть переопределен в этом классе.

Перед отправкой запроса к веб-драйверу можно выполнить предварительные действия, используя декоратор. Декоратор по умолчанию находится в родительском классе. Для активации декоратора необходимо передать значение в `Context.locator`. При необходимости можно реализовать свой собственный декоратор, раскомментировав соответствующие строки кода и переопределив его поведение.

## Классы

### `Graber`

**Описание**: Класс `Graber` предназначен для сбора данных о товарах с сайта `gearbest.com`. Он наследует функциональность из базового класса `Graber` и предоставляет возможность переопределять методы для обработки специфических полей данных.

**Наследует**:
- `Graber` (as `Grbr`) из `src.suppliers.graber`

**Атрибуты**:
- `supplier_prefix` (str): Префикс поставщика, устанавливается как `'etzmaleh'`.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `Graber`.

## Методы класса

### `__init__`

```python
def __init__(self, driver: Driver, lang_index):
    """Инициализация класса сбора полей товара."""
    ...
```

**Назначение**: Инициализирует экземпляр класса `Graber`, устанавливая префикс поставщика и вызывая конструктор родительского класса. Также устанавливает глобальные настройки через `Context`.

**Параметры**:
- `driver` (Driver): Экземпляр веб-драйвера, используемый для взаимодействия с веб-страницей.
- `lang_index` (int): Индекс языка, используемый для локализации.

**Возвращает**:
- `None`

**Как работает функция**:
1. Устанавливает атрибут `supplier_prefix` в значение `'etzmaleh'`.
2. Вызывает конструктор родительского класса `Graber` с переданными параметрами `supplier_prefix`, `driver` и `lang_index`.
3. Устанавливает атрибут `Context.locator_for_decorator` в значение `None`. Если установить значение - то оно выполнится в декораторе `@close_pop_up`

**Примеры**:

```python
from src.webdriver.driver import Driver, Firefox
from src.suppliers.suppliers_list.gearbest.graber import Graber

# Пример создания экземпляра класса Graber
driver = Driver(Firefox)
graber = Graber(driver=driver, lang_index=0)
```
## Переменные класса

- `supplier_prefix` (str): Префикс поставщика, используемый в классе. По умолчанию имеет значение `'etzmaleh'`.