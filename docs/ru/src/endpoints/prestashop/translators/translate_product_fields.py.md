# Модуль: src.translators.translate_product_fields

## Обзор

Модуль `translate_product_fields.py` предназначен для управления переводами полей товаров, обеспечивая взаимодействие между словарем полей товара, таблицей переводов и сервисами перевода. Он включает функции для получения переводов из базы данных PrestaShop, добавления новых переводов и перевода отдельных записей.

## Подробней

Этот модуль служит связующим звеном между различными компонентами системы перевода товаров. Он обеспечивает получение существующих переводов из базы данных PrestaShop, вставку новых переводов и использование сервисов машинного перевода для автоматического перевода контента.

## Функции

### `get_translations_from_presta_translations_table`

```python
def get_translations_from_presta_translations_table(product_reference: str, credentials: dict, i18n: str = None) -> list:
    """Функция возвращает словарь переводов полей товара.

    Args:
        product_reference (str): Артикул товара, для которого требуется получить переводы.
        credentials (dict): Параметры подключения к базе данных PrestaShop.
        i18n (str, optional): Язык перевода в формате en_EN, he_HE, ru-RU. По умолчанию `None`.

    Returns:
        list: Список словарей, содержащих переводы полей товара.

    Как работает функция:
        - Функция создает инстанс класса `ProductTranslationsManager` для управления соединениями с базой данных.
        - Формирует фильтр поиска по артикулу товара.
        - Выполняет запрос к базе данных для получения записей переводов, соответствующих фильтру.
        - Возвращает список найденных записей.
    """
    ...
```

**Параметры**:
- `product_reference` (str): Артикул товара.
- `credentials` (dict): Параметры подключения к базе данных PrestaShop.
- `i18n` (str, optional): Язык перевода. По умолчанию `None`.

**Возвращает**:
- `list`: Список словарей с переводами.

**Пример**:

```python
product_reference = "REF123"
credentials = {
    "host": "localhost",
    "user": "user",
    "password": "password",
    "database": "prestashop_db"
}
i18n = "ru_RU"

translations = get_translations_from_presta_translations_table(product_reference, credentials, i18n)
print(translations) # Вывод: [{'id': 1, 'product_reference': 'REF123', 'name': 'Товар 123', ...}, ...]
```

### `insert_new_translation_to_presta_translations_table`

```python
def insert_new_translation_to_presta_translations_table(record: dict, credentials: dict):
    """Функция для вставки новой записи перевода в таблицу переводов PrestaShop.

    Args:
        record (dict): Словарь с данными для новой записи перевода.
        credentials (dict): Параметры подключения к базе данных PrestaShop.

   Как работает функция:
        - Функция создает инстанс класса `ProductTranslationsManager` для управления соединениями с базой данных.
        - Выполняет вставку записи перевода в базу данных.
    """
    ...
```

**Параметры**:
- `record` (dict): Данные для вставки.
- `credentials` (dict): Параметры подключения к базе данных PrestaShop.

**Пример**:

```python
record = {
    "product_reference": "REF456",
    "name": "Новый товар 456",
    "description": "Описание нового товара 456"
}
credentials = {
    "host": "localhost",
    "user": "user",
    "password": "password",
    "database": "prestashop_db"
}

insert_new_translation_to_presta_translations_table(record, credentials)
```

### `translate_record`

```python
def translate_record(record: dict, from_locale: str, to_locale: str) -> dict:
    """Функция для перевода полей товара.

    Args:
        record (dict): Словарь с полями товара для перевода.
        from_locale (str): Исходный язык перевода.
        to_locale (str): Язык, на который требуется перевести.

    Returns:
        dict: Словарь с переведенными полями товара.

    Как работает функция:
        - Функция вызывает функцию `translate` из модуля `src.llm` для выполнения перевода.
        - Производит обработку полученной переведенной записи (детали обработки не указаны в предоставленном коде).
        - Возвращает словарь с переведенными данными.
    """
    ...
```

**Параметры**:
- `record` (dict): Данные для перевода.
- `from_locale` (str): Исходный язык.
- `to_locale` (str): Целевой язык.

**Возвращает**:
- `dict`: Словарь с переведенными данными.

**Пример**:

```python
record = {
    "name": "Product 789",
    "description": "Description of product 789"
}
from_locale = "en"
to_locale = "ru"

translated_record = translate_record(record, from_locale, to_locale)
print(translated_record) # Вывод: {'name': 'Товар 789', 'description': 'Описание товара 789'}
```