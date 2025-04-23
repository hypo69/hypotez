### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предоставляет набор функций для работы с переводами полей товара, предназначенных для использования с PrestaShop. Он включает в себя извлечение существующих переводов из базы данных, вставку новых переводов и перевод записей с одного языка на другой с использованием LLM.

Шаги выполнения
-------------------------
1. **Извлечение переводов из таблицы PrestaShop**:
   - Функция `get_translations_from_presta_translations_table` принимает референс товара (`product_reference`), учетные данные для подключения к базе данных (`credentials`) и код языка (`i18n`).
   - Она использует `ProductTranslationsManager` для подключения к базе данных и выполняет запрос для получения переводов продукта на основе `product_reference`.
   - Возвращает список найденных переводов.

2. **Вставка нового перевода в таблицу PrestaShop**:
   - Функция `insert_new_translation_to_presta_translations_table` принимает запись (`record`) с данными для вставки и учетные данные для подключения к базе данных (`credentials`).
   - Она использует `ProductTranslationsManager` для подключения к базе данных и выполняет операцию вставки записи (`record`) в таблицу переводов.

3. **Перевод записи**:
   - Функция `translate_record` принимает запись (`record`) для перевода, исходный язык (`from_locale`) и целевой язык (`to_locale`).
   - Она вызывает функцию `translate` (из модуля `src.llm`) для выполнения перевода записи с одного языка на другой.
   - Возвращает переведенную запись.

Пример использования
-------------------------

```python
from src.endpoints.prestashop.translators.translate_product_fields import (
    get_translations_from_presta_translations_table,
    insert_new_translation_to_presta_translations_table,
    translate_record
)

# Пример использования get_translations_from_presta_translations_table
product_reference = "REF123"
credentials = {
    "host": "localhost",
    "user": "user",
    "password": "password",
    "database": "prestashop_db"
}
i18n = "ru-RU"
translations = get_translations_from_presta_translations_table(product_reference, credentials, i18n)
if translations:
    print(f"Найдены переводы: {translations}")
else:
    print("Переводы не найдены.")

# Пример использования insert_new_translation_to_presta_translations_table
new_record = {
    "product_reference": "REF456",
    "field_name": "description",
    "locale": "en-US",
    "translation": "New description"
}
insert_new_translation_to_presta_translations_table(new_record, credentials)
print("Новый перевод добавлен.")

# Пример использования translate_record
record_to_translate = {
    "name": "Product Name",
    "description": "Product Description"
}
from_locale = "en"
to_locale = "fr"
translated_record = translate_record(record_to_translate, from_locale, to_locale)
print(f"Переведенная запись: {translated_record}")