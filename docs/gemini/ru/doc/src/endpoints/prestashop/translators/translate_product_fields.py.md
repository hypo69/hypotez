# Модуль управления переводами

## Обзор

Модуль `translate_product_fields.py` обеспечивает связь между словарем полей товара, таблицей переводов в PrestaShop и переводчиками. Он предоставляет функции для получения переводов из базы данных PrestaShop, добавления новых переводов, а также для перевода полей товара с использованием моделей машинного перевода.

## Функции

### `get_translations_from_presta_translations_table`

**Назначение**: Извлекает переводы полей товара из таблицы переводов в базе данных PrestaShop.

**Параметры**:

- `product_reference` (str):  Референс товара (например, SKU).
- `credentials` (dict): Словарь с параметрами подключения к базе данных PrestaShop.
- `i18n` (str, optional): Код языка перевода в формате en_EN, he_HE, ru-RU. По умолчанию `None`.

**Возвращает**:

- list: Список словарей, содержащих переводы полей товара.

**Как работает функция**:

1. Функция принимает референс товара, параметры подключения к базе данных PrestaShop и код языка.
2. Создается фильтр для поиска полей товара по референсу товара.
3. Используется менеджер `ProductTranslationsManager` для выборки переводов из таблицы переводов с использованием созданного фильтра.
4. Результат выборки (список словарей переводов) возвращается.

**Примеры**:

```python
>>> credentials = {'host': 'localhost', 'database': 'prestashop', 'user': 'root', 'password': 'password'}
>>> product_reference = '123456789'
>>> translations = get_translations_from_presta_translations_table(product_reference, credentials, i18n='ru-RU')
>>> pprint(translations)
[
    {
        'product_reference': '123456789',
        'id_lang': 1,
        'field_name': 'name',
        'translation': 'Название товара на русском языке'
    },
    {
        'product_reference': '123456789',
        'id_lang': 1,
        'field_name': 'description',
        'translation': 'Описание товара на русском языке'
    }
]
```

### `insert_new_translation_to_presta_translations_table`

**Назначение**: Добавляет новые переводы в таблицу переводов в базе данных PrestaShop.

**Параметры**:

- `record` (dict): Словарь, содержащий данные о переводе.
- `credentials` (dict): Словарь с параметрами подключения к базе данных PrestaShop.

**Возвращает**:

- None: Функция не возвращает значение.

**Как работает функция**:

1. Функция принимает словарь с данными о переводе и параметры подключения к базе данных PrestaShop.
2. Используется менеджер `ProductTranslationsManager` для добавления новой записи в таблицу переводов.

**Пример**:

```python
>>> credentials = {'host': 'localhost', 'database': 'prestashop', 'user': 'root', 'password': 'password'}
>>> new_translation = {'product_reference': '123456789', 'id_lang': 1, 'field_name': 'name', 'translation': 'New product name'}
>>> insert_new_translation_to_presta_translations_table(new_translation, credentials)
```

### `translate_record`

**Назначение**: Переводит поля товара с использованием модели машинного перевода.

**Параметры**:

- `record` (dict): Словарь с данными о полях товара.
- `from_locale` (str): Код языка исходного текста.
- `to_locale` (str): Код языка, на который нужно перевести.

**Возвращает**:

- dict: Словарь с переведенными полями товара.

**Как работает функция**:

1. Функция принимает словарь с данными о полях товара, код языка исходного текста и код языка, на который нужно перевести.
2. Использует функцию `translate` из модуля `src.llm` для перевода всех полей товара.
3. Обрабатывает переведенные записи (например, сохраняет их в базе данных).
4. Возвращает словарь с переведенными полями товара.

**Пример**:

```python
>>> record = {'name': 'Product name', 'description': 'Product description'}
>>> from_locale = 'en_EN'
>>> to_locale = 'ru-RU'
>>> translated_record = translate_record(record, from_locale, to_locale)
>>> pprint(translated_record)
{
    'name': 'Название товара',
    'description': 'Описание товара'
}
```

## Дополнительные сведения

- В функции `translate_record` нужно добавить обработку переведенной записи (например, сохранение в базе данных).
- Для перевода полей товара используйте функцию `translate` из модуля `src.llm`, которая использует модель машинного перевода.
- Для работы с базой данных PrestaShop используйте менеджер `ProductTranslationsManager` из модуля `src.db`.
- Для вывода данных на консоль используйте функцию `pprint` из модуля `src.utils.printer`.