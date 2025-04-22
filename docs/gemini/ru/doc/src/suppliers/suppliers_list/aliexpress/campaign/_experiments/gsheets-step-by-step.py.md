# Модуль: Эксперименты с Google Таблицами для AliExpress Campaign

## Обзор

Этот модуль предназначен для экспериментов с Google Таблицами в контексте управления рекламными кампаниями на AliExpress. Он предоставляет инструменты для чтения, редактирования и обновления данных кампаний, категорий и товаров через Google Sheets. Модуль включает в себя интеграцию с Google Sheets API для автоматизации процессов управления кампаниями.

## Подробнее

Модуль позволяет автоматизировать процесс обновления информации о кампаниях AliExpress через Google Sheets. Он включает в себя:

-   Чтение и запись данных категорий и товаров кампании в Google Sheets.
-   Обновление информации о категориях на основе данных, отредактированных в Google Sheets.
-   Преобразование данных между различными форматами (например, `SimpleNamespace`, `dict`, `list`) для упрощения работы с Google Sheets API и внутренними структурами данных кампании.
-   Использование класса `AliCampaignGoogleSheet` для взаимодействия с Google Sheets API.
-   Использование класса `AliCampaignEditor` для редактирования данных кампании.
-   Логирование для отслеживания изменений и отладки.

## Классы

В данном коде используются следующие классы:

### `AliCampaignGoogleSheet`

**Описание**: Класс для взаимодействия с Google Sheets API в контексте управления рекламными кампаниями на AliExpress.

**Атрибуты**:

*   Отсутствуют явные атрибуты, но класс инициализируется с использованием идентификатора Google Sheet.

**Методы**:

*   `__init__(spreadsheet_id: str)`: Инициализирует экземпляр класса с указанным идентификатором Google Sheet.
*   `set_categories(categories_list: list[CategoryType])`: Записывает список категорий в Google Sheet.
*   `get_categories() -> list[dict]`: Получает список категорий из Google Sheet.
*   `set_category_products(category_name: str, products: list[dict])`: Записывает список товаров для указанной категории в Google Sheet.

### `AliCampaignEditor`

**Описание**: Класс для редактирования данных рекламных кампаний на AliExpress.

**Атрибуты**:

*   `campaign`: Объект, содержащий данные о рекламной кампании.

**Методы**:

*   `__init__(campaign_name: str, language: str, currency: str)`: Инициализирует экземпляр класса с указанными параметрами кампании.
*   `get_category_products(category_name: str) -> list[dict]`: Получает список товаров для указанной категории.
*   `update_campaign(edited_campaign: SimpleNamespace)`: Обновляет данные кампании.

## Функции

### Отсутствуют функции. Весь код выполняется сразу
```python
gs = AliCampaignGoogleSheet('1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0')
...
```

**Описание**: Создается экземпляр класса `AliCampaignGoogleSheet` для взаимодействия с Google Sheets API.

**Как работает функция**:

1.  Инициализируется класс `AliCampaignGoogleSheet` с указанным идентификатором Google Sheet, что позволяет читать и записывать данные в соответствующую таблицу.

###  
```python
campaign_name = "lighting"
language = 'EN'
currency = 'USD'
campaign_editor = AliCampaignEditor(campaign_name, language, currency)
campaign_data = campaign_editor.campaign
_categories: SimpleNamespace = campaign_data.category
```

**Описание**: Инициализация данных кампании и категорий.

**Как работает функция**:

1.  Определяются параметры кампании, такие как название, язык и валюта.
2.  Создается экземпляр класса `AliCampaignEditor` с указанными параметрами.
3.  Извлекаются данные кампании и категории из экземпляра `AliCampaignEditor`.

###  
```python
categories_dict: dict[str, CategoryType] = {category_name: getattr(_categories, category_name) for category_name in vars(_categories)}
```

**Описание**: Преобразование категорий из `SimpleNamespace` в словарь.

**Как работает функция**:

1.  Преобразует атрибуты объекта `_categories` (типа `SimpleNamespace`) в словарь, где ключами являются имена категорий, а значениями - объекты `CategoryType`.

###  
```python
categories_list: list[CategoryType] = list(categories_dict.values())
```

**Описание**: Преобразование категорий из словаря в список.

**Как работает функция**:

1.  Извлекает значения (объекты `CategoryType`) из словаря `categories_dict` и преобразует их в список.

###  
```python
gs.set_categories(categories_list)
```

**Описание**: Установка категорий в Google Sheet.

**Как работает функция**:

1.  Вызывает метод `set_categories` объекта `gs` для записи списка категорий в Google Sheet.

###  
```python
edited_categories: list[dict] = gs.get_categories()
```

**Описание**: Получение отредактированных категорий из Google Sheet.

**Как работает функция**:

1.  Вызывает метод `get_categories` объекта `gs` для чтения отредактированных данных категорий из Google Sheet.

###  
```python
for _cat in edited_categories:
    _cat_ns: SimpleNamespace = SimpleNamespace(**{
        'name':_cat['name'],
        'title':_cat['title'],
        'description':_cat['description'],
        'tags':_cat['tags'],
        'products_count':_cat['products_count']
    }
    )
    logger.info(f"Updating category: {_cat_ns.name}")
    categories_dict[_cat_ns.name] = _cat_ns
    products = campaign_editor.get_category_products(_cat_ns.name)
    gs.set_category_products(_cat_ns.name,products)
```

**Описание**: Обновление данных категорий на основе информации из Google Sheet.

**Как работает функция**:

1.  Перебирает список отредактированных категорий, полученных из Google Sheet.
2.  Преобразует каждую категорию из словаря в объект `SimpleNamespace`.
3.  Обновляет соответствующую категорию в словаре `categories_dict`.
4.  Получает список товаров для каждой категории с помощью `campaign_editor.get_category_products()`.
5.  Записывает список товаров для каждой категории в Google Sheet с помощью `gs.set_category_products()`.
6.  Логирует обновление категории с указанием её имени.

###  
```python
_updated_categories = SimpleNamespace(**categories_dict)
```

**Описание**: Преобразование категорий обратно в `SimpleNamespace`.

**Как работает функция**:

1.  Преобразует обновленный словарь `categories_dict` обратно в объект `SimpleNamespace`.

###  
```python
pprint(_updated_categories)
```

**Описание**: Вывод данных для отладки.

**Как работает функция**:

1.  Выводит содержимое объекта `_updated_categories` для отладки.

###  
```python
campaign_dict: dict = {
    'name': campaign_data.campaign_name,
    'title': campaign_data.title,
    'language': language,
    'currency': currency,
    'category': _updated_categories
}
```

**Описание**: Создание словаря для кампании.

**Как работает функция**:

1.  Создает словарь, содержащий информацию о кампании, включая название, язык, валюту и обновленные категории.

###  
```python
edited_campaign: SimpleNamespace = SimpleNamespace(**campaign_dict)
pprint(edited_campaign)
campaign_editor.update_campaign(edited_campaign)
```

**Описание**: Обновление данных кампании и вывод для отладки.

**Как работает функция**:

1.  Преобразует словарь `campaign_dict` в объект `SimpleNamespace`.
2.  Выводит содержимое объекта `edited_campaign` для отладки.
3.  Обновляет данные кампании с помощью метода `update_campaign` объекта `campaign_editor`.

## Примеры

### Инициализация и обновление кампании

```python
gs = AliCampaignGoogleSheet('1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0')
campaign_name = "lighting"
language = 'EN'
currency = 'USD'

campaign_editor = AliCampaignEditor(campaign_name, language, currency)
campaign_data = campaign_editor.campaign
_categories: SimpleNamespace = campaign_data.category

categories_dict: dict[str, CategoryType] = {category_name: getattr(_categories, category_name) for category_name in vars(_categories)}
categories_list: list[CategoryType] = list(categories_dict.values())

gs.set_categories(categories_list)
edited_categories: list[dict] = gs.get_categories()

for _cat in edited_categories:
    _cat_ns: SimpleNamespace = SimpleNamespace(**{
        'name':_cat['name'],
        'title':_cat['title'],
        'description':_cat['description'],
        'tags':_cat['tags'],
        'products_count':_cat['products_count']
    }
    )
    logger.info(f"Updating category: {_cat_ns.name}")
    categories_dict[_cat_ns.name] = _cat_ns
    products = campaign_editor.get_category_products(_cat_ns.name)
    gs.set_category_products(_cat_ns.name,products)

_updated_categories = SimpleNamespace(**categories_dict)

pprint(_updated_categories)

campaign_dict: dict = {
    'name': campaign_data.campaign_name,
    'title': campaign_data.title,
    'language': language,
    'currency': currency,
    'category': _updated_categories
}

edited_campaign: SimpleNamespace = SimpleNamespace(**campaign_dict)

pprint(edited_campaign)
campaign_editor.update_campaign(edited_campaign)
```

В этом примере демонстрируется полный цикл обновления данных кампании через Google Sheets. Сначала данные категорий записываются в Google Sheet, затем считываются обратно после редактирования, и, наконец, обновляются данные кампании.