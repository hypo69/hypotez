# Модуль `notebook_header.py`

## Обзор

Модуль `notebook_header.py` предназначен для настройки окружения и импорта необходимых библиотек для экспериментов с поставщиком Amazon в проекте `hypotez`. Он добавляет корневую директорию проекта в `sys.path`, чтобы обеспечить доступ к другим модулям проекта, и импортирует необходимые классы и функции.

## Подробней

Этот файл служит заголовком для экспериментов, проводимых с Amazon. Он выполняет следующие задачи:

1.  Добавляет корневую директорию проекта в `sys.path`, чтобы обеспечить доступ к другим модулям проекта.
2.  Импортирует необходимые библиотеки и классы, такие как `Path`, `json`, `re`, `gs`, `Driver`, `Supplier`, `Product`, `Category`, `StringFormatter`, `StringNormalizer`, `pprint` и `save_text_file`.
3.  Определяет функцию `start_supplier`, которая используется для запуска поставщика с заданными параметрами.

## Функции

### `start_supplier`

```python
def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.

    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль поставщика.

    Returns:
        Supplier | str: Объект поставщика или сообщение об ошибке, если параметры не заданы.
    """
    if not supplier_prefix and not locale:
        return "Не задан сценарий и язык"

    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }

    return Supplier(**params)
```

**Назначение**: Запускает поставщика с заданными параметрами.

**Параметры**:

*   `supplier_prefix` (str): Префикс поставщика.
*   `locale` (str): Локаль поставщика.

**Возвращает**:

*   `Supplier | str`: Объект поставщика или сообщение об ошибке, если параметры не заданы.

**Как работает функция**:

1.  Проверяет, заданы ли параметры `supplier_prefix` и `locale`. Если нет, возвращает сообщение об ошибке.
2.  Создает словарь `params` с параметрами поставщика.
3.  Создает экземпляр класса `Supplier` с использованием параметров из словаря `params` и возвращает его.

**Примеры**:

```python
# Пример вызова функции start_supplier с заданными параметрами
supplier = start_supplier(supplier_prefix='amazon', locale='en_US')
print(supplier)  # Выведет объект Supplier, если параметры заданы

# Пример вызова функции start_supplier без параметров
error_message = start_supplier(supplier_prefix='', locale='')
print(error_message)  # Выведет "Не задан сценарий и язык"
```