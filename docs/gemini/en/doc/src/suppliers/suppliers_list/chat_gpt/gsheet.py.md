# Module:  AliExpress Campaign Editor via Google Sheets

## Overview

This module provides functionality for managing AliExpress campaigns through Google Sheets. The `GptGs` class leverages the `SpreadSheet` and `AliCampaignEditor` classes to handle Google Sheets operations, including writing category and product data, and formatting sheets. 

## Table of Contents

- **Classes:**
    - [`GptGs`](#gptgs)
- **Functions:**
    - [`clear`](#clear)
    - [`update_chat_worksheet`](#update_chat_worksheet)
    - [`get_campaign_worksheet`](#get_campaign_worksheet)
    - [`set_category_worksheet`](#set_category_worksheet)
    - [`get_category_worksheet`](#get_category_worksheet)
    - [`set_categories_worksheet`](#set_categories_worksheet)
    - [`get_categories_worksheet`](#get_categories_worksheet)
    - [`set_product_worksheet`](#set_product_worksheet)
    - [`get_product_worksheet`](#get_product_worksheet)
    - [`set_products_worksheet`](#set_products_worksheet)
    - [`delete_products_worksheets`](#delete_products_worksheets)
    - [`save_categories_from_worksheet`](#save_categories_from_worksheet)
    - [`save_campaign_from_worksheet`](#save_campaign_from_worksheet)

## Classes

### `GptGs`

**Description**: Класс для управления Google Sheets в рамках кампаний AliExpress.

**Inherits**: `SpreadSheet` and `AliCampaignEditor`

**Attributes**: None

**Methods**:

- [`__init__`](#__init__)
- [`clear`](#clear)
- [`update_chat_worksheet`](#update_chat_worksheet)
- [`get_campaign_worksheet`](#get_campaign_worksheet)
- [`set_category_worksheet`](#set_category_worksheet)
- [`get_category_worksheet`](#get_category_worksheet)
- [`set_categories_worksheet`](#set_categories_worksheet)
- [`get_categories_worksheet`](#get_categories_worksheet)
- [`set_product_worksheet`](#set_product_worksheet)
- [`get_product_worksheet`](#get_product_worksheet)
- [`set_products_worksheet`](#set_products_worksheet)
- [`delete_products_worksheets`](#delete_products_worksheets)
- [`save_categories_from_worksheet`](#save_categories_from_worksheet)
- [`save_campaign_from_worksheet`](#save_campaign_from_worksheet)

### `__init__`

```python
    def __init__(self):
        """
        Инициализирует AliCampaignGoogleSheet с указанным идентификатором Google Sheets таблицы и дополнительными параметрами.
        @param campaign_name `str`: Название кампании.
        @param category_name `str`: Название категории.
        @param language `str`: Язык для кампании.
        @param currency `str`: Валюта для кампании.
        """
        # Инициализирует SpreadSheet с идентификатором таблицы
        super().__init__('1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0')
```

**Purpose**: Инициализирует класс `GptGs`, задавая идентификатор Google Sheets таблицы и, возможно, дополнительные параметры (например, название кампании, категории, язык и валюту).

**Parameters**: 

- **`campaign_name` (`str`)**: Название кампании. 
- **`category_name` (`str`)**: Название категории.
- **`language` (`str`)**: Язык для кампании.
- **`currency` (`str`)**: Валюта для кампании.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**: 
- Использует `super().__init__()` для вызова конструктора базового класса `SpreadSheet` и передачи идентификатора таблицы.
- Инициализирует  `AliCampaignEditor` объект, если `campaign_name`, `category_name`, `language` и `currency` заданы.

**Examples**:
```python
# Инициализация с заданием всех параметров
gpt_gs = GptGs(campaign_name='My Campaign', category_name='Electronics', language='en', currency='USD')
```


### `clear`

```python
    def clear(self):
        """
        Очищает содержимое.
        Удаляет листы продуктов и очищает данные на листах категорий и других указанных листах.
        """
        try:
            self.delete_products_worksheets()
            # ws_to_clear = ['category','categories','campaign']
            # for ws in self.spreadsheet.worksheets():
            #     self.get_worksheet(ws).clear()
                
        except Exception as ex:
            logger.error("Ошибка очистки",ex)
```

**Purpose**: Очищает содержимое Google Sheets таблицы, удаляя листы продуктов и очищая данные на листах категорий и других указанных листах.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: `Exception`

**How the Function Works**: 
- Вызывает `self.delete_products_worksheets()` для удаления листов продуктов.
- Очищает указанные листы (`ws_to_clear`) с помощью `self.get_worksheet(ws).clear()`.

**Examples**:
```python
# Очистка Google Sheets таблицы
gpt_gs.clear()
```

### `update_chat_worksheet`

```python
    def update_chat_worksheet(self, data: SimpleNamespace|dict|list, conversation_name:str, language: str = None):
        """
        Записывает данные кампании на лист Google Sheets.
        @param campaign `SimpleNamespace | str`: Объект SimpleNamespace с полями данных кампании для записи.
        @param language `str`: Необязательный параметр языка.
        @param currency `str`: Необязательный параметр валюты.
        """
       
        try:
            ws: Worksheet = self.get_worksheet(conversation_name)
            _ = data.__dict__
                # Извлекает данные из атрибута SimpleNamespace
            name =  _.get('name','')
            title =  _.get('title')
            description =  _.get('description')
            tags =  ', '.join(map(str, _.get('tags', [])))
            products_count =  _.get('products_count','~')
            
            # Подготавливает обновления для заданного объекта SimpleNamespace
            updates = [
                {'range': f'A{start_row}', 'values': [[name]]},
                {'range': f'B{start_row}', 'values': [[title]]},
                {'range': f'C{start_row}', 'values': [[description]]},
                {'range': f'D{start_row}', 'values': [[tags]]},
                {'range': f'E{start_row}', 'values': [[products_count]]},
            ]
            
        except Exception as ex:
            logger.error("Error writing campaign data to worksheet.", ex, exc_info=True)
            raise
```

**Purpose**: Записывает данные кампании на указанный лист Google Sheets. 

**Parameters**:

- **`data` (`SimpleNamespace` | `dict` | `list`)**: Объект `SimpleNamespace`, словарь или список, содержащий поля данных кампании для записи.
- **`conversation_name` (`str`)**: Название листа, на который записываются данные.
- **`language` (`str`)**: Необязательный параметр языка для кампании.
- **`currency` (`str`)**: Необязательный параметр валюты для кампании.

**Returns**: None

**Raises Exceptions**: `Exception`

**How the Function Works**: 
- Получает ссылку на указанный лист (`conversation_name`) с помощью `self.get_worksheet()`.
- Извлекает данные из `data` объекта. 
- Подготавливает список обновлений (`updates`) для записи данных в Google Sheets, задавая диапазон ячеек и значения.
- Выполняет пакетное обновление листа с помощью `ws.batch_update(updates)`.

**Examples**:
```python
# Запись данных кампании на лист "My Conversation"
campaign_data = SimpleNamespace(name='Campaign Name', title='Campaign Title', description='Campaign Description', tags=['tag1', 'tag2'], products_count=10)
gpt_gs.update_chat_worksheet(campaign_data, conversation_name='My Conversation')
```


### `get_campaign_worksheet`

```python
    def get_campaign_worksheet(self) -> SimpleNamespace:
        """
        Читает данные кампании с листа 'campaign'.
        @return `SimpleNamespace`: Объект SimpleNamespace с полями данных кампании.
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
            
        except Exception as ex:
            logger.error("Error getting campaign worksheet data.", ex, exc_info=True)
            raise
```

**Purpose**: Читает данные кампании с листа 'campaign' в Google Sheets.

**Parameters**: None

**Returns**: `SimpleNamespace`: Объект `SimpleNamespace`, содержащий поля данных кампании.

**Raises Exceptions**: `ValueError`, `Exception`

**How the Function Works**:
- Получает ссылку на лист 'campaign' с помощью `self.get_worksheet()`.
- Читает все значения с листа с помощью `ws.get_all_values()`.
- Создает объект `SimpleNamespace` с полями данных кампании, извлекая данные из `data` списка.
- Выводит информационное сообщение в лог.

**Examples**:
```python
# Чтение данных кампании с листа 'campaign'
campaign_data = gpt_gs.get_campaign_worksheet()
print(f"Campaign name: {campaign_data.name}")
```


### `set_category_worksheet`

```python
    def set_category_worksheet(self, category: SimpleNamespace | str):
        """
        Записывает данные из объекта SimpleNamespace в ячейки Google Sheets вертикально.
        @param category `SimpleNamespace`: Объект SimpleNamespace с полями данных для записи.
        """
        category = category if isinstance(category, SimpleNamespace) else self.get_campaign_category(category)
        try:
            ws: Worksheet = self.get_worksheet('category')
            
            if isinstance(category, SimpleNamespace):
                # Подготавливает данные для вертикальной записи
                _ = category.__dict__
                vertical_data = [
                    ['Name', _.get('name','')],
                    ['Title', _.get('title','')],
                    ['Description', _.get('description')],
                    ['Tags', ', '.join(map(str, _.get('tags', [])))],
                    ['Products Count', _.get('products_count', '~')]
                ]
            
                # Записывает данные вертикально
                ws.update('A1:B{}'.format(len(vertical_data)), vertical_data)
                
                logger.info("Category data written to 'category' worksheet vertically.")
            else:
                raise TypeError("Expected SimpleNamespace for category.")
                
        except Exception as ex:
            logger.error("Error setting category worksheet.", ex, exc_info=True)
            raise
```

**Purpose**: Записывает данные из объекта `SimpleNamespace` в ячейки Google Sheets вертикально.

**Parameters**:

- **`category` (`SimpleNamespace` | `str`)**: Объект `SimpleNamespace`, содержащий поля данных категории для записи, или строка, представляющая название категории.

**Returns**: None

**Raises Exceptions**: `TypeError`, `Exception`

**How the Function Works**: 
- Получает ссылку на лист 'category' с помощью `self.get_worksheet()`.
- Проверяет, является ли `category` объектом `SimpleNamespace`. 
- Подготавливает данные для записи в формате `vertical_data`, где каждый элемент - список, содержащий имя поля и его значение. 
- Записывает данные вертикально в ячейки `A1:B{len(vertical_data)}` с помощью `ws.update()`. 
- Выводит информационное сообщение в лог.

**Examples**:
```python
# Запись данных категории на лист 'category'
category_data = SimpleNamespace(name='Category Name', title='Category Title', description='Category Description', tags=['tag1', 'tag2'], products_count=10)
gpt_gs.set_category_worksheet(category_data)
```


### `get_category_worksheet`

```python
    def get_category_worksheet(self) -> SimpleNamespace:
        """
        Читает данные категории с листа 'category'.
        @return `SimpleNamespace`: Объект SimpleNamespace с полями данных категории.
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
            
        except Exception as ex:
            logger.error("Error getting category worksheet data.", ex, exc_info=True)
            raise
```

**Purpose**: Читает данные категории с листа 'category' в Google Sheets.

**Parameters**: None

**Returns**: `SimpleNamespace`: Объект `SimpleNamespace`, содержащий поля данных категории.

**Raises Exceptions**: `ValueError`, `Exception`

**How the Function Works**: 
- Получает ссылку на лист 'category' с помощью `self.get_worksheet()`.
- Читает все значения с листа с помощью `ws.get_all_values()`.
- Создает объект `SimpleNamespace` с полями данных категории, извлекая данные из `data` списка. 
- Выводит информационное сообщение в лог.

**Examples**:
```python
# Чтение данных категории с листа 'category'
category_data = gpt_gs.get_category_worksheet()
print(f"Category name: {category_data.name}")
```


### `set_categories_worksheet`

```python
    def set_categories_worksheet(self, categories: SimpleNamespace):
        """
        Записывает данные из объекта SimpleNamespace в ячейки Google Sheets.
        @param categories `SimpleNamespace`: Объект SimpleNamespace с полями данных для записи.
        """
        ws: Worksheet = self.get_worksheet('categories')
        # ws.clear()  # Очищает лист 'categories'
        
        try:
            # Инициализирует начальную строку
            start_row = 2
            
            # Итерирует по всем атрибутам объекта categories
            for attr_name in dir(categories):
                attr_value = getattr(categories, attr_name, None)
            
                # Пропускает не-SimpleNamespace атрибуты или атрибуты без данных
                if not isinstance(attr_value, SimpleNamespace) or not any(
                    hasattr(attr_value, field) for field in ['name', 'title', 'description', 'tags', 'products_count']
                ):
                    continue
                _ = attr_value.__dict__
                # Извлекает данные из атрибута SimpleNamespace
                name =  _.get('name','')
                title =  _.get('title')
                description =  _.get('description')
                tags =  ', '.join(map(str, _.get('tags', [])))
                products_count =  _.get('products_count','~')
                
                # Подготавливает обновления для заданного объекта SimpleNamespace
                updates = [
                    {'range': f'A{start_row}', 'values': [[name]]},
                    {'range': f'B{start_row}', 'values': [[title]]},
                    {'range': f'C{start_row}', 'values': [[description]]},
                    {'range': f'D{start_row}', 'values': [[tags]]},
                    {'range': f'E{start_row}', 'values': [[products_count]]},
                ]
                
                # Выполняет пакетное обновление
                if updates:
                    ws.batch_update(updates)
                    logger.info(f"Category data written to 'categories' worksheet for {attr_name}.")
            
                # Переходит к следующей строке
                start_row += 1
                
        except Exception as ex:
            logger.error("Error setting categories worksheet.", ex, exc_info=True)
            raise
```

**Purpose**: Записывает данные из объекта `SimpleNamespace`, представляющего список категорий, в Google Sheets.

**Parameters**:

- **`categories` (`SimpleNamespace`)**: Объект `SimpleNamespace`, содержащий поля данных категорий для записи. 

**Returns**: None

**Raises Exceptions**: `Exception`

**How the Function Works**: 
- Получает ссылку на лист 'categories' с помощью `self.get_worksheet()`. 
- Итерирует по атрибутам объекта `categories`. 
- Извлекает данные из каждого атрибута, который является объектом `SimpleNamespace`. 
- Подготавливает список обновлений (`updates`) для записи данных в Google Sheets, задавая диапазон ячеек и значения.
- Выполняет пакетное обновление листа с помощью `ws.batch_update(updates)`.

**Examples**:
```python
# Запись данных категорий на лист 'categories'
categories_data = SimpleNamespace(category1=SimpleNamespace(name='Category 1', title='Category 1 Title', description='Category 1 Description', tags=['tag1', 'tag2'], products_count=10), category2=SimpleNamespace(name='Category 2', title='Category 2 Title', description='Category 2 Description', tags=['tag3', 'tag4'], products_count=5))
gpt_gs.set_categories_worksheet(categories_data)
```


### `get_categories_worksheet`

```python
    def get_categories_worksheet(self) -> List[List[str]]:
        """
        Читает данные из столбцов A по E, начиная со второй строки, с листа 'categories'.
        @return `List[List[str]]`: Список строк с данными из столбцов A по E.
        """
        try:
            ws: Worksheet = self.get_worksheet('categories')
            if not ws:
                raise ValueError("Worksheet 'categories' not found.")
        
            # Читает все значения с листа
            data = ws.get_all_values()
        
            # Извлекает данные из столбцов A по E, начиная со второй строки
            data = [row[:5] for row in data[1:] if len(row) >= 5]  
        
            logger.info("Category data read from 'categories' worksheet.")
            return data
            
        except Exception as ex:
            logger.error("Error getting category data from worksheet.", ex, exc_info=True)
            raise
```

**Purpose**: Читает данные из столбцов A по E, начиная со второй строки, с листа 'categories' в Google Sheets.

**Parameters**: None

**Returns**: `List[List[str]]`: Список строк, где каждая строка представляет данные из столбцов A по E.

**Raises Exceptions**: `ValueError`, `Exception`

**How the Function Works**: 
- Получает ссылку на лист 'categories' с помощью `self.get_worksheet()`. 
- Читает все значения с листа с помощью `ws.get_all_values()`.
- Извлекает данные из столбцов A по E, начиная со второй строки, используя `data = [row[:5] for row in data[1:] if len(row) >= 5]`.
- Выводит информационное сообщение в лог.

**Examples**:
```python
# Чтение данных категорий с листа 'categories'
category_data = gpt_gs.get_categories_worksheet()
print(category_data)
```


### `set_product_worksheet`

```python
    def set_product_worksheet(self, product: SimpleNamespace | str, category_name: str):
        """
        Записывает данные о продукте на новый лист Google Sheets.
        @param category_name Название категории.
        @param product Объект SimpleNamespace с полями данных о продукте для записи.
        """
        time.sleep(10)
        ws = self.copy_worksheet('product_template', category_name)  # Копирует 'product_template' на новый лист
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
            
            _ = product.__dict__
            row_data = [
                str(_.get('product_id')),
                str(_.get('app_sale_price')),
                str(_.get('original_price')),
                str(_.get('sale_price')),
                str(_.get('discount')),
                str(_.get('product_main_image_url')),
                str(_.get('local_image_path')),
                ', '.join(map(str, _.get('product_small_image_urls', []))),
                str(_.get('product_video_url')),
                str(_.get('local_video_path')),
                str(_.get('first_level_category_id')),
                str(_.get('first_level_category_name')),
                str(_.get('second_level_category_id')),
                str(_.get('second_level_category_name')),
                str(_.get('target_sale_price')),
                str(_.get('target_sale_price_currency')),
                str(_.get('target_app_sale_price_currency')),
                str(_.get('target_original_price_currency')),
                str(_.get('original_price_currency')),
                str(_.get('product_title')),
                str(_.get('evaluate_rate')),
                str(_.get('promotion_link')),
                str(_.get('shop_url')),
                str(_.get('shop_id')),
                ', '.join(map(str, _.get('tags', [])))
            ]
            
            ws.update('A2:Y2', [row_data])  # Обновляет данные строки в одной строке
            
            logger.info("Product data written to worksheet.")
        except Exception as ex:
            logger.error("Error updating product data in worksheet.", ex, exc_info=True)
            raise
```

**Purpose**: Записывает данные о продукте на новый лист Google Sheets, созданный на основе шаблона `product_template`.

**Parameters**:

- **`product` (`SimpleNamespace` | `str`)**: Объект `SimpleNamespace`, содержащий поля данных продукта для записи.
- **`category_name` (`str`)**: Название категории, для которой создается лист.

**Returns**: None

**Raises Exceptions**: `Exception`

**How the Function Works**: 
- Создает новый лист `category_name` на основе шаблона `product_template` с помощью `self.copy_worksheet()`.
- Задает заголовки столбцов (`headers`) на первой строке.
- Извлекает данные из `product` объекта.
- Записывает данные продукта (`row_data`) во вторую строку листа.
- Выводит информационное сообщение в лог.

**Examples**:
```python
# Запись данных продукта на лист "Electronics"
product_data = SimpleNamespace(product_id='12345', app_sale_price=10, original_price=15, ...)
gpt_gs.set_product_worksheet(product_data, category_name='Electronics')
```


### `get_product_worksheet`

```python
    def get_product_worksheet(self) -> SimpleNamespace:
        """
        Читает данные о продукте с листа 'products'.
        @return `SimpleNamespace`: Объект SimpleNamespace с полями данных о продукте.
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
            
        except Exception as ex:
            logger.error("Error getting product worksheet data.", ex, exc_info=True)
            raise
```

**Purpose**: Читает данные о продукте с листа 'products' в Google Sheets.

**Parameters**: None

**Returns**: `SimpleNamespace`: Объект `SimpleNamespace`, содержащий поля данных продукта.

**Raises Exceptions**: `ValueError`, `Exception`

**How the Function Works**:
- Получает ссылку на лист 'products' с помощью `self.get_worksheet()`. 
- Читает все значения с листа с помощью `ws.get_all_values()`.
- Создает объект `SimpleNamespace` с полями данных продукта, извлекая данные из `data` списка.
- Выводит информационное сообщение в лог.

**Examples**:
```python
# Чтение данных продукта с листа 'products'
product_data = gpt_gs.get_product_worksheet()
print(f"Product ID: {product_data.id}")
```


### `set_products_worksheet`

```python
    def set_products_worksheet(self, category_name:str):
        """
        Записывает данные из списка объектов SimpleNamespace в ячейки Google Sheets.
        @param ns_list `List[SimpleNamespace]`|`SimpleNamespace`: Список объектов SimpleNamespace с полями данных для записи.
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
                updates.append({'range': f'A{index}', 'values': [[str(_.get('product_id',' '))]]})
                updates.append({'range': f'B{index}', 'values': [[str(_.get('product_title',' '))]]})
                updates.append({'range': f'C{index}', 'values': [[str(_.get('title',' '))]]})
                updates.append({'range': f'D{index}', 'values': [[str(_.get('local_image_path',' '))]]})
                updates.append({'range': f'D{index}', 'values': [[str(_.get('product_video_url',' '))]]})
                updates.append({'range': f'F{index}', 'values': [[str(_.get('original_price',' '))]]})
                updates.append({'range': f'F{index}', 'values': [[str(_.get('app_sale_price',' '))]]})
                updates.append({'range': f'F{index}', 'values': [[str(_.get('target_sale_price',' '))]]})
                updates.append({'range': f'F{index}', 'values': [[str(_.get('target_sale_price',' '))]]})
                
            ws.batch_update(updates)
            logger.info("Products data written to 'products' worksheet.")
            
        
        except Exception as ex:
            logger.error("Error setting products worksheet.", ex, exc_info=True)
            raise
```

**Purpose**: Записывает данные из списка `products_ns`, представляющего список товаров, на лист Google Sheets.

**Parameters**: 

- **`category_name` (`str`)**: Название категории, для которой записываются товары.

**Returns**: None

**Raises Exceptions**: `Exception`

**How the Function Works**: 
- Извлекает список товаров `products_ns` из объекта `self.campaign.category` по указанному `category_name`.
- Получает ссылку на лист Google Sheets с помощью `self.get_worksheet()`. 
- Итерирует по списку товаров.
- Подготавливает список обновлений (`updates`) для записи данных в Google Sheets, задавая диапазон ячеек и значения.
- Выполняет пакетное обновление листа с помощью `ws.batch_update(updates)`.

**Examples**:
```python
# Запись данных товаров на лист "Electronics"
gpt_gs.set_products_worksheet(category_name='Electronics')
```


### `delete_products_worksheets`

```python
    def delete_products_worksheets(self):
        """
        Удаляет все листы из Google Sheets таблицы, кроме 'categories' и 'product_template'.
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

**Purpose**: Удаляет все листы из Google Sheets таблицы, кроме 'categories', 'product', 'category' и 'campaign'.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: `Exception`

**How the Function Works**: 
- Получает список всех листов (`worksheets`) с помощью `self.spreadsheet.worksheets()`. 
- Итерирует по каждому листу. 
- Если название листа не входит в список исключений (`excluded_titles`), удаляет лист с помощью `self.spreadsheet.del_worksheet_by_id(sheet.id)`.
- Выводит сообщение об успешном удалении листа в лог.

**Examples**:
```python
# Удаление всех листов, кроме 'categories' и 'product_template'
gpt_gs.delete_products_worksheets()
```


### `save_categories_from_worksheet`

```python
    def save_categories_from_worksheet(self, update:bool=False):
        """ Сохраняю данные, отредактированные в гугл таблице """
        
        edited_categories: list[dict] = self.get_categories_worksheet()
        _categories_ns:SimpleNamespace = SimpleNamespace()
        for _cat in edited_categories:
            _cat_ns: SimpleNamespace = SimpleNamespace(**{
                'name':_cat[0],
                'title':_cat[1],
                'description':_cat[2],
                'tags':_cat[3].split(","),
                'products_count':_cat[4],
            }
            )
            setattr(_categories_ns,_cat_ns.name,_cat_ns)
        ...
        self.campaign.category = _categories_ns
        if update: self.update_campaign()
```

**Purpose**: Сохраняет данные категорий, отредактированные в Google Sheets таблице.

**Parameters**:

- **`update` (`bool`)**: Если `True`, обновляет данные кампании после сохранения категорий.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**: 
- Читает данные из Google Sheets таблицы с помощью `self.get_categories_worksheet()`. 
- Создает объект `SimpleNamespace` для хранения данных категорий. 
- Итерирует по каждой строке с данными категории.
- Извлекает данные из каждой строки и создает новый объект `SimpleNamespace` для каждой категории.
- Записывает новый объект `SimpleNamespace` для каждой категории в `self.campaign.category`.
- Если `update` установлено в `True`, обновляет данные кампании с помощью `self.update_campaign()`.

**Examples**:
```python
# Сохранение категорий из Google Sheets таблицы и обновление кампании
gpt_gs.save_categories_from_worksheet(update=True)
```

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

**Purpose**: Сохраняет рекламную кампанию, данные которой были отредактированы в Google Sheets таблице.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:
- Сохраняет данные категорий из Google Sheets таблицы с помощью `self.save_categories_from_worksheet(False)`.
- Читает данные кампании с помощью `self.get_campaign_worksheet()`. 
- Обновляет объект `self.campaign` с сохраненными данными. 
- Обновляет данные кампании с помощью `self.update_campaign()`.

**Examples**:
```python
# Сохранение рекламной кампании из Google Sheets таблицы
gpt_gs.save_campaign_from_worksheet()
```