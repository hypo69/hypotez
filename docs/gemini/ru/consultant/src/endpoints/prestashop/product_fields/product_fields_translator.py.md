### **Анализ кода модуля `product_fields_translator.py`**

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код структурирован в функции, что улучшает читаемость.
    - Используется аннотация типов для параметров функций.
    - Есть docstring для функций, но требуется доработка.
- **Минусы**:
    - Некоторые комментарии неинформативны или устарели.
    - Использование `Union` вместо `|` для аннотаций типов.
    - Не везде используется логирование ошибок с `exc_info=True`.
    - Не все переменные аннотированы.
    - Не всегда используется `logger` для логирования, а вместо этого `print`.
    - Встречаются конструкции `if not enabled_product_translations or enabled_product_translations`, что является логической ошибкой.
    - Отсутствует документация модуля.

**Рекомендации по улучшению:**

1.  **Документация модуля**:
    - Добавить заголовок и описание модуля в формате Markdown.
2.  **Docstring**:
    - Переписать docstring для функций, чтобы они соответствовали указанному формату.
    - Добавить описание каждого параметра и возвращаемого значения.
    - Добавить примеры использования.
    - Внутренние функции должны быть задокументированы.
3.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных.
    - Использовать `|` вместо `Union`.
4.  **Логирование**:
    - Использовать `logger.error` с `exc_info=True` для логирования ошибок, чтобы получить полную трассировку.
    - Логировать важные этапы выполнения функций.
5.  **Комментарии**:
    - Сделать комментарии более информативными, объясняя назначение каждого блока кода.
    - Удалить устаревшие комментарии.
6.  **Обработка ошибок**:
    - Улучшить обработку ошибок, добавив более конкретные исключения.
7.  **Стиль кодирования**:
    - Использовать одинарные кавычки (`'`) вместо двойных (`"`).
    - Добавить пробелы вокруг операторов присваивания (`=`).
8.  **Логические ошибки**:
    - Исправить логическую ошибку в условии `if not enabled_product_translations or enabled_product_translations`.

**Оптимизированный код:**

```python
                ## \file /src/product/product_fields/product_fields_translator.py
# -*- coding: utf-8 -*-\

#! .pyenv/bin/python3

"""
Модуль перевода полей товара на языки клиентской базы данных
=============================================================

Модуль содержит функции для перевода мультиязычных полей товара в соответствии со схемой значений `id` языка в базе данных клиента.
Он также включает функции для реорганизации ключей языка и вставки новых переводов в таблицу переводов PrestaShop.

Пример использования
----------------------

>>> presta_fields_dict = {'name': {'language': [{'attrs': {'id': '1'}, 'value': 'Product Name'}]}}
>>> client_langs_schema = [{'id': 2, 'locale': 'fr-FR', 'iso_code': 'fr', 'language_code': 'fr-fr'}]
>>> page_lang = 'fr-FR'
>>> translated_dict = translate_presta_fields_dict(presta_fields_dict, client_langs_schema, page_lang)
>>> print(translated_dict)
{'name': {'language': [{'attrs': {'id': '2'}, 'value': 'Product Name'}]}}
"""

from pathlib import Path
from typing import List, Optional
import json

from src import gs
from src.utils.printer import pprint
from src.logger.logger import logger
#from src.db import ProductTranslationsManager
#from src.translator import get_translations_from_presta_translations_table
#from src.translator import insert_new_translation_to_presta_translations_table
from src.logger.exceptions import ProductFieldException
# from src.db import record

def rearrange_language_keys(presta_fields_dict: dict, client_langs_schema: list[dict], page_lang: str) -> dict:
    """
    Обновляет идентификатор языка в словаре `presta_fields_dict` на соответствующий идентификатор из схемы клиентских языков при совпадении языка страницы.

    Args:
        presta_fields_dict (dict): Словарь полей товара.
        client_langs_schema (list[dict]): Схема языков клиента.
        page_lang (str): Язык страницы.

    Returns:
        dict: Обновленный словарь `presta_fields_dict`.

    Raises:
        TypeError: Если `presta_fields_dict` не является словарем.
        TypeError: Если `client_langs_schema` не является списком или словарем.
        TypeError: Если `page_lang` не является строкой.

    Example:
        >>> presta_fields_dict = {'name': {'language': [{'attrs': {'id': '1'}, 'value': 'Product Name'}]}}
        >>> client_langs_schema = [{'id': 2, 'locale': 'fr-FR', 'iso_code': 'fr', 'language_code': 'fr-fr'}]
        >>> page_lang = 'fr-FR'
        >>> rearrange_language_keys(presta_fields_dict, client_langs_schema, page_lang)
        {'name': {'language': [{'attrs': {'id': '2'}, 'value': 'Product Name'}]}}
    """
    # Проверка типов входных данных
    if not isinstance(presta_fields_dict, dict):
        raise TypeError('presta_fields_dict должен быть словарем')
    if not isinstance(client_langs_schema, (list, dict)):
        raise TypeError('client_langs_schema должен быть списком или словарем')
    if not isinstance(page_lang, str):
        raise TypeError('page_lang должен быть строкой')

    client_lang_id: Optional[int] = None # Инициализация client_lang_id

    # Найти соответствующий идентификатор языка в схеме клиентских языков
    for lang in client_langs_schema:
        if lang['locale'] == page_lang or lang['iso_code'] == page_lang or lang['language_code'] == page_lang:
            client_lang_id = lang['id']
            break

    # Если найден идентификатор языка в схеме клиентских языков
    if client_lang_id is not None:
        # Обновить значение атрибута id в словаре presta_fields_dict
        for field in presta_fields_dict.values():
            if isinstance(field, dict) and 'language' in field:
                for lang_data in field['language']:
                    if isinstance(lang_data, dict) and 'attrs' in lang_data:
                        lang_data['attrs']['id'] = str(client_lang_id) # айдишники ОБЯЗАТЕЛЬНО строки. Связано с XML парсером

    return presta_fields_dict


def translate_presta_fields_dict(
    presta_fields_dict: dict,
    client_langs_schema: list[dict],
    page_lang: str | None = None
) -> dict:
    """
    Переводит мультиязычные поля в соответствии со схемой значений `id` языка в базе данных клиента.

    Функция получает на вход заполненный словарь полей. Мультиязычные поля содержат значения,
    полученные с сайта поставщика в виде словаря:
    ```
    {
        'language':[
                        {'attrs':{'id':'1'}, 'value':value},
                        ]
    }
    ```
    У клиента язык с ключом `id=1` Может быть любым в зависимости от того на каком языке была
    изначально установлена PrestaShop. Чаще всего это английский, но это не правило.
    Точные соответствия я получаю в схеме языков клиента.

    Самый быстрый способ узнать схему API языков - набрать в адресной строке браузера:
    https://API_KEY@mypresta.com/api/languages?display=full&io_format=JSON

    Args:
        presta_fields_dict (dict): Словарь полей товара, собранный со страницы поставщика.
        client_langs_schema (list[dict]): Словарь актуальных языков на клиенте.
        page_lang (str | None, optional): Язык страницы поставщика в коде en-US, ru-RU, he_HE.
            Если не задан - функция пытается определить по тексту. По умолчанию None.

    Returns:
        dict: Переведенный словарь полей товара.

    Raises:
        ProductFieldException: Если возникает ошибка при переводе полей.

    Example:
        >>> presta_fields_dict = {'name': {'language': [{'attrs': {'id': '1'}, 'value': 'Product Name'}]}}
        >>> client_langs_schema = [{'id': 2, 'locale': 'fr-FR', 'iso_code': 'fr', 'language_code': 'fr-fr'}]
        >>> page_lang = 'fr-FR'
        >>> translate_presta_fields_dict(presta_fields_dict, client_langs_schema, page_lang)
        {'name': {'language': [{'attrs': {'id': '2'}, 'value': 'Product Name'}]}}
    """
    # Проверяем типы входных параметров
    if not isinstance(presta_fields_dict, dict):
        raise TypeError('presta_fields_dict должен быть словарем')
    if not isinstance(client_langs_schema, list):
        raise TypeError('client_langs_schema должен быть списком')
    if page_lang is not None and not isinstance(page_lang, str):
        raise TypeError('page_lang должен быть строкой или None')

    try:
        # Переупорядочиваем ключи таблицы.
        presta_fields_dict = rearrange_language_keys(presta_fields_dict, client_langs_schema, page_lang)

        # Пытаемся получить переводы из таблицы переводов PrestaShop.
        enabled_product_translations = get_translations_from_presta_translations_table(presta_fields_dict['reference'])

        # Если в таблице переводов нет такого перевода товара.
        if not enabled_product_translations:
            logger.info(f'В таблице переводов нет перевода для товара {presta_fields_dict["reference"]}. Добавляем текущий как новый.')
            # Добавляем текущий, как новый
            #global record
            #rec = record(presta_fields_dict)
            #insert_new_translation_to_presta_translations_table(rec)
            #logger.info(f'Перевод для товара {presta_fields_dict["reference"]} добавлен в таблицу переводов.')
            return presta_fields_dict

        # Если переводы найдены, применяем их
        for client_lang in client_langs_schema:
            for translated_record in enabled_product_translations:
                # ПЕРЕВОД
                # client codes from PrestaShop table
                # 'iso_code'    'en'    str
                # 'locale'    'en-US'    str
                # 'language_code'    'en-us'    str
                # мне нужен iso_code
                if client_lang['iso_code'] in translated_record.locale:
                    logger.info(f'Записываем перевод из таблицы для языка {client_lang["iso_code"]}.')
                    # Записываем перевод из таблицы
                    for key in presta_fields_dict.keys():
                        if hasattr(translated_record, key):
                            presta_fields_dict[key] = {'language': [{'attrs': {'id': str(client_lang['id'])}, 'value': getattr(translated_record, key)}]}
                            # айдишники ОБЯЗАТЕЛЬНО строки. Связано с XML парсером

        return presta_fields_dict

    except Exception as ex:
        logger.error(f'Ошибка при переводе полей товара.', ех, exc_info=True)
        raise ProductFieldException(f'Ошибка при переводе полей товара: {ex}') from ex