# src.suppliers.ebay.\_experiments.JUPYTER_header

## Обзор

Модуль содержит набор экспериментов и вспомогательных функций для работы с поставщиком eBay. Он включает импорт необходимых библиотек, настройку путей и функций для запуска поставщика.

## Подробнее

Модуль предназначен для экспериментов, связанных с парсингом и обработкой данных с eBay. Он настраивает пути к корневой директории проекта, импортирует необходимые модули и содержит функцию для запуска поставщика.

## Параметры модуля

- `dir_root` (Path): Корневая директория проекта `hypotez`.
- `dir_src` (Path): Директория `src` внутри корневой директории.

## Подключаемые модули

- `sys`: Используется для работы с системными параметрами и функциями.
- `os`: Используется для работы с операционной системой, например, для получения текущей директории.
- `pathlib.Path`: Используется для работы с путями к файлам и директориям.
- `json`: Используется для работы с данными в формате JSON.
- `re`: Используется для работы с регулярными выражениями.
- `src.webdriver.driver.Driver`: Класс для управления веб-драйвером.
- `src.product.Product`: Класс, представляющий товар.
- `src.product.ProductFields`: Класс, представляющий поля товара.
- `src.category.Category`: Класс, представляющий категорию товара.
- `src.utils.StringFormatter`: Класс для форматирования строк.
- `src.utils.StringNormalizer`: Класс для нормализации строк.
- `src.utils.printer.pprint`: Функция для красивой печати данных.
- `src.endpoints.PrestaShop.Product`: Класс для работы с товарами в PrestaShop.
- `src.endpoints.PrestaShop.save_text_file`: Функция для сохранения текста в файл.
- `src.suppliers.Supplier`: Класс для представления поставщика.

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

**Назначение**: Функция создает и возвращает объект поставщика с заданными параметрами.

**Параметры**:

- `supplier_prefix` (str, optional): Префикс поставщика. По умолчанию `'aliexpress'`.
- `locale` (str, optional): Локаль поставщика. По умолчанию `'en'`.

**Возвращает**:

- `Supplier`: Объект поставщика, созданный с использованием переданных параметров.

**Как работает функция**:

1. Определяет параметры поставщика в виде словаря `params`.
2. Создает объект `Supplier`, передавая в него параметры `supplier_prefix` и `locale`.
3. Возвращает созданный объект `Supplier`.

**Примеры**:

```python
from src.suppliers import Supplier  # Предполагается, что класс Supplier находится в этом модуле

# Пример 1: Запуск поставщика с префиксом 'aliexpress' и локалью 'en'
supplier1 = start_supplier()
print(supplier1)  # Вывод: <src.suppliers.Supplier object at ...>

# Пример 2: Запуск поставщика с префиксом 'ebay' и локалью 'ru'
supplier2 = start_supplier(supplier_prefix='ebay', locale='ru')
print(supplier2)  # Вывод: <src.suppliers.Supplier object at ...>