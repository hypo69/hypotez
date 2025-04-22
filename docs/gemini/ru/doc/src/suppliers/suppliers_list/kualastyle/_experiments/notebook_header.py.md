# src.suppliers.kualastyle._experiments.notebook_header

## Обзор

Модуль `notebook_header` содержит код, необходимый для инициализации и запуска поставщика `kualastyle`. Он добавляет корневую директорию проекта в `sys.path`, импортирует необходимые библиотеки и модули, а также содержит функцию для запуска поставщика.

## Подробней

Этот модуль предназначен для экспериментов и отладки, связанными с поставщиком `kualastyle`. Он содержит импорты, настройки путей и функцию `start_supplier`, которая инициализирует и возвращает объект `Supplier`.

## Классы

В данном модуле классы отсутствуют.

## Функции

### `start_supplier`

```python
def start_supplier(supplier_prefix: str = 'kualastyle'):
    """ Старт поставщика (kualastyle)
    Args:
        supplier_prefix (str, optional): Префикс поставщика. По умолчанию 'kualastyle'.

    Returns:
        Supplier: Возвращает экземпляр класса `Supplier`.
    """
    params: dict = {
        'supplier_prefix': supplier_prefix
    }
    
    return Supplier(**params)
```

**Назначение**: Запускает поставщика `kualastyle`, создавая экземпляр класса `Supplier` с указанным префиксом.

**Параметры**:
- `supplier_prefix` (str, optional): Префикс поставщика. По умолчанию имеет значение `'kualastyle'`.

**Возвращает**:
- `Supplier`: Объект класса `Supplier`, инициализированный с переданным префиксом.

**Как работает функция**:
1. Определяется словарь `params`, содержащий префикс поставщика.
2. Создается и возвращается экземпляр класса `Supplier` с использованием оператора `**params` для передачи параметров в конструктор класса `Supplier`.

**Примеры**:

```python
supplier = start_supplier()  # Создает поставщика с префиксом 'kualastyle'
supplier = start_supplier(supplier_prefix='another_supplier')  # Создает поставщика с префиксом 'another_supplier'
```