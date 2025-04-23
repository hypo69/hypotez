# Module `src.endpoints.prestashop.shop`

## Обзор

Модуль `src.endpoints.prestashop.shop` предназначен для работы с магазинами PrestaShop. Он содержит класс `PrestaShopShop`, который расширяет класс `PrestaShop` из модуля `src.endpoints.prestashop.api`.
Модуль позволяет инициализировать магазины PrestaShop с использованием домена API и ключа API.

## Более подробная информация

Этот модуль предоставляет удобный способ взаимодействия с API PrestaShop, позволяя выполнять различные операции, такие как получение и обновление данных о товарах, категориях и т.д.
Он использует классы и функции из других модулей, таких как `src.logger.logger` для логирования, `src.utils.jjson` для работы с JSON, и `src.endpoints.prestashop.api` для взаимодействия с API PrestaShop.

## Классы

### `PrestaShopShop`

**Описание**: Класс для работы с магазинами PrestaShop.

**Наследует**:
- `PrestaShop` (из `src.endpoints.prestashop.api`): Предоставляет базовую функциональность для взаимодействия с API PrestaShop.

**Атрибуты**:
- Нет специфических атрибутов, кроме тех, что наследуются от `PrestaShop`.

**Параметры**:
- `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или объект `SimpleNamespace` с параметрами `api_domain` и `api_key`. По умолчанию `None`.
- `api_domain` (Optional[str], optional): Домен API. По умолчанию `None`.
- `api_key` (Optional[str], optional): Ключ API. По умолчанию `None`.
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса.
- `**kwargs`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса.

**Принцип работы**:
- Класс `PrestaShopShop` инициализируется с использованием домена API и ключа API, которые могут быть переданы как отдельные параметры или в виде словаря/объекта `SimpleNamespace` через параметр `credentials`.
- Если `api_domain` и `api_key` не переданы, или если они отсутствуют в `credentials`, выбрасывается исключение `ValueError`.
- Класс наследует функциональность для взаимодействия с API PrestaShop от класса `PrestaShop`.

**Методы**:
- `__init__`: Инициализация экземпляра класса `PrestaShopShop`.

## Методы класса

### `__init__`

```python
def __init__(self,
                 credentials: Optional[dict | SimpleNamespace] = None,
                 api_domain: Optional[str] = None,
                 api_key: Optional[str] = None,
                 *args, **kwargs):
    """Инициализация магазина PrestaShop.

    Args:
        credentials (Optional[dict | SimpleNamespace], optional): Словарь или объект SimpleNamespace с параметрами `api_domain` и `api_key`. Defaults to None.
        api_domain (Optional[str], optional): Домен API. Defaults to None.
        api_key (Optional[str], optional): Ключ API. Defaults to None.
    """
```

**Назначение**: Инициализирует экземпляр класса `PrestaShopShop`, устанавливая домен API и ключ API для взаимодействия с магазином PrestaShop.

**Параметры**:
- `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или объект `SimpleNamespace`, содержащий параметры `api_domain` и `api_key`. По умолчанию `None`.
- `api_domain` (Optional[str], optional): Домен API. По умолчанию `None`.
- `api_key` (Optional[str], optional): Ключ API. По умолчанию `None`.
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса.
- `**kwargs`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса.

**Как работает функция**:
- Функция проверяет, переданы ли `api_domain` и `api_key` напрямую или через параметр `credentials`.
- Если переданы `credentials`, функция пытается извлечь `api_domain` и `api_key` из него.
- Если `api_domain` или `api_key` отсутствуют, выбрасывается исключение `ValueError`.
- Функция вызывает конструктор родительского класса `PrestaShop` с переданными параметрами.

**Примеры**:

```python
# Инициализация с использованием отдельных параметров
shop = PrestaShopShop(api_domain='example.com', api_key='12345')

# Инициализация с использованием словаря credentials
credentials = {'api_domain': 'example.com', 'api_key': '12345'}
shop = PrestaShopShop(credentials=credentials)

# Инициализация с использованием объекта SimpleNamespace
credentials = SimpleNamespace(api_domain='example.com', api_key='12345')
shop = PrestaShopShop(credentials=credentials)
```