# Модуль `product_translator`

## Обзор

Модуль `product_translator` предназначен для управления переводами полей товара PrestaShop. Он обеспечивает связь между словарем полей товара, таблицей переводов и сервисами перевода.

## Подробней

Модуль предоставляет функции для получения переводов из базы данных PrestaShop, вставки новых переводов, а также для перевода полей товара с использованием внешних сервисов, таких как OpenAI.

## Функции

### `rearrange_language_keys`

```python
def rearrange_language_keys(presta_fields_dict: dict, client_langs_schema: dict | List[dict], page_lang: str) -> dict:
    """Функция обновляет идентификатор языка в словаре presta_fields_dict на соответствующий идентификатор
    из схемы клиентских языков при совпадении языка страницы.

    Args:
        presta_fields_dict (dict): Словарь полей товара.
        page_lang (str): Язык страницы.
        client_langs_schema (list | dict): Схема языков клиента.

    Returns:
        dict: Обновленный словарь presta_fields_dict.
    """
    ...
```

**Назначение**: Обновляет идентификатор языка в словаре `presta_fields_dict` на соответствующий идентификатор из схемы клиентских языков при совпадении языка страницы.

**Параметры**:
- `presta_fields_dict` (dict): Словарь полей товара.
- `client_langs_schema` (list | dict): Схема языков клиента.
- `page_lang` (str): Язык страницы.

**Возвращает**:
- `dict`: Обновленный словарь `presta_fields_dict`.

**Как работает функция**:

1.  Находит соответствующий идентификатор языка в схеме клиентских языков, сравнивая `page_lang` с `locale`, `iso_code` и `language_code` каждого языка в `client_langs_schema`.
2.  Если найден соответствующий идентификатор языка, обновляет атрибут `id` в словаре `presta_fields_dict` для всех мультиязычных полей.

### `get_translations_from_presta_translations_table`

```python
def get_translations_from_presta_translations_table(product_reference: str, i18n: str = None) -> list:
    """Функция возвращает словарь переводов полей товара."""
    ...
```

**Назначение**: Возвращает список переводов полей товара из таблицы переводов.

**Параметры**:
- `product_reference` (str): Артикул товара.
- `i18n` (str, optional): Локаль (например, `'en_EN'`, `'he_HE'`, `'ru-RU'`). Defaults to None.

**Возвращает**:
- `list`: Список переводов полей товара.

**Как работает функция**:

1.  Использует класс `ProductTranslationsManager` для выполнения запроса к базе данных.
2.  Возвращает список найденных переводов.

### `insert_new_translation_to_presta_translations_table`

```python
def insert_new_translation_to_presta_translations_table(record):
    ...
```

**Назначение**: Вставляет новую запись перевода в таблицу переводов.

**Параметры**:
- `record` (dict): Запись для вставки.

**Как работает функция**:

1.  Использует класс `ProductTranslationsManager` для вставки новой записи в таблицу переводов.

### `translate_record`

```python
def translate_record(record: dict, from_locale: str, to_locale: str) -> dict:
    """Функция для перевода полей товара."""
    ...
```

**Назначение**: Переводит поля товара с использованием внешнего сервиса перевода (например, OpenAI).

**Параметры**:
- `record` (dict): Запись для перевода.
- `from_locale` (str): Локаль исходного языка.
- `to_locale` (str): Локаль целевого языка.

**Возвращает**:
- `dict`: Переведенная запись.

**Как работает функция**:

1.  Использует функцию `translate` из модуля `src.llm.openai` для перевода полей товара.
2.  Добавляет обработку переведенной записи (реализация не показана в предоставленном коде).