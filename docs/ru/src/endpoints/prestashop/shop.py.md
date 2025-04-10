# Модуль для работы с магазинами PrestaShop

## Обзор

Модуль `src.endpoints.prestashop.shop` предоставляет класс `PrestaShopShop`, который упрощает взаимодействие с магазинами PrestaShop через API. Он наследуется от класса `PrestaShop` и позволяет инициализировать магазин, используя домен API и ключ API.

## Подробнее

Модуль предназначен для упрощения работы с API PrestaShop. Он позволяет инициализировать подключение к магазину, используя домен и ключ API, которые могут быть переданы как отдельные параметры, так и в виде словаря или объекта `SimpleNamespace`. Класс `PrestaShopShop` предоставляет удобный интерфейс для взаимодействия с API PrestaShop, что упрощает автоматизацию задач, связанных с управлением магазином.

## Классы

### `PrestaShopShop`

**Описание**: Класс `PrestaShopShop` предназначен для работы с магазинами PrestaShop через API. Он наследуется от класса `PrestaShop` и предоставляет функциональность для инициализации подключения к магазину и взаимодействия с его API.

**Наследует**:
- `PrestaShop`: Класс, предоставляющий базовую функциональность для работы с API PrestaShop.

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

**Назначение**: Инициализирует экземпляр класса `PrestaShopShop`, устанавливая параметры подключения к API PrestaShop.

**Параметры**:
- `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или объект `SimpleNamespace`, содержащий параметры `api_domain` и `api_key`. По умолчанию `None`.
- `api_domain` (Optional[str], optional): Домен API PrestaShop. По умолчанию `None`.
- `api_key` (Optional[str], optional): Ключ API PrestaShop. По умолчанию `None`.
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса.
- `**kwards`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса.

**Вызывает исключения**:
- `ValueError`: Если не предоставлены оба параметра `api_domain` и `api_key`.

**Как работает функция**:

1.  **Проверка наличия `credentials`**: Проверяется, передан ли аргумент `credentials`.
2.  **Извлечение параметров из `credentials`**: Если `credentials` передан, из него извлекаются значения `api_domain` и `api_key`, перезаписывая значения, переданные напрямую, если они есть.
3.  **Проверка наличия `api_domain` и `api_key`**: Проверяется, установлены ли значения `api_domain` и `api_key`. Если хотя бы один из них не установлен, выбрасывается исключение `ValueError`.
4.  **Инициализация родительского класса**: Вызывается конструктор родительского класса `PrestaShop` с переданными параметрами.

```
Проверка наличия credentials --> Извлечение api_domain и api_key из credentials --> Проверка наличия api_domain и api_key --> Инициализация родительского класса PrestaShop
```

**Примеры**:

1.  Инициализация с использованием отдельных параметров:

```python
shop = PrestaShopShop(api_domain='example.com', api_key='12345')
```

2.  Инициализация с использованием словаря `credentials`:

```python
credentials = {'api_domain': 'example.com', 'api_key': '12345'}
shop = PrestaShopShop(credentials=credentials)
```

3.  Инициализация с использованием объекта `SimpleNamespace`:

```python
credentials = SimpleNamespace(api_domain='example.com', api_key='12345')
shop = PrestaShopShop(credentials=credentials)
```

4.  Вызов исключения `ValueError`:

```python
try:
    shop = PrestaShopShop()
except ValueError as ex:
    print(f"Ошибка: {ex}")  # Вывод: Ошибка: Необходимы оба параметра: api_domain и api_key.