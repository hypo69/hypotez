# Модуль для редактирования рекламных кампаний AliExpress

## Обзор

Модуль `ali_campaign_editor.py` предоставляет инструменты для редактирования рекламных кампаний на платформе AliExpress. Он включает в себя классы и методы для создания, обновления и удаления информации о кампаниях, категориях и продуктах. Модуль позволяет автоматизировать рутинные операции, такие как удаление товаров без партнерских ссылок, обновление деталей продуктов и категорий, а также управление параметрами кампаний.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для работы с рекламными кампаниями на AliExpress. Он расширяет возможности класса `AliPromoCampaign`, предоставляя инструменты для более детального управления кампаниями. С помощью этого модуля можно автоматизировать задачи, связанные с обновлением информации о продуктах, категориях и параметрах кампаний, что упрощает процесс управления рекламными кампаниями и повышает их эффективность.

## Классы

### `AliCampaignEditor`

**Описание**: Класс `AliCampaignEditor` предназначен для редактирования рекламных кампаний. Он предоставляет методы для управления продуктами, категориями и другими параметрами кампании.

**Наследует**: `AliPromoCampaign`

**Атрибуты**:
- Нет специфичных атрибутов, кроме наследованных от `AliPromoCampaign`.

**Параметры**:
- Отсутствуют.

**Принцип работы**:
Класс `AliCampaignEditor` инициализируется с именем кампании, языком и валютой. Он предоставляет методы для удаления продуктов, обновления деталей продуктов, обновления параметров кампании и управления категориями. Класс использует другие модули и функции, такие как `AliPromoCampaign`, `j_loads`, `j_dumps` и другие утилиты для работы с файлами и данными.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `AliCampaignEditor`.
- `delete_product`: Удаляет продукт из кампании.
- `update_product`: Обновляет информацию о продукте в кампании.
- `update_campaign`: Обновляет параметры кампании.
- `update_category`: Обновляет информацию о категории в файле JSON.
- `get_category`: Получает объект категории `SimpleNamespace` по имени.
- `list_categories`: Получает список категорий в кампании.
- `get_category_products`: Получает список товаров для указанной категории.

## Методы класса

### `__init__`

```python
def __init__(self, 
             campaign_name: str, 
             language: Optional[str | dict] = None, 
             currency: Optional[str] = None):
    """ Initialize the AliCampaignEditor with the given parameters.
    
    Args:
        campaign_name (Optional[str]): The name of the campaign. Defaults to `None`.
        language (Optional[str | dict]): The language of the campaign. Defaults to 'EN'.
        currency (Optional[str]): The currency for the campaign. Defaults to 'USD'.
        campaign_file (Optional[str | Path]): Optionally load a `<lang>_<currency>.json` file from the campaign root folder. Defaults to `None`.

    Raises:
        CriticalError: If neither `campaign_name` nor `campaign_file` is provided.
    
    Example:
    # 1. by campaign parameters
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale", language="EN", currency="USD")
    # 2. load fom file
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale", campaign_file="EN_USD.JSON")
    """
    ...
    super().__init__(campaign_name = campaign_name, language = language, currency = currency)
    #self.google_sheet = AliCampaignGoogleSheet(campaign_name = campaign_name, language = language, currency = currency, campaign_editor = self)
```

**Назначение**: Инициализирует класс `AliCampaignEditor` с заданными параметрами.

**Параметры**:
- `campaign_name` (str): Название кампании.
- `language` (Optional[str | dict]): Язык кампании. По умолчанию `None`.
- `currency` (Optional[str]): Валюта кампании. По умолчанию `None`.

**Возвращает**:
- None

**Вызывает исключения**:
- `CriticalError`: Если не предоставлены `campaign_name` и `campaign_file`.

**Как работает функция**:
- Вызывает конструктор родительского класса `AliPromoCampaign` с переданными параметрами.
- Инициализирует объект `AliCampaignGoogleSheet` (закомментировано в текущей версии кода).

**Примеры**:
```python
# 1. Создание экземпляра класса с параметрами кампании
editor = AliCampaignEditor(campaign_name="Summer Sale", language="EN", currency="USD")

# 2. Создание экземпляра класса с загрузкой из файла
editor = AliCampaignEditor(campaign_name="Summer Sale", campaign_file="EN_USD.JSON")
```

### `delete_product`

```python
def delete_product(self, product_id: str, exc_info: bool = False):
    """ Delete a product that does not have an affiliate link.
    
    Args:
        product_id (str): The ID of the product to be deleted.
        exc_info (bool): Whether to include exception information in logs. Defaults to `False`.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> editor.delete_product("12345")
    """
    ...
    _product_id = extract_prod_ids(product_id)
    
    product_path = self.category_path / 'sources.txt'
    prepared_product_path = self.category_path / '_sources.txt'
    products_list = read_text_file(product_path)
    if products_list:
        for record in products_list:
            if _product_id:
                record_id = extract_prod_ids(record)
                if record_id == str(product_id):
                    products_list.remove(record)
                    save_text_file((products_list, '\n'), prepared_product_path)
                    break
            else:
                if record == str(product_id):
                    products_list.remove(record)
                    save_text_file((products_list, '\n'), product_path)
                
    else:
        product_path = self.category_path / 'sources' / f'{product_id}.html'    
        try:
            product_path.rename(self.category_path / 'sources' / f'{product_id}_.html')
            logger.success(f"Product file {product_path=} renamed successfully.")
        except FileNotFoundError as ex:
            logger.error(f"Product file {product_path=} not found.", exc_info=exc_info)
        except Exception as ex:
            logger.critical(f"An error occurred while deleting the product file {product_path}.", ex)
```

**Назначение**: Удаляет продукт, у которого нет партнерской ссылки.

**Параметры**:
- `product_id` (str): ID продукта, который нужно удалить.
- `exc_info` (bool): Определяет, включать ли информацию об исключении в логи. По умолчанию `False`.

**Возвращает**:
- None

**Как работает функция**:
- Извлекает ID продукта с помощью `extract_prod_ids`.
- Определяет пути к файлам `sources.txt` и `_sources.txt` в каталоге категории.
- Читает список продуктов из файла `sources.txt` с помощью `read_text_file`.
- Если список продуктов существует, перебирает записи и удаляет соответствующую запись.
- Сохраняет обновленный список в файл `_sources.txt` с помощью `save_text_file`.
- Если список продуктов не существует, пытается переименовать файл продукта, добавляя к имени символ подчеркивания.
- Логирует успешное переименование файла или ошибки, если файл не найден или произошла другая ошибка.

**Примеры**:
```python
editor = AliCampaignEditor(campaign_name="Summer Sale")
editor.delete_product("12345")
```

### `update_product`

```python
def update_product(self, category_name: str, lang: str, product: dict):
    """ Update product details within a category.

    Args:
        category_name (str): The name of the category where the product should be updated.
        lang (str): The language of the campaign.
        product (dict): A dictionary containing product details.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> editor.update_product("Electronics", "EN", {"product_id": "12345", "title": "Smartphone"})
    """
    ...
    self.dump_category_products_files(category_name, lang, product)
```

**Назначение**: Обновляет детали продукта в пределах категории.

**Параметры**:
- `category_name` (str): Название категории, в которой нужно обновить продукт.
- `lang` (str): Язык кампании.
- `product` (dict): Словарь, содержащий детали продукта.

**Возвращает**:
- None

**Как работает функция**:
- Вызывает метод `dump_category_products_files` для обновления информации о продукте в файлах категории.

**Примеры**:
```python
editor = AliCampaignEditor(campaign_name="Summer Sale")
editor.update_product("Electronics", "EN", {"product_id": "12345", "title": "Smartphone"})
```

### `update_campaign`

```python
def update_campaign(self):
    """ Update campaign properties such as `description`, `tags`, etc.
    
    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> editor.update_campaign()
    """
    ...
```

**Назначение**: Обновляет свойства кампании, такие как `description`, `tags` и т.д.

**Параметры**:
- None

**Возвращает**:
- None

**Как работает функция**:
- Функция содержит заглушку `...`, что означает, что детали реализации отсутствуют в предоставленном коде.

**Примеры**:
```python
editor = AliCampaignEditor(campaign_name="Summer Sale")
editor.update_campaign()
```

### `update_category`

```python
def update_category(self, json_path: Path, category: SimpleNamespace) -> bool:
    """ Update the category in the JSON file.

    Args:
        json_path (Path): Path to the JSON file.
        category (SimpleNamespace): Category object to be updated.

    Returns:
        bool: True if update is successful, False otherwise.

    Example:
        >>> category = SimpleNamespace(name="New Category", description="Updated description")
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> result = editor.update_category(Path("category.json"), category)
        >>> print(result)  # True if successful
    """
    ...
    try:
        data = j_loads(json_path)  # Read JSON data from file
        data['category'] = category.__dict__  # Convert SimpleNamespace to dict
        j_dumps(data, json_path)  # Write updated JSON data back to file
        return True
    except Exception as ex:
        logger.error(f"Failed to update category {json_path}: {ex}")
        return False
```

**Назначение**: Обновляет категорию в JSON-файле.

**Параметры**:
- `json_path` (Path): Путь к JSON-файлу.
- `category` (SimpleNamespace): Объект категории для обновления.

**Возвращает**:
- `bool`: `True`, если обновление успешно, `False` в противном случае.

**Как работает функция**:
- Пытается прочитать данные из JSON-файла с помощью `j_loads`.
- Преобразует объект `SimpleNamespace` категории в словарь.
- Записывает обновленные данные обратно в JSON-файл с помощью `j_dumps`.
- Возвращает `True` при успешном обновлении и `False` при возникновении ошибки.
- Логирует ошибку, если не удается обновить категорию.

**Примеры**:
```python
category = SimpleNamespace(name="New Category", description="Updated description")
editor = AliCampaignEditor(campaign_name="Summer Sale")
result = editor.update_category(Path("category.json"), category)
print(result)  # True if successful
```

### `get_category`

```python
def get_category(self, category_name: str) -> Optional[SimpleNamespace]:
    """ Returns the SimpleNamespace object for a given category name.

    Args:
        category_name (str): The name of the category to retrieve.

    Returns:
        Optional[SimpleNamespace]: SimpleNamespace object representing the category or `None` if not found.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> category = editor.get_category("Electronics")
        >>> print(category)  # SimpleNamespace or None
    """
    ...
    try:
        if hasattr(self.campaign.category, category_name):
            return getattr(self.campaign.category, category_name)
        else:
            logger.warning(f"Category {category_name} not found in the campaign.")
            return
    except Exception as ex:
        logger.error(f"Error retrieving category {category_name}.", ex, exc_info=True)
        return
```

**Назначение**: Возвращает объект `SimpleNamespace` для заданного имени категории.

**Параметры**:
- `category_name` (str): Имя категории для получения.

**Возвращает**:
- `Optional[SimpleNamespace]`: Объект `SimpleNamespace`, представляющий категорию, или `None`, если категория не найдена.

**Как работает функция**:
- Проверяет, существует ли атрибут с именем категории в объекте `self.campaign.category`.
- Если категория найдена, возвращает соответствующий атрибут.
- Если категория не найдена, логирует предупреждение и возвращает `None`.
- Логирует ошибку, если происходит исключение при получении категории.

**Примеры**:
```python
editor = AliCampaignEditor(campaign_name="Summer Sale")
category = editor.get_category("Electronics")
print(category)  # SimpleNamespace or None
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
        >>> print(categories)  # ['Electronics', 'Fashion', 'Home']
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

**Назначение**: Получает список категорий в текущей кампании.

**Параметры**:
- None

**Возвращает**:
- `Optional[List[str]]`: Список названий категорий или `None`, если категории не найдены.

**Как работает функция**:
- Проверяет, есть ли у кампании атрибут `category` и является ли он экземпляром `SimpleNamespace`.
- Если да, возвращает список ключей (названий категорий) из атрибута `category`.
- Если нет, логирует предупреждение и возвращает `None`.
- Логирует ошибку, если происходит исключение при получении списка категорий.

**Примеры**:
```python
editor = AliCampaignEditor(campaign_name="Summer Sale")
categories = editor.categories_list
print(categories)  # ['Electronics', 'Fashion', 'Home']
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
            f"No JSON files found for {category_name=} at {category_path=}.\nStart prepare category"
        )
        self.process_category_products(category_name)
        return 
```

**Назначение**: Читает данные о товарах из JSON-файлов для конкретной категории.

**Параметры**:
- `category_name` (str): Имя категории.

**Возвращает**:
- `Optional[List[SimpleNamespace]]`: Список объектов `SimpleNamespace`, представляющих товары.

**Как работает функция**:
- Формирует путь к директории категории на основе `base_path`, `category_name`, `language` и `currency`.
- Получает список JSON-файлов в директории категории с помощью `get_filenames_from_directory`.
- Если JSON-файлы найдены, перебирает их и загружает данные о товарах с помощью `j_loads_ns`.
- Создает объекты `SimpleNamespace` для каждого товара и добавляет их в список `products`.
- Если JSON-файлы не найдены, логирует ошибку и запускает процесс подготовки товаров для категории с помощью `process_category_products`.

**Примеры**:
```python
products = campaign.get_category_products("Electronics")
print(len(products))
# 15
```

## Параметры класса

- `campaign_name` (str): Название кампании.
- `language` (Optional[str | dict]): Язык кампании. По умолчанию `None`.
- `currency` (Optional[str]): Валюта кампании. По умолчанию `None`.

## Примеры

Создание экземпляра класса `AliCampaignEditor` с параметрами кампании:

```python
editor = AliCampaignEditor(campaign_name="Summer Sale", language="EN", currency="USD")
```

Удаление продукта из кампании:

```python
editor = AliCampaignEditor(campaign_name="Summer Sale")
editor.delete_product("12345")
```

Обновление категории в JSON-файле:

```python
category = SimpleNamespace(name="New Category", description="Updated description")
editor = AliCampaignEditor(campaign_name="Summer Sale")
result = editor.update_category(Path("category.json"), category)
print(result)  # True if successful