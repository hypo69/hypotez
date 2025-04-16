# Модуль для работы с языками в PrestaShop

## Обзор

Модуль `src.endpoints.prestashop.language` предоставляет инструменты для взаимодействия с языками (languages) в CMS PrestaShop через PrestaShop API.

## Подробней

Модуль предоставляет класс `PrestaLanguage` для получения информации о языках, поддерживаемых в магазине PrestaShop.

## Классы

### `PrestaLanguage`

**Описание**: Класс, отвечающий за настройки языков магазина PrestaShop.

**Наследует**:

*   `PrestaShop`: Предоставляет базовые методы для взаимодействия с API PrestaShop.

**Атрибуты**:

*   Нет явно определенных атрибутов, но наследует атрибуты от класса `PrestaShop`, такие как `api_key` и `api_domain`.

**Методы**:

*   `__init__(self, *args, **kwards)`: Инициализирует объект `PrestaLanguage`.
*   `get_lang_name_by_index(self, lang_index: int | str) -> str`: Извлекает ISO код языка из магазина `Prestashop`.
*   `get_languages_schema(self) -> Optional[dict]`: Извлекает словарь актуальных языков для данного магазина.

## Методы класса `PrestaLanguage`

### `__init__`

```python
def __init__(self, *args, **kwards):
```

**Назначение**: Инициализирует объект `PrestaLanguage`.

**Параметры**:

*   `*args`: Произвольные аргументы.
*   `**kwards`: Произвольные именованные аргументы.

**Как работает функция**:

1.  Вызывает конструктор родительского класса `PrestaShop` с переданными аргументами.

**Примечание**:

Важно помнить, что у каждого магазина своя нумерация языков. Я определяю языки в своих базах в таком порядке:
`en` - 1;
`he` - 2;
`ru` - 3.

### `get_lang_name_by_index`

```python
def get_lang_name_by_index(self, lang_index: int | str) -> str:
```

**Назначение**: Функция извлекает ISO код языка из магазина `Prestashop`.

**Параметры**:

*   `lang_index` (int | str): Индекс языка в таблице PrestaShop.

**Возвращает**:

*   `str`: Имя языка ISO по его индексу в таблице PrestaShop.

**Как работает функция**:

1.  Вызывает метод `get` родительского класса `PrestaShop` для получения информации о языке из API PrestaShop.
2.  В случае ошибки логирует информацию об ошибке и возвращает пустую строку.

### `get_languages_schema`

```python
def get_languages_schema(self) -> Optional[dict]:
```

**Назначение**: Функция извлекает словарь актуальных языков для данного магазина.

**Возвращает**:

*   `Optional[dict]`: Language schema или `None` при неудаче.

**Как работает функция**:

1.  Вызывает метод `_exec` для выполнения запроса к API PrestaShop и получения списка языков.
2.  Возвращает полученный ответ.
3.  В случае ошибки логирует информацию об ошибке и возвращает `None`.

**Примеры**:

```python
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
```

## Примеры

### `main` (заглушка)

```python
async def main():
    """
    Example:
        >>> asyncio.run(main())
    """
    ...
    lang_class = PrestaLanguage()
    languagas_schema = await lang_class.get_languages_schema()
    print(languagas_schema)
```

**Назначение**: Определяет асинхронную функцию `main`, которая демонстрирует использование класса `PrestaLanguage`.

**Как работает функция**:

1.  Создает экземпляр класса `PrestaLanguage`.
2.  Вызывает метод `get_languages_schema` для получения схемы языков.
3.  Выводит полученную схему.