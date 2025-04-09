# Модуль aliexpress

## Обзор

Модуль `aliexpress` предоставляет класс `Aliexpress`, который объединяет функциональность классов `Supplier`, `AliRequests` и `AliApi` для взаимодействия с AliExpress. Он предназначен для задач, связанных с парсингом и взаимодействием с API AliExpress.

## Содержание

- [Модуль aliexpress](#модуль-aliexpress)
- [Класс Aliexpress](#класс-aliexpress)
  - [Метод __init__](#метод-__init__)

## Класс Aliexpress

### `Aliexpress`

**Описание**: Базовый класс для работы с AliExpress. Объединяет возможности классов `Supplier`, `AliRequests` и `AliApi` для удобного взаимодействия с AliExpress.

**Примеры использования**:

```python
# Инициализация без WebDriver
a = Aliexpress()

# Chrome WebDriver
a = Aliexpress('chrome')

# Режим запросов
a = Aliexpress(requests=True)
```

### Метод `__init__`

**Описание**: Инициализирует класс `Aliexpress`.

```python
def __init__(
    self,
    webdriver: bool | str = False,
    locale: str | dict = {'EN': 'USD'},
    *args,
    **kwargs,
) -> None:
    """Инициализирует класс `Aliexpress`.

    Args:
        webdriver (bool | str, optional): Определяет режим использования WebDriver. Возможные значения:
            - `False` (по умолчанию): Без WebDriver.
            - `'chrome'`: Chrome WebDriver.
            - `'mozilla'`: Mozilla WebDriver.
            - `'edge'`: Edge WebDriver.
            - `'default'`: Системный WebDriver по умолчанию.
        locale (str | dict, optional): Настройки языка и валюты. По умолчанию `{'EN': 'USD'}`.
        *args: Дополнительные позиционные аргументы.
        **kwargs: Дополнительные именованные аргументы.

    Returns:
        None: Функция не возвращает значение.

    Raises:
        Возможные исключения, связанные с инициализацией WebDriver или ошибками при взаимодействии с AliExpress.

    Example:
        >>> a = Aliexpress()
        >>> a = Aliexpress('chrome')
    """
    ...
```

**Параметры**:

- `webdriver` (bool | str, optional): Определяет режим использования WebDriver. Возможные значения:
  - `False` (по умолчанию): Без WebDriver.
  - `'chrome'`: Chrome WebDriver.
  - `'mozilla'`: Mozilla WebDriver.
  - `'edge'`: Edge WebDriver.
  - `'default'`: Системный WebDriver по умолчанию.
- `locale` (str | dict, optional): Настройки языка и валюты. По умолчанию `{'EN': 'USD'}`.
- `*args`: Дополнительные позиционные аргументы.
- `**kwargs`: Дополнительные именованные аргументы.

**Примеры**:

```python
# Инициализация без WebDriver
a = Aliexpress()

# Chrome WebDriver
a = Aliexpress('chrome')
```

**Возвращает**:

- Не возвращает значение.

**Вызывает исключения**:

- Возможные исключения, связанные с инициализацией WebDriver или ошибками при взаимодействии с AliExpress.