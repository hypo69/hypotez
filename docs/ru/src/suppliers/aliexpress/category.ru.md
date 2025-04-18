# Модуль управления категориями Aliexpress

## Обзор

Этот модуль предоставляет функциональность для работы с категориями товаров на платформе Aliexpress. Он включает функции для получения ссылок на товары в категории, обновления категорий на основе данных с сайта и операций с базой данных.

## Подробней

Модуль предназначен для управления категориями товаров на Aliexpress и включает в себя следующие ключевые функции:

- Получение списка товаров из категории.
- Обновление категорий в сценарии на основе данных с сайта.
- Операции с базой данных для работы с категориями.

## Функции модуля

### `get_list_products_in_category(s)`

**Назначение**: Считывает URL товаров со страницы категории. Если есть несколько страниц с товарами, функция будет перелистывать все страницы.

**Параметры**:
- `s` (`Supplier`): Экземпляр поставщика.

**Возвращает**:
- Список URL продуктов в категории.

**Как работает функция**:
Функция принимает экземпляр поставщика в качестве аргумента и использует его для считывания URL товаров со страницы категории. Если категория содержит несколько страниц с товарами, функция автоматически перелистывает их, собирая URL с каждой страницы.

**Примеры**:

```python
# Пример использования функции get_list_products_in_category
products = get_list_products_in_category(supplier)
```

### `get_prod_urls_from_pagination(s)`

**Назначение**: Собирает ссылки на товары с страницы категории с перелистыванием страниц.

**Параметры**:
- `s` (`Supplier`): Экземпляр поставщика.

**Возвращает**:
- Список ссылок на товары.

**Как работает функция**:
Функция принимает экземпляр поставщика и использует его для сбора ссылок на товары с текущей страницы категории. Если на странице есть пагинация (перелистывание страниц), функция автоматически переходит на следующие страницы и продолжает сбор ссылок.

**Примеры**:

```python
# Пример использования функции get_prod_urls_from_pagination
product_urls = get_prod_urls_from_pagination(supplier)
```

### `update_categories_in_scenario_file(s, scenario_filename)`

**Назначение**: Проверяет изменения категорий на сайте и обновляет файл сценария.

**Параметры**:
- `s` (`Supplier`): Экземпляр поставщика.
- `scenario_filename` (str): Имя файла сценария для обновления.

**Возвращает**:
- `True`, если обновление прошло успешно.

**Как работает функция**:
Функция принимает экземпляр поставщика и имя файла сценария. Она проверяет, произошли ли изменения в категориях на сайте поставщика, и если да, обновляет файл сценария с новыми данными.

**Примеры**:

```python
# Пример использования функции update_categories_in_scenario_file
updated = update_categories_in_scenario_file(supplier, "scenario_file.json")
```

### `get_list_categories_from_site(s, scenario_file, brand='')`

**Назначение**: Получает список категорий с сайта на основе файла сценария.

**Параметры**:
- `s` (`Supplier`): Экземпляр поставщика.
- `scenario_file` (str): Имя файла сценария.
- `brand` (str, optional): Опциональное имя бренда.

**Возвращает**:
- Список категорий.

**Как работает функция**:
Функция получает список категорий с сайта поставщика на основе информации, содержащейся в файле сценария. Опционально можно указать имя бренда, чтобы фильтровать категории по бренду.

**Примеры**:

```python
# Пример использования функции get_list_categories_from_site
categories = get_list_categories_from_site(supplier, "scenario_file.json", brand="ExampleBrand")
```

### Класс `DBAdaptor`

**Описание**: Предоставляет методы для выполнения операций с базой данных, таких как `SELECT`, `INSERT`, `UPDATE` и `DELETE`.

**Принцип работы**:
Класс `DBAdaptor` предназначен для упрощения взаимодействия с базой данных, в которой хранятся категории товаров. Он предоставляет методы для выполнения основных операций CRUD (Create, Read, Update, Delete) с данными категорий.

**Методы**:

#### `select(cat_id, parent_id, project_cat_id)`

**Назначение**: Выбирает записи из базы данных.

**Параметры**:
- `cat_id`: ID категории.
- `parent_id`: ID родительской категории.
- `project_cat_id`: ID категории проекта.

**Как работает функция**:
Метод `select` выполняет запрос к базе данных для выбора записей, соответствующих заданным критериям (`cat_id`, `parent_id`, `project_cat_id`).

#### `insert()`

**Назначение**: Вставляет новые записи в базу данных.

**Как работает функция**:
Метод `insert` добавляет новые записи в таблицу категорий базы данных.

#### `update()`

**Назначение**: Обновляет записи в базе данных.

**Как работает функция**:
Метод `update` изменяет существующие записи в таблице категорий базы данных.

#### `delete()`

**Назначение**: Удаляет записи из базы данных.

**Как работает функция**:
Метод `delete` удаляет записи из таблицы категорий базы данных.

**Примеры**:

```python
# Пример использования DBAdaptor для операций с базой данных
db = DBAdaptor()
db.select(cat_id=123)
db.insert()
db.update()
db.delete()
```