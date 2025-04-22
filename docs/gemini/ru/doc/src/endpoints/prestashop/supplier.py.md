# Модуль `src.endpoints.prestashop.supplier`

## Обзор

Модуль `src.endpoints.prestashop.supplier` предназначен для работы с поставщиками в PrestaShop. Он содержит класс `PrestaSupplier`, который наследует функциональность от класса `PrestaShop` и предоставляет методы для взаимодействия с API PrestaShop для управления поставщиками.

## Подробнее

Модуль предоставляет удобный интерфейс для выполнения операций, связанных с поставщиками, таких как получение информации о поставщиках, создание, обновление и удаление поставщиков.

## Классы

### `PrestaSupplier`

**Описание**: Класс `PrestaSupplier` предназначен для работы с поставщиками PrestaShop. Он наследует функциональность от класса `PrestaShop` и предоставляет методы для взаимодействия с API PrestaShop для управления поставщиками.

**Наследует**:
- `PrestaShop`: Класс, предоставляющий общую функциональность для взаимодействия с API PrestaShop.

**Атрибуты**:
- Отсутствуют, класс использует атрибуты родительского класса `PrestaShop`.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `PrestaSupplier`.

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

**Назначение**: Инициализирует экземпляр класса `PrestaSupplier`, устанавливая параметры для подключения к API PrestaShop.

**Параметры**:
- `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или объект `SimpleNamespace`, содержащий параметры `api_domain` и `api_key`. По умолчанию `None`.
- `api_domain` (Optional[str], optional): Домен API PrestaShop. По умолчанию `None`.
- `api_key` (Optional[str], optional): Ключ API PrestaShop. По умолчанию `None`.
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса.
- `**kwards`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса.

**Как работает функция**:
- Если передан параметр `credentials`, функция пытается извлечь значения `api_domain` и `api_key` из него.
- Проверяется, что параметры `api_domain` и `api_key` установлены (либо переданы напрямую, либо извлечены из `credentials`). Если хотя бы один из них не установлен, выбрасывается исключение `ValueError`.
- Вызывается конструктор родительского класса `PrestaShop` с переданными параметрами, инициализируя подключение к API PrestaShop.

**Вызывает исключения**:
- `ValueError`: Если не переданы параметры `api_domain` и `api_key` (непосредственно или через `credentials`).

**Примеры**:

1.  Инициализация с использованием параметров:

```python
supplier = PrestaSupplier(api_domain='example.com', api_key='your_api_key')
```

2.  Инициализация с использованием словаря `credentials`:

```python
credentials = {'api_domain': 'example.com', 'api_key': 'your_api_key'}
supplier = PrestaSupplier(credentials=credentials)
```

3.  Инициализация с использованием `SimpleNamespace`:

```python
from types import SimpleNamespace
credentials = SimpleNamespace(api_domain='example.com', api_key='your_api_key')
supplier = PrestaSupplier(credentials=credentials)