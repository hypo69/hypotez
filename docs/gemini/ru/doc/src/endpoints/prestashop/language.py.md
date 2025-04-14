# Модуль для работы с языками в PrestaShop

## Обзор

Модуль `language.py` предоставляет интерфейс для взаимодействия с сущностью `language` в CMS PrestaShop через API PrestaShop. Он содержит класс `PrestaLanguage`, который позволяет получать информацию о языках, используемых в магазине PrestaShop.

## Подробнее

Модуль предназначен для упрощения работы с языками в PrestaShop, предоставляя методы для получения схемы языков и имени языка по его индексу. Важно помнить, что у каждого магазина своя нумерация языков.

## Классы

### `PrestaLanguage`

**Описание**: Класс `PrestaLanguage` наследует класс `PrestaShop` и предназначен для работы с языками магазина PrestaShop.

**Наследует**:

- `PrestaShop`: Этот класс предоставляет базовый функционал для взаимодействия с API PrestaShop.

**Атрибуты**:

- Отсутствуют явно определенные атрибуты в коде, но класс наследует все атрибуты от родительского класса `PrestaShop`, такие как параметры для подключения к API PrestaShop.

**Принцип работы**:

Класс `PrestaLanguage` инициализируется с параметрами, необходимыми для подключения к API PrestaShop. Он предоставляет методы для получения информации о языках, таких как схема языков и имя языка по его индексу.

**Методы**:

- `__init__`: Конструктор класса.
- `get_lang_name_by_index`: Получает ISO-код языка из магазина PrestaShop по его индексу.
- `get_languages_schema`: Извлекает словарь актуальных языков для данного магазина.

## Методы класса

### `__init__`

```python
def __init__(self, *args, **kwards):
    """
    Args:
        *args: Произвольные аргументы.
        **kwards: Произвольные именованные аргументы.

    Note:
        Важно помнить, что у каждого магазина своя нумерация языков.
        Я определяю языки в своих базах в таком порядке:
        `en` - 1;
        `he` - 2;
        `ru` - 3.
    """
    ...
```

**Назначение**: Инициализирует экземпляр класса `PrestaLanguage`.

**Параметры**:

- `*args`: Произвольные позиционные аргументы.
- `**kwards`: Произвольные именованные аргументы.

**Возвращает**:

- None

**Вызывает исключения**:

- Отсутствуют явные исключения.

### `get_lang_name_by_index`

```python
def get_lang_name_by_index(self, lang_index: int | str) -> str:
    """
    Функция извлекает ISO код азыка из магазина `Prestashop`

    Args:
        lang_index: Индекс языка в таблице PrestaShop.

    Returns:
        Имя языка ISO по его индексу в таблице PrestaShop.
    """
    ...
```

**Назначение**: Извлекает ISO-код языка из магазина PrestaShop по его индексу.

**Параметры**:

- `lang_index` (int | str): Индекс языка в таблице PrestaShop.

**Возвращает**:

- `str`: Имя языка ISO по его индексу в таблице PrestaShop.

**Вызывает исключения**:

- `Exception`: В случае ошибки при получении языка по индексу, ошибка логируется.

**Примеры**:

```python
prestalanguage = PrestaLanguage()
lang_name = prestalanguage.get_lang_name_by_index(1)
print(lang_name)  # Например, выводит "English"
```

### `get_languages_schema`

```python
def get_languages_schema(self) -> Optional[dict]:
    """Функция извлекает словарь актуальных языков дла данного магазина.

    Returns:
        Language schema or `None` on failure.

    Examples:
        # Возвращаемый словарь:
        {
            "languages": {
                    "language": [
                                    {
                                    "attrs": {
                                        "id": "1"
                                    },
                                    "value": ""
                                    },
                                    {
                                    "attrs": {
                                        "id": "2"
                                    },
                                    "value": ""
                                    },
                                    {
                                    "attrs": {
                                        "id": "3"
                                    },
                                    "value": ""
                                    }
                                ]
            }
        }
    """
    ...
```

**Назначение**: Извлекает словарь актуальных языков для данного магазина.

**Параметры**:

- Отсутствуют.

**Возвращает**:

- `Optional[dict]`: Схема языков или `None` в случае неудачи.

**Вызывает исключения**:

- `Exception`: В случае ошибки при выполнении запроса, ошибка логируется.

**Примеры**:

```python
prestalanguage = PrestaLanguage()
languages_schema = prestalanguage.get_languages_schema()
print(languages_schema)
```

## Параметры класса

- `API_DOMAIN` (str): Домен API PrestaShop.
- `API_KEY` (str): Ключ API PrestaShop.

## Примеры

```python
# Пример создания экземпляра класса PrestaLanguage
prestalanguage = PrestaLanguage(API_DOMAIN='your_api_domain', API_KEY='your_api_key')

# Пример получения схемы языков
languages_schema = prestalanguage.get_languages_schema()
if languages_schema:
    print(languages_schema)

# Пример получения имени языка по индексу
lang_name = prestalanguage.get_lang_name_by_index(1)
if lang_name:
    print(lang_name)
```