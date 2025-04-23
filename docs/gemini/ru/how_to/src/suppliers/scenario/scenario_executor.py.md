### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода содержит функции для выполнения сценариев сбора данных о товарах с веб-сайтов поставщиков. Он включает в себя загрузку сценариев из файлов, навигацию по страницам категорий и товаров, извлечение информации о товарах и сохранение этих данных.

Шаги выполнения
-------------------------
1. **`dump_journal(s, journal: dict) -> None`**:
   - Функция сохраняет данные журнала выполнения сценария в JSON-файл.
   - Аргументы:
     - `s`: Объект поставщика (supplier instance).
     - `journal`: Словарь, содержащий данные журнала.
   - Функция создает файл `[timestamp].json` в директории `s.supplier_abs_path/_journal/`.

2. **`run_scenario_files(s, scenario_files_list: List[Path] | Path) -> bool`**:
   - Функция выполняет сценарии, загруженные из списка файлов.
   - Аргументы:
     - `s`: Объект поставщика.
     - `scenario_files_list`: Список путей к файлам сценариев или путь к одному файлу сценария.
   - Для каждого файла сценария:
     - Вызывает функцию `run_scenario_file` для выполнения сценария.
     - Логирует результаты выполнения сценария.

3. **`run_scenario_file(s, scenario_file: Path) -> bool`**:
   - Функция загружает и выполняет сценарии из указанного файла.
   - Аргументы:
     - `s`: Объект поставщика.
     - `scenario_file`: Путь к файлу сценария.
   - Извлекает сценарии из файла, используя `j_loads`.
   - Вызывает функцию `run_scenario` для каждого сценария.
   - Обрабатывает исключения, возникающие при загрузке или обработке файла сценария.

4. **`run_scenarios(s, scenarios: Optional[List[dict] | dict] = None, _journal=None) -> List | dict | bool`**:
   - Функция выполняет список сценариев (не файлов).
   - Аргументы:
     - `s`: Объект поставщика.
     - `scenarios`: Список словарей, представляющих сценарии, или один словарь. Если не указан, использует `s.current_scenario`.
   - Вызывает функцию `run_scenario` для каждого сценария.

5. **`run_scenario(supplier, scenario: dict, scenario_name: str, _journal=None) -> List | dict | bool`**:
   - Функция выполняет полученный сценарий.
   - Аргументы:
     - `supplier`: Объект поставщика.
     - `scenario`: Словарь, содержащий детали сценария.
     - `scenario_name`: Имя сценария.
   - Функция:
     - Инициализирует URL, указанный в сценарии, используя `d.get_url(scenario['url'])`.
     - Извлекает список товаров в категории, вызывая `s.related_modules.get_list_products_in_category(s)`.
     - Переходит по URL каждого товара в списке и извлекает данные о товаре, вызывая `s.related_modules.grab_product_page(s)` и `s.related_modules.grab_page(s)`.
     - Сохраняет извлеченные данные о товаре.

6. **`insert_grabbed_data_to_prestashop(f: ProductFields, coupon_code: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> bool`**:
   - Функция вставляет данные о товаре в PrestaShop.
   - Аргументы:
     - `f`: `ProductFields` instance, содержащий информацию о товаре.
     - `coupon_code`: Код купона (необязательный).
     - `start_date`: Дата начала акции (необязательная).
     - `end_date`: Дата окончания акции (необязательная).
   - Функция:
     - Вызывает `presta.post_product_data` для отправки данных о товаре в PrestaShop.

Пример использования
-------------------------

```python
from pathlib import Path
from src.suppliers.scenario.scenario_executor import run_scenario_files

# Пример использования run_scenario_files
supplier = ...  # инициализация объекта поставщика
scenario_files = [Path("/path/to/scenario1.json"), Path("/path/to/scenario2.json")]
result = run_scenario_files(supplier, scenario_files)
if result:
    print("Все сценарии выполнены успешно")
else:
    print("Некоторые сценарии не были выполнены")
```
```python
from pathlib import Path
from src.suppliers.scenario.scenario_executor import run_scenario_file

# Пример использования run_scenario_file
supplier = ...  # инициализация объекта поставщика
scenario_file = Path("/path/to/scenario.json")
result = run_scenario_file(supplier, scenario_file)
if result:
    print("Сценарий выполнен успешно")
else:
    print("Сценарий не был выполнен")
```
```python
from src.suppliers.scenario.scenario_executor import run_scenarios

# Пример использования run_scenarios
supplier = ...  # инициализация объекта поставщика
scenarios = [
    {"url": "http://example.com/category1"},
    {"url": "http://example.com/category2"}
]
result = run_scenarios(supplier, scenarios)
print(result)
```
```python
from src.suppliers.scenario.scenario_executor import run_scenario

# Пример использования run_scenario
supplier = ...  # инициализация объекта поставщика
scenario = {"url": "http://example.com/product"}
scenario_name = "product_scraping"
result = run_scenario(supplier, scenario, scenario_name)
print(result)
```

```python
from src.suppliers.scenario.scenario_executor import insert_grabbed_data_to_prestashop
from src.endpoints.prestashop.product_async import ProductFields

# Пример использования insert_grabbed_data_to_prestashop
f = ProductFields(
    product_id="123",
    product_name="Test Product",
    product_category="Test Category",
    product_price="10.00",
    description="Test Description"
)
result = await insert_grabbed_data_to_prestashop(f, coupon_code="SUMMER20", start_date="2024-06-01", end_date="2024-06-30")
if result:
    print("Данные успешно вставлены в PrestaShop")
else:
    print("Не удалось вставить данные в PrestaShop")
```