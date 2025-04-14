# Модуль `supplier.py`

## Обзор

Модуль `supplier.py` предназначен для работы с поставщиками в PrestaShop. Он содержит класс `PrestaSupplier`, который наследует функциональность от класса `PrestaShop` и предоставляет методы для взаимодействия с API PrestaShop, специфичные для управления поставщиками.

## Подробней

Модуль предоставляет возможность инициализировать объект поставщика PrestaShop с использованием домена API и ключа API. Он также включает обработку учетных данных, переданных в виде словаря или объекта `SimpleNamespace`. Класс `PrestaSupplier` позволяет выполнять операции, такие как получение, создание, обновление и удаление информации о поставщиках в PrestaShop. Расположение файла в структуре проекта `/src/endpoints/prestashop/supplier.py` указывает на его роль в качестве одного из endpoint'ов для взаимодействия с PrestaShop API.

## Классы

### `PrestaSupplier`

**Описание**: Класс `PrestaSupplier` предназначен для работы с поставщиками в PrestaShop. Он наследуется от класса `PrestaShop` и расширяет его функциональность, предоставляя возможность управления поставщиками через API PrestaShop.

**Наследует**:

- `PrestaShop`: Класс `PrestaSupplier` наследует методы и атрибуты класса `PrestaShop`, что позволяет ему использовать общую логику для взаимодействия с API PrestaShop.

**Атрибуты**:

- Отсутствуют специфические атрибуты, помимо наследованных от `PrestaShop`.

**Методы**:

- `__init__`: Инициализирует экземпляр класса `PrestaSupplier`.

### `__init__`

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

**Назначение**: Инициализация экземпляра класса `PrestaSupplier`. Этот метод устанавливает параметры подключения к API PrestaShop, такие как домен API и ключ API.

**Параметры**:

- `credentials` (Optional[dict | SimpleNamespace], optional): Словарь или объект `SimpleNamespace`, содержащий параметры `api_domain` и `api_key`. По умолчанию `None`.
- `api_domain` (Optional[str], optional): Домен API PrestaShop. По умолчанию `None`.
- `api_key` (Optional[str], optional): Ключ API PrestaShop. По умолчанию `None`.
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса.
- `**kwards`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса.

**Возвращает**:

- None

**Вызывает исключения**:

- `ValueError`: Если не предоставлены оба параметра `api_domain` и `api_key`.

**Как работает функция**:

1.  **Обработка учетных данных**: Функция проверяет, были ли переданы учетные данные через параметр `credentials`. Если да, она извлекает `api_domain` и `api_key` из этого объекта.
2.  **Проверка наличия обязательных параметров**: Функция проверяет, были ли предоставлены `api_domain` и `api_key` либо через `credentials`, либо непосредственно. Если хотя бы один из них отсутствует, вызывается исключение `ValueError`.
3.  **Инициализация родительского класса**: Функция вызывает конструктор родительского класса `PrestaShop` с переданными параметрами, инициализируя базовую функциональность для взаимодействия с API PrestaShop.

```ascii
    Проверка наличия credentials --> Извлечение api_domain и api_key из credentials (если credentials переданы)
    |
    V
    Проверка наличия api_domain и api_key --> Вызов исключения ValueError, если api_domain или api_key отсутствуют
    |
    V
    Вызов конструктора родительского класса PrestaShop с api_domain и api_key
```

**Примеры**:

```python
# Пример 1: Инициализация с передачей api_domain и api_key напрямую
supplier = PrestaSupplier(api_domain='example.com', api_key='test_key')

# Пример 2: Инициализация с передачей credentials в виде словаря
credentials = {'api_domain': 'example.com', 'api_key': 'test_key'}
supplier = PrestaSupplier(credentials=credentials)

# Пример 3: Инициализация с передачей credentials в виде SimpleNamespace
credentials = SimpleNamespace(api_domain='example.com', api_key='test_key')
supplier = PrestaSupplier(credentials=credentials)