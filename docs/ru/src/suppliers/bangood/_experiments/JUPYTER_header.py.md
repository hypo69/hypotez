# Модуль `src.suppliers.bangood._experiments`

## Обзор

Модуль предназначен для экспериментов с поставщиком Banggood. Он содержит инструменты и функции для работы с данными, полученными от этого поставщика, включая обработку категорий, продуктов и другие вспомогательные функции.

## Подробней

Модуль предоставляет возможности для запуска поставщика, а также содержит импорты необходимых библиотек и модулей для работы с веб-драйвером, продуктами, категориями и другими сущностями. Он также включает вспомогательные классы и функции для форматирования и нормализации строк.

## Классы

В данном файле классы не определены.

## Функции

### `start_supplier`

```python
def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en' ):
    """ Старт поставщика """
    params: dict = \
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params))
```

**Назначение**: Запускает поставщика с указанными параметрами.

**Параметры**:
- `supplier_prefix` (str): Префикс поставщика. По умолчанию `'aliexpress'`.
- `locale` (str): Локаль поставщика. По умолчанию `'en'`.

**Возвращает**:
- `Supplier`: Объект поставщика, созданный с переданными параметрами.

**Как работает функция**:
- Функция принимает префикс поставщика и локаль в качестве аргументов.
- Формирует словарь `params`, содержащий переданные значения.
- Создает и возвращает экземпляр класса `Supplier` с использованием распаковки словаря `params` в качестве аргументов конструктора.

**Примеры**:

```python
from src.suppliers import Supplier  # Предполагая, что Supplier импортируется именно так

# Запуск поставщика с префиксом по умолчанию и локалью по умолчанию
supplier1 = start_supplier()
print(type(supplier1))  # Вывод: <class 'src.suppliers.Supplier'>

# Запуск поставщика с указанным префиксом и локалью
supplier2 = start_supplier(supplier_prefix='banggood', locale='ru')
print(type(supplier2))  # Вывод: <class 'src.suppliers.Supplier'>