# Модуль управления переводами

## Обзор

Модуль `src/endpoints/prestashop/translators/product_translator.py` предоставляет функциональность для управления переводами в контексте работы с товарами. Он служит связующим звеном между словарем полей товара, таблицей переводов и переводчиками.

## Детали

Модуль `product_translator.py`  предоставляет функции для получения переводов полей товара из таблицы переводов PrestaShop, вставки новых записей переводов в таблицу и перевода полей товара с помощью сторонних переводчиков.

## Функции

### `get_translations_from_presta_translations_table(product_reference: str, i18n: str = None) -> list:`

**Описание**:  Функция извлекает переводы полей товара из таблицы переводов PrestaShop.

**Параметры**:

- `product_reference` (str):  Референс товара, по которому производится поиск переводов.
- `i18n` (str, optional): Локаль языка перевода (например, `en_EN`, `he_HE`, `ru-RU`). По умолчанию `None`.

**Возвращает**:

- `list`: Список словарей с переводами полей товара.

**Как работает**:

1. Функция использует менеджер `ProductTranslationsManager` для подключения к таблице переводов PrestaShop.
2. Создается фильтр поиска `search_filter` с референсом товара.
3. Выполняется выборка записей из таблицы переводов с использованием менеджера `translations_manager` и фильтра `search_filter`.
4. Функция возвращает результат выборки в виде списка словарей.


### `insert_new_translation_to_presta_translations_table(record)`

**Описание**: Функция вставляет новую запись перевода в таблицу переводов PrestaShop.

**Параметры**:

- `record` (dict): Словарь с данными перевода, который нужно добавить в таблицу.

**Возвращает**:

- `None`

**Как работает**:

1. Функция использует менеджер `ProductTranslationsManager` для подключения к таблице переводов PrestaShop.
2. Вызывается метод `insert_record` менеджера для вставки новой записи с использованием данных из словаря `record`.


### `translate_record(record: dict, from_locale: str, to_locale: str) -> dict:`

**Описание**: Функция переводит поля товара с использованием стороннего переводчика.

**Параметры**:

- `record` (dict): Словарь с данными товара, которые нужно перевести.
- `from_locale` (str): Локаль исходного языка.
- `to_locale` (str): Локаль целевого языка.

**Возвращает**:

- `dict`: Словарь с переведенными полями товара.

**Как работает**:

1.  Функция использует функцию `translate` из модуля `src.llm.openai` для перевода данных товара с использованием модели OpenAI.
2.  Функция обрабатывает переведенную запись (реализацию пока нет).
3.  Функция возвращает словарь с переведенными полями товара.


## Примеры

### Получение переводов полей товара

```python
product_reference = 'PRD123'
i18n = 'ru-RU'

translations = get_translations_from_presta_translations_table(product_reference, i18n)

# Проверка, были ли найдены переводы
if translations:
    pprint(translations)
else:
    print('Переводы для товара не найдены.')
```

### Вставка новой записи перевода

```python
# Создание записи перевода
record = {
    'product_reference': 'PRD456',
    'locale': 'en_EN',
    'name': 'Product Name',
    # ... другие поля перевода
}

# Вставка записи в таблицу
insert_new_translation_to_presta_translations_table(record)
```

### Перевод полей товара

```python
record = {
    'name': 'Товар на русском',
    # ... другие поля товара
}

from_locale = 'ru-RU'
to_locale = 'en_EN'

translated_record = translate_record(record, from_locale, to_locale)

pprint(translated_record)
```

## Дополнительная информация

- В модуле используются функции `pprint`, `j_loads_ns`, `j_dumps` из модуля `src.utils.jjson`.
- Модуль `src.logger.logger` используется для логгирования событий.
- Модуль `src.db.ProductTranslationsManager` предоставляет доступ к таблице переводов PrestaShop.
- Модуль `src.llm.openai` используется для вызова функций OpenAI API.

## Замечания

- Необходимо продумать парсер для локалей `en_EN`, `he_HE`, `ru-RU`.
- Необходимо добавить обработку переведенной записи в функцию `translate_record`.