## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предоставляет функции для получения, добавления и перевода записей в таблице переводов продуктов PrestaShop.

Шаги выполнения
-------------------------
1. **Получение переводов:**  
    - `get_translations_from_presta_translations_table(product_reference, credentials, i18n)` извлекает переводы полей товара из таблицы переводов PrestaShop.
    - Функция принимает референс товара (`product_reference`), параметры подключения к базе (`credentials`) и язык перевода (`i18n`).
    - Она создает запрос для выборки данных и возвращает список найденных записей.
2. **Добавление нового перевода:**
    - `insert_new_translation_to_presta_translations_table(record, credentials)` вставляет новую запись перевода в таблицу переводов PrestaShop.
    - Функция принимает словарь записи перевода (`record`) и параметры подключения к базе (`credentials`).
    - Она использует объект `ProductTranslationsManager` для выполнения операции вставки.
3. **Перевод записи:**
    - `translate_record(record, from_locale, to_locale)` переводит поля товара с помощью модели LLM (Large Language Model).
    - Функция принимает словарь с полями товара (`record`), исходный язык (`from_locale`) и целевой язык (`to_locale`).
    - Она использует функцию `translate` из модуля `src.llm` для выполнения перевода.
    - После перевода запись должна быть обработана (необходимая обработка не указана).
    - Возвращает переведенную запись.

Пример использования
-------------------------

```python
from src.endpoints.PrestaShop import PrestaShop
from src.product.product_fields.product_fields import record
from src.db import ProductTranslationsManager

# Получение настроек подключения к PrestaShop
credentials = PrestaShop.get_credentials()

# Получение референса товара
product_reference = "12345"

# Получение переводов
translations = get_translations_from_presta_translations_table(product_reference, credentials, i18n="ru-RU")

# Вывод полученных переводов
print(translations)

# Создание новой записи для перевода
new_translation = {
    'product_reference': product_reference,
    'field_name': 'Название',
    'field_value': 'Название товара на русском',
    'locale': 'ru-RU'
}

# Добавление новой записи в таблицу переводов
insert_new_translation_to_presta_translations_table(new_translation, credentials)

# Перевод записи товара с английского на русский
record = {
    'Название': 'Product Name',
    'Описание': 'Product description'
}
translated_record = translate_record(record, from_locale='en_EN', to_locale='ru-RU')

# Вывод переведенной записи
print(translated_record)
```

### **Дополнительно:**

- Модуль `src.llm` предоставляет функции для перевода с помощью моделей LLM.
- Модуль `src.db` обеспечивает доступ к менеджеру таблицы переводов `ProductTranslationsManager`, который позволяет работать с данными в таблице.
- Модуль `src.product.product_fields.product_fields` предоставляет структуру `record` для хранения полей товара.

**Важно:** Не забывайте заменять примеры значений (`product_reference`, `credentials` и т.д.) на ваши реальные данные.