# Модуль `shop`

## Обзор

Модуль `shop` предназначен для работы с магазинами PrestaShop, предоставляя класс `PrestaShopShop` для взаимодействия с API PrestaShop. Он позволяет инициализировать магазин PrestaShop с использованием домена API и ключа API.

## Подробней

Модуль `shop` является частью подсистемы взаимодействия с PrestaShop и предоставляет удобный интерфейс для работы с магазинами на этой платформе. Он использует класс `PrestaShop` из модуля `api` для выполнения основных операций API. Расположение файла: `/src/endpoints/prestashop/shop.py`.

## Классы

### `PrestaShopShop`

**Описание**: Класс `PrestaShopShop` предназначен для работы с магазинами PrestaShop. Он наследует функциональность от класса `PrestaShop` и предоставляет методы для взаимодействия с API PrestaShop.

**Наследует**:
- `PrestaShop`: Класс, предоставляющий базовые методы для взаимодействия с API PrestaShop.

**Атрибуты**:
- Нет специфических атрибутов, кроме тех, что наследуются от `PrestaShop`.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `PrestaShopShop`.

### `__init__`
```python
def __init__(self, 
             credentials: Optional[dict | SimpleNamespace] = None, 
             api_domain: Optional[str] = None, 
             api_key: Optional[str] = None, 
             *args, **kwargs) -> None:
    """Инициализация магазина PrestaShop.

    Args:
        credentials (Optional[dict | SimpleNamespace], optional): Словарь или объект SimpleNamespace с параметрами `api_domain` и `api_key`. Defaults to None.
        api_domain (Optional[str], optional): Домен API. Defaults to None.
        api_key (Optional[str], optional): Ключ API. Defaults to None.
    """
```

**Назначение**:
Инициализирует экземпляр класса `PrestaShopShop`, устанавливая параметры подключения к API PrestaShop.

**Параметры**:
- `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или объект `SimpleNamespace`, содержащий параметры `api_domain` и `api_key`. Используется для передачи учетных данных вместо отдельных параметров `api_domain` и `api_key`. По умолчанию `None`.
- `api_domain` (Optional[str], optional): Домен API PrestaShop. По умолчанию `None`.
- `api_key` (Optional[str], optional): Ключ API PrestaShop. По умолчанию `None`.
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса `PrestaShop`.
- `**kwargs`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса `PrestaShop`.

**Как работает функция**:
1. Проверяет, переданы ли учетные данные через параметр `credentials`. Если да, извлекает значения `api_domain` и `api_key` из этого словаря или объекта `SimpleNamespace`.
2. Проверяет, установлены ли значения `api_domain` и `api_key`. Если хотя бы одно из них не установлено, вызывает исключение `ValueError`.
3. Вызывает конструктор родительского класса `PrestaShop`, передавая ему параметры `api_domain`, `api_key`, `*args` и `**kwargs`.

**Вызывает исключения**:
- `ValueError`: Если не переданы `api_domain` и `api_key` ни по отдельности, ни в составе параметра `credentials`.

**Примеры**:

1. Инициализация с использованием отдельных параметров:

```python
shop = PrestaShopShop(api_domain='example.com', api_key='your_api_key')
```

2. Инициализация с использованием параметра `credentials`:

```python
from types import SimpleNamespace

credentials = SimpleNamespace(api_domain='example.com', api_key='your_api_key')
shop = PrestaShopShop(credentials=credentials)
```

3. Вызов исключения `ValueError`:

```python
try:
    shop = PrestaShopShop()
except ValueError as ex:
    print(f"Ошибка: {ex}")  # Вывод: Ошибка: Необходимы оба параметра: api_domain и api_key.