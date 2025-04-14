# Модуль `JUPYTER_header`

## Обзор

Модуль содержит набор импортов и определение функции `start_supplier`, предназначенных для инициализации и запуска поставщика (supplier) в контексте проекта `hypotez`. Модуль обеспечивает интеграцию различных компонентов проекта, таких как веб-драйвер, модели данных (продукты, категории) и утилиты для работы со строками.

## Подробнее

Модуль `JUPYTER_header.py` является частью структуры проекта `hypotez` и, вероятно, используется для экспериментов и отладки, связанных с поставщиками (suppliers) и их интеграцией в систему. Он содержит импорты необходимых библиотек и модулей, а также функцию `start_supplier`, которая принимает префикс поставщика и локаль в качестве параметров и возвращает экземпляр класса `Supplier`.

## Функции

### `start_supplier`

```python
def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en') -> Supplier:
    """Старт поставщика

    Args:
        supplier_prefix (str, optional): Префикс поставщика. По умолчанию 'aliexpress'.
        locale (str, optional): Локаль. По умолчанию 'en'.

    Returns:
        Supplier: Объект поставщика.
    """
    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    return Supplier(**params)
```

**Назначение**:
Функция `start_supplier` предназначена для создания и инициализации объекта поставщика (`Supplier`) с заданными параметрами.

**Параметры**:

- `supplier_prefix` (str, optional): Префикс поставщика, используемый для идентификации конкретного поставщика (например, `'aliexpress'`). По умолчанию `'aliexpress'`.
- `locale` (str, optional): Локаль, определяющая язык и региональные настройки для работы с поставщиком. По умолчанию `'en'`.

**Возвращает**:

- `Supplier`: Объект класса `Supplier`, инициализированный с переданными параметрами.

**Как работает функция**:

1. Функция принимает два параметра: `supplier_prefix` и `locale`, с значениями по умолчанию `'aliexpress'` и `'en'` соответственно.
2. Создается словарь `params`, содержащий переданные параметры.
3. Используя оператор `**params`, словарь передается в качестве именованных аргументов конструктору класса `Supplier`.
4. Функция возвращает созданный экземпляр класса `Supplier`.

**Примеры**:

```python
from src.suppliers import Supplier
from src.suppliers.suppliers_list.grandadvance.scenarios._experiments.JUPYTER_header import start_supplier

# Пример 1: Запуск поставщика с префиксом 'aliexpress' и локалью 'en'
supplier1 = start_supplier()
print(type(supplier1))  # Вывод: <class 'src.suppliers.supplier.Supplier'>

# Пример 2: Запуск поставщика с префиксом 'amazon' и локалью 'de'
supplier2 = start_supplier(supplier_prefix='amazon', locale='de')
print(type(supplier2))  # Вывод: <class 'src.suppliers.supplier.Supplier'>