# Модуль тестирования поставщика

## Обзор

Модуль `test_supplier.py` содержит набор юнит-тестов для класса `Supplier`. Он использует библиотеку `unittest` для организации тестовых случаев и `unittest.mock` для имитации зависимостей и изоляции тестируемого кода.

## Подробней

Этот модуль предназначен для проверки правильности инициализации, загрузки настроек и выполнения сценариев класса `Supplier`. Он охватывает различные аспекты работы класса, включая взаимодействие с веб-драйвером, API и файлами конфигурации.

## Классы

### `TestSupplier`

**Описание**: Класс `TestSupplier` является производным от `unittest.TestCase` и содержит набор тестов для класса `Supplier`.

**Наследует**: `unittest.TestCase`

**Атрибуты**:
- `supplier_prefix` (str): Префикс поставщика, используемый в тестах.
- `lang` (str): Язык, используемый в тестах.
- `method` (str): Метод парсинга, используемый в тестах (`web` или `api`).
- `supplier_settings` (dict): Настройки поставщика, используемые в тестах.
- `locators` (dict): Локаторы элементов, используемые в тестах.
- `supplier` (Supplier): Экземпляр класса `Supplier`, используемый в тестах.
- `settings_file` (Path): Путь к файлу настроек поставщика.
- `locators_file` (Path): Путь к файлу локаторов элементов.

**Методы**:
- `setUp()`: Метод, выполняющийся перед каждым тестовым случаем. Инициализирует атрибуты класса для каждого теста.
- `test_init_webdriver()`: Тестирует инициализацию класса `Supplier` с методом парсинга `webdriver`.
- `test_init_api()`: Тестирует инициализацию класса `Supplier` с методом парсинга `api`.
- `test_supplier_load_settings_success()`: Проверяет успешную загрузку настроек поставщика.
- `test_supplier_load_settings_failure()`: Проверяет неудачную загрузку настроек поставщика.
- `test_load_settings()`: Проверяет загрузку настроек.
- `test_load_settings_invalid_path()`: Проверяет обработку неверного пути к настройкам.
- `test_load_settings_invalid_locators_path()`: Проверяет обработку неверного пути к локаторам.
- `test_load_settings_api()`: Проверяет загрузку настроек при использовании API.
- `test_load_related_functions()`: Проверяет загрузку связанных функций.
- `test_init()`: Проверяет инициализацию основных параметров класса `Supplier`.
- `test_load_settings_success()`: Проверяет успешную загрузку настроек поставщика.
- `test_load_settings_failure()`: Проверяет неудачную загрузку настроек поставщика.
- `test_run_api()`: Тестирует выполнение API.
- `test_run_scenario_files_success()`: Тестирует успешное выполнение файлов сценариев.
- `test_run_scenario_files_failure()`: Тестирует неудачное выполнение файлов сценариев.
- `test_run_with_login()`: Тестирует выполнение с логином.
- `test_run_without_login()`: Тестирует выполнение без логина.

## Методы класса

### `setUp`

```python
def setUp(self):
    """
    Инициализирует атрибуты класса для каждого тестового случая.
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

**Назначение**: Инициализация тестового окружения перед каждым тестом.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
Метод `setUp` инициализирует атрибуты класса, такие как префикс поставщика, язык, метод парсинга, настройки поставщика, локаторы элементов, экземпляр класса `Supplier`, путь к файлу настроек и путь к файлу локаторов. Эти атрибуты используются в дальнейших тестах для проверки правильности работы класса `Supplier`.

**Примеры**:
```python
class TestSupplier(unittest.TestCase):
    def setUp(self):
        self.supplier_prefix = 'test_supplier'
        ...
```

### `test_init_webdriver`

```python
@patch('mymodule.supplier.gs.j_loads')
@patch('mymodule.supplier.Driver')
def test_init_webdriver(self, mock_driver, mock_j_loads):
    """
    Тестирует инициализацию класса `Supplier` с методом парсинга `webdriver`.

    Args:
        mock_driver (MagicMock): Заглушка для класса `Driver`.
        mock_j_loads (MagicMock): Заглушка для функции `j_loads`.
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

**Назначение**: Тестирование инициализации класса `Supplier` при использовании `webdriver` для парсинга.

**Параметры**:
- `mock_driver` (MagicMock): Заглушка для класса `Driver`.
- `mock_j_loads` (MagicMock): Заглушка для функции `j_loads`.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
Этот метод использует `unittest.mock.patch` для замены `Driver` и `j_loads` на заглушки `MagicMock`. Это позволяет изолировать код инициализации `Supplier` и проверить, что он правильно вызывает `j_loads` для загрузки настроек поставщика и инициализирует `Driver`. Утверждения `self.assertEqual` используются для проверки того, что атрибуты `Supplier` правильно установлены на основе загруженных настроек.

**Примеры**:
```python
@patch('mymodule.supplier.gs.j_loads')
@patch('mymodule.supplier.Driver')
def test_init_webdriver(self, mock_driver, mock_j_loads):
    mock_j_loads.return_value = self.supplier_settings
    mock_driver.return_value = MagicMock()
    supplier = Supplier(self.supplier_prefix, self.lang, self.method)
    ...
```

### `test_init_api`

```python
@patch('mymodule.supplier.gs.j_loads')
def test_init_api(self, mock_j_loads):
    """
    Тестирует инициализацию класса `Supplier` с методом парсинга `api`.

    Args:
        mock_j_loads (MagicMock): Заглушка для функции `j_loads`.
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

**Назначение**: Тестирование инициализации класса `Supplier` при использовании `api` для парсинга.

**Параметры**:
- `mock_j_loads` (MagicMock): Заглушка для функции `j_loads`.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
Этот метод аналогичен `test_init_webdriver`, но предназначен для тестирования инициализации `Supplier` с методом парсинга `api`. Он также использует `unittest.mock.patch` для замены `j_loads` на заглушку `MagicMock` и проверяет, что атрибуты `Supplier` правильно установлены на основе загруженных настроек.

**Примеры**:
```python
@patch('mymodule.supplier.gs.j_loads')
def test_init_api(self, mock_j_loads):
    self.method = 'api'
    mock_j_loads.return_value = self.supplier_settings
    supplier = Supplier(self.supplier_prefix, self.lang, self.method)
    ...
```

### `test_supplier_load_settings_success`

```python
def test_supplier_load_settings_success():
    """
    Проверяет успешную загрузку настроек поставщика.
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

**Назначение**: Проверка успешной загрузки настроек поставщика по умолчанию.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
Метод создает экземпляр класса `Supplier` с префиксом `dummy` и проверяет, что все основные параметры класса были успешно загружены и имеют ожидаемые значения по умолчанию. Это важный тест, чтобы убедиться, что при создании поставщика с указанным префиксом все работает правильно.

**Примеры**:
```python
def test_supplier_load_settings_success():
    supplier = Supplier(supplier_prefix='dummy')
    assert supplier.supplier_id == 'dummy'
    ...
```

### `test_supplier_load_settings_failure`

```python
def test_supplier_load_settings_failure():
    """
    Проверяет неудачную загрузку настроек поставщика.
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

**Назначение**: Проверка неудачной загрузки настроек поставщика, когда поставщик не существует.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
Метод создает экземпляр класса `Supplier` с префиксом `nonexistent` (то есть поставщик, которого не существует) и проверяет, что все основные параметры класса равны `None` или пустой строке. Это позволяет убедиться, что в случае отсутствия поставщика класс обрабатывает это корректно.

**Примеры**:
```python
def test_supplier_load_settings_failure():
    supplier = Supplier(supplier_prefix='nonexistent')
    assert supplier.supplier_id == None
    ...
```

### `test_load_settings`

```python
def test_load_settings(supplier):
    """
    Проверяет загрузку настроек.

    Args:
        supplier: Экземпляр класса `Supplier` для тестирования.
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

**Назначение**: Проверка загрузки корректных настроек для поставщика.

**Параметры**:
- `supplier`: Экземпляр класса `Supplier` для тестирования.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
Метод проверяет, что экземпляр класса `Supplier` загружает все необходимые параметры из файла настроек и устанавливает их значения правильно.

**Примеры**:
```python
def test_load_settings(supplier):
    assert supplier.supplier_prefix == 'example_supplier'
    assert supplier.lang == 'en'
    ...
```

### `test_load_settings_invalid_path`

```python
def test_load_settings_invalid_path(supplier, caplog):
    """
    Проверяет обработку неверного пути к настройкам.

    Args:
        supplier: Экземпляр класса `Supplier` для тестирования.
        caplog: Объект для захвата логов.
    """
    supplier._load_settings()
    assert 'Error reading suppliers/example_supplier/example_supplier.json' in caplog.text
```

**Назначение**: Проверка обработки ситуации, когда путь к файлу настроек неверен.

**Параметры**:
- `supplier`: Экземпляр класса `Supplier` для тестирования.
- `caplog`: Объект для захвата логов.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
Метод вызывает функцию `_load_settings()` у экземпляра `supplier` и проверяет, что в логах присутствует сообщение об ошибке, указывающее на неверный путь к файлу настроек.

**Примеры**:
```python
def test_load_settings_invalid_path(supplier, caplog):
    supplier._load_settings()
    assert 'Error reading suppliers/example_supplier/example_supplier.json' in caplog.text
```

### `test_load_settings_invalid_locators_path`

```python
def test_load_settings_invalid_locators_path(supplier, caplog):
    """
    Проверяет обработку неверного пути к локаторам.

    Args:
        supplier: Экземпляр класса `Supplier` для тестирования.
        caplog: Объект для захвата логов.
    """
    supplier.scrapping_method = 'api'
    supplier._load_settings()
    assert 'Error reading suppliers/example_supplier/locators.json' in caplog.text
```

**Назначение**: Проверка обработки ситуации, когда путь к файлу локаторов неверен.

**Параметры**:
- `supplier`: Экземпляр класса `Supplier` для тестирования.
- `caplog`: Объект для захвата логов.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
Метод устанавливает метод сбора данных поставщика на `api`, вызывает функцию `_load_settings()` и проверяет, что в логах присутствует сообщение об ошибке, указывающее на неверный путь к файлу локаторов.

**Примеры**:
```python
def test_load_settings_invalid_locators_path(supplier, caplog):
    supplier.scrapping_method = 'api'
    supplier._load_settings()
    assert 'Error reading suppliers/example_supplier/locators.json' in caplog.text
```

### `test_load_settings_api`

```python
def test_load_settings_api(supplier):
    """
    Проверяет загрузку настроек при использовании API.

    Args:
        supplier: Экземпляр класса `Supplier` для тестирования.
    """
    supplier.scrapping_method = 'api'
    assert supplier.locators is None
    assert supplier.driver is None
```

**Назначение**: Проверяет, что при использовании API локаторы и драйвер не загружаются.

**Параметры**:
- `supplier`: Экземпляр класса `Supplier` для тестирования.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
Метод устанавливает метод сбора данных поставщика на `api` и проверяет, что атрибуты `locators` и `driver` равны `None`.

**Примеры**:
```python
def test_load_settings_api(supplier):
    supplier.scrapping_method = 'api'
    assert supplier.locators is None
    assert supplier.driver is None
```

### `test_load_related_functions`

```python
def test_load_related_functions(supplier):
    """
    Проверяет загрузку связанных функций.

    Args:
        supplier: Экземпляр класса `Supplier` для тестирования.
    """
    assert hasattr(supplier, 'related_modules')
    assert hasattr(supplier.related_modules, 'example_function')
```

**Назначение**: Проверяет, что связанные функции загружаются корректно.

**Параметры**:
- `supplier`: Экземпляр класса `Supplier` для тестирования.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
Метод проверяет наличие атрибута `related_modules` у экземпляра `supplier` и наличие функции `example_function` в этом атрибуте.

**Примеры**:
```python
def test_load_related_functions(supplier):
    assert hasattr(supplier, 'related_modules')
    assert hasattr(supplier.related_modules, 'example_function')
```

### `test_init`

```python
def test_init(supplier):
    """
    Проверяет инициализацию основных параметров класса `Supplier`.

    Args:
        supplier: Экземпляр класса `Supplier` для тестирования.
    """
    assert supplier.driver is not None
    assert isinstance(supplier.p, list)
    assert isinstance(supplier.c, list)
    assert supplier.current_scenario_filename is None
    assert supplier.current_scenario is None
```

**Назначение**: Проверка инициализации различных атрибутов класса `Supplier`.

**Параметры**:
- `supplier`: Экземпляр класса `Supplier` для тестирования.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
Метод проверяет, что драйвер инициализирован, `p` и `c` являются списками, а `current_scenario_filename` и `current_scenario` равны `None`.

**Примеры**:
```python
def test_init(supplier):
    assert supplier.driver is not None
    assert isinstance(supplier.p, list)
    ...
```

### `test_load_settings_success`

```python
def test_load_settings_success(self):
    """
    Проверяет успешную загрузку настроек поставщика.
    """
    with patch('builtins.open', return_value=MagicMock(spec=open, read=lambda: json.dumps({'supplier_id': 123}))) as mock_open:
        result = self.supplier._load_settings()
        self.assertTrue(result)
        self.assertEqual(self.supplier.supplier_id, 123)
```

**Назначение**: Проверяет успешную загрузку настроек поставщика, используя `MagicMock` для имитации открытия и чтения файла настроек.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
Используется `patch` для замены встроенной функции `open` объектом `MagicMock`, который имитирует открытие и чтение файла JSON с настройками. Затем вызывается метод `_load_settings` поставщика и проверяется, что настройки загружены успешно и `supplier_id` установлен в ожидаемое значение.

**Примеры**:
```python
def test_load_settings_success(self):
    with patch('builtins.open', return_value=MagicMock(...)) as mock_open:
        result = self.supplier._load_settings()
        ...
```

### `test_load_settings_failure`

```python
def test_load_settings_failure(self):
    """
    Проверяет неудачную загрузку настроек поставщика.
    """
    with patch('builtins.open', side_effect=Exception):
        result = self.supplier._load_settings()
        self.assertFalse(result)
```

**Назначение**: Проверяет, что метод `_load_settings` возвращает `False` при возникновении исключения во время загрузки настроек.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
Используется `patch` для вызова исключения при попытке открыть файл настроек. Затем вызывается метод `_load_settings` поставщика и проверяется, что метод вернул `False`, что свидетельствует о неудачной загрузке настроек.

**Примеры**:
```python
def test_load_settings_failure(self):
    with patch('builtins.open', side_effect=Exception):
        result = self.supplier._load_settings()
        self.assertFalse(result)
```

### `test_run_api`

```python
def test_run_api(self):
    """
    Тестирует выполнение API.
    """
    with patch('my_module.supplier.importlib.import_module') as mock_import:
        mock_module = MagicMock()
        mock_module.run_api.return_value = True
        mock_import.return_value = mock_module
        result = self.supplier.run()
        self.assertTrue(result)
```

**Назначение**: Проверка успешного выполнения API путем имитации импорта модуля и вызова функции `run_api`.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
Метод использует `patch` для имитации импорта модуля `my_module.supplier`. Создается объект `MagicMock` для имитации модуля и устанавливается возвращаемое значение функции `run_api` в `True`. Затем вызывается метод `run` поставщика и проверяется, что он возвращает `True`, что указывает на успешное выполнение API.

**Примеры**:
```python
def test_run_api(self):
    with patch('my_module.supplier.importlib.import_module') as mock_import:
        mock_module = MagicMock()
        mock_module.run_api.return_value = True
        ...
```

### `test_run_scenario_files_success`

```python
def test_run_scenario_files_success(self):
    """
    Тестирует успешное выполнение файлов сценариев.
    """
    with patch.object(self.supplier, 'login', return_value=True):
        self.supplier._load_settings()
        scenario_file = Path(__file__).parent / 'data/example_supplier/scenario.json'
        result = self.supplier.run_scenario_files(str(scenario_file))
        self.assertTrue(result)
```

**Назначение**: Проверка успешного выполнения сценариев из файла, имитируя успешный логин.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
Метод использует `patch.object` для имитации успешного логина поставщика. Затем загружаются настройки поставщика, определяется путь к файлу сценария и вызывается метод `run_scenario_files` с путем к файлу сценария. Проверяется, что метод возвращает `True`, что указывает на успешное выполнение сценариев.

**Примеры**:
```python
def test_run_scenario_files_success(self):
    with patch.object(self.supplier, 'login', return_value=True):
        self.supplier._load_settings()
        ...
```

### `test_run_scenario_files_failure`

```python
def test_run_scenario_files_failure(self):
    """
    Тестирует неудачное выполнение файлов сценариев.
    """
    with patch.object(self.supplier, 'login', return_value=True):
        self.supplier._load_settings()
        scenario_file = Path(__file__).parent / 'data/example_supplier/invalid_scenario.json'
        result = self.supplier.run_scenario_files(str(scenario_file))
        self.assertFalse(result)
```

**Назначение**: Проверка неудачного выполнения файлов сценариев.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
Аналогично `test_run_scenario_files_success`, но использует файл сценария `invalid_scenario.json`, который предназначен для вызова ошибки. Проверяется, что метод `run_scenario_files` возвращает `False`, что указывает на неудачное выполнение сценариев.

**Примеры**:
```python
def test_run_scenario_files_failure(self):
    with patch.object(self.supplier, 'login', return_value=True):
        self.supplier._load_settings()
        ...
```

### `test_run_with_login`

```python
def test_run_with_login(self):
    """
    Тестирует выполнение с логином.
    """
    with patch.object(self.supplier, 'login', return_value=True) as mock_login:
        self.supplier._load_settings()
        result = self.supplier.run()
        self.assertTrue(mock_login.called)
        self.assertTrue(result)
```

**Назначение**: Проверяет, что при выполнении с логином вызывается функция логина и что выполнение успешно.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
Используется `patch.object` для имитации успешного логина поставщика. Затем загружаются настройки поставщика и вызывается метод `run`. Проверяется, что функция логина была вызвана и что метод `run` возвращает `True`, что указывает на успешное выполнение.

**Примеры**:
```python
def test_run_with_login(self):
    with patch.object(self.supplier, 'login', return_value=True) as mock_login:
        self.supplier._load_settings()
        ...
```

### `test_run_without_login`

```python
def test_run_without_login(self):
    """
    Тестирует выполнение без логина.
    """
    self.supplier.login['if_login'] = False
    with patch.object(self.supplier, 'run_scenario_files', return_value=True) as mock_run_scenario_files:
        self.supplier._load_settings()
        result = self.supplier.run()
        self.assertFalse(mock_run_scenario_files.called_with())
        self.assertTrue(result)
```

**Назначение**: Проверка выполнения без логина.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
Устанавливает значение `'if_login'` в настройках логина поставщика в `False`. Затем использует `patch.object` для имитации успешного выполнения файлов сценариев. Вызывает метод `run` поставщика и проверяет, что функция `run_scenario_files` не была вызвана и что метод `run` возвращает `True`, что указывает на успешное выполнение.

**Примеры**:
```python
def test_run_without_login(self):
    self.supplier.login['if_login'] = False
    with patch.object(self.supplier, 'run_scenario_files', return_value=True) as mock_run_scenario_files:
        self.supplier._load_settings()
        ...