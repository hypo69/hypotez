# Модуль для работы с языками в PrestaShop.

## Обзор

Модуль предоставляет интерфейс взаимодействия с сущностью `language` в CMS `Prestashop` через `API Prestashop`.

## Детали

Этот модуль упрощает управление языками в PrestaShop, предоставляя методы для добавления, удаления, обновления и получения информации о языках через API PrestaShop. Он использует классы `PrestaShop` и `gs` из других модулей для выполнения HTTP-запросов и обработки данных.

## Классы

### `PrestaLanguage`

Класс, отвечающий за настройки языков магазина PrestaShop.

**Наследует**:
- `PrestaShop`: Класс для взаимодействия с API PrestaShop.

**Пример использования**:
```python
    >>> prestalanguage = PrestaLanguage(API_DOMAIN=API_DOMAIN, API_KEY=API_KEY)
    >>> prestalanguage.add_language_PrestaShop('English', 'en')
    >>> prestalanguage.delete_language_PrestaShop(3)
    >>> prestalanguage.update_language_PrestaShop(4, 'Updated Language Name')
    >>> print(prestalanguage.get_language_details_PrestaShop(5))
```

**Методы**:
- `__init__`: Инициализирует экземпляр класса `PrestaLanguage`.
- `get_lang_name_by_index`: Извлекает ISO код языка из магазина `Prestashop`.
- `get_languages_schema`: Извлекает словарь актуальных языков для данного магазина.

## Методы класса

### `__init__`

```python
def __init__(self, *args, **kwargs):
    """
    Инициализирует экземпляр класса `PrestaLanguage`.

    Args:
        *args: Произвольные аргументы.
        **kwargs: Произвольные именованные аргументы.

    Note:
        Важно помнить, что у каждого магазина своя нумерация языков.
        Я определяю языки в своих базах в таком порядке:
        `en` - 1;
        `he` - 2;
        `ru` - 3.
    """
    ...
```
### `get_lang_name_by_index`

```python
def get_lang_name_by_index(self, lang_index: int | str) -> str:
    """
    Функция извлекает ISO код языка из магазина `Prestashop`.

    Args:
        lang_index: Индекс языка в таблице PrestaShop.

    Returns:
        str: Имя языка ISO по его индексу в таблице PrestaShop.
    
    Raises:
        PrestaShopException: Если происходит ошибка при получении языка по индексу.
    """
```

**Как работает функция**:
- Функция `get_lang_name_by_index` пытается получить язык из PrestaShop по указанному индексу, используя метод `get` суперкласса (`PrestaShop`).
- В случае успеха возвращается ISO код языка. Если происходит ошибка, она логируется, и возвращается пустая строка.
    
### `get_languages_schema`

```python
def get_languages_schema(self) -> Optional[dict]:
    """
    Функция извлекает словарь актуальных языков для данного магазина.

    Returns:
        Optional[dict]: Language schema or `None` on failure.

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
    
    Raises:
        PrestaShopException: Если происходит ошибка при выполнении запроса к API PrestaShop.
    """
```

**Как работает функция**:
- Функция `get_languages_schema` отправляет запрос к API PrestaShop для получения схемы языков.
- Она вызывает метод `_exec` с параметрами `'languages'`, `display='full'`, и `io_format='JSON'`.
- В случае успеха возвращается словарь, представляющий схему языков. Если происходит ошибка, она логируется, и возвращается `None`.

## Функции

### `main`

```python
async def main():
    """
    Пример асинхронного вызова методов класса `PrestaLanguage`.
    """
    ...