# Модуль `campaign`

## Обзор

Модуль `campaign` предназначен для управления процессом создания и публикации рекламных кампаний в Facebook. Он включает в себя функциональность для инициализации параметров кампании (имя, язык, валюта), создания структуры каталогов, сохранения конфигураций для новой кампании, сбора и сохранения данных о продуктах через `ali` или `html`, генерации рекламных материалов, просмотра кампании и публикации ее в Facebook.

## Подробней

Этот модуль играет важную роль в проекте `hypotez`, автоматизируя создание и публикацию рекламных кампаний на Facebook. Он обеспечивает структурированный подход к управлению данными и материалами кампании, начиная от инициализации параметров и заканчивая публикацией готовой кампании.

## Классы

### `AliCampaignEditor`

**Описание**: Класс `AliCampaignEditor` предназначен для редактирования рекламных кампаний на AliExpress. Он предоставляет методы для обновления, удаления и получения информации о продуктах и категориях в рамках кампании.

**Наследует**:
- `AliPromoCampaign`

**Атрибуты**:
- Отсутствуют явные атрибуты, но используются атрибуты родительского класса `AliPromoCampaign`.

**Методы**:
- `delete_product`: Удаляет продукт из кампании.
- `update_product`: Обновляет информацию о продукте в кампании.
- `update_campaign`: Обновляет параметры кампании, такие как описание.
- `update_category`: Обновляет информацию о категории в JSON-файле.
- `get_category`: Получает информацию о категории по её имени.
- `list_categories`: Получает список всех категорий в кампании.
- `get_category_products`: Получает список продуктов для заданной категории.

**Принцип работы**:

Класс `AliCampaignEditor` инициализируется с использованием параметров кампании и предоставляет методы для выполнения различных операций по редактированию кампании. Он использует другие модули и функции для чтения и записи данных, а также для взаимодействия с файловой системой.

```python
class AliCampaignEditor(AliPromoCampaign):
    ...
```

## Методы класса

### `delete_product`

```python
def delete_product(self, product_id: str) -> None:
    """Удаляет продукт из кампании.

    Args:
        product_id (str): ID продукта для удаления.

    Raises:
        FileNotFoundError: Если файл с информацией о продукте не найден.
        Exception: При возникновении других ошибок в процессе удаления.

    Example:
        >>> editor = AliCampaignEditor(campaign_name='test_campaign', language='ru', currency='RUB')
        >>> editor.delete_product('1234567890')
    """
    ...
```

**Назначение**: Удаляет продукт из кампании по его `product_id`.

**Параметры**:
- `product_id` (str): ID продукта, который нужно удалить.

**Возвращает**:
- `None`

**Вызывает исключения**:
- `FileNotFoundError`: Если файл с информацией о продукте не найден.
- `Exception`: При возникновении других ошибок в процессе удаления.

**Как работает функция**:
1. Проверяет наличие партнерской ссылки в `product_id`.
2. Формирует пути к файлам продукта (основной и резервный).
3. Пытается удалить основной файл продукта.
4. Если основной файл не найден, пытается удалить резервный файл.
5. Если ни один из файлов не найден, вызывает исключение `FileNotFoundError`.

**Примеры**:

```python
editor = AliCampaignEditor(campaign_name='test_campaign', language='ru', currency='RUB')
editor.delete_product('1234567890')
```

### `update_product`

```python
def update_product(self, product: dict) -> None:
    """Обновляет информацию о продукте в кампании.

    Args:
        product (dict): Словарь с обновленной информацией о продукте.

    Raises:
        Exception: Если возникает ошибка при обновлении информации о продукте.

    Example:
        >>> editor = AliCampaignEditor(campaign_name='test_campaign', language='ru', currency='RUB')
        >>> product_data = {'product_id': '1234567890', 'title': 'New Title', 'price': 99.99}
        >>> editor.update_product(product_data)
    """
    ...
```

**Назначение**: Обновляет информацию о продукте в кампании, используя данные из переданного словаря.

**Параметры**:
- `product` (dict): Словарь с обновленной информацией о продукте. Обязательно должен содержать ключ `product_id`.

**Возвращает**:
- `None`

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при обновлении информации о продукте.

**Как работает функция**:
1. Формирует путь к файлу продукта на основе `product_id`.
2. Загружает данные категории продукта.
3. Обновляет информацию о продукте в файле.
4. Вызывает метод `dump_category_products_files` для обновления файлов категорий с новыми данными продукта.

**Примеры**:

```python
editor = AliCampaignEditor(campaign_name='test_campaign', language='ru', currency='RUB')
product_data = {'product_id': '1234567890', 'title': 'New Title', 'price': 99.99}
editor.update_product(product_data)
```

### `update_campaign`

```python
def update_campaign(self, description: str) -> None:
    """Обновляет описание кампании.

    Args:
        description (str): Новое описание кампании.

    Raises:
        Exception: Если возникает ошибка при обновлении параметров кампании.

    Example:
        >>> editor = AliCampaignEditor(campaign_name='test_campaign', language='ru', currency='RUB')
        >>> editor.update_campaign('Новое описание кампании')
    """
    ...
```

**Назначение**: Обновляет описание кампании.

**Параметры**:
- `description` (str): Новое описание кампании.

**Возвращает**:
- `None`

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при обновлении параметров кампании.

**Как работает функция**:
1. Обновляет параметр `description` в конфигурации кампании, используя метод `update_params`.

**Примеры**:

```python
editor = AliCampaignEditor(campaign_name='test_campaign', language='ru', currency='RUB')
editor.update_campaign('Новое описание кампании')
```

### `update_category`

```python
def update_category(self, category_name: str, new_category_data: dict) -> None:
    """Обновляет категорию в JSON-файле.

    Args:
        category_name (str): Имя категории для обновления.
        new_category_data (dict): Словарь с новыми данными для категории.

    Raises:
        FileNotFoundError: Если JSON-файл категории не найден.
        KeyError: Если категория не найдена в файле.
        Exception: Если возникает ошибка при обновлении данных категории.

    Example:
        >>> editor = AliCampaignEditor(campaign_name='test_campaign', language='ru', currency='RUB')
        >>> new_data = {'name': 'New Category Name', 'description': 'New Description'}
        >>> editor.update_category('old_category_name', new_data)
    """
    ...
```

**Назначение**: Обновляет данные категории в JSON-файле.

**Параметры**:
- `category_name` (str): Имя категории, которую нужно обновить.
- `new_category_data` (dict): Словарь с новыми данными для категории.

**Возвращает**:
- `None`

**Вызывает исключения**:
- `FileNotFoundError`: Если JSON-файл категории не найден.
- `KeyError`: Если категория не найдена в файле.
- `Exception`: Если возникает ошибка при обновлении данных категории.

**Как работает функция**:
1. Формирует путь к JSON-файлу категории.
2. Загружает данные из JSON-файла.
3. Обновляет данные категории в загруженных данных.
4. Сохраняет обновленные данные обратно в JSON-файл.

**Примеры**:

```python
editor = AliCampaignEditor(campaign_name='test_campaign', language='ru', currency='RUB')
new_data = {'name': 'New Category Name', 'description': 'New Description'}
editor.update_category('old_category_name', new_data)
```

### `get_category`

```python
def get_category(self, category_name: str) -> SimpleNamespace | None:
    """Получает категорию по имени.

    Args:
        category_name (str): Имя категории для поиска.

    Returns:
        SimpleNamespace | None: Объект SimpleNamespace с данными категории, если категория найдена, иначе None.

    Example:
        >>> editor = AliCampaignEditor(campaign_name='test_campaign', language='ru', currency='RUB')
        >>> category = editor.get_category('example_category')
        >>> if category:
        ...     print(category.name, category.description)
    """
    ...
```

**Назначение**: Получает категорию по её имени.

**Параметры**:
- `category_name` (str): Имя категории для поиска.

**Возвращает**:
- `SimpleNamespace | None`: Объект `SimpleNamespace` с данными категории, если категория найдена, иначе `None`.

**Как работает функция**:
1. Получает путь к файлу категории.
2. Проверяет, существует ли файл категории.
3. Если файл существует, возвращает объект `SimpleNamespace` с данными категории.
4. Если файл не существует, логирует предупреждение и возвращает `None`.

**Примеры**:

```python
editor = AliCampaignEditor(campaign_name='test_campaign', language='ru', currency='RUB')
category = editor.get_category('example_category')
if category:
    print(category.name, category.description)
```

### `list_categories`

```python
def list_categories(self) -> list[str]:
    """Получает список всех категорий в кампании.

    Returns:
        list[str]: Список имен категорий.

    Example:
        >>> editor = AliCampaignEditor(campaign_name='test_campaign', language='ru', currency='RUB')
        >>> categories = editor.list_categories()
        >>> print(categories)
    """
    ...
```

**Назначение**: Получает список всех категорий в кампании.

**Параметры**:
- Нет параметров.

**Возвращает**:
- `list[str]`: Список имен категорий.

**Как работает функция**:
1. Проверяет, существуют ли категории в кампании.
2. Если категории существуют, возвращает список их имен.
3. Если категории не существуют, логирует предупреждение и возвращает пустой список.

**Примеры**:

```python
editor = AliCampaignEditor(campaign_name='test_campaign', language='ru', currency='RUB')
categories = editor.list_categories()
print(categories)
```

### `get_category_products`

```python
def get_category_products(self, category_name: str) -> list[SimpleNamespace]:
    """Получает список продуктов для заданной категории.

    Args:
        category_name (str): Имя категории, для которой нужно получить продукты.

    Returns:
        list[SimpleNamespace]: Список продуктов в виде объектов SimpleNamespace.

    Raises:
        FileNotFoundError: Если не найдены файлы продуктов в категории.

    Example:
        >>> editor = AliCampaignEditor(campaign_name='test_campaign', language='ru', currency='RUB')
        >>> products = editor.get_category_products('example_category')
        >>> for product in products:
        ...     print(product.title, product.price)
    """
    ...
```

**Назначение**: Получает список продуктов для заданной категории.

**Параметры**:
- `category_name` (str): Имя категории, для которой нужно получить продукты.

**Возвращает**:
- `list[SimpleNamespace]`: Список продуктов в виде объектов `SimpleNamespace`.

**Вызывает исключения**:
- `FileNotFoundError`: Если не найдены файлы продуктов в категории.

**Как работает функция**:
1. Строит путь к файлам продуктов в категории.
2. Получает список JSON-файлов продуктов в категории.
3. Если файлы не найдены, логирует ошибку и запускает подготовку продуктов для категории.
4. Загружает данные из JSON-файлов и преобразует их в объекты `SimpleNamespace`.
5. Возвращает список продуктов.

**Примеры**:

```python
editor = AliCampaignEditor(campaign_name='test_campaign', language='ru', currency='RUB')
products = editor.get_category_products('example_category')
for product in products:
    print(product.title, product.price)
```

## Другие методы

Методы, такие как `AliPromoCampaign.__init__`, `dump_category_products_files`, `update_params`, и другие, выполняют важные вспомогательные функции, такие как инициализация кампании, сохранение данных в файлы и обновление параметров конфигурации.

## Схемы рабочих процессов

В документе также представлены схемы рабочих процессов для редактирования и подготовки кампаний, которые визуально отображают последовательность шагов и логику выполнения операций. Эти схемы помогают разработчикам понять общий поток данных и взаимосвязи между различными компонентами модуля.