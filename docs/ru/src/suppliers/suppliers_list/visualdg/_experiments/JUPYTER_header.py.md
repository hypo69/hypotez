# src.suppliers.visualdg.\_experiments.JUPYTER_header

## Обзор

Модуль содержит набор импортов и вспомогательных функций для экспериментов, связанных с поставщиками данных, в частности, для `visualdg`. Он настраивает пути для импорта, импортирует необходимые модули и определяет функцию для запуска поставщика.

## Подробней

Модуль предназначен для использования в Jupyter Notebook или других интерактивных средах для тестирования и экспериментов с кодом, связанным с поставщиками. Он включает в себя настройку путей к директориям проекта, импорт необходимых модулей и определение функции `start_supplier` для запуска поставщика с заданными параметрами.

## Импортированные модули

В данном модуле импортируются следующие модули:

- `sys`: Для работы с системными параметрами и функциями.
- `os`: Для работы с операционной системой.
- `pathlib.Path`: Для удобной работы с путями к файлам и директориям.
- `json`: Для работы с JSON-данными.
- `re`: Для работы с регулярными выражениями.
- `src.webdriver.driver.Driver`: Для управления веб-драйвером.
- `src.product.Product`: Для работы с товарами.
- `src.product.ProductFields`: Для работы с полями товаров.
- `src.category.Category`: Для работы с категориями товаров.
- `src.utils.StringFormatter`: Для форматирования строк.
- `src.utils.StringNormalizer`: Для нормализации строк.
- `src.utils.printer.pprint`: Для "красивой" печати данных.
- `src.endpoints.PrestaShop.Product`: Для работы с товарами в PrestaShop.
- `src.endpoints.PrestaShop.save_text_file`: Для сохранения текстовых файлов.

## Функции

### `start_supplier`

```python
def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en' ) -> Supplier:
    """
    Старт поставщика

    Args:
        supplier_prefix (str, optional): Префикс поставщика. По умолчанию 'aliexpress'.
        locale (str, optional): Локаль. По умолчанию 'en'.

    Returns:
        Supplier: Объект поставщика.

    """
    params: dict = \
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)
```

**Назначение**: Запускает поставщика с заданными параметрами.

**Параметры**:
- `supplier_prefix` (str, optional): Префикс поставщика. По умолчанию `'aliexpress'`.
- `locale` (str, optional): Локаль. По умолчанию `'en'`.

**Возвращает**:
- `Supplier`: Объект поставщика.

**Как работает функция**:
Функция создает словарь `params` с префиксом поставщика и локалью, затем возвращает объект `Supplier`, инициализированный с этими параметрами. Функция предполагает, что класс `Supplier` определен в другом месте и доступен для импорта.

**Примеры**:

```python
supplier = start_supplier(supplier_prefix='aliexpress', locale='ru')
# Запускает поставщика AliExpress с русской локалью

supplier = start_supplier()
# Запускает поставщика AliExpress с английской локалью (параметры по умолчанию)