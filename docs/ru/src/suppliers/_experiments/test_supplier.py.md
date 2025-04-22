# Модуль `test_supplier`

## Обзор

Модуль содержит набор тестов для класса `Supplier`, используемого для взаимодействия с различными поставщиками данных. Здесь определены юнит-тесты, проверяющие инициализацию, загрузку настроек и выполнение сценариев для поставщиков.

## Подробней

Этот модуль предоставляет тесты, которые охватывают различные аспекты работы с поставщиками, включая загрузку настроек из файлов, инициализацию с использованием веб-драйвера или API, а также выполнение сценариев. Он использует `unittest` для организации тестов и `mock` для изоляции тестируемого кода от внешних зависимостей.

## Классы

### `TestSupplier`

**Описание**: Класс `TestSupplier` содержит набор тестов для класса `Supplier`.

**Наследует**: `unittest.TestCase`.

**Атрибуты**:
- `supplier_prefix` (str): Префикс имени поставщика для тестов.
- `lang` (str): Язык поставщика.
- `method` (str): Метод парсинга (`web` или `api`).
- `supplier_settings` (dict): Настройки поставщика для тестов.
- `locators` (dict): Локаторы элементов для веб-драйвера.
- `supplier` (Supplier): Экземпляр класса `Supplier` для тестов.
- `settings_file` (Path): Путь к файлу настроек поставщика.
- `locators_file` (Path): Путь к файлу локаторов элементов.

**Методы**:
- `setUp()`: Метод подготовки тестовой среды перед каждым тестом.
- `test_init_webdriver()`: Тест инициализации поставщика с использованием веб-драйвера.
- `test_init_api()`: Тест инициализации поставщика с использованием API.
- `test_supplier_load_settings_success()`: Тест успешной загрузки настроек поставщика.
- `test_supplier_load_settings_failure()`: Тест неудачной загрузки настроек поставщика.
- `test_load_settings()`: Тест загрузки настроек.
- `test_load_settings_invalid_path()`: Тест обработки неверного пути к настройкам.
- `test_load_settings_invalid_locators_path()`: Тест обработки неверного пути к локаторам.
- `test_load_settings_api()`: Тест загрузки настроек для API.
- `test_load_related_functions()`: Тест загрузки связанных функций.
- `test_init()`: Тест инициализации экземпляра `Supplier`.
- `test_load_settings_success()`: Тест успешной загрузки настроек поставщика.
- `test_load_settings_failure()`: Тест неудачной загрузки настроек поставщика.
- `test_run_api()`: Тест запуска поставщика через API.
- `test_run_scenario_files_success()`: Тест успешного выполнения сценариев из файлов.
- `test_run_scenario_files_failure()`: Тест неудачного выполнения сценариев из файлов.
- `test_run_with_login()`: Тест запуска поставщика с авторизацией.
- `test_run_without_login()`: Тест запуска поставщика без авторизации.

## Методы класса

### `setUp`

```python
def setUp(self):
    """
    Метод подготовки тестовой среды перед каждым тестом.

    Выполняет настройку тестового окружения, инициализирует атрибуты класса
    значениями, необходимыми для проведения тестов. Определяет префикс
    поставщика, язык, метод парсинга, настройки поставщика, локаторы элементов,
    создает экземпляр класса `Supplier`, а также определяет пути к файлам
    настроек и локаторов.
    """
    self.supplier_prefix = 'test_supplier'
    self.lang = 'en'
    self.method = 'web'
    self.supplier_settings = {
        'supplier_id': '123',
        'price_rule': '*1.2',
        'if_login': True,
        'login_url': 'http://example.com/login',
        'start_url': 'http://example.com/start',
        'parcing method [webdriver|api]': 'webdriver',
        'scenarios': [
            {'name': 'scenario1', 'file': 'scenario1.json'},
            {'name': 'scenario2', 'file': 'scenario2.json'},
        ]
    }
    self.locators = {
        'search_box': {'xpath': '//*[@id="search-box"]'},
        'search_button': {'xpath': '//*[@id="search-button"]'},
        'product_name': {'xpath': '//*[@id="product-name"]'},
        'product_price': {'xpath': '//*[@id="product-price"]'},
    }
    self.supplier = Supplier('example_supplier')
    self.settings_file = Path(__file__).parent / 'data/example_supplier/example_supplier.json'
    self.locators_file = Path(__file__).parent / 'data/example_supplier/locators.json'
```

### `test_init_webdriver`

```python
@patch('mymodule.supplier.gs.j_loads')
@patch('mymodule.supplier.Driver')
def test_init_webdriver(self, mock_driver, mock_j_loads):
    """
    Тест инициализации поставщика с использованием веб-драйвера.

    Args:
        mock_driver (MagicMock): Заглушка для класса `Driver`.
        mock_j_loads (MagicMock): Заглушка для функции `j_loads`.

    Описание:
        Тест проверяет корректность инициализации класса `Supplier` при использовании
        веб-драйвера. Подменяет функции `j_loads` и класс `Driver` заглушками,
        устанавливает возвращаемые значения для `j_loads` и проверяет, что
        атрибуты экземпляра `Supplier` инициализированы правильно.
        Также проверяет, что `j_loads` и `Driver` были вызваны с ожидаемыми аргументами.
    """
    mock_j_loads.return_value = self.supplier_settings
    mock_driver.return_value = MagicMock()
    supplier = Supplier(self.supplier_prefix, self.lang, self.method)
    self.assertEqual(supplier.supplier_prefix, self.supplier_prefix)
    self.assertEqual(supplier.lang, self.lang)
    self.assertEqual(supplier.scrapping_method, self.method)
    self.assertEqual(supplier.supplier_id, self.supplier_settings['supplier_id'])
    self.assertEqual(supplier.price_rule, self.supplier_settings['price_rule'])
    self.assertEqual(supplier.login_data['if_login'], self.supplier_settings['if_login'])
    self.assertEqual(supplier.login_data['login_url'], self.supplier_settings['login_url'])
    self.assertEqual(supplier.start_url, self.supplier_settings['start_url'])
    self.assertEqual(supplier.scenarios, self.supplier_settings['scenarios'])
    mock_j_loads.assert_called_once_with(Path('suppliers', self.supplier_prefix, f'{self.supplier_prefix}.json'))
    mock_driver.assert_called_once()
```

### `test_init_api`

```python
@patch('mymodule.supplier.gs.j_loads')
def test_init_api(self, mock_j_loads):
    """
    Тест инициализации поставщика с использованием API.

    Args:
        mock_j_loads (MagicMock): Заглушка для функции `j_loads`.

    Описание:
        Тест проверяет корректность инициализации класса `Supplier` при использовании API.
        Подменяет функцию `j_loads` заглушкой, устанавливает возвращаемое значение
        и проверяет, что атрибуты экземпляра `Supplier` инициализированы правильно.
        Также проверяет, что `j_loads` была вызвана с ожидаемыми аргументами.
    """
    self.method = 'api'
    mock_j_loads.return_value = self.supplier_settings
    supplier = Supplier(self.supplier_prefix, self.lang, self.method)
    self.assertEqual(supplier.supplier_prefix, self.supplier_prefix)
    self.assertEqual(supplier.lang, self.lang)
    self.assertEqual(supplier.scrapping_method, self.method)
    self.assertEqual(supplier.supplier_id, self.supplier_settings['supplier_id'])
    self.assertEqual(supplier.price_rule, self.supplier_settings['price_rule'])
    self.assertEqual(supplier.login_data['if_login'], self.supplier_settings['if_login'])
    self.assertEqual(supplier.login_data['login_url'], self.supplier_settings['login_url'])
    self.assertEqual(supplier.start_url, self.supplier_settings['start_url'])
    self.assertEqual(supplier.scenarios, self.supplier_settings['scenarios'])
    mock_j_loads.assert_called_once_with(Path('suppliers', self.supplier_prefix, f'{self.supplier_prefix}.json'))
```

### `test_supplier_load_settings_success`

```python
def test_supplier_load_settings_success():
    """
    Тест успешной загрузки настроек поставщика.

    Описание:
        Тест проверяет, что при успешной загрузке настроек поставщика атрибуты
        экземпляра `Supplier` инициализируются значениями по умолчанию.
    """
    supplier = Supplier(supplier_prefix='dummy')
    assert supplier.supplier_id == 'dummy'
    assert supplier.price_rule == 'dummy'
    assert supplier.login_data == {
        'if_login': None,
        'login_url': None,
        'user': None,
        'password': None,
    }
    assert supplier.start_url == 'dummy'
    assert supplier.scrapping_method == 'web'
    assert supplier.scenarios == []
```

### `test_supplier_load_settings_failure`

```python
def test_supplier_load_settings_failure():
    """
    Тест неудачной загрузки настроек поставщика.

    Описание:
        Тест проверяет, что при неудачной загрузке настроек поставщика атрибуты
        экземпляра `Supplier` инициализируются значением `None` или пустой строкой.
    """
    supplier = Supplier(supplier_prefix='nonexistent')
    assert supplier.supplier_id == None
    assert supplier.price_rule == None
    assert supplier.login_data == {
        'if_login': None,
        'login_url': None,
        'user': None,
        'password': None,
    }
    assert supplier.start_url == None
    assert supplier.scrapping_method == ''
```

### `test_load_settings`

```python
def test_load_settings(supplier):
    """
    Тест загрузки настроек.

    Args:
        supplier (Supplier): Экземпляр класса `Supplier` для теста.

    Описание:
        Тест проверяет, что настройки экземпляра `Supplier` загружаются правильно
        из файла настроек. Сравнивает значения атрибутов экземпляра с ожидаемыми
        значениями.
    """
    assert supplier.supplier_prefix == 'example_supplier'
    assert supplier.lang == 'en'
    assert supplier.scrapping_method == 'web'
    assert supplier.supplier_id == '1234'
    assert supplier.price_rule == 'example_price_rule'
    assert supplier.login_data == {'if_login': True, 'login_url': 'https://example.com/login', 'user': None, 'password': None}
    assert supplier.start_url == 'https://example.com/start'
    assert supplier.scenarios == [{'name': 'scenario1', 'steps': [{'type': 'click', 'locator': 'example_locator'}]}]
    assert supplier.locators == {'example_locator': '//html/body/div'}
```

### `test_load_settings_invalid_path`

```python
def test_load_settings_invalid_path(supplier, caplog):
    """
    Тест обработки неверного пути к настройкам.

    Args:
        supplier (Supplier): Экземпляр класса `Supplier` для теста.
        caplog: Объект для перехвата логов.

    Описание:
        Тест проверяет, что при указании неверного пути к файлу настроек в лог
        записывается сообщение об ошибке.
    """
    supplier._load_settings()
    assert 'Error reading suppliers/example_supplier/example_supplier.json' in caplog.text
```

### `test_load_settings_invalid_locators_path`

```python
def test_load_settings_invalid_locators_path(supplier, caplog):
    """
    Тест обработки неверного пути к локаторам.

    Args:
        supplier (Supplier): Экземпляр класса `Supplier` для теста.
        caplog: Объект для перехвата логов.

    Описание:
        Тест проверяет, что при указании неверного пути к файлу локаторов в лог
        записывается сообщение об ошибке. Устанавливает метод парсинга в `api`
        и проверяет, что сообщение об ошибке содержит информацию о неверном пути
        к файлу `locators.json`.
    """
    supplier.scrapping_method = 'api'
    supplier._load_settings()
    assert 'Error reading suppliers/example_supplier/locators.json' in caplog.text
```

### `test_load_settings_api`

```python
def test_load_settings_api(supplier):
    """
    Тест загрузки настроек для API.

    Args:
        supplier (Supplier): Экземпляр класса `Supplier` для теста.

    Описание:
        Тест проверяет, что при методе парсинга `api` атрибуты `locators` и `driver`
        экземпляра `Supplier` устанавливаются в `None`.
    """
    supplier.scrapping_method = 'api'
    assert supplier.locators is None
    assert supplier.driver is None
```

### `test_load_related_functions`

```python
def test_load_related_functions(supplier):
    """
    Тест загрузки связанных функций.

    Args:
        supplier (Supplier): Экземпляр класса `Supplier` для теста.

    Описание:
        Тест проверяет, что атрибут `related_modules` экземпляра `Supplier` существует
        и содержит функцию `example_function`.
    """
    assert hasattr(supplier, 'related_modules')
    assert hasattr(supplier.related_modules, 'example_function')
```

### `test_init`

```python
def test_init(supplier):
    """
    Тест инициализации экземпляра `Supplier`.

    Args:
        supplier (Supplier): Экземпляр класса `Supplier` для теста.

    Описание:
        Тест проверяет, что атрибуты `driver`, `p`, `c`, `current_scenario_filename`
        и `current_scenario` экземпляра `Supplier` инициализированы правильно.
    """
    assert supplier.driver is not None
    assert isinstance(supplier.p, list)
    assert isinstance(supplier.c, list)
    assert supplier.current_scenario_filename is None
    assert supplier.current_scenario is None
```

### `test_load_settings_success`

```python
def test_load_settings_success(self):
    """
    Тест успешной загрузки настроек поставщика.

    Описание:
        Тест проверяет, что при успешной загрузке настроек поставщика атрибут
        `supplier_id` экземпляра `Supplier` устанавливается в значение,
        загруженное из файла настроек. Использует `patch` для подмены функции
        `open` и возвращает фиктивные данные JSON.
    """
    with patch('builtins.open', return_value=MagicMock(spec=open, read=lambda: json.dumps({'supplier_id': 123}))) as mock_open:
        result = self.supplier._load_settings()
        self.assertTrue(result)
        self.assertEqual(self.supplier.supplier_id, 123)
```

### `test_load_settings_failure`

```python
def test_load_settings_failure(self):
    """
    Тест неудачной загрузки настроек поставщика.

    Описание:
        Тест проверяет, что при неудачной загрузке настроек поставщика метод
        `_load_settings` возвращает `False`. Использует `patch` для подмены
        функции `open` и вызывает исключение.
    """
    with patch('builtins.open', side_effect=Exception):
        result = self.supplier._load_settings()
        self.assertFalse(result)
```

### `test_run_api`

```python
def test_run_api(self):
    """
    Тест запуска поставщика через API.

    Описание:
        Тест проверяет, что при запуске поставщика через API вызывается функция
        `run_api` из импортированного модуля. Использует `patch` для подмены
        функции `importlib.import_module` и возвращает фиктивный модуль с
        функцией `run_api`.
    """
    with patch('my_module.supplier.importlib.import_module') as mock_import:
        mock_module = MagicMock()
        mock_module.run_api.return_value = True
        mock_import.return_value = mock_module
        result = self.supplier.run()
        self.assertTrue(result)
```

### `test_run_scenario_files_success`

```python
def test_run_scenario_files_success(self):
    """
    Тест успешного выполнения сценариев из файлов.

    Описание:
        Тест проверяет, что при успешном выполнении сценариев из файлов метод
        `run_scenario_files` возвращает `True`. Использует `patch.object` для
        подмены метода `login` и `_load_settings`, а также указывает путь к файлу
        сценария.
    """
    with patch.object(self.supplier, 'login', return_value=True):
        self.supplier._load_settings()
        scenario_file = Path(__file__).parent / 'data/example_supplier/scenario.json'
        result = self.supplier.run_scenario_files(str(scenario_file))
        self.assertTrue(result)
```

### `test_run_scenario_files_failure`

```python
def test_run_scenario_files_failure(self):
    """
    Тест неудачного выполнения сценариев из файлов.

    Описание:
        Тест проверяет, что при неудачном выполнении сценариев из файлов метод
        `run_scenario_files` возвращает `False`. Использует `patch.object` для
        подмены метода `login` и `_load_settings`, а также указывает путь к файлу
        с неверным сценарием.
    """
    with patch.object(self.supplier, 'login', return_value=True):
        self.supplier._load_settings()
        scenario_file = Path(__file__).parent / 'data/example_supplier/invalid_scenario.json'
        result = self.supplier.run_scenario_files(str(scenario_file))
        self.assertFalse(result)
```

### `test_run_with_login`

```python
def test_run_with_login(self):
    """
    Тест запуска поставщика с авторизацией.

    Описание:
        Тест проверяет, что при запуске поставщика с авторизацией вызывается метод
        `login`. Использует `patch.object` для подмены метода `login` и проверяет,
        что он был вызван.
    """
    with patch.object(self.supplier, 'login', return_value=True) as mock_login:
        self.supplier._load_settings()
        result = self.supplier.run()
        self.assertTrue(mock_login.called)
        self.assertTrue(result)
```

### `test_run_without_login`

```python
def test_run_without_login(self):
    """
    Тест запуска поставщика без авторизации.

    Описание:
        Тест проверяет, что при запуске поставщика без авторизации не вызывается
        метод `run_scenario_files`. Использует `patch.object` для подмены метода
        `run_scenario_files` и проверяет, что он не был вызван.
    """
    self.supplier.login['if_login'] = False
    with patch.object(self.supplier, 'run_scenario_files', return_value=True) as mock_run_scenario_files:
        self.supplier._load_settings()
        result = self.supplier.run()
        self.assertFalse(mock_run_scenario_files.called_with())
        self.assertTrue(result)
```

## Параметры класса

- `supplier_prefix` (str): Префикс имени поставщика для тестов.
- `lang` (str): Язык поставщика.
- `method` (str): Метод парсинга (`web` или `api`).
- `supplier_settings` (dict): Настройки поставщика для тестов.
- `locators` (dict): Локаторы элементов для веб-драйвера.
- `supplier` (Supplier): Экземпляр класса `Supplier` для тестов.
- `settings_file` (Path): Путь к файлу настроек поставщика.
- `locators_file` (Path): Путь к файлу локаторов элементов.