# Модуль для экспериментов с заголовком notebook_header-Copy1.py

## Обзор

Модуль содержит набор импортов и функцию `start_supplier`. Предназначен для экспериментов и, вероятно, содержит заголовочную информацию для notebook-ов.
Расположен в директории `src/suppliers/hb/_experiments`.

## Подробней

Модуль является частью проекта `hypotez` и предназначен для экспериментов в рамках работы с поставщиками (suppliers). Содержит импорты различных модулей и функцию для запуска поставщика. Расположение файла указывает на то, что он относится к экспериментальной части проекта и, возможно, используется для отладки или тестирования новых функций.

## Импортированные модули

Модуль импортирует следующие модули:

- `sys`: Для работы с системными параметрами и функциями.
- `os`: Для взаимодействия с операционной системой.
- `pathlib.Path`: Для удобной работы с путями к файлам и директориям.
- `json`: Для работы с данными в формате JSON.
- `re`: Для работы с регулярными выражениями.
- `src.gs`: Модуль `gs` из директории `src` проекта `hypotez`.
- `src.webdriver.driver.Driver`, `src.webdriver.driver.executor`: Классы `Driver` и `executor` из модуля `driver` в директории `src.webdriver` проекта `hypotez`.
- `src.suppliers.Supplier`: Класс `Supplier` из модуля `Supplier` в директории `src.suppliers` проекта `hypotez`.
- `src.product.Product`, `src.product.ProductFields`: Классы `Product` и `ProductFields` из модуля `product` в директории `src.product` проекта `hypotez`.
- `src.category.Category`: Класс `Category` из модуля `category` в директории `src.category` проекта `hypotez`.
- `src.utils.StringFormatter`, `src.utils.StringNormalizer`: Классы `StringFormatter` и `StringNormalizer` из модуля `utils` в директории `src.utils` проекта `hypotez`.
- `src.utils.printer.pprint`, `src.utils.printer.save_text_file`: Функции `pprint` и `save_text_file` из модуля `printer` в директории `src.utils` проекта `hypotez`.
- `src.scenario.run_scenarios`: Функция `run_scenarios` из модуля `scenario` в директории `src.scenario` проекта `hypotez`.

## Функция `start_supplier`

### `start_supplier`

```python
def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика на основе переданных параметров.

    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль.

    Returns:
        Supplier | str: Объект поставщика `Supplier` или сообщение об ошибке, если не заданы сценарий и язык.

    Как работает функция:
    - Проверяет, заданы ли параметры `supplier_prefix` и `locale`. Если оба параметра не заданы, возвращает сообщение об ошибке.
    - Создает словарь `params` с переданными параметрами.
    - Инициализирует и возвращает объект `Supplier` с переданными параметрами.

    Примеры:
        >>> start_supplier('hb', 'ru')
        <src.suppliers.Supplier object at 0x...>

        >>> start_supplier('', '')
        'Не задан сценарий и язык'
    """
    if not supplier_prefix and not locale: return "Не задан сценарий и язык"
    
    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)
```