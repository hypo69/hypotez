# Модуль для работы с гугл-таблицами

## Обзор

Этот модуль содержит код, который демонстрирует взаимодействие с Google Sheets с помощью библиотеки gspread.

## Подробнее

Данный файл `gsheets-step-by-step.py` является примером использования Google Sheets для управления данными кампании в проекте `hypotez`. В нём реализован алгоритм, который позволяет редактировать категории товаров в Google Sheets и затем обновлять данные кампании в соответствии с внесенными изменениями.

## Классы

### `gs`

**Описание**: Объект класса `AliCampaignGoogleSheet`, созданный для работы с Google Sheets. 

**Атрибуты**:

- `gs` (Spreadsheet): Объект Google Sheets, содержащий данные кампании.
- `spreadsheet_id` (str): Идентификатор Google Sheets.

**Методы**:

- `set_categories(categories: list[CategoryType])`:  Метод для загрузки данных о категориях в Google Sheet.
- `get_categories()`:  Метод для получения данных о категориях из Google Sheet.
- `set_category_products(category_name: str, products: list[ProductType])`:  Метод для загрузки данных о товарах в Google Sheet. 

## Функции

### `update_campaign_from_gsheet(campaign_name: str, language: str, currency: str)`

**Назначение**:  Функция выполняет  обновление данных о кампании из Google Sheet.

**Параметры**:

- `campaign_name` (str):  Название кампании.
- `language` (str):  Язык кампании.
- `currency` (str): Валюта кампании.

**Возвращает**: 

- `None`

**Как работает функция**:

1. **Инициализация**:  Создание объектов `AliCampaignEditor` и `AliCampaignGoogleSheet`.
2. **Получение данных**: Извлечение данных о кампании с использованием `AliCampaignEditor`. 
3. **Обработка категорий**: Преобразование данных о категориях в формат, совместимый с Google Sheets.
4. **Обновление Google Sheet**: Загрузка отредактированных данных категорий в Google Sheet.
5. **Обновление данных кампании**: Обновление данных о кампании на основе данных из Google Sheet.

**Примеры**:

```python
update_campaign_from_gsheet(campaign_name='lighting', language='EN', currency='USD')
```

**Внутренние функции**:

### `get_category_products(category_name: str)`

**Назначение**:  Функция получает список товаров для заданной категории.

**Параметры**:

- `category_name` (str):  Название категории.

**Возвращает**:

- `list[ProductType]`:  Список товаров.

**Как работает функция**:

1. **Получение данных**: Извлечение данных о товарах для заданной категории с использованием `AliCampaignEditor`.
2. **Возвращение списка**: Возвращение списка товаров.

**Примеры**:

```python
products = get_category_products(category_name='lighting')
```


### `set_category_products(category_name: str, products: list[ProductType])`

**Назначение**:  Функция загружает данные о товарах для заданной категории в Google Sheet.

**Параметры**:

- `category_name` (str):  Название категории.
- `products` (list[ProductType]): Список товаров.

**Возвращает**:

- `None`

**Как работает функция**:

1. **Получение листа**: Получение нужного листа в Google Sheet.
2. **Загрузка данных**: Загрузка данных о товарах в Google Sheet.

**Примеры**:

```python
set_category_products(category_name='lighting', products=products)
```


## Параметры

- `campaign_name` (str):  Название кампании.
- `language` (str):  Язык кампании.
- `currency` (str):  Валюта кампании.


## Примеры

```python
# Загрузка данных о кампании
campaign_name = "lighting"
language = 'EN'
currency = 'USD'

# Создание объекта кампании
campaign_editor = AliCampaignEditor(campaign_name, language, currency)

# Обновление данных кампании из Google Sheet
update_campaign_from_gsheet(campaign_name, language, currency)
```

```python
# Пример использования функций для работы с товарами

# Получение товаров для категории "lighting"
products = get_category_products(category_name='lighting')

# Загрузка товаров в Google Sheet
set_category_products(category_name='lighting', products=products)
```
```markdown