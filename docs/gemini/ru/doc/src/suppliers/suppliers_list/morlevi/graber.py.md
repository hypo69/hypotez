# Модуль `src.suppliers.morlevi.graber`

## Обзор

Этот модуль реализует класс `Graber`, который отвечает за сбор информации о товаре с сайта `morlevi.co.il`. Класс наследует от базового класса `Graber`, предоставляемого модулем `src.suppliers.graber`.  

## Подробности

Модуль `src.suppliers.morlevi.graber` предназначен для сбора данных о товарах с интернет-магазина `morlevi.co.il`. 

## Классы

### `class Graber`

**Описание**: Класс `Graber`  наследует от базового класса `Grbr` (из `src.suppliers.graber`) и предоставляет специализированную логику сбора данных для сайта `morlevi.co.il`.

**Наследует**: `Grbr` (из `src.suppliers.graber`)

**Атрибуты**:

- `supplier_prefix: str = 'morlevi'`: Префикс для идентификации поставщика.

**Параметры**:

- `driver: Optional[\'Driver\'] = None`: Объект драйвера для взаимодействия с браузером.
- `lang_index:Optional[int] = None`: Индекс языка, используемый для сбора данных.

**Принцип работы**:

- Класс `Graber` инициализируется с использованием базового класса `Grbr`, передавая префикс поставщика (`self.supplier_prefix`) и драйвер (`driver`).
- Значение `Config.driver`  устанавливается в `self.driver`.
- Значение `Config.locator_for_decorator` устанавливается в `self.product_locator.close_pop_up`, что указывает на локатор, который будет использоваться декоратором.

**Методы**:

- `__init__(self, driver: Optional[\'Driver\'] = None, lang_index:Optional[int] = None)`: Инициализация класса.

## Методы класса

### `__init__(self, driver: Optional[\'Driver\'] = None, lang_index:Optional[int] = None)`

```python
    def __init__(self, driver: Optional[\'Driver\'] = None, lang_index:Optional[int] = None):
        """Инициализация класса сбора полей товара."""
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)
        Config.driver = self.driver
        Config.locator_for_decorator = self.product_locator.close_pop_up 
```

**Описание**: 
- Инициализирует класс `Graber`, вызывая конструктор базового класса `Grbr`.
- Передает префикс поставщика (`self.supplier_prefix`), драйвер (`driver`) и индекс языка (`lang_index`).
- Устанавливает значение `Config.driver`  в `self.driver`.
- Устанавливает значение `Config.locator_for_decorator`  в `self.product_locator.close_pop_up`.

**Параметры**:

- `driver: Optional[\'Driver\'] = None`: Объект драйвера для взаимодействия с браузером.
- `lang_index:Optional[int] = None`: Индекс языка, используемый для сбора данных.


**Пример**:

```python
# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)
# Инициализация класса Graber
graber = Graber(driver=driver)
```

## Параметры класса

- `supplier_prefix: str = 'morlevi'`: Префикс для идентификации поставщика.
- `driver: Optional[\'Driver\'] = None`: Объект драйвера для взаимодействия с браузером.
- `lang_index:Optional[int] = None`: Индекс языка, используемый для сбора данных.