# Модуль gshet-step-by-step.py

## Обзор

Модуль представляет собой эксперимент по работе с Google Sheets для управления кампаниями AliExpress. Он включает в себя чтение, редактирование и обновление категорий товаров в Google Sheets, а также применение этих изменений к кампании.

## Подробней

Этот модуль предназначен для автоматизации процесса управления кампаниями AliExpress с использованием Google Sheets. Он позволяет изменять категории товаров, их названия, описания и теги непосредственно в Google Sheets, а затем применять эти изменения к кампании. Это упрощает процесс обновления и управления большими объемами данных о товарах.

## Функции

### `AliCampaignGoogleSheet`

**Назначение**: Класс для взаимодействия с Google Sheets, содержащим данные о кампаниях AliExpress.

**Параметры**:
- `spreadsheet_id` (str): Идентификатор таблицы Google Sheets.

**Методы**:
- `set_categories(categories_list: list[CategoryType]) -> None`: Записывает список категорий в Google Sheets.
- `get_categories() -> list[dict]`: Считывает отредактированные категории из Google Sheets.
- `set_category_products(category_name: str, products: list) -> None`: Записывает список продуктов для заданной категории в Google Sheets.

**Как работает класс**:
- Класс инициализируется с идентификатором таблицы Google Sheets.
- Метод `set_categories` преобразует список категорий в формат, подходящий для записи в Google Sheets, и записывает их.
- Метод `get_categories` считывает данные из Google Sheets и преобразует их в список словарей.
- Метод `set_category_products` записывает продукты для указанной категории в Google Sheets.

### `AliCampaignEditor`

**Назначение**: Класс для редактирования данных кампании AliExpress.

**Параметры**:
- `campaign_name` (str): Название кампании.
- `language` (str): Язык кампании.
- `currency` (str): Валюта кампании.

**Методы**:
- `get_category_products(category_name: str) -> list`: Возвращает список продуктов для заданной категории.
- `update_campaign(edited_campaign: SimpleNamespace) -> None`: Обновляет данные кампании.

**Как работает класс**:
- Класс инициализируется с названием кампании, языком и валютой.
- Метод `get_category_products` возвращает список продуктов для указанной категории.
- Метод `update_campaign` обновляет данные кампании с использованием предоставленных отредактированных данных.

### Основной блок кода

1.  **Инициализация**:
    *   Создается экземпляр класса `AliCampaignGoogleSheet` для работы с Google Sheets.
    *   Определяются параметры кампании: `campaign_name`, `language`, `currency`.
    *   Создается экземпляр класса `AliCampaignEditor` для редактирования данных кампании.
    *   Получаются данные кампании из `campaign_editor`.

2.  **Работа с категориями**:
    *   Преобразуются категории из формата `SimpleNamespace` в словарь `categories_dict`.
    *   Преобразуются категории в список `categories_list` для записи в Google Sheets.
    *   Устанавливаются категории в Google Sheets с использованием `gs.set_categories(categories_list)`.
    *   Получаются отредактированные категории из Google Sheets с использованием `gs.get_categories()`.

3.  **Обновление категорий**:
    *   Обновляется словарь `categories_dict` с отредактированными данными из Google Sheets.
    *   Для каждой категории обновляются продукты с использованием `campaign_editor.get_category_products(_cat_ns.name)` и записываются в Google Sheets с использованием `gs.set_category_products(_cat_ns.name, products)`.

4.  **Финальные шаги**:
    *   Преобразуется `categories_dict` обратно в `SimpleNamespace` вручную.
    *   Создается словарь для кампании `campaign_dict` с обновленными категориями.
    *   Создается `SimpleNamespace` для отредактированной кампании `edited_campaign`.
    *   Обновляется кампания с использованием `campaign_editor.update_campaign(edited_campaign)`.

```python
gs = AliCampaignGoogleSheet('1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0')
...
campaign_name = "lighting"
language = 'EN'
currency = 'USD'

campaign_editor = AliCampaignEditor(campaign_name, language, currency)
campaign_data = campaign_editor.campaign
_categories: SimpleNamespace = campaign_data.category

# Преобразование _categories в словарь
categories_dict: dict[str, CategoryType] = {category_name: getattr(_categories, category_name) for category_name in vars(_categories)}

# Преобразование категорий в список для Google Sheets
categories_list: list[CategoryType] = list(categories_dict.values())

# Установка категорий в Google Sheet
gs.set_categories(categories_list)

# Получение отредактированных категорий из Google Sheet
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

# Преобразование categories_dict обратно в SimpleNamespace вручную
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
...
```
**Как работает код**:

1.  **Инициализация объектов**:
    *   Создается объект `AliCampaignGoogleSheet` для взаимодействия с Google Sheets. В конструктор передается ID таблицы.
    *   Задаются основные параметры кампании: название, язык и валюта.
    *   Создается объект `AliCampaignEditor`, который будет использоваться для редактирования кампании.

2.  **Работа с категориями**:
    *   Извлекаются категории из данных кампании и преобразуются в словарь `categories_dict`. Это необходимо для удобства дальнейшей работы с категориями.
    *   Категории преобразуются в список `categories_list`, чтобы их можно было записать в Google Sheets.
    *   Вызывается метод `gs.set_categories(categories_list)` для записи категорий в Google Sheets.
    *   Считываются отредактированные категории из Google Sheets с помощью `gs.get_categories()`.

3.  **Обновление данных кампании**:
    *   Происходит итерация по отредактированным категориям, полученным из Google Sheets.
    *   Для каждой категории создается объект `SimpleNamespace` с данными из Google Sheets.
    *   Обновляются продукты для каждой категории с использованием методов `campaign_editor.get_category_products(_cat_ns.name)` и `gs.set_category_products(_cat_ns.name, products)`.
    *   Обновленный словарь категорий преобразуется обратно в `SimpleNamespace`.

4.  **Финальное обновление и вывод**:
    *   Создается словарь `campaign_dict` с обновленными данными кампании.
    *   Из словаря создается объект `SimpleNamespace` `edited_campaign`.
    *   Вызывается метод `campaign_editor.update_campaign(edited_campaign)` для обновления данных кампании.
    *   Используется `pprint` для вывода данных на экран в удобном формате.

**Примеры**:

```python
# Пример инициализации AliCampaignGoogleSheet
gs = AliCampaignGoogleSheet('1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0')

# Пример установки категорий в Google Sheet
categories = [{'name': 'category1', 'title': 'Category 1'}, {'name': 'category2', 'title': 'Category 2'}]
gs.set_categories(categories)

# Пример получения отредактированных категорий из Google Sheet
edited_categories = gs.get_categories()

# Пример обновления кампании
campaign_editor.update_campaign(edited_campaign)