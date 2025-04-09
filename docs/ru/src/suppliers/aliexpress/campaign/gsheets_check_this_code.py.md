# Модуль для работы с Google Sheets в кампаниях AliExpress

## Обзор

Модуль `gsheets_check_this_code.py` предназначен для интеграции с Google Sheets в рамках управления рекламными кампаниями на платформе AliExpress. Он предоставляет инструменты для автоматизации записи и чтения данных о кампаниях, категориях и продуктах, а также для форматирования листов Google Sheets. Модуль использует классы `SpreadSheet` и `AliCampaignEditor` для выполнения основных операций.

## Подробнее

Модуль предоставляет класс `AliCampaignGoogleSheet`, который наследует класс `SpreadSheet` и расширяет его функциональность для работы с данными рекламных кампаний AliExpress. Он позволяет автоматически создавать и обновлять листы Google Sheets с информацией о категориях и продуктах, а также форматировать их для удобства просмотра и анализа.

Модуль включает следующие функции:

-   Автоматическое создание и удаление листов продуктов.
-   Запись данных о кампании, категориях и продуктах в соответствующие листы.
-   Форматирование листов для улучшения читаемости.

## Классы

### `AliCampaignGoogleSheet`

**Описание**: Класс для работы с Google Sheets в рамках кампаний AliExpress.

**Наследует**:

-   `SpreadSheet`: Предоставляет базовые методы для работы с Google Sheets.

**Атрибуты**:

-   `spreadsheet_id` (str): ID Google Sheets таблицы.
-   `spreadsheet` (SpreadSheet): Экземпляр класса `SpreadSheet` для работы с таблицей.
-   `worksheet` (Worksheet): Текущий рабочий лист Google Sheets.
-   `driver` (Driver): Драйвер для управления браузером (Chrome).
-   `editor` (AliCampaignEditor): Редактор кампании AliExpress.

**Методы**:

-   `__init__(campaign_name: str, language: str | dict = None, currency: str = None)`: Инициализирует класс `AliCampaignGoogleSheet` с указанным ID Google Sheets таблицы и дополнительными параметрами.
-   `clear()`: Очищает содержимое листов, удаляет листы продуктов и очищает данные на листах категорий и других указанных листах.
-   `delete_products_worksheets()`: Удаляет все листы из Google Sheets, кроме 'categories', 'product', 'category', 'campaign'.
-   `set_campaign_worksheet(campaign: SimpleNamespace)`: Записывает данные кампании на лист Google Sheets.
-   `set_products_worksheet(category_name: str)`: Записывает данные о продуктах категории на лист Google Sheets.
-   `set_categories_worksheet(categories: SimpleNamespace)`: Записывает данные о категориях на лист Google Sheets.
-   `get_categories()`: Получает данные из таблицы Google Sheets.
-   `set_category_products(category_name: str, products: dict)`: Записывает данные о продуктах в новую таблицу Google Sheets.
-   `_format_categories_worksheet(ws: Worksheet)`: Форматирует лист 'categories'.
-   `_format_category_products_worksheet(ws: Worksheet)`: Форматирует лист с продуктами категории.

### `__init__`

```python
def __init__(self, campaign_name: str, language: str | dict = None, currency: str = None):
    """Инициализирует AliCampaignGoogleSheet с указанным Google Sheets spreadsheet ID и дополнительными параметрами.
    Args:
        campaign_name (str): Название кампании.
        language (str | dict, optional): Язык для кампании. По умолчанию None.
        currency (str, optional): Валюта для кампании. По умолчанию None.
    """
    ...
```

**Назначение**: Инициализирует экземпляр класса `AliCampaignGoogleSheet`.

**Параметры**:

-   `campaign_name` (str): Имя кампании.
-   `language` (str | dict, optional): Язык кампании. По умолчанию `None`.
-   `currency` (str, optional): Валюта кампании. По умолчанию `None`.

**Как работает функция**:

1.  Вызывает конструктор родительского класса `SpreadSheet` с указанным `spreadsheet_id`.
2.  Инициализирует атрибут `editor` экземпляром класса `AliCampaignEditor` с переданными параметрами `campaign_name`, `language` и `currency`.
3.  Вызывает метод `clear()` для очистки существующих данных в таблице.
4.  Вызывает метод `set_campaign_worksheet()` для записи данных кампании в лист `campaign`.
5.  Вызывает метод `set_categories_worksheet()` для записи данных о категориях в лист `categories`.
6.  Открывает Google Sheets в браузере, используя `driver.get_url()`.

```
A.__init__
|
-- super().__init__
|
-- self.editor = AliCampaignEditor(...)
|
-- self.clear()
|
-- self.set_campaign_worksheet(...)
|
-- self.set_categories_worksheet(...)
|
B.driver.get_url()
```

Где:

-   `A.__init__`: Инициализация экземпляра класса `AliCampaignGoogleSheet`.
-   `B.driver.get_url()`: Открытие Google Sheets в браузере.

### `clear`

```python
def clear(self):
    """Очищает содержимое листов, удаляет листы продуктов и очищает данные на листах категорий и других указанных листах."""
    ...
```

**Назначение**: Очищает содержимое листов, удаляет листы продуктов.

**Как работает функция**:

1.  Вызывает метод `delete_products_worksheets()` для удаления листов продуктов.
2.  Обрабатывает возможное исключение `Exception` при удалении листов и логирует ошибку.

```
A.clear
|
-- B.delete_products_worksheets()
|
-- C.except Exception
```

Где:

-   `A.clear`: Очистка содержимого листов.
-   `B.delete_products_worksheets()`: Удаление листов продуктов.
-   `C.except Exception`: Обработка исключения при удалении листов.

### `delete_products_worksheets`

```python
def delete_products_worksheets(self):
    """Удаляет все листы из Google Sheets, кроме 'categories', 'product', 'category', 'campaign'."""
    ...
```

**Назначение**: Удаляет все листы из Google Sheets, кроме 'categories', 'product', 'category', 'campaign'.

**Как работает функция**:

1.  Определяет множество `excluded_titles` с названиями листов, которые не нужно удалять.
2.  Получает список всех листов в таблице с помощью `self.spreadsheet.worksheets()`.
3.  Итерируется по списку листов и удаляет каждый лист, если его название не входит в `excluded_titles`.
4.  Логирует успешное удаление каждого листа.
5.  Обрабатывает возможное исключение `Exception` и логирует ошибку.

```
A.delete_products_worksheets
|
-- B.excluded_titles = {...}
|
-- C.worksheets = self.spreadsheet.worksheets()
|
-- D.for sheet in worksheets
|   |
|   -- E.if sheet.title not in excluded_titles
|   |   |
|   |   -- F.self.spreadsheet.del_worksheet_by_id(sheet.id)
|   |   |
|   |   -- G.logger.success(...)
|
-- H.except Exception
```

Где:

-   `A.delete_products_worksheets`: Удаление листов продуктов.
-   `B.excluded_titles`: Определение множества исключенных листов.
-   `C.worksheets`: Получение списка всех листов.
-   `D.for sheet in worksheets`: Итерация по листам.
-   `E.if sheet.title not in excluded_titles`: Проверка, нужно ли удалять лист.
-   `F.self.spreadsheet.del_worksheet_by_id(sheet.id)`: Удаление листа.
-   `G.logger.success(...)`: Логирование успешного удаления.
-   `H.except Exception`: Обработка исключения.

### `set_campaign_worksheet`

```python
def set_campaign_worksheet(self, campaign: SimpleNamespace):
    """Записывает данные кампании на лист Google Sheets.
    Args:
        campaign (SimpleNamespace): Объект SimpleNamespace с данными кампании для записи.
    """
    ...
```

**Назначение**: Записывает данные кампании на лист Google Sheets.

**Параметры**:

-   `campaign` (SimpleNamespace): Объект `SimpleNamespace` с данными кампании для записи.

**Как работает функция**:

1.  Получает экземпляр листа Google Sheets с именем 'campaign'.
2.  Формирует список кортежей `vertical_data`, содержащих данные для записи в вертикальном формате (ячейка, заголовок, значение).
3.  Итерируется по списку `vertical_data` и добавляет операции обновления в список `updates`.
4.  Выполняет пакетное обновление листа Google Sheets с помощью `ws.batch_update(updates)`.
5.  Логирует информацию об успешной записи данных кампании.
6.  Обрабатывает возможное исключение `Exception` и логирует ошибку.

```
A.set_campaign_worksheet
|
-- B.ws = self.get_worksheet('campaign')
|
-- C.vertical_data = [...]
|
-- D.updates = []
|
-- E.for cell, header, value in vertical_data
|   |
|   -- F.updates.append(...)
|
-- G.if updates
|   |
|   -- H.ws.batch_update(updates)
|
-- I.logger.info(...)
|
-- J.except Exception
```

Где:

-   `A.set_campaign_worksheet`: Запись данных кампании на лист.
-   `B.ws`: Получение листа 'campaign'.
-   `C.vertical_data`: Формирование данных для записи.
-   `D.updates`: Инициализация списка обновлений.
-   `E.for cell, header, value in vertical_data`: Итерация по данным.
-   `F.updates.append(...)`: Добавление операций обновления.
-   `G.if updates`: Проверка, есть ли обновления.
-   `H.ws.batch_update(updates)`: Пакетное обновление листа.
-   `I.logger.info(...)`: Логирование успешной записи.
-   `J.except Exception`: Обработка исключения.

### `set_products_worksheet`

```python
def set_products_worksheet(self, category_name: str):
    """Записывает данные из списка объектов SimpleNamespace в ячейки Google Sheets.
    Args:
        category_name (str): Название категории для получения продуктов.
    """
    ...
```

**Назначение**: Записывает данные из списка объектов `SimpleNamespace` в ячейки Google Sheets.

**Параметры**:

-   `category_name` (str): Название категории для получения продуктов.

**Как работает функция**:

1.  Получает объект категории и список продуктов из `self.editor.campaign.category` по имени категории.
2.  Копирует лист 'product' и переименовывает его в `category_name`.
3.  Формирует список данных `row_data` для записи в лист Google Sheets, извлекая данные из каждого продукта.
4.  Итерируется по списку `row_data` и обновляет соответствующие строки листа Google Sheets.
5.  Вызывает метод `_format_category_products_worksheet(ws)` для форматирования листа.
6.  Логирует информацию об успешном обновлении продуктов.
7.  Обрабатывает возможное исключение `Exception` и логирует ошибку.

```
A.set_products_worksheet
|
-- B.category = self.editor.campaign.category.category_name
|
-- C.products = category.products
|
-- D.ws = self.copy_worksheet('product', category_name)
|
-- E.row_data = []
|
-- F.for product in products
|   |
|   -- G.row_data.append(...)
|
-- H.for index, row in enumerate(row_data, start=2)
|   |
|   -- I.ws.update(f'A{index}:Y{index}', [row])
|   |
|   -- J.logger.info(...)
|
-- K.self._format_category_products_worksheet(ws)
|
-- L.logger.info(...)
|
-- M.except Exception
```

Где:

-   `A.set_products_worksheet`: Запись данных о продуктах на лист.
-   `B.category`: Получение объекта категории.
-   `C.products`: Получение списка продуктов.
-   `D.ws`: Копирование листа 'product'.
-   `E.row_data`: Инициализация списка данных для записи.
-   `F.for product in products`: Итерация по продуктам.
-   `G.row_data.append(...)`: Формирование данных для строки.
-   `H.for index, row in enumerate(row_data, start=2)`: Итерация по строкам.
-   `I.ws.update(f'A{index}:Y{index}', [row])`: Обновление строки в листе.
-   `J.logger.info(...)`: Логирование успешного обновления.
-   `K.self._format_category_products_worksheet(ws)`: Форматирование листа.
-   `L.logger.info(...)`: Логирование успешного обновления.
-   `M.except Exception`: Обработка исключения.

### `set_categories_worksheet`

```python
def set_categories_worksheet(self, categories: SimpleNamespace):
    """Запись данных из объекта SimpleNamespace с категориями в ячейки Google Sheets.
    Args:
        categories (SimpleNamespace): Объект, где ключи — это категории с данными для записи.
    """
    ...
```

**Назначение**: Запись данных из объекта `SimpleNamespace` с категориями в ячейки Google Sheets.

**Параметры**:

-   `categories` (SimpleNamespace): Объект, где ключи — это категории с данными для записи.

**Как работает функция**:

1.  Получает экземпляр листа Google Sheets с именем 'categories'.
2.  Очищает содержимое листа Google Sheets.
3.  Получает данные категорий из объекта `categories`.
4.  Проверяет наличие необходимых атрибутов у всех объектов категорий.
5.  Формирует заголовки для таблицы.
6.  Формирует данные для записи в таблицу.
7.  Обновляет лист Google Sheets данными.
8.  Вызывает метод `_format_categories_worksheet(ws)` для форматирования листа.
9.  Логирует информацию об успешном обновлении категорий.
10. Обрабатывает возможное исключение `Exception` и логирует ошибку.

```
A.set_categories_worksheet
|
-- B.ws = self.get_worksheet('categories')
|
-- C.ws.clear()
|
-- D.category_data = categories.__dict__
|
-- E.required_attrs = [...]
|
-- F.if all(all(hasattr(category, attr) for attr in required_attrs) for category in category_data.values())
|   |
|   -- G.headers = [...]
|   |
|   -- H.rows = []
|   |
|   -- I.for category in category_data.values()
|   |   |
|   |   -- J.row_data = [...]
|   |   |
|   |   -- K.rows.append(row_data)
|   |
|   -- L.ws.update(f'A2:E{1 + len(rows)}', rows)
|   |
|   -- M.self._format_categories_worksheet(ws)
|   |
|   -- N.logger.info(...)
|
-- O.except Exception
```

Где:

-   `A.set_categories_worksheet`: Запись данных о категориях на лист.
-   `B.ws`: Получение листа 'categories'.
-   `C.ws.clear()`: Очистка листа.
-   `D.category_data`: Получение данных категорий.
-   `E.required_attrs`: Список необходимых атрибутов.
-   `F.if all(...)`: Проверка наличия атрибутов.
-   `G.headers`: Формирование заголовков.
-   `H.rows`: Инициализация списка строк.
-   `I.for category in category_data.values()`: Итерация по категориям.
-   `J.row_data`: Формирование данных для строки.
-   `K.rows.append(row_data)`: Добавление строки в список.
-   `L.ws.update(...)`: Обновление листа.
-   `M.self._format_categories_worksheet(ws)`: Форматирование листа.
-   `N.logger.info(...)`: Логирование успешного обновления.
-   `O.except Exception`: Обработка исключения.

### `get_categories`

```python
def get_categories(self):
    """Получение данных из таблицы Google Sheets.
    Returns:
        Данные из таблицы в виде списка словарей.
    """
    ...
```

**Назначение**: Получение данных из таблицы Google Sheets.

**Возвращает**:

-   `list[dict]`: Данные из таблицы в виде списка словарей.

**Как работает функция**:

1.  Получает экземпляр листа Google Sheets с именем 'categories'.
2.  Получает все записи из листа с помощью `ws.get_all_records()`.
3.  Логирует информацию об успешном получении данных.
4.  Возвращает полученные данные.

```
A.get_categories
|
-- B.ws = self.get_worksheet('categories')
|
-- C.data = ws.get_all_records()
|
-- D.logger.info(...)
|
-- E.return data
```

Где:

-   `A.get_categories`: Получение данных о категориях.
-   `B.ws`: Получение листа 'categories'.
-   `C.data`: Получение всех записей.
-   `D.logger.info(...)`: Логирование успешного получения данных.
-   `E.return data`: Возврат данных.

### `set_category_products`

```python
def set_category_products(self, category_name: str, products: dict):
    """Запись данных о продуктах в новую таблицу Google Sheets.
    Args:
        category_name (str): Название категории.
        products (dict): Словарь с данными о продуктах.
    """
    ...
```

**Назначение**: Запись данных о продуктах в новую таблицу Google Sheets.

**Параметры**:

-   `category_name` (str): Название категории.
-   `products` (dict): Словарь с данными о продуктах.

**Как работает функция**:

1.  Получает объект категории и список продуктов из `self.editor.campaign.category` по имени категории.
2.  Копирует лист 'product' и переименовывает его в `category_name`.
3.  Определяет заголовки для таблицы продуктов.
4.  Формирует список данных `row_data` для записи в лист Google Sheets, извлекая данные из каждого продукта.
5.  Итерируется по списку `row_data` и обновляет соответствующие строки листа Google Sheets.
6.  Вызывает метод `_format_category_products_worksheet(ws)` для форматирования листа.
7.  Логирует информацию об успешном обновлении продуктов.
8.  Обрабатывает возможное исключение `Exception` и логирует ошибку.

```
A.set_category_products
|
-- B.category_ns = ...
|
-- C.products_ns = ...
|
-- D.ws = self.copy_worksheet('product', category_name)
|
-- E.headers = [...]
|
-- F.updates = [...]
|
-- G.row_data = []
|
-- H.for product in products
|   |
|   -- I._ = product.__dict__
|   |
|   -- J.row_data.append(...)
|
-- K.for index, row in enumerate(row_data, start=2)
|   |
|   -- L.ws.update(f'A{index}:Y{index}', [row])
|   |
|   -- M.logger.info(...)
|
-- N.self._format_category_products_worksheet(ws)
|
-- O.logger.info(...)
|
-- P.except Exception
```

Где:

-   `A.set_category_products`: Запись данных о продуктах на лист.
-   `B.category_ns`: Получение объекта категории.
-   `C.products_ns`: Получение списка продуктов.
-   `D.ws`: Копирование листа 'product'.
-   `E.headers`: Определение заголовков.
-   `F.updates`: Формирование данных для заголовков.
-   `G.row_data`: Инициализация списка данных для записи.
-   `H.for product in products`: Итерация по продуктам.
-   `I._ = product.__dict__`: Получение словаря атрибутов продукта.
-   `J.row_data.append(...)`: Формирование данных для строки.
-   `K.for index, row in enumerate(row_data, start=2)`: Итерация по строкам.
-   `L.ws.update(f'A{index}:Y{index}', [row])`: Обновление строки в листе.
-   `M.logger.info(...)`: Логирование успешного обновления.
-   `N.self._format_category_products_worksheet(ws)`: Форматирование листа.
-   `O.logger.info(...)`: Логирование успешного обновления.
-   `P.except Exception`: Обработка исключения.

### `_format_categories_worksheet`

```python
def _format_categories_worksheet(self, ws: Worksheet):
    """Форматирование листа 'categories'.
    Args:
        ws (Worksheet): Лист Google Sheets для форматирования.
    """
    ...
```

**Назначение**: Форматирование листа 'categories'.

**Параметры**:

-   `ws` (Worksheet): Лист Google Sheets для форматирования.

**Как работает функция**:

1.  Устанавливает ширину столбцов A, B, C, D, E.
2.  Устанавливает высоту строки 1 (заголовки).
3.  Определяет формат для заголовков (жирный шрифт, размер 12, выравнивание по центру, серый фон).
4.  Применяет формат к диапазону ячеек A1:E1.
5.  Логирует информацию об успешном форматировании листа.
6.  Обрабатывает возможное исключение `Exception` и логирует ошибку.

```
A._format_categories_worksheet
|
-- B.set_column_width(...)
|
-- C.set_row_height(...)
|
-- D.header_format = cellFormat(...)
|
-- E.format_cell_range(ws, 'A1:E1', header_format)
|
-- F.logger.info(...)
|
-- G.except Exception
```

Где:

-   `A._format_categories_worksheet`: Форматирование листа 'categories'.
-   `B.set_column_width(...)`: Установка ширины столбцов.
-   `C.set_row_height(...)`: Установка высоты строк.
-   `D.header_format`: Определение формата заголовков.
-   `E.format_cell_range(...)`: Применение формата к ячейкам.
-   `F.logger.info(...)`: Логирование успешного форматирования.
-   `G.except Exception`: Обработка исключения.

### `_format_category_products_worksheet`

```python
def _format_category_products_worksheet(self, ws: Worksheet):
    """Форматирование листа с продуктами категории.
    Args:
        ws (Worksheet): Лист Google Sheets для форматирования.
    """
    ...
```

**Назначение**: Форматирование листа с продуктами категории.

**Параметры**:

-   `ws` (Worksheet): Лист Google Sheets для форматирования.

**Как работает функция**:

1.  Устанавливает ширину столбцов A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y.
2.  Устанавливает высоту строки 1 (заголовки).
3.  Определяет формат для заголовков (жирный шрифт, размер 12, выравнивание по центру, серый фон).
4.  Применяет формат к диапазону ячеек A1:Y1.
5.  Логирует информацию об успешном форматировании листа.
6.  Обрабатывает возможное исключение `Exception` и логирует ошибку.

```
A._format_category_products_worksheet
|
-- B.set_column_width(...)
|
-- C.set_row_height(...)
|
-- D.header_format = cellFormat(...)
|
-- E.format_cell_range(ws, 'A1:Y1', header_format)
|
-- F.logger.info(...)
|
-- G.except Exception
```

Где:

-   `A._format_category_products_worksheet`: Форматирование листа продуктов.
-   `B.set_column_width(...)`: Установка ширины столбцов.
-   `C.set_row_height(...)`: Установка высоты строк.
-   `D.header_format`: Определение формата заголовков.
-   `E.format_cell_range(...)`: Применение формата к ячейкам.
-   `F.logger.info(...)`: Логирование успешного форматирования.
-   `G.except Exception`: Обработка исключения.

## Функции

В данном модуле функции отсутствуют.