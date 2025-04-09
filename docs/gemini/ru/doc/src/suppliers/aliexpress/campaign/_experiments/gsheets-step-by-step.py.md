# Модуль для экспериментов с Google Sheets в кампаниях AliExpress

## Обзор

Модуль предназначен для экспериментов с Google Sheets в контексте управления кампаниями AliExpress. Он включает в себя настройку категорий продуктов, получение данных из Google Sheets и обновление информации о кампаниях.

## Подробней

Модуль позволяет автоматизировать процесс работы с кампаниями AliExpress, используя Google Sheets для хранения и редактирования данных. Он включает в себя функции для установки категорий, получения отредактированных категорий и обновления информации о кампаниях. Этот код является частью экспериментов, направленных на улучшение процесса управления кампаниями AliExpress через интеграцию с Google Sheets.

## Функции

### `AliCampaignGoogleSheet`

*   **Назначение**: Инициализация класса для работы с Google Sheets, содержащими данные о кампаниях AliExpress.
*   **Параметры**:
    *   `spreadsheet_id` (str): ID таблицы Google Sheets.
*   **Возвращает**: None
*   **Примеры**:

    ```python
    gs = AliCampaignGoogleSheet('1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0')
    ```

### `AliCampaignEditor`

*   **Назначение**: Инициализация редактора кампаний AliExpress.
*   **Параметры**:

    *   `campaign_name` (str): Название кампании.
    *   `language` (str): Язык кампании.
    *   `currency` (str): Валюта кампании.
*   **Возвращает**: None
*   **Примеры**:

    ```python
    campaign_editor = AliCampaignEditor(campaign_name, language, currency)
    ```

### Преобразование \_categories в словарь

*   **Назначение**: Преобразует объект `_categories` (типа `SimpleNamespace`) в словарь, где ключами являются названия категорий, а значениями - объекты типа `CategoryType`.
*   **Параметры**:

    *   `_categories` (SimpleNamespace): Объект, содержащий категории.
*   **Возвращает**:

    *   `dict[str, CategoryType]`: Словарь категорий.
*   **Как работает функция**:

    *   Используется генератор словаря для итерации по атрибутам объекта `_categories` и создания словаря, где ключами являются имена атрибутов (категорий), а значениями - соответствующие объекты `CategoryType`.
*   **Примеры**:

    ```python
    categories_dict: dict[str, CategoryType] = {category_name: getattr(_categories, category_name) for category_name in vars(_categories)}
    ```

### Преобразование категорий в список для Google Sheets

*   **Назначение**: Преобразует словарь категорий в список значений типа `CategoryType`.
*   **Параметры**:

    *   `categories_dict` (dict[str, CategoryType]): Словарь категорий.
*   **Возвращает**:

    *   `list[CategoryType]`: Список категорий.
*   **Как работает функция**:

    *   Используется метод `values()` словаря `categories_dict` для получения коллекции значений (объектов `CategoryType`), которые затем преобразуются в список.
*   **Примеры**:

    ```python
    categories_list: list[CategoryType] = list(categories_dict.values())
    ```

### `gs.set_categories(categories_list)`

*   **Назначение**: Устанавливает список категорий в Google Sheet.
*   **Параметры**:

    *   `categories_list` (list[CategoryType]): Список категорий для установки.
*   **Возвращает**: None
*   **Примеры**:

    ```python
    gs.set_categories(categories_list)
    ```

### `gs.get_categories()`

*   **Назначение**: Получает отредактированные категории из Google Sheet.
*   **Параметры**:

    *   Нет
*   **Возвращает**:

    *   `list[dict]`: Список отредактированных категорий в формате словаря.
*   **Примеры**:

    ```python
    edited_categories: list[dict] = gs.get_categories()
    ```

### Обновление словаря categories\_dict с отредактированными данными

*   **Назначение**: Обновляет словарь `categories_dict` данными из списка отредактированных категорий, полученных из Google Sheets.
*   **Параметры**:

    *   `edited_categories` (list[dict]): Список словарей, содержащих отредактированные данные категорий.
*   **Как работает функция**:

    1.  Итерируется по списку `edited_categories`.
    2.  Для каждого элемента (категории) создается объект `SimpleNamespace` из словаря `_cat`.
    3.  Выполняется логирование имени обновляемой категории.
    4.  Обновляется соответствующая категория в словаре `categories_dict` объектом `_cat_ns`.
    5.  Получает продукты для категории с помощью `campaign_editor.get_category_products(_cat_ns.name)`.
    6.  Устанавливает продукты категории в Google Sheets с помощью `gs.set_category_products(_cat_ns.name, products)`.
*   **Примеры**:

    ```python
    for _cat in edited_categories:
        _cat_ns: SimpleNamespace = SimpleNamespace(**{
            'name':_cat['name'],
            'title':_cat['title'],
            'description':_cat['description'],
            'tags':_cat['tags'],
            'products_count':_cat['products_count']
        })
        logger.info(f"Updating category: {_cat_ns.name}")
        categories_dict[_cat_ns.name] = _cat_ns
        products = campaign_editor.get_category_products(_cat_ns.name)
        gs.set_category_products(_cat_ns.name, products)
    ```

### Преобразование categories\_dict обратно в SimpleNamespace вручную

*   **Назначение**: Преобразует обновленный словарь `categories_dict` обратно в объект `SimpleNamespace`.
*   **Параметры**:

    *   `categories_dict` (dict): Словарь, содержащий обновленные данные категорий.
*   **Возвращает**:

    *   `SimpleNamespace`: Объект `SimpleNamespace`, содержащий категории.
*   **Как работает функция**:

    *   Используется конструктор `SimpleNamespace` для создания объекта из словаря `categories_dict`.
*   **Примеры**:

    ```python
    _updated_categories = SimpleNamespace(**categories_dict)
    ```

### Создание словаря для кампании

*   **Назначение**: Создает словарь, содержащий данные кампании, включая имя, заголовок, язык, валюту и обновленные категории.
*   **Параметры**:

    *   `campaign_data` (SimpleNamespace): Объект, содержащий данные кампании.
    *   `language` (str): Язык кампании.
    *   `currency` (str): Валюта кампании.
    *   `_updated_categories` (SimpleNamespace): Объект, содержащий обновленные категории.
*   **Возвращает**:

    *   `dict`: Словарь с данными кампании.
*   **Как работает функция**:

    *   Создается словарь, где ключами являются атрибуты кампании (`name`, `title`, `language`, `currency`, `category`), а значениями - соответствующие данные из объектов `campaign_data`, `language`, `currency` и `_updated_categories`.
*   **Примеры**:

    ```python
    campaign_dict: dict = {
        'name': campaign_data.campaign_name,
        'title': campaign_data.title,
        'language': language,
        'currency': currency,
        'category': _updated_categories
    }
    ```

### `SimpleNamespace(**campaign_dict)`

*   **Назначение**: Создает объект `SimpleNamespace` из словаря `campaign_dict`, содержащего данные о кампании.
*   **Параметры**:

    *   `campaign_dict` (dict): Словарь, содержащий данные о кампании.
*   **Возвращает**:

    *   `SimpleNamespace`: Объект, содержащий данные о кампании.
*   **Как работает функция**:

    *   Используется конструктор `SimpleNamespace` для создания объекта из словаря `campaign_dict`.
*   **Примеры**:

    ```python
    edited_campaign: SimpleNamespace = SimpleNamespace(**campaign_dict)
    ```

### `campaign_editor.update_campaign(edited_campaign)`

*   **Назначение**: Обновляет данные кампании с использованием объекта `edited_campaign`.
*   **Параметры**:

    *   `edited_campaign` (SimpleNamespace): Объект, содержащий обновленные данные о кампании.
*   **Возвращает**: None
*   **Примеры**:

    ```python
    campaign_editor.update_campaign(edited_campaign)