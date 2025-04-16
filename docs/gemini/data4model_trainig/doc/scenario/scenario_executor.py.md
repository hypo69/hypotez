# Модуль `scenario_executor`

## Обзор

Модуль предназначен для исполнения сценариев работы с поставщиками. Он обеспечивает автоматизацию взаимодействия с веб-сайтами поставщиков, извлечение информации о товарах и добавление ее в PrestaShop.

## Подробней

Модуль предоставляет набор функций, позволяющих загружать и выполнять различные сценарии работы с поставщиками, такие как сбор товаров в определенной категории или по заданному фильтру. Он включает в себя чтение файлов сценариев, извлечение данных с веб-сайтов, обработку данных и их интеграцию с PrestaShop.

## Основные функции

### `dump_journal(s, journal: dict) -> None`

```python
def dump_journal(s, journal: dict) -> None:
    """!
    Save the journal data to a JSON file.

    Args:
        s (object): Supplier instance.
        journal (dict): Dictionary containing the journal data.

    Returns:
        None
    """
    ...
```

**Назначение**: Сохраняет данные журнала в JSON-файл.

**Параметры**:

*   `s` (object): Экземпляр поставщика.
*   `journal` (dict): Словарь, содержащий данные журнала.

**Как работает функция**:

1.  Формирует путь к файлу журнала на основе пути поставщика и имени журнала.
2.  Сохраняет словарь журнала в JSON-файл.

### `run_scenario_files(s, scenario_files_list: List[Path] | Path) -> bool`

```python
def run_scenario_files(s, scenario_files_list: List[Path] | Path) -> bool:
    """!
    Executes a list of scenario files.

    Args:
        s (object): Supplier instance.
        scenario_files_list (List[Path] | Path): List of file paths for scenario files, or a single file path.

    Returns:
        bool: True if all scenarios were executed successfully, False otherwise.

    Raises:
        TypeError: If scenario_files_list is not a list or a Path object.
    """
    ...
```

**Назначение**: Выполняет список файлов сценариев.

**Параметры**:

*   `s` (object): Экземпляр поставщика.
*   `scenario_files_list` (List[Path] | Path): Список путей к файлам сценариев или путь к одному файлу.

**Возвращает**:

*   `bool`: `True`, если все сценарии были выполнены успешно, иначе `False`.

**Вызывает исключения**:

*   `TypeError`: Если `scenario_files_list` не является списком или объектом `Path`.

**Как работает функция**:

1.  Проверяет тип `scenario_files_list` и преобразует в список, если это необходимо.
2.  Итерируется по списку файлов сценариев.
3.  Для каждого файла вызывает функцию `run_scenario_file` для выполнения сценария.
4.  Записывает результаты выполнения в журнал.

### `run_scenario_file(s, scenario_file: Path) -> bool`

```python
def run_scenario_file(s, scenario_file: Path) -> bool:
    """!
    Loads and executes scenarios from a file.

    Args:
        s (object): Supplier instance.
        scenario_file (Path): Path to the scenario file.

    Returns:
        bool: True if the scenario was executed successfully, False otherwise.
    """
    ...
```

**Назначение**: Загружает и выполняет сценарии из файла.

**Параметры**:

*   `s` (object): Экземпляр поставщика.
*   `scenario_file` (Path): Путь к файлу сценария.

**Возвращает**:

*   `bool`: `True`, если сценарий был выполнен успешно, иначе `False`.

**Как работает функция**:

1.  Загружает сценарии из JSON-файла.
2.  Итерируется по сценариям в файле.
3.  Для каждого сценария вызывает функцию `run_scenario` для его выполнения.

### `run_scenarios(s, scenarios: Optional[List[dict] | dict] = None, _journal=None) -> List | dict | bool`

```python
def run_scenarios(s, scenarios: Optional[List[dict] | dict] = None, _journal=None) -> List | dict | bool:
    """!
    Executes a list of scenarios (NOT FILES).

    Args:
        s (object): Supplier instance.
        scenarios (Optional[List[dict] | dict], optional): Accepts a list of scenarios or a single scenario as a dictionary. Defaults to None.

    Returns:
        List | dict | bool: The result of executing the scenarios, or False in case of an error.

    Todo:
        Check the option when no scenarios are specified from all sides. For example, when s.current_scenario is not specified and scenarios are not specified.
    """
    ...
```

**Назначение**: Выполняет список сценариев (не файлов).

**Параметры**:

*   `s` (object): Экземпляр поставщика.
*   `scenarios` (Optional[List[dict] | dict]): Список сценариев или один сценарий в виде словаря.

**Возвращает**:

*   `List | dict | bool`: Результат выполнения сценариев или `False` в случае ошибки.

**Как работает функция**:

1.  Проверяет, предоставлены ли сценарии, и использует `s.current_scenario`, если они не предоставлены.
2.  Преобразует входные данные в список сценариев.
3.  Итерируется по списку сценариев и выполняет каждый сценарий с помощью функции `run_scenario`.
4.  Записывает результаты выполнения в журнал.

### `run_scenario(supplier, scenario: dict, scenario_name: str, _journal=None) -> List | dict | bool`

```python
def run_scenario(supplier, scenario: dict, scenario_name: str, _journal=None) -> List | dict | bool:
    """!
    Executes the received scenario.

    Args:
        supplier (object): Supplier instance.
        scenario (dict): Dictionary containing scenario details.
        scenario_name (str): Name of the scenario.

    Returns:
        List | dict | bool: The result of executing the scenario.

    Todo:
        Check the need for the scenario_name parameter.
    """
    ...
```

**Назначение**: Выполняет полученный сценарий.

**Параметры**:

*   `supplier` (object): Экземпляр поставщика.
*   `scenario` (dict): Словарь, содержащий детали сценария.
*   `scenario_name` (str): Имя сценария.

**Возвращает**:

*   `List | dict | bool`: Результат выполнения сценария.

**Как работает функция**:

1.  Инициализирует экземпляр поставщика.
2.  Получает URL из сценария и переходит по нему.
3.  Получает список товаров в категории с помощью функции `s.related_modules.get_list_products_in_category(s)`.
4.  Для каждого URL в списке товаров:
    *   Переходит на страницу товара.
    *   Получает поля товара с помощью `s.related_modules.grab_product_page(s)`.
    *   Создает объект `Product` и вставляет полученные данные.

### `insert_grabbed_data_to_prestashop(f: ProductFields, coupon_code: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> bool`

```python
async def insert_grabbed_data_to_prestashop(
    f: ProductFields, coupon_code: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None
) -> bool:
    """!
    Inserts the product into PrestaShop.

    Args:
        f (ProductFields): ProductFields instance containing the product information.
        coupon_code (Optional[str], optional): Optional coupon code. Defaults to None.
        start_date (Optional[str], optional): Optional start date for the promotion. Defaults to None.
        end_date (Optional[str], optional): Optional end date for the promotion. Defaults to None.

    Returns:
        bool: True if the insertion was successful, False otherwise.
    """
    ...
```

**Назначение**: Вставляет данные о товаре в PrestaShop.

**Параметры**:

*   `f` (ProductFields): Экземпляр ProductFields, содержащий информацию о товаре.
*   `coupon_code` (Optional[str], optional): Код купона (по умолчанию `None`).
*   `start_date` (Optional[str], optional): Дата начала акции (по умолчанию `None`).
*   `end_date` (Optional[str], optional): Дата окончания акции (по умолчанию `None`).

**Возвращает**:

*   `bool`: `True`, если вставка прошла успешно, иначе `False`.

**Как работает функция**:

1.  Инициализирует класс `PrestaShop()`.
2.  Вызывает функцию `presta.post_product_data()` для вставки товара в PrestaShop.

## Зависимости

*   `requests`: Для выполнения HTTP запросов.
*   `asyncio`: Для асинхронных операций.
*   `pathlib`: Для работы с путями к файлам.
*   `typing`: Для аннотаций типов.
*   `src.endpoints.prestashop.product_async`: Для асинхронного взаимодействия с PrestaShop API.
*   `src.logger.logger`: Для логирования информации о процессе выполнения скрипта.
*   `src.endpoints.prestashop.db`: Для работы с базой данных PrestaShop.
*   `src.webdriver.driver`: Для управления веб-драйвером.
*   `src.webdriver.firefox`: Для использования Firefox в качестве веб-драйвера.
*   `src.webdriver.playwright`: Для использования Playwright в качестве веб-драйвера.
*   `src.suppliers.get_graber_by_supplier`: Для получения грабера на основе URL поставщика.
*   `src.endpoints.fetch_one_tab`: Для извлечения URL из OneTab.
*   `src.utils.jjson`: Для работы с JSON-файлами.

## Замечания

Модуль предназначен для автоматизации взаимодействия с поставщиками и имеет сложную структуру.
Перед использованием модуля необходимо настроить параметры подключения к PrestaShop и веб-драйверу. Обратите внимание на обработки ошибок, которые могут возникнуть в процессе выполнения сценария. В коде есть TODO - проверить параметр scenario_name в функции run_scenario.
```python
...
```
Данный код указывает на то, что в модуле есть еще не реализованная функциональность.