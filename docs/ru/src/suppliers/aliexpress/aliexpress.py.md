# Модуль aliexpress

## Обзор

Модуль `aliexpress` предоставляет класс `Aliexpress`, который объединяет функциональность классов `Supplier`, `AliRequests` и `AliApi` для работы с AliExpress. Он предназначен для упрощения взаимодействия с платформой AliExpress, предлагая различные режимы работы, включая использование веб-драйвера и выполнение запросов напрямую.

## Подробней

Модуль `aliexpress` разработан для обеспечения удобного и гибкого взаимодействия с AliExpress. Он позволяет выполнять запросы к API AliExpress, обрабатывать ответы и автоматизировать задачи, такие как сбор данных о товарах. Класс `Aliexpress` объединяет в себе функциональность для работы с запросами, API и общие функции поставщика, что упрощает разработку скриптов и приложений для работы с AliExpress.

## Классы

### `Aliexpress`

**Описание**: Базовый класс для работы с AliExpress.

**Наследует**:
- `Supplier`: Предоставляет общую функциональность поставщика.
- `AliRequests`: Отвечает за выполнение HTTP-запросов к AliExpress.
- `AliApi`: Предоставляет методы для взаимодействия с API AliExpress.

**Атрибуты**:

- `supplier_prefix` (str): Префикс поставщика (в данном случае, 'aliexpress').
- `locale` (str | dict): Языковые и валютные настройки для скрипта.
- `webdriver` (bool | str): Режим веб-драйвера.

**Методы**:
- `__init__`: Инициализирует класс `Aliexpress`.

### Методы класса

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

**Назначение**: Инициализирует класс `Aliexpress`, настраивая режим веб-драйвера, языковые и валютные параметры.

**Параметры**:
- `webdriver` (bool | str): Определяет, использовать ли веб-драйвер и какой именно. Поддерживаемые значения:
    - `False` (по умолчанию): Без веб-драйвера.
    - `'chrome'`: Использовать Chrome webdriver.
    - `'mozilla'`: Использовать Mozilla webdriver.
    - `'edge'`: Использовать Edge webdriver.
    - `'default'`: Использовать системный веб-драйвер по умолчанию.
- `locale` (str | dict): Языковые и валютные настройки для скрипта. По умолчанию `{'EN': 'USD'}`.
- `*args`: Дополнительные позиционные аргументы, которые передаются в конструктор базового класса.
- `**kwargs`: Дополнительные именованные аргументы, которые передаются в конструктор базового класса.

**Как работает функция**:

1.  Вызывает конструктор базового класса `Supplier` с параметрами `supplier_prefix`, `locale` и `webdriver`, а также всеми дополнительными позиционными и именованными аргументами.

**Примеры**:

```python
# Запуск без веб-драйвера
a = Aliexpress()

# Запуск с Chrome webdriver
a = Aliexpress('chrome')