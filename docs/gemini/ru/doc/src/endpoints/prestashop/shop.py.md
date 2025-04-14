# Модуль для работы с магазинами PrestaShop

## Обзор

Модуль `src.endpoints.prestashop.shop` предоставляет класс `PrestaShopShop`, который расширяет функциональность класса `PrestaShop` для взаимодействия с магазинами, работающими на платформе PrestaShop. Он позволяет инициализировать подключение к магазину PrestaShop с использованием домена API и ключа API.

## Подробней

Этот модуль предназначен для упрощения работы с API PrestaShop, предоставляя удобный интерфейс для выполнения различных операций, таких как получение и обновление данных магазина. Он использует модуль `src.logger.logger` для логирования и модуль `src.utils.jjson` для обработки JSON-данных. Расположение файла в структуре проекта `hypotez` указывает на то, что он является частью подсистемы, отвечающей за взаимодействие с PrestaShop.

## Классы

### `PrestaShopShop`

**Описание**: Класс `PrestaShopShop` предназначен для работы с магазинами PrestaShop. Он наследуется от класса `PrestaShop` и предоставляет функциональность для инициализации подключения к магазину с использованием домена API и ключа API.

**Наследует**:

- `PrestaShop`: Класс, предоставляющий базовую функциональность для работы с API PrestaShop.

**Атрибуты**:

- Отсутствуют. Все атрибуты наследуются от родительского класса `PrestaShop`.

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
    ...
```

**Назначение**: Инициализирует экземпляр класса `PrestaShopShop`, устанавливая соединение с API PrestaShop.

**Параметры**:

- `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или объект `SimpleNamespace`, содержащий параметры `api_domain` и `api_key`. По умолчанию `None`.
- `api_domain` (Optional[str], optional): Домен API PrestaShop. По умолчанию `None`.
- `api_key` (Optional[str], optional): Ключ API PrestaShop. По умолчанию `None`.
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса.
- `**kwards`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса.

**Как работает функция**:

1.  Проверяет, переданы ли учетные данные (`credentials`). Если да, пытается извлечь `api_domain` и `api_key` из них.
2.  Проверяет, переданы ли `api_domain` и `api_key` напрямую или через `credentials`. Если хотя бы один из них не передан, выбрасывает исключение `ValueError`.
3.  Вызывает конструктор родительского класса `PrestaShop` с переданными `api_domain`, `api_key`, `*args` и `**kwards` для инициализации соединения с API PrestaShop.

**Вызывает исключения**:

- `ValueError`: Если не переданы `api_domain` и `api_key`.

**Примеры**:

```python
# Пример 1: Инициализация с использованием api_domain и api_key
shop = PrestaShopShop(api_domain='your_api_domain', api_key='your_api_key')

# Пример 2: Инициализация с использованием credentials
credentials = SimpleNamespace(api_domain='your_api_domain', api_key='your_api_key')
shop = PrestaShopShop(credentials=credentials)

# Пример 3: Попытка инициализации без api_domain и api_key вызовет исключение
try:
    shop = PrestaShopShop()
except ValueError as ex:
    print(f"Ошибка: {ex}")  # Выведет: Ошибка: Необходимы оба параметра: api_domain и api_key.