# Модуль для работы с переводами полей продукта

## Обзор

Модуль `translate_product_fields.py` предназначен для управления переводами полей товара. Он обеспечивает связь между словарем полей товара, таблицей переводов и переводчиками. Модуль включает функции для получения переводов из базы данных PrestaShop, добавления новых переводов и перевода записей с использованием AI.

## Подробней

Этот модуль является важной частью процесса локализации продуктов в PrestaShop. Он использует класс `ProductTranslationsManager` для взаимодействия с базой данных переводов и функцию `translate` для выполнения фактического перевода полей.

## Функции

### `get_translations_from_presta_translations_table`

```python
def get_translations_from_presta_translations_table(product_reference: str, credentials: dict, i18n: str = None) -> list:
    """Функция возвращает словарь переводов полей товара."""
    ...
```

**Назначение**:
Извлекает переводы полей товара из таблицы переводов PrestaShop.

**Параметры**:
- `product_reference` (str): Уникальный идентификатор товара.
- `credentials` (dict): Параметры подключения к базе данных.
- `i18n` (str, optional): Язык перевода в формате `en_EN`, `he_HE`, `ru-RU`. По умолчанию `None`.

**Возвращает**:
- `list`: Список словарей, содержащих переводы полей товара.

**Как работает функция**:
1. Функция принимает референс товара, параметры подключения к базе данных переводов PrestaShop и желаемый язык перевода.
2. Использует класс `ProductTranslationsManager` для подключения к базе данных.
3. Формирует фильтр поиска по референсу товара.
4. Выполняет запрос к базе данных и возвращает результат в виде списка словарей.

**Примеры**:

```python
product_reference = 'REF123'
credentials = {'host': 'localhost', 'user': 'admin', 'password': 'password', 'database': 'prestashop'}
i18n = 'ru-RU'
translations = get_translations_from_presta_translations_table(product_reference, credentials, i18n)
if translations:
    print(f'Переводы для товара {product_reference}: {translations}')
else:
    print(f'Переводы для товара {product_reference} не найдены')
```

### `insert_new_translation_to_presta_translations_table`

```python
def insert_new_translation_to_presta_translations_table(record, credentials):
    """Функция вставляет новую запись перевода в таблицу переводов PrestaShop."""
    ...
```

**Назначение**:
Добавляет новую запись перевода в таблицу переводов PrestaShop.

**Параметры**:
- `record` (dict): Словарь с данными для вставки (поля и их переводы).
- `credentials` (dict): Параметры подключения к базе данных.

**Как работает функция**:
1. Функция принимает словарь с данными перевода и параметры подключения к базе данных.
2. Использует класс `ProductTranslationsManager` для подключения к базе данных.
3. Вызывает метод `insert_record` для добавления новой записи в таблицу переводов.

**Примеры**:

```python
record = {'product_reference': 'REF456', 'field1': 'Перевод поля 1', 'field2': 'Перевод поля 2'}
credentials = {'host': 'localhost', 'user': 'admin', 'password': 'password', 'database': 'prestashop'}
insert_new_translation_to_presta_translations_table(record, credentials)
print(f'Новый перевод для товара {record["product_reference"]} успешно добавлен')
```

### `translate_record`

```python
def translate_record(record: dict, from_locale: str, to_locale: str) -> dict:
    """Функция для перевода полей товара."""
    ...
```

**Назначение**:
Переводит поля товара с одного языка на другой.

**Параметры**:
- `record` (dict): Словарь с полями товара для перевода.
- `from_locale` (str): Исходный язык.
- `to_locale` (str): Целевой язык.

**Возвращает**:
- `dict`: Словарь с переведенными полями товара.

**Как работает функция**:
1. Функция принимает словарь с полями товара, исходный и целевой языки.
2. Вызывает функцию `translate` из модуля `src.ai` для выполнения перевода.
3. Обрабатывает переведенную запись.
4. Возвращает словарь с переведенными полями.

**Примеры**:

```python
record = {'name': 'Product Name', 'description': 'Product Description'}
from_locale = 'en'
to_locale = 'ru'
translated_record = translate_record(record, from_locale, to_locale)
print(f'Переведенная запись: {translated_record}')