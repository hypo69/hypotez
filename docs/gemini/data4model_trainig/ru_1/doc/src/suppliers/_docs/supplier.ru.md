# Модуль `Supplier`

## Обзор

Модуль содержит базовый класс `Supplier`, который служит основой для работы с поставщиками данных в приложении. Он предоставляет общие методы и атрибуты для реализации различных поставщиков, таких как Amazon, AliExpress и Walmart.

## Подробней

Класс `Supplier` предназначен для упрощения интеграции с различными источниками данных, предоставляя единый интерфейс для настройки, аутентификации и выполнения сценариев сбора данных. Он позволяет абстрагироваться от специфических деталей каждого поставщика, упрощая тем самым разработку и поддержку приложения.

## Классы

### `Supplier`

**Описание**: Базовый класс для работы с поставщиками данных.

**Наследует**: Нет.

**Атрибуты**:
- `supplier_id` (str): Уникальный идентификатор поставщика.
- `supplier_prefix` (str): Префикс поставщика, например, `aliexpress` или `amazon`.
- `supplier_settings` (dict): Настройки поставщика, загруженные из конфигурационного файла.
- `locale` (str): Код локализации (например, `en` для английского, `ru` для русского).
- `price_rule` (Any): Правило для расчета цены.
- `related_modules` (ModuleType): Модуль, содержащий специфические для поставщика функции.
- `scenario_files` (List[str]): Список файлов сценариев для выполнения.
- `current_scenario` (str): Текущий сценарий выполнения.
- `login_data` (dict): Данные для входа на сайт поставщика.
- `locators` (dict): Локаторы для веб-элементов на страницах сайта поставщика.
- `driver` (WebDriver): Веб-драйвер для взаимодействия с сайтом поставщика.
- `parsing_method` (str): Метод парсинга данных (например, `webdriver`, `api`, `xls`, `csv`).

**Принцип работы**:
Класс `Supplier` предоставляет основу для создания конкретных классов поставщиков. При инициализации загружаются настройки поставщика, определяется метод парсинга данных и настраивается веб-драйвер (если необходимо). Затем можно выполнить вход на сайт поставщика и запустить сценарии для сбора данных.

## Методы

### `__init__`

```python
def __init__(self, supplier_prefix: str, locale: str = 'en', webdriver: str | Driver | bool = 'default', *attrs, **kwargs) -> None:
    """
    Инициализирует экземпляр класса `Supplier`.

    Args:
        supplier_prefix (str): Префикс поставщика (например, 'aliexpress').
        locale (str): Код локали (например, 'en'). По умолчанию 'en'.
        webdriver (str | Driver | bool): Тип веб-драйвера или его экземпляр. По умолчанию 'default'.
        *attrs: Дополнительные атрибуты.
        **kwargs: Дополнительные именованные аргументы.

    Raises:
        ValueError: Если `supplier_prefix` не является строкой.

    Пример:
        >>> supplier = Supplier(supplier_prefix='aliexpress', locale='ru', webdriver='firefox')
    """
```

**Назначение**: Инициализация объекта класса `Supplier`.

**Параметры**:
- `supplier_prefix` (str): Префикс поставщика.
- `locale` (str): Локаль поставщика.
- `webdriver` (str | Driver | bool): Веб-драйвер для использования.
- `*attrs`: Дополнительные атрибуты.
- `**kwargs`: Дополнительные именованные аргументы.

**Как работает функция**:
1. Инициализирует атрибуты `supplier_prefix`, `locale` и `webdriver`.
2. Вызывает метод `_payload` для загрузки настроек поставщика и инициализации веб-драйвера.

### `_payload`

```python
def _payload(self, webdriver: str | Driver | bool, *attrs, **kwargs) -> bool:
    """
    Загружает настройки поставщика, конфигурационные файлы и инициализирует веб-драйвер.

    Args:
        webdriver (str | Driver | bool): Тип веб-драйвера или его экземпляр.
        *attrs: Дополнительные атрибуты.
        **kwargs: Дополнительные именованные аргументы.

    Returns:
        bool: `True`, если загрузка выполнена успешно, иначе `False`.

    Raises:
        FileNotFoundError: Если не найден файл конфигурации поставщика.
        Exception: Если произошла ошибка при загрузке настроек или инициализации драйвера.

    Пример:
        >>> supplier = Supplier(supplier_prefix='aliexpress', locale='ru')
        >>> supplier._payload(webdriver='chrome')
        True
    """
```

**Назначение**: Загрузка конфигурации и инициализация веб-драйвера.

**Параметры**:
- `webdriver` (str | Driver | bool): Веб-драйвер для использования.
- `*attrs`: Дополнительные атрибуты.
- `**kwargs`: Дополнительные именованные аргументы.

**Как работает функция**:
1. Определяет путь к файлу конфигурации на основе `supplier_prefix`.
2. Загружает настройки из файла конфигурации с использованием `j_loads_ns`.
3. Инициализирует веб-драйвер, если он не был передан в конструктор.

### `login`

```python
def login(self) -> bool:
    """
    Выполняет вход на сайт поставщика.

    Returns:
        bool: `True`, если вход выполнен успешно, иначе `False`.

    Raises:
        NotImplementedError: Если метод не реализован в подклассе.

    Пример:
        >>> supplier = Supplier(supplier_prefix='aliexpress', locale='ru', webdriver='chrome')
        >>> supplier.login()
        True
    """
```

**Назначение**: Выполнение входа на сайт поставщика.

**Возвращает**:
- `bool`: `True`, если вход выполнен успешно, иначе `False`.

**Как работает функция**:
1. Проверяет, заданы ли данные для входа.
2. Если данные заданы, пытается выполнить вход на сайт, используя данные из `login_data` и локаторы.

### `run_scenario_files`

```python
def run_scenario_files(self, scenario_files: str | List[str] = None) -> bool:
    """
    Запускает выполнение файлов сценариев.

    Args:
        scenario_files (str | List[str]): Путь к файлу сценария или список путей. По умолчанию `None`.

    Returns:
        bool: `True`, если выполнение сценариев завершено успешно, иначе `False`.

    Raises:
        FileNotFoundError: Если не найден файл сценария.
        Exception: Если произошла ошибка при выполнении сценария.

    Пример:
        >>> supplier = Supplier(supplier_prefix='aliexpress', locale='ru', webdriver='chrome')
        >>> supplier.run_scenario_files(['scenario1.json', 'scenario2.json'])
        True
    """
```

**Назначение**: Запуск выполнения сценариев из файлов.

**Параметры**:
- `scenario_files` (str | List[str]): Путь к файлу сценария или список путей.

**Как работает функция**:
1. Проверяет, переданы ли файлы сценариев.
2. Если файлы переданы, загружает их и выполняет каждый сценарий.

### `run_scenarios`

```python
def run_scenarios(self, scenarios: dict | list[dict]) -> bool:
    """
    Запускает один или несколько сценариев.

    Args:
        scenarios (dict | list[dict]): Словарь или список словарей, представляющих сценарии для выполнения.

    Returns:
        bool: `True`, если выполнение сценариев завершено успешно, иначе `False`.

    Raises:
        ValueError: Если `scenarios` не является словарем или списком словарей.
        Exception: Если произошла ошибка при выполнении сценария.

    Пример:
        >>> supplier = Supplier(supplier_prefix='aliexpress', locale='ru', webdriver='chrome')
        >>> supplier.run_scenarios([{'action': 'scrape', 'target': 'product_list'}])
        True
    """
```

**Назначение**: Запуск выполнения одного или нескольких сценариев.

**Параметры**:
- `scenarios` (dict | list[dict]): Сценарии для выполнения.

**Как работает функция**:
1. Проверяет, переданы ли сценарии.
2. Если сценарии переданы, выполняет каждый сценарий.

## Примеры

```python
# Создаем объект для поставщика 'aliexpress'
supplier = Supplier(supplier_prefix='aliexpress', locale='en', webdriver='chrome')

# Выполняем вход на сайт поставщика
supplier.login()

# Запускаем сценарии из файлов
supplier.run_scenario_files(['example_scenario.json'])

# Или запускаем сценарии по определенным условиям
supplier.run_scenarios([{'action': 'scrape', 'target': 'product_list'}])