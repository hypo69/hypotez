# Модуль для сбора данных о товарах с hb.co.il

## Обзор

Этот модуль содержит класс `Graber`, который собирает данные о товарах с сайта hb.co.il.

## Подробней

Класс `Graber` наследует от базового класса `Graber` и переопределяет некоторые методы для сбора данных с hb.co.il.

## Классы

### `Graber`

**Описание**: Класс для сбора данных о товарах с hb.co.il.

**Наследует**: `Graber` (базовый класс для сбора данных)

**Атрибуты**:

- `supplier_prefix` (str): Префикс поставщика, в данном случае `'hb'`.

**Методы**:

- `__init__(self, driver: Optional['Driver'] = None, lang_index:Optional[int] = None)`: Инициализирует класс сбора полей товара.
- `default_image_url(self, value:Optional[Any] = None) -> bool`: Заглушка для получения URL изображения.
- `price(self, value:Optional[Any] = None) -> bool`: Заглушка для получения цены.

**Как работает класс**:

- Класс `Graber` создается с помощью конструктора `__init__`, который инициализирует базовый класс `Graber`.
- В конструкторе устанавливается значение `supplier_prefix` и создается объект `Config` для глобальных настроек.
- Класс `Graber` переопределяет методы `default_image_url` и `price`, которые отвечают за получение URL изображения и цены товара соответственно.

## Методы класса

### `__init__(self, driver: Optional['Driver'] = None, lang_index:Optional[int] = None)`

```python
    def __init__(self, driver: Optional['Driver'] = None, lang_index:Optional[int] = None):
        """Инициализация класса сбора полей товара."""
        self.supplier_prefix = 'hb'
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)
        # Устанавливаем глобальные настройки через Context
        
        Config.locator_for_decorator = None # <- если будет уастановлено значение - то оно выполнится в декораторе `@close_pop_up`
```

**Назначение**: Инициализирует класс сбора полей товара.

**Параметры**:

- `driver` (Optional['Driver'], optional): Драйвер для взаимодействия с веб-сайтом. По умолчанию `None`.
- `lang_index` (Optional[int], optional): Индекс языка. По умолчанию `None`.

**Как работает функция**:

- В конструкторе класса `Graber` устанавливается значение `supplier_prefix` и вызывается конструктор базового класса `Graber`.
- В конструкторе базового класса инициализируются атрибуты класса `Graber` и настраиваются глобальные настройки через объект `Config`.

### `default_image_url(self, value:Optional[Any] = None) -> bool`

```python
    async def default_image_url(self, value:Optional[Any] = None) -> bool:
        return True
```

**Назначение**: Заглушка для получения URL изображения.

**Параметры**:

- `value` (Optional[Any], optional): Значение для замены. По умолчанию `None`.

**Возвращает**:

- `bool`: `True` - если функция выполнена успешно, `False` - в противном случае.

**Как работает функция**:

- В данном случае функция просто возвращает `True`, так как это заглушка.

### `price(self, value:Optional[Any] = None) -> bool`

```python
    async def price(self, value:Optional[Any] = None) -> bool:
        """Заглушка для цены"""
        self.fields.price = 150.00
        return True
```

**Назначение**: Заглушка для получения цены.

**Параметры**:

- `value` (Optional[Any], optional): Значение для замены. По умолчанию `None`.

**Возвращает**:

- `bool`: `True` - если функция выполнена успешно, `False` - в противном случае.

**Как работает функция**:

- В данном случае функция устанавливает значение поля `self.fields.price` на `150.00` и возвращает `True`, так как это заглушка.