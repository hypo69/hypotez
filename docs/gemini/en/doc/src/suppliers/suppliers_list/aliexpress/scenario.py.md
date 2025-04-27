# Модуль для управления категориями AliExpress

## Обзор

Модуль предназначен для управления категориями товаров на платформе AliExpress. Он позволяет:

- Считывать URL товаров со страницы категории.
- Собирать ссылки на товары со страницы категории с перелистыванием страниц.
- Сравнивать текущее состояние списка категорий на сайте с файлом сценария.
- Обновлять файл сценария категорий на основе данных, полученных с сайта.

## Детали

Модуль использует драйвер веб-браузера (`webdriver`) для сбора информации о категориях с сайта AliExpress. 

## Классы

### `class DBAdaptor`

**Описание**: Класс предоставляет примеры операций с базой данных для работы с категориями AliExpress.

**Inherits**: None

**Attributes**: None

**Methods**:

- `select(cat_id:int = None, parent_id:int = None, project_cat_id:int = None )`:  Пример операции `SELECT`. Выполняет выборку записей из таблицы `AliexpressCategory` с заданными условиями.
- `insert()`: Пример операции `INSERT`. Вставляет новую запись в таблицу `AliexpressCategory`.
- `update()`: Пример операции `UPDATE`. Обновляет запись в таблице `AliexpressCategory` с заданным идентификатором.
- `delete()`: Пример операции `DELETE`. Удаляет запись из таблицы `AliexpressCategory` с заданным идентификатором.

## Функции

### `get_list_products_in_category(s) -> list[str, str]`

**Цель**: Считывает URL товаров со страницы категории.

**Параметры**:

- `s` (`Supplier`): Экземпляр поставщика.
- `run_async` (`bool`): Определяет синхронность/асинхронность исполнения функции `async_get_list_products_in_category()`.

**Возвращает**:

- `list_products_in_category` (`list`): Список собранных URL товаров. Может быть пустым, если в исследуемой категории нет товаров.

**Поднятие исключений**:

- `Exception`: Возникает, если произошла ошибка при чтении URL.

**Пример**:

```python
# Пример использования функции:
from src.suppliers.aliexpress import AliExpress
supplier = AliExpress()
products_in_category = get_list_products_in_category(supplier)
print(products_in_category)
```

### `get_prod_urls_from_pagination(s) -> list[str]`

**Цель**: Собирает ссылки на товары со страницы категории с перелистыванием страниц.

**Параметры**:

- `s` (`Supplier`): Экземпляр поставщика.

**Возвращает**:

- `list_products_in_category` (`list`): Список ссылок, собранных со страницы категории.

**Поднятие исключений**:

- `Exception`: Возникает, если произошла ошибка при чтении URL.

**Пример**:

```python
# Пример использования функции:
from src.suppliers.aliexpress import AliExpress
supplier = AliExpress()
products_in_category = get_prod_urls_from_pagination(supplier)
print(products_in_category)
```

### `update_categories_in_scenario_file(s, scenario_filename: str) -> bool`

**Цель**: Проверка изменений категорий на сайте и обновление файла сценария.

**Параметры**:

- `s` (`Supplier`): Экземпляр поставщика.
- `scenario_filename` (`str`): Имя файла сценария.

**Возвращает**:

- `bool`: `True`, если файл сценария обновлен.

**Поднятие исключений**:

- `Exception`: Возникает, если произошла ошибка при чтении файла сценария или при обновлении данных.

**Пример**:

```python
# Пример использования функции:
from src.suppliers.aliexpress import AliExpress
supplier = AliExpress()
update_categories_in_scenario_file(supplier, 'aliexpress.json')
```

### `get_list_categories_from_site(s,scenario_file,brand=\'\')`

**Цель**: Получение списка категорий с сайта AliExpress.

**Параметры**:

- `s` (`Supplier`): Экземпляр поставщика.
- `scenario_file` (`str`): Имя файла сценария.
- `brand` (`str`):  Название бренда (по умолчанию пустая строка).

**Возвращает**:

- `list`: Список категорий.

**Поднятие исключений**:

- `Exception`: Возникает, если произошла ошибка при получении данных с сайта.

**Пример**:

```python
# Пример использования функции:
from src.suppliers.aliexpress import AliExpress
supplier = AliExpress()
categories = get_list_categories_from_site(supplier, 'aliexpress.json')
print(categories)
```

## Внутренние функции

### `_update_all_ids_in_file()`: 

**Цель**: Обновление идентификаторов категорий в файле сценария.

**Параметры**: None

**Возвращает**: None

**Поднятие исключений**:

- `Exception`: Возникает, если произошла ошибка при обработке файла сценария.

**Пример**:

```python
# Пример использования функции:
_update_all_ids_in_file()
```


## Примечания

- Модуль использует `webdriver` для сбора данных с сайта AliExpress.
- Файл сценария `aliexpress.json` содержит информацию о категориях, их идентификаторах и URL.
- Функция `update_categories_in_scenario_file` сравнивает данные из файла сценария с данными, полученными с сайта, и обновляет файл в случае необходимости.
- Класс `DBAdaptor` предоставляет примеры операций с базой данных для работы с категориями AliExpress.

## Примеры

### Пример работы с категориями

```python
from src.suppliers.aliexpress import AliExpress
from src.suppliers.suppliers_list.aliexpress.scenario import get_list_categories_from_site
from src.suppliers.suppliers_list.aliexpress.scenario import update_categories_in_scenario_file

# Создаем экземпляр поставщика AliExpress
supplier = AliExpress()

# Получаем список категорий с сайта
categories = get_list_categories_from_site(supplier, 'aliexpress.json')

# Обновляем файл сценария
update_categories_in_scenario_file(supplier, 'aliexpress.json')
```

### Пример работы с базой данных

```python
from src.suppliers.suppliers_list.aliexpress.scenario import DBAdaptor

# Создаем экземпляр класса DBAdaptor
db = DBAdaptor()

# Выбираем все записи из таблицы AliexpressCategory, где parent_category_id равен 'parent_id_value'
db.select(parent_id='parent_id_value')

# Вставляем новую запись в таблицу AliexpressCategory
db.insert()

# Обновляем запись в таблице AliexpressCategory, где hypotez_category_id равен 'hypotez_id_value'
db.update()

# Удаляем запись из таблицы AliexpressCategory, где hypotez_category_id равен 'hypotez_id_value'
db.delete()
```