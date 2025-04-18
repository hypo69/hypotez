# Модуль для асинхронного управления языками в PrestaShop
## Обзор

Модуль `language_async.py` предоставляет асинхронный класс `PrestaLanguageAync`, который упрощает взаимодействие с API PrestaShop для управления языками магазина. Он позволяет получать информацию о языках, добавлять, удалять и обновлять языки в асинхронном режиме.

## Подробнее

Модуль предназначен для использования в асинхронных приложениях, где требуется взаимодействие с API PrestaShop для управления языками магазина. Он расширяет класс `PrestaShopAsync` и предоставляет методы для получения информации о языках по их индексу или ISO-коду.

## Классы

### `PrestaLanguageAync`

**Описание**: Класс `PrestaLanguageAync` предназначен для управления языками в PrestaShop через API. Он предоставляет методы для получения имени языка по индексу, получения схемы языков и другие операции.

**Наследует**: `PrestaShopAsync`

**Методы**:

- `__init__(self, *args, **kwards)`: Инициализирует экземпляр класса `PrestaLanguageAync`.
- `get_lang_name_by_index(self, lang_index: int | str) -> str`: Асинхронно возвращает ISO-код языка по его индексу в PrestaShop.
- `get_languages_schema(self) -> dict`: Асинхронно возвращает схему языков PrestaShop.

## Методы класса

### `__init__`

```python
def __init__(self, *args, **kwards):
    """Класс интерфейс взаимодействия языками в Prestashop
    Важно помнить, что у каждого магазина своя нумерация языков
    :lang_string: ISO названия языка. Например: en, ru, he
    """
    ...
```

**Назначение**: Инициализирует экземпляр класса `PrestaLanguageAync`. Важно помнить, что у каждого магазина своя нумерация языков. Параметр `lang_string` определяет ISO-код языка (например, `en`, `ru`, `he`).

**Параметры**:

- `*args`: Произвольные позиционные аргументы.
- `**kwards`: Произвольные именованные аргументы.

### `get_lang_name_by_index`

```python
async def get_lang_name_by_index(self, lang_index: int | str) -> str:
    """Возвращает имя языка ISO по его индексу в таблице Prestashop"""
    ...
```

**Назначение**: Асинхронно возвращает ISO-код языка по его индексу в таблице PrestaShop.

**Параметры**:

- `lang_index` (int | str): Индекс языка в PrestaShop.

**Возвращает**:

- `str`: ISO-код языка или пустую строку в случае ошибки.

**Вызывает исключения**:

- `Exception`: Если возникает ошибка при получении языка по индексу.

**Как работает функция**:

- Пытается получить язык по индексу, используя метод `get` из родительского класса `PrestaShopAsync`.
- Если возникает ошибка, логирует её с помощью `logger.error` и возвращает пустую строку.

**Примеры**:

```python
# Пример вызова функции
lang_class = PrestaLanguageAync()
lang_name = await lang_class.get_lang_name_by_index(1)
print(lang_name)
```

### `get_languages_schema`

```python
async def get_languages_schema(self) -> dict:
    """ """
    ...
```

**Назначение**: Асинхронно получает схему языков PrestaShop.

**Возвращает**:

- `dict`: Схема языков PrestaShop.

**Как работает функция**:

- Вызывает метод `get_languages_schema` из родительского класса `PrestaShopAsync`.
- Выводит полученную схему языков с использованием `print`.

**Примеры**:

```python
# Пример вызова функции
lang_class = PrestaLanguageAync()
languages_schema = await lang_class.get_languages_schema()
print(languages_schema)
```

## Другие функции

### `main`

```python
async def main():
    """"""
    ...
```

**Назначение**: Асинхронная функция, демонстрирующая использование класса `PrestaLanguageAync`.

**Как работает функция**:

- Создает экземпляр класса `PrestaLanguageAync`.
- Получает схему языков с использованием метода `get_languages_schema`.
- Выводит полученную схему языков с использованием `print`.

**Примеры**:

```python
# Пример вызова функции
asyncio.run(main())
```