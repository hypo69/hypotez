# Асинхронный модуль для работы с языками в PrestaShop

## Обзор

Модуль `src.endpoints.prestashop.language_async` предоставляет асинхронные инструменты для взаимодействия с языками в PrestaShop.

## Подробней

Модуль содержит класс `PrestaLanguageAync`, который позволяет асинхронно получать информацию о языках, поддерживаемых в магазине PrestaShop.

## Классы

### `PrestaLanguageAync`

**Описание**: Класс, отвечающий за настройки языков магазина PrestaShop (асинхронная версия).

**Наследует**:

*   `PrestaShopAsync`: Предоставляет асинхронные методы для взаимодействия с API PrestaShop.

**Атрибуты**:

*   Нет явно определенных атрибутов, но наследует атрибуты от класса `PrestaShopAsync`, такие как `api_key` и `api_domain`.

**Методы**:

*   `__init__(self, *args, **kwards)`: Инициализирует объект `PrestaLanguageAync`.
*   `get_lang_name_by_index(self, lang_index: int | str) -> str`: Возвращает имя языка ISO по его индексу в таблице Prestashop.
*   `get_languages_schema(self) -> dict`: Извлекает схему языков.

## Методы класса `PrestaLanguageAync`

### `__init__`

```python
def __init__(self, *args, **kwards):
```

**Назначение**: Инициализирует объект `PrestaLanguageAync`.

**Параметры**:

*   `*args`: Произвольные аргументы.
*   `**kwards`: Произвольные именованные аргументы.

**Как работает функция**:

1.  Вызывает конструктор родительского класса `PrestaShopAsync` с переданными аргументами.

**Примечание**:

Важно помнить, что у каждого магазина своя нумерация языков. Я определяю языки в своих базах в таком порядке:
`en` - 1;
`he` - 2;
`ru` - 3.
ISO названия языка. Например: en, ru, he

### `get_lang_name_by_index`

```python
async def get_lang_name_by_index(self, lang_index: int | str) -> str:
```

**Назначение**: Асинхронно возвращает имя языка ISO по его индексу в таблице Prestashop.

**Параметры**:

*   `lang_index` (int | str): Индекс языка в таблице PrestaShop.

**Возвращает**:

*   `str`: Имя языка ISO по его индексу в таблице PrestaShop.

**Как работает функция**:

1.  Асинхронно вызывает метод `get` родительского класса `PrestaShopAsync` для получения информации о языке из API PrestaShop.
2.  В случае ошибки логирует информацию об ошибке и возвращает пустую строку.

### `get_languages_schema`

```python
async def get_languages_schema(self) -> dict:
```

**Назначение**: Асинхронно извлекает схему языков.

**Возвращает**:

*   `dict`: Схема языков.

**Как работает функция**:

1.  Вызывает метод `get_languages_schema` родительского класса `PrestaShopAsync` для получения схемы языков.
2.  Выводит полученную схему.

## Примеры

### `main` (заглушка)

```python
async def main():
    """"""
    ...
    lang_class = PrestaLanguageAync()
    languagas_schema = await  lang_class.get_languages_schema()
    print(languagas_schema)
```

**Назначение**: Определяет асинхронную функцию `main`, которая демонстрирует использование класса `PrestaLanguageAync`.

**Как работает функция**:

1.  Создает экземпляр класса `PrestaLanguageAync`.
2.  Вызывает метод `get_languages_schema` для получения схемы языков.
3.  Выводит полученную схему.