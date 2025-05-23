# Документация для модуля `_experiments`

## Обзор

Модуль содержит эксперименты, связанные с поставщиком Etzmaleh. В нём выполняются различные тестовые сценарии и отладочные действия.

## Подробней

Этот модуль предназначен для проведения экспериментов и отладки кода, связанного с поставщиком Etzmaleh. Он включает в себя импорты различных библиотек и модулей, используемых в проекте, а также содержит функцию для запуска поставщика. Расположение модуля указывает на его использование в экспериментальных целях, а не в основной логике проекта.

## Импортированные модули

- `sys`: Используется для работы с системными параметрами и функциями.
- `os`: Используется для взаимодействия с операционной системой.
- `pathlib.Path`: Используется для работы с путями к файлам и директориям.
- `json`: Используется для работы с данными в формате JSON.
- `re`: Используется для работы с регулярными выражениями.
- `src.webdriver.driver.Driver`: Используется для управления веб-драйвером.
- `src.product.Product, ProductFields`: Используется для работы с товарами и их полями.
- `src.category.Category`: Используется для работы с категориями товаров.
- `src.utils.StringFormatter, StringNormalizer`: Используется для форматирования и нормализации строк.
- `src.utils.printer.pprint`: Используется для "красивой" печати данных.
- `src.endpoints.PrestaShop.Product`: Используется для взаимодействия с PrestaShop.

## Переменные модуля

- `dir_root (Path)`: Определяет корневую директорию проекта ("hypotez") и добавляет её в `sys.path`.
- `dir_src (Path)`: Определяет директорию `src` внутри корневой директории.

## Функции

### `start_supplier`

```python
def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en') -> Supplier:
    """ Старт поставщика 
    Args:
        supplier_prefix (str, optional): Префикс поставщика. По умолчанию 'aliexpress'.
        locale (str, optional): Локаль. По умолчанию 'en'.

    Returns:
        Supplier: Объект поставщика.
    """
```

**Назначение**: Функция для запуска поставщика.

**Параметры**:

- `supplier_prefix` (str, optional): Префикс поставщика. По умолчанию `'aliexpress'`.
- `locale` (str, optional): Локаль. По умолчанию `'en'`.

**Возвращает**:

- `Supplier`: Объект поставщика.

**Как работает функция**:

- Создает словарь `params` с параметрами поставщика (`supplier_prefix` и `locale`).
- Создает и возвращает экземпляр класса `Supplier`, передавая в него словарь `params`.

**Примеры**:

```python
# Пример вызова функции start_supplier
supplier = start_supplier(supplier_prefix='my_supplier', locale='ru')
```
```python
# Пример вызова функции start_supplier с параметрами по умолчанию
supplier = start_supplier()