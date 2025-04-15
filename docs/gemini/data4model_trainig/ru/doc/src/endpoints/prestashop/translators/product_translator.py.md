# Модуль `product_translator`

## Обзор

Модуль `product_translator.py` предназначен для управления переводами данных о товарах, извлеченных из PrestaShop. Он обеспечивает связь между словарем полей товара, таблицей переводов и инструментами перевода. Модуль предоставляет функции для получения, вставки и перевода записей о товарах.

## Подробней

Этот модуль служит центральным компонентом для обработки мультиязычного контента товаров в системе. Он обеспечивает возможность извлечения существующих переводов, добавления новых и автоматического перевода контента с использованием внешних сервисов, таких как OpenAI. Это позволяет поддерживать актуальность и согласованность информации о товарах на разных языках.

## Функции

### `get_translations_from_presta_translations_table`

```python
def get_translations_from_presta_translations_table(product_reference: str, i18n: str = None) -> list:
    """Функция возвращает словарь переводов полей товара."""
    ...
```

**Назначение**:
Извлекает переводы полей товара из таблицы переводов PrestaShop на основе предоставленного артикула товара.

**Параметры**:
- `product_reference` (str): Артикул товара, для которого требуется получить переводы.
- `i18n` (str, optional): Локаль перевода (например, 'en_US', 'ru_RU'). По умолчанию `None`.

**Возвращает**:
- `list`: Список словарей, содержащих переводы для указанного артикула товара.

**Как работает функция**:
1. Использует менеджер `ProductTranslationsManager` для взаимодействия с базой данных.
2. Формирует фильтр поиска по артикулу товара.
3. Извлекает записи, соответствующие фильтру, из таблицы переводов.
4. Возвращает список найденных переводов.

**Примеры**:
```python
product_reference = "12345"
translations = get_translations_from_presta_translations_table(product_reference)
if translations:
    print(f"Найдены переводы для товара {product_reference}: {translations}")
else:
    print(f"Переводы для товара {product_reference} не найдены")
```

### `insert_new_translation_to_presta_translations_table`

```python
def insert_new_translation_to_presta_translations_table(record):
    """Функция для вставки новой записи перевода товара."""
    ...
```

**Назначение**:
Вставляет новую запись перевода товара в таблицу переводов PrestaShop.

**Параметры**:
- `record` (dict): Словарь, содержащий данные для вставки в таблицу переводов.

**Как работает функция**:
1. Использует менеджер `ProductTranslationsManager` для взаимодействия с базой данных.
2. Вставляет предоставленную запись в таблицу переводов.

**Примеры**:
```python
new_translation = {
    "product_reference": "67890",
    "locale": "fr_FR",
    "name": "Nouveau Produit"
}
insert_new_translation_to_presta_translations_table(new_translation)
print(f"Новый перевод для товара {new_translation['product_reference']} добавлен")
```

### `translate_record`

```python
def translate_record(record: dict, from_locale: str, to_locale: str) -> dict:
    """Функция для перевода полей товара."""
    ...
```

**Назначение**:
Переводит поля товара с одного языка на другой с использованием внешнего сервиса перевода.

**Параметры**:
- `record` (dict): Словарь, содержащий поля товара для перевода.
- `from_locale` (str): Локаль исходного языка (например, 'en_US').
- `to_locale` (str): Локаль целевого языка (например, 'ru_RU').

**Возвращает**:
- `dict`: Словарь с переведенными полями товара.

**Как работает функция**:
1. Вызывает функцию `translate` из модуля `src.ai.openai` для выполнения перевода.
2. <Добавить обработку переведенной записи>
3. Возвращает словарь с переведенными данными.

**Примеры**:
```python
product_data = {
    "name": "Новый продукт",
    "description": "Описание продукта"
}
from_locale = "ru_RU"
to_locale = "en_US"
translated_data = translate_record(product_data, from_locale, to_locale)
print(f"Переведенные данные: {translated_data}")