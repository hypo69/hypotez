### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Этот блок кода содержит функции для получения, добавления и перевода данных о товарах, используя базу данных переводов PrestaShop и инструменты машинного перевода. Он включает в себя функции для извлечения переводов из базы данных, добавления новых переводов и выполнения машинного перевода записей.

Шаги выполнения
-------------------------
1. **Получение переводов товара:**
   - Функция `get_translations_from_presta_translations_table` извлекает переводы для товара из таблицы переводов PrestaShop на основе `product_reference`.
   - Создается экземпляр класса `ProductTranslationsManager` для управления соединениями с базой данных.
   - Формируется фильтр поиска `search_filter` для запроса к базе данных с использованием `product_reference`.
   - Функция `select_record` вызывается для получения записей, соответствующих фильтру.
   - Полученные переводы возвращаются в виде списка.

2. **Добавление нового перевода товара:**
   - Функция `insert_new_translation_to_presta_translations_table` добавляет новую запись перевода в таблицу переводов PrestaShop.
   - Создается экземпляр класса `ProductTranslationsManager` для управления соединениями с базой данных.
   - Функция `insert_record` вызывается для вставки записи `record` в таблицу.

3. **Перевод записи товара:**
   - Функция `translate_record` переводит запись товара `record` с одного языка (`from_locale`) на другой (`to_locale`).
   - Вызывается функция `translate` для выполнения машинного перевода записи.
   - **TODO**: Добавляется обработка переведенной записи (в текущей версии кода отсутствует).
   - Переведенная запись возвращается.

Пример использования
-------------------------

```python
from src.endpoints.prestashop.translators.product_translator import (
    get_translations_from_presta_translations_table,
    insert_new_translation_to_presta_translations_table,
    translate_record,
)

# Пример получения переводов товара
product_reference = "PRODUCT123"
translations = get_translations_from_presta_translations_table(product_reference)
if translations:
    print(f"Найдены переводы: {translations}")
else:
    print("Переводы не найдены.")

# Пример добавления нового перевода товара
new_record = {
    "product_reference": "PRODUCT456",
    "locale": "fr-FR",
    "name": "Nouveau Produit",
    "description": "Description du nouveau produit"
}
insert_new_translation_to_presta_translations_table(new_record)
print("Новый перевод добавлен.")

# Пример перевода записи товара
record_to_translate = {
    "name": "New Product",
    "description": "Description of the new product"
}
from_locale = "en-US"
to_locale = "ru-RU"
translated_record = translate_record(record_to_translate, from_locale, to_locale)
print(f"Переведенная запись: {translated_record}")