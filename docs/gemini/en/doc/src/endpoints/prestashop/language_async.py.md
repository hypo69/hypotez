# Модуль `language_async.py`

## Обзор

Модуль `language_async.py` предназначен для асинхронного взаимодействия с API PrestaShop для управления языками в интернет-магазине. Он содержит класс `PrestaLanguageAync`, который позволяет добавлять, удалять, обновлять и получать информацию о языках, используемых в PrestaShop.

## Детальное описание

Модуль предоставляет асинхронные методы для работы с языками PrestaShop, что позволяет эффективно управлять языковыми настройками магазина. Он использует асинхронные запросы к API PrestaShop для выполнения операций, таких как получение схемы языков и получение имени языка по индексу.

## Классы

### `PrestaLanguageAync`

**Описание**: Класс `PrestaLanguageAync` предоставляет интерфейс для взаимодействия с языками в PrestaShop. Он наследуется от класса `PrestaShopAsync` и использует его методы для выполнения API-запросов.

**Наследует**:
- `PrestaShopAsync`: Предоставляет базовые методы для асинхронного взаимодействия с API PrestaShop.

**Атрибуты**:
- Отсутствуют явно определенные атрибуты, но используются атрибуты родительского класса `PrestaShopAsync` для хранения параметров подключения к API.

**Методы**:
- `__init__(self, *args, **kwargs)`: Конструктор класса.
- `get_lang_name_by_index(self, lang_index: int | str) -> str`: Асинхронно возвращает имя языка (ISO код) по его индексу в таблице PrestaShop.
- `get_languages_schema(self) -> dict`: Асинхронно получает и возвращает схему языков из PrestaShop.

## Методы класса

### `__init__`

```python
def __init__(self, *args, **kwargs):
    """Класс интерфейс взаимодействия языками в Prestashop
    Важно помнить, что у каждого магазина своя нумерация языков
    :lang_string: ISO названия языка. Например: en, ru, he
    """
    ...
```

**Описание**:
Конструктор класса `PrestaLanguageAync`.

**Параметры**:
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса.
- `**kwargs`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса.

**Как работает**:
- Определяет интерфейс взаимодействия с языками в PrestaShop. Важно помнить, что нумерация языков может отличаться для каждого магазина.  `lang_string` - это ISO-код языка, например: `en`, `ru`, `he`.

**Примеры**:
```python
presta_language = PrestaLanguageAync(API_DOMAIN="your_api_domain", API_KEY="your_api_key")
```

### `get_lang_name_by_index`

```python
async def get_lang_name_by_index(self, lang_index: int | str) -> str:
    """Возвращает имя языка ISO по его индексу в таблице Prestashop"""
    try:
        return super().get('languagaes', resource_id=str(lang_index), display='full', io_format='JSON')
    except Exception as ex:
        logger.error(f"Ошибка получения языка по индексу {lang_index=}", ex)
        return ''
```

**Описание**:
Асинхронно получает имя языка (ISO код) по его индексу в таблице PrestaShop.

**Параметры**:
- `lang_index` (int | str): Индекс языка в таблице PrestaShop.

**Возвращает**:
- `str`: Имя языка (ISO код) или пустую строку в случае ошибки.

**Как работает**:
- Функция пытается получить имя языка, используя метод `get` родительского класса `PrestaShopAsync`.
- В случае возникновения ошибки, она логируется, и функция возвращает пустую строку.

**Примеры**:
```python
lang_name = await presta_language.get_lang_name_by_index(1)
print(lang_name)
```

### `get_languages_schema`

```python
async def get_languages_schema(self) -> dict:
    lang_dict = super().get_languages_schema()
    print(lang_dict)
```

**Описание**:
Асинхронно получает схему языков из PrestaShop.

**Возвращает**:
- `dict`: Схема языков.

**Как работает**:
- Функция вызывает метод `get_languages_schema` родительского класса `PrestaShopAsync` для получения схемы языков.
- Полученная схема выводится в консоль с использованием функции `print`.

**Примеры**:
```python
languages_schema = await presta_language.get_languages_schema()
print(languages_schema)
```

## Функции

### `main`

```python
async def main():
    """"""
    ...
    lang_class = PrestaLanguageAync()
    languagas_schema = await  lang_class.get_languages_schema()
    print(languagas_schema)
```

**Описание**:
Асинхронная функция `main` выполняет основные действия, необходимые для демонстрации работы класса `PrestaLanguageAync`.

**Как работает**:
- Создает экземпляр класса `PrestaLanguageAync`.
- Получает схему языков с помощью метода `get_languages_schema`.
- Выводит полученную схему языков в консоль.

**Примеры**:
```python
asyncio.run(main())