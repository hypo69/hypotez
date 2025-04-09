# Модуль для работы с магазинами PrestaShop

## Обзор

Модуль `src.endpoints.prestashop.shop` предоставляет класс `PrestaShopShop` для взаимодействия с магазинами PrestaShop. Он наследует функциональность от класса `PrestaShop` и предназначен для упрощения работы с API PrestaShop.

## Подробней

Модуль содержит класс `PrestaShopShop`, который используется для инициализации и управления магазином PrestaShop. Он позволяет установить соединение с API PrestaShop, используя домен API и ключ API.

## Классы

### `PrestaShopShop`

**Описание**: Класс `PrestaShopShop` предназначен для работы с магазинами PrestaShop через API.

**Наследует**:

- `PrestaShop`: Класс `PrestaShopShop` наследует методы и атрибуты от класса `PrestaShop`, который предоставляет базовую функциональность для взаимодействия с API PrestaShop.

**Атрибуты**:

- Нет дополнительных атрибутов, кроме тех, что наследуются от `PrestaShop`.

**Методы**:

- `__init__`: Метод инициализации класса `PrestaShopShop`.

### `__init__`

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

**Назначение**: Инициализация экземпляра класса `PrestaShopShop`.

**Параметры**:

- `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или объект `SimpleNamespace`, содержащий параметры `api_domain` и `api_key`. По умолчанию `None`.
- `api_domain` (Optional[str], optional): Домен API магазина PrestaShop. По умолчанию `None`.
- `api_key` (Optional[str], optional): Ключ API для доступа к магазину PrestaShop. По умолчанию `None`.
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса.
- `**kwards`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса.

**Возвращает**:

- `None`

**Вызывает исключения**:

- `ValueError`: Если не указаны `api_domain` и `api_key` ни в `credentials`, ни по отдельности.

**Как работает функция**:

1. **Инициализация**:
   - Функция инициализирует класс `PrestaShopShop`, устанавливая соединение с API PrestaShop.
   - Проверяет, переданы ли параметры `api_domain` и `api_key` через аргумент `credentials` или напрямую.

2. **Проверка параметров**:
   - Если `credentials` предоставлены, функция пытается извлечь `api_domain` и `api_key` из `credentials`.
   - Если `api_domain` или `api_key` не указаны ни в `credentials`, ни как отдельные параметры, вызывается исключение `ValueError`.

3. **Вызов родительского конструктора**:
   - Если все необходимые параметры присутствуют, вызывается конструктор родительского класса `PrestaShop` с переданными `api_domain`, `api_key`, `*args` и `**kwards`.

```
    Начало
    │
    ├── Проверка `credentials`
    │   └── Извлечение `api_domain` и `api_key` из `credentials` (если есть)
    │
    ├── Проверка наличия `api_domain` и `api_key`
    │   └── Выброс `ValueError`, если отсутствуют
    │
    └── Вызов конструктора `PrestaShop` с `api_domain`, `api_key`, `*args`, `**kwards`
        │
        Конец
```

**Примеры**:

1. Инициализация с использованием отдельных параметров:

```python
shop = PrestaShopShop(api_domain='https://your-prestashop.com/api', api_key='your_api_key')
```

2. Инициализация с использованием словаря `credentials`:

```python
credentials = {'api_domain': 'https://your-prestashop.com/api', 'api_key': 'your_api_key'}
shop = PrestaShopShop(credentials=credentials)
```

3. Инициализация с использованием `SimpleNamespace`:

```python
credentials = SimpleNamespace(api_domain='https://your-prestashop.com/api', api_key='your_api_key')
shop = PrestaShopShop(credentials=credentials)