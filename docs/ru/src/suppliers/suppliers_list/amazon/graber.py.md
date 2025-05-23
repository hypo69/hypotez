# Модуль для сбора данных о товарах с Amazon

## Обзор

Модуль содержит класс `Graber`, предназначенный для сбора информации о товарах с веб-сайта Amazon. Он наследуется от базового класса `src.suppliers.graber.Graber` и предоставляет методы для обработки различных полей товара на странице. В случае необходимости нестандартной обработки поля, метод может быть переопределен.

## Подробней

Этот модуль является частью системы сбора данных о товарах от различных поставщиков, где каждый поставщик имеет свой собственный модуль для обработки специфических особенностей веб-сайта. `Graber` специализируется на Amazon и предоставляет механизмы для извлечения информации о товарах, адаптированные к структуре и особенностям этого веб-сайта. Модуль позволяет настраивать поведение сбора данных через параметры конфигурации и, при необходимости, переопределять методы обработки полей для учета изменений на сайте Amazon.

## Классы

### `Graber`

**Описание**: Класс `Graber` предназначен для сбора данных о товарах с веб-сайта Amazon.

**Наследует**:
- `src.suppliers.graber.Graber`: Наследует базовый класс для сбора данных, предоставляющий общую функциональность и интерфейс.

**Атрибуты**:
- `supplier_prefix` (str): Префикс поставщика, используемый для идентификации Amazon как поставщика.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `Graber`, устанавливает префикс поставщика и вызывает конструктор родительского класса.

#### `__init__(self, driver: Driver, lang_index: int)`

**Назначение**: Инициализация экземпляра класса `Graber`.

**Параметры**:
- `driver` (Driver): Инстанс веб-драйвера для управления браузером и взаимодействия с веб-страницей.
- `lang_index` (int): Индекс языка, используемый для локализации контента.

**Как работает функция**:
1. Устанавливает атрибут `supplier_prefix` в значение `'amazon'`, что идентифицирует данного грабера как источник данных с Amazon.
2. Вызывает метод `__init__` родительского класса `Grbr` (Graber из `src.suppliers.graber`) с переданными параметрами, передавая `supplier_prefix`, `driver` и `lang_index`. Это позволяет инициализировать базовые параметры и настройки, необходимые для сбора данных.
3. Устанавливает `Config.locator_for_decorator` в `None`. Это отключает выполнение какого-либо локатора в декораторе `@close_pop_up`. Если установить значение, то локатор будет выполнен перед каждым запросом к странице.

**Примеры**:
```python
from src.webdriver.driver import Driver
from src.webdriver.chrome import Chrome

# Пример создания инстанса драйвера Chrome
driver = Driver(Chrome)
lang_index = 0  # Пример значения индекса языка

# Создание экземпляра грабера для Amazon
graber = Graber(driver, lang_index)