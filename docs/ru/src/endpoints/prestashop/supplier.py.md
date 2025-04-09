# Модуль для работы с поставщиками PrestaShop

## Обзор

Модуль `supplier.py` предназначен для взаимодействия с API PrestaShop с целью управления информацией о поставщиках. Он содержит класс `PrestaSupplier`, который расширяет функциональность базового класса `PrestaShop` и предоставляет методы для работы с поставщиками в магазине PrestaShop.

## Подробнее

Модуль предоставляет возможность инициализации подключения к PrestaShop API с использованием домена API и ключа API. Он также обрабатывает случаи, когда необходимые параметры (домен API и ключ API) не предоставлены, и вызывает исключение `ValueError`.

## Классы

### `PrestaSupplier`

**Описание**: Класс `PrestaSupplier` предназначен для работы с поставщиками в PrestaShop.

**Наследует**:
- `PrestaShop`: Класс наследует функциональность для взаимодействия с API PrestaShop.

**Атрибуты**:
- Нет дополнительных атрибутов, кроме унаследованных от `PrestaShop`.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `PrestaSupplier`.

### `PrestaSupplier.__init__`

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

**Назначение**: Инициализация экземпляра класса `PrestaSupplier`.

**Параметры**:
- `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или объект `SimpleNamespace`, содержащий параметры `api_domain` и `api_key`. По умолчанию `None`.
- `api_domain` (Optional[str], optional): Домен API. По умолчанию `None`.
- `api_key` (Optional[str], optional): Ключ API. По умолчанию `None`.
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса `PrestaShop`.
- `**kwards`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса `PrestaShop`.

**Возвращает**:
- None

**Вызывает исключения**:
- `ValueError`: Если не предоставлены `api_domain` и `api_key`.

**Как работает функция**:

1.  Функция инициализации `__init__` класса `PrestaSupplier` принимает учетные данные, домен API и ключ API.
2.  Если предоставлены учетные данные, функция пытается извлечь `api_domain` и `api_key` из них.
3.  Проверяет, что `api_domain` и `api_key` установлены. Если нет, вызывает исключение `ValueError`.
4.  Вызывает конструктор родительского класса `PrestaShop` с переданными аргументами `api_domain`, `api_key`, `*args`, `**kwards`.

```
Инициализация
│
├── Проверка наличия credentials
│   └── Извлечение api_domain и api_key из credentials (если credentials предоставлены)
│
├── Проверка наличия api_domain и api_key
│   └── Вызов исключения ValueError (если api_domain или api_key не предоставлены)
│
└── Вызов конструктора родительского класса PrestaShop
```

**Примеры**:

1.  Инициализация с использованием параметров:

```python
supplier = PrestaSupplier(api_domain='example.com', api_key='12345')
```

2.  Инициализация с использованием словаря `credentials`:

```python
credentials = {'api_domain': 'example.com', 'api_key': '12345'}
supplier = PrestaSupplier(credentials=credentials)