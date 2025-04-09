# Модуль для работы с AliExpress

## Обзор

Модуль предоставляет класс `Aliexpress`, который объединяет функциональность классов `Supplier`, `AliRequests` и `AliApi` для работы с AliExpress. Он позволяет взаимодействовать с AliExpress как через веб-драйвер, так и напрямую через запросы, а также предоставляет API для работы с данными AliExpress.

## Подробнее

Этот модуль предназначен для автоматизации работы с AliExpress, включая поиск товаров, сбор информации о товарах, оформление заказов и другие операции. Класс `Aliexpress` является центральным элементом модуля, объединяющим в себе функциональность различных классов для удобства использования. Он позволяет настраивать язык и валюту, использовать веб-драйвер для эмуляции действий пользователя в браузере или отправлять прямые HTTP-запросы к API AliExpress.

## Классы

### `Aliexpress`

**Описание**: Базовый класс для работы с AliExpress.

**Наследует**:
- `Supplier`: Предоставляет базовую функциональность для работы с поставщиками.
- `AliRequests`: Предоставляет методы для отправки HTTP-запросов к AliExpress.
- `AliApi`: Предоставляет API для работы с данными AliExpress.

**Атрибуты**: Отсутствуют в явном виде, но используются атрибуты родительских классов.

**Методы**:
- `__init__`: Инициализирует класс `Aliexpress`.

### `__init__`

```python
def __init__(self, 
             webdriver: bool | str = False, 
             locale: str | dict = {'EN': 'USD'},
             *args, **kwargs):
    """
    Initialize the Aliexpress class.

    :param webdriver: Webdriver mode. Supported values are:
        - `False` (default): No webdriver.
        - `'chrome'`: Use the Chrome webdriver.
        - `'mozilla'`: Use the Mozilla webdriver.
        - `'edge'`: Use the Edge webdriver.
        - `'default'`: Use the system's default webdriver.
    :type webdriver: bool | str

    :param locale: The language and currency settings for the script.
    :type locale: str | dict

    :param args: Additional positional arguments.
    :param kwargs: Additional keyword arguments.

    **Examples**:

    .. code-block:: python

        # Run without a webdriver
        a = Aliexpress()

        # Webdriver `Chrome`
        a = Aliexpress('chrome')

    """
```

**Назначение**: Инициализация экземпляра класса `Aliexpress`.

**Параметры**:
- `webdriver` (bool | str): Режим веб-драйвера. Возможные значения:
    - `False` (по умолчанию): Без веб-драйвера.
    - `'chrome'`: Использовать веб-драйвер Chrome.
    - `'mozilla'`: Использовать веб-драйвер Mozilla Firefox.
    - `'edge'`: Использовать веб-драйвер Edge.
    - `'default'`: Использовать системный веб-драйвер по умолчанию.
- `locale` (str | dict): Настройки языка и валюты для скрипта. По умолчанию `{'EN': 'USD'}`.
- `*args`: Дополнительные позиционные аргументы.
- `**kwargs`: Дополнительные именованные аргументы.

**Возвращает**: Ничего (None).

**Вызывает исключения**: Нет информации об исключениях.

**Как работает функция**:

1.  Функция `__init__` инициализирует класс `Aliexpress`, настраивая режим работы с веб-драйвером и локализацию.
2.  Она вызывает конструктор родительского класса `Supplier` с передачей префикса поставщика `'aliexpress'`, настроек локали и режима веб-драйвера.
3.  Дополнительные аргументы `*args` и `**kwargs` передаются в конструктор родительского класса.

**Примеры**:

```python
# Запуск без веб-драйвера
a = Aliexpress()

# Запуск с веб-драйвером Chrome
a = Aliexpress('chrome')
```
```
A: Начало
|
B: Вызов __init__ родительского класса Supplier
|
C: Передача аргументов (supplier_prefix, locale, webdriver, *args, **kwargs) в Supplier
|
D: Конец