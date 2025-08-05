# Модуль gshet-step-by-step

## Обзор

Этот модуль предназначен для экспериментов с Google Sheets в контексте кампаний AliExpress. Он включает в себя чтение, редактирование и обновление данных кампаний, категорий и товаров, используя Google Sheets в качестве промежуточного хранилища данных.

## Подробней

Модуль предназначен для работы с данными кампаний AliExpress, используя Google Sheets в качестве промежуточного хранилища. Он позволяет извлекать категории товаров, редактировать их через Google Sheets и затем обновлять данные кампании с учетом внесенных изменений. Это обеспечивает удобный способ для ручного редактирования и управления большими объемами данных.

## Классы

### `AliCampaignGoogleSheet`

**Описание**: Класс для работы с Google Sheets, содержащими данные о кампаниях AliExpress.

### `AliCampaignEditor`

**Описание**: Класс для редактирования данных кампаний AliExpress.

## Функции

### `AliCampaignGoogleSheet`

```python
class AliCampaignGoogleSheet:
    """
    Args:
        spreadsheet_id (str): ID таблицы Google Sheets.
    """
```

### `AliCampaignEditor`

```python
class AliCampaignEditor:
    """
    Args:
        campaign_name (str): Название кампании.
        language (str): Язык кампании.
        currency (str): Валюта кампании.
    """
```

### Основной код

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

**Назначение**:

Основной блок кода выполняет следующие шаги:

1.  Инициализация объектов `AliCampaignGoogleSheet` и `AliCampaignEditor` с необходимыми параметрами (ID таблицы Google Sheets, имя кампании, язык и валюта).
2.  Извлечение данных о категориях из объекта `campaign_data` и преобразование их в словарь, а затем в список для записи в Google Sheets.
3.  Запись списка категорий в Google Sheets с помощью метода `gs.set_categories()`.
4.  Чтение отредактированных категорий из Google Sheets с помощью метода `gs.get_categories()`.
5.  Обновление словаря `categories_dict` данными из Google Sheets. Для каждой категории создается объект `SimpleNamespace` с атрибутами, соответствующими данным из Google Sheets.
6.  Логирование информации об обновляемой категории.
7.  Обновление товаров категории с помощью метода `campaign_editor.get_category_products()` и запись их в Google Sheets с помощью метода `gs.set_category_products()`.
8.  Преобразование обновленного словаря категорий обратно в объект `SimpleNamespace`.
9.  Вывод обновленных категорий и данных кампании с помощью функции `pprint` для отладки.
10. Создание словаря для кампании и обновление данных кампании с использованием отредактированных категорий.
11. Обновление кампании с помощью метода `campaign_editor.update_campaign()`.

**Переменные**:

*   `gs`: Объект класса `AliCampaignGoogleSheet`, предназначенный для работы с Google Sheets.
*   `campaign_name`: Имя кампании (строка).
*   `language`: Язык кампании (строка).
*   `currency`: Валюта кампании (строка).
*   `campaign_editor`: Объект класса `AliCampaignEditor`, предназначенный для редактирования данных кампании.
*   `campaign_data`: Данные кампании.
*   `_categories`: Объект `SimpleNamespace`, содержащий категории кампании.
*   `categories_dict`: Словарь, содержащий категории кампании, где ключ - имя категории, значение - объект `CategoryType`.
*   `categories_list`: Список объектов `CategoryType`, представляющих категории кампании.
*   `edited_categories`: Список словарей, содержащих отредактированные данные категорий из Google Sheets.
*   `_cat`: Итератор по списку `edited_categories`.
*   `_cat_ns`: Объект `SimpleNamespace`, представляющий отредактированную категорию.
*   `_updated_categories`: Объект `SimpleNamespace`, содержащий обновленные категории кампании.
*   `campaign_dict`: Словарь, содержащий данные кампании, включая обновленные категории.
*   `edited_campaign`: Объект `SimpleNamespace`, представляющий отредактированную кампанию.

**Примеры**:

```python
gs = AliCampaignGoogleSheet('1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0')
campaign_name = "lighting"
language = 'EN'
currency = 'USD'
campaign_editor = AliCampaignEditor(campaign_name, language, currency)