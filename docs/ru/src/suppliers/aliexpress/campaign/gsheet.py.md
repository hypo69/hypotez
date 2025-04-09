# Модуль для работы с Google Sheets в рамках кампаний AliExpress

## Обзор

Модуль `gsheet.py` предоставляет класс `AliCampaignGoogleSheet` для работы с Google Sheets при управлении рекламными кампаниями на AliExpress. Он наследует класс `SpreadSheet` и добавляет функциональность для управления листами, записи данных о категориях и продуктах, а также форматирования листов.

## Подробнее

Модуль предназначен для автоматизации работы с Google Sheets, используемыми для хранения и управления данными рекламных кампаний AliExpress. Он обеспечивает удобный интерфейс для записи и чтения данных, а также для форматирования листов в соответствии с требованиями.

## Классы

### `AliCampaignGoogleSheet`

**Описание**: Класс для работы с Google Sheets в рамках кампаний AliExpress.

**Наследует**: `SpreadSheet`

**Атрибуты**:

- `spreadsheet_id` (str): Идентификатор Google Sheets spreadsheet.
- `spreadsheet` (SpreadSheet): Экземпляр класса `SpreadSheet` для работы с Google Sheets.
- `worksheet` (Worksheet): Экземпляр класса `Worksheet` для работы с конкретным листом Google Sheets.

**Методы**:

- `__init__(self, campaign_name: str, language: str | dict = None, currency: str = None)`: Инициализирует экземпляр класса `AliCampaignGoogleSheet`.
- `clear(self)`: Очищает содержимое листов продуктов, категорий и других указанных листов.
- `delete_products_worksheets(self)`: Удаляет все листы, кроме 'categories', 'product', 'category', 'campaign'.
- `set_campaign_worksheet(self, campaign: SimpleNamespace, language: str = None, currency: str = None)`: Записывает данные кампании на лист Google Sheets.
- `set_products_worksheet(self, category_name: str)`: Записывает данные о продуктах на лист Google Sheets.
- `set_categories_worksheet(self, categories: SimpleNamespace)`: Записывает данные о категориях на лист Google Sheets.
- `get_categories(self)`: Получает данные о категориях из таблицы Google Sheets.
- `set_category_products(self, category_name: str, products: dict)`: Записывает данные о продуктах категории в таблицу Google Sheets.
- `_format_categories_worksheet(self, ws: Worksheet)`: Форматирует лист 'categories'.
- `_format_category_products_worksheet(self, ws: Worksheet)`: Форматирует лист с продуктами категории.

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
    super().__init__(spreadsheet_id = self.spreadsheet_id)
    #self.capmaign_editor = AliCampaignEditor(campaign_name=campaign_name, language=language, currency=currency)
    # if campaign_editor:
    #     self.set_campaign_worksheet(campaign_editor.campaign)
    #     self.set_categories_worksheet(campaign_editor.campaign.category)
```

**Назначение**: Инициализирует экземпляр класса `AliCampaignGoogleSheet`.

**Параметры**:

- `campaign_name` (str): Имя кампании.
- `language` (str | dict, optional): Язык кампании. По умолчанию `None`.
- `currency` (str, optional): Валюта кампании. По умолчанию `None`.

**Как работает функция**:

1. Вызывает конструктор родительского класса `SpreadSheet` с идентификатором spreadsheet.
2. Инициализирует экземпляр класса `AliCampaignGoogleSheet` с заданными параметрами.

**Примеры**:

```python
campaign_gsheet = AliCampaignGoogleSheet(campaign_name='test_campaign', language='ru', currency='USD')
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

**Назначение**: Очищает содержимое листов продуктов, категорий и других указанных листов.

**Как работает функция**:

1. Вызывает метод `delete_products_worksheets` для удаления листов продуктов.
2. Обрабатывает исключение, если возникает ошибка при очистке, и логирует ошибку.

**Примеры**:

```python
campaign_gsheet.clear()
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

**Назначение**: Удаляет все листы из Google Sheets, кроме 'categories', 'product', 'category', 'campaign'.

**Как работает функция**:

1. Определяет список листов, которые не нужно удалять (`excluded_titles`).
2. Получает список всех листов в Google Sheets.
3. Перебирает листы и удаляет те, которые не входят в список исключений.
4. Логирует информацию об удаленных листах.
5. Обрабатывает исключение, если возникает ошибка при удалении листов, и логирует ошибку.

**Примеры**:

```python
campaign_gsheet.delete_products_worksheets()
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
            ('A1', 'Campaign Name', campaign.campaign_name),
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

**Назначение**: Записывает данные кампании на лист Google Sheets.

**Параметры**:

- `campaign` (SimpleNamespace): Объект SimpleNamespace с данными кампании для записи.

**Как работает функция**:

1. Получает лист 'campaign' из Google Sheets.
2. Формирует список операций обновления для записи данных кампании в вертикальном формате.
3. Выполняет пакетное обновление листа с данными кампании.
4. Логирует информацию об успешной записи данных кампании.
5. Обрабатывает исключение, если возникает ошибка при записи данных кампании, и логирует ошибку.

**Примеры**:

```python
from types import SimpleNamespace

campaign_data = SimpleNamespace(
    campaign_name='test_campaign',
    title='Test Campaign Title',
    language='ru',
    currency='USD',
    description='Test campaign description'
)

campaign_gsheet.set_campaign_worksheet(campaign_data)
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
        logger.warning(f"No products found for {category=}\n{products=}.")
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

**Назначение**: Записывает данные о продуктах на лист Google Sheets.

**Параметры**:

- `category_name` (str): Название категории, продукты которой нужно получить.

**Как работает функция**:

1.  Извлекает категорию и список продуктов из `self.editor.campaign.category` по `category_name`.
2.  Если продукты не найдены, функция завершает работу и выводит предупреждение в лог.
3.  Копирует лист `product` и переименовывает его в `category_name`.
4.  Формирует список данных о продуктах для записи в Google Sheets.
5.  Обновляет лист Google Sheets данными о продуктах.
6.  Вызывает метод `_format_category_products_worksheet` для форматирования листа.
7.  Логирует информацию об успешной записи данных о продуктах.
8.  Обрабатывает исключение, если возникает ошибка при записи данных о продуктах, и логирует ошибку.

**Примеры**:

```python
campaign_gsheet.set_products_worksheet(category_name='test_category')
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

**Назначение**: Записывает данные о категориях на лист Google Sheets.

**Параметры**:

- `categories` (SimpleNamespace): Объект SimpleNamespace с данными о категориях для записи.

**Как работает функция**:

1. Получает лист 'categories' из Google Sheets.
2. Очищает лист 'categories'.
3. Извлекает данные о категориях из объекта SimpleNamespace.
4. Проверяет наличие необходимых атрибутов у каждой категории.
5. Формирует список заголовков для таблицы.
6. Формирует список данных о категориях для записи в Google Sheets.
7. Обновляет лист Google Sheets данными о категориях.
8. Вызывает метод `_format_categories_worksheet` для форматирования листа.
9. Логирует информацию об успешной записи данных о категориях.
10. Обрабатывает исключение, если возникает ошибка при записи данных о категориях, и логирует ошибку.

**Примеры**:

```python
from types import SimpleNamespace

category1 = SimpleNamespace(
    name='test_category1',
    title='Test Category 1 Title',
    description='Test category 1 description',
    tags=['tag1', 'tag2'],
    products_count=10
)

category2 = SimpleNamespace(
    name='test_category2',
    title='Test Category 2 Title',
    description='Test category 2 description',
    tags=['tag3', 'tag4'],
    products_count=20
)

categories_data = SimpleNamespace(
    test_category1=category1,
    test_category2=category2
)

campaign_gsheet.set_categories_worksheet(categories_data)
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

**Назначение**: Получает данные о категориях из таблицы Google Sheets.

**Возвращает**:

- `list[dict]`: Список словарей с данными о категориях.

**Как работает функция**:

1. Получает лист 'categories' из Google Sheets.
2. Извлекает все записи из листа.
3. Логирует информацию об успешном получении данных о категориях.
4. Возвращает данные о категориях в виде списка словарей.

**Примеры**:

```python
categories = campaign_gsheet.get_categories()
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

**Назначение**: Записывает данные о продуктах категории в таблицу Google Sheets.

**Параметры**:

- `category_name` (str): Название категории.
- `products` (dict): Словарь с данными о продуктах.

**Как работает функция**:

1.  Извлекает категорию и список продуктов из `self.editor.campaign.category` по `category_name`.
2.  Если продукты не найдены, функция завершает работу и выводит предупреждение в лог.
3.  Копирует лист `product` и переименовывает его в `category_name`.
4.  Формирует список данных о продуктах для записи в Google Sheets.
5.  Обновляет лист Google Sheets данными о продуктах.
6.  Вызывает метод `_format_category_products_worksheet` для форматирования листа.
7.  Логирует информацию об успешной записи данных о продуктах.
8.  Обрабатывает исключение, если возникает ошибка при записи данных о продуктах, и логирует ошибку.

**Примеры**:

```python
campaign_gsheet.set_category_products(category_name='test_category', products=[{'product_id': 1, 'app_sale_price': 10.0}])
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
2. Устанавливает высоту строки 1.
3. Определяет формат заголовков (жирный шрифт, размер 12, центрирование, вертикальное выравнивание по середине, серый фон).
4. Применяет формат заголовков к диапазону A1:E1.
5. Логирует информацию об успешном форматировании листа.
6. Обрабатывает исключение, если возникает ошибка при форматировании листа, и логирует ошибку.

**Примеры**:

```python
ws = campaign_gsheet.get_worksheet('categories')
campaign_gsheet._format_categories_worksheet(ws)
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
2. Устанавливает высоту строки 1.
3. Определяет формат заголовков (жирный шрифт, размер 12, центрирование, вертикальное выравнивание по верхнему краю, серый фон).
4. Применяет формат заголовков к диапазону A1:Y1.
5. Логирует информацию об успешном форматировании листа.
6. Обрабатывает исключение, если возникает ошибка при форматировании листа, и логирует ошибку.

**Примеры**:

```python
ws = campaign_gsheet.get_worksheet('test_category')
campaign_gsheet._format_category_products_worksheet(ws)
```