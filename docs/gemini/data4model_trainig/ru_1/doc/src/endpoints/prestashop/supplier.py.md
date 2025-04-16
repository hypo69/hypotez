# Модуль для работы с поставщиками PrestaShop
## Обзор

Модуль `src.endpoints.prestashop.supplier` предназначен для взаимодействия с API PrestaShop для управления поставщиками. Он содержит класс `PrestaSupplier`, который наследует функциональность из класса `PrestaShop` и предоставляет методы для работы с поставщиками в магазине PrestaShop.

## Подробнее

Этот модуль обеспечивает удобный интерфейс для выполнения операций, связанных с поставщиками PrestaShop, используя API PrestaShop.  Он позволяет инициализировать подключение к API PrestaShop, используя домен API и ключ API, либо напрямую, либо через предоставление объекта `credentials`.

## Классы

### `PrestaSupplier`

**Описание**: Класс `PrestaSupplier` предназначен для работы с поставщиками PrestaShop. Он расширяет класс `PrestaShop` и предоставляет функциональность для взаимодействия с API PrestaShop для выполнения операций, связанных с поставщиками.

**Наследует**:
- `PrestaShop`: Класс `PrestaSupplier` наследует от класса `PrestaShop`, который предоставляет базовую функциональность для взаимодействия с API PrestaShop.

**Атрибуты**:
- Отсутствуют специфические атрибуты, кроме наследованных от `PrestaShop`.

**Методы**:
- `__init__`: Метод инициализации класса `PrestaSupplier`.

## Методы класса

### `__init__`

```python
def __init__(self, 
                 credentials: Optional[dict | SimpleNamespace] = None, 
                 api_domain: Optional[str] = None, 
                 api_key: Optional[str] = None, 
                 *args, **kwards):
    """Инициализация поставщика PrestaShop.

    Args:
        credentials (Optional[dict | SimpleNamespace], optional): Словарь или объект SimpleNamespace с параметрами `api_domain` и `api_key`. Defaults to None.
        api_domain (Optional[str], optional): Домен API. Defaults to None.
        api_key (Optional[str], optional): Ключ API. Defaults to None.
    """
```

**Назначение**: Инициализирует экземпляр класса `PrestaSupplier`.

**Параметры**:
- `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или объект `SimpleNamespace`, содержащий параметры `api_domain` и `api_key`. По умолчанию `None`.
- `api_domain` (Optional[str], optional): Домен API PrestaShop. По умолчанию `None`.
- `api_key` (Optional[str], optional): Ключ API PrestaShop. По умолчанию `None`.
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса `PrestaShop`.
- `**kwards`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса `PrestaShop`.

**Возвращает**:
- None

**Вызывает исключения**:
- `ValueError`: Если не указаны `api_domain` и `api_key` ни в `credentials`, ни как отдельные параметры.

**Как работает функция**:
- При инициализации проверяется, переданы ли параметры `api_domain` и `api_key` напрямую или через словарь `credentials`.
- Если `credentials` переданы, метод пытается извлечь `api_domain` и `api_key` из этого словаря.
- Если хотя бы один из параметров (`api_domain` или `api_key`) не указан, возбуждается исключение `ValueError`.
- Затем вызывается конструктор родительского класса `PrestaShop` с переданными параметрами для инициализации базового API PrestaShop.

**Примеры**:

1.  Инициализация с использованием параметров `api_domain` и `api_key`:

```python
supplier = PrestaSupplier(api_domain='your_api_domain', api_key='your_api_key')
```

2.  Инициализация с использованием объекта `credentials`:

```python
from types import SimpleNamespace
credentials = SimpleNamespace(api_domain='your_api_domain', api_key='your_api_key')
supplier = PrestaSupplier(credentials=credentials)
```

3.  Инициализация с отсутствующими параметрами:

```python
try:
    supplier = PrestaSupplier()
except ValueError as ex:
    print(f"Ошибка: {ex}")
    # Вывод: Ошибка: Необходимы оба параметра: api_domain и api_key.