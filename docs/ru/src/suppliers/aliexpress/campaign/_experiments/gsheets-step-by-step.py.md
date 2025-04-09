# Модуль для экспериментов с Google Sheets в кампаниях AliExpress

## Обзор

Этот модуль предназначен для экспериментов по интеграции Google Sheets в процесс управления кампаниями AliExpress. Он позволяет автоматизировать чтение и запись данных кампаний, категорий и продуктов, используя Google Sheets в качестве источника данных и инструмента для редактирования. Модуль содержит логику для синхронизации данных между локальными структурами данных кампании и Google Sheets.

## Подробней

Модуль `gsheets-step-by-step.py` предоставляет функциональность для работы с Google Sheets в контексте управления кампаниями на AliExpress. Он включает в себя чтение и запись данных категорий и продуктов кампании, а также механизм обновления данных кампании на основе информации, полученной из Google Sheets.

## Функции

### `AliCampaignGoogleSheet`

**Описание**: Класс для работы с Google Sheets, содержащими данные кампании AliExpress.

**Методы**:
- `__init__`: Инициализирует подключение к Google Sheets.
- `set_categories`: Записывает список категорий в Google Sheet.
- `get_categories`: Получает список категорий из Google Sheet.
- `set_category_products`: Записывает список продуктов для определенной категории в Google Sheet.
- `get_category_products`: Получает список продуктов для определенной категории из Google Sheet.

### `AliCampaignEditor`

**Описание**: Класс для редактирования данных кампании AliExpress.

**Методы**:
- `__init__`: Инициализирует редактор кампании с указанным именем, языком и валютой.
- `get_category_products`: Получает список продуктов для заданной категории.
- `update_campaign`: Обновляет данные кампании.

## Обзор кода

### Создание экземпляров классов `AliCampaignGoogleSheet` и `AliCampaignEditor`

```python
gs = AliCampaignGoogleSheet('1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0')
...
campaign_name = "lighting"
language = 'EN'
currency = 'USD'

campaign_editor = AliCampaignEditor(campaign_name, language, currency)
campaign_data = campaign_editor.campaign
_categories: SimpleNamespace = campaign_data.category
```

- Создается экземпляр класса `AliCampaignGoogleSheet` с указанием идентификатора Google Sheet.
- Определяются параметры кампании: имя, язык и валюта.
- Создается экземпляр класса `AliCampaignEditor` с указанными параметрами.
- Извлекаются данные кампании и категории.

### Преобразование и установка категорий в Google Sheets

```python
categories_dict: dict[str, CategoryType] = {category_name: getattr(_categories, category_name) for category_name in vars(_categories)}

# Преобразование категорий в список для Google Sheets
categories_list: list[CategoryType] = list(categories_dict.values())

# Установка категорий в Google Sheet
gs.set_categories(categories_list)
```

- Преобразование категорий из `SimpleNamespace` в словарь для удобства работы.
- Преобразование словаря категорий в список для записи в Google Sheets.
- Установка списка категорий в Google Sheets с использованием метода `set_categories` класса `AliCampaignGoogleSheet`.

### Получение и обновление категорий из Google Sheets

```python
edited_categories: list[dict] = gs.get_categories()

# Обновление словаря categories_dict с отредактированными данными
for _cat in edited_categories:
    _cat_ns: SimpleNamespace = SimpleNamespace(**{
        'name':_cat['name'],
        'title':_cat['title'],
        'description':_cat['description'],
        'tags':_cat['tags'],
        'products_count':_cat['products_count']
    }
    )
    # Логирование для отладки
    logger.info(f"Updating category: {_cat_ns.name}")
    categories_dict[_cat_ns.name] = _cat_ns
    products = campaign_editor.get_category_products(_cat_ns.name)
    gs.set_category_products(_cat_ns.name,products)
```

- Получение отредактированных категорий из Google Sheets с использованием метода `get_categories` класса `AliCampaignGoogleSheet`.
- Обновление данных в словаре `categories_dict` на основе данных из Google Sheets.
- Для каждой категории создается `SimpleNamespace` и обновляются данные.
- Логирование процесса обновления категорий.
- Получение списка продуктов для каждой категории и запись их в Google Sheets.

### Преобразование и обновление данных кампании

```python
_updated_categories = SimpleNamespace(**categories_dict)

# Вывод данных для отладки
pprint(_updated_categories)

# Создание словаря для кампании
campaign_dict: dict = {
    'name': campaign_data.campaign_name,
    'title': campaign_data.title,
    'language': language,
    'currency': currency,
    'category': _updated_categories
}

edited_campaign: SimpleNamespace = SimpleNamespace(**campaign_dict)

# Пример использования pprint для вывода данных
pprint(edited_campaign)
campaign_editor.update_campaign(edited_campaign)
```

- Преобразование обновленного словаря категорий обратно в `SimpleNamespace`.
- Создание словаря для кампании с обновленными данными категорий.
- Создание `SimpleNamespace` для отредактированной кампании.
- Вывод данных кампании для отладки.
- Обновление данных кампании с использованием метода `update_campaign` класса `AliCampaignEditor`.

## Функции

### `categories_dict: dict[str, CategoryType]`

**Назначение**: Преобразование категорий из `SimpleNamespace` в словарь.

**Параметры**:
- Отсутствуют явные параметры, функция использует переменные из окружающей области видимости.

**Возвращает**:
- `dict[str, CategoryType]`: Словарь, где ключи - имена категорий, а значения - объекты `CategoryType`.

**Как работает функция**:
1. Извлекает имена атрибутов из объекта `_categories`.
2. Для каждого имени атрибута получает соответствующий атрибут из `_categories` с помощью `getattr`.
3. Создает словарь, где ключом является имя категории, а значением - соответствующий объект `CategoryType`.

```
_categories (SimpleNamespace) --> vars(_categories) --> category_name --> getattr(_categories, category_name) --> categories_dict (dict)
```

**Примеры**:

```python
# Пример: Допустим, _categories имеет атрибуты 'lighting' и 'furniture'
# categories_dict будет содержать {'lighting': <CategoryType object>, 'furniture': <CategoryType object>}
```

### `edited_categories: list[dict]`

**Назначение**: Получение отредактированных категорий из Google Sheets.

**Параметры**:
- Отсутствуют явные параметры, функция использует `gs` (экземпляр `AliCampaignGoogleSheet`).

**Возвращает**:
- `list[dict]`: Список словарей, представляющих отредактированные категории.

**Как работает функция**:
1. Вызывает метод `gs.get_categories()`, который обращается к Google Sheets и извлекает данные категорий.
2. Возвращает список словарей, содержащих информацию о категориях.

```
gs (AliCampaignGoogleSheet) --> gs.get_categories() --> edited_categories (list[dict])
```

**Примеры**:

```python
# Пример: edited_categories может содержать
# [{'name': 'lighting', 'title': 'Lighting Solutions', ...}, {'name': 'furniture', 'title': 'Furniture', ...}]
```

### `_cat_ns: SimpleNamespace`

**Назначение**: Преобразование данных категории из словаря в `SimpleNamespace`.

**Параметры**:
- Отсутствуют явные параметры, функция использует `_cat` (словарь с данными категории).

**Возвращает**:
- `SimpleNamespace`: Объект `SimpleNamespace`, содержащий данные категории.

**Как работает функция**:
1. Принимает словарь `_cat`, содержащий данные категории.
2. Создает `SimpleNamespace` с атрибутами, соответствующими ключам и значениям словаря.

```
_cat (dict) --> SimpleNamespace(**_cat) --> _cat_ns (SimpleNamespace)
```

**Примеры**:

```python
# Пример: _cat может содержать {'name': 'lighting', 'title': 'Lighting Solutions', ...}
# _cat_ns будет объектом SimpleNamespace с атрибутами _cat_ns.name, _cat_ns.title и т.д.
```

### `campaign_dict: dict`

**Назначение**: Создание словаря для представления данных кампании.

**Параметры**:
- Отсутствуют явные параметры, функция использует `campaign_data`, `language`, `currency` и `_updated_categories`.

**Возвращает**:
- `dict`: Словарь, содержащий данные кампании.

**Как работает функция**:
1. Создает словарь, содержащий имя, заголовок, язык, валюту и категории кампании.
2. Данные берутся из `campaign_data`, `language`, `currency` и `_updated_categories`.

```
campaign_data, language, currency, _updated_categories --> campaign_dict (dict)
```

**Примеры**:

```python
# Пример: campaign_dict может содержать
# {'name': 'lighting', 'title': 'Lighting Campaign', 'language': 'EN', 'currency': 'USD', 'category': <SimpleNamespace object>}
```

### `edited_campaign: SimpleNamespace`

**Назначение**: Преобразование данных кампании из словаря в `SimpleNamespace`.

**Параметры**:
- Отсутствуют явные параметры, функция использует `campaign_dict`.

**Возвращает**:
- `SimpleNamespace`: Объект `SimpleNamespace`, содержащий данные кампании.

**Как работает функция**:
1. Принимает словарь `campaign_dict`, содержащий данные кампании.
2. Создает `SimpleNamespace` с атрибутами, соответствующими ключам и значениям словаря.

```
campaign_dict (dict) --> SimpleNamespace(**campaign_dict) --> edited_campaign (SimpleNamespace)
```

**Примеры**:

```python
# Пример: campaign_dict может содержать
# {'name': 'lighting', 'title': 'Lighting Campaign', 'language': 'EN', 'currency': 'USD', 'category': <SimpleNamespace object>}
# edited_campaign будет объектом SimpleNamespace с атрибутами edited_campaign.name, edited_campaign.title и т.д.
```