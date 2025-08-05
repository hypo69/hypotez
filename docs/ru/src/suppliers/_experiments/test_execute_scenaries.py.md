# Документация модуля `test_execute_scenaries.py`

## Обзор

Модуль содержит юнит-тесты для проверки функциональности выполнения сценариев, включая запуск сценариев из файлов, запуск отдельных сценариев и извлечение данных со страниц товаров.
Этот файл содержит тесты для следующих функций: `run_scenarios`, `run_scenario_file`, `run_scenario` и `grab_product_page`.

## Подробней

Этот модуль использует библиотеку `unittest` для организации и выполнения тестов. Он также использует `MagicMock` из модуля `unittest.mock` для создания мок-объектов, которые имитируют поведение зависимостей, таких как объекты поставщиков и другие функции.
В тестах проверяется правильность выполнения сценариев в различных условиях, таких как наличие или отсутствие файлов сценариев, различные настройки парсинга (webdriver/api), а также успешное или неуспешное извлечение данных со страниц товаров.

## Классы

### `TestRunListOfScenarioFiles`

**Описание**: Класс содержит юнит-тесты для функции `run_scenarios`, которая отвечает за запуск списка файлов сценариев.

**Методы**:

- `test_with_scenario_files_...ed()`: Тест проверяет, что функция `run_scenarios` корректно обрабатывает список файлов сценариев.
- `test_with_no_scenario_files_...ed()`: Тест проверяет, что функция `run_scenarios` корректно обрабатывает случай, когда список файлов сценариев не предоставлен.

### `TestRunScenarioFile`

**Описание**: Класс содержит юнит-тесты для функции `run_scenario_file`, которая отвечает за запуск сценария из файла.

**Методы**:

- `setUp()`: Функция создает мок-объект `Supplier` с необходимыми атрибутами для тестов.
- `test_run_scenario_file_webdriver()`: Тест проверяет, что функция `run_scenario_file` корректно запускает сценарий из файла с использованием `webdriver`.
- `test_run_scenario_file_api()`: Тест проверяет, что функция `run_scenario_file` корректно запускает сценарий из файла с использованием `api`.
- `test_run_scenario_file_no_scenarios()`: Тест проверяет, что функция `run_scenario_file` корректно обрабатывает случай, когда в файле сценариев нет сценариев.

### `TestGrabProductPage`

**Описание**: Класс содержит юнит-тесты для функции `grab_product_page`, которая отвечает за извлечение данных со страницы товара.

**Методы**:

- `setUp()`: Функция создает мок-объект `Supplier` с необходимыми атрибутами для тестов.
- `test_grab_product_page_succesStringFormatterul()`: Тест проверяет, что функция `grab_product_page` корректно извлекает данные со страницы товара, когда все необходимые данные присутствуют.
- `test_grab_product_page_failure()`: Тест проверяет, что функция `grab_product_page` корректно обрабатывает случай, когда некоторые необходимые данные отсутствуют.

### `TestRunScenario`

**Описание**: Класс содержит юнит-тесты для функции `run_scenario`, которая отвечает за запуск отдельного сценария.

**Методы**:

- `setUp()`: Функция создает мок-объект `Supplier` с необходимыми атрибутами для тестов.
- `tearDown()`: Функция выполняет очистку после каждого теста.
- `test_run_scenario_no_url()`: Тест проверяет, что функция `run_scenario` корректно обрабатывает случай, когда в сценарии не указан URL.
- `test_run_scenario_valid_url()`: Тест проверяет, что функция `run_scenario` корректно запускает сценарий с валидным URL.
- `test_run_scenario_export_empty_list()`: Тест проверяет, что функция `run_scenario` корректно обрабатывает случай, когда список товаров для экспорта пуст.

## Функции

### `run_scenarios`

**Назначение**: Запускает сценарии из списка файлов или из настроек, если список файлов не предоставлен.

**Параметры**:

- `s` (MagicMock): Мок-объект поставщика (Supplier).
- `scenario_files` (Optional[List[str]]): Список файлов сценариев.

**Возвращает**:

- `bool`: `True`, если все сценарии выполнены успешно, `False` в противном случае.

**Как работает функция**:

Функция проверяет, предоставлен ли список файлов сценариев. Если да, то она запускает сценарии из каждого файла. Если нет, то она запускает сценарии, указанные в настройках поставщика.
После выполнения всех сценариев функция обновляет настройки поставщика, сохраняя информацию о последнем запущенном сценарии.

**Примеры**:

```python
# Пример запуска сценариев из списка файлов
s = MagicMock()
scenario_files = ["scenario1.json", "scenario2.json"]
s.settings = {
    'check categories on site': False,
    'scenarios': ["default1.json", "default2.json"]
}

result = run_scenarios(s, scenario_files)
```

```python
# Пример запуска сценариев из настроек
s = MagicMock()
s.settings = {
    'check categories on site': True,
    'scenarios': ["default1.json", "default2.json"]
}

result = run_scenarios(s)
```

### `run_scenario_file`

**Назначение**: Запускает сценарии, описанные в файле сценариев.

**Параметры**:

- `s` (MagicMock): Мок-объект поставщика (Supplier).
- `scenario_file` (str): Имя файла сценариев.

**Возвращает**:

- `bool`: `True`, если все сценарии в файле выполнены успешно, `False` в противном случае.

**Как работает функция**:

Функция загружает сценарии из указанного файла. Затем, в зависимости от настройки `parcing method [webdriver|api]`, она запускает сценарии либо с использованием `webdriver`, либо с использованием `api`.
Если сценарии не найдены, функция логирует ошибку и возвращает `False`.

**Примеры**:

```python
# Пример запуска сценариев из файла с использованием webdriver
s = MagicMock()
s.current_scenario_filename = "test_scenario.json"
s.settings = {
    "parcing method [webdriver|api]": "webdriver"
}
s.dir_export_imagesECTORY_FOR_STORE = "/path/to/images"
s.scenarios = {
    "scenario1": {
        "url": "https://example.com",
        "steps": []
    }
}

run_scenario_file(s, "test_scenario.json")
```

```python
# Пример запуска сценариев из файла с использованием api
s = MagicMock()
s.current_scenario_filename = "test_scenario.json"
s.settings = {
    "parcing method [webdriver|api]": "api"
}
s.dir_export_imagesECTORY_FOR_STORE = "/path/to/images"
s.scenarios = {
    "scenario1": {
        "url": "https://example.com",
        "steps": []
    }
}

run_scenario_file(s, "test_scenario.json")
```

### `grab_product_page`

**Назначение**: Извлекает данные со страницы товара с использованием метода `grab_product_page` объекта поставщика.

**Параметры**:

- `s` (Supplier): Объект поставщика (Supplier).

**Возвращает**:

- `bool`: `True`, если данные успешно извлечены, `False` в противном случае.

**Как работает функция**:

Функция вызывает метод `grab_product_page` объекта поставщика для извлечения данных со страницы товара. Если все необходимые данные (id, price, name) присутствуют, функция добавляет извлеченные данные в список `s.p` и возвращает `True`. В противном случае функция возвращает `False`.

**Примеры**:

```python
# Пример успешного извлечения данных со страницы товара
s = Supplier()
s.grab_product_page = lambda _: {'id': '123', 'price': 19.99, 'name': 'Product Name'}
result = grab_product_page(s)
```

```python
# Пример неуспешного извлечения данных со страницы товара
s = Supplier()
s.grab_product_page = lambda _: {'name': 'Product Name'}
result = grab_product_page(s)
```

### `run_scenario`

**Назначение**: Запускает отдельный сценарий.

**Параметры**:

- `scenario` (dict): Словарь, содержащий информацию о сценарии.

**Возвращает**:

- `bool`: `True`, если сценарий выполнен успешно, `False` в противном случае.

**Как работает функция**:

Функция проверяет наличие URL в сценарии. Если URL отсутствует, функция возвращает `False`. Если URL присутствует, функция получает список товаров в категории, извлекает данные со страницы каждого товара и экспортирует данные в файл.

**Примеры**:

```python
# Пример запуска сценария с валидным URL
scenario = {'name': 'scenario2', 'url': 'https://example.com/products'}
self.supplier.scenarios = {'scenario2': scenario}
self.supplier.get_list_products_in_category = MagicMock(return_value=['https://example.com/products/1', 'https://example.com/products/2'])
self.supplier.grab_product_page = MagicMock(return_value=True)
self.supplier.export_files = MagicMock()
self.assertTrue(self.supplier.run_scenario(scenario))
self.assertEqual(len(self.supplier.p), 2)
self.supplier.export_files.assert_called_once_with(self.supplier, self.supplier.p, 'test_export-1', ['csv'])
```

```python
# Пример запуска сценария без URL
scenario = {'name': 'scenario1', 'url': None}
self.supplier.scenarios = {'scenario1': scenario}
self.supplier.get_list_products_in_category = MagicMock(return_value=[])
self.assertFalse(self.supplier.run_scenario(scenario))
```