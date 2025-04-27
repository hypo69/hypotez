## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Блок кода настраивает среду выполнения для работы с поставщиками, задавая путь к корневому каталогу проекта, импортируя необходимые модули и определяя функцию `start_supplier`.

Шаги выполнения
-------------------------
1. Определяет корневой каталог проекта (`dir_root`) и добавляет его в системный путь (`sys.path`).
2. Импортирует необходимые модули из проекта `hypotez`, включая:
    - `Driver` из `src.webdriver.driver`: для работы с браузером.
    - `Product`, `ProductFields` из `src.product`: для работы с продуктами.
    - `Category` из `src.category`: для работы с категориями.
    - `StringFormatter`, `StringNormalizer` из `src.utils`: для работы со строками.
    - `pprint` из `src.utils.printer`: для вывода информации.
    - `Product` из `src.endpoints.PrestaShop`: для работы с продуктами PrestaShop.
    - `save_text_file` из `src.utils`: для сохранения текста в файл.
3. Определяет функцию `start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en' )`, которая:
    - Принимает префикс поставщика (`supplier_prefix`) и язык (`locale`) в качестве аргументов.
    - Создает словарь `params` с данными о поставщике.
    - Возвращает объект `Supplier` с заданными параметрами.

Пример использования
-------------------------

```python
from src.suppliers.ivory._experiments.JUPYTER_header import start_supplier

# Запуск поставщика AliExpress на английском языке
supplier = start_supplier(supplier_prefix='aliexpress', locale='en')

# Вывод информации о поставщике
print(supplier)
```