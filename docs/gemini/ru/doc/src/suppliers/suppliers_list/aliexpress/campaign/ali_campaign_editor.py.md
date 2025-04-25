# AliCampaignEditor

## Обзор

Модуль `AliCampaignEditor` предоставляет функциональность для редактирования рекламных кампаний в AliExpress. Он расширяет класс `AliPromoCampaign`, предоставляя методы для работы с продуктами, категориями и настройками кампании.

## Подробнее

Модуль `AliCampaignEditor` используется для управления рекламными кампаниями AliExpress, предоставляя функциональность для обновления продуктов, категорий и настроек кампании. Он взаимодействует с файлами JSON, CSV и текстовыми файлами, хранящими информацию о кампаниях.

## Классы

### `AliCampaignEditor`

**Описание**: Класс `AliCampaignEditor` предоставляет инструменты для редактирования рекламных кампаний AliExpress. Он наследует класс `AliPromoCampaign` и расширяет его функциональность.

**Наследует**: `AliPromoCampaign`

**Атрибуты**:

- `campaign_name` (str): Название кампании.
- `language` (Optional[str | dict]): Язык кампании.
- `currency` (Optional[str]): Валюта кампании.
- `google_sheet` (Optional[AliCampaignGoogleSheet]): Инстанс класса `AliCampaignGoogleSheet`, используемый для взаимодействия с Google Sheets.

**Методы**:

- `__init__(self, campaign_name: str, language: Optional[str | dict] = None, currency: Optional[str] = None)`: Инициализирует объект `AliCampaignEditor`.
- `delete_product(self, product_id: str, exc_info: bool = False)`: Удаляет продукт, который не имеет партнерской ссылки.
- `update_product(self, category_name: str, lang: str, product: dict)`: Обновляет данные продукта в категории.
- `update_campaign(self)`: Обновляет свойства кампании, такие как описание, теги и т.д.
- `update_category(self, json_path: Path, category: SimpleNamespace) -> bool`: Обновляет категорию в JSON файле.
- `get_category(self, category_name: str) -> Optional[SimpleNamespace]`: Возвращает объект `SimpleNamespace` для заданного имени категории.
- `list_categories(self) -> Optional[List[str]]`: Возвращает список имен категорий в текущей кампании.
- `get_category_products(self, category_name: str) -> Optional[List[SimpleNamespace]]`: Чтение данных о товарах из JSON файлов для конкретной категории.

## Методы класса

### `delete_product`

```python
def delete_product(self, product_id: str, exc_info: bool = False):
    """ Удаляет продукт, который не имеет партнерской ссылки. 
    
    Args:
        product_id (str): ID продукта, который необходимо удалить.
        exc_info (bool): Флаг, указывающий, нужно ли выводить подробную информацию об ошибке. По умолчанию `False`.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> editor.delete_product("12345")
    """
    ...
```

**Назначение**: Функция `delete_product` удаляет продукт из списка продуктов кампании, если у него нет партнерской ссылки.

**Параметры**:

- `product_id` (str): ID продукта, который необходимо удалить.
- `exc_info` (bool): Флаг, указывающий, нужно ли выводить подробную информацию об ошибке.

**Возвращает**: 
- `None`

**Как работает функция**:

- Функция сначала извлекает ID продукта из переданного параметра `product_id`.
- Затем функция считывает список продуктов из файла `sources.txt` в директории категории.
- Функция итерирует по списку продуктов и ищет совпадение по ID продукта.
- Если совпадение найдено, функция удаляет запись продукта из списка и сохраняет обновленный список в файл `_sources.txt`.
- Если совпадение не найдено, функция пытается переименовать файл продукта в директории `sources`, добавив символ "_" к его названию.

**Примеры**:

```python
>>> editor = AliCampaignEditor(campaign_name="Summer Sale")
>>> editor.delete_product("12345")
```


### `update_product`

```python
def update_product(self, category_name: str, lang: str, product: dict):
    """ Обновляет данные продукта в категории. 

    Args:
        category_name (str): Имя категории, в которой необходимо обновить продукт.
        lang (str): Язык кампании.
        product (dict): Словарь с данными о продукте.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> editor.update_product("Electronics", "EN", {"product_id": "12345", "title": "Smartphone"})\n
    """
    ...
```

**Назначение**: Функция `update_product` обновляет данные о продукте в категории.

**Параметры**:

- `category_name` (str): Имя категории, в которой необходимо обновить продукт.
- `lang` (str): Язык кампании.
- `product` (dict): Словарь с данными о продукте.

**Возвращает**: 
- `None`

**Как работает функция**:

- Функция вызывает функцию `dump_category_products_files`, передавая ей имя категории, язык и данные о продукте.

**Примеры**:

```python
>>> editor = AliCampaignEditor(campaign_name="Summer Sale")
>>> editor.update_product("Electronics", "EN", {"product_id": "12345", "title": "Smartphone"})
```


### `update_campaign`

```python
def update_campaign(self):
    """ Обновляет свойства кампании, такие как `description`, `tags` и т.д.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> editor.update_campaign()
    """
    ...
```

**Назначение**: Функция `update_campaign` обновляет свойства кампании, такие как описание, теги, ключевые слова и т.д.

**Параметры**: 
- `None`

**Возвращает**: 
- `None`

**Как работает функция**:

- Функция обновляет свойства кампании, используя данные из объекта `self.campaign`.
- Функция использует методы класса `AliPromoCampaign` для обновления свойств кампании.

**Примеры**:

```python
>>> editor = AliCampaignEditor(campaign_name="Summer Sale")
>>> editor.update_campaign()
```


### `update_category`

```python
def update_category(self, json_path: Path, category: SimpleNamespace) -> bool:
    """ Обновляет категорию в JSON файле.

    Args:
        json_path (Path): Путь к JSON файлу.
        category (SimpleNamespace): Объект категории для обновления.

    Returns:
        bool: `True`, если обновление прошло успешно, иначе `False`.

    Example:
        >>> category = SimpleNamespace(name="New Category", description="Updated description")
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> result = editor.update_category(Path("category.json"), category)
        >>> print(result)  # True if successful
    """
    ...
```

**Назначение**: Функция `update_category` обновляет данные о категории в JSON файле.

**Параметры**:

- `json_path` (Path): Путь к JSON файлу, который необходимо обновить.
- `category` (SimpleNamespace): Объект `SimpleNamespace` с данными о категории для обновления.

**Возвращает**: 
- `bool`: `True`, если обновление прошло успешно, иначе `False`.

**Как работает функция**:

- Функция считывает данные из JSON файла, используя функцию `j_loads`.
- Функция обновляет данные категории в файле, используя функцию `j_dumps`.

**Примеры**:

```python
>>> category = SimpleNamespace(name="New Category", description="Updated description")
>>> editor = AliCampaignEditor(campaign_name="Summer Sale")
>>> result = editor.update_category(Path("category.json"), category)
>>> print(result)  # True if successful
```


### `get_category`

```python
def get_category(self, category_name: str) -> Optional[SimpleNamespace]:
    """ Возвращает объект SimpleNamespace для заданного имени категории.

    Args:
        category_name (str): Имя категории.

    Returns:
        Optional[SimpleNamespace]: Объект `SimpleNamespace`, представляющий категорию, или `None`, если категория не найдена.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> category = editor.get_category("Electronics")
        >>> print(category)  # SimpleNamespace or None
    """
    ...
```

**Назначение**: Функция `get_category` возвращает объект `SimpleNamespace` для заданного имени категории.

**Параметры**:

- `category_name` (str): Имя категории, которую необходимо получить.

**Возвращает**: 
- `Optional[SimpleNamespace]`: Объект `SimpleNamespace`, представляющий категорию, или `None`, если категория не найдена.

**Как работает функция**:

- Функция проверяет, существует ли атрибут с именем категории в объекте `self.campaign`.
- Если атрибут существует, функция возвращает его.
- Если атрибут не найден, функция выводит предупреждение в лог и возвращает `None`.

**Примеры**:

```python
>>> editor = AliCampaignEditor(campaign_name="Summer Sale")
>>> category = editor.get_category("Electronics")
>>> print(category)  # SimpleNamespace or None
```


### `list_categories`

```python
@property
def list_categories(self) -> Optional[List[str]]:
    """ Retrieve a list of categories in the current campaign.

    Returns:
        Optional[List[str]]: A list of category names, or None if no categories are found.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> categories = editor.categories_list
        >>> print(categories)  # [\'Electronics\', \'Fashion\', \'Home\']
    """
    try:
        # Ensure campaign has a category attribute and it is a SimpleNamespace
        if hasattr(self.campaign, 'category') and isinstance(self.campaign.category, SimpleNamespace):
            return list(vars(self.campaign.category).keys())
        else:
            logger.warning("No categories found in the campaign.")
            return
    except Exception as ex:
        logger.error(f"Error retrieving categories list: {ex}")
        return
```

**Назначение**: Функция `list_categories` возвращает список имен категорий в текущей кампании.

**Параметры**: 
- `None`

**Возвращает**: 
- `Optional[List[str]]`: Список имен категорий или `None`, если категории не найдены.

**Как работает функция**:

- Функция проверяет, существует ли атрибут `category` в объекте `self.campaign` и является ли он объектом `SimpleNamespace`.
- Если атрибут `category` существует, функция возвращает список имен категорий из объекта `SimpleNamespace`.
- Если атрибут `category` не найден или не является `SimpleNamespace`, функция выводит предупреждение в лог и возвращает `None`.

**Примеры**:

```python
>>> editor = AliCampaignEditor(campaign_name="Summer Sale")
>>> categories = editor.categories_list
>>> print(categories)  # [\'Electronics\', \'Fashion\', \'Home\']
```


### `get_category_products`

```python
async def get_category_products(
    self, category_name: str
) -> Optional[List[SimpleNamespace]]:
    """Чтение данных о товарах из JSON файлов для конкретной категории.

    Args:
        category_name (str): Имя категории.

    Returns:
        Optional[List[SimpleNamespace]]: Список объектов SimpleNamespace, представляющих товары.

    Example:
        >>> products = campaign.get_category_products("Electronics")
        >>> print(len(products))
        15
    """
    category_path = (
        self.base_path
        / "category"
        / category_name
        / f"{self.language}_{self.currency}"
    )
    json_filenames = await get_filenames_from_directory (category_path, extensions="json")
    products = []

    if json_filenames:
        for json_filename in json_filenames:
            product_data = j_loads_ns(category_path / json_filename)
            product = SimpleNamespace(**vars(product_data))
            products.append(product)
        return products
    else:
        logger.error(
            f"No JSON files found for {category_name=} at {category_path=}.\\nStart prepare category"
        )
        self.process_category_products(category_name)
        return 
```

**Назначение**: Функция `get_category_products` асинхронно считывает данные о товарах из JSON файлов для конкретной категории.

**Параметры**:

- `category_name` (str): Имя категории.

**Возвращает**: 
- `Optional[List[SimpleNamespace]]`: Список объектов `SimpleNamespace`, представляющих товары, или `None`, если JSON файлы не найдены.

**Как работает функция**:

- Функция определяет путь к директории категории.
- Функция асинхронно получает список имен JSON файлов в директории категории, используя функцию `get_filenames_from_directory`.
- Если JSON файлы найдены, функция считывает данные из каждого файла, используя функцию `j_loads_ns`, и создает объект `SimpleNamespace` для каждого товара.
- Функция возвращает список объектов `SimpleNamespace`, представляющих товары.
- Если JSON файлы не найдены, функция выводит сообщение об ошибке в лог и вызывает функцию `process_category_products` для подготовки данных о товарах.

**Примеры**:

```python
>>> products = campaign.get_category_products("Electronics")
>>> print(len(products))
15
```

## Параметры класса

- `campaign_name` (str): Название кампании.
- `language` (Optional[str | dict]): Язык кампании.
- `currency` (Optional[str]): Валюта кампании.


## Примеры

```python
# 1. Создание объекта AliCampaignEditor
editor = AliCampaignEditor(campaign_name="Summer Sale", language="EN", currency="USD")

# 2. Удаление продукта
editor.delete_product("12345")

# 3. Обновление продукта
editor.update_product("Electronics", "EN", {"product_id": "12345", "title": "Smartphone"})

# 4. Обновление кампании
editor.update_campaign()

# 5. Обновление категории
category = SimpleNamespace(name="New Category", description="Updated description")
editor.update_category(Path("category.json"), category)

# 6. Получение категории
category = editor.get_category("Electronics")
print(category)

# 7. Получение списка категорий
categories = editor.list_categories
print(categories)

# 8. Получение данных о товарах
products = editor.get_category_products("Electronics")
print(products)