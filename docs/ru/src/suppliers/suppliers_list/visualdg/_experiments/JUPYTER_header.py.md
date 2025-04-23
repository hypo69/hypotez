# src.suppliers.visualdg._experiments.JUPYTER_header

## Обзор

Файл содержит настройки и импорты, необходимые для экспериментов с поставщиком `visualdg` в проекте `hypotez`. Он добавляет корневую директорию проекта в `sys.path`, импортирует необходимые модули и определяет функцию для запуска поставщика.

## Подробней

Этот файл используется для настройки окружения и импорта необходимых модулей для экспериментов, связанных с поставщиком `visualdg`. Он также содержит функцию `start_supplier`, которая создает и возвращает экземпляр класса `Supplier`.

## Импортированные модули

- `sys`: Для работы с системными параметрами и функциями.
- `os`: Для взаимодействия с операционной системой.
- `pathlib.Path`: Для работы с путями к файлам и директориям.
- `json`: Для работы с данными в формате JSON.
- `re`: Для работы с регулярными выражениями.
- `src.webdriver.driver.Driver`: Для управления веб-драйвером.
- `src.product.Product`, `src.product.ProductFields`: Для работы с товарами и их полями.
- `src.category.Category`: Для работы с категориями товаров.
- `src.utils.StringFormatter`, `src.utils.StringNormalizer`: Для форматирования и нормализации строк.
- `src.utils.printer.pprint`: Для красивой печати данных.
- `src.endpoints.PrestaShop.Product`: Для работы с продуктами в PrestaShop.
- `src.endpoints.PrestaShop.save_text_file`: Для сохранения текста в файл.

## Переменные

- `dir_root (Path)`: Корневая директория проекта `hypotez`, определяется на основе текущей рабочей директории.
- `dir_src (Path)`: Директория `src` в корневой директории проекта.

## Функции

### `start_supplier`

```python
def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en'):
    """ Старт поставщика 
    Args:
        supplier_prefix (str, optional): Префикс поставщика. По умолчанию 'aliexpress'.
        locale (str, optional): Локаль. По умолчанию 'en'.
    Returns:
        Supplier: Возвращает экземпляр класса `Supplier`.
    """
    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)
```

**Назначение**: Функция создает и возвращает экземпляр класса `Supplier` с заданными параметрами.

**Параметры**:
- `supplier_prefix` (str, optional): Префикс поставщика. По умолчанию `'aliexpress'`.
- `locale` (str, optional): Локаль. По умолчанию `'en'`.

**Возвращает**:
- `Supplier`: Экземпляр класса `Supplier`, созданный с переданными параметрами.

**Как работает функция**:
1. Определяет словарь `params` с параметрами `supplier_prefix` и `locale`.
2. Создает и возвращает экземпляр класса `Supplier`, используя параметры из словаря `params`.

**Примеры**:

```python
supplier = start_supplier(supplier_prefix='ozon', locale='ru')
# Создает экземпляр класса Supplier с префиксом 'ozon' и локалью 'ru'.

supplier = start_supplier()
# Создает экземпляр класса Supplier с префиксом 'aliexpress' и локалью 'en' (значения по умолчанию).