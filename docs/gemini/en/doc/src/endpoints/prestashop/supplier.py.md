# Модуль для работы с поставщиками PrestaShop

## Обзор

Этот модуль предоставляет класс `PrestaSupplier` для взаимодействия с API PrestaShop для управления поставщиками. Он позволяет инициализировать подключение к PrestaShop API, используя домен API и ключ API.

## Более детально

Модуль `PrestaSupplier` упрощает работу с поставщиками в PrestaShop, предоставляя удобный интерфейс для выполнения различных операций через API PrestaShop. Для аутентификации используются домен API и ключ API, которые могут быть переданы как отдельные параметры или через объект `credentials`.

## Классы

### `PrestaSupplier`

**Описание**: Класс для работы с поставщиками PrestaShop.

**Inherits**:
- Наследуется от класса `PrestaShop`.

**Attributes**:
- Нет специфических атрибутов, кроме тех, что наследуются от `PrestaShop`.

**Parameters**:
- `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или объект SimpleNamespace с параметрами `api_domain` и `api_key`. Defaults to None.
- `api_domain` (Optional[str], optional): Домен API. Defaults to None.
- `api_key` (Optional[str], optional): Ключ API. Defaults to None.

**Принцип работы**:
1. Класс принимает параметры для подключения к API PrestaShop, такие как `api_domain` и `api_key`.
2. Если переданы `credentials`, он пытается извлечь `api_domain` и `api_key` из них.
3. Если `api_domain` или `api_key` не предоставлены, вызывается исключение `ValueError`.
4. Инициализирует базовый класс `PrestaShop` с предоставленными учетными данными.

## Методы класса

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

**Назначение**: Инициализирует экземпляр класса `PrestaSupplier`.

**Параметры**:
- `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или `SimpleNamespace` объект, содержащий `api_domain` и `api_key`. По умолчанию `None`.
- `api_domain` (Optional[str], optional): Домен API PrestaShop. По умолчанию `None`.
- `api_key` (Optional[str], optional): Ключ API PrestaShop. По умолчанию `None`.

**Raises**:
- `ValueError`: Если не предоставлены `api_domain` и `api_key`.

**Пример**:
```python
supplier = PrestaSupplier(api_domain='your_api_domain', api_key='your_api_key')
```

## Параметры класса

- `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или объект `SimpleNamespace`, содержащий учетные данные API. Если предоставлен, `api_domain` и `api_key` будут извлечены из него.
- `api_domain` (Optional[str], optional): Домен API PrestaShop.
- `api_key` (Optional[str], optional): Ключ API PrestaShop.

**Примеры**:

Пример инициализации с использованием `api_domain` и `api_key`:
```python
supplier = PrestaSupplier(api_domain='your_api_domain', api_key='your_api_key')
```

Пример инициализации с использованием `credentials` в виде словаря:
```python
credentials = {'api_domain': 'your_api_domain', 'api_key': 'your_api_key'}
supplier = PrestaSupplier(credentials=credentials)
```

Пример инициализации с использованием `credentials` в виде `SimpleNamespace`:
```python
from types import SimpleNamespace
credentials = SimpleNamespace(api_domain='your_api_domain', api_key='your_api_key')
supplier = PrestaSupplier(credentials=credentials)
```