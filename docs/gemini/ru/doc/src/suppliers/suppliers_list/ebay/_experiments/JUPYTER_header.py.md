# src.suppliers.ebay.\_experiments.JUPYTER_header

## Обзор

Данный модуль предназначен для экспериментов с поставщиком eBay. Он содержит импорты необходимых библиотек и классов для работы с продуктами, категориями, веб-драйвером и другими утилитами.

## Подробнее

Модуль подготавливает окружение для экспериментов, добавляя корневую директорию проекта в `sys.path`, что позволяет импортировать модули из других частей проекта. Также, он содержит функцию `start_supplier`, которая, предположительно, должна создавать и возвращать инстанс класса `Supplier` с заданными параметрами.

## Классы

В данном файле классы не представлены.

## Функции

### `start_supplier`

```python
def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en' ) -> Supplier:
    """ Старт поставщика 
    Args:
        supplier_prefix (str, optional): Префикс поставщика. По умолчанию 'aliexpress'.
        locale (str, optional): Локаль поставщика. По умолчанию 'en'.

    Returns:
        Supplier: Инстанс класса `Supplier` с заданными параметрами.
    """
    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)
```

**Назначение**: Функция `start_supplier` предназначена для создания и возвращения объекта поставщика (предположительно класса `Supplier`).

**Параметры**:
- `supplier_prefix` (str, optional): Префикс поставщика, по умолчанию `'aliexpress'`.
- `locale` (str, optional): Локаль поставщика, по умолчанию `'en'`.

**Возвращает**:
- `Supplier`: Объект класса `Supplier`, созданный с использованием переданных параметров.

**Как работает функция**:
1. Определяется словарь `params`, содержащий переданные аргументы `supplier_prefix` и `locale`.
2. Возвращается инстанс класса `Supplier`, созданный с использованием распакованного словаря `params` в качестве аргументов.

**Примеры**:

```python
supplier1 = start_supplier(supplier_prefix='ebay', locale='de')
# Создаст объект Supplier с supplier_prefix='ebay' и locale='de'

supplier2 = start_supplier()
# Создаст объект Supplier с supplier_prefix='aliexpress' и locale='en' (значения по умолчанию)