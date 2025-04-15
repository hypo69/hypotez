# Модуль `product_fields_translator`

## Обзор

Модуль `product_fields_translator` предназначен для перевода полей товара на языки, используемые в клиентской базе данных PrestaShop. Он содержит функции для корректировки идентификаторов языков и применения переводов к полям товара, собранным с сайта поставщика. Модуль обеспечивает соответствие языковых идентификаторов в данных о товаре с идентификаторами, используемыми в конкретной установке PrestaShop клиента.

## Подробней

Этот модуль играет важную роль в процессе интеграции данных о товарах от поставщиков в систему PrestaShop клиента. Поскольку идентификаторы языков могут отличаться в разных установках PrestaShop, модуль выполняет переназначение идентификаторов и применение переводов, хранящихся в базе данных клиента. Это позволяет обеспечить корректное отображение информации о товарах на разных языках в клиентском магазине.

## Функции

### `rearrange_language_keys`

```python
def rearrange_language_keys(presta_fields_dict: dict, client_langs_schema: dict | List[dict], page_lang: str) -> dict:
    """Функция обновляет идентификатор языка в словаре presta_fields_dict на соответствующий идентификатор
    из схемы клиентских языков при совпадении языка страницы.

    Args:
        presta_fields_dict (dict): Словарь полей товара.
        page_lang (str): Язык страницы.
        client_langs_schema (list | dict): Схема языков клиента.

    Returns:
        dict: Обновленный словарь presta_fields_dict.

    """
    ...
```

**Назначение**: Обновление идентификаторов языка в словаре полей товара (`presta_fields_dict`) на соответствующие идентификаторы из схемы языков клиента (`client_langs_schema`) при совпадении языка страницы (`page_lang`).

**Параметры**:
- `presta_fields_dict` (dict): Словарь полей товара, содержащий мультиязычные значения.
- `client_langs_schema` (dict | List[dict]): Схема языков клиента, содержащая соответствия между локалями, ISO-кодами и идентификаторами языков.
- `page_lang` (str): Язык страницы поставщика, например, `'en-US'` или `'ru-RU'`.

**Возвращает**:
- `dict`: Обновленный словарь `presta_fields_dict` с новыми идентификаторами языков.

**Как работает функция**:
- Функция итерируется по схеме языков клиента (`client_langs_schema`) и сравнивает локаль, ISO-код и код языка с языком страницы (`page_lang`).
- Если соответствие найдено, извлекается идентификатор языка клиента (`client_lang_id`).
- Затем функция итерируется по полям в словаре `presta_fields_dict` и обновляет атрибут `'id'` в поле `'language'`, если он существует, на `client_lang_id`.

**Примеры**:

Предположим, у нас есть следующий словарь `presta_fields_dict` и схема языков клиента `client_langs_schema`:

```python
presta_fields_dict = {
    'name': {
        'language': [
            {'attrs': {'id': '1'}, 'value': 'Product Name'}
        ]
    }
}

client_langs_schema = [
    {'id': '3', 'locale': 'en-US', 'iso_code': 'en', 'language_code': 'en-us'},
    {'id': '4', 'locale': 'fr-FR', 'iso_code': 'fr', 'language_code': 'fr-fr'}
]

page_lang = 'en-US'
```

После вызова функции:

```python
updated_dict = rearrange_language_keys(presta_fields_dict, client_langs_schema, page_lang)
print(updated_dict)
```

Результат будет:

```
{
    'name': {
        'language': [
            {'attrs': {'id': '3'}, 'value': 'Product Name'}
        ]
    }
}
```

### `translate_presta_fields_dict`

```python
def translate_presta_fields_dict (presta_fields_dict: dict, 
                                  client_langs_schema: list | dict, 
                                  page_lang: str = None) -> dict:
    """ @Перевод мультиязычных полей в соответствии со схемой значений `id` языка в базе данных клиента
	    Функция получает на вход заполненный словарь полей. Мультиязычные поля содржат значения,\n
	    полученные с сайта поставщика в виде словаря 
	    ```\n
	    {\n
	\t    \'language\':[\n
	\t\t\t\t\t    {\'attrs\':{\'id\':\'1\'}, \'value\':value},\n
	\t\t\t\t\t    ]\n
	    }\n
	    ```\n
	    У клиента язык с ключом `id=1` Может быть любым в зависимости от того на каком языке была \n
	    изначально установлена PrestaShop. Чаще всего это английский, но это не правило.\n
	    Точные соответствия я получаю в схеме языков клиента \n
	    locator_description\n
	    Самый быстрый способ узнать схему API языков - набрать в адресной строке браузера\n
	    https://API_KEY@mypresta.com/api/languages?display=full&io_format=JSON\n
	  
    @param client_langs_schema `dict` словарь актуальных языков на клиенте\n
    @param presta_fields_dict `dict` словарь полей товара собранный со страницы поставщика\n
    @param page_lang `str` язык страницы поставщика в коде en-US, ru-RU, he_HE. \n
    Если не задан - функция пытается определить п тексту\n
    @returns presta_fields_dict переведенный словарь полей товара
    """
    ...
```

**Назначение**: Перевод мультиязычных полей в словаре `presta_fields_dict` в соответствии со схемой значений `id` языка в базе данных клиента.

**Параметры**:
- `presta_fields_dict` (dict): Словарь полей товара, собранный со страницы поставщика.
- `client_langs_schema` (list | dict): Словарь актуальных языков на клиенте.
- `page_lang` (str, optional): Язык страницы поставщика в формате `en-US`, `ru-RU`, `he_HE`. Если не задан, функция пытается определить его автоматически. По умолчанию `None`.

**Возвращает**:
- `dict`: Переведенный словарь полей товара (`presta_fields_dict`).

**Как работает функция**:
1. **Переупорядочивание ключей таблицы**:
   - Вызывает функцию `rearrange_language_keys` для обновления идентификаторов языков в `presta_fields_dict` в соответствии со схемой языков клиента.
2. **Поиск существующих переводов**:
   - Получает существующие переводы товара из таблицы переводов PrestaShop.
3. **Добавление новых переводов**:
   - Если в таблице переводов нет записей для данного товара, добавляет текущие значения как новый перевод.
4. **Применение переводов из таблицы**:
   - Итерируется по доступным языкам клиента и записям перевода.
   - Если находит соответствие между ISO-кодом языка клиента и локалью переведенной записи, применяет перевод из таблицы к соответствующим полям в `presta_fields_dict`.
5. **Обработка ошибок**:
   - Логирует ошибки, возникающие в процессе применения переводов.

**Примеры**:

Предположим, у нас есть следующий словарь `presta_fields_dict`, схема языков клиента `client_langs_schema` и записи переводов `enabled_product_translations`:

```python
presta_fields_dict = {
    'name': {
        'language': [
            {'attrs': {'id': '1'}, 'value': 'Product Name'}
        ]
    },
    'reference': '12345'
}

client_langs_schema = [
    {'id': '3', 'locale': 'en-US', 'iso_code': 'en', 'language_code': 'en-us'},
    {'id': '4', 'locale': 'fr-FR', 'iso_code': 'fr', 'language_code': 'fr-fr'}
]

class TranslatedRecord:
    def __init__(self, locale, name):
        self.locale = locale
        self.name = name

enabled_product_translations = [
    TranslatedRecord(locale='en-US', name='Translated Product Name')
]
```

После вызова функции:

```python
updated_dict = translate_presta_fields_dict(presta_fields_dict, client_langs_schema, page_lang='en-US')
print(updated_dict)
```

Результат будет:

```
{
    'name': {'language': [{'attrs': {'id': '3'}, 'value': 'Translated Product Name'}]},
    'reference': '12345'
}