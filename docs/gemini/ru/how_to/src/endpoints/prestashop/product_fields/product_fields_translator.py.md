## Как использовать функцию `rearrange_language_keys`
=========================================================================================

Описание
-------------------------
Функция `rearrange_language_keys` обновляет идентификатор языка в словаре `presta_fields_dict` на соответствующий идентификатор из схемы клиентских языков, если язык страницы совпадает.  

Шаги выполнения
-------------------------
1. **Находит соответствующий идентификатор языка**: Функция перебирает языки в `client_langs_schema` и сравнивает их с языком страницы `page_lang`. Если совпадение найдено, сохраняется идентификатор языка из схемы.
2. **Обновляет идентификатор языка в `presta_fields_dict`**: Если найден идентификатор языка в `client_langs_schema`, функция перебирает все поля в `presta_fields_dict`. Если поле содержит информацию о языке (`'language' in field`),  функция перебирает все языковые данные в поле (`field['language']`) и обновляет атрибут `'id'` на найденный идентификатор языка. 

Пример использования
-------------------------

```python
from src.product.product_fields.product_fields_translator import rearrange_language_keys

presta_fields_dict = {
    'name': {
        'language': [
            {'attrs': {'id': '1'}, 'value': 'Product Name English'},
            {'attrs': {'id': '2'}, 'value': 'Product Name French'}
        ]
    },
    'description': {
        'language': [
            {'attrs': {'id': '1'}, 'value': 'Product Description English'},
            {'attrs': {'id': '2'}, 'value': 'Product Description French'}
        ]
    }
}

client_langs_schema = [
    {'id': 10, 'locale': 'en-US', 'iso_code': 'en', 'language_code': 'en-us'},
    {'id': 20, 'locale': 'fr-FR', 'iso_code': 'fr', 'language_code': 'fr-fr'}
]

page_lang = 'en-US'

updated_presta_fields_dict = rearrange_language_keys(presta_fields_dict, client_langs_schema, page_lang)

# После обновления:
print(updated_presta_fields_dict)
# Вывод:
# {'name': {'language': [{'attrs': {'id': '10'}, 'value': 'Product Name English'}, {'attrs': {'id': '20'}, 'value': 'Product Name French'}]}, 'description': {'language': [{'attrs': {'id': '10'}, 'value': 'Product Description English'}, {'attrs': {'id': '20'}, 'value': 'Product Description French'}]}}
```

В этом примере функция `rearrange_language_keys` находит идентификатор языка `10` в `client_langs_schema`  и обновляет значения атрибута `'id'` в `presta_fields_dict`.