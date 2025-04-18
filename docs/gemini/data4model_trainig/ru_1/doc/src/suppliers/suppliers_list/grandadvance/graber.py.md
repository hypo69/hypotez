# Модуль для сбора данных о товарах с Grandadvance

## Обзор

Модуль содержит класс `Graber`, предназначенный для сбора информации о товарах с веб-сайта `grandadvance.com`. Он наследует класс `Graber` из модуля `src.suppliers.graber`, расширяя его функциональность для конкретного поставщика.

## Подробнее

Этот модуль предоставляет специализированную реализацию класса `Graber` для работы с сайтом `grandadvance.com`. Он использует JSON-файлы конфигурации и локаторы для определения элементов на веб-странице и извлечения данных о товарах.

## Классы

### `Graber`

**Описание**: Класс `Graber` наследуется от базового класса `Graber` из модуля `src.suppliers.graber` и предназначен для сбора данных о товарах с сайта `grandadvance.com`.

**Наследует**:
- `Graber` (src.suppliers.graber.Graber): Обеспечивает базовую функциональность для сбора данных о товарах с веб-сайтов поставщиков.

**Атрибуты**: отсутствуют, так как все атрибуты определяются в родительском классе.

**Методы**:
- `__init__(driver: Driver, lang_index: int)`: Конструктор класса. Инициализирует класс `Graber`, загружает конфигурацию и локаторы, а также устанавливает локатор для декоратора.

**Принцип работы**:
Класс `Graber` инициализируется с использованием объекта `Driver` (веб-драйвер) и индекса языка. Он загружает JSON-конфигурацию и локаторы, специфичные для `grandadvance.com`, а затем вызывает конструктор родительского класса `Graber` для выполнения основной настройки.

## Методы класса

### `__init__`

```python
def __init__(self, driver: Driver, lang_index:int):
    """Конструктор класса. Инициализирует класс `Graber`, загружает конфигурацию и локаторы,
    а также устанавливает локатор для декоратора.

    Args:
        driver (Driver): Объект веб-драйвера для взаимодействия с веб-страницей.
        lang_index (int): Индекс языка, используемый для локализации.

    Raises:
        FileNotFoundError: Если не удается найти файлы конфигурации или локаторов.
        json.JSONDecodeError: Если не удается декодировать JSON-файлы.

    Example:
        >>> driver = Driver(Browser.Chrome)
        >>> graber = Graber(driver, 0)
    """
    ...
```
**Назначение**: Инициализация экземпляра класса `Graber`. Загружает конфигурацию и локаторы, необходимые для работы с сайтом `grandadvance.com`.

**Параметры**:
- `driver` (Driver): Объект веб-драйвера для взаимодействия с веб-страницей.
- `lang_index` (int): Индекс языка, используемый для локализации.

**Возвращает**: Ничего.

**Вызывает исключения**:
- `FileNotFoundError`: Если не удается найти файлы конфигурации или локаторов.
- `json.JSONDecodeError`: Если не удается декодировать JSON-файлы.

**Внутренние функции**: отсутствуют.

**Как работает функция**:
1. Загружает JSON-конфигурацию из файла `grandadvance.json` с использованием функции `j_loads_ns`.
2. Загружает локаторы для элементов продукта из файла `product.json` с использованием функции `j_loads_ns`.
3. Вызывает конструктор родительского класса `Graber` с указанием префикса поставщика, объекта веб-драйвера и индекса языка.
4. Устанавливает локатор для декоратора, используемого для выполнения предварительных действий перед отправкой запроса к веб-драйверу.

**Примеры**:

```python
from src.webdriver.driver import Driver
from src.webdriver.browser import Browser

# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Browser.Chrome)

# Создание инстанса класса Graber
graber = Graber(driver, 0)
```
## Параметры класса

- `driver` (Driver): Объект веб-драйвера для взаимодействия с веб-страницей.
- `lang_index` (int): Индекс языка, используемый для локализации.

```python
config:SimpleNamespace = j_loads_ns(gs.path.src / 'suppliers' / ENDPOINT / f'{ENDPOINT}.json')
locator: SimpleNamespace = j_loads_ns(gs.path.src / 'suppliers' / ENDPOINT / 'locators' / 'product.json')
super().__init__(supplier_prefix=ENDPOINT, driver=driver, lang_index=lang_index)
Context.locator_for_decorator = locator.click_to_specifications # <- if locator not definded decorator