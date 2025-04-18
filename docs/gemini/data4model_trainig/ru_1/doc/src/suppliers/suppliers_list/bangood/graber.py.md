# Модуль для сбора данных о товарах с Bangood

## Обзор

Модуль содержит класс `Graber`, предназначенный для сбора данных о товарах с веб-сайта `bangood.com`. Он наследуется от базового класса `src.suppliers.graber.Graber`. Класс `Graber` предоставляет методы для обработки различных полей товара на странице. В случае необходимости нестандартной обработки поля, метод может быть переопределен. Для каждого поля страницы товара сделана функция обработки поля в родительском `Graber`. Если нужна нестандертная обработка, можно перегрузить метод здесь, в этом классе.

Перед отправкой запроса к вебдрайверу можно совершить предварительные действия через декоратор. Декоратор по умолчанию находится в родительском классе. Для того, чтобы декоратор сработал надо передать значение в `Context.locator`. Если надо реализовать свой декоратор - раскоментируйте строки с декоратором и переопределите его поведение. Вы также можете реализовать свой собственный декоратор, раскомментировав соответствующие строки кода.

## Подробнее

Более подробное описание. Модуль используется для извлечения информации о товарах с сайта Banggood, позволяя переопределять методы обработки полей для нестандартных ситуаций.

## Классы

### `Graber`

**Описание**: Класс `Graber` предназначен для сбора данных о товарах с веб-сайта Banggood.

**Наследует**:
- `Grbr` (из `src.suppliers.graber`): Базовый класс для грабберов, определяющий основную логику сбора данных о товарах.

**Атрибуты**:
- `supplier_prefix` (str): Префикс поставщика, устанавливается как `'bangood'`.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `Graber`, устанавливает префикс поставщика и вызывает конструктор родительского класса.

**Принцип работы**:
1. **Инициализация**: При создании экземпляра класса `Graber` вызывается метод `__init__`, который устанавливает префикс поставщика как `'bangood'` и инициализирует родительский класс `Graber` (из модуля `src.suppliers.graber`).
2. **Наследование**: Класс наследует методы обработки полей товаров от родительского класса `Graber`.
3. **Переопределение**: При необходимости нестандартной обработки полей товаров, методы родительского класса могут быть переопределены в классе `Graber`.
4. **Декораторы**: Перед отправкой запроса к вебдрайверу можно выполнить предварительные действия, используя декораторы. Декоратор по умолчанию находится в родительском классе.

### `__init__`

```python
def __init__(self, driver: Driver, lang_index: int):
    """Инициализация класса сбора полей товара.

    Args:
        driver (Driver): Экземпляр драйвера WebDriver для управления браузером.
        lang_index (int): Индекс языка для выбора языковых настроек на сайте.

    """
    ...
```

**Назначение**: Инициализация экземпляра класса `Graber`, устанавливает префикс поставщика и вызывает конструктор родительского класса.

**Параметры**:
- `driver` (Driver): Экземпляр драйвера WebDriver для управления браузером.
- `lang_index` (int): Индекс языка для выбора языковых настроек на сайте.

**Как работает функция**:
1. Устанавливает атрибут `supplier_prefix` равным `'bangood'`.
2. Вызывает конструктор родительского класса `Grbr` (из `src.suppliers.graber`) с переданными параметрами и `supplier_prefix`.
3. Устанавливает `Context.locator_for_decorator` в `None`.

**Примеры**:

```python
from src.webdriver.driver import Driver
from src.webdriver.chrome import Chrome
# from src.suppliers.suppliers_list.bangood.graber import Graber # закомментировано - чтобы не было ошибки импорта

# Создание экземпляра драйвера (пример с Chrome)
driver = Driver(Chrome)
lang_index = 1  # Пример индекса языка

# Создание экземпляра класса Graber
# grabber = Graber(driver, lang_index)  #  закомментировано - чтобы не было ошибки импорта