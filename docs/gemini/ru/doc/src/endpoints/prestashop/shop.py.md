# Модуль для работы с магазинами PrestaShop
## Обзор

Модуль `src.endpoints.prestashop.shop` предназначен для взаимодействия с магазинами PrestaShop через API. Он включает класс `PrestaShopShop`, который предоставляет функциональность для управления магазином PrestaShop.

## Подробней

Модуль содержит класс `PrestaShopShop`, который упрощает взаимодействие с API PrestaShop. Этот класс наследует функциональность из класса `PrestaShop` и предоставляет методы для работы с магазином PrestaShop, используя предоставленные учетные данные (домен API и ключ API).

## Классы

### `PrestaShopShop`

**Описание**: Класс `PrestaShopShop` предназначен для работы с магазинами PrestaShop. Он позволяет инициализировать магазин, используя учетные данные для доступа к API PrestaShop.

**Наследует**: `PrestaShop`

**Атрибуты**:
- Нет специфических атрибутов, кроме наследованных от `PrestaShop`.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `PrestaShopShop`.

#### `__init__`

```python
def __init__(self, 
             credentials: Optional[dict | SimpleNamespace] = None, 
             api_domain: Optional[str] = None, 
             api_key: Optional[str] = None, 
             *args, **kwards):
    """Инициализация магазина PrestaShop.

    Args:
        credentials (Optional[dict | SimpleNamespace], optional): Словарь или объект SimpleNamespace с параметрами `api_domain` и `api_key`. Defaults to None.
        api_domain (Optional[str], optional): Домен API. Defaults to None.
        api_key (Optional[str], optional): Ключ API. Defaults to None.
    """
```

**Назначение**: Инициализирует экземпляр класса `PrestaShopShop`, устанавливая домен API и ключ API для доступа к магазину PrestaShop.

**Параметры**:
- `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или объект `SimpleNamespace`, содержащий параметры `api_domain` и `api_key`. По умолчанию `None`.
- `api_domain` (Optional[str], optional): Домен API. По умолчанию `None`.
- `api_key` (Optional[str], optional): Ключ API. По умолчанию `None`.
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса.
- `**kwards`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса.

**Как работает функция**:
1. Проверяет, предоставлены ли учетные данные через параметр `credentials`. Если да, извлекает `api_domain` и `api_key` из этого словаря или объекта.
2. Проверяет, установлены ли `api_domain` и `api_key`. Если хотя бы один из них не установлен, вызывает исключение `ValueError`.
3. Вызывает конструктор родительского класса `PrestaShop` с переданными параметрами.

**Возвращает**:
- Ничего (None).

**Вызывает исключения**:
- `ValueError`: Если не предоставлены `api_domain` и `api_key`.

**Примеры**:
```python
# Пример 1: Инициализация с использованием отдельных параметров
shop = PrestaShopShop(api_domain="https://example.com/api", api_key="your_api_key")

# Пример 2: Инициализация с использованием словаря credentials
credentials = {"api_domain": "https://example.com/api", "api_key": "your_api_key"}
shop = PrestaShopShop(credentials=credentials)

# Пример 3: Инициализация с использованием SimpleNamespace
credentials = SimpleNamespace(api_domain="https://example.com/api", api_key="your_api_key")
shop = PrestaShopShop(credentials=credentials)