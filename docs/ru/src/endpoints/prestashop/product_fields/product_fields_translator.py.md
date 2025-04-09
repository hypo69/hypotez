# Модуль перевода полей товара `product_fields_translator`

## Обзор

Модуль предназначен для перевода полей товара на языки клиентской базы данных. Он содержит функции для обновления идентификаторов языков в словаре полей товара в соответствии со схемой языков клиента.

## Подробней

Этот модуль помогает адаптировать поля товаров, полученные от поставщика, к языковым настройкам конкретной клиентской базы данных PrestaShop. Это необходимо, поскольку идентификаторы языков в PrestaShop могут отличаться в разных установках.

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

**Назначение**: Обновление идентификатора языка в словаре `presta_fields_dict` на соответствующий идентификатор из схемы клиентских языков при совпадении языка страницы.

**Параметры**:
- `presta_fields_dict` (dict): Словарь полей товара, который необходимо обновить.
- `client_langs_schema` (dict | List[dict]): Схема языков клиента, используемая для поиска соответствия идентификаторов.
- `page_lang` (str): Язык страницы, для которого выполняется поиск соответствия.

**Возвращает**:
- `dict`: Обновленный словарь `presta_fields_dict` с новыми идентификаторами языков.

**Как работает функция**:
1. **Поиск идентификатора языка**: Функция итерируется по схеме клиентских языков (`client_langs_schema`) и ищет соответствие языка страницы (`page_lang`) на основе полей `locale`, `iso_code` или `language_code`.
2. **Обновление идентификатора**: Если соответствующий идентификатор языка найден, функция итерируется по полям товара в `presta_fields_dict`. Для каждого поля, содержащего информацию о языке, обновляется атрибут `id` на найденный `client_lang_id`.

```
Начало
│
├── Поиск client_lang_id в client_langs_schema (по locale, iso_code, language_code)
│
├── Если client_lang_id найден:
│   │
│   └── Обновление attrs['id'] в presta_fields_dict на client_lang_id
│
└── Возврат обновленного presta_fields_dict
```

**Примеры**:

Предположим, у нас есть словарь полей товара:

```python
presta_fields_dict = {
    'name': {
        'language': [
            {'attrs': {'id': '1'}, 'value': 'Product Name'}
        ]
    }
}
```

и схема языков клиента:

```python
client_langs_schema = [
    {'id': '2', 'locale': 'ru-RU', 'iso_code': 'ru', 'language_code': 'ru-ru'}
]
```

и язык страницы:

```python
page_lang = 'ru-RU'
```

Вызов функции будет выглядеть так:

```python
result = rearrange_language_keys(presta_fields_dict, client_langs_schema, page_lang)
print(result)
# Вывод: {'name': {'language': [{'attrs': {'id': '2'}, 'value': 'Product Name'}]}}
```

### `translate_presta_fields_dict`

```python
def translate_presta_fields_dict (presta_fields_dict: dict, 
                                  client_langs_schema: list | dict, 
                                  page_lang: str = None) -> dict:
    """ @Перевод мультиязычных полей в соответствии со схемой значений `id` языка в базе данных клиента
	    Функция получает на вход заполненный словарь полей. Мультиязычные поля содржат значения,
	    полученные с сайта поставщика в виде словаря 
	    ```
	    {
	\t    \'language\':[\
	\t\t\t\t\t    {\'attrs\':{\'id\':\'1\'}, \'value\':value},\
	\t\t\t\t\t    ]\
	    }\
	    ```
	    У клиента язык с ключом `id=1` Может быть любым в зависимости от того на каком языке была 
	    изначально установлена PrestaShop. Чаще всего это английский, но это не правило.
	    Точные соответствия я получаю в схеме языков клиента 
	    locator_description
	    Самый быстрый способ узнать схему API языков - набрать в адресной строке браузера
	    https://API_KEY@mypresta.com/api/languages?display=full&io_format=JSON
	  
    @param client_langs_schema `dict` словарь актуальных языков на клиенте
    @param presta_fields_dict `dict` словарь полей товара собранный со страницы поставщика
    @param page_lang `str` язык страницы поставщика в коде en-US, ru-RU, he_HE. 
    Если не задан - функция пытается определить п тексту
    @returns presta_fields_dict переведенный словарь полей товара
    """
    ...
```

**Назначение**: Перевод мультиязычных полей в соответствии со схемой значений `id` языка в базе данных клиента.

**Параметры**:
- `presta_fields_dict` (dict): Словарь полей товара, собранный со страницы поставщика.
- `client_langs_schema` (list | dict): Словарь актуальных языков на клиенте.
- `page_lang` (str, optional): Язык страницы поставщика в коде (например, en-US, ru-RU, he_HE). Если не задан, функция пытается определить язык автоматически. По умолчанию `None`.

**Возвращает**:
- `dict`: Переведенный словарь полей товара.

**Как работает функция**:

1.  **Переупорядочивание ключей таблицы**:
    *   Вызывается функция `rearrange_language_keys` для обновления идентификаторов языков в соответствии со схемой клиента.
2.  **Получение переводов из таблицы**:
    *   Вызывается функция `get_translations_from_presta_translations_table`, чтобы получить существующие переводы товара.
3.  **Обработка отсутствующих переводов**:
    *   Если переводы отсутствуют, текущие значения добавляются в таблицу переводов.
4.  **Перевод полей**:
    *   Функция итерируется по доступным языкам клиента (`client_langs_schema`) и сравнивает их с переводами из таблицы.
    *   Если находится соответствие, значения полей товара перезаписываются переведенными значениями из таблицы.

```
Начало
│
├── Переупорядочивание ключей таблицы (rearrange_language_keys)
│
├── Получение переводов из таблицы (get_translations_from_presta_translations_table)
│
├── Если нет переводов:
│   │
│   └── Добавление текущих значений в таблицу переводов (insert_new_translation_to_presta_translations_table)
│
├── Для каждого языка клиента:
│   │
│   └── Для каждой записи перевода:
│       │
│       └── Если iso_code языка клиента есть в locale записи перевода:
│           │
│           └── Запись перевода из таблицы
│
└── Возврат переведенного presta_fields_dict
```

**Примеры**:

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
    {'id': '1', 'locale': 'en-US', 'iso_code': 'en', 'language_code': 'en-us'},
    {'id': '2', 'locale': 'ru-RU', 'iso_code': 'ru', 'language_code': 'ru-ru'}
]

# Предположим, что функция get_translations_from_presta_translations_table возвращает следующий объект:
class TranslatedRecord:
    def __init__(self, name_ru):
        self.name = name_ru

    @property
    def locale(self):
        return 'ru-RU'

    @property
    def name(self):
        return {'language': [{'attrs': {'id': '2'}, 'value': 'Имя продукта'}]}

enabled_product_translations = [
    TranslatedRecord(name_ru={'language': [{'attrs': {'id': '2'}, 'value': 'Имя продукта'}]})
]


def get_translations_from_presta_translations_table(reference: str) -> list:
    # Эмулируем получение данных из базы данных
    return enabled_product_translations  # Возвращаем тестовый экземпляр

presta_fields_dict = translate_presta_fields_dict(presta_fields_dict, client_langs_schema, page_lang='ru-RU')
print(presta_fields_dict)
# {'name': {'language': [{'attrs': {'id': '2'}, 'value': 'Имя продукта'}]}, 'reference': '12345'}