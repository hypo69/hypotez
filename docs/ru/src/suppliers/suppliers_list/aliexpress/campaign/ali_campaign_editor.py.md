# Модуль ali_campaign_editor.py

## Обзор

Модуль `ali_campaign_editor.py` предоставляет редактор для рекламных кампаний AliExpress. Он позволяет создавать, изменять и удалять товары в кампаниях, а также обновлять информацию о кампаниях и категориях. Модуль использует классы `AliPromoCampaign` и `AliCampaignGoogleSheet` для управления данными кампаний и интеграции с Google Sheets.

## Подробней

Этот модуль предназначен для редактирования рекламных кампаний AliExpress. Он предоставляет функциональность для удаления товаров, обновления информации о товарах и категориях, а также для обновления свойств кампании, таких как описание и теги. Модуль использует JSON файлы для хранения данных о кампаниях и категориях, а также предоставляет возможность интеграции с Google Sheets для управления данными.

## Классы

### `AliCampaignEditor`

**Описание**: Редактор для рекламных кампаний.
**Наследует**: `AliPromoCampaign`

**Атрибуты**:
- Отсутствуют, так как все атрибуты наследуются от `AliPromoCampaign`.

**Методы**:
- `__init__(self, campaign_name: str, language: Optional[str | dict] = None, currency: Optional[str] = None)`: Инициализирует редактор кампании.
- `delete_product(self, product_id: str, exc_info: bool = False)`: Удаляет товар, у которого нет партнерской ссылки.
- `update_product(self, category_name: str, lang: str, product: dict)`: Обновляет данные товара в категории.
- `update_campaign(self)`: Обновляет свойства кампании, такие как описание и теги.
- `update_category(self, json_path: Path, category: SimpleNamespace) -> bool`: Обновляет категорию в JSON файле.
- `get_category(self, category_name: str) -> Optional[SimpleNamespace]`: Возвращает объект `SimpleNamespace` для указанной категории.
- `list_categories`: Возвращает список категорий в текущей кампании.
- `get_category_products(self, category_name: str) -> Optional[List[SimpleNamespace]]`: Читает данные о товарах из JSON файлов для конкретной категории.

#### `__init__`

```python
def __init__(self, 
             campaign_name: str, 
             language: Optional[str | dict] = None, 
             currency: Optional[str] = None):
    """ Инициализация AliCampaignEditor с заданными параметрами.
    
    Args:
        campaign_name (Optional[str]): Название кампании. По умолчанию `None`.
        language (Optional[str | dict]): Язык кампании. По умолчанию \'EN\'.
        currency (Optional[str]): Валюта для кампании. По умолчанию \'USD\'.
        campaign_file (Optional[str | Path]): При необходимости загружает файл `<lang>_<currency>.json` из корневой папки кампании. По умолчанию `None`.

    Raises:
        CriticalError: Если не указаны `campaign_name` и `campaign_file`.
    
    Example:
    # 1. По параметрам кампании
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale", language="EN", currency="USD")
    # 2. Загрузка из файла
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale", campaign_file="EN_USD.JSON")
    """
    ...
```
**Назначение**: Инициализирует объект `AliCampaignEditor`.

**Параметры**:
- `campaign_name` (str): Название кампании.
- `language` (Optional[str | dict], optional): Язык кампании. По умолчанию `None`.
- `currency` (Optional[str], optional): Валюта кампании. По умолчанию `None`.

**Возвращает**:
- Ничего.

**Как работает функция**:
- Вызывает конструктор родительского класса `AliPromoCampaign` для инициализации общих параметров кампании.

**Примеры**:
```python
# 1. Инициализация с указанием названия, языка и валюты кампании.
editor = AliCampaignEditor(campaign_name="Summer Sale", language="EN", currency="USD")

# 2. Инициализация с загрузкой файла конфигурации кампании.
editor = AliCampaignEditor(campaign_name="Summer Sale", campaign_file="EN_USD.JSON")
```

#### `delete_product`

```python
def delete_product(self, product_id: str, exc_info: bool = False):
    """ Удаляет товар, у которого нет партнерской ссылки.
    
    Args:
        product_id (str): ID товара, который нужно удалить.
        exc_info (bool): Включать ли информацию об исключении в логи. По умолчанию `False`.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> editor.delete_product("12345")
    """
    ...
```
**Назначение**: Удаляет товар из списка товаров кампании.

**Параметры**:
- `product_id` (str): Идентификатор товара, который необходимо удалить.
- `exc_info` (bool, optional): Определяет, нужно ли включать информацию об исключении в логи. По умолчанию `False`.

**Возвращает**:
- Ничего.

**Как работает функция**:
- Извлекает ID товара.
- Определяет путь к файлу `sources.txt`, содержащему список товаров.
- Читает список товаров из файла.
- Если товар найден в списке, он удаляется, и обновленный список сохраняется в файл `_sources.txt`.
- Если товар не найден в списке, функция пытается переименовать файл товара, добавляя к имени файла символ "_".
- Логирует успешное переименование файла или ошибки, если файл не найден или произошла другая ошибка.

**Примеры**:
```python
# 1. Создание экземпляра редактора кампании и удаление товара с указанным ID.
editor = AliCampaignEditor(campaign_name="Summer Sale")
editor.delete_product("12345")
```

#### `update_product`

```python
def update_product(self, category_name: str, lang: str, product: dict):
    """ Обновляет данные товара в категории.

    Args:
        category_name (str): Название категории, в которой нужно обновить товар.
        lang (str): Язык кампании.
        product (dict): Словарь, содержащий данные товара.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> editor.update_product("Electronics", "EN", {"product_id": "12345", "title": "Smartphone"})
    """
    ...
```
**Назначение**: Обновляет данные о товаре в указанной категории.

**Параметры**:
- `category_name` (str): Название категории, в которой находится товар.
- `lang` (str): Язык кампании.
- `product` (dict): Словарь с данными товара для обновления.

**Возвращает**:
- Ничего.

**Как работает функция**:
- Вызывает метод `dump_category_products_files` для сохранения обновленных данных товара в файле категории.

**Примеры**:
```python
# 1. Создание экземпляра редактора кампании и обновление данных товара в категории "Electronics".
editor = AliCampaignEditor(campaign_name="Summer Sale")
editor.update_product("Electronics", "EN", {"product_id": "12345", "title": "Smartphone"})
```

#### `update_campaign`

```python
def update_campaign(self):
    """ Обновляет свойства кампании, такие как `description`, `tags` и т.д.
    
    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> editor.update_campaign()
    """
    ...
```
**Назначение**: Обновляет свойства кампании, такие как описание и теги.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Ничего.

**Как работает функция**:
- Не выполняет никаких действий. Предположительно, здесь должен быть код для обновления параметров кампании.

**Примеры**:
```python
# 1. Создание экземпляра редактора кампании и вызов метода обновления кампании.
editor = AliCampaignEditor(campaign_name="Summer Sale")
editor.update_campaign()
```

#### `update_category`

```python
def update_category(self, json_path: Path, category: SimpleNamespace) -> bool:
    """ Обновляет категорию в JSON файле.

    Args:
        json_path (Path): Путь к JSON файлу.
        category (SimpleNamespace): Объект категории для обновления.

    Returns:
        bool: True, если обновление успешно, False в противном случае.

    Example:
        >>> category = SimpleNamespace(name="New Category", description="Updated description")
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> result = editor.update_category(Path("category.json"), category)
        >>> print(result)  # True, если успешно
    """
    ...
```
**Назначение**: Обновляет информацию о категории в JSON-файле.

**Параметры**:
- `json_path` (Path): Путь к JSON-файлу, который содержит информацию о категориях.
- `category` (SimpleNamespace): Объект `SimpleNamespace`, содержащий обновленные данные категории.

**Возвращает**:
- `bool`: `True`, если обновление категории прошло успешно, и `False` в случае ошибки.

**Как работает функция**:
- Читает JSON данные из файла, указанного в `json_path`.
- Преобразует объект `SimpleNamespace` категории в словарь.
- Записывает обновленные данные категории в JSON-файл.
- Логирует ошибку, если не удалось обновить категорию.

**Примеры**:
```python
# 1. Создание объекта SimpleNamespace с данными новой категории и обновление категории в JSON файле.
category = SimpleNamespace(name="New Category", description="Updated description")
editor = AliCampaignEditor(campaign_name="Summer Sale")
result = editor.update_category(Path("category.json"), category)
print(result)  # True, если успешно
```

#### `get_category`

```python
def get_category(self, category_name: str) -> Optional[SimpleNamespace]:
    """ Возвращает объект SimpleNamespace для указанного имени категории.

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
**Назначение**: Возвращает объект `SimpleNamespace`, представляющий категорию, по её имени.

**Параметры**:
- `category_name` (str): Имя категории, которую нужно получить.

**Возвращает**:
- `Optional[SimpleNamespace]`: Объект `SimpleNamespace`, представляющий категорию, или `None`, если категория не найдена.

**Как работает функция**:
- Проверяет, существует ли атрибут с именем категории в объекте `self.campaign.category`.
- Если категория найдена, возвращает соответствующий объект `SimpleNamespace`.
- Если категория не найдена, логирует предупреждение и возвращает `None`.
- В случае возникновения ошибки логирует ошибку и возвращает `None`.

**Примеры**:
```python
# 1. Создание экземпляра редактора кампании и получение категории "Electronics".
editor = AliCampaignEditor(campaign_name="Summer Sale")
category = editor.get_category("Electronics")
print(category)  # SimpleNamespace или None
```

#### `list_categories`

```python
@property
def list_categories(self) -> Optional[List[str]]:
    """ Получает список категорий в текущей кампании.

    Returns:
        Optional[List[str]]: Список названий категорий или None, если категории не найдены.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> categories = editor.categories_list
        >>> print(categories)  # ['Electronics', 'Fashion', 'Home']
    """
    try:
        # Убедитесь, что у кампании есть атрибут category, и это SimpleNamespace
        if hasattr(self.campaign, 'category') and isinstance(self.campaign.category, SimpleNamespace):
            return list(vars(self.campaign.category).keys())
        else:
            logger.warning("В кампании не найдены категории.")
            return
    except Exception as ex:
        logger.error(f"Ошибка при получении списка категорий: {ex}")
        return
```
**Назначение**: Получает список категорий в текущей кампании.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `Optional[List[str]]`: Список названий категорий или `None`, если категории не найдены.

**Как работает функция**:
- Проверяет, существует ли атрибут `category` у объекта `self.campaign` и является ли он экземпляром класса `SimpleNamespace`.
- Если атрибут существует и является экземпляром `SimpleNamespace`, функция возвращает список ключей атрибута `category`, которые представляют собой названия категорий.
- Если атрибут не существует или не является экземпляром `SimpleNamespace`, функция логирует предупреждение и возвращает `None`.
- В случае возникновения ошибки функция логирует ошибку и возвращает `None`.

**Примеры**:
```python
# 1. Создание экземпляра редактора кампании и получение списка категорий.
editor = AliCampaignEditor(campaign_name="Summer Sale")
categories = editor.categories_list
print(categories)  # ['Electronics', 'Fashion', 'Home']
```

#### `get_category_products`

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

**Назначение**: Асинхронно читает данные о товарах из JSON-файлов для указанной категории.

**Параметры**:
- `category_name` (str): Имя категории, для которой требуется получить товары.

**Возвращает**:
- `Optional[List[SimpleNamespace]]`: Список объектов `SimpleNamespace`, представляющих товары, или `None`, если JSON-файлы не найдены.

**Как работает функция**:
1. Формирует путь к директории категории на основе базового пути, имени категории, языка и валюты.
2. Получает список JSON-файлов в директории категории.
3. Если JSON-файлы найдены, функция итерируется по ним, читает данные из каждого файла, преобразует данные в объект `SimpleNamespace` и добавляет его в список товаров.
4. Если JSON-файлы не найдены, функция логирует ошибку и запускает процесс подготовки товаров для категории.

**Примеры**:
```python
# 1. Получение списка товаров для категории "Electronics".
products = campaign.get_category_products("Electronics")
print(len(products))  # 15
```