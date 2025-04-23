## Как использовать модуль управления категориями Aliexpress
=========================================================================================

Описание
-------------------------
Этот модуль предназначен для управления категориями товаров на платформе AliExpress. Он предоставляет инструменты для извлечения URL товаров, синхронизации категорий и взаимодействия с базой данных для управления данными о категориях.

Шаги выполнения
-------------------------
1. **Извлечение URL товаров**:
   - Функция `get_list_products_in_category(s: Supplier) -> list[str, str]` извлекает список URL товаров из указанной категории, учитывая пагинацию. Функция принимает экземпляр класса `Supplier`, содержащий драйвер браузера и локаторы элементов страницы.
   - Функция `get_prod_urls_from_pagination(s: Supplier) -> list[str]` выполняет получение URL товаров с категорийных страниц, обрабатывая пагинацию. Функция принимает экземпляр класса `Supplier`, содержащий драйвер браузера и локаторы элементов страницы.
2. **Синхронизация категорий**:
   - Функция `update_categories_in_scenario_file(s: Supplier, scenario_filename: str) -> bool` сравнивает категории на сайте с категориями, указанными в файле сценария, и обновляет файл, если обнаружены изменения. Функция принимает экземпляр класса `Supplier` и имя файла сценария (`scenario_filename`).
   - Функция `get_list_categories_from_site(s: Supplier, scenario_file: str, brand: str = '') -> list` извлекает список категорий с сайта AliExpress на основе данных из файла сценария. Функция принимает экземпляр класса `Supplier`, имя файла сценария (`scenario_file`) и, опционально, бренд (`brand`).
3. **Взаимодействие с базой данных**:
   - Класс `DBAdaptor` предоставляет методы для взаимодействия с базой данных, включая выборку (`select`), вставку (`insert`), обновление (`update`) и удаление (`delete`) записей в таблице `AliexpressCategory`.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.category import get_list_products_in_category, update_categories_in_scenario_file
from src.suppliers.supplier import Supplier  # Предполагается, что класс Supplier находится в этом модуле

# Создание экземпляра класса Supplier (требуется инициализация драйвера и локаторов)
supplier_instance = Supplier()

# Извлечение URL товаров из категории
category_urls = get_list_products_in_category(supplier_instance)
if category_urls:
    print(f"Обнаружено {len(category_urls)} URL товаров.")
else:
    print("Не удалось получить URL товаров из категории.")

# Обновление категорий в файле сценария
scenario_file = 'example_scenario.json'
update_result = update_categories_in_scenario_file(supplier_instance, scenario_file)
if update_result:
    print(f"Файл сценария '{scenario_file}' успешно обновлен.")
else:
    print(f"Не удалось обновить файл сценария '{scenario_file}'.")