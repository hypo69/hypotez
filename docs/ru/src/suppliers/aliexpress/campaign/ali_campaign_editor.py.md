# Модуль для редактирования рекламных кампаний AliExpress

## Обзор

Модуль `ali_campaign_editor.py` предназначен для редактирования рекламных кампаний на платформе AliExpress. Он содержит класс `AliCampaignEditor`, который позволяет создавать, обновлять и удалять продукты в кампаниях, а также управлять категориями и другими параметрами кампании. Модуль использует другие модули проекта, такие как `ali_promo_campaign`, `ali_campaign_google_sheet` и другие утилиты для работы с данными и файлами.

## Подробнее

Этот модуль является частью системы управления рекламными кампаниями AliExpress в проекте `hypotez`. Он предоставляет интерфейс для выполнения различных операций над кампаниями, таких как удаление продуктов, обновление информации о продуктах, изменение категорий и т.д. Модуль использует файлы JSON для хранения данных о кампаниях и продуктах, а также предоставляет функции для работы с Google Sheets для импорта и экспорта данных.

## Классы

### `AliCampaignEditor`

**Описание**: Редактор для рекламных кампаний.

**Принцип работы**:
Класс `AliCampaignEditor` наследует функциональность от класса `AliPromoCampaign` и предоставляет методы для редактирования рекламных кампаний AliExpress. Он включает в себя методы для удаления продуктов, обновления информации о продуктах, управления категориями и другими параметрами кампании.

**Наследует**:
- `AliPromoCampaign`: Класс, предоставляющий базовую функциональность для управления рекламными кампаниями AliExpress.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `AliCampaignEditor`.
- `delete_product`: Удаляет продукт, у которого нет партнерской ссылки.
- `update_product`: Обновляет детали продукта в категории.
- `update_campaign`: Обновляет свойства кампании, такие как описание и теги.
- `update_category`: Обновляет категорию в файле JSON.
- `get_category`: Возвращает объект SimpleNamespace для заданного имени категории.
- `list_categories`: Возвращает список категорий в текущей кампании.
- `get_category_products`: Читает данные о товарах из JSON файлов для конкретной категории.

## Функции

### `__init__`

```python
 def __init__(self, 
                 campaign_name: str, 
                 language: Optional[str | dict] = None, 
                 currency: Optional[str] = None):
        """ Initialize the AliCampaignEditor with the given parameters.
        
        Args:
            campaign_name (Optional[str]): The name of the campaign. Defaults to `None`.\n
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

**Назначение**: Инициализация класса `AliCampaignEditor` с заданными параметрами.

**Параметры**:
- `campaign_name` (str): Имя кампании.
- `language` (Optional[str | dict]): Язык кампании. По умолчанию 'EN'.
- `currency` (Optional[str]): Валюта кампании. По умолчанию 'USD'.

**Возвращает**:
- None

**Вызывает исключения**:
- `CriticalError`: Если не указано ни `campaign_name`, ни `campaign_file`.

**Как работает функция**:

1. Функция принимает имя кампании, язык и валюту в качестве параметров.
2.  Вызывается конструктор родительского класса `AliPromoCampaign` с переданными параметрами.
3.  Опционально инициализируется объект `AliCampaignGoogleSheet` для работы с Google Sheets.

```
A[Получение параметров кампании: campaign_name, language, currency]
    ↓
B[Вызов конструктора AliPromoCampaign с этими параметрами]
    ↓
C[Инициализация AliCampaignGoogleSheet (опционально)]
```

**Примеры**:

```python
# 1. Создание экземпляра класса с указанием параметров кампании
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

**Назначение**: Удаление товара, у которого нет партнерской ссылки.

**Параметры**:
- `product_id` (str): ID товара, который нужно удалить.
- `exc_info` (bool): Определяет, нужно ли включать информацию об исключении в логи. По умолчанию `False`.

**Возвращает**:
- None

**Как работает функция**:

1. Извлекает ID товара из входного параметра `product_id`.
2.  Определяет пути к файлу `sources.txt` и временному файлу `_sources.txt` в каталоге категории.
3.  Читает список товаров из файла `sources.txt`.
4.  Если список товаров существует, перебирает записи в списке.
5.  Если `_product_id` существует, извлекает ID записи и сравнивает его с `product_id`.
6.  Если ID совпадают, удаляет запись из списка и сохраняет обновленный список во временный файл `_sources.txt`.
7.  Если `_product_id` не существует, сравнивает запись с `product_id` и, если они совпадают, удаляет запись из списка и сохраняет обновленный список в файл `sources.txt`.
8.  Если список товаров не существует, определяет путь к файлу товара в каталоге `sources`.
9.  Пытается переименовать файл товара, добавляя символ `_` в конец имени.
10. В случае успеха логирует сообщение об успешном переименовании файла.
11. В случае ошибки `FileNotFoundError` логирует сообщение об ошибке, что файл не найден.
12. В случае другой ошибки логирует критическую ошибку с информацией об исключении.

```
A[Получение product_id]
    ↓
B[Определение путей к файлам sources.txt и _sources.txt]
    ↓
C[Чтение списка товаров из sources.txt]
    ↓
D{Список товаров существует?}
    ├── Да
    │   ↓
    │   E[Перебор списка товаров]
    │   ↓
    │   F{Извлечение и сравнение product_id}
    │       ├── Совпадает
    │       │   ↓
    │       │   G[Удаление записи из списка и сохранение во временный файл _sources.txt]
    │       └── Не совпадает
    │           ↓
    │           H[Проверка на соответствие записи и product_id]
    │           ↓
    │           I[Удаление записи из списка и сохранение в sources.txt]
    └── Нет
        ↓
        J[Определение пути к файлу товара в каталоге sources]
        ↓
        K[Попытка переименовать файл товара]
        ↓
        L{Успешно?}
            ├── Да
            │   ↓
            │   M[Логирование успешного переименования]
            └── Нет
                ↓
                N{Ошибка?}
                    ├── FileNotFoundError
                    │   ↓
                    │   O[Логирование ошибки: файл не найден]
                    └── Другая ошибка
                        ↓
                        P[Логирование критической ошибки с информацией об исключении]

```

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

**Назначение**: Обновление информации о продукте в категории.

**Параметры**:
- `category_name` (str): Название категории, в которой нужно обновить продукт.
- `lang` (str): Язык кампании.
- `product` (dict): Словарь, содержащий детали продукта.

**Возвращает**:
- None

**Как работает функция**:

1.  Вызывает метод `dump_category_products_files` с переданными параметрами `category_name`, `lang` и `product`.

```
A[Получение параметров: category_name, lang, product]
    ↓
B[Вызов dump_category_products_files с этими параметрами]
```

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

**Назначение**: Обновление свойств кампании, таких как `description`, `tags` и т.д.

**Параметры**:
- None

**Возвращает**:
- None

**Как работает функция**:

1.  <Код для обновления параметров кампании>

```
A[Вызов функции update_campaign]
    ↓
B[Обновление параметров кампании: description, tags и т.д.]
```

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

**Назначение**: Обновление категории в файле JSON.

**Параметры**:
- `json_path` (Path): Путь к файлу JSON.
- `category` (SimpleNamespace): Объект категории, который нужно обновить.

**Возвращает**:
- `bool`: `True`, если обновление успешно, `False` в противном случае.

**Как работает функция**:

1.  Пытается прочитать данные JSON из файла по указанному пути.
2.  Преобразует объект `SimpleNamespace` категории в словарь.
3.  Обновляет данные категории в прочитанных данных JSON.
4.  Записывает обновленные данные JSON обратно в файл.
5.  В случае успеха возвращает `True`.
6.  В случае ошибки логирует сообщение об ошибке и возвращает `False`.

```
A[Получение параметров: json_path, category]
    ↓
B[Чтение JSON данных из файла]
    ↓
C[Преобразование SimpleNamespace в словарь]
    ↓
D[Обновление данных категории в JSON]
    ↓
E[Запись обновленных данных JSON обратно в файл]
    ↓
F{Успешно?}
    ├── Да
    │   ↓
    │   G[Возврат True]
    └── Нет
        ↓
        H[Логирование ошибки]
        ↓
        I[Возврат False]
```

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
- `category_name` (str): Имя категории, которую нужно получить.

**Возвращает**:
- `Optional[SimpleNamespace]`: Объект `SimpleNamespace`, представляющий категорию, или `None`, если категория не найдена.

**Как работает функция**:

1.  Пытается получить атрибут категории из объекта кампании по имени `category_name`.
2.  Если атрибут существует, возвращает его значение.
3.  Если атрибут не существует, логирует предупреждение и возвращает `None`.
4.  В случае ошибки логирует сообщение об ошибке с информацией об исключении и возвращает `None`.

```
A[Получение параметра: category_name]
    ↓
B[Проверка наличия атрибута category в self.campaign]
    ↓
C{Атрибут существует?}
    ├── Да
    │   ↓
    │   D[Возврат значения атрибута]
    └── Нет
        ↓
        E[Логирование предупреждения]
        ↓
        F[Возврат None]
    ↓
G{Произошла ошибка?}
    ├── Да
    │   ↓
    │   H[Логирование ошибки]
    │   ↓
    │   I[Возврат None]
    └── Нет
        ↓
        J[Конец]
```

**Примеры**:

```python
editor = AliCampaignEditor(campaign_name="Summer Sale")
category = editor.get_category("Electronics")
print(category)  # SimpleNamespace или None
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

**Назначение**: Получение списка категорий в текущей кампании.

**Параметры**:
- None

**Возвращает**:
- `Optional[List[str]]`: Список названий категорий или `None`, если категории не найдены.

**Как работает функция**:

1.  Пытается получить список категорий из объекта кампании.
2.  Проверяет, есть ли у кампании атрибут `category` и является ли он экземпляром `SimpleNamespace`.
3.  Если атрибут существует и является экземпляром `SimpleNamespace`, возвращает список ключей атрибута `category`.
4.  Если атрибут не существует или не является экземпляром `SimpleNamespace`, логирует предупреждение и возвращает `None`.
5.  В случае ошибки логирует сообщение об ошибке и возвращает `None`.

```
A[Вызов функции list_categories]
    ↓
B[Проверка наличия атрибута category в self.campaign и является ли он SimpleNamespace]
    ↓
C{Атрибут существует и является SimpleNamespace?}
    ├── Да
    │   ↓
    │   D[Возврат списка ключей атрибута category]
    └── Нет
        ↓
        E[Логирование предупреждения]
        ↓
        F[Возврат None]
    ↓
G{Произошла ошибка?}
    ├── Да
    │   ↓
    │   H[Логирование ошибки]
    │   ↓
    │   I[Возврат None]
    └── Нет
        ↓
        J[Конец]
```

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
            f"No JSON files found for {category_name=} at {category_path=}.\\nStart prepare category"
        )
        self.process_category_products(category_name)
        return
```

**Назначение**: Чтение данных о товарах из JSON файлов для конкретной категории.

**Параметры**:
- `category_name` (str): Имя категории.

**Возвращает**:
- `Optional[List[SimpleNamespace]]`: Список объектов `SimpleNamespace`, представляющих товары.

**Как работает функция**:

1.  Формирует путь к каталогу категории на основе базового пути, имени категории, языка и валюты.
2.  Получает список JSON файлов в каталоге категории.
3.  Если JSON файлы найдены, перебирает их и читает данные о товарах из каждого файла.
4.  Преобразует данные о товарах в объекты `SimpleNamespace` и добавляет их в список.
5.  Возвращает список товаров.
6.  Если JSON файлы не найдены, логирует сообщение об ошибке и вызывает метод `process_category_products` для подготовки категории.
7.  Возвращает `None`.

```
A[Получение параметра: category_name]
    ↓
B[Формирование пути к каталогу категории]
    ↓
C[Получение списка JSON файлов в каталоге категории]
    ↓
D{JSON файлы найдены?}
    ├── Да
    │   ↓
    │   E[Перебор JSON файлов]
    │   ↓
    │   F[Чтение данных о товарах из файла]
    │   ↓
    │   G[Преобразование данных в объект SimpleNamespace]
    │   ↓
    │   H[Добавление объекта в список]
    │   ↓
    │   I[Возврат списка товаров]
    └── Нет
        ↓
        J[Логирование ошибки]
        ↓
        K[Вызов process_category_products для подготовки категории]
        ↓
        L[Возврат None]
```

**Примеры**:

```python
products = campaign.get_category_products("Electronics")
print(len(products))
15