# Модуль `supplier.py`

## Обзор

Модуль `supplier.py` предназначен для работы с поставщиками в PrestaShop. Он содержит класс `PrestaSupplier`, который наследует функциональность от класса `PrestaShop` и предоставляет методы для взаимодействия с API PrestaShop для управления поставщиками.

## Подробнее

Модуль предназначен для упрощения интеграции с PrestaShop API для управления поставщиками. Он использует класс `PrestaSupplier`, который инициализируется с учетными данными API и предоставляет методы для выполнения запросов к API PrestaShop.

## Классы

### `PrestaSupplier`

**Описание**: Класс для работы с поставщиками PrestaShop.

**Наследует**:
- `PrestaShop`: Класс, предоставляющий базовую функциональность для взаимодействия с API PrestaShop.

**Атрибуты**:
- Отсутствуют, но использует атрибуты, унаследованные от класса `PrestaShop`.

**Методы**:
- `__init__(credentials: Optional[dict | SimpleNamespace] = None, api_domain: Optional[str] = None, api_key: Optional[str] = None, *args, **kwargs)`: Инициализирует экземпляр класса `PrestaSupplier`.

### `__init__`

```python
def __init__(self, 
                 credentials: Optional[dict | SimpleNamespace] = None, 
                 api_domain: Optional[str] = None, 
                 api_key: Optional[str] = None, 
                 *args, **kwargs):
    """Инициализация поставщика PrestaShop.

    Args:
        credentials (Optional[dict | SimpleNamespace], optional): Словарь или объект SimpleNamespace с параметрами `api_domain` и `api_key`. Defaults to None.
        api_domain (Optional[str], optional): Домен API. Defaults to None.
        api_key (Optional[str], optional): Ключ API. Defaults to None.
    """
```

**Назначение**: Инициализирует экземпляр класса `PrestaSupplier`, проверяет и устанавливает учетные данные для доступа к API PrestaShop.

**Параметры**:
- `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или объект `SimpleNamespace`, содержащий параметры `api_domain` и `api_key`. По умолчанию `None`.
- `api_domain` (Optional[str], optional): Домен API PrestaShop. По умолчанию `None`.
- `api_key` (Optional[str], optional): Ключ API PrestaShop. По умолчанию `None`.
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса.
- `**kwargs`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса.

**Как работает функция**:

1. **Проверка `credentials`**: Если передан аргумент `credentials`, функция пытается извлечь значения `api_domain` и `api_key` из него. Это позволяет передавать учетные данные как единый объект.
2. **Проверка наличия `api_domain` и `api_key`**: Если `api_domain` или `api_key` не предоставлены (либо не были извлечены из `credentials`), функция вызывает исключение `ValueError`, указывающее на необходимость обоих параметров.
3. **Вызов конструктора родительского класса**: Если все проверки пройдены успешно, функция вызывает конструктор родительского класса (`PrestaShop`) с переданными учетными данными и любыми дополнительными аргументами `*args` и `**kwargs`.

**Примеры**:

```python
from types import SimpleNamespace

# Пример 1: Инициализация с использованием параметров api_domain и api_key
supplier = PrestaSupplier(api_domain='your_api_domain', api_key='your_api_key')

# Пример 2: Инициализация с использованием объекта credentials
credentials = SimpleNamespace(api_domain='your_api_domain', api_key='your_api_key')
supplier = PrestaSupplier(credentials=credentials)

# Пример 3: Инициализация с отсутствующими параметрами (вызовет исключение)
try:
    supplier = PrestaSupplier()
except ValueError as ex:
    print(f"Ошибка: {ex}")

# Пример 4: Инициализация с неполным объектом credentials (вызовет исключение)
credentials = {'api_domain': 'your_api_domain'}
try:
    supplier = PrestaSupplier(credentials=credentials)
except ValueError as ex:
    print(f"Ошибка: {ex}")