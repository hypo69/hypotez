# Модуль `product_fields_translator`

## Обзор

Модуль предназначен для перевода полей товара на языки, используемые в клиентской базе данных PrestaShop. Он обеспечивает соответствие идентификаторов языков в данных о товаре идентификаторам, используемым в системе клиента, что необходимо для корректного отображения информации о товаре на разных языках.

## Подробнее

Этот модуль играет важную роль в процессе интеграции данных о товарах из внешних источников (например, от поставщиков) в систему PrestaShop. Поскольку идентификаторы языков могут отличаться между системами поставщика и клиента, модуль выполняет преобразование этих идентификаторов, чтобы обеспечить правильную локализацию данных о товаре.

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

**Назначение**: Обновление идентификатора языка в словаре полей товара (`presta_fields_dict`) на соответствующий идентификатор из схемы языков клиента (`client_langs_schema`) при совпадении языка страницы (`page_lang`).

**Параметры**:

-   `presta_fields_dict` (dict): Словарь полей товара, содержащий мультиязычные значения.
-   `client_langs_schema` (dict | List[dict]): Схема языков клиента, содержащая информацию о соответствии локалей и идентификаторов языков.
-   `page_lang` (str): Язык текущей страницы товара в формате, например, 'en-US' или 'ru-RU'.

**Возвращает**:

-   `dict`: Обновленный словарь `presta_fields_dict` с новыми идентификаторами языков, соответствующими схеме клиента.

**Как работает функция**:

1.  **Инициализация**: Функция начинает с поиска соответствующего идентификатора языка в схеме клиентских языков.
2.  **Поиск соответствия**: Перебирает языки в `client_langs_schema` и сравнивает их поля `locale`, `iso_code` и `language_code` с `page_lang`.
3.  **Обновление идентификатора**: Если соответствие найдено, функция переходит к обновлению атрибута `id` в полях `language` словаря `presta_fields_dict`.
4.  **Преобразование `id` в строку**: Значение `id` преобразуется в строку, так как XML парсер требует строковые значения.

```
A[Начало]
|
B[Найти client_lang_id в client_langs_schema]
|
C[Если client_lang_id найден] -- D[Обновить id в presta_fields_dict]
|
E[Возврат presta_fields_dict]
|
F[Конец]
```

**Примеры**:

```python
# Пример вызова функции
client_langs_schema = [
    {'id': '2', 'locale': 'ru-RU', 'iso_code': 'ru', 'language_code': 'ru-ru'},
    {'id': '1', 'locale': 'en-US', 'iso_code': 'en', 'language_code': 'en-us'}
]
presta_fields_dict = {
    'name': {'language': [{'attrs': {'id': '1'}, 'value': 'Product Name'}]}
}
page_lang = 'ru-RU'
updated_dict = rearrange_language_keys(presta_fields_dict, client_langs_schema, page_lang)
print(updated_dict)
# {'name': {'language': [{'attrs': {'id': '2'}, 'value': 'Product Name'}]}}
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
	    ```\
	    У клиента язык с ключом `id=1` Может быть любым в зависимости от того на каком языке была 
	    изначально установлена PrestaShop. Чаще всего это английский, но это не правило.\
	    Точные соответствия я получаю в схеме языков клиента 
	    locator_description\
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

-   `presta_fields_dict` (dict): Словарь полей товара, собранный со страницы поставщика.
-   `client_langs_schema` (list | dict): Словарь актуальных языков на клиенте.
-   `page_lang` (str, optional): Язык страницы поставщика в коде (например, 'en-US', 'ru-RU'). Если не задан, функция пытается определить язык автоматически.

**Возвращает**:

-   `dict`: Переведенный словарь полей товара `presta_fields_dict`.

**Как работает функция**:

1.  **Переупорядочивание ключей**: Сначала вызывается функция `rearrange_language_keys` для обновления идентификаторов языков в соответствии со схемой клиента.
2.  **Получение переводов из таблицы**: Функция пытается получить переводы товара из таблицы переводов PrestaShop.
3.  **Обработка отсутствующих переводов**: Если переводы для данного товара отсутствуют в таблице, текущие значения добавляются как новые переводы.
4.  **Перевод полей**: Если переводы найдены, функция перебирает языки клиента и записи переводов, чтобы обновить значения полей товара соответствующими переводами из таблицы.
5.  **Обработка ошибок**: При возникновении ошибок в процессе перевода, информация об ошибке и параметры клиента логируются с использованием `logger.error`.

```
A[Начало]
|
B[Переупорядочивание ключей: rearrange_language_keys]
|
C[Получение переводов из таблицы: get_translations_from_presta_translations_table]
|
D[Если нет переводов] -- E[Добавить текущий как новый: insert_new_translation_to_presta_translations_table]
|
F[Для каждого языка клиента] -- G[Для каждой записи перевода] -- H[Если iso_code совпадает] -- I[Записать перевод из таблицы]
|
J[Возврат presta_fields_dict]
|
K[Конец]
```

**Примеры**:

```python
# Пример вызова функции
client_langs_schema = [
    {'id': '2', 'locale': 'ru-RU', 'iso_code': 'ru', 'language_code': 'ru-ru'},
    {'id': '1', 'locale': 'en-US', 'iso_code': 'en', 'language_code': 'en-us'}
]
presta_fields_dict = {
    'name': {'language': [{'attrs': {'id': '1'}, 'value': 'Product Name'}]},
    'reference': 'PRODUCT123'
}
page_lang = 'ru-RU'

# Здесь необходимо определить функции get_translations_from_presta_translations_table и insert_new_translation_to_presta_translations_table

translated_dict = translate_presta_fields_dict(presta_fields_dict, client_langs_schema, page_lang)
print(translated_dict)
# {'name': {'language': [{'attrs': {'id': '2'}, 'value': 'Translated Product Name'}]}, 'reference': 'PRODUCT123'}