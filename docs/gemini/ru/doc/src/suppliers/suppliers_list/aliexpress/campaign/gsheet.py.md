# Модуль: Редактор рекламной кампании через Google Sheets

## Обзор

Модуль `gsheet.py` предназначен для работы с Google Sheets в рамках управления рекламными кампаниями AliExpress. Он предоставляет функциональность для создания, редактирования и форматирования Google Sheets, используемых для хранения информации о кампаниях, категориях и продуктах.

## Подробней

Этот модуль упрощает взаимодействие с Google Sheets, позволяя автоматизировать запись и чтение данных о рекламных кампаниях AliExpress. Он включает в себя функции для очистки листов, удаления листов продуктов, записи данных кампаний, категорий и продуктов, а также для форматирования листов для удобства просмотра и редактирования.

## Классы

### `AliCampaignGoogleSheet`

**Описание**: Класс `AliCampaignGoogleSheet` предназначен для работы с Google Sheets в рамках кампаний AliExpress.

**Наследует**:

- `SpreadSheet`: Класс наследует класс `SpreadSheet` из модуля `src.goog.spreadsheet.spreadsheet`, что позволяет ему использовать функциональность для работы с Google Sheets.

**Атрибуты**:

- `spreadsheet_id` (str): Идентификатор Google Sheets spreadsheet.
- `spreadsheet` (SpreadSheet): Объект SpreadSheet для работы с Google Sheets.
- `worksheet` (Worksheet): Объект Worksheet для работы с листом Google Sheets.

**Методы**:

- `__init__(self, campaign_name: str, language: str | dict = None, currency: str = None)`: Инициализирует объект `AliCampaignGoogleSheet` с указанным ID Google Sheets spreadsheet и дополнительными параметрами.
- `clear(self)`: Очищает содержимое Google Sheets, удаляя листы продуктов и очищая данные на листах категорий и других указанных листах.
- `delete_products_worksheets(self)`: Удаляет все листы из Google Sheets spreadsheet, кроме листов 'categories', 'product', 'category' и 'campaign'.
- `set_campaign_worksheet(self, campaign: SimpleNamespace)`: Записывает данные кампании в Google Sheets worksheet.
- `set_products_worksheet(self, category_name: str)`: Записывает данные о продуктах из списка объектов SimpleNamespace в ячейки Google Sheets.
- `set_categories_worksheet(self, categories: SimpleNamespace)`: Записывает данные из объекта SimpleNamespace с категориями в ячейки Google Sheets.
- `get_categories(self)`: Получает данные из таблицы Google Sheets.
- `set_category_products(self, category_name: str, products: dict)`: Записывает данные о продуктах в новую таблицу Google Sheets.
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

**Назначение**: Инициализирует объект `AliCampaignGoogleSheet` с указанным идентификатором Google Sheets и дополнительными параметрами.

**Параметры**:

- `campaign_name` (str): Название кампании.
- `language` (str | dict, optional): Язык кампании. По умолчанию `None`.
- `currency` (str, optional): Валюта кампании. По умолчанию `None`.

**Как работает функция**:

1. Вызывает конструктор родительского класса `SpreadSheet` с указанным `spreadsheet_id`.
2. Инициализирует объект `AliCampaignGoogleSheet` с заданными параметрами.
3. Закомментированный код предполагает интеграцию с `AliCampaignEditor` для автоматической настройки листов кампании и категорий.

**Примеры**:

```python
campaign_sheet = AliCampaignGoogleSheet(campaign_name='SummerSale', language='en', currency='USD')
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

1. Пытается удалить листы продуктов, вызывая метод `delete_products_worksheets()`.
2. В случае возникновения ошибки логирует её с использованием `logger.error()`.

**Примеры**:

```python
campaign_sheet.clear()
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

**Назначение**: Удаляет все листы из Google Sheets spreadsheet, кроме листов 'categories', 'product', 'category' и 'campaign'.

**Как работает функция**:

1. Определяет множество `excluded_titles` с названиями листов, которые не нужно удалять.
2. Получает список всех листов в spreadsheet.
3. Перебирает листы и удаляет те, чьи названия не входят в `excluded_titles`.
4. Логирует успешное удаление каждого листа с использованием `logger.success()`.
5. В случае возникновения ошибки логирует её с использованием `logger.error()` и поднимает исключение.

**Примеры**:

```python
campaign_sheet.delete_products_worksheets()
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

**Назначение**: Записывает данные кампании в Google Sheets worksheet.

**Параметры**:

- `campaign` (SimpleNamespace): Объект SimpleNamespace с данными кампании для записи.

**Как работает функция**:

1. Получает worksheet с названием 'campaign'.
2. Готовит данные для вертикальной записи, формируя список кортежей с информацией о ячейке, заголовке и значении.
3. Формирует список операций обновления для пакетной записи данных в worksheet.
4. Выполняет пакетное обновление worksheet, если есть данные для записи.
5. Логирует успешную запись данных кампании с использованием `logger.info()`.
6. В случае возникновения ошибки логирует её с использованием `logger.error()` и поднимает исключение.

**Примеры**:

```python
from types import SimpleNamespace
campaign_data = SimpleNamespace(campaign_name='SummerSale', title='Летняя распродажа', language='en', currency='USD', description='Описание летней распродажи')
campaign_sheet.set_campaign_worksheet(campaign_data)
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
        logger.warning(f"No products found for {category=}\\n{products=}.")
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

**Назначение**: Записывает данные о продуктах из списка объектов `SimpleNamespace` в ячейки Google Sheets.

**Параметры**:

- `category_name` (str): Название категории, из которой нужно получить продукты.

**Как работает функция**:

1. Если `category_name` указан, пытается получить категорию и список продуктов из атрибута `editor.campaign.category`.
2. Если продукты не найдены, логирует предупреждение и завершает выполнение.
3. Копирует worksheet 'product' и присваивает ему имя `category_name`.
4. Формирует список данных для записи в worksheet, извлекая информацию о каждом продукте.
5. Записывает данные о продуктах в worksheet, обновляя каждую строку.
6. Логирует успешное обновление каждого продукта с использованием `logger.info()`.
7. Вызывает метод `_format_category_products_worksheet()` для форматирования worksheet.
8. Логирует успешное обновление продуктов в worksheet с использованием `logger.info()`.
9. В случае возникновения ошибки логирует её с использованием `logger.error()` и поднимает исключение.

**Примеры**:

```python
campaign_sheet.set_products_worksheet(category_name='Electronics')
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

**Назначение**: Записывает данные из объекта `SimpleNamespace` с категориями в ячейки Google Sheets.

**Параметры**:

- `categories` (SimpleNamespace): Объект, где ключи — это категории с данными для записи.

**Как работает функция**:

1. Получает worksheet с названием 'categories' и очищает его содержимое.
2. Извлекает данные о категориях из объекта `categories`.
3. Проверяет, что все объекты категории имеют необходимые атрибуты: 'name', 'title', 'description', 'tags', 'products_count'.
4. Записывает заголовки таблицы в worksheet.
5. Готовит данные для записи, извлекая информацию о каждой категории.
6. Записывает данные о категориях в worksheet.
7. Вызывает метод `_format_categories_worksheet()` для форматирования worksheet.
8. Логирует успешное обновление полей категорий с использованием `logger.info()`.
9. В случае отсутствия необходимых атрибутов у категорий логирует предупреждение с использованием `logger.warning()`.
10. В случае возникновения ошибки логирует её с использованием `logger.error()` и поднимает исключение.

**Примеры**:

```python
from types import SimpleNamespace
categories_data = SimpleNamespace(
    Electronics=SimpleNamespace(name='Electronics', title='Электроника', description='Описание электроники', tags=['электроника', 'товары'], products_count=100),
    Clothing=SimpleNamespace(name='Clothing', title='Одежда', description='Описание одежды', tags=['одежда', 'мода'], products_count=50)
)
campaign_sheet.set_categories_worksheet(categories_data)
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

**Назначение**: Получает данные из таблицы Google Sheets.

**Возвращает**:

- list[dict]: Данные из таблицы в виде списка словарей.

**Как работает функция**:

1. Получает worksheet с названием 'categories'.
2. Получает все записи из worksheet с помощью метода `get_all_records()`.
3. Логирует успешное получение данных о категориях с использованием `logger.info()`.
4. Возвращает полученные данные.

**Примеры**:

```python
categories = campaign_sheet.get_categories()
if categories:
    for category in categories:
        print(category['Name'])
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

1. Если `category_name` указан, пытается получить категорию и список продуктов из атрибута `editor.campaign.category`.
2. Если продукты не найдены, логирует предупреждение и завершает выполнение.
3. Копирует worksheet 'product' и присваивает ему имя `category_name`.
4. Записывает заголовки таблицы в worksheet.
5. Формирует список данных для записи в worksheet, извлекая информацию о каждом продукте.
6. Записывает данные о продуктах в worksheet, обновляя каждую строку.
7. Логирует успешное обновление каждого продукта с использованием `logger.info()`.
8. Вызывает метод `_format_category_products_worksheet()` для форматирования worksheet.
9. Логирует успешное обновление продуктов в worksheet с использованием `logger.info()`.
10. В случае возникновения ошибки логирует её с использованием `logger.error()` и поднимает исключение.

**Примеры**:

```python
products_data = [
    {'product_id': '123', 'app_sale_price': '10.00', 'original_price': '12.00', 'sale_price': '11.00', 'discount': '10%', 'product_main_image_url': 'http://example.com/image.jpg', 'local_image_path': '/tmp/image.jpg', 'product_small_image_urls': ['http://example.com/image_small.jpg'], 'product_video_url': 'http://example.com/video.mp4', 'local_video_path': '/tmp/video.mp4', 'first_level_category_id': '1', 'first_level_category_name': 'Электроника', 'second_level_category_id': '2', 'second_level_category_name': 'Телефоны', 'target_sale_price': '11.00', 'target_sale_price_currency': 'USD', 'target_app_sale_price_currency': 'USD', 'target_original_price_currency': 'USD', 'original_price_currency': 'USD', 'product_title': 'Телефон', 'evaluate_rate': '4.5', 'promotion_link': 'http://example.com/promotion', 'shop_url': 'http://example.com/shop', 'shop_id': '1', 'tags': ['телефон', 'электроника']}
]
campaign_sheet.set_category_products(category_name='Телефоны', products=products_data)
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

**Назначение**: Форматирует лист 'categories'.

**Параметры**:

- `ws` (Worksheet): Лист Google Sheets для форматирования.

**Как работает функция**:

1. Устанавливает ширину столбцов A, B, C, D и E.
2. Устанавливает высоту строки 1.
3. Задает формат для заголовков, включая жирный шрифт, размер шрифта, выравнивание по центру и цвет фона.
4. Применяет формат к диапазону ячеек A1:E1.
5. Логирует успешное форматирование worksheet с использованием `logger.info()`.
6. В случае возникновения ошибки логирует её с использованием `logger.error()` и поднимает исключение.

**Примеры**:

```python
ws = campaign_sheet.get_worksheet('categories')
campaign_sheet._format_categories_worksheet(ws)
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

**Назначение**: Форматирует лист с продуктами категории.

**Параметры**:

- `ws` (Worksheet): Лист Google Sheets для форматирования.

**Как работает функция**:

1. Устанавливает ширину столбцов от A до Y.
2. Устанавливает высоту строки 1.
3. Задает формат для заголовков, включая жирный шрифт, размер шрифта, выравнивание по центру и цвет фона.
4. Применяет формат к диапазону ячеек A1:Y1.
5. Логирует успешное форматирование worksheet с использованием `logger.info()`.
6. В случае возникновения ошибки логирует её с использованием `logger.error()` и поднимает исключение.

**Примеры**:

```python
ws = campaign_sheet.get_worksheet('Электроника')
campaign_sheet._format_category_products_worksheet(ws)
```