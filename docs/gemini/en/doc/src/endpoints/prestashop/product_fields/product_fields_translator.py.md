# Модуль перевода полей товара на языки клиентской базы данных
===============================================================

Модуль перевода полей товара на языки клиентской базы данных. 

## Table of Contents

- [Функция `rearrange_language_keys`](#функция-rearrange_language_keys)
- [Функция `translate_presta_fields_dict`](#функция-translate_presta_fields_dict)

## Функция `rearrange_language_keys`

### Purpose: 
Обновляет идентификатор языка в словаре `presta_fields_dict` на соответствующий идентификатор из схемы клиентских языков при совпадении языка страницы.

### Parameters:
- `presta_fields_dict` (dict): Словарь полей товара.
- `client_langs_schema` (list | dict): Схема языков клиента.
- `page_lang` (str): Язык страницы.

### Returns:
- `dict`: Обновленный словарь `presta_fields_dict`.

### How the Function Works:
- Функция ищет соответствующий идентификатор языка в схеме клиентских языков, сравнивая язык страницы с `locale`, `iso_code` и `language_code`.
- Если идентификатор найден, функция обновляет значение атрибута `id` в словаре `presta_fields_dict` для всех полей, которые являются словарями и содержат ключ `language`.

### Examples:
```python
>>> from src.product.product_fields.product_fields_translator import rearrange_language_keys
>>> presta_fields_dict = {'name': {'language': [{'attrs': {'id': '1'}, 'value': 'Product Name'}]}}
>>> client_langs_schema = [{'id': 2, 'locale': 'en-US', 'iso_code': 'en', 'language_code': 'en-us'}]
>>> page_lang = 'en-US'
>>> rearranged_dict = rearrange_language_keys(presta_fields_dict, client_langs_schema, page_lang)
>>> print(rearranged_dict)
{'name': {'language': [{'attrs': {'id': '2'}, 'value': 'Product Name'}]}}
```

## Функция `translate_presta_fields_dict`

### Purpose: 
Переводит мультиязычные поля товара в соответствии со схемой значений `id` языка в базе данных клиента. 

### Parameters:
- `presta_fields_dict` (dict): Словарь полей товара, собранный со страницы поставщика.
- `client_langs_schema` (list | dict): Схема языков клиента.
- `page_lang` (str): Язык страницы поставщика в коде en-US, ru-RU, he_HE.

### Returns:
- `dict`: Переведенный словарь полей товара.

### How the Function Works:
- Функция переупорядочивает ключи в таблице `presta_fields_dict` с использованием функции `rearrange_language_keys`.
- Извлекает переводы товара из таблицы переводов `presta_translations_table`.
- Если переводы не найдены, функция добавляет текущие переводы в таблицу переводов.
- Затем функция итеративно проходит по каждому языку клиента и записи перевода, и записывает перевод из таблицы в `presta_fields_dict`, если `iso_code` языка клиента присутствует в записи перевода. 
- Идентификаторы языка в переводах обязательно должны быть строками, что связано с парсером XML.

### Examples:
```python
>>> from src.product.product_fields.product_fields_translator import translate_presta_fields_dict
>>> presta_fields_dict = {'name': {'language': [{'attrs': {'id': '1'}, 'value': 'Product Name'}]}}
>>> client_langs_schema = [{'id': 2, 'locale': 'en-US', 'iso_code': 'en', 'language_code': 'en-us'}]
>>> page_lang = 'en-US'
>>> translated_dict = translate_presta_fields_dict(presta_fields_dict, client_langs_schema, page_lang)
>>> print(translated_dict)
{'name': {'language': [{'attrs': {'id': '2'}, 'value': 'Product Name'}]}}
```
```python
>>> from src.product.product_fields.product_fields_translator import translate_presta_fields_dict
>>> presta_fields_dict = {'name': {'language': [{'attrs': {'id': '1'}, 'value': 'Product Name'}]}, 'description': {'language': [{'attrs': {'id': '1'}, 'value': 'Product Description'}]}}
>>> client_langs_schema = [{'id': 2, 'locale': 'en-US', 'iso_code': 'en', 'language_code': 'en-us'}]
>>> page_lang = 'en-US'
>>> translated_dict = translate_presta_fields_dict(presta_fields_dict, client_langs_schema, page_lang)
>>> print(translated_dict)
{'name': {'language': [{'attrs': {'id': '2'}, 'value': 'Product Name'}]}, 'description': {'language': [{'attrs': {'id': '2'}, 'value': 'Product Description'}]}}
```

## Inner Functions:
- `rearrange_language_keys`: Обновляет идентификатор языка в словаре `presta_fields_dict` на соответствующий идентификатор из схемы клиентских языков при совпадении языка страницы.

## Parameter Details:
- `presta_fields_dict` (dict): Словарь полей товара.
- `client_langs_schema` (list | dict): Схема языков клиента.
- `page_lang` (str): Язык страницы.

## Examples:
- `rearrange_language_keys`: 
```python
>>> from src.product.product_fields.product_fields_translator import rearrange_language_keys
>>> presta_fields_dict = {'name': {'language': [{'attrs': {'id': '1'}, 'value': 'Product Name'}]}}
>>> client_langs_schema = [{'id': 2, 'locale': 'en-US', 'iso_code': 'en', 'language_code': 'en-us'}]
>>> page_lang = 'en-US'
>>> rearranged_dict = rearrange_language_keys(presta_fields_dict, client_langs_schema, page_lang)
>>> print(rearranged_dict)
{'name': {'language': [{'attrs': {'id': '2'}, 'value': 'Product Name'}]}}
```
- `translate_presta_fields_dict`: 
```python
>>> from src.product.product_fields.product_fields_translator import translate_presta_fields_dict
>>> presta_fields_dict = {'name': {'language': [{'attrs': {'id': '1'}, 'value': 'Product Name'}]}}
>>> client_langs_schema = [{'id': 2, 'locale': 'en-US', 'iso_code': 'en', 'language_code': 'en-us'}]
>>> page_lang = 'en-US'
>>> translated_dict = translate_presta_fields_dict(presta_fields_dict, client_langs_schema, page_lang)
>>> print(translated_dict)
{'name': {'language': [{'attrs': {'id': '2'}, 'value': 'Product Name'}]}}
```
```python
>>> from src.product.product_fields.product_fields_translator import translate_presta_fields_dict
>>> presta_fields_dict = {'name': {'language': [{'attrs': {'id': '1'}, 'value': 'Product Name'}]}, 'description': {'language': [{'attrs': {'id': '1'}, 'value': 'Product Description'}]}}
>>> client_langs_schema = [{'id': 2, 'locale': 'en-US', 'iso_code': 'en', 'language_code': 'en-us'}]
>>> page_lang = 'en-US'
>>> translated_dict = translate_presta_fields_dict(presta_fields_dict, client_langs_schema, page_lang)
>>> print(translated_dict)
{'name': {'language': [{'attrs': {'id': '2'}, 'value': 'Product Name'}]}, 'description': {'language': [{'attrs': {'id': '2'}, 'value': 'Product Description'}]}}
```
```python
>>> from src.product.product_fields.product_fields_translator import translate_presta_fields_dict
>>> presta_fields_dict = {'name': {'language': [{'attrs': {'id': '1'}, 'value': 'Product Name'}]}, 'description': {'language': [{'attrs': {'id': '1'}, 'value': 'Product Description'}]}, 'short_description': {'language': [{'attrs': {'id': '1'}, 'value': 'Short Description'}]}}
>>> client_langs_schema = [{'id': 2, 'locale': 'en-US', 'iso_code': 'en', 'language_code': 'en-us'}]
>>> page_lang = 'en-US'
>>> translated_dict = translate_presta_fields_dict(presta_fields_dict, client_langs_schema, page_lang)
>>> print(translated_dict)
{'name': {'language': [{'attrs': {'id': '2'}, 'value': 'Product Name'}]}, 'description': {'language': [{'attrs': {'id': '2'}, 'value': 'Product Description'}]}, 'short_description': {'language': [{'attrs': {'id': '2'}, 'value': 'Short Description'}]}}