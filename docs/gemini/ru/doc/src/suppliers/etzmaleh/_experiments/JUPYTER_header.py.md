# Документация для модуля `src.suppliers.etzmaleh._experiments`

## Обзор

Модуль `src.suppliers.etzmaleh._experiments` предназначен для экспериментов, связанных с поставщиком `etzmaleh`. Включает в себя импорты необходимых библиотек, настройку путей для импорта модулей из проекта `hypotez`, а также функцию для запуска поставщика.

## Подробней

Модуль содержит настройки путей для работы с проектом, импорты различных классов и функций, используемых в проекте `hypotez`, а также функцию `start_supplier` для запуска поставщика с заданными параметрами.
Анализируя предоставленный код, можно понять, что он служит для подготовки окружения и запуска процесса работы с определенным поставщиком (например, `aliexpress`) в рамках проекта `hypotez`.

## Функции

### `start_supplier`

```python
def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en') -> Supplier:
    """ Старт поставщика """
    params: dict = \
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)
```

**Назначение**: Функция `start_supplier` предназначена для запуска поставщика с заданными параметрами.

**Параметры**:
- `supplier_prefix` (str, optional): Префикс поставщика. По умолчанию `'aliexpress'`.
- `locale` (str, optional): Локаль поставщика. По умолчанию `'en'`.

**Возвращает**:
- `Supplier`: Объект класса `Supplier`, созданный с переданными параметрами.

**Как работает функция**:
1. Функция принимает два параметра: `supplier_prefix` и `locale`, которые определяют, какого поставщика и с какой локалью нужно запустить.
2. Создается словарь `params`, содержащий переданные параметры.
3. Создается и возвращается объект класса `Supplier` с использованием оператора распаковки `**params`.

**Примеры**:

```python
from src.suppliers import Supplier  # Предполагается, что класс Supplier импортирован

# Запуск поставщика aliexpress с английской локалью
supplier1 = start_supplier(supplier_prefix='aliexpress', locale='en')

# Запуск поставщика example с русской локалью
supplier2 = start_supplier(supplier_prefix='example', locale='ru')