# Модуль Graber Cdata
## Обзор

Модуль содержит класс `Graber`, который используется для сбора данных о товарах с веб-сайта `bangood.com`. Он наследуется от базового класса `src.suppliers.graber.Graber`.

Класс `Graber` предоставляет методы для обработки различных полей товара на странице. В случае необходимости нестандартной обработки поля, метод может быть переопределен.

Для каждого поля страницы товара сделана функция обработки поля в родительском `Graber`. Если нужна нестандертная обработка, можно перегрузить метод здесь, в этом классе.

## Детали

### Декоратор
Перед отправкой запроса к вебдрайверу можно совершить предварительные действия через декоратор. Декоратор по умолчанию находится в родительском классе. Для того, чтобы декоратор сработал надо передать значение в `Context.locator`, Если надо реализовать свой декоратор - раскоментируйте строки с декоратором и переопределите его поведение.

Вы также можете реализовать свой собственный декоратор, раскомментировав соответствующие строки кода.

## Классы

### `Graber`

**Описание**: Класс для операций захвата Morlevi.

**Наследует**: `src.suppliers.graber.Graber`

**Атрибуты**:

- `supplier_prefix` (str): Префикс поставщика.

**Методы**:

- `__init__(self, driver: Driver, lang_index: int)`: Инициализация класса сбора полей товара.

##  Функции

###  `__init__(self, driver: Driver, lang_index: int)` 

**Описание**: Инициализация класса сбора полей товара.

**Параметры**:

- `driver` (Driver): Экземпляр вебдрайвера.
- `lang_index` (int): Индекс языка.

**Возвращает**: 
- None

**Описание работы**:

- Устанавливает `supplier_prefix` как 'cdata'.
- Вызывает метод `__init__` родительского класса `Grbr` с параметрами `supplier_prefix`, `driver` и `lang_index`.
- Устанавливает глобальные настройки через `Context`.
- `Config.locator_for_decorator` устанавливается в `None`, что означает, что по умолчанию декоратор `@close_pop_up` не будет использоваться.

**Пример**:

```python
# Creating a driver instance (example with Chrome)
driver = Driver(Chrome)

# Initialize the Graber class with the driver and language index
graber = Graber(driver, lang_index=0)
```

## Примеры

```python
# Creating a driver instance (example with Chrome)
driver = Driver(Chrome)

# Initialize the Graber class with the driver and language index
graber = Graber(driver, lang_index=0)