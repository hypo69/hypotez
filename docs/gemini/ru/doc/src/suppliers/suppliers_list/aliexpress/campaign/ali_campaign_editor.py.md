# Модуль: Редактор рекламных кампаний AliExpress

## Обзор

Модуль `ali_campaign_editor.py` предоставляет класс `AliCampaignEditor`, предназначенный для редактирования рекламных кампаний на платформе AliExpress. Он позволяет управлять параметрами кампаний, обновлять информацию о товарах, категориях и другие свойства.

## Подробнее

Этот модуль является частью проекта `hypotez` и предназначен для автоматизации процессов, связанных с управлением рекламными кампаниями на AliExpress. Он включает в себя функциональность для удаления продуктов, обновления деталей продуктов, редактирования свойств кампании и управления категориями.

## Классы

### `AliCampaignEditor`

**Описание**: Класс `AliCampaignEditor` предназначен для редактирования рекламных кампаний AliExpress. Он наследует функциональность от класса `AliPromoCampaign` и предоставляет дополнительные методы для управления продуктами и категориями.

**Наследует**:

- `AliPromoCampaign`: Предоставляет базовую функциональность для работы с рекламными кампаниями AliExpress.

**Атрибуты**:

- Нет дополнительных атрибутов, кроме унаследованных от `AliPromoCampaign`.

**Методы**:

- `__init__`: Инициализирует экземпляр класса `AliCampaignEditor`.
- `delete_product`: Удаляет продукт, у которого нет партнерской ссылки.
- `update_product`: Обновляет детали продукта в заданной категории.
- `update_campaign`: Обновляет свойства кампании, такие как описание и теги.
- `update_category`: Обновляет категорию в JSON-файле.
- `get_category`: Возвращает объект `SimpleNamespace` для заданной категории.
- `list_categories`: Возвращает список категорий в текущей кампании.
- `get_category_products`: Возвращает список товаров в заданной категории.

#### `__init__`

```python
def __init__(self, 
             campaign_name: str, 
             language: Optional[str | dict] = None, 
             currency: Optional[str] = None):
    """
    Инициализирует AliCampaignEditor с заданными параметрами.

    Args:
        campaign_name (str): Имя кампании.
        language (Optional[str | dict]): Язык кампании. По умолчанию 'EN'.
        currency (Optional[str]): Валюта кампании. По умолчанию 'USD'.
        campaign_file (Optional[str | Path]): Файл `<lang>_<currency>.json` для загрузки из корневой папки кампании. По умолчанию `None`.

    Raises:
        CriticalError: Если не указаны `campaign_name` и `campaign_file`.

    Example:
        # 1. По параметрам кампании
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale", language="EN", currency="USD")
        # 2. Загрузка из файла
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale", campaign_file="EN_USD.JSON")
    """
```

**Назначение**:
Инициализирует объект `AliCampaignEditor`, устанавливая основные параметры кампании, такие как имя, язык и валюта. Если предоставлен `campaign_file`, он пытается загрузить конфигурацию кампании из указанного файла.

**Параметры**:

- `campaign_name` (str): Имя кампании.
- `language` (Optional[str | dict], optional): Язык кампании. По умолчанию `None`.
- `currency` (Optional[str], optional): Валюта кампании. По умолчанию `None`.

**Как работает функция**:

1. Вызывает конструктор родительского класса `AliPromoCampaign` для инициализации базовых параметров кампании.

**Примеры**:

```python
# Инициализация с параметрами кампании
editor = AliCampaignEditor(campaign_name="Summer Sale", language="EN", currency="USD")

# Инициализация с загрузкой из файла
editor = AliCampaignEditor(campaign_name="Summer Sale", campaign_file="EN_USD.JSON")
```

#### `delete_product`

```python
def delete_product(self, product_id: str, exc_info: bool = False):
    """
    Удаляет продукт, у которого нет партнерской ссылки.

    Args:
        product_id (str): ID продукта для удаления.
        exc_info (bool): Включать ли информацию об исключениях в логи. По умолчанию `False`.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> editor.delete_product("12345")
    """
```

**Назначение**:
Удаляет продукт из кампании, если у него отсутствует партнерская ссылка. Функция ищет продукт в файле `sources.txt` или переименовывает соответствующий HTML-файл.

**Параметры**:

- `product_id` (str): ID продукта, который нужно удалить.
- `exc_info` (bool, optional): Флаг, указывающий, нужно ли включать информацию об исключениях в сообщения журнала. По умолчанию `False`.

**Как работает функция**:

1. Извлекает ID продукта с помощью функции `extract_prod_ids`.
2. Определяет пути к файлам `sources.txt` и `_sources.txt` в каталоге категории.
3. Читает список продуктов из файла `sources.txt`.
4. Если список продуктов существует, перебирает записи и удаляет соответствующую запись, если ID продукта совпадает.
5. Сохраняет обновленный список продуктов в файл `_sources.txt`.
6. Если список продуктов не существует, пытается переименовать HTML-файл продукта, добавляя к имени файла символ подчеркивания.
7. Логирует успешное переименование или ошибки, если файл не найден или произошла другая ошибка.

**Примеры**:

```python
# Пример удаления продукта с ID "12345"
editor = AliCampaignEditor(campaign_name="Summer Sale")
editor.delete_product("12345")
```

#### `update_product`

```python
def update_product(self, category_name: str, lang: str, product: dict):
    """
    Обновляет детали продукта в заданной категории.

    Args:
        category_name (str): Имя категории, в которой нужно обновить продукт.
        lang (str): Язык кампании.
        product (dict): Словарь, содержащий детали продукта.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> editor.update_product("Electronics", "EN", {"product_id": "12345", "title": "Smartphone"})
    """
```

**Назначение**:
Обновляет информацию о продукте в указанной категории.

**Параметры**:

- `category_name` (str): Имя категории, в которой находится продукт.
- `lang` (str): Язык кампании.
- `product` (dict): Словарь с деталями продукта для обновления.

**Как работает функция**:

1. Вызывает метод `dump_category_products_files` для обновления информации о продукте.

**Примеры**:

```python
# Пример обновления информации о продукте в категории "Electronics"
editor = AliCampaignEditor(campaign_name="Summer Sale")
editor.update_product("Electronics", "EN", {"product_id": "12345", "title": "Smartphone"})
```

#### `update_campaign`

```python
def update_campaign(self):
    """
    Обновляет свойства кампании, такие как `description`, `tags` и т.д.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> editor.update_campaign()
    """
```

**Назначение**:
Обновляет общие параметры кампании, такие как описание и теги.

**Параметры**:

- Нет параметров.

**Как работает функция**:

1. Функция не реализована (стоит `...`).

**Примеры**:

```python
# Пример обновления параметров кампании
editor = AliCampaignEditor(campaign_name="Summer Sale")
editor.update_campaign()
```

#### `update_category`

```python
def update_category(self, json_path: Path, category: SimpleNamespace) -> bool:
    """
    Обновляет категорию в JSON-файле.

    Args:
        json_path (Path): Путь к JSON-файлу.
        category (SimpleNamespace): Объект категории для обновления.

    Returns:
        bool: True, если обновление успешно, False в противном случае.

    Example:
        >>> category = SimpleNamespace(name="New Category", description="Updated description")
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> result = editor.update_category(Path("category.json"), category)
        >>> print(result)  # True, если успешно
    """
```

**Назначение**:
Обновляет информацию о категории в JSON-файле.

**Параметры**:

- `json_path` (Path): Путь к JSON-файлу, который нужно обновить.
- `category` (SimpleNamespace): Объект `SimpleNamespace`, содержащий обновленные данные категории.

**Возвращает**:

- `bool`: `True`, если обновление выполнено успешно, `False` в случае ошибки.

**Как работает функция**:

1. Читает JSON-данные из файла, используя `j_loads`.
2. Преобразует объект `SimpleNamespace` категории в словарь.
3. Записывает обновленные данные категории в JSON-файл, используя `j_dumps`.
4. Возвращает `True` при успешном обновлении, `False` в случае ошибки.
5. Логирует ошибки с помощью `logger.error`.

**Примеры**:

```python
# Пример обновления категории в JSON-файле
category = SimpleNamespace(name="New Category", description="Updated description")
editor = AliCampaignEditor(campaign_name="Summer Sale")
result = editor.update_category(Path("category.json"), category)
print(result)  # Выведет: True, если успешно
```

#### `get_category`

```python
def get_category(self, category_name: str) -> Optional[SimpleNamespace]:
    """
    Возвращает объект SimpleNamespace для заданной категории.

    Args:
        category_name (str): Имя категории для извлечения.

    Returns:
        Optional[SimpleNamespace]: Объект SimpleNamespace, представляющий категорию, или None, если не найдена.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> category = editor.get_category("Electronics")
        >>> print(category)  # SimpleNamespace или None
    """
```

**Назначение**:
Извлекает объект `SimpleNamespace`, представляющий категорию, по её имени.

**Параметры**:

- `category_name` (str): Имя категории, которую необходимо получить.

**Возвращает**:

- `Optional[SimpleNamespace]`: Объект `SimpleNamespace`, представляющий категорию, или `None`, если категория не найдена.

**Как работает функция**:

1. Проверяет, существует ли атрибут с именем категории в объекте `self.campaign.category`.
2. Если категория найдена, возвращает соответствующий атрибут.
3. Если категория не найдена, записывает предупреждение в журнал и возвращает `None`.
4. Перехватывает возможные исключения и записывает информацию об ошибке в журнал.

**Примеры**:

```python
# Пример получения категории "Electronics"
editor = AliCampaignEditor(campaign_name="Summer Sale")
category = editor.get_category("Electronics")
print(category)  # Выведет: SimpleNamespace или None
```

#### `list_categories`

```python
@property
def list_categories(self) -> Optional[List[str]]:
    """
    Возвращает список категорий в текущей кампании.

    Returns:
        Optional[List[str]]: Список имен категорий или None, если категории не найдены.

    Example:
        >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
        >>> categories = editor.categories_list
        >>> print(categories)  # ['Electronics', 'Fashion', 'Home']
    """
```

**Назначение**:
Возвращает список категорий, определенных в текущей кампании.

**Параметры**:

- Нет параметров.

**Возвращает**:

- `Optional[List[str]]`: Список имен категорий в кампании или `None`, если категории не найдены.

**Как работает функция**:

1. Проверяет, существует ли атрибут `category` в объекте `self.campaign` и является ли он экземпляром `SimpleNamespace`.
2. Если условие выполняется, извлекает имена категорий из атрибутов `self.campaign.category` и возвращает их в виде списка.
3. Если категории не найдены, записывает предупреждение в журнал и возвращает `None`.
4. Перехватывает возможные исключения и записывает информацию об ошибке в журнал.

**Примеры**:

```python
# Пример получения списка категорий
editor = AliCampaignEditor(campaign_name="Summer Sale")
categories = editor.categories_list
print(categories)  # Выведет: ['Electronics', 'Fashion', 'Home']
```

#### `get_category_products`

```python
async def get_category_products(
    self, category_name: str
) -> Optional[List[SimpleNamespace]]:
    """
    Чтение данных о товарах из JSON файлов для конкретной категории.

    Args:
        category_name (str): Имя категории.

    Returns:
        Optional[List[SimpleNamespace]]: Список объектов SimpleNamespace, представляющих товары.

    Example:
        >>> products = campaign.get_category_products("Electronics")
        >>> print(len(products))
        15
    """
```

**Назначение**:
Получает данные о товарах из JSON-файлов для указанной категории.

**Параметры**:

- `category_name` (str): Имя категории, для которой требуется получить список товаров.

**Возвращает**:

- `Optional[List[SimpleNamespace]]`: Список объектов `SimpleNamespace`, представляющих товары в категории. Если JSON-файлы не найдены, возвращает `None`.

**Как работает функция**:

1. Формирует путь к каталогу категории на основе имени категории, языка и валюты.
2. Получает список JSON-файлов в каталоге категории с помощью асинхронной функции `get_filenames_from_directory`.
3. Если JSON-файлы найдены, читает данные из каждого файла, преобразует их в объекты `SimpleNamespace` и добавляет в список товаров.
4. Если JSON-файлы не найдены, записывает сообщение об ошибке в журнал и вызывает метод `process_category_products` для подготовки категории.

**Примеры**:

```python
# Пример получения списка товаров для категории "Electronics"
products = campaign.get_category_products("Electronics")
print(len(products))  # Выведет: 15