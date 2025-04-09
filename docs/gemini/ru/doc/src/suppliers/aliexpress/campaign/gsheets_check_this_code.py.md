# Модуль для работы с Google Sheets в рамках кампаний AliExpress

## Обзор

Модуль `gsheets_check_this_code.py` предназначен для интеграции с Google Sheets для управления рекламными кампаниями на AliExpress. Он предоставляет функциональность для создания, редактирования и форматирования Google Sheets, содержащих информацию о кампаниях, категориях и продуктах.

## Подробней

Модуль содержит класс `AliCampaignGoogleSheet`, который наследует класс `SpreadSheet` и расширяет его функциональность для работы с данными кампаний AliExpress. Он позволяет автоматизировать процесс заполнения и обновления данных в Google Sheets, что упрощает управление рекламными кампаниями.

## Классы

### `AliCampaignGoogleSheet`

**Описание**: Класс для работы с Google Sheets в рамках кампаний AliExpress.

**Наследует**: `SpreadSheet`

**Атрибуты**:

- `spreadsheet_id` (str): ID Google Sheets spreadsheet.
- `spreadsheet` (SpreadSheet): Экземпляр класса `SpreadSheet` для работы с Google Sheets.
- `worksheet` (Worksheet): Текущий рабочий лист Google Sheets.
- `driver` (Driver): Драйвер для управления браузером. По умолчанию используется `Chrome`.
- `editor` (AliCampaignEditor): Редактор кампании AliExpress.

**Методы**:

- `__init__(campaign_name: str, language: str | dict = None, currency: str = None)`: Инициализирует класс `AliCampaignGoogleSheet`.
- `clear()`: Очищает содержимое Google Sheets.
- `delete_products_worksheets()`: Удаляет все листы продуктов из Google Sheets.
- `set_campaign_worksheet(campaign: SimpleNamespace)`: Записывает данные кампании в Google Sheets.
- `set_products_worksheet(category_name: str)`: Записывает данные о продуктах в Google Sheets.
- `set_categories_worksheet(categories: SimpleNamespace)`: Записывает данные о категориях в Google Sheets.
- `get_categories()`: Получает данные о категориях из Google Sheets.
- `set_category_products(category_name: str, products: dict)`: Записывает данные о продуктах категории в Google Sheets.
- `_format_categories_worksheet(ws: Worksheet)`: Форматирует лист с категориями.
- `_format_category_products_worksheet(ws: Worksheet)`: Форматирует лист с продуктами категории.

## Методы класса

### `__init__`

```python
def __init__(self, campaign_name: str, language: str | dict = None, currency: str = None):
    """ Initialize AliCampaignGoogleSheet with specified Google Sheets spreadsheet ID and additional parameters.
    @param campaign_name `str`: The name of the campaign.
    @param category_name `str`: The name of the category.   
    @param language `str`: The language for the campaign.
    @param currency `str`: The currency for the campaign.
    """
    # Initialize SpreadSheet with the spreadsheet ID
    super().__init__(spreadsheet_id=self.spreadsheet_id)
    self.editor = AliCampaignEditor(campaign_name=campaign_name, language=language, currency=currency)
    self.clear()
    self.set_campaign_worksheet(self.editor.campaign)
    self.set_categories_worksheet(self.editor.campaign.category)
    self.driver.get_url(f'https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}')
```

**Назначение**: Инициализирует класс `AliCampaignGoogleSheet`, настраивая параметры кампании, очищая старые данные и подготавливая листы Google Sheets.

**Параметры**:

- `campaign_name` (str): Название кампании.
- `language` (str | dict, optional): Язык кампании. По умолчанию `None`.
- `currency` (str, optional): Валюта кампании. По умолчанию `None`.

**Как работает функция**:

1. Вызывает конструктор родительского класса `SpreadSheet` с указанным `spreadsheet_id`.
2. Инициализирует редактор кампании `AliCampaignEditor` с переданными параметрами.
3. Очищает существующие данные, вызывая метод `clear`.
4. Устанавливает лист кампании, записывая данные кампании с помощью метода `set_campaign_worksheet`.
5. Устанавливает лист категорий, записывая данные о категориях с помощью метода `set_categories_worksheet`.
6. Открывает Google Sheets в браузере, используя `driver.get_url`.

**Примеры**:

```python
campaign = AliCampaignGoogleSheet(campaign_name='SummerSale', language='ru', currency='USD')
```

### `clear`

```python
def clear(self):
    """ Clear contents.
    Delete product sheets and clear data on the categories and other specified sheets.
    """
    try:
        self.delete_products_worksheets()
    except Exception as ex:
        logger.error("Ошибка очистки", ex)
```

**Назначение**: Очищает содержимое Google Sheets, удаляя листы продуктов и очищая данные на листах категорий и других указанных листах.

**Как работает функция**:

1. Пытается удалить листы продуктов, вызывая метод `delete_products_worksheets`.
2. Если возникает исключение при удалении листов, логирует ошибку с помощью `logger.error`.

**Примеры**:

```python
campaign = AliCampaignGoogleSheet(campaign_name='SummerSale')
campaign.clear()
```

### `delete_products_worksheets`

```python
def delete_products_worksheets(self):
    """ Delete all sheets from the Google Sheets spreadsheet except 'categories' and 'product_template'.
    """
    excluded_titles = {'categories', 'product', 'category', 'campaign'}
    try:
        worksheets = self.spreadsheet.worksheets()
        for sheet in worksheets:
            if sheet.title not in excluded_titles:
                self.spreadsheet.del_worksheet_by_id(sheet.id)
                logger.success(f"Worksheet '{sheet.title}' deleted.")
    except Exception as ex:
        logger.error("Error deleting all worksheets.", ex, exc_info=True)
        raise
```

**Назначение**: Удаляет все листы из Google Sheets, кроме листов с названиями 'categories', 'product', 'category', 'campaign'.

**Как работает функция**:

1. Определяет набор `excluded_titles`, содержащий названия листов, которые не нужно удалять.
2. Получает список всех листов в Google Sheets с помощью `self.spreadsheet.worksheets()`.
3. Итерируется по листам и удаляет каждый лист, название которого отсутствует в `excluded_titles`, используя `self.spreadsheet.del_worksheet_by_id`.
4. Логирует успешное удаление каждого листа с помощью `logger.success`.
5. Если возникает исключение, логирует ошибку с помощью `logger.error` и вызывает исключение повторно.

**Примеры**:

```python
campaign = AliCampaignGoogleSheet(campaign_name='SummerSale')
campaign.delete_products_worksheets()
```

### `set_campaign_worksheet`

```python
def set_campaign_worksheet(self, campaign: SimpleNamespace):
    """ Write campaign data to a Google Sheets worksheet.
    @param campaign `SimpleNamespace | str`: SimpleNamespace object with campaign data fields for writing.
    @param language `str`: Optional language parameter.
    @param currency `str`: Optional currency parameter.
    """
    try:
        ws: Worksheet = self.get_worksheet('campaign')  # Clear the 'campaign' worksheet

        # Prepare data for vertical writing
        updates = []
        vertical_data = [
            ('A1', 'Campaign Name', campaign.name),
            ('A2', 'Campaign Title', campaign.title),
            ('A3', 'Campaign Language', campaign.language),
            ('A4', 'Campaign Currency', campaign.currency),
            ('A5', 'Campaign Description', campaign.description),              

        ]

        # Add update operations to batch_update list
        for cell, header, value in vertical_data:
            updates.append({'range': cell, 'values': [[header]]})
            updates.append({'range': f'B{cell[1]}', 'values': [[str(value)]]})

        # Perform batch update
        if updates:
            ws.batch_update(updates)

        logger.info("Campaign data written to 'campaign' worksheet vertically.")

    except Exception as ex:
        logger.error("Error setting campaign worksheet.", ex, exc_info=True)
        raise
```

**Назначение**: Записывает данные кампании в Google Sheets на лист 'campaign'.

**Параметры**:

- `campaign` (SimpleNamespace): Объект SimpleNamespace с данными кампании.

**Как работает функция**:

1. Получает лист 'campaign' из Google Sheets с помощью `self.get_worksheet`.
2. Подготавливает данные для записи в виде списка кортежей, содержащих ячейку, заголовок и значение.
3. Формирует список операций обновления `updates` для пакетной записи данных.
4. Выполняет пакетное обновление листа с помощью `ws.batch_update`.
5. Логирует успешную запись данных с помощью `logger.info`.
6. Если возникает исключение, логирует ошибку с помощью `logger.error` и вызывает исключение повторно.

**Примеры**:

```python
from types import SimpleNamespace
campaign_data = SimpleNamespace(name='SummerSale', title='Летняя распродажа', language='ru', currency='USD', description='Распродажа летних товаров')
campaign = AliCampaignGoogleSheet(campaign_name='SummerSale')
campaign.set_campaign_worksheet(campaign_data)
```

### `set_products_worksheet`

```python
def set_products_worksheet(self, category_name: str):
    """ Write data from a list of SimpleNamespace objects to Google Sheets cells.
    @param category_name `str`: The name of the category to fetch products from.
    """
    if category_name:
        category: SimpleNamespace = getattr(self.editor.campaign.category, category_name)
        products: list[SimpleNamespace] = category.products
    else:
        logger.warning("No products found for category.")
        return

    ws = self.copy_worksheet('product', category_name)

    try:
        # headers = [
        #     'product_id', 'app_sale_price', 'original_price', 'sale_price', 'discount',
        #     'product_main_image_url', 'local_image_path', 'product_small_image_urls',
        #     'product_video_url', 'local_video_path', 'first_level_category_id',
        #     'first_level_category_name', 'second_level_category_id', 'second_level_category_name',
        #     'target_sale_price', 'target_sale_price_currency', 'target_app_sale_price_currency',
        #     'target_original_price_currency', 'original_price_currency', 'product_title',
        #     'evaluate_rate', 'promotion_link', 'shop_url', 'shop_id', 'tags'
        # ]
        # updates = [{'range': 'A1:Y1', 'values': [headers]}]  # Add headers to the worksheet

        row_data = []
        for product in products:
            _ = product.__dict__
            row_data.append([
                str(_.get('product_id')),
                _.get('product_title'),
                _.get('promotion_link'),
                str(_.get('app_sale_price')),
                _.get('original_price'),
                _.get('sale_price'),
                _.get('discount'),
                _.get('product_main_image_url'),
                _.get('local_image_path'),
                ', '.join(_.get('product_small_image_urls', [])),
                _.get('product_video_url'),
                _.get('local_video_path'),
                _.get('first_level_category_id'),
                _.get('first_level_category_name'),
                _.get('second_level_category_id'),
                _.get('second_level_category_name'),
                _.get('target_sale_price'),
                _.get('target_sale_price_currency'),
                _.get('target_app_sale_price_currency'),
                _.get('target_original_price_currency'),
                _.get('original_price_currency'),
                
                _.get('evaluate_rate'),
                
                _.get('shop_url'),
                _.get('shop_id'),
                ', '.join(_.get('tags', []))
            ])
        
        for index, row in enumerate(row_data, start=2):
            ws.update(f'A{index}:Y{index}', [row])
            logger.info(f"Products {str(_.get('product_id'))} updated .")

        self._format_category_products_worksheet(ws)

        logger.info("Products updated in worksheet.")


    except Exception as ex:
        logger.error("Error setting products worksheet.", ex, exc_info=True)
        raise
```

**Назначение**: Записывает данные о продуктах из SimpleNamespace в Google Sheets.

**Параметры**:

- `category_name` (str): Название категории, продукты которой нужно записать.

**Как работает функция**:

1. Проверяет, передано ли имя категории. Если нет, логирует предупреждение и завершает выполнение.
2. Получает объект категории из `self.editor.campaign.category` с помощью `getattr`.
3. Получает список продуктов из категории.
4. Копирует лист 'product' в новый лист с именем категории с помощью `self.copy_worksheet`.
5. Формирует список данных о продуктах для записи в Google Sheets.
6. Записывает данные каждого продукта в отдельную строку листа, начиная со второй строки.
7. Логирует информацию об обновлении каждого продукта.
8. Вызывает метод `self._format_category_products_worksheet` для форматирования листа.
9. Логирует сообщение об успешном обновлении продуктов.
10. Если возникает исключение, логирует ошибку и вызывает исключение повторно.

**Примеры**:

```python
campaign = AliCampaignGoogleSheet(campaign_name='SummerSale')
campaign.set_products_worksheet(category_name='shoes')
```

### `set_categories_worksheet`

```python
def set_categories_worksheet(self, categories: SimpleNamespace):
    """ Запись данных из объекта SimpleNamespace с категориями в ячейки Google Sheets.
    @param categories `SimpleNamespace`: Объект, где ключи — это категории с данными для записи.
    """
    ws: Worksheet = self.get_worksheet('categories')
    ws.clear()  # Очистка рабочей таблицы перед записью данных

    try:
        # Получение всех ключей (категорий) и соответствующих значений
        category_data = categories.__dict__

        # Проверка, что все объекты категории имеют необходимые атрибуты
        required_attrs = ['name', 'title', 'description', 'tags', 'products_count']

        if all(all(hasattr(category, attr) for attr in required_attrs) for category in category_data.values()):
            # Заголовки для таблицы
            headers = ['Name', 'Title', 'Description', 'Tags', 'Products Count']
            ws.update('A1:E1', [headers])
        
            # Подготовка данных для записи
            rows = []
            for category in category_data.values():
                row_data = [
                    category.name,
                    category.title,
                    category.description,
                    ', '.join(category.tags),
                    category.products_count,
                ]
                rows.append(row_data)
        
            # Обновляем строки данных
            ws.update(f'A2:E{1 + len(rows)}', rows)
        
            # Форматируем таблицу
            self._format_categories_worksheet(ws)
        
            logger.info("Category fields updated from SimpleNamespace object.")
        else:
            logger.warning("One or more category objects do not contain all required attributes.")

    except Exception as ex:
        logger.error("Error updating fields from SimpleNamespace object.", ex, exc_info=True)
        raise
```

**Назначение**: Записывает данные о категориях из объекта SimpleNamespace в Google Sheets на лист 'categories'.

**Параметры**:

- `categories` (SimpleNamespace): Объект SimpleNamespace, содержащий данные о категориях.

**Как работает функция**:

1. Получает лист 'categories' из Google Sheets с помощью `self.get_worksheet`.
2. Очищает содержимое листа с помощью `ws.clear()`.
3. Получает словарь с данными категорий из объекта `categories.__dict__`.
4. Проверяет, что все объекты категорий имеют необходимые атрибуты ('name', 'title', 'description', 'tags', 'products_count').
5. Записывает заголовки таблицы в первую строку листа.
6. Формирует список данных для записи в Google Sheets.
7. Записывает данные о категориях в лист.
8. Вызывает метод `self._format_categories_worksheet` для форматирования листа.
9. Логирует успешную запись данных или предупреждение, если не все атрибуты присутствуют.
10. Если возникает исключение, логирует ошибку и вызывает исключение повторно.

**Примеры**:

```python
from types import SimpleNamespace
category1 = SimpleNamespace(name='shoes', title='Обувь', description='Различная обувь для всех случаев', tags=['обувь', 'кроссовки', 'ботинки'], products_count=100)
category2 = SimpleNamespace(name='bags', title='Сумки', description='Сумки для мужчин и женщин', tags=['сумки', 'рюкзаки', 'клатчи'], products_count=50)
categories_data = SimpleNamespace(**{'shoes': category1, 'bags': category2})

campaign = AliCampaignGoogleSheet(campaign_name='SummerSale')
campaign.set_categories_worksheet(categories_data)
```

### `get_categories`

```python
def get_categories(self):
    """ Получение данных из таблицы Google Sheets.
    @return Данные из таблицы в виде списка словарей.
    """
    ws = self.get_worksheet('categories') 
    data = ws.get_all_records()
    logger.info("Categories data retrieved from worksheet.")
    return data
```

**Назначение**: Получает данные о категориях из Google Sheets.

**Возвращает**:

- `list[dict]`: Список словарей, где каждый словарь представляет собой строку таблицы.

**Как работает функция**:

1. Получает лист 'categories' из Google Sheets с помощью `self.get_worksheet`.
2. Получает все записи из листа с помощью `ws.get_all_records()`.
3. Логирует информацию об успешном получении данных.
4. Возвращает полученные данные.

**Примеры**:

```python
campaign = AliCampaignGoogleSheet(campaign_name='SummerSale')
categories = campaign.get_categories()
print(categories)
```

### `set_category_products`

```python
def set_category_products(self, category_name: str, products: dict):
    """ Запись данных о продуктах в новую таблицу Google Sheets.
    @param category_name Название категории.
    @param products Словарь с данными о продуктах.
    """
    if category_name:
        category_ns: SimpleNamespace = getattr(self.editor.campaign.category, category_name)
        products_ns: list[SimpleNamespace] = category_ns.products
    else:
        logger.warning("No products found for category.")
        return
    
    ws = self.copy_worksheet('product', category_name)
    try:
        headers = [
            'product_id', 'app_sale_price', 'original_price', 'sale_price', 'discount',
            'product_main_image_url', 'local_image_path', 'product_small_image_urls',
            'product_video_url', 'local_video_path', 'first_level_category_id',
            'first_level_category_name', 'second_level_category_id', 'second_level_category_name',
            'target_sale_price', 'target_sale_price_currency', 'target_app_sale_price_currency',
            'target_original_price_currency', 'original_price_currency', 'product_title',
            'evaluate_rate', 'promotion_link', 'shop_url', 'shop_id', 'tags'
        ]
        updates = [{'range': 'A1:Y1', 'values': [headers]}]  # Add headers to the worksheet

        row_data = []
        for product in products:
            _ = product.__dict__
            row_data.append([
                str(_.get('product_id')),
                str(_.get('app_sale_price')),
                _.get('original_price'),
                _.get('sale_price'),
                _.get('discount'),
                _.get('product_main_image_url'),
                _.get('local_image_path'),
                ', '.join(_.get('product_small_image_urls', [])),
                _.get('product_video_url'),
                _.get('local_video_path'),
                _.get('first_level_category_id'),
                _.get('first_level_category_name'),
                _.get('second_level_category_id'),
                _.get('second_level_category_name'),
                _.get('target_sale_price'),
                _.get('target_sale_price_currency'),
                _.get('target_app_sale_price_currency'),
                _.get('target_original_price_currency'),
                _.get('original_price_currency'),
                _.get('product_title'),
                _.get('evaluate_rate'),
                _.get('promotion_link'),
                _.get('shop_url'),
                _.get('shop_id'),
                ', '.join(_.get('tags', []))
            ])
        
        for index, row in enumerate(row_data, start=2):
            ws.update(f'A{index}:Y{index}', [row])
            logger.info(f"Products {str(_.get('product_id'))} updated .")

        self._format_category_products_worksheet(ws)

        logger.info("Products updated in worksheet.")
    except Exception as ex:
        logger.error("Error updating products in worksheet.", ex, exc_info=True)
        raise
```

**Назначение**: Записывает данные о продуктах в новую таблицу Google Sheets.

**Параметры**:

- `category_name` (str): Название категории.
- `products` (dict): Словарь с данными о продуктах.

**Как работает функция**:

1. Проверяет, передано ли имя категории. Если нет, логирует предупреждение и завершает выполнение.
2. Получает объект категории из `self.editor.campaign.category` с помощью `getattr`.
3. Получает список продуктов из категории.
4. Копирует лист 'product' в новый лист с именем категории с помощью `self.copy_worksheet`.
5. Определяет заголовки таблицы.
6. Формирует список данных о продуктах для записи в Google Sheets.
7. Записывает данные каждого продукта в отдельную строку листа, начиная со второй строки.
8. Логирует информацию об обновлении каждого продукта.
9. Вызывает метод `self._format_category_products_worksheet` для форматирования листа.
10. Логирует сообщение об успешном обновлении продуктов.
11. Если возникает исключение, логирует ошибку и вызывает исключение повторно.

**Примеры**:

```python
campaign = AliCampaignGoogleSheet(campaign_name='SummerSale')
products_data = [{'product_id': 1, 'product_title': 'Кроссовки', 'app_sale_price': 50.0}, {'product_id': 2, 'product_title': 'Ботинки', 'app_sale_price': 80.0}]
campaign.set_category_products(category_name='shoes', products=products_data)
```

### `_format_categories_worksheet`

```python
def _format_categories_worksheet(self, ws: Worksheet):
    """ Форматирование листа 'categories'.
    @param ws Лист Google Sheets для форматирования.
    """
    try:
        # Установка ширины столбцов
        set_column_width(ws, 'A:A', 150)  # Ширина столбца A
        set_column_width(ws, 'B:B', 200)  # Ширина столбца B
        set_column_width(ws, 'C:C', 300)  # Ширина столбца C
        set_column_width(ws, 'D:D', 200)  # Ширина столбца D
        set_column_width(ws, 'E:E', 150)  # Ширина столбца E
        
        # Установка высоты строк
        set_row_height(ws, '1:1', 40)  # Высота заголовков

        # Форматирование заголовков
        header_format = cellFormat(
            textFormat=textFormat(bold=True, fontSize=12),
            horizontalAlignment='CENTER',
            verticalAlignment='MIDDLE',  # Добавлено вертикальное выравнивание
            backgroundColor=Color(0.8, 0.8, 0.8)  # Используем Color для задания цвета
        )
        format_cell_range(ws, 'A1:E1', header_format)

        logger.info("Categories worksheet formatted.")
    except Exception as ex:
        logger.error("Error formatting categories worksheet.", ex, exc_info=True)
        raise
```

**Назначение**: Форматирует лист 'categories' в Google Sheets.

**Параметры**:

- `ws` (Worksheet): Лист Google Sheets для форматирования.

**Как работает функция**:

1. Устанавливает ширину столбцов A, B, C, D и E.
2. Устанавливает высоту первой строки (заголовков).
3. Определяет формат заголовков, включая жирный шрифт, размер шрифта, выравнивание и цвет фона.
4. Применяет формат к диапазону ячеек A1:E1.
5. Логирует информацию об успешном форматировании листа.
6. Если возникает исключение, логирует ошибку и вызывает исключение повторно.

**Примеры**:

```python
campaign = AliCampaignGoogleSheet(campaign_name='SummerSale')
ws = campaign.get_worksheet('categories')
campaign._format_categories_worksheet(ws)
```

### `_format_category_products_worksheet`

```python
def _format_category_products_worksheet(self, ws: Worksheet):
    """ Форматирование листа с продуктами категории.
    @param ws Лист Google Sheets для форматирования.
    """
    try:
        # Установка ширины столбцов
        set_column_width(ws, 'A:A', 250)  # Ширина столбца A
        set_column_width(ws, 'B:B', 220)  # Ширина столбца B
        set_column_width(ws, 'C:C', 220)  # Ширина столбца C
        set_column_width(ws, 'D:D', 220)  # Ширина столбца D
        set_column_width(ws, 'E:E', 200)  # Ширина столбца E
        set_column_width(ws, 'F:F', 200)  # Ширина столбца F
        set_column_width(ws, 'G:G', 200)  # Ширина столбца G
        set_column_width(ws, 'H:H', 200)  # Ширина столбца H
        set_column_width(ws, 'I:I', 200)  # Ширина столбца I
        set_column_width(ws, 'J:J', 200)  # Ширина столбца J
        set_column_width(ws, 'K:K', 200)  # Ширина столбца K
        set_column_width(ws, 'L:L', 200)  # Ширина столбца L
        set_column_width(ws, 'M:M', 200)  # Ширина столбца M
        set_column_width(ws, 'N:N', 200)  # Ширина столбца N
        set_column_width(ws, 'O:O', 200)  # Ширина столбца O
        set_column_width(ws, 'P:P', 200)  # Ширина столбца P
        set_column_width(ws, 'Q:Q', 200)  # Ширина столбца Q
        set_column_width(ws, 'R:R', 200)  # Ширина столбца R
        set_column_width(ws, 'S:S', 200)  # Ширина столбца S
        set_column_width(ws, 'T:T', 200)  # Ширина столбца T
        set_column_width(ws, 'U:U', 200)  # Ширина столбца U
        set_column_width(ws, 'V:V', 200)  # Ширина столбца V
        set_column_width(ws, 'W:W', 200)  # Ширина столбца W
        set_column_width(ws, 'X:X', 200)  # Ширина столбца X
        set_column_width(ws, 'Y:Y', 200)  # Ширина столбца Y

        # Установка высоты строк
        set_row_height(ws, '1:1', 40)  # Высота заголовков

        # Форматирование заголовков
        header_format = cellFormat(
            textFormat=textFormat(bold=True, fontSize=12),
            horizontalAlignment='CENTER',
            verticalAlignment='TOP',  # Добавлено вертикальное выравнивание
            backgroundColor=Color(0.8, 0.8, 0.8)  # Используем Color для задания цвета
        )
        format_cell_range(ws, 'A1:Y1', header_format)

        logger.info("Category products worksheet formatted.")
    except Exception as ex:
        logger.error("Error formatting category products worksheet.", ex, exc_info=True)
        raise
```

**Назначение**: Форматирует лист с продуктами категории в Google Sheets.

**Параметры**:

- `ws` (Worksheet): Лист Google Sheets для форматирования.

**Как работает функция**:

1. Устанавливает ширину столбцов от A до Y.
2. Устанавливает высоту первой строки (заголовков).
3. Определяет формат заголовков, включая жирный шрифт, размер шрифта, выравнивание и цвет фона.
4. Применяет формат к диапазону ячеек A1:Y1.
5. Логирует информацию об успешном форматировании листа.
6. Если возникает исключение, логирует ошибку и вызывает исключение повторно.

**Примеры**:

```python
campaign = AliCampaignGoogleSheet(campaign_name='SummerSale')
ws = campaign.get_worksheet('shoes')
campaign._format_category_products_worksheet(ws)
```