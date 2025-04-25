# Модуль для перевода полей товара на языки клиентской базы данных
===============================================================

Модуль `src.product.product_fields.product_fields_translator` содержит функции для перевода полей товара на языки клиентской базы данных. Он используется для обработки мультиязычных полей товара, полученных с сайта поставщика, и преобразования их в формат, совместимый с базой данных клиента.

## Содержание

- [Обзор](#обзор)
- [Функции](#функции)
    - [rearrange_language_keys](#rearrange_language_keys)
    - [translate_presta_fields_dict](#translate_presta_fields_dict)

## Обзор

Модуль предназначен для решения проблемы несовместимости форматов языков между сайтом поставщика и базой данных клиента. 
Функции модуля получают на вход словарь полей товара (в формате PrestaShop) и схему языков клиента. 
Далее происходит перевод полей товара на языки клиента, учитывая соответствие между идентификаторами языков в PrestaShop и клиентской базе данных. 

## Функции

### `rearrange_language_keys`

#### Назначение:

Обновляет идентификатор языка в словаре `presta_fields_dict` на соответствующий идентификатор из схемы клиентских языков при совпадении языка страницы.

#### Параметры:

- `presta_fields_dict (dict)`: Словарь полей товара.
- `client_langs_schema (list | dict)`: Схема языков клиента.
- `page_lang (str)`: Язык страницы.

#### Возвращает:

- `dict`: Обновленный словарь `presta_fields_dict`.

#### Как работает функция:

1. Функция ищет соответствующий идентификатор языка в схеме клиентских языков, сравнивая значение `locale`, `iso_code` и `language_code` с языком страницы.
2. Если идентификатор найден, функция обновляет значение атрибута `id` в словаре `presta_fields_dict` для всех полей товара, которые являются словарями и содержат ключ `language`.

#### Примеры:

```python
>>> presta_fields_dict = {'name': {'language': [{'attrs': {'id': '1'}, 'value': 'Product Name'}]}}
>>> client_langs_schema = [{'id': 2, 'locale': 'en-US'}]
>>> page_lang = 'en-US'
>>> rearrange_language_keys(presta_fields_dict, client_langs_schema, page_lang)
{'name': {'language': [{'attrs': {'id': '2'}, 'value': 'Product Name'}]}}
```

### `translate_presta_fields_dict`

#### Назначение:

Переводит мультиязычные поля товара в соответствии со схемой значений `id` языка в базе данных клиента.

#### Параметры:

- `presta_fields_dict (dict)`: Словарь полей товара, полученный с сайта поставщика.
- `client_langs_schema (list | dict)`: Схема языков клиента.
- `page_lang (str)`: Язык страницы поставщика в коде `en-US`, `ru-RU`, `he_HE`. 
Если не задан - функция пытается определить язык по тексту.

#### Возвращает:

- `dict`: Переведенный словарь полей товара.

#### Как работает функция:

1. Функция переупорядочивает ключи таблицы с помощью функции `rearrange_language_keys`.
2. Извлекает переводы товара из таблицы переводов.
3. Если переводы товара отсутствуют в таблице, добавляет текущий перевод как новый.
4. Для каждого языка клиента функция проверяет, есть ли перевод в таблице переводов, и, если есть, обновляет соответствующие поля товара в словаре `presta_fields_dict`.

#### Примеры:

```python
>>> presta_fields_dict = {'name': {'language': [{'attrs': {'id': '1'}, 'value': 'Product Name'}]}}
>>> client_langs_schema = [{'id': 2, 'iso_code': 'en'}]
>>> page_lang = 'en-US'
>>> translate_presta_fields_dict(presta_fields_dict, client_langs_schema, page_lang)
{'name': {'language': [{'attrs': {'id': '2'}, 'value': 'Product Name'}]}}
```

```python
>>> presta_fields_dict = {'name': {'language': [{'attrs': {'id': '1'}, 'value': 'Product Name'}]}}
>>> client_langs_schema = [{'id': 2, 'iso_code': 'ru'}]
>>> page_lang = 'en-US'
>>> translate_presta_fields_dict(presta_fields_dict, client_langs_schema, page_lang)
{'name': {'language': [{'attrs': {'id': '2'}, 'value': 'Product Name'}]}}
```
```python
>>> presta_fields_dict = {'name': {'language': [{'attrs': {'id': '1'}, 'value': 'Product Name'}]}}
>>> client_langs_schema = [{'id': 2, 'iso_code': 'he'}]
>>> page_lang = 'en-US'
>>> translate_presta_fields_dict(presta_fields_dict, client_langs_schema, page_lang)
{'name': {'language': [{'attrs': {'id': '2'}, 'value': 'Product Name'}]}}
```

## Внутренние функции

- `get_translations_from_presta_translations_table(presta_fields_dict['reference'])`: 
   - **Назначение**: 
     - Извлекает переводы товара из таблицы переводов PrestaShop по `reference` товара.
   - **Параметры**:
     - `presta_fields_dict['reference'] (str)`: `reference` товара.
   - **Возвращает**:
     - `list`: Список переводов товара.
- `insert_new_translation_to_presta_translations_table(rec)`: 
   - **Назначение**: 
     - Вставляет новый перевод товара в таблицу переводов PrestaShop.
   - **Параметры**:
     - `rec (dict)`: Словарь с данными о переводе товара.
   - **Возвращает**:
     - `None`.

## Принцип работы функции `translate_presta_fields_dict`

Функция `translate_presta_fields_dict` работает по следующему алгоритму:

1. Проверяется наличие перевода товара в таблице переводов.
2. Если переводы отсутствуют - вставляется новый перевод товара в таблицу переводов.
3. Для каждого языка клиента функция проверяет наличие перевода товара в таблице переводов.
4. Если перевод найден - значение поля товара в словаре `presta_fields_dict` обновляется значением из таблицы переводов. 

## Примечания

- В функции `rearrange_language_keys` при сравнении языков нужно учитывать, что `locale`, `iso_code` и `language_code` могут иметь разные значения. 
- В функции `translate_presta_fields_dict` необходимо убедиться, что идентификаторы языков в таблице переводов соответствуют идентификаторам языков в базе данных клиента.
- `id` в `attrs` ОБЯЗАТЕЛЬНО должны быть строками, а не числами. Связано с XML парсером.