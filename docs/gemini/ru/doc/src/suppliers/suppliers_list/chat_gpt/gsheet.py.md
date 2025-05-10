# Модуль Google Sheet для работы с кампаниями AliExpress

## Обзор

Этот модуль (`src/suppliers/chat_gpt/gsheet.py`) предоставляет класс `GptGs` для управления Google Sheets в контексте кампаний AliExpress. 

Он использует класс `SpreadSheet` из `src.goog.spreadsheet.spreadsheet` для взаимодействия с Google Sheets и позволяет  сохранять, обновлять и извлекать данные о категориях и товарах в кампании.

## Подробнее

`GptGs` предоставляет методы для:

- Очистки таблицы: удаления листов товаров и очистки данных в категориях и других листах.
- Обновления листа чата: записи данных кампании в лист Google Sheets.
- Чтения данных кампании: чтения данных кампании из листа "campaign".
- Записи данных категории: записи данных о категории в лист "category".
- Чтения данных категории: чтения данных о категории из листа "category".
- Записи данных категорий: записи данных о категориях из списка объектов `SimpleNamespace` в лист "categories".
- Чтения данных категорий: чтения данных категорий из листа "categories".
- Записи данных товара: записи данных о товаре в новый лист Google Sheets.
- Чтения данных товара: чтения данных о товаре из листа "products".
- Записи данных товаров: записи данных о товарах в лист "products".
- Удаления листов товаров: удаления всех листов, кроме "categories", "product" и "product_template" из таблицы Google Sheets.
- Сохранения категорий: сохранения данных из листа "categories" в объект кампании.
- Сохранения кампании: сохранения данных из листа "campaign" и категорий в объект кампании.

## Классы

### `GptGs`

**Описание**:  Класс для управления Google Sheets в контексте кампаний AliExpress.

**Наследует**: 
  - `SpreadSheet`
  - `AliCampaignEditor` 

**Атрибуты**:

- `spreadsheet_id` (`str`): ID Google Sheets таблицы.

**Методы**:

- `__init__`: Инициализирует `GptGs` с указанным ID Google Sheets таблицы.
- `clear`: Очищает содержимое таблицы.
- `update_chat_worksheet`: Записывает данные о чате в лист Google Sheets.
- `get_campaign_worksheet`: Читает данные о кампании из листа "campaign".
- `set_category_worksheet`: Записывает данные о категории в лист "category".
- `get_category_worksheet`: Читает данные о категории из листа "category".
- `set_categories_worksheet`: Записывает данные о категориях из списка объектов `SimpleNamespace` в лист "categories".
- `get_categories_worksheet`: Читает данные о категориях из листа "categories".
- `set_product_worksheet`: Записывает данные о товаре в новый лист Google Sheets.
- `get_product_worksheet`: Читает данные о товаре из листа "products".
- `set_products_worksheet`: Записывает данные о товарах в лист "products".
- `delete_products_worksheets`: Удаляет все листы, кроме "categories", "product" и "product_template" из таблицы Google Sheets.
- `save_categories_from_worksheet`: Сохраняет данные из листа "categories" в объект кампании.
- `save_campaign_from_worksheet`: Сохраняет данные из листа "campaign" и категорий в объект кампании.

## Методы класса

### `__init__`

```python
    def __init__(self):
        """ Initialize AliCampaignGoogleSheet with specified Google Sheets spreadsheet ID and additional parameters.\n
        @param campaign_name `str`: The name of the campaign.\n
        @param category_name `str`: The name of the category.\n
        @param language `str`: The language for the campaign.\n
        @param currency `str`: The currency for the campaign.\n
        """
        # Initialize SpreadSheet with the spreadsheet ID
        super().__init__('1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0')
        
       
```

**Назначение**: Инициализирует `GptGs` с указанным ID Google Sheets таблицы.

**Параметры**:

- `spreadsheet_id` (`str`): ID Google Sheets таблицы.

**Возвращает**: 
- `None`.

**Как работает функция**:
-  Инициализирует класс `SpreadSheet` с заданным ID Google Sheets таблицы.

### `clear`

```python
    def clear(self):
        """ Clear contents.\n
        Delete product sheets and clear data on the categories and other specified sheets.\n
        """
        try:
            self.delete_products_worksheets()
            # ws_to_clear = ['category','categories','campaign']
            # for ws in self.spreadsheet.worksheets():
            #     self.get_worksheet(ws).clear()
                
        except Exception as ex:
            logger.error("Ошибка очистки",ex)
```

**Назначение**: Очищает содержимое таблицы.

**Параметры**:
- `None`.

**Возвращает**: 
- `None`.

**Как работает функция**:
- Удаляет листы товаров с помощью метода `delete_products_worksheets`.
- Очищает данные в листах "category", "categories" и "campaign" (хотя этот блок кода закомментирован).


### `update_chat_worksheet`

```python
    def update_chat_worksheet(self, data: SimpleNamespace|dict|list, conversation_name:str, language: str = None):
        """ Write campaign data to a Google Sheets worksheet.\n
        @param campaign `SimpleNamespace | str`: SimpleNamespace object with campaign data fields for writing.\n
        @param language `str`: Optional language parameter.\n
        @param currency `str`: Optional currency parameter.\n
        """
       
        try:
            ws: Worksheet = self.get_worksheet(conversation_name)
            _ = data.__dict__
                # Extract data from the SimpleNamespace attribute
            name =  _.get('name','')
            title =  _.get('title')
            description =  _.get('description')
            tags =  ', '.join(map(str, _.get('tags', [])))
            products_count =  _.get('products_count','~')
```

**Назначение**: Записывает данные о чате в лист Google Sheets.

**Параметры**:

- `data` (`SimpleNamespace | dict | list`): Объект `SimpleNamespace`, словарь или список с данными о чате для записи.
- `conversation_name` (`str`): Название листа, куда нужно записывать данные.
- `language` (`str`, optional): Язык для записи. По умолчанию `None`.

**Возвращает**: 
- `None`.

**Как работает функция**:
- Получает ссылку на лист Google Sheets по имени `conversation_name` с помощью метода `get_worksheet`.
- Извлекает данные из объекта `SimpleNamespace`, словаря или списка в переменные `name`, `title`, `description`, `tags` и `products_count`.
- Подготавливает обновления для листа Google Sheets, используя `updates` список словарей с информацией о том, какие данные нужно записать в какие ячейки.

### `get_campaign_worksheet`

```python
    def get_campaign_worksheet(self) -> SimpleNamespace:
        """ Read campaign data from the 'campaign' worksheet.\n
        @return `SimpleNamespace`: SimpleNamespace object with campaign data fields.\n
        """
        try:
            ws: Worksheet = self.get_worksheet('campaign')
            if not ws:
                raise ValueError("Worksheet 'campaign' not found.")
            
            data = ws.get_all_values()
            campaign_data = SimpleNamespace(
                name=data[0][1],
                title=data[1][1],
                language=data[2][1],
                currency=data[3][1],
                description=data[4][1]
            )
            
            logger.info("Campaign data read from 'campaign' worksheet.")
            return campaign_data
```

**Назначение**: Читает данные о кампании из листа "campaign".

**Параметры**:

- `None`.

**Возвращает**: 
- `SimpleNamespace`: Объект `SimpleNamespace` с данными о кампании.

**Как работает функция**:
- Получает ссылку на лист Google Sheets "campaign" с помощью метода `get_worksheet`.
- Читает все значения из листа с помощью метода `get_all_values`.
- Создает объект `SimpleNamespace` с данными о кампании, извлеченными из листа.


### `set_category_worksheet`

```python
    def set_category_worksheet(self, category: SimpleNamespace | str):
        """ Write data from a SimpleNamespace object to Google Sheets cells vertically.\n
        @param category `SimpleNamespace`: SimpleNamespace object with data fields for writing.\n
        """
        category = category if isinstance(category, SimpleNamespace) else self.get_campaign_category(category)
        try:
            ws: Worksheet = self.get_worksheet('category')
```

**Назначение**: Записывает данные о категории в лист "category".

**Параметры**:

- `category` (`SimpleNamespace | str`): Объект `SimpleNamespace` с данными о категории для записи.

**Возвращает**: 
- `None`.

**Как работает функция**:
- Проверяет, является ли `category` объектом `SimpleNamespace`. Если нет, то использует метод `get_campaign_category` для получения объекта `SimpleNamespace` по имени категории.
- Получает ссылку на лист Google Sheets "category" с помощью метода `get_worksheet`.
- Подготавливает данные для записи в лист, используя `vertical_data` список списков, где каждый подсписок представляет собой строку с именем атрибута и его значением.
- Записывает данные в лист с помощью метода `update`, который принимает диапазон ячеек для записи и список данных.

### `get_category_worksheet`

```python
    def get_category_worksheet(self) -> SimpleNamespace:
        """ Read category data from the 'category' worksheet.\n
        @return `SimpleNamespace`: SimpleNamespace object with category data fields.\n
        """
        try:
            ws: Worksheet = self.get_worksheet('category')
            if not ws:
                raise ValueError("Worksheet 'category' not found.")
            
            data = ws.get_all_values()
            category_data = SimpleNamespace(
                name=data[1][1],
                title=data[2][1],
                description=data[3][1],
                tags=data[4][1].split(', '),
                products_count=int(data[5][1])
            )
            
            logger.info("Category data read from 'category' worksheet.")
            return category_data
```

**Назначение**: Читает данные о категории из листа "category".

**Параметры**:

- `None`.

**Возвращает**: 
- `SimpleNamespace`: Объект `SimpleNamespace` с данными о категории.

**Как работает функция**:
- Получает ссылку на лист Google Sheets "category" с помощью метода `get_worksheet`.
- Читает все значения из листа с помощью метода `get_all_values`.
- Создает объект `SimpleNamespace` с данными о категории, извлеченными из листа.

### `set_categories_worksheet`

```python
    def set_categories_worksheet(self, categories: SimpleNamespace):
        """ Write data from a SimpleNamespace object to Google Sheets cells.\n
        @param categories `SimpleNamespace`: SimpleNamespace object with data fields for writing.\n
        """
        ws: Worksheet = self.get_worksheet('categories')
        # ws.clear()  # Clear the 'categories' worksheet
```

**Назначение**: Записывает данные о категориях из списка объектов `SimpleNamespace` в лист "categories".

**Параметры**:

- `categories` (`SimpleNamespace`): Объект `SimpleNamespace` с данными о категориях для записи.

**Возвращает**: 
- `None`.

**Как работает функция**:
- Получает ссылку на лист Google Sheets "categories" с помощью метода `get_worksheet`.
- Проходит по всем атрибутам объекта `categories` и проверяет, является ли каждый атрибут объектом `SimpleNamespace` и содержит ли он данные о категории.
- Извлекает данные из объекта `SimpleNamespace` в переменные `name`, `title`, `description`, `tags` и `products_count`.
- Подготавливает обновления для листа Google Sheets, используя `updates` список словарей с информацией о том, какие данные нужно записать в какие ячейки.
- Выполняет пакетное обновление листа Google Sheets с помощью метода `batch_update`.


### `get_categories_worksheet`

```python
    def get_categories_worksheet(self) -> List[List[str]]:
        """ Read data from columns A to E, starting from the second row, from the 'categories' worksheet.\n
        @return `List[List[str]]`: List of rows with data from columns A to E.\n
        """
        try:
            ws: Worksheet = self.get_worksheet('categories')
            if not ws:
                raise ValueError("Worksheet 'categories' not found.")
        
            # Read all values from the worksheet
            data = ws.get_all_values()
        
            # Extract data from columns A to E, starting from the second row
            data = [row[:5] for row in data[1:] if len(row) >= 5]  
        
            logger.info("Category data read from 'categories' worksheet.")
            return data
```

**Назначение**: Читает данные о категориях из листа "categories".

**Параметры**:

- `None`.

**Возвращает**: 
- `List[List[str]]`: Список строк с данными о категориях.

**Как работает функция**:
- Получает ссылку на лист Google Sheets "categories" с помощью метода `get_worksheet`.
- Читает все значения из листа с помощью метода `get_all_values`.
- Извлекает данные из столбцов A-E, начиная со второй строки, и возвращает их в виде списка списков строк.

### `set_product_worksheet`

```python
    def set_product_worksheet(self, product: SimpleNamespace | str, category_name: str):
        """ Write product data to a new Google Sheets spreadsheet.\n
        @param category_name Category name.\n
        @param product SimpleNamespace object with product data fields for writing.\n
        """
        time.sleep(10)
        ws = self.copy_worksheet('product_template', category_name)  # Copy 'product_template' to new worksheet
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
            ws.update('A1:Y1', [headers])
```

**Назначение**: Записывает данные о товаре в новый лист Google Sheets.

**Параметры**:

- `product` (`SimpleNamespace | str`): Объект `SimpleNamespace` с данными о товаре для записи.
- `category_name` (`str`): Имя категории, для которой создается лист.

**Возвращает**: 
- `None`.

**Как работает функция**:
- Копирует лист "product_template" в новый лист с именем, полученным из `category_name`.
- Записывает заголовки столбцов в первую строку листа.
- Извлекает данные из объекта `SimpleNamespace` в переменные, представляющие данные о товаре.
- Записывает данные о товаре во вторую строку листа.

### `get_product_worksheet`

```python
    def get_product_worksheet(self) -> SimpleNamespace:
        """ Read product data from the 'products' worksheet.\n
        @return `SimpleNamespace`: SimpleNamespace object with product data fields.\n
        """
        try:
            ws: Worksheet = self.get_worksheet('products')
            if not ws:
                raise ValueError("Worksheet 'products' not found.")
            
            data = ws.get_all_values()
            product_data = SimpleNamespace(
                id=data[1][1],
                name=data[2][1],
                title=data[3][1],
                description=data[4][1],
                tags=data[5][1].split(', '),
                price=float(data[6][1])
            )
            
            logger.info("Product data read from 'products' worksheet.")
            return product_data
```

**Назначение**: Читает данные о товаре из листа "products".

**Параметры**:

- `None`.

**Возвращает**: 
- `SimpleNamespace`: Объект `SimpleNamespace` с данными о товаре.

**Как работает функция**:
- Получает ссылку на лист Google Sheets "products" с помощью метода `get_worksheet`.
- Читает все значения из листа с помощью метода `get_all_values`.
- Создает объект `SimpleNamespace` с данными о товаре, извлеченными из листа.

### `set_products_worksheet`

```python
    def set_products_worksheet(self, category_name:str):
        """ Write data from a list of SimpleNamespace objects to Google Sheets cells.\n
        @param ns_list `List[SimpleNamespace]`|`SimpleNamespace`: List of SimpleNamespace objects with data fields for writing.\n
        """
        if category_name:
            category_ns:SimpleNamespace = getattr(self.campaign.category,category_name)
            products_ns:SimpleNamespace = category_ns.products
        else:
            logger.warning(f"На ашел товары в {pprint(category_ns)}")
            return    
        ws: Worksheet = self.get_worksheet(category_name)
        
        try:
            updates:list=[]
            for index, value in enumerate(products_ns, start=2):
                _ = value.__dict__
                updates.append({'range': f'A{index}', 'values': [[str(_.get('product_id',''))]])
                updates.append({'range': f'B{index}', 'values': [[str(_.get('product_title',''))]])
                updates.append({'range': f'C{index}', 'values': [[str(_.get('title',''))]])
                updates.append({'range': f'D{index}', 'values': [[str(_.get('local_image_path',''))]])
                updates.append({'range': f'D{index}', 'values': [[str(_.get('product_video_url',''))]])
                updates.append({'range': f'F{index}', 'values': [[str(_.get('original_price',''))]])
                updates.append({'range': f'F{index}', 'values': [[str(_.get('app_sale_price',''))]])
                updates.append({'range': f'F{index}', 'values': [[str(_.get('target_sale_price',''))]])
                updates.append({'range': f'F{index}', 'values': [[str(_.get('target_sale_price',''))]])
                
            ws.batch_update(updates)
            logger.info("Products data written to 'products' worksheet.")
```

**Назначение**: Записывает данные о товарах в лист Google Sheets.

**Параметры**:

- `category_name` (`str`): Имя категории, для которой нужно записать данные о товарах.

**Возвращает**: 
- `None`.

**Как работает функция**:
- Получает ссылки на объекты `SimpleNamespace` для категории и ее товаров.
- Получает ссылку на лист Google Sheets по имени категории.
- Создает список обновлений для листа, где каждое обновление содержит информацию о том, какие данные нужно записать в какие ячейки.
- Выполняет пакетное обновление листа с помощью метода `batch_update`.

### `delete_products_worksheets`

```python
    def delete_products_worksheets(self):
        """ Delete all sheets from the Google Sheets spreadsheet except 'categories' and 'product_template'.\n
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

**Назначение**: Удаляет все листы, кроме "categories", "product" и "product_template" из таблицы Google Sheets.

**Параметры**:

- `None`.

**Возвращает**: 
- `None`.

**Как работает функция**:
- Получает список всех листов из таблицы Google Sheets с помощью метода `worksheets`.
- Проходит по всем листам и удаляет те, которые не входят в список `excluded_titles`.
- Использует метод `del_worksheet_by_id` для удаления листа.

### `save_categories_from_worksheet`

```python
    def save_categories_from_worksheet(self, update:bool=False):
        """ Сохраняю данные, отредактированные в гугл таблице """
```

**Назначение**: Сохраняет данные из листа "categories" в объект кампании.

**Параметры**:

- `update` (`bool`, optional): Флаг, определяющий, нужно ли обновлять кампанию после сохранения данных о категориях. По умолчанию `False`.

**Возвращает**: 
- `None`.

**Как работает функция**:
- Читает данные о категориях из листа "categories" с помощью метода `get_categories_worksheet`.
- Создает объект `SimpleNamespace` для хранения данных о категориях.
- Записывает данные о категориях в объект `SimpleNamespace`.
- Записывает объект `SimpleNamespace` с данными о категориях в атрибут `category` объекта кампании.
- Если `update` установлен в `True`, то обновляет кампанию.

### `save_campaign_from_worksheet`

```python
    def save_campaign_from_worksheet(self):
        """ Сохраняю реклманую каманию """
        self.save_categories_from_worksheet(False)
        data = self.get_campaign_worksheet()
        data.category = self.campaign.category
        self.campaign = data
        self.update_campaign()
        ...
```

**Назначение**: Сохраняет данные из листа "campaign" и категорий в объект кампании.

**Параметры**:

- `None`.

**Возвращает**: 
- `None`.

**Как работает функция**:
- Сохраняет данные из листа "categories" в объект кампании с помощью метода `save_categories_from_worksheet`.
- Читает данные о кампании из листа "campaign" с помощью метода `get_campaign_worksheet`.
- Записывает объект `SimpleNamespace` с данными о категориях в атрибут `category` объекта `data`.
- Обновляет объект кампании данными из `data`.
- Обновляет кампанию с помощью метода `update_campaign`. 

## Параметры класса

- `spreadsheet_id` (`str`): ID Google Sheets таблицы.
- `campaign_name` (`str`): Название кампании.
- `category_name` (`str`): Название категории.
- `language` (`str`): Язык для кампании.
- `currency` (`str`): Валюта для кампании.

## Примеры

```python
# Создание инстанса Google Sheet
gsheet = GptGs()

# Очистка содержимого таблицы
gsheet.clear()

# Обновление листа чата
gsheet.update_chat_worksheet(data, 'conversation_name')

# Чтение данных кампании
campaign_data = gsheet.get_campaign_worksheet()

# Запись данных категории
gsheet.set_category_worksheet(category)

# Чтение данных категории
category_data = gsheet.get_category_worksheet()

# Запись данных категорий
gsheet.set_categories_worksheet(categories)

# Чтение данных категорий
categories_data = gsheet.get_categories_worksheet()

# Запись данных товара
gsheet.set_product_worksheet(product, 'category_name')

# Чтение данных товара
product_data = gsheet.get_product_worksheet()

# Запись данных товаров
gsheet.set_products_worksheet('category_name')

# Удаление листов товаров
gsheet.delete_products_worksheets()

# Сохранение категорий
gsheet.save_categories_from_worksheet()

# Сохранение кампании
gsheet.save_campaign_from_worksheet()