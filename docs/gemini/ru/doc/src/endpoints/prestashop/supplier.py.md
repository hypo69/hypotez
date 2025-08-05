# Модуль `src.endpoints.prestashop.supplier`

## Обзор

Модуль `src.endpoints.prestashop.supplier` предоставляет функциональность для взаимодействия с поставщиками в платформе PrestaShop через API. В модуле реализован класс `PrestaSupplier`, который наследуется от `PrestaShop`, чтобы обеспечить доступ к API-методам, специфичным для работы с поставщиками. 

## Классы

### `PrestaSupplier`

**Описание**: Класс `PrestaSupplier` реализует функциональность для работы с поставщиками в PrestaShop. Он наследует от `PrestaShop` и предоставляет дополнительные методы для управления поставщиками. 

**Наследует**: `PrestaShop`

**Атрибуты**:

- `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или объект `SimpleNamespace` с параметрами `api_domain` и `api_key`. По умолчанию `None`.
- `api_domain` (Optional[str], optional): Домен API. По умолчанию `None`.
- `api_key` (Optional[str], optional): Ключ API. По умолчанию `None`.

**Методы**:

- `__init__()`: Инициализирует класс `PrestaSupplier`. Принимает на вход параметры `credentials`, `api_domain` и `api_key`. 

    **Параметры**:

    - `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или объект `SimpleNamespace` с параметрами `api_domain` и `api_key`. По умолчанию `None`.
    - `api_domain` (Optional[str], optional): Домен API. По умолчанию `None`.
    - `api_key` (Optional[str], optional): Ключ API. По умолчанию `None`.

    **Принцип работы**:

    - Проверяет наличие параметров `api_domain` и `api_key`. 
    - Если `credentials` не `None`, то извлекает из него значения `api_domain` и `api_key`. 
    - Если `api_domain` и `api_key` отсутствуют, то генерируется исключение `ValueError`.
    - Вызывает метод `__init__` родительского класса `PrestaShop` для инициализации объекта.


## Примеры

```python
from src.endpoints.prestashop.supplier import PrestaSupplier

# Инициализация с использованием словаря credentials
credentials = {
    'api_domain': 'https://example.com',
    'api_key': 'your_api_key',
}
supplier = PrestaSupplier(credentials=credentials)

# Инициализация с использованием объекта SimpleNamespace
credentials = SimpleNamespace(
    api_domain='https://example.com',
    api_key='your_api_key',
)
supplier = PrestaSupplier(credentials=credentials)

# Инициализация с использованием отдельных параметров
supplier = PrestaSupplier(api_domain='https://example.com', api_key='your_api_key')
```