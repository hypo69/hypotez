# Модуль для перевода полей товара

## Обзор

Модуль `translate_product_fields.py` предназначен для управления переводами полей товара, обеспечивая связь между словарем полей товара, таблицей переводов и переводчиками. Он включает в себя функции для получения, вставки и выполнения перевода записей о товарах.

## Подробней

Модуль содержит функции для работы с переводами, такие как получение существующих переводов из базы данных, вставка новых переводов и перевод содержимого записей о товарах с использованием внешних сервисов перевода.
Модуль использует класс `ProductTranslationsManager` для взаимодействия с базой данных и класс `translate` из `src.llm` для выполнения переводов.

## Функции

### `get_translations_from_presta_translations_table`

```python
def get_translations_from_presta_translations_table(product_reference: str, credentials: dict, i18n: str = None) -> list:
    """Функция возвращает словарь переводов полей товара."""
    with ProductTranslationsManager(credentials) as translations_manager:
        search_filter = {'product_reference': product_reference}
        product_translations = translations_manager.select_record(**search_filter)
    return product_translations
```

**Назначение**:
Функция извлекает переводы полей товара из таблицы переводов PrestaShop на основе предоставленного референса товара и учетных данных для доступа к базе данных.

**Параметры**:
- `product_reference` (str): Уникальный идентификатор товара, для которого требуется получить переводы.
- `credentials` (dict): Словарь, содержащий учетные данные для подключения к базе данных, где хранятся переводы.
- `i18n` (str, optional): Языковой код перевода (например, 'en_EN', 'he_HE', 'ru-RU'). По умолчанию `None`.

**Возвращает**:
- `list`: Список, содержащий записи переводов полей товара, найденные в базе данных.

**Как работает функция**:
1. Функция принимает референс товара, учетные данные для подключения к базе данных и, опционально, языковой код.
2. Использует менеджер контекста `ProductTranslationsManager` для автоматического управления подключением к базе данных.
3. Формирует фильтр поиска по референсу товара.
4. Выполняет запрос к базе данных через метод `select_record` менеджера переводов.
5. Возвращает список найденных переводов.

**Примеры**:
```python
# Пример вызова функции
product_reference = "12345"
credentials = {
    'host': 'localhost',
    'user': 'user',
    'password': 'password',
    'database': 'prestashop_db'
}
translations = get_translations_from_presta_translations_table(product_reference, credentials, i18n='ru-RU')
print(translations)
```

### `insert_new_translation_to_presta_translations_table`

```python
def insert_new_translation_to_presta_translations_table(record, credentials):
    """Функция возвращает словарь переводов полей товара."""
    with ProductTranslationsManager(credentials) as translations_manager:
        translations_manager.insert_record(record)
```

**Назначение**:
Функция добавляет новую запись перевода в таблицу переводов PrestaShop.

**Параметры**:
- `record` (dict): Словарь, представляющий запись перевода, которую необходимо добавить в базу данных.
- `credentials` (dict): Словарь, содержащий учетные данные для подключения к базе данных.

**Как работает функция**:
1. Функция принимает запись перевода и учетные данные для подключения к базе данных.
2. Использует менеджер контекста `ProductTranslationsManager` для автоматического управления подключением к базе данных.
3. Выполняет вставку записи в базу данных через метод `insert_record` менеджера переводов.

**Примеры**:
```python
# Пример вызова функции
record = {
    'product_reference': '12345',
    'field_name': 'name',
    'lang': 'ru-RU',
    'translation': 'Новое название товара'
}
credentials = {
    'host': 'localhost',
    'user': 'user',
    'password': 'password',
    'database': 'prestashop_db'
}
insert_new_translation_to_presta_translations_table(record, credentials)
```

### `translate_record`

```python
def translate_record(record: dict, from_locale: str, to_locale: str) -> dict:
    """Функция для перевода полей товара."""
    translated_record = translate(record, from_locale, to_locale)
    ... # Добавить обработку переведенной записи
    return translated_record
```

**Назначение**:
Функция переводит поля товара из одного языка на другой с использованием внешнего сервиса перевода.

**Параметры**:
- `record` (dict): Словарь, содержащий поля товара для перевода.
- `from_locale` (str): Языковой код исходного языка (например, 'en_EN').
- `to_locale` (str): Языковой код целевого языка (например, 'ru-RU').

**Возвращает**:
- `dict`: Словарь с переведенными полями товара.

**Как работает функция**:
1. Функция принимает запись о товаре, языковой код исходного языка и языковой код целевого языка.
2. Вызывает функцию `translate` из модуля `src.llm` для выполнения перевода.
3. Возвращает словарь с переведенными полями.

**Примеры**:
```python
# Пример вызова функции
record = {
    'name': 'Product Name',
    'description': 'Product Description'
}
from_locale = 'en'
to_locale = 'ru'
translated_record = translate_record(record, from_locale, to_locale)
print(translated_record)