# Модуль управления переводами

## Обзор

Модуль `product_translator` реализует слой связи между словарем полей товара, таблицей переводов и переводчиками. 
Он предоставляет функции для получения переводов из базы данных PrestaShop, вставки новых переводов и перевода 
полей товара с использованием модели OpenAI для машинного перевода.

## Подробней

Данный модуль взаимодействует с базой данных PrestaShop для получения и записи данных о переводах полей товара. 
Он использует модуль `src.db.ProductTranslationsManager` для работы с таблицей переводов. 
Для перевода текста используется модуль `src.llm.openai.translate`, который использует модель OpenAI для машинного перевода.

## Классы

### `ProductTranslationsManager`

**Описание**: Класс для работы с таблицей переводов товаров в базе данных PrestaShop.

**Наследует**: 
    - `src.db.DBManager`

**Атрибуты**:
    - `connection`:  Объект соединения с базой данных.

**Методы**:
    - `select_record(**kwargs)`: Выборка записей из таблицы переводов, используя фильтры.
    - `insert_record(record: dict)`: Вставка новой записи о переводе в таблицу переводов.


## Функции

### `get_translations_from_presta_translations_table`

**Назначение**: Функция извлекает записи о переводах из базы данных PrestaShop, используя информацию о референсе товара и языке. 

**Параметры**:
    - `product_reference` (str):  Референс товара.
    - `i18n` (str, optional): Язык перевода. По умолчанию None.

**Возвращает**:
    - `list`: Список словарей с данными о переводах. 

**Примеры**:

```python
from src.translators.product_translator import get_translations_from_presta_translations_table

# Получение переводов для товара с референсом "123456789" 
translations = get_translations_from_presta_translations_table('123456789', 'ru-RU')
print(translations)
```


### `insert_new_translation_to_presta_translations_table`

**Назначение**: Функция вставляет новую запись о переводе в таблицу переводов в базе данных PrestaShop.

**Параметры**:
    - `record` (dict): Словарь с данными о переводе.

**Примеры**:

```python
from src.translators.product_translator import insert_new_translation_to_presta_translations_table

# Словарь с данными о переводе
record = {
    'product_reference': '123456789',
    'locale': 'ru-RU',
    'name': 'Название товара на русском',
    # ... другие поля
}

insert_new_translation_to_presta_translations_table(record)
```


### `translate_record`

**Назначение**: Функция переводит поля товара с помощью модели машинного перевода OpenAI.

**Параметры**:
    - `record` (dict): Словарь с данными о переводе.
    - `from_locale` (str): Язык исходного текста.
    - `to_locale` (str): Язык перевода.

**Возвращает**:
    - `dict`: Переведенный словарь с данными о переводе. 

**Примеры**:

```python
from src.translators.product_translator import translate_record

# Словарь с данными о переводе
record = {
    'product_reference': '123456789',
    'locale': 'en-US',
    'name': 'Product name in English',
    # ... другие поля
}

# Перевод на русский язык
translated_record = translate_record(record, 'en-US', 'ru-RU')
print(translated_record)
```

```python
# # def record(presta_fields:Dict, i18n:str = None, i:int = 0) -> Dict:
# #     """ Вытаскивает из словаря полей престашоп 
# #     `dict_product_fields` значения мультиязычных полей 
# #     @param dict_product_fields престашоп словарь полей товара
# #     @param i18n Локаль: en-US, ru-RU, he-IL
# #     @param i индекс языка в мультиязычных полях
# #     """
# #     ...
# #     i18n = i18n if i18n else presta_fields.get(\'locale\')
# #     if not i18n:
# #         text = presta_fields.language[0][\'value\']
# #         i18n = detect(text)
# #         ...
# #     i = 0 # <- Вытаскивает первый из списка языков в мультиязычных полях
    
# #     # словарь record со всеми ключами
# #     record = {
# #     \'product_reference\': presta_fields.get(\'reference\'),
# #     \'locale\': i18n,
# #     \'name\': presta_fields.get(\'name\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'description\': presta_fields.get(\'description\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'description_short\': presta_fields.get(\'description_short\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'link_rewrite\': presta_fields.get(\'link_rewrite\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'meta_description\': presta_fields.get(\'meta_description\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'meta_keywords\': presta_fields.get(\'meta_keywords\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'meta_title\': presta_fields.get(\'meta_title\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'available_now\': presta_fields.get(\'available_now\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'available_later\': presta_fields.get(\'available_later\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'delivery_in_stock\': presta_fields.get(\'delivery_in_stock\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'delivery_out_stock\': presta_fields.get(\'delivery_out_stock\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'delivery_additional_message\': presta_fields.get(\'delivery_additional_message\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'affiliate_short_link\': presta_fields.get(\'affiliate_short_link\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'affiliate_text\': presta_fields.get(\'affiliate_text\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'affiliate_summary\': presta_fields.get(\'affiliate_summary\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'affiliate_summary_2\': presta_fields.get(\'affiliate_summary_2\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'affiliate_image_small\': presta_fields.get(\'affiliate_image_small\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'affiliate_image_medium\': presta_fields.get(\'affiliate_image_medium\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'affiliate_image_large\': presta_fields.get(\'affiliate_image_large\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'ingredients\': presta_fields.get(\'ingredients\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'how_to_use\': presta_fields.get(\'how_to_use\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     \'specification\': presta_fields.get(\'specification\', {\'language\': [{\'value\': \'\'}]}).get(\'language\', [{}])[i].get(\'value\', \'\'),
# #     }\n#     return  record