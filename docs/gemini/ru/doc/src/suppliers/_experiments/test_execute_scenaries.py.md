# Модуль для тестирования выполнения сценариев

## Обзор

Модуль содержит тесты для проверки функциональности выполнения сценариев парсинга данных.
Он включает в себя тесты для запуска сценариев из файлов, запуска отдельных сценариев и извлечения данных со страниц продуктов.

## Подробней

Этот модуль предоставляет набор тестов для проверки правильности работы функций, отвечающих за выполнение сценариев парсинга.
Он включает в себя тестирование различных сценариев, таких как запуск сценариев из файлов, запуск отдельных сценариев и обработка данных, полученных со страниц продуктов.
Анализируя результаты этих тестов, можно убедиться в стабильности и надежности работы системы парсинга.

## Классы

### `TestRunListOfScenarioFiles`

**Описание**: Класс содержит тесты для функции `run_scenarios`, которая отвечает за запуск списка файлов сценариев.

**Наследует**: `unittest.TestCase`

**Методы**:

- `test_with_scenario_files_...ed`: Тест проверяет запуск сценариев из списка файлов.
- `test_with_no_scenario_files_...ed`: Тест проверяет запуск сценариев, когда список файлов не предоставлен.

### `TestRunScenarioFile`

**Описание**: Класс содержит тесты для функции `run_scenario_file`, которая отвечает за запуск сценария из файла.

**Наследует**: `unittest.TestCase`

**Методы**:

- `setUp`: Подготавливает тестовое окружение, создавая mock-объекты и настраивая необходимые атрибуты.
- `test_run_scenario_file_webdriver`: Тест проверяет запуск сценария из файла с использованием webdriver.
- `test_run_scenario_file_api`: Тест проверяет запуск сценария из файла с использованием API.
- `test_run_scenario_file_no_scenarios`: Тест проверяет ситуацию, когда файл сценария не содержит сценариев.

### `TestGrabProductPage`

**Описание**: Класс содержит тесты для функции `grab_product_page`, которая отвечает за извлечение данных со страницы продукта.

**Наследует**: `unittest.TestCase`

**Методы**:

- `setUp`: Подготавливает тестовое окружение, создавая mock-объекты и настраивая необходимые атрибуты.
- `test_grab_product_page_succesStringFormatterul`: Тест проверяет успешное извлечение данных со страницы продукта.
- `test_grab_product_page_failure`: Тест проверяет ситуацию, когда не удается извлечь данные со страницы продукта.

### `TestRunScenario`

**Описание**: Класс содержит тесты для функции `run_scenario`, которая отвечает за запуск отдельного сценария.

**Наследует**: `unittest.TestCase`

**Методы**:

- `setUp`: Подготавливает тестовое окружение, создавая mock-объекты и настраивая необходимые атрибуты.
- `tearDown`: Выполняет очистку после каждого теста.
- `test_run_scenario_no_url`: Тест проверяет ситуацию, когда в сценарии не указан URL.
- `test_run_scenario_valid_url`: Тест проверяет запуск сценария с валидным URL.
- `test_run_scenario_export_empty_list`: Тест проверяет ситуацию, когда список продуктов для экспорта пуст.

## Функции

### `run_scenarios`

```python
def run_scenarios(s, scenario_files):
    """
    Запускает сценарии парсинга, определенные в предоставленных файлах сценариев.

    Args:
        s (MagicMock): Mock-объект, представляющий поставщика (Supplier).
        scenario_files (list, optional): Список имен файлов сценариев для запуска. Если не указан, используются сценарии из настроек поставщика.

    Returns:
        bool: Возвращает True, если все сценарии успешно выполнены, иначе False.

    Raises:
        AssertionError: Если `s` не является экземпляром `MagicMock`.

    Example:
        >>> s = MagicMock()
        >>> scenario_files = ["scenario1.json", "scenario2.json"]
        >>> s.settings = {
        ...     'check categories on site': False,
        ...     'scenarios': ["default1.json", "default2.json"]
        ... }
        >>> result = run_scenarios(s, scenario_files)
        >>> assert result is True
    """
    ...
```

### `run_scenario_file`

```python
def run_scenario_file(s, scenario_file):
    """
    Запускает сценарии, определенные в указанном файле сценария.

    Args:
        s (MagicMock): Mock-объект, представляющий поставщика (Supplier).
        scenario_file (str): Имя файла сценария для запуска.

    Returns:
        bool: Возвращает True, если сценарии успешно выполнены, иначе False.

    Raises:
        AssertionError: Если `s` не является экземпляром `MagicMock`.

    Example:
        >>> s = MagicMock()
        >>> s.current_scenario_filename = "test_scenario.json"
        >>> s.settings = {
        ...     "parcing method [webdriver|api]": "webdriver"
        ... }
        >>> s.dir_export_imagesECTORY_FOR_STORE = "/path/to/images"
        >>> s.scenarios = {
        ...     "scenario1": {
        ...         "url": "https://example.com",
        ...         "steps": []
        ...     }
        ... }
        >>> result = run_scenario_file(s, "test_scenario.json")
        >>> assert result is True
    """
    ...
```

### `run_scenario`

```python
def run_scenario(self, scenario: dict) -> bool:
    """
    Выполняет сценарий парсинга, определенный в словаре `scenario`.

    Args:
        scenario (dict): Словарь, содержащий параметры сценария, такие как 'name' и 'url'.

    Returns:
        bool: Возвращает `True`, если выполнение сценария завершилось успешно, и `False` в противном случае.

    Raises:
        Исключения не вызываются напрямую, но могут быть вызваны внутри вызываемых методов, таких как `self.get_list_products_in_category`, `self.grab_product_page` и `self.export_files`.

    Пример:
        >>> supplier = Supplier()
        >>> supplier.settings['parcing method [webdriver|api]'] = 'webdriver'
        >>> supplier.current_scenario_filename = 'test_scenario.json'
        >>> supplier.export_file_name = 'test_export'
        >>> supplier.dir_export_imagesECTORY_FOR_STORE = '/test/path'
        >>> supplier.p = []
        >>> scenario = {'name': 'scenario2', 'url': 'https://example.com/products'}
        >>> supplier.scenarios = {'scenario2': scenario}
        >>> supplier.get_list_products_in_category = MagicMock(return_value=['https://example.com/products/1', 'https://example.com/products/2'])
        >>> supplier.grab_product_page = MagicMock(return_value=True)
        >>> supplier.export_files = MagicMock()
        >>> result = supplier.run_scenario(scenario)
        >>> assert result is True
    """
    ...
```

### `grab_product_page`

```python
def grab_product_page(s):
    """
    Извлекает данные со страницы продукта, используя метод `grab_product_page` объекта `s`.

    Args:
        s (Supplier): Объект, представляющий поставщика (Supplier), с методом `grab_product_page`.

    Returns:
        bool: Возвращает True, если все необходимые данные успешно извлечены и добавлены в список продуктов `s.p`, иначе False.

    Raises:
        AssertionError: Если `s` не является экземпляром `Supplier`.

    Example:
        >>> s = Supplier()
        >>> s.grab_product_page = lambda _: {'id': '123', 'price': 19.99, 'name': 'Product Name'}
        >>> result = grab_product_page(s)
        >>> assert result is True
        >>> assert len(s.p) == 1
        >>> assert s.p[0]['id'] == '123'
        >>> assert s.p[0]['price'] == 19.99
        >>> assert s.p[0]['name'] == 'Product Name'
    """
    ...