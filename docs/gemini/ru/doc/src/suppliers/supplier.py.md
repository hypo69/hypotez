# Модуль `src.suppliers.supplier`

## Обзор

Модуль `src.suppliers.supplier` содержит базовый класс `Supplier`, предназначенный для унификации взаимодействия с различными поставщиками. Он предоставляет абстракцию для запуска сценариев сбора данных, управления локаторами элементов страницы и взаимодействия с веб-драйвером.

## Подробней

Этот модуль является ключевым компонентом системы, обеспечивающим стандартизированный интерфейс для работы с различными поставщиками. Класс `Supplier` предназначен для управления и выполнения сценариев сбора данных, а также для обработки и адаптации логики взаимодействия с веб-страницами поставщиков. Он включает в себя функциональность для загрузки связанных модулей поставщика и управления сценариями, что позволяет расширять и адаптировать систему под новых поставщиков без изменения основного кода.

## Классы

### `Supplier`

**Описание**: Класс `Supplier` выполняет сценарии для различных поставщиков, обеспечивая взаимодействие с веб-драйвером и управление локаторами элементов страницы.

**Атрибуты**:

- `supplier_id` (Optional[int]): Идентификатор поставщика.
- `supplier_prefix` (str): Префикс поставщика.
- `locale` (str): Код локали в формате ISO 639-1 (по умолчанию 'en').
- `price_rule` (Optional[str]): Правило расчета цен.
- `related_modules` (Optional[ModuleType]): Функции, относящиеся к каждому поставщику.
- `scenario_files` (List[str]): Список файлов сценариев для выполнения.
- `current_scenario` (Dict[str, Any]): Текущий исполняемый сценарий.
- `locators` (List[SimpleNamespace]): Локаторы для элементов страницы.
- `driver` (Optional['Driver']): Веб-драйвер.

**Принцип работы**:

Класс `Supplier` инициализируется с набором параметров, которые определяют поставщика и его конфигурацию. В процессе инициализации загружаются настройки поставщика, а также связанные с ним модули. Затем класс предоставляет методы для входа на сайт поставщика и выполнения сценариев сбора данных.

### `Supplier.Config`

**Описание**: Вложенный класс `Config` используется для настройки модели `Supplier` с использованием `pydantic`.

**Атрибуты**:
- `arbitrary_types_allowed` (bool): Определяет, разрешены ли произвольные типы данных.

### Методы класса `Supplier`

#### `__init__`

```python
def __init__(self, **data):
    """Инициализация поставщика, загрузка конфигурации."""
    ...
```

**Назначение**: Инициализирует экземпляр класса `Supplier`, загружает конфигурацию поставщика и выполняет начальную настройку.

**Параметры**:
- `**data`: Произвольные параметры, передаваемые при инициализации объекта.

**Вызывает исключения**:
- `DefaultSettingsException`: Если не удается загрузить параметры поставщика.

**Как работает функция**:
- Вызывает конструктор родительского класса `BaseModel` для инициализации базовых атрибутов.
- Пытается загрузить параметры поставщика, вызывая метод `_payload`.
- Если загрузка параметров завершается неудачей, выбрасывает исключение `DefaultSettingsException`.

#### `_payload`

```python
def _payload(self) -> bool:
    """Загрузка параметров поставщика с использованием `j_loads_ns`."""
    ...
```

**Назначение**: Загружает параметры поставщика, включая связанные модули, необходимые для работы с конкретным поставщиком.

**Возвращает**:
- `bool`: `True`, если загрузка выполнена успешно, иначе `False`.

**Как работает функция**:
- Логирует начало загрузки настроек для поставщика.
- Пытается импортировать модуль, связанный с конкретным поставщиком, используя `importlib.import_module`.
- В случае успеха устанавливает модуль как атрибут `related_modules` объекта `Supplier`.
- В случае ошибки логирует ошибку и возвращает `False`.

**Примеры**:
```python
# Пример успешной загрузки параметров поставщика
supplier = Supplier(supplier_prefix='example_supplier')
```

```python
# Пример неудачной загрузки параметров поставщика (модуль не найден)
try:
    supplier = Supplier(supplier_prefix='non_existent_supplier')
except DefaultSettingsException as ex:
    logger.error('Ошибка при создании поставщика', ex, exc_info=True)
```

#### `login`

```python
 def login(self) -> bool:
    """Выполняет вход на сайт поставщика."""
    ...
```

**Назначение**: Выполняет вход на сайт поставщика с использованием логики, определенной в `related_modules`.

**Возвращает**:
- `bool`: `True`, если вход выполнен успешно, иначе `False`.

**Как работает функция**:
- Вызывает функцию `login` из модуля `related_modules`, передавая текущий экземпляр `Supplier` в качестве аргумента.
- Возвращает результат вызова функции `login`.

**Примеры**:
```python
# Пример входа на сайт поставщика
supplier = Supplier(supplier_prefix='example_supplier')
if supplier.login():
    logger.info('Успешный вход на сайт поставщика')
else:
    logger.warning('Не удалось войти на сайт поставщика')
```

#### `run_scenario_files`

```python
def run_scenario_files(self, scenario_files: Optional[str | List[str]] = None) -> bool:
    """Выполнение одного или нескольких файлов сценариев."""
    ...
```

**Назначение**: Выполняет один или несколько файлов сценариев, используя `run_scenario_files` из модуля `src.suppliers.scenario.scenario_executor`.

**Параметры**:
- `scenario_files` (Optional[str | List[str]]): Список файлов сценариев для выполнения. Если не указан, используется `self.scenario_files`.

**Возвращает**:
- `bool`: `True`, если все сценарии успешно выполнены, иначе `False`.

**Как работает функция**:
- Если `scenario_files` не указан, использует список файлов сценариев из атрибута `self.scenario_files`.
- Вызывает функцию `run_scenario_files` из модуля `src.suppliers.scenario.scenario_executor`, передавая текущий экземпляр `Supplier` и список файлов сценариев.
- Возвращает результат вызова функции `run_scenario_files`.

**Примеры**:
```python
# Пример выполнения списка файлов сценариев
supplier = Supplier(supplier_prefix='example_supplier', scenario_files=['scenario1.json', 'scenario2.json'])
if supplier.run_scenario_files():
    logger.info('Сценарии успешно выполнены')
else:
    logger.warning('Не удалось выполнить сценарии')
```

#### `run_scenarios`

```python
def run_scenarios(self, scenarios: dict | List[dict]) -> bool:
    """Выполнение списка или одного сценария."""
    ...
```

**Назначение**: Выполняет один или несколько сценариев, используя `run_scenarios` из модуля `src.suppliers.scenario.scenario_executor`.

**Параметры**:
- `scenarios` (dict | List[dict]): Сценарий или список сценариев для выполнения.

**Возвращает**:
- `bool`: `True`, если сценарий успешно выполнен, иначе `False`.

**Как работает функция**:
- Вызывает функцию `run_scenarios` из модуля `src.suppliers.scenario.scenario_executor`, передавая текущий экземпляр `Supplier` и сценарии для выполнения.
- Возвращает результат вызова функции `run_scenarios`.

**Примеры**:
```python
# Пример выполнения одного сценария
supplier = Supplier(supplier_prefix='example_supplier')
scenario = {'name': 'example_scenario', 'steps': []}
if supplier.run_scenarios(scenario):
    logger.info('Сценарий успешно выполнен')
else:
    logger.warning('Не удалось выполнить сценарий')
```

```python
# Пример выполнения списка сценариев
supplier = Supplier(supplier_prefix='example_supplier')
scenarios = [{'name': 'scenario1', 'steps': []}, {'name': 'scenario2', 'steps': []}]
if supplier.run_scenarios(scenarios):
    logger.info('Сценарии успешно выполнены')
else:
    logger.warning('Не удалось выполнить сценарии')
```
```python
    @validator(\'supplier_prefix\')
    def check_supplier_prefix(cls, value: str) -> str:
        """Проверка префикса поставщика на пустое значение."""
        if not value:
            raise ValueError(\'supplier_prefix не может быть пустым\')
        return value
```

**Назначение**: Валидатор для проверки префикса поставщика на пустое значение.

**Параметры**:
- `value` (str): Префикс поставщика.

**Возвращает**:
- `str`: Префикс поставщика, если он не пустой.

**Вызывает исключения**:
- `ValueError`: Если префикс поставщика пустой.

**Как работает функция**:
- Проверяет, является ли переданное значение пустым.
- Если значение пустое, поднимается исключение `ValueError` с сообщением о том, что префикс поставщика не может быть пустым.
- Если значение не пустое, возвращает его.

## Параметры класса

- `supplier_id` (Optional[int]): Идентификатор поставщика, может быть `None`, если не задан.
- `supplier_prefix` (str): Префикс поставщика, обязательное поле.
- `locale` (str): Код локали в формате ISO 639-1, по умолчанию 'en'.
- `price_rule` (Optional[str]): Правило расчета цен, может быть `None`, если не задано.
- `related_modules` (Optional[ModuleType]): Функции, относящиеся к каждому поставщику, может быть `None`, если не заданы.
- `scenario_files` (List[str]): Список файлов сценариев для выполнения, по умолчанию пустой список.
- `current_scenario` (Dict[str, Any]): Текущий исполняемый сценарий, по умолчанию пустой словарь.
- `locators` (List[SimpleNamespace]): Локаторы для элементов страницы, по умолчанию пустой словарь.
- `driver` (Optional['Driver']): Веб-драйвер, может быть `None`, если не задан.

## Примеры

Примеры создания экземпляра класса `Supplier` и вызова его методов:

```python
from src.suppliers.supplier import Supplier
from src.logger.logger import logger

# Пример создания экземпляра класса Supplier
try:
    supplier = Supplier(supplier_prefix='example_supplier', locale='ru', scenario_files=['scenario.json'])
    logger.info(f'Создан поставщик: {supplier.supplier_prefix}')

    # Пример выполнения сценариев
    if supplier.run_scenario_files():
        logger.info('Сценарии успешно выполнены')
    else:
        logger.warning('Не удалось выполнить сценарии')
except Exception as ex:
    logger.error('Ошибка при создании или выполнении сценариев поставщика', ex, exc_info=True)
```
```python
from src.suppliers.supplier import Supplier
from src.logger.logger import logger

# Пример создания экземпляра класса Supplier с неправильным supplier_prefix
try:
    supplier = Supplier(supplier_prefix='')
except Exception as ex:
    logger.error('Ошибка при создании или выполнении сценариев поставщика', ex, exc_info=True)