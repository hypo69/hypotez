# Модуль `product_translator`

## Обзор

Модуль `product_translator` предназначен для управления переводами данных о товарах. Он обеспечивает связь между словарем полей товара, таблицей переводов и сервисами перевода. Модуль позволяет извлекать, добавлять и переводить записи о товарах, используя базу данных переводов PrestaShop и сервисы машинного перевода.

## Подробней

Модуль предоставляет функции для работы с переводами товаров, такие как получение переводов из базы данных PrestaShop, добавление новых переводов и перевод существующих записей. Он использует класс `ProductTranslationsManager` для взаимодействия с базой данных и функцию `translate` для выполнения машинного перевода.

## Функции

### `get_translations_from_presta_translations_table`

```python
def get_translations_from_presta_translations_table(product_reference: str, i18n: str = None) -> list:
    """Функция возвращает словарь переводов полей товара."""
```

**Назначение**:
Функция извлекает переводы полей товара из таблицы переводов PrestaShop на основе reference товара.

**Параметры**:
- `product_reference` (str): Уникальный идентификатор товара, для которого требуется получить переводы.
- `i18n` (str, optional): Локаль перевода. По умолчанию `None`.

**Возвращает**:
- `list`: Список словарей, содержащих переводы полей товара.

**Как работает функция**:
1. Функция создает экземпляр класса `ProductTranslationsManager` для управления базой данных переводов.
2. Определяет фильтр поиска по reference товара.
3. Выполняет запрос к базе данных для получения записи о товаре с указанным reference.
4. Возвращает полученный список переводов.

**Примеры**:

```python
product_reference = "12345"
translations = get_translations_from_presta_translations_table(product_reference)
if translations:
    print(f"Найдено {len(translations)} переводов для товара {product_reference}")
else:
    print(f"Переводы для товара {product_reference} не найдены")
```

### `insert_new_translation_to_presta_translations_table`

```python
def insert_new_translation_to_presta_translations_table(record):
    """Функция добавления нового перевода в таблицу переводов PrestaShop."""
```

**Назначение**:
Функция добавляет новую запись перевода в таблицу переводов PrestaShop.

**Параметры**:
- `record` (dict): Словарь, содержащий данные для новой записи перевода.

**Как работает функция**:
1. Функция создает экземпляр класса `ProductTranslationsManager` для управления базой данных переводов.
2. Выполняет операцию вставки записи в таблицу переводов, используя предоставленные данные.

**Примеры**:

```python
new_translation = {
    "product_reference": "67890",
    "locale": "fr-FR",
    "name": "Nouveau Produit",
    "description": "Description du nouveau produit"
}
insert_new_translation_to_presta_translations_table(new_translation)
print("Новый перевод добавлен в базу данных")
```

### `translate_record`

```python
def translate_record(record: dict, from_locale: str, to_locale: str) -> dict:
    """Функция для перевода полей товара."""
```

**Назначение**:
Функция переводит поля товара с одного языка на другой, используя машинный перевод.

**Параметры**:
- `record` (dict): Словарь, содержащий данные о товаре для перевода.
- `from_locale` (str): Локаль исходного языка.
- `to_locale` (str): Локаль целевого языка.

**Возвращает**:
- `dict`: Словарь с переведенными данными о товаре.

**Как работает функция**:
1. Функция вызывает функцию `translate` из модуля `src.llm.openai` для выполнения машинного перевода записи.
2. <добавить обработку переведенной записи>.
3. Возвращает словарь с переведенными данными.

**Примеры**:

```python
record_to_translate = {
    "product_reference": "13579",
    "name": "Original Product Name",
    "description": "Original product description"
}
from_locale = "en-US"
to_locale = "ru-RU"
translated_record = translate_record(record_to_translate, from_locale, to_locale)
print("Запись переведена")
print(translated_record)