# Модуль для редактирования рекламных кампаний AliExpress

## Обзор

Этот модуль предоставляет инструменты для редактирования рекламных кампаний на AliExpress. Он включает в себя классы и методы для создания, обновления и удаления продуктов, категорий и других параметров кампании.

## Подробней

Модуль `ali_campaign_editor.py` является частью проекта `hypotez` и предназначен для работы с рекламными кампаниями на AliExpress. Он предоставляет функциональность для редактирования кампаний, включая добавление, удаление и обновление продуктов, категорий и других параметров. Модуль использует другие модули проекта, такие как `ali_promo_campaign`, `ali_campaign_google_sheet`, `jjson`, `csv`, `file` и `logger`.

## Классы

### `AliCampaignEditor`

**Описание**: Редактор для рекламных кампаний.

**Наследует**: `AliPromoCampaign`

**Атрибуты**:
- Нет дополнительных атрибутов, кроме тех, что наследуются от `AliPromoCampaign`.

**Методы**:
- `__init__`: Инициализирует объект `AliCampaignEditor`.
- `delete_product`: Удаляет продукт, у которого нет партнерской ссылки.
- `update_product`: Обновляет детали продукта в категории.
- `update_campaign`: Обновляет свойства кампании, такие как описание и теги.
- `update_category`: Обновляет категорию в JSON-файле.
- `get_category`: Возвращает объект `SimpleNamespace` для заданного имени категории.
- `list_categories`: Возвращает список категорий в текущей кампании.
- `get_category_products`: Чтение данных о товарах из JSON файлов для конкретной категории.

#### `__init__`

```python
def __init__(self, 
             campaign_name: str, 
             language: Optional[str | dict] = None, 
             currency: Optional[str] = None) -> None:
    """ Инициализирует AliCampaignEditor с заданными параметрами.

    Args:
        campaign_name (str): Имя кампании.
        language (Optional[str | dict], optional): Язык кампании. По умолчанию 'EN'.
        currency (Optional[str], optional): Валюта для кампании. По умолчанию 'USD'.

    Raises:
        CriticalError: Если не указаны ни `campaign_name`, ни `campaign_file`.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale", language="EN", currency="USD")
    """
    ...
```

#### `delete_product`

```python
def delete_product(self, product_id: str, exc_info: bool = False) -> None:
    """ Удаляет продукт, у которого нет партнерской ссылки.

    Args:
        product_id (str): ID продукта для удаления.
        exc_info (bool): Включать ли информацию об исключении в логи. По умолчанию `False`.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> editor.delete_product("12345")
    """
    ...
```

#### `update_product`

```python
def update_product(self, category_name: str, lang: str, product: dict) -> None:
    """ Обновляет детали продукта в категории.

    Args:
        category_name (str): Имя категории, где нужно обновить продукт.
        lang (str): Язык кампании.
        product (dict): Словарь с деталями продукта.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> editor.update_product("Electronics", "EN", {"product_id": "12345", "title": "Smartphone"})
    """
    ...
```

#### `update_campaign`

```python
def update_campaign(self) -> None:
    """ Обновляет свойства кампании, такие как `description`, `tags` и т.д.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> editor.update_campaign()
    """
    ...
```

#### `update_category`

```python
def update_category(self, json_path: Path, category: SimpleNamespace) -> bool:
    """ Обновляет категорию в JSON-файле.

    Args:
        json_path (Path): Путь к JSON-файлу.
        category (SimpleNamespace): Объект категории для обновления.

    Returns:
        bool: `True`, если обновление успешно, `False` в противном случае.

    Example:
        >>> category = SimpleNamespace(name="New Category", description="Updated description")
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> result = editor.update_category(Path("category.json"), category)
        >>> print(result)  # True если успешно
    """
    ...
```

#### `get_category`

```python
def get_category(self, category_name: str) -> Optional[SimpleNamespace]:
    """ Возвращает объект SimpleNamespace для заданного имени категории.

    Args:
        category_name (str): Имя категории для получения.

    Returns:
        Optional[SimpleNamespace]: Объект SimpleNamespace, представляющий категорию, или `None`, если не найдена.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> category = editor.get_category("Electronics")
        >>> print(category)  # SimpleNamespace или None
    """
    ...
```

#### `list_categories`

```python
def list_categories(self) -> Optional[List[str]]:
    """ Возвращает список категорий в текущей кампании.

    Returns:
        Optional[List[str]]: Список имен категорий или `None`, если категории не найдены.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> categories = editor.categories_list
        >>> print(categories)  # ['Electronics', 'Fashion', 'Home']
    """
    ...
```

#### `get_category_products`

```python
async def get_category_products(self, category_name: str) -> Optional[List[SimpleNamespace]]:
    """ Чтение данных о товарах из JSON файлов для конкретной категории.

    Args:
        category_name (str): Имя категории.

    Returns:
        Optional[List[SimpleNamespace]]: Список объектов SimpleNamespace, представляющих товары.

    Example:
        >>> products = campaign.get_category_products("Electronics")
        >>> print(len(products))
        15
    """
    ...
```
## Методы класса

Здесь представлены методы класса `AliCampaignEditor` и их описания.

### `__init__`
**Назначение**: Инициализирует объект `AliCampaignEditor` с заданными параметрами.

**Параметры**:
- `campaign_name` (str): Имя кампании.
- `language` (Optional[str | dict], optional): Язык кампании. По умолчанию 'EN'.
- `currency` (Optional[str], optional): Валюта для кампании. По умолчанию 'USD'.

**Вызывает исключения**:
- `CriticalError`: Если не указаны ни `campaign_name`, ни `campaign_file`.

**Как работает функция**:
- Вызывает конструктор родительского класса `AliPromoCampaign` для инициализации общих параметров кампании.

**Примеры**:
```python
editor = AliCampaignEditor(campaign_name="Summer Sale", language="EN", currency="USD")
```

### `delete_product`
**Назначение**: Удаляет продукт, у которого нет партнерской ссылки.

**Параметры**:
- `product_id` (str): ID продукта для удаления.
- `exc_info` (bool): Включать ли информацию об исключении в логи. По умолчанию `False`.

**Как работает функция**:
1. Извлекает ID продукта из входного параметра `product_id`.
2. Определяет пути к файлу `sources.txt` и временному файлу `_sources.txt` в каталоге категории.
3. Читает список продуктов из файла `sources.txt`.
4. Если список продуктов существует, перебирает записи в списке.
5. Для каждой записи извлекает ID продукта и сравнивает его с `product_id`.
6. Если ID совпадают, удаляет запись из списка и сохраняет обновленный список во временный файл `_sources.txt`.
7. Если список продуктов не существует, пытается переименовать HTML-файл продукта, добавляя к имени символ "_".

**Примеры**:
```python
editor = AliCampaignEditor(campaign_name="Summer Sale")
editor.delete_product("12345")
```

### `update_product`
**Назначение**: Обновляет детали продукта в категории.

**Параметры**:
- `category_name` (str): Имя категории, где нужно обновить продукт.
- `lang` (str): Язык кампании.
- `product` (dict): Словарь с деталями продукта.

**Как работает функция**:
- Вызывает метод `dump_category_products_files` для обновления информации о продукте в файлах категории.

**Примеры**:
```python
editor = AliCampaignEditor(campaign_name="Summer Sale")
editor.update_product("Electronics", "EN", {"product_id": "12345", "title": "Smartphone"})
```

### `update_campaign`
**Назначение**: Обновляет свойства кампании, такие как `description`, `tags` и т.д.

**Как работает функция**:
- Внутри метода `update_campaign` находится заготовка `...`, указывающая на необходимость добавления логики для обновления параметров кампании.

**Примеры**:
```python
editor = AliCampaignEditor(campaign_name="Summer Sale")
editor.update_campaign()
```

### `update_category`
**Назначение**: Обновляет категорию в JSON-файле.

**Параметры**:
- `json_path` (Path): Путь к JSON-файлу.
- `category` (SimpleNamespace): Объект категории для обновления.

**Возвращает**:
- `bool`: `True`, если обновление успешно, `False` в противном случае.

**Как работает функция**:
1. Читает данные из JSON-файла по указанному пути.
2. Преобразует объект `SimpleNamespace` категории в словарь.
3. Обновляет данные в JSON-файле, записывая словарь категории.
4. Возвращает `True` в случае успеха и `False` в случае ошибки.

**Примеры**:
```python
category = SimpleNamespace(name="New Category", description="Updated description")
editor = AliCampaignEditor(campaign_name="Summer Sale")
result = editor.update_category(Path("category.json"), category)
print(result)  # True если успешно
```

### `get_category`
**Назначение**: Возвращает объект `SimpleNamespace` для заданного имени категории.

**Параметры**:
- `category_name` (str): Имя категории для получения.

**Возвращает**:
- `Optional[SimpleNamespace]`: Объект `SimpleNamespace`, представляющий категорию, или `None`, если не найдена.

**Как работает функция**:
1. Проверяет, существует ли атрибут с именем категории в объекте `self.campaign.category`.
2. Если категория найдена, возвращает соответствующий объект `SimpleNamespace`.
3. Если категория не найдена, регистрирует предупреждение и возвращает `None`.

**Примеры**:
```python
editor = AliCampaignEditor(campaign_name="Summer Sale")
category = editor.get_category("Electronics")
print(category)  # SimpleNamespace или None
```

### `list_categories`
**Назначение**: Возвращает список категорий в текущей кампании.

**Возвращает**:
- `Optional[List[str]]`: Список имен категорий или `None`, если категории не найдены.

**Как работает функция**:
1. Проверяет, существует ли атрибут `category` в объекте `self.campaign` и является ли он экземпляром `SimpleNamespace`.
2. Если атрибут существует и является экземпляром `SimpleNamespace`, возвращает список ключей атрибута `category`.
3. Если атрибут не существует или не является экземпляром `SimpleNamespace`, регистрирует предупреждение и возвращает `None`.

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
    """ Чтение данных о товарах из JSON файлов для конкретной категории.

    Args:
        category_name (str): Имя категории.

    Returns:
        Optional[List[SimpleNamespace]]: Список объектов SimpleNamespace, представляющих товары.
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

**Назначение**: Чтение данных о товарах из JSON файлов для конкретной категории.

**Параметры**:
- `category_name` (str): Имя категории.

**Возвращает**:
- `Optional[List[SimpleNamespace]]`: Список объектов SimpleNamespace, представляющих товары.

**Как работает функция**:
1. Формирует путь к каталогу категории на основе имени категории, языка и валюты.
2. Получает список JSON файлов в каталоге категории.
3. Если JSON файлы найдены, читает данные из каждого файла, преобразует их в объекты SimpleNamespace и добавляет в список товаров.
4. Если JSON файлы не найдены, регистрирует ошибку и запускает процесс подготовки товаров для категории.

**Примеры**:
```python
products = campaign.get_category_products("Electronics")
print(len(products)) # 15