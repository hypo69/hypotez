# Модуль: Исполнитель сценариев поставщиков (`scenario_executor`)

## Обзор

Модуль `scenario_executor` предназначен для выполнения различных сценариев, связанных с поставщиками. Он позволяет автоматизировать такие задачи, как сбор информации о товарах в определенной категории, по заданным фильтрам или производителям. Модуль предоставляет функциональность для загрузки, обработки и выполнения сценариев, а также логирование процесса выполнения.

## Подробнее

Этот модуль является центральным элементом в процессе автоматизации сбора данных о товарах от поставщиков. Он использует сценарии, определяющие последовательность действий для извлечения информации о товарах, и обеспечивает гибкий механизм для настройки процесса сбора данных.
Модуль включает в себя функции для запуска сценариев из файлов, обработки отдельных сценариев и сохранения результатов выполнения.

## Классы

В данном модуле классы отсутствуют.

## Функции

### `dump_journal`

```python
def dump_journal(s, journal: dict) -> None:
    """
    Сохраняет данные журнала в JSON-файл.

    Args:
        s (object): Объект поставщика.
        journal (dict): Словарь, содержащий данные журнала.

    Returns:
        None

    """
    _journal_file_path = Path(s.supplier_abs_path, '_journal', f"{journal['name']}.json")
    j_dumps(journal, _journal_file_path)
```

**Назначение**: Сохраняет журнал выполнения сценария в формате JSON.

**Параметры**:
- `s` (object): Объект поставщика, содержащий информацию о поставщике.
- `journal` (dict): Словарь с данными журнала, такими как имя сценария и результаты выполнения.

**Возвращает**:
- `None`: Функция ничего не возвращает.

**Как работает функция**:
- Функция формирует путь к файлу журнала на основе абсолютного пути поставщика, добавляя поддиректорию `_journal` и имя файла, основанное на имени журнала.
- Использует функцию `j_dumps` для записи содержимого словаря `journal` в JSON-файл.

**Примеры**:
```python
from pathlib import Path
from typing import Dict

class MockSupplier:
    def __init__(self, supplier_abs_path: Path):
        self.supplier_abs_path = supplier_abs_path

# Создаем моковый объект поставщика
supplier = MockSupplier(Path("/tmp/supplier"))

# Создаем моковый журнал
journal_data: Dict = {"name": "test_scenario", "status": "completed"}

# Вызываем функцию dump_journal
dump_journal(supplier, journal_data)
```

### `run_scenario_files`

```python
def run_scenario_files(s, scenario_files_list: List[Path] | Path) -> bool:
    """
    Выполняет список файлов сценариев.

    Args:
        s (object): Объект поставщика.
        scenario_files_list (List[Path] | Path): Список путей к файлам сценариев или путь к одному файлу.

    Returns:
        bool: True, если все сценарии выполнены успешно, False в противном случае.

    Raises:
        TypeError: Если scenario_files_list не является списком или объектом Path.
    """
    if isinstance(scenario_files_list, Path):
        scenario_files_list = [scenario_files_list]
    elif not isinstance(scenario_files_list, list):
        raise TypeError('scenario_files_list must be a list or a Path object.')
    scenario_files_list = scenario_files_list if scenario_files_list else s.scenario_files

    _journal['scenario_files'] = {}
    for scenario_file in scenario_files_list:
        _journal['scenario_files'][scenario_file.name] = {}
        try:
            if run_scenario_file(s, scenario_file):
                _journal['scenario_files'][scenario_file.name]['message'] = f'{scenario_file} completed successfully!'
                logger.success(f'Scenario {scenario_file} completed successfully!')
            else:
                _journal['scenario_files'][scenario_file.name]['message'] = f'{scenario_file} FAILED!'
                logger.error(f'Scenario {scenario_file} failed to execute!')
        except Exception as ex:
            logger.critical(f'An error occurred while processing {scenario_file}: {ex}')
            _journal['scenario_files'][scenario_file.name]['message'] = f'Error: {ex}'
    return True
```

**Назначение**: Выполняет сценарии, описанные в указанных файлах.

**Параметры**:
- `s` (object): Объект поставщика, содержащий информацию о поставщике и его сценариях.
- `scenario_files_list` (List[Path] | Path): Список объектов `Path`, указывающих на файлы сценариев, которые необходимо выполнить.

**Возвращает**:
- `bool`: Возвращает `True`, если все сценарии были успешно выполнены.

**Вызывает исключения**:
- `TypeError`: Если `scenario_files_list` не является списком или объектом `Path`.

**Как работает функция**:
- Проверяет тип входного параметра `scenario_files_list` и преобразует его в список, если это один объект `Path`.
- Итерируется по списку файлов сценариев.
- Для каждого файла сценария вызывает функцию `run_scenario_file` для выполнения сценария.
- Логирует результаты выполнения сценария, используя `logger.success` и `logger.error`.
- В случае возникновения исключения логирует критическую ошибку с использованием `logger.critical`.
- Обновляет глобальный журнал `_journal` информацией о выполнении каждого сценария.

**Примеры**:
```python
from pathlib import Path
from typing import List

class MockSupplier:
    def __init__(self, scenario_files: List[Path]):
        self.scenario_files = scenario_files
        self.supplier_abs_path = Path("/tmp/supplier")

# Создаем моковый объект поставщика
supplier = MockSupplier([Path("scenario1.json"), Path("scenario2.json")])

# Создаем список моковых файлов сценариев
scenario_files_list: List[Path] = [Path("scenario1.json"), Path("scenario2.json")]

# Вызываем функцию run_scenario_files
result: bool = run_scenario_files(supplier, scenario_files_list)
```

### `run_scenario_file`

```python
def run_scenario_file(s, scenario_file: Path) -> bool:
    """
    Загружает и выполняет сценарии из файла.

    Args:
        s (object): Объект поставщика.
        scenario_file (Path): Путь к файлу сценария.

    Returns:
        bool: True, если сценарий выполнен успешно, False в противном случае.
    """
    try:
        scenarios_dict = j_loads(scenario_file)['scenarios']
        for scenario_name, scenario in scenarios_dict.items():
            s.current_scenario = scenario
            if run_scenario(s, scenario, scenario_name):
                logger.success(f'Scenario {scenario_name} completed successfully!')
            else:
                logger.error(f'Scenario {scenario_name} failed to execute!')
        return True
    except (FileNotFoundError, json.JSONDecodeError) as ex:
        logger.critical(f'Error loading or processing scenario file {scenario_file}: {ex}')
        return False
```

**Назначение**: Загружает сценарии из указанного файла и выполняет их.

**Параметры**:
- `s` (object): Объект поставщика, содержащий необходимую информацию для выполнения сценария.
- `scenario_file` (Path): Объект `Path`, представляющий путь к файлу, содержащему сценарии.

**Возвращает**:
- `bool`: `True`, если все сценарии из файла были успешно выполнены, `False` в случае ошибки.

**Как работает функция**:
- Пытается загрузить сценарии из файла, используя функцию `j_loads`. Ожидается, что файл содержит JSON-структуру со списком сценариев под ключом `'scenarios'`.
- Перебирает сценарии в загруженном словаре.
- Для каждого сценария вызывает функцию `run_scenario` для выполнения сценария.
- Логирует результаты выполнения каждого сценария, используя `logger.success` и `logger.error`.
- В случае возникновения исключений `FileNotFoundError` или `json.JSONDecodeError` логирует критическую ошибку с использованием `logger.critical`.

**Примеры**:
```python
from pathlib import Path

class MockSupplier:
    def __init__(self):
        self.current_scenario = None
        self.supplier_abs_path = Path("/tmp/supplier")

# Создаем моковый объект поставщика
supplier = MockSupplier()

# Создаем моковый файл сценария
scenario_file: Path = Path("scenario.json")

# Вызываем функцию run_scenario_file
result: bool = run_scenario_file(supplier, scenario_file)
```

### `run_scenarios`

```python
def run_scenarios(s, scenarios: Optional[List[dict] | dict] = None, _journal=None) -> List | dict | bool:
    """
    Выполняет список сценариев (НЕ ФАЙЛОВ).

    Args:
        s (object): Объект поставщика.
        scenarios (Optional[List[dict] | dict], optional): Список сценариев или один сценарий в виде словаря. Defaults to None.

    Returns:
        List | dict | bool: Результат выполнения сценариев или False в случае ошибки.

    Todo:
        Check the option when no scenarios are specified from all sides. For example, when s.current_scenario is not specified and scenarios are not specified.
    """
    if not scenarios:
        scenarios = [s.current_scenario]

    scenarios = scenarios if isinstance(scenarios, list) else [scenarios]
    res = []
    for scenario in scenarios:
        res = run_scenario(s, scenario)
        _journal['scenario_files'][-1][scenario] = str(res)
        dump_journal(s, _journal)
    return res
```

**Назначение**: Выполняет предоставленные сценарии (не файлы).

**Параметры**:
- `s` (object): Объект поставщика.
- `scenarios` (Optional[List[dict]  |  dict], optional): Список сценариев или один сценарий в виде словаря. По умолчанию `None`.
- `_journal` (Optional[dict], optional): Журнал выполнения. По умолчанию `None`.

**Возвращает**:
- `List | dict | bool`: Результат выполнения сценариев. Возвращает список, словарь или `False` в случае ошибки.

**Как работает функция**:
- Если `scenarios` не предоставлены, использует `s.current_scenario` в качестве сценария для выполнения.
- Преобразует входные `scenarios` в список, если они предоставлены в виде словаря.
- Выполняет каждый сценарий из списка, вызывая функцию `run_scenario`.
- Обновляет журнал `_journal` результатом выполнения каждого сценария.
- Сохраняет журнал с помощью функции `dump_journal`.

**Примеры**:
```python
from typing import List, Dict, Optional

class MockSupplier:
    def __init__(self):
        self.current_scenario = {"name": "default_scenario"}
        self.supplier_abs_path = Path("/tmp/supplier")

# Создаем моковый объект поставщика
supplier = MockSupplier()

# Создаем список моковых сценариев
scenarios_list: List[Dict] = [{"name": "scenario1"}, {"name": "scenario2"}]

# Вызываем функцию run_scenarios
result = run_scenarios(supplier, scenarios_list)
```

### `run_scenario`

```python
def run_scenario(supplier, scenario: dict, scenario_name: str, _journal=None) -> List | dict | bool:
    """
    Выполняет полученный сценарий.

    Args:
        supplier (object): Объект поставщика.
        scenario (dict): Словарь, содержащий детали сценария.
        scenario_name (str): Имя сценария.

    Returns:
        List | dict | bool: Результат выполнения сценария.

    Todo:
        Check the need for the scenario_name parameter.
    """
    s = supplier
    logger.info(f'Starting scenario: {scenario_name}')
    s.current_scenario = scenario
    d = s.driver
    d.get_url(scenario['url'])

    # Get list of products in the category
    list_products_in_category: list = s.related_modules.get_list_products_in_category(s)

    # No products in the category (or they haven't loaded yet)
    if not list_products_in_category:
        logger.warning('No product list collected from the category page. Possibly an empty category - ', d.current_url)
        return False

    for url in list_products_in_category:
        if not d.get_url(url):
            logger.error(f'Error navigating to product page at: {url}')
            continue  # <- Error navigating to the page. Skip

        # Grab product page fields
        grabbed_fields = s.related_modules.grab_product_page(s)
        f: ProductFields = asyncio.run(s.related_modules.grab_page(s))
        if not f:
            logger.error('Failed to collect product fields')
            continue

        presta_fields_dict, assist_fields_dict = f.presta_fields_dict, f.assist_fields_dict
        try:
            product: Product = Product(supplier_prefix=s.supplier_prefix, presta_fields_dict=presta_fields_dict)
            insert_grabbed_data(f)
        except Exception as ex:
            logger.error(f'Product {product.fields["name"][1]} could not be saved', ex)
            continue

    return list_products_in_category
```

**Назначение**: Выполняет переданный сценарий.

**Параметры**:
- `supplier` (object): Объект поставщика, содержащий информацию о поставщике и необходимые методы для выполнения сценария.
- `scenario` (dict): Словарь, содержащий детали сценария, такие как URL для посещения.
- `scenario_name` (str): Имя выполняемого сценария.
- `_journal` (Optional[dict], optional): Журнал выполнения. По умолчанию `None`.

**Возвращает**:
- `List | dict | bool`: Результат выполнения сценария. В данном случае, возвращает список URL товаров, собранных в ходе выполнения сценария, или `False`, если не удалось собрать список товаров.

**Как работает функция**:
1. Инициализирует объект поставщика `s` и логирует начало выполнения сценария с использованием `logger.info`.
2. Устанавливает текущий сценарий поставщика равным переданному сценарию.
3. Извлекает объект драйвера `d` из объекта поставщика `s` и использует его для перехода по URL, указанному в сценарии.
4. Получает список товаров в категории, используя метод `get_list_products_in_category` из `s.related_modules`.
5. Если список товаров пуст, логирует предупреждение и возвращает `False`.
6. Перебирает URL товаров в списке и выполняет следующие действия для каждого URL:
   - Переходит по URL, используя метод `d.get_url`. Если переход не удался, логирует ошибку и переходит к следующему URL.
   - Собирает поля страницы товара, используя метод `s.related_modules.grab_page(s)`. Если не удалось собрать поля, логирует ошибку и переходит к следующему URL.
   - Извлекает словари `presta_fields_dict` и `assist_fields_dict` из объекта `f`.
   - Создает объект `Product` с использованием префикса поставщика и словаря `presta_fields_dict`.
   - Пытается вставить собранные данные, используя функцию `insert_grabbed_data(f)`. Если вставка не удалась, логирует ошибку и переходит к следующему URL.
7. Возвращает список URL товаров, собранных в ходе выполнения сценария.

**Примеры**:
```python
import asyncio
from typing import List, Dict
from pathlib import Path

class MockDriver:
    def get_url(self, url: str) -> bool:
        """Моковый метод для перехода по URL."""
        print(f"Переход по URL: {url}")
        return True

class MockRelatedModules:
    def get_list_products_in_category(self, s) -> List[str]:
        """Моковый метод для получения списка товаров в категории."""
        print("Получение списка товаров в категории")
        return ["http://example.com/product1", "http://example.com/product2"]

    async def grab_page(self, s):
        """Моковый метод для сбора информации о товаре."""
        print("Сбор информации о товаре")
        return True

class MockSupplier:
    def __init__(self):
        self.driver = MockDriver()
        self.related_modules = MockRelatedModules()
        self.supplier_prefix = "mock"
        self.supplier_abs_path = Path("/tmp/supplier")

# Создаем моковый объект поставщика
supplier = MockSupplier()

# Создаем моковый сценарий
scenario: Dict = {"url": "http://example.com/category"}

# Вызываем функцию run_scenario
result = run_scenario(supplier, scenario, "test_scenario")
```

### `insert_grabbed_data_to_prestashop`

```python
async def insert_grabbed_data_to_prestashop(
    f: ProductFields, coupon_code: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None
) -> bool:
    """
    Вставляет продукт в PrestaShop.

    Args:
        f (ProductFields): Экземпляр ProductFields, содержащий информацию о продукте.
        coupon_code (Optional[str], optional): Код купона. Defaults to None.
        start_date (Optional[str], optional): Дата начала акции. Defaults to None.
        end_date (Optional[str], optional): Дата окончания акции. Defaults to None.

    Returns:
        bool: True, если вставка прошла успешно, False в противном случае.
    """
    try:
        presta = PrestaShop()
        return await presta.post_product_data(
            product_id=f.product_id,
            product_name=f.product_name,
            product_category=f.product_category,
            product_price=f.product_price,
            description=f.description,
            coupon_code=coupon_code,
            start_date=start_date,
            end_date=end_date,
        )

    except Exception as ex:
        logger.error('Failed to insert product data into PrestaShop: ', ex)
        return False
```

**Назначение**: Функция для вставки данных о товаре в PrestaShop.

**Параметры**:
- `f` (ProductFields): Экземпляр класса `ProductFields`, содержащий информацию о товаре, который нужно вставить.
- `coupon_code` (Optional[str], optional): Опциональный код купона для товара. По умолчанию `None`.
- `start_date` (Optional[str], optional): Опциональная дата начала действия купона. По умолчанию `None`.
- `end_date` (Optional[str], optional): Опциональная дата окончания действия купона. По умолчанию `None`.

**Возвращает**:
- `bool`: Возвращает `True`, если данные успешно вставлены в PrestaShop, и `False` в случае неудачи.

**Как работает функция**:
- Создает экземпляр класса `PrestaShop`.
- Вызывает асинхронный метод `post_product_data` для отправки данных о товаре в PrestaShop.
- Передает все необходимые параметры, такие как `product_id`, `product_name`, `product_category`, `product_price`, `description`, `coupon_code`, `start_date` и `end_date`.
- В случае возникновения исключения при вставке данных, логирует ошибку с помощью `logger.error` и возвращает `False`.

**Примеры**:
```python
import asyncio
from typing import Optional

class MockProductFields:
    def __init__(self):
        self.product_id = "123"
        self.product_name = "Test Product"
        self.product_category = "Test Category"
        self.product_price = "100"
        self.description = "Test Description"

class MockPrestaShop:
    async def post_product_data(self, product_id, product_name, product_category,
                               product_price, description, coupon_code, start_date, end_date):
        """Моковый метод для вставки данных о товаре."""
        print("Вставка данных о товаре в PrestaShop")
        return True

# Создаем моковый объект ProductFields
product_fields = MockProductFields()

# Вызываем функцию insert_grabbed_data_to_prestashop
result = asyncio.run(insert_grabbed_data_to_prestashop(product_fields, coupon_code="TEST10",
                                                       start_date="2024-01-01", end_date="2024-01-31"))