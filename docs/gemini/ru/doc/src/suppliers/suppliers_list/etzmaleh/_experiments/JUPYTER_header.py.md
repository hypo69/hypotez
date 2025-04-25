# Модуль для запуска поставщика

## Обзор

Модуль содержит функцию `start_supplier`, которая используется для запуска поставщика.

## Подробнее

Функция `start_supplier` принимает два аргумента:
- `supplier_prefix`: префикс поставщика (например, 'aliexpress').
- `locale`: язык (например, 'en').

Функция создает словарь `params` с переданными аргументами и возвращает объект класса `Supplier`.

## Функции

### `start_supplier`

**Назначение**: Запуск поставщика.

**Параметры**:
- `supplier_prefix` (str): Префикс поставщика.
- `locale` (str): Язык.

**Возвращает**:
- `Supplier`: Объект класса `Supplier`.

**Как работает функция**:
- Функция создает словарь `params` с переданными аргументами.
- Функция возвращает объект класса `Supplier` с параметрами из словаря `params`.

**Примеры**:

```python
from src.suppliers.etzmaleh._experiments.JUPYTER_header import start_supplier

# Запуск поставщика 'aliexpress' на английском языке
supplier = start_supplier(supplier_prefix='aliexpress', locale='en')

# Запуск поставщика 'amazon' на русском языке
supplier = start_supplier(supplier_prefix='amazon', locale='ru')
```

## Параметры

- `supplier_prefix` (str): Префикс поставщика.
- `locale` (str): Язык.