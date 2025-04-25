# Модуль `campaign`

## Обзор

Модуль `campaign` предназначен для управления процессом создания и публикации рекламных кампаний на Facebook. Он включает в себя функциональность для инициализации параметров кампании (имя, язык, валюта), создания структуры каталогов, сохранения конфигурации для новой кампании, сбора и сохранения данных о продуктах через `ali` или `html`, создания рекламных материалов, проверки кампании и публикации ее на Facebook.

## Подробней

Модуль `campaign` реализует различные этапы создания рекламной кампании на Facebook.  Он включает в себя:

* **Инициализацию кампании:** 
    * Определение имени, языка и валюты кампании. 
    * Создание каталогов и файлов для хранения данных кампании.
    * Сохранение настроек кампании в файл конфигурации.
* **Сбор и обработку данных:**
    * Сбор данных о продуктах, которые будут рекламироваться в кампании. 
    * Сохранение данных о продуктах в базу данных или файл.
* **Создание рекламных материалов:** 
    * Создание графики, баннеров и других рекламных материалов для кампании.
* **Проверка и публикация:**
    * Проверка готовности кампании к публикации. 
    * Публикация кампании на Facebook.

## Классы

### `AliCampaignEditor`

**Описание:** Класс `AliCampaignEditor` предоставляет функциональность для редактирования параметров кампании AliExpress.

**Наследует:** 
    - `object`

**Атрибуты:**

 - `campaign_name` (str): Имя кампании.
 - `language` (str): Язык кампании.
 - `currency` (str): Валюта кампании.
 - `category` (str): Категория кампании.
 - `campaign_directory` (str): Путь к директории кампании.

**Методы:**

#### `delete_product`
**Описание:** Удаляет продукт из кампании.

**Параметры:**
 - `product_id` (str): ID продукта, который нужно удалить.

**Возвращает:**
 - `None`

**Вызывает исключения:**
 - `ValueError`: Если `product_id` не найден.

**Пример:**

```python
# Удаление продукта с ID '123456'
editor = AliCampaignEditor('summer_sale', 'english', 'usd')
editor.delete_product('123456')
```


#### `update_product`
**Описание:** Обновляет данные о продукте в кампании.

**Параметры:**
 - `product_id` (str): ID продукта, который нужно обновить.
 - `new_data` (dict): Новые данные для продукта. 

**Возвращает:**
 - `None`

**Вызывает исключения:**
 - `ValueError`: Если `product_id` не найден.

**Пример:**

```python
# Обновление данных продукта с ID '123456'
editor = AliCampaignEditor('summer_sale', 'english', 'usd')
new_data = {'price': 10.99, 'description': 'Updated product description'}
editor.update_product('123456', new_data)
```

#### `update_campaign`
**Описание:** Обновляет данные о кампании.

**Параметры:**
 - `new_data` (dict): Новые данные для кампании.

**Возвращает:**
 - `None`

**Вызывает исключения:**
 - `ValueError`: Если `new_data` неверный формат.

**Пример:**

```python
# Обновление описания кампании
editor = AliCampaignEditor('summer_sale', 'english', 'usd')
new_data = {'description': 'Updated campaign description'}
editor.update_campaign(new_data)
```

#### `update_category`
**Описание:** Обновляет категорию в кампании.

**Параметры:**
 - `category_name` (str): Имя категории.
 - `new_data` (dict): Новые данные для категории.

**Возвращает:**
 - `None`

**Вызывает исключения:**
 - `ValueError`: Если `category_name` не найден.

**Пример:**

```python
# Обновление данных категории 'Electronics'
editor = AliCampaignEditor('summer_sale', 'english', 'usd')
new_data = {'description': 'Updated category description'}
editor.update_category('Electronics', new_data)
```

#### `get_category`
**Описание:** Возвращает данные о категории.

**Параметры:**
 - `category_name` (str): Имя категории.

**Возвращает:**
 - `SimpleNamespace`: Объект с данными о категории.

**Вызывает исключения:**
 - `ValueError`: Если `category_name` не найден.

**Пример:**

```python
# Получение данных о категории 'Electronics'
editor = AliCampaignEditor('summer_sale', 'english', 'usd')
category = editor.get_category('Electronics')
```

#### `list_categories`
**Описание:** Возвращает список всех категорий в кампании.

**Параметры:**
 - `None`

**Возвращает:**
 - `list`: Список имен категорий.

**Вызывает исключения:**
 - `None`

**Пример:**

```python
# Получение списка всех категорий в кампании
editor = AliCampaignEditor('summer_sale', 'english', 'usd')
categories = editor.list_categories()
```

#### `get_category_products`
**Описание:** Возвращает список продуктов для заданной категории.

**Параметры:**
 - `category_name` (str): Имя категории.

**Возвращает:**
 - `list`: Список объектов `SimpleNamespace` с данными о продуктах.

**Вызывает исключения:**
 - `ValueError`: Если `category_name` не найден.

**Пример:**

```python
# Получение списка продуктов для категории 'Electronics'
editor = AliCampaignEditor('summer_sale', 'english', 'usd')
products = editor.get_category_products('Electronics')
```

#### `get_product`
**Описание:** Возвращает данные о продукте по ID.

**Параметры:**
 - `product_id` (str): ID продукта.

**Возвращает:**
 - `SimpleNamespace`: Объект с данными о продукте.

**Вызывает исключения:**
 - `ValueError`: Если `product_id` не найден.

**Пример:**

```python
# Получение данных о продукте с ID '123456'
editor = AliCampaignEditor('summer_sale', 'english', 'usd')
product = editor.get_product('123456')
```

#### `list_products`
**Описание:** Возвращает список всех продуктов в кампании.

**Параметры:**
 - `None`

**Возвращает:**
 - `list`: Список объектов `SimpleNamespace` с данными о продуктах.

**Вызывает исключения:**
 - `None`

**Пример:**

```python
# Получение списка всех продуктов в кампании
editor = AliCampaignEditor('summer_sale', 'english', 'usd')
products = editor.list_products()
```

#### `add_product`
**Описание:** Добавляет новый продукт в кампанию.

**Параметры:**
 - `product_data` (dict): Данные о продукте.

**Возвращает:**
 - `None`

**Вызывает исключения:**
 - `ValueError`: Если `product_data` неверный формат.

**Пример:**

```python
# Добавление нового продукта в кампанию
editor = AliCampaignEditor('summer_sale', 'english', 'usd')
product_data = {'product_id': '123456', 'name': 'Product Name', 'price': 10.99, 'description': 'Product description'}
editor.add_product(product_data)
```

#### `other_methods`
**Описание:** Другие методы класса `AliCampaignEditor`.

**Параметры:**
 - `None`

**Возвращает:**
 - `None`

**Вызывает исключения:**
 - `None`

**Пример:**

```python
# Пример использования других методов
editor = AliCampaignEditor('summer_sale', 'english', 'usd')
# ...
```


## Функции

### `generate_promo_materials`

**Назначение:** Создает рекламные материалы для кампании AliExpress.

**Параметры:**
 - `campaign_name` (str): Имя кампании.
 - `language` (str): Язык кампании.
 - `currency` (str): Валюта кампании.
 - `products` (list): Список объектов `SimpleNamespace` с данными о продуктах.

**Возвращает:**
 - `None`

**Вызывает исключения:**
 - `ValueError`: Если `campaign_name`, `language`, `currency` или `products` неверные.

**Пример:**

```python
# Создание рекламных материалов для кампании 'summer_sale'
generate_promo_materials(
    campaign_name='summer_sale',
    language='english',
    currency='usd',
    products=[
        {'product_id': '123456', 'name': 'Product Name', 'price': 10.99, 'description': 'Product description'},
        {'product_id': '789012', 'name': 'Another Product', 'price': 15.99, 'description': 'Another product description'},
    ]
)
```

### `get_campaign_data`

**Назначение:** Возвращает данные о кампании AliExpress по имени.

**Параметры:**
 - `campaign_name` (str): Имя кампании.

**Возвращает:**
 - `dict`: Словарь с данными о кампании.

**Вызывает исключения:**
 - `ValueError`: Если `campaign_name` не найден.

**Пример:**

```python
# Получение данных о кампании 'summer_sale'
campaign_data = get_campaign_data(campaign_name='summer_sale')
```

### `save_campaign_data`

**Назначение:** Сохраняет данные о кампании AliExpress в файл.

**Параметры:**
 - `campaign_data` (dict): Данные о кампании.

**Возвращает:**
 - `None`

**Вызывает исключения:**
 - `ValueError`: Если `campaign_data` неверный формат.

**Пример:**

```python
# Сохранение данных о кампании 'summer_sale'
save_campaign_data(
    campaign_data={
        'campaign_name': 'summer_sale',
        'language': 'english',
        'currency': 'usd',
        'products': [
            {'product_id': '123456', 'name': 'Product Name', 'price': 10.99, 'description': 'Product description'},
            {'product_id': '789012', 'name': 'Another Product', 'price': 15.99, 'description': 'Another product description'},
        ]
    }
)
```

### `process_campaign`

**Назначение:** Обрабатывает рекламную кампанию AliExpress.

**Параметры:**
 - `campaign_name` (str): Имя кампании.
 - `language` (str): Язык кампании.
 - `currency` (str): Валюта кампании.
 - `categories` (list): Список категорий для обработки.
 - `update_products` (bool): Нужно ли обновлять данные о продуктах.

**Возвращает:**
 - `None`

**Вызывает исключения:**
 - `ValueError`: Если `campaign_name`, `language`, `currency` или `categories` неверные.

**Пример:**

```python
# Обработка кампании 'summer_sale'
process_campaign(
    campaign_name='summer_sale',
    language='english',
    currency='usd',
    categories=['Electronics', 'Fashion'],
    update_products=True
)
```

## Параметры класса

- `campaign_name` (str): Имя кампании.
- `language` (str): Язык кампании.
- `currency` (str): Валюта кампании.
- `category` (str): Категория кампании.
- `campaign_directory` (str): Путь к директории кампании.


## Примеры

```python
# Создание объекта AliCampaignEditor
editor = AliCampaignEditor(campaign_name='summer_sale', language='english', currency='usd')

# Получение списка категорий в кампании
categories = editor.list_categories()

# Получение данных о категории 'Electronics'
category = editor.get_category('Electronics')

# Получение списка продуктов для категории 'Electronics'
products = editor.get_category_products('Electronics')

# Обновление данных о продукте с ID '123456'
editor.update_product('123456', {'price': 10.99})

# Удаление продукта с ID '123456'
editor.delete_product('123456')
```

```python
# Создание рекламных материалов для кампании 'summer_sale'
generate_promo_materials(
    campaign_name='summer_sale',
    language='english',
    currency='usd',
    products=[
        {'product_id': '123456', 'name': 'Product Name', 'price': 10.99, 'description': 'Product description'},
        {'product_id': '789012', 'name': 'Another Product', 'price': 15.99, 'description': 'Another product description'},
    ]
)
```

```python
# Получение данных о кампании 'summer_sale'
campaign_data = get_campaign_data(campaign_name='summer_sale')

# Сохранение данных о кампании 'summer_sale'
save_campaign_data(
    campaign_data={
        'campaign_name': 'summer_sale',
        'language': 'english',
        'currency': 'usd',
        'products': [
            {'product_id': '123456', 'name': 'Product Name', 'price': 10.99, 'description': 'Product description'},
            {'product_id': '789012', 'name': 'Another Product', 'price': 15.99, 'description': 'Another product description'},
        ]
    }
)
```

```python
# Обработка кампании 'summer_sale'
process_campaign(
    campaign_name='summer_sale',
    language='english',
    currency='usd',
    categories=['Electronics', 'Fashion'],
    update_products=True
)