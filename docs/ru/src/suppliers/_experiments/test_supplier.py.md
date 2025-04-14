# Модуль для тестирования класса Supplier
## Обзор

Модуль `test_supplier.py` содержит набор тестов для класса `Supplier`, расположенного в модуле `mymodule.supplier`. Он использует библиотеку `unittest` для определения тестовых случаев и `unittest.mock` для имитации зависимостей, таких как чтение файлов и взаимодействие с веб-драйвером.

## Подробней

Этот модуль предназначен для проверки корректности инициализации, загрузки настроек и выполнения сценариев класса `Supplier`. Тесты охватывают различные аспекты функциональности класса, включая работу с веб-драйвером и API, загрузку параметров из файлов конфигурации и выполнение сценариев.

## Классы

### `TestSupplier`

**Описание**: Класс `TestSupplier` является подклассом `unittest.TestCase` и содержит набор тестовых методов для проверки класса `Supplier`.

**Наследует**:
- `unittest.TestCase`

**Атрибуты**:
- `supplier_prefix` (str): Префикс поставщика, используемый в тестах.
- `lang` (str): Язык, используемый в тестах.
- `method` (str): Метод парсинга, используемый в тестах ('web' или 'api').
- `supplier_settings` (dict): Настройки поставщика, используемые в тестах.
- `locators` (dict): Локаторы элементов веб-страницы, используемые в тестах.
- `supplier` (Supplier): Экземпляр класса `Supplier`, используемый в тестах.
- `settings_file` (Path): Путь к файлу настроек поставщика.
- `locators_file` (Path): Путь к файлу локаторов.

**Методы**:
- `setUp()`: Метод, выполняемый перед каждым тестовым методом. Инициализирует атрибуты класса, необходимые для тестов.
- `test_init_webdriver()`: Тестирует инициализацию класса `Supplier` с методом парсинга 'web'.
- `test_init_api()`: Тестирует инициализацию класса `Supplier` с методом парсинга 'api'.
- `test_supplier_load_settings_success()`: Тестирует успешную загрузку настроек поставщика.
- `test_supplier_load_settings_failure()`: Тестирует неудачную загрузку настроек поставщика.
- `test_load_settings()`: Тестирует загрузку настроек.
- `test_load_settings_invalid_path()`: Тестирует загрузку настроек при неверном пути к файлу.
- `test_load_settings_invalid_locators_path()`: Тестирует загрузку настроек при неверном пути к файлу с локаторами.
- `test_load_settings_api()`: Тестирует загрузку настроек при методе парсинга 'api'.
- `test_load_related_functions()`: Тестирует загрузку связанных функций.
- `test_init()`: Тестирует инициализацию экземпляра класса `Supplier`.
- `test_load_settings_success()`: Тестирует успешную загрузку настроек из файла.
- `test_load_settings_failure()`: Тестирует неудачную загрузку настроек из файла.
- `test_run_api()`: Тестирует запуск поставщика с методом парсинга 'api'.
- `test_run_scenario_files_success()`: Тестирует успешное выполнение сценария из файла.
- `test_run_scenario_files_failure()`: Тестирует неудачное выполнение сценария из файла.
- `test_run_with_login()`: Тестирует запуск поставщика с предварительной авторизацией.
- `test_run_without_login()`: Тестирует запуск поставщика без авторизации.

## Методы класса

### `setUp`

```python
def setUp(self):
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

**Назначение**: Метод `setUp` инициализирует атрибуты класса `TestSupplier` перед каждым тестовым методом.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Метод задает значения атрибутам, таким как `supplier_prefix`, `lang`, `method`, `supplier_settings` и `locators`.
- Создает экземпляр класса `Supplier` с префиксом 'example_supplier'.
- Определяет пути к файлам настроек и локаторов.

**Примеры**:

```python
# Пример использования метода setUp (вызывается автоматически перед каждым тестом)
test_case = TestSupplier()
test_case.setUp()
print(test_case.supplier_prefix)  # Вывод: test_supplier
```

### `test_init_webdriver`

```python
@patch('mymodule.supplier.gs.j_loads')
@patch('mymodule.supplier.Driver')
def test_init_webdriver(self, mock_driver, mock_j_loads):
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

**Назначение**: Метод `test_init_webdriver` тестирует инициализацию класса `Supplier` с методом парсинга 'web' (webdriver).

**Параметры**:
- `mock_driver` (MagicMock): Имитированный класс `Driver`.
- `mock_j_loads` (MagicMock): Имитированная функция `j_loads`.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Метод использует декораторы `@patch` для имитации функций `j_loads` и класса `Driver`.
- Функция `j_loads` возвращает предопределенные настройки поставщика (`self.supplier_settings`).
- Класс `Driver` возвращает имитированный объект `MagicMock`.
- Создается экземпляр класса `Supplier` с заданными префиксом, языком и методом парсинга.
- Проверяются атрибуты созданного экземпляра `Supplier` на соответствие ожидаемым значениям.
- Утверждается, что функция `j_loads` была вызвана с правильным путем к файлу настроек.
- Утверждается, что класс `Driver` был вызван один раз.

**Примеры**:

```python
# Пример использования метода test_init_webdriver (вызывается автоматически при запуске тестов)
test_case = TestSupplier()
test_case.setUp()
test_case.test_init_webdriver()
```

### `test_init_api`

```python
@patch('mymodule.supplier.gs.j_loads')
def test_init_api(self, mock_j_loads):
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

**Назначение**: Метод `test_init_api` тестирует инициализацию класса `Supplier` с методом парсинга 'api'.

**Параметры**:
- `mock_j_loads` (MagicMock): Имитированная функция `j_loads`.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Метод использует декоратор `@patch` для имитации функции `j_loads`.
- Устанавливает атрибут `self.method` в значение 'api'.
- Функция `j_loads` возвращает предопределенные настройки поставщика (`self.supplier_settings`).
- Создается экземпляр класса `Supplier` с заданными префиксом, языком и методом парсинга.
- Проверяются атрибуты созданного экземпляра `Supplier` на соответствие ожидаемым значениям.
- Утверждается, что функция `j_loads` была вызвана с правильным путем к файлу настроек.

**Примеры**:

```python
# Пример использования метода test_init_api (вызывается автоматически при запуске тестов)
test_case = TestSupplier()
test_case.setUp()
test_case.test_init_api()
```

### `test_supplier_load_settings_success`

```python
def test_supplier_load_settings_success():
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

**Назначение**: Метод `test_supplier_load_settings_success` тестирует успешную загрузку настроек поставщика.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Создается экземпляр класса `Supplier` с префиксом 'dummy'.
- Проверяются атрибуты созданного экземпляра `Supplier` на соответствие значениям по умолчанию.

**Примеры**:

```python
# Пример использования метода test_supplier_load_settings_success (вызывается автоматически при запуске тестов)
test_case = TestSupplier()
test_case.test_supplier_load_settings_success()
```

### `test_supplier_load_settings_failure`

```python
def test_supplier_load_settings_failure():
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

**Назначение**: Метод `test_supplier_load_settings_failure` тестирует неудачную загрузку настроек поставщика.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Создается экземпляр класса `Supplier` с префиксом 'nonexistent'.
- Проверяются атрибуты созданного экземпляра `Supplier` на соответствие значениям по умолчанию в случае отсутствия настроек.

**Примеры**:

```python
# Пример использования метода test_supplier_load_settings_failure (вызывается автоматически при запуске тестов)
test_case = TestSupplier()
test_case.test_supplier_load_settings_failure()
```

### `test_load_settings`

```python
def test_load_settings(supplier, caplog):
    supplier._load_settings()
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

**Назначение**: Метод `test_load_settings` тестирует загрузку настроек.

**Параметры**:
- `supplier` (Supplier): Экземпляр класса `Supplier`.
- `caplog`: Объект для захвата логов.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Вызывается метод `_load_settings` экземпляра класса `Supplier`.
- Проверяются атрибуты экземпляра `Supplier` на соответствие ожидаемым значениям после загрузки настроек.

**Примеры**:

```python
# Пример использования метода test_load_settings (вызывается автоматически при запуске тестов)
test_case = TestSupplier()
test_case.setUp()
test_case.test_load_settings(test_case.supplier, caplog)
```

### `test_load_settings_invalid_path`

```python
def test_load_settings_invalid_path(supplier, caplog):
    supplier._load_settings()
    assert 'Error reading suppliers/example_supplier/example_supplier.json' in caplog.text
```

**Назначение**: Метод `test_load_settings_invalid_path` тестирует загрузку настроек при неверном пути к файлу.

**Параметры**:
- `supplier` (Supplier): Экземпляр класса `Supplier`.
- `caplog`: Объект для захвата логов.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Вызывается метод `_load_settings` экземпляра класса `Supplier`.
- Проверяется наличие сообщения об ошибке в логах, указывающего на неверный путь к файлу настроек.

**Примеры**:

```python
# Пример использования метода test_load_settings_invalid_path (вызывается автоматически при запуске тестов)
test_case = TestSupplier()
test_case.setUp()
test_case.test_load_settings_invalid_path(test_case.supplier, caplog)
```

### `test_load_settings_invalid_locators_path`

```python
def test_load_settings_invalid_locators_path(supplier, caplog):
    supplier.scrapping_method = 'api'
    supplier._load_settings()
    assert 'Error reading suppliers/example_supplier/locators.json' in caplog.text
```

**Назначение**: Метод `test_load_settings_invalid_locators_path` тестирует загрузку настроек при неверном пути к файлу с локаторами.

**Параметры**:
- `supplier` (Supplier): Экземпляр класса `Supplier`.
- `caplog`: Объект для захвата логов.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Устанавливается атрибут `scrapping_method` экземпляра класса `Supplier` в значение 'api'.
- Вызывается метод `_load_settings` экземпляра класса `Supplier`.
- Проверяется наличие сообщения об ошибке в логах, указывающего на неверный путь к файлу локаторов.

**Примеры**:

```python
# Пример использования метода test_load_settings_invalid_locators_path (вызывается автоматически при запуске тестов)
test_case = TestSupplier()
test_case.setUp()
test_case.test_load_settings_invalid_locators_path(test_case.supplier, caplog)
```

### `test_load_settings_api`

```python
def test_load_settings_api(supplier):
    supplier.scrapping_method = 'api'
    assert supplier.locators is None
    assert supplier.driver is None
```

**Назначение**: Метод `test_load_settings_api` тестирует загрузку настроек при методе парсинга 'api'.

**Параметры**:
- `supplier` (Supplier): Экземпляр класса `Supplier`.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Устанавливается атрибут `scrapping_method` экземпляра класса `Supplier` в значение 'api'.
- Проверяется, что атрибуты `locators` и `driver` экземпляра класса `Supplier` равны `None`.

**Примеры**:

```python
# Пример использования метода test_load_settings_api (вызывается автоматически при запуске тестов)
test_case = TestSupplier()
test_case.setUp()
test_case.test_load_settings_api(test_case.supplier)
```

### `test_load_related_functions`

```python
def test_load_related_functions(supplier):
    assert hasattr(supplier, 'related_modules')
    assert hasattr(supplier.related_modules, 'example_function')
```

**Назначение**: Метод `test_load_related_functions` тестирует загрузку связанных функций.

**Параметры**:
- `supplier` (Supplier): Экземпляр класса `Supplier`.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Проверяется наличие атрибута `related_modules` у экземпляра класса `Supplier`.
- Проверяется наличие атрибута `example_function` у атрибута `related_modules` экземпляра класса `Supplier`.

**Примеры**:

```python
# Пример использования метода test_load_related_functions (вызывается автоматически при запуске тестов)
test_case = TestSupplier()
test_case.setUp()
test_case.test_load_related_functions(test_case.supplier)
```

### `test_init`

```python
def test_init(supplier):
    assert supplier.driver is not None
    assert isinstance(supplier.p, list)
    assert isinstance(supplier.c, list)
    assert supplier.current_scenario_filename is None
    assert supplier.current_scenario is None
```

**Назначение**: Метод `test_init` тестирует инициализацию экземпляра класса `Supplier`.

**Параметры**:
- `supplier` (Supplier): Экземпляр класса `Supplier`.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Проверяется, что атрибут `driver` экземпляра класса `Supplier` не равен `None`.
- Проверяется, что атрибуты `p` и `c` экземпляра класса `Supplier` являются списками.
- Проверяется, что атрибуты `current_scenario_filename` и `current_scenario` экземпляра класса `Supplier` равны `None`.

**Примеры**:

```python
# Пример использования метода test_init (вызывается автоматически при запуске тестов)
test_case = TestSupplier()
test_case.setUp()
test_case.test_init(test_case.supplier)
```

### `test_load_settings_success`

```python
def test_load_settings_success(self):
    with patch('builtins.open', return_value=MagicMock(spec=open, read=lambda: json.dumps({'supplier_id': 123}))) as mock_open:
        result = self.supplier._load_settings()
        self.assertTrue(result)
        self.assertEqual(self.supplier.supplier_id, 123)
```

**Назначение**: Метод `test_load_settings_success` тестирует успешную загрузку настроек из файла.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Используется менеджер контекста `with patch` для имитации функции `open`.
- Функция `open` возвращает имитированный объект `MagicMock`, который возвращает JSON-строку с `supplier_id = 123`.
- Вызывается метод `_load_settings` экземпляра класса `Supplier`.
- Проверяется, что метод `_load_settings` вернул `True`.
- Проверяется, что атрибут `supplier_id` экземпляра класса `Supplier` равен 123.

**Примеры**:

```python
# Пример использования метода test_load_settings_success (вызывается автоматически при запуске тестов)
test_case = TestSupplier()
test_case.setUp()
test_case.test_load_settings_success()
```

### `test_load_settings_failure`

```python
def test_load_settings_failure(self):
    with patch('builtins.open', side_effect=Exception):
        result = self.supplier._load_settings()
        self.assertFalse(result)
```

**Назначение**: Метод `test_load_settings_failure` тестирует неудачную загрузку настроек из файла.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Используется менеджер контекста `with patch` для имитации функции `open`.
- Функция `open` вызывает исключение `Exception`.
- Вызывается метод `_load_settings` экземпляра класса `Supplier`.
- Проверяется, что метод `_load_settings` вернул `False`.

**Примеры**:

```python
# Пример использования метода test_load_settings_failure (вызывается автоматически при запуске тестов)
test_case = TestSupplier()
test_case.setUp()
test_case.test_load_settings_failure()
```

### `test_run_api`

```python
def test_run_api(self):
    with patch('my_module.supplier.importlib.import_module') as mock_import:
        mock_module = MagicMock()
        mock_module.run_api.return_value = True
        mock_import.return_value = mock_module
        result = self.supplier.run()
        self.assertTrue(result)
```

**Назначение**: Метод `test_run_api` тестирует запуск поставщика с методом парсинга 'api'.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Используется менеджер контекста `with patch` для имитации функции `importlib.import_module`.
- Функция `importlib.import_module` возвращает имитированный модуль `MagicMock`.
- Метод `run_api` имитированного модуля возвращает `True`.
- Вызывается метод `run` экземпляра класса `Supplier`.
- Проверяется, что метод `run` вернул `True`.

**Примеры**:

```python
# Пример использования метода test_run_api (вызывается автоматически при запуске тестов)
test_case = TestSupplier()
test_case.setUp()
test_case.test_run_api()
```

### `test_run_scenario_files_success`

```python
def test_run_scenario_files_success(self):
    with patch.object(self.supplier, 'login', return_value=True):
        self.supplier._load_settings()
        scenario_file = Path(__file__).parent / 'data/example_supplier/scenario.json'
        result = self.supplier.run_scenario_files(str(scenario_file))
        self.assertTrue(result)
```

**Назначение**: Метод `test_run_scenario_files_success` тестирует успешное выполнение сценария из файла.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Используется менеджер контекста `with patch.object` для имитации метода `login` экземпляра класса `Supplier`.
- Метод `login` возвращает `True`.
- Вызывается метод `_load_settings` экземпляра класса `Supplier`.
- Определяется путь к файлу сценария.
- Вызывается метод `run_scenario_files` экземпляра класса `Supplier` с путем к файлу сценария.
- Проверяется, что метод `run_scenario_files` вернул `True`.

**Примеры**:

```python
# Пример использования метода test_run_scenario_files_success (вызывается автоматически при запуске тестов)
test_case = TestSupplier()
test_case.setUp()
test_case.test_run_scenario_files_success()
```

### `test_run_scenario_files_failure`

```python
def test_run_scenario_files_failure(self):
    with patch.object(self.supplier, 'login', return_value=True):
        self.supplier._load_settings()
        scenario_file = Path(__file__).parent / 'data/example_supplier/invalid_scenario.json'
        result = self.supplier.run_scenario_files(str(scenario_file))
        self.assertFalse(result)
```

**Назначение**: Метод `test_run_scenario_files_failure` тестирует неудачное выполнение сценария из файла.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Используется менеджер контекста `with patch.object` для имитации метода `login` экземпляра класса `Supplier`.
- Метод `login` возвращает `True`.
- Вызывается метод `_load_settings` экземпляра класса `Supplier`.
- Определяется путь к файлу сценария.
- Вызывается метод `run_scenario_files` экземпляра класса `Supplier` с путем к файлу сценария.
- Проверяется, что метод `run_scenario_files` вернул `False`.

**Примеры**:

```python
# Пример использования метода test_run_scenario_files_failure (вызывается автоматически при запуске тестов)
test_case = TestSupplier()
test_case.setUp()
test_case.test_run_scenario_files_failure()
```

### `test_run_with_login`

```python
def test_run_with_login(self):
    with patch.object(self.supplier, 'login', return_value=True) as mock_login:
        self.supplier._load_settings()
        result = self.supplier.run()
        self.assertTrue(mock_login.called)
        self.assertTrue(result)
```

**Назначение**: Метод `test_run_with_login` тестирует запуск поставщика с предварительной авторизацией.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Используется менеджер контекста `with patch.object` для имитации метода `login` экземпляра класса `Supplier`.
- Метод `login` возвращает `True`.
- Вызывается метод `_load_settings` экземпляра класса `Supplier`.
- Вызывается метод `run` экземпляра класса `Supplier`.
- Проверяется, что метод `login` был вызван.
- Проверяется, что метод `run` вернул `True`.

**Примеры**:

```python
# Пример использования метода test_run_with_login (вызывается автоматически при запуске тестов)
test_case = TestSupplier()
test_case.setUp()
test_case.test_run_with_login()
```

### `test_run_without_login`

```python
def test_run_without_login(self):
    self.supplier.login['if_login'] = False
    with patch.object(self.supplier, 'run_scenario_files', return_value=True) as mock_run_scenario_files:
        self.supplier._load_settings()
        result = self.supplier.run()
        self.assertFalse(mock_run_scenario_files.called_with())
        self.assertTrue(result)
```

**Назначение**: Метод `test_run_without_login` тестирует запуск поставщика без авторизации.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Устанавливается значение ключа `if_login` словаря `login` экземпляра класса `Supplier` в `False`.
- Используется менеджер контекста `with patch.object` для имитации метода `run_scenario_files` экземпляра класса `Supplier`.
- Метод `run_scenario_files` возвращает `True`.
- Вызывается метод `_load_settings` экземпляра класса `Supplier`.
- Вызывается метод `run` экземпляра класса `Supplier`.
- Проверяется, что метод `run_scenario_files` не был вызван.
- Проверяется, что метод `run` вернул `True`.

**Примеры**:

```python
# Пример использования метода test_run_without_login (вызывается автоматически при запуске тестов)
test_case = TestSupplier()
test_case.setUp()
test_case.test_run_without_login()