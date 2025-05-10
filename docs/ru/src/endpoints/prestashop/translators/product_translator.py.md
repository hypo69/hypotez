# Модуль `product_translator`

## Обзор

Модуль `product_translator` предназначен для управления переводами данных о товарах, получаемых из PrestaShop. Он обеспечивает связь между словарем полей товара, таблицей переводов и инструментами для перевода.

## Подробней

Модуль предоставляет функции для получения, добавления и перевода записей, связанных с переводами товаров. Он использует класс `ProductTranslationsManager` для взаимодействия с базой данных и модуль `src.llm.openai.translate` для выполнения фактического перевода текста.

## Функции

### `get_translations_from_presta_translations_table`

```python
def get_translations_from_presta_translations_table(product_reference: str, i18n: str = None) -> list:
    """Функция возвращает словарь переводов полей товара.

    Args:
        product_reference (str): Артикул товара, для которого требуется получить переводы.
        i18n (str, optional): Локаль перевода. По умолчанию `None`.

    Returns:
        list: Список записей с переводами полей товара.
    """
```

**Назначение**: Функция извлекает переводы полей товара из таблицы переводов PrestaShop на основе артикула товара.

**Параметры**:
- `product_reference` (str): Артикул товара, для которого требуется получить переводы.
- `i18n` (str, optional): Локаль перевода. По умолчанию `None`.

**Возвращает**:
- `list`: Список записей с переводами полей товара.

**Как работает функция**:
1. Создает экземпляр класса `ProductTranslationsManager` для управления соединениями с базой данных.
2. Формирует фильтр поиска по артикулу товара.
3. Вызывает метод `select_record` для получения записей из базы данных на основе заданного фильтра.
4. Возвращает полученный список записей.

**Примеры**:

```python
from src.endpoints.prestashop.translators.product_translator import get_translations_from_presta_translations_table

product_reference = "PRODUCT123"
translations = get_translations_from_presta_translations_table(product_reference)
print(translations)  # Вывод: [{'product_reference': 'PRODUCT123', 'locale': 'ru-RU', 'name': 'Товар 123', ...}, ...]
```

### `insert_new_translation_to_presta_translations_table`

```python
def insert_new_translation_to_presta_translations_table(record: dict) -> None:
    """Функция для добавления новой записи перевода в таблицу переводов.

    Args:
        record (dict): Словарь, содержащий данные для вставки в таблицу переводов.
    """
```

**Назначение**: Функция добавляет новую запись перевода в таблицу переводов PrestaShop.

**Параметры**:
- `record` (dict): Словарь, содержащий данные для вставки в таблицу переводов.

**Как работает функция**:
1. Создает экземпляр класса `ProductTranslationsManager` для управления соединениями с базой данных.
2. Вызывает метод `insert_record` для вставки записи в базу данных.

**Примеры**:

```python
from src.endpoints.prestashop.translators.product_translator import insert_new_translation_to_presta_translations_table

record = {'product_reference': 'PRODUCT456', 'locale': 'en-US', 'name': 'Product 456'}
insert_new_translation_to_presta_translations_table(record)
```

### `translate_record`

```python
def translate_record(record: dict, from_locale: str, to_locale: str) -> dict:
    """Функция для перевода полей товара.

    Args:
        record (dict): Словарь с данными для перевода.
        from_locale (str): Исходная локаль перевода.
        to_locale (str): Целевая локаль перевода.

    Returns:
        dict: Словарь с переведенными данными.
    """
```

**Назначение**: Функция переводит поля товара с одной локали на другую, используя модуль `src.llm.openai.translate`.

**Параметры**:
- `record` (dict): Словарь с данными для перевода.
- `from_locale` (str): Исходная локаль перевода.
- `to_locale` (str): Целевая локаль перевода.

**Возвращает**:
- `dict`: Словарь с переведенными данными.

**Как работает функция**:
1. Вызывает функцию `translate` из модуля `src.llm.openai` для выполнения перевода.
2.  Добавляет обработку переведенной записи <добавить обработку переведенной записи>.
3. Возвращает словарь с переведенными данными.

**Примеры**:

```python
from src.endpoints.prestashop.translators.product_translator import translate_record

record = {'name': 'Product 789', 'description': 'Описание товара 789'}
from_locale = 'ru-RU'
to_locale = 'en-US'
translated_record = translate_record(record, from_locale, to_locale)
print(translated_record)  # Вывод: {'name': 'Product 789', 'description': 'Product Description 789'}
```