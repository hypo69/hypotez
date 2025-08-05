# Модуль управления переводами

## Обзор

Модуль `src/endpoints/prestashop/translators/translate_product_fields.py` предоставляет функции для управления переводами полей товара в PrestaShop.

## Детали

Модуль содержит функции для получения переводов из таблицы переводов PrestaShop, вставки новых переводов в таблицу и перевода полей товара с помощью моделей ИИ.

## Функции

### `get_translations_from_presta_translations_table(product_reference: str, credentials: dict, i18n: str = None) -> list`

**Назначение**: Функция извлекает переводы полей товара из таблицы переводов PrestaShop.

**Параметры**:

- `product_reference` (str): Референс товара.
- `credentials` (dict): Параметры подключения к базе переводов PrestaShop.
- `i18n` (str, optional): Язык перевода в формате en_EN, he_HE, ru-RU. По умолчанию `None`.

**Возвращает**:

- `list`: Список переводов полей товара.

**Пример**:

```python
from src.endpoints.PrestaShop import PrestaShop
from src.translators import get_translations_from_presta_translations_table

credentials = {'host': 'localhost', 'user': 'root', 'password': '', 'database': 'prestashop'}
translations = get_translations_from_presta_translations_table('product_reference', credentials, i18n='ru-RU')
print(translations)
```

### `insert_new_translation_to_presta_translations_table(record, credentials)`

**Назначение**: Функция вставляет новую запись перевода в таблицу переводов PrestaShop.

**Параметры**:

- `record`: Запись перевода, которую нужно вставить.
- `credentials` (dict): Параметры подключения к базе переводов PrestaShop.

**Возвращает**:

- `None`: Не возвращает значение.

**Пример**:

```python
from src.endpoints.PrestaShop import PrestaShop
from src.translators import insert_new_translation_to_presta_translations_table

credentials = {'host': 'localhost', 'user': 'root', 'password': '', 'database': 'prestashop'}
record = {'product_reference': 'product_reference', 'field_name': 'name', 'lang_iso': 'ru-RU', 'translation': 'Название товара'}
insert_new_translation_to_presta_translations_table(record, credentials)
```

### `translate_record(record: dict, from_locale: str, to_locale: str) -> dict`

**Назначение**: Функция переводит поля товара с использованием модели ИИ.

**Параметры**:

- `record` (dict): Словарь полей товара.
- `from_locale` (str): Исходный язык перевода.
- `to_locale` (str): Целевой язык перевода.

**Возвращает**:

- `dict`: Переведенный словарь полей товара.

**Пример**:

```python
from src.translators import translate_record

record = {'name': 'Product Name', 'description': 'Product Description'}
translated_record = translate_record(record, 'en_EN', 'ru-RU')
print(translated_record)
```