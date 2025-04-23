# Документация модуля управления категориями AliExpress

## Обзор

Этот модуль предоставляет функциональность для управления категориями на AliExpress. Он позволяет извлекать URL-адреса товаров, обновлять списки категорий и взаимодействовать с платформой AliExpress для синхронизации категорий.

### Основные функции:

- **Получение URL-адресов товаров**: Собирает URL-адреса товаров со страниц категорий.
- **Синхронизация категорий**: Сравнивает и обновляет категории на сайте с категориями в локальных файлах сценариев.
- **Взаимодействие с базой данных**: Предлагает операции с базой данных для управления категориями.

## Подробнее

Модуль содержит различные функции и методы для взаимодействия с категориями товаров на AliExpress, включая извлечение URL-адресов товаров, обновление категорий в файлах сценариев и управление данными категорий в базе данных.

## Функции

### `get_list_products_in_category(s: Supplier) -> list[str, str]`

Извлекает список URL-адресов товаров со страницы категории, включая пагинацию.

#### Параметры:

- `s` (Supplier): Экземпляр поставщика с драйвером браузера и локаторами.

#### Возвращает:

- Список URL-адресов товаров со страницы категории.

#### Как работает функция:

Функция `get_list_products_in_category` получает список URL-адресов товаров со страницы категории, обрабатывая пагинацию, если она есть. Функция использует экземпляр `Supplier`, который содержит драйвер браузера и локаторы для взаимодействия с веб-страницей AliExpress.

#### Примеры:

```python
from src.suppliers.suppliers_list.aliexpress.category import get_list_products_in_category
from src.supplier import Supplier

# Пример использования
supplier_instance = Supplier()  # Предполагается, что класс Supplier инициализируется с необходимыми параметрами
category_urls = get_list_products_in_category(supplier_instance)
if category_urls:
    print(f"Найденные URL-адреса товаров: {category_urls[:5]}...")  # Вывод первых 5 URL-адресов для примера
else:
    print("Не удалось получить URL-адреса товаров из категории.")
```

---

### `get_prod_urls_from_pagination(s: Supplier) -> list[str]`

Извлекает URL-адреса товаров со страниц категорий, обрабатывая пагинацию.

#### Параметры:

- `s` (Supplier): Экземпляр поставщика с драйвером браузера и локаторами.

#### Возвращает:

- Список URL-адресов товаров.

#### Как работает функция:

Функция `get_prod_urls_from_pagination` получает URL-адреса товаров со страниц категорий, обрабатывая пагинацию. Функция использует экземпляр `Supplier`, который содержит драйвер браузера и локаторы для взаимодействия с веб-страницей AliExpress.

#### Примеры:

```python
from src.suppliers.suppliers_list.aliexpress.category import get_prod_urls_from_pagination
from src.supplier import Supplier

# Пример использования
supplier_instance = Supplier()  # Предполагается, что класс Supplier инициализируется с необходимыми параметрами
product_urls = get_prod_urls_from_pagination(supplier_instance)
if product_urls:
    print(f"Полученные URL-адреса товаров: {product_urls[:5]}...")  # Вывод первых 5 URL-адресов для примера
else:
    print("Не удалось получить URL-адреса товаров из пагинации.")
```

---

### `update_categories_in_scenario_file(s: Supplier, scenario_filename: str) -> bool`

Сравнивает категории на сайте с категориями в предоставленном файле сценариев и обновляет файл с любыми изменениями.

#### Параметры:

- `s` (Supplier): Экземпляр поставщика с драйвером браузера и локаторами.
- `scenario_filename` (str): Имя файла сценария для обновления.

#### Возвращает:

- `True`, если категории были успешно обновлены, `False` в противном случае.

#### Как работает функция:

Функция `update_categories_in_scenario_file` сравнивает категории на сайте с категориями в файле сценариев и обновляет файл, если есть изменения. Функция использует экземпляр `Supplier` и имя файла сценария.

#### Примеры:

```python
from src.suppliers.suppliers_list.aliexpress.category import update_categories_in_scenario_file
from src.supplier import Supplier

# Пример использования
supplier_instance = Supplier()  # Предполагается, что класс Supplier инициализируется с необходимыми параметрами
scenario_file = 'example_scenario.json'
update_result = update_categories_in_scenario_file(supplier_instance, scenario_file)
if update_result:
    print(f"Файл сценария '{scenario_file}' успешно обновлен.")
else:
    print(f"Не удалось обновить файл сценария '{scenario_file}'.")
```

---

### `get_list_categories_from_site(s: Supplier, scenario_file: str, brand: str = '') -> list`

Извлекает список категорий с сайта AliExpress на основе предоставленного файла сценариев.

#### Параметры:

- `s` (Supplier): Экземпляр поставщика с драйвером браузера и локаторами.
- `scenario_file` (str): Файл сценария, содержащий информацию о категориях.
- `brand` (str, optional): Фильтр по бренду для категорий.

#### Возвращает:

- Список категорий с сайта.

#### Как работает функция:

Функция `get_list_categories_from_site` извлекает список категорий с сайта AliExpress на основе файла сценариев. Она может фильтровать категории по бренду, если указано. Функция использует экземпляр `Supplier` и имя файла сценария.

#### Примеры:

```python
from src.suppliers.suppliers_list.aliexpress.category import get_list_categories_from_site
from src.supplier import Supplier

# Пример использования
supplier_instance = Supplier()  # Предполагается, что класс Supplier инициализируется с необходимыми параметрами
scenario_file = 'example_scenario.json'
categories = get_list_categories_from_site(supplier_instance, scenario_file)
if categories:
    print(f"Полученные категории: {categories[:5]}...")  # Вывод первых 5 категорий для примера
else:
    print("Не удалось получить список категорий с сайта.")

# Пример использования с фильтром по бренду
brand_name = 'ExampleBrand'
branded_categories = get_list_categories_from_site(supplier_instance, scenario_file, brand_name)
if branded_categories:
    print(f"Полученные категории для бренда '{brand_name}': {branded_categories[:5]}...")  # Вывод первых 5 категорий для примера
else:
    print(f"Не удалось получить список категорий для бренда '{brand_name}' с сайта.")
```

---

## Классы

### `DBAdaptor`

Предоставляет методы для взаимодействия с базой данных, позволяя выполнять стандартные операции, такие как `SELECT`, `INSERT`, `UPDATE` и `DELETE` для записей `AliexpressCategory`.

#### Методы:

- `select`: Извлекает записи из таблицы `AliexpressCategory`.
- `insert`: Вставляет новую запись в таблицу `AliexpressCategory`.
- `update`: Обновляет существующую запись в таблице `AliexpressCategory`.
- `delete`: Удаляет запись из таблицы `AliexpressCategory`.

#### Принцип работы:

Класс `DBAdaptor` предоставляет интерфейс для выполнения операций с базой данных, специфичных для категорий AliExpress. Каждый метод соответствует стандартной операции CRUD (Create, Read, Update, Delete).

#### Примеры:

```python
from src.suppliers.suppliers_list.aliexpress.category import DBAdaptor

# Пример использования (предполагается, что DBAdaptor инициализируется с необходимыми параметрами подключения к базе данных)
db_adaptor = DBAdaptor()

# Пример выполнения запроса SELECT
records = db_adaptor.select(where="category_name = 'ExampleCategory'")
if records:
    print(f"Найденные записи: {records}")
else:
    print("Записи не найдены.")

# Пример выполнения запроса INSERT (требуется предварительное создание объекта AliexpressCategory)
# new_category = AliexpressCategory(category_name='NewCategory', category_url='http://example.com/newcategory')
# db_adaptor.insert(new_category)
# print("Новая категория успешно добавлена.")

# Пример выполнения запроса UPDATE (требуется указание условий и новых значений)
# db_adaptor.update(where="category_name = 'OldCategory'", values={'category_name': 'UpdatedCategory'})
# print("Категория успешно обновлена.")

# Пример выполнения запроса DELETE (требуется указание условий)
# db_adaptor.delete(where="category_name = 'CategoryToDelete'")
# print("Категория успешно удалена.")
```

---

## Зависимости

Этот модуль зависит от нескольких других модулей для различной функциональности:

- `src.db.manager_categories.suppliers_categories`: Для управления категориями в базе данных.
- `src.utils.jjson`: Для работы с данными JSON.
- `src.logger`: Для протоколирования ошибок и сообщений.
- `requests`: Для выполнения HTTP-запросов для получения данных о категориях с сайта AliExpress.

---

## Пример использования

```python
from src.suppliers.suppliers_list.aliexpress.category import get_list_products_in_category, update_categories_in_scenario_file
from src.supplier import Supplier

# Пример использования
supplier_instance = Supplier()  # Предполагается, что класс Supplier инициализируется с необходимыми параметрами
category_urls = get_list_products_in_category(supplier_instance)
update_categories_in_scenario_file(supplier_instance, 'example_scenario.json')
```

---

## Лицензия

Этот модуль лицензирован в соответствии с лицензией MIT.