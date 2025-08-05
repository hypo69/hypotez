# Модуль для подготовки кампаний AliExpress
## Обзор
Модуль `prepare_campaigns.py` используется для подготовки кампаний AliExpress. Он обрабатывает категории, данные кампаний и генерирует рекламные материалы.

## Детали
Модуль `prepare_campaigns.py` находится в папке `src/suppliers/aliexpress/campaign` проекта `hypotez`. Он предоставляет набор функций для обработки данных AliExpress, которые затем используются для создания рекламных материалов.

## TOC
- ## Классы
    - ### `AliCampaignEditor`
- ## Функции
    - ### `process_campaign_category`
    - ### `process_campaign`
    - ### `process_all_campaigns`
    - ### `main_process`
    - ### `main`

## Классы
### `AliCampaignEditor`
**Описание**: Класс для обработки данных кампаний AliExpress.

**Attributes**:
- `campaign_name` (str): Название рекламной кампании.
- `language` (str): Язык кампании.
- `currency` (str): Валюта кампании.

**Methods**:
- `process_campaign_category(category_name: str) -> List[str]`: Обрабатывает категорию в рамках кампании и возвращает список названий товаров.
- `process_campaign() -> None`: Обрабатывает всю кампанию.

## Функции
### `process_campaign_category`
**Purpose**: Обрабатывает категорию в рамках кампании для заданного языка и валюты.

**Parameters**:
- `campaign_name` (str): Название рекламной кампании.
- `category_name` (str): Категория для кампании.
- `language` (str): Язык для кампании.
- `currency` (str): Валюта для кампании.

**Returns**:
- `List[str]`: Список названий товаров в категории.

**Raises Exceptions**:
- `Exception`: Если возникает ошибка при обработке категории.

**Examples**:
```python
>>> titles: List[str] = process_campaign_category("summer_sale", "electronics", "EN", "USD")
>>> print(titles)
['Product 1', 'Product 2']
```

**How the Function Works**:
- Создает экземпляр класса `AliCampaignEditor` с заданными параметрами.
- Вызывает метод `process_campaign_category` для обработки категории.
- Возвращает список названий товаров, полученных из обработанной категории.

### `process_campaign`
**Purpose**: Обрабатывает кампанию и управляет настройкой и обработкой кампании.

**Parameters**:
- `campaign_name` (str): Название рекламной кампании.
- `language` (Optional[str]): Язык для кампании. Если не указан, обрабатывается для всех локалей.
- `currency` (Optional[str]): Валюта для кампании. Если не указана, обрабатывается для всех локалей.
- `campaign_file` (Optional[str]): Необязательный путь к файлу с описанием кампании.

**Returns**:
- `bool`: True, если кампания обработана, иначе False.

**Examples**:
```python
>>> res = process_campaign("summer_sale", "EN", "USD", "campaign_file.json")
```

**How the Function Works**:
- Преобразует список словарей в список пар (язык, валюта).
- Если указаны язык и валюта, фильтрует список по ним.
- Обрабатывает каждую пару (язык, валюта), создавая экземпляр `AliCampaignEditor` и вызывая метод `process_campaign()`.

### `process_all_campaigns`
**Purpose**: Обрабатывает все кампании в каталоге `campaigns` для заданного языка и валюты.

**Parameters**:
- `language` (Optional[str]): Язык для кампаний.
- `currency` (Optional[str]): Валюта для кампаний.

**Examples**:
```python
>>> process_all_campaigns("EN", "USD")
```

**How the Function Works**:
- Определяет локали для обработки, основываясь на переданных языке и валюте.
- Проходит по каталогу `campaigns`, обрабатывая каждую кампанию с использованием `AliCampaignEditor` и `process_campaign()`.

### `main_process`
**Purpose**: Главная функция для обработки кампании.

**Parameters**:
- `campaign_name` (str): Название рекламной кампании.
- `categories` (List[str]): Список категорий для кампании. Если пуст, кампания обрабатывается без категорий.
- `language` (Optional[str]): Язык для кампании.
- `currency` (Optional[str]): Валюта для кампании.

**Examples**:
```python
>>> main_process("summer_sale", ["electronics"], "EN", "USD")
>>> main_process("summer_sale", [], "EN", "USD")
```

**How the Function Works**:
- Определяет локали для обработки на основе заданных языка и валюты.
- Если заданы категории, обрабатывает каждую категорию с помощью `process_campaign_category`.
- Если нет заданных категорий, обрабатывает всю кампанию с помощью `process_campaign`.

### `main`
**Purpose**: Главная функция для парсинга аргументов и запуска обработки.

**Examples**:
```python
>>> main()
```

**How the Function Works**:
- Использует `argparse` для парсинга аргументов командной строки.
- Запускает `process_all_campaigns`, если задан флаг `--all`.
- Вызывает `main_process`, если флаг `--all` не задан.