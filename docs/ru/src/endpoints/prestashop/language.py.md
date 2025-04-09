# Модуль для работы с языками в PrestaShop (`language.py`)

## Обзор

Модуль `language.py` предназначен для взаимодействия с сущностью `language` в CMS PrestaShop через API PrestaShop. Он предоставляет класс `PrestaLanguage`, который позволяет получать информацию о языках, а также добавлять, удалять и обновлять их.

## Подробней

Этот модуль предоставляет интерфейс для управления языками в PrestaShop, что может быть полезно для автоматизации задач, связанных с локализацией и мультиязычностью интернет-магазина. Он использует API PrestaShop для выполнения операций и предоставляет методы для получения информации о языках, добавления новых языков, удаления существующих и обновления информации о них.

## Классы

### `PrestaLanguage`

**Описание**: Класс `PrestaLanguage` наследуется от класса `PrestaShop` и предназначен для работы с языками в магазине PrestaShop.

**Наследует**:
- `PrestaShop`: Предоставляет базовый функционал для взаимодействия с API PrestaShop.

**Атрибуты**:
- Отсутствуют явно объявленные атрибуты, но используются атрибуты, унаследованные от класса `PrestaShop`, такие как параметры для подключения к API.

**Методы**:
- `__init__(self, *args, **kwards)`: Инициализирует экземпляр класса `PrestaLanguage`.
- `get_lang_name_by_index(self, lang_index: int | str) -> str`: Извлекает ISO код языка из магазина PrestaShop по его индексу.
- `get_languages_schema(self) -> Optional[dict]`: Извлекает словарь актуальных языков для данного магазина.

#### `__init__(self, *args, **kwards)`

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

**Как работает**:
1.  Метод `__init__` вызывается при создании нового экземпляра класса `PrestaLanguage`.
2.  Принимает произвольные позиционные и именованные аргументы.
3.  В теле функции стоит `...`, что означает, что здесь должна быть реализация инициализации объекта, например, инициализация соединения с API PrestaShop и другие необходимые параметры.

#### `get_lang_name_by_index(self, lang_index: int | str) -> str`

```python
def get_lang_name_by_index(self, lang_index: int | str) -> str:
    """
    Функция извлекает ISO код азыка из магазина `Prestashop`

    Args:
        lang_index: Индекс языка в таблице PrestaShop.

    Returns:
        Имя языка ISO по его индексу в таблице PrestaShop.
    """
    try:
        return super().get('languagaes', resource_id=str(lang_index), display='full', io_format='JSON')
    except Exception as ex:
        logger.error(f'Ошибка получения языка по индексу {lang_index=}', ex)
        return ''
```

**Назначение**: Извлекает ISO код языка из магазина PrestaShop по его индексу.

**Параметры**:
- `lang_index` (int | str): Индекс языка в таблице PrestaShop.

**Возвращает**:
- `str`: Имя языка ISO по его индексу в таблице PrestaShop. Возвращает пустую строку в случае ошибки.

**Вызывает исключения**:
- `Exception`: Обрабатывается внутри функции, логируется ошибка.

**Как работает функция**:

1.  Функция `get_lang_name_by_index` принимает индекс языка в PrestaShop в качестве аргумента.
2.  Вызывает метод `get` родительского класса (`PrestaShop`) для выполнения запроса к API PrestaShop.
3.  В случае успеха возвращает имя языка ISO.
4.  Если происходит ошибка, логирует её и возвращает пустую строку.

```
    lang_index
    |
    V
    Получение данных о языке из API PrestaShop
    |
    V
    Успешно?
    |
    да --> Возврат имени языка
    |
    нет --> Логирование ошибки и возврат пустой строки
```

**Примеры**:

```python
# Пример использования функции
presta_language = PrestaLanguage()
lang_name = presta_language.get_lang_name_by_index(1)
print(lang_name)  # Вывод: <Имя языка>
```

#### `get_languages_schema(self) -> Optional[dict]`

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
    try:
        response = self._exec('languages', display='full', io_format='JSON')
        return response
    except Exception as ex:
        logger.error(f'Error:', ex)
        return
```

**Назначение**: Извлекает словарь актуальных языков для данного магазина.

**Возвращает**:
- `Optional[dict]`: Language schema или `None` в случае ошибки.

**Вызывает исключения**:
- `Exception`: Обрабатывается внутри функции, логируется ошибка.

**Как работает функция**:

1.  Функция `get_languages_schema` вызывает метод `_exec` для выполнения запроса к API PrestaShop для получения списка языков.
2.  В случае успеха возвращает словарь с информацией о языках.
3.  Если происходит ошибка, логирует её и возвращает `None`.

```
    Вызов API PrestaShop для получения списка языков
    |
    V
    Успешно?
    |
    да --> Возврат словаря с информацией о языках
    |
    нет --> Логирование ошибки и возврат None
```

**Примеры**:

```python
# Пример использования функции
presta_language = PrestaLanguage()
languages_schema = presta_language.get_languages_schema()
print(languages_schema)  # Вывод: <Словарь с информацией о языках>
```

## Функции

### `main()`

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

**Назначение**: Пример асинхронной функции для демонстрации работы с классом `PrestaLanguage`.

**Как работает функция**:

1.  Функция `main` является асинхронной функцией.
2.  Создает экземпляр класса `PrestaLanguage`.
3.  Вызывает метод `get_languages_schema` для получения списка языков.
4.  Выводит полученный список языков.
5.  В теле функции стоит `...`, что означает, что здесь может быть дополнительная логика.

### Запуск модуля

```python
if __name__ == '__main__':
    asyncio.run(main())
```

**Назначение**: Запускает асинхронную функцию `main`, если скрипт запущен как основной.