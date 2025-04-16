# Модуль `ali_promo_campaign.py`

## Обзор

Модуль `ali_promo_campaign.py` предназначен для управления рекламными кампаниями на платформе AliExpress. Он включает в себя функциональность для обработки данных о категориях и товарах, создания и редактирования JSON-файлов с информацией о кампаниях, а также использование AI для генерации данных о кампаниях. Класс `AliPromoCampaign` позволяет загружать и обрабатывать данные рекламных кампаний, управлять категориями и товарами, а также использовать ИИ для генерации описаний и других данных. Модуль поддерживает различные языки и валюты, обеспечивая гибкость в настройке кампаний.

## Подробнее

Этот модуль играет центральную роль в автоматизации и оптимизации рекламных кампаний на AliExpress. Он предоставляет инструменты для создания, управления и анализа данных кампаний, интегрируя возможности искусственного интеллекта для улучшения контента и повышения эффективности рекламы.

## Классы

### `AliPromoCampaign`

**Описание**: Класс `AliPromoCampaign` предназначен для управления рекламными кампаниями на AliExpress. Он позволяет загружать, обрабатывать и генерировать данные, необходимые для проведения рекламных кампаний.

**Атрибуты**:
- `language` (str): Язык, используемый в кампании.
- `currency` (str): Валюта, используемая в кампании.
- `base_path` (Path): Базовый путь к файлам кампании.
- `campaign_name` (str): Название кампании.
- `campaign` (SimpleNamespace): Объект, представляющий данные кампании.
- `campaign_ai` (SimpleNamespace): Объект, представляющий AI-данные кампании.
- `gemini` (GoogleGenerativeAi): Объект для взаимодействия с моделью Gemini AI.
- `openai` (OpenAIModel): Объект для взаимодействия с моделью OpenAI.

**Методы**:
- `__init__`: Инициализирует объект `AliPromoCampaign`.
- `_models_payload`: Загружает полезные данные для моделей AI.
- `process_campaign`: Итерируется по категориям кампании и обрабатывает товары.
- `process_campaign_category`: Обрабатывает конкретную категорию кампании для всех языков и валют.
- `process_new_campaign`: Создает новую рекламную кампанию.
- `process_llm_category`: Обрабатывает AI-данные для указанной категории.
- `process_category_products`: Обрабатывает товары в указанной категории.
- `dump_category_products_files`: Сохраняет данные о товарах в JSON-файлы.
- `set_categories_from_directories`: Устанавливает категории кампании из названий директорий.
- `generate_output`: Сохраняет данные о товарах в различных форматах.
- `generate_html`: Создает HTML-файл для категории и корневой индексный файл.
- `generate_html_for_campaign`: Генерирует HTML-страницы для рекламной кампании.

## Методы класса

### `__init__`

```python
def __init__(
    self,
    campaign_name: str,
    language: Optional[str] = None,
    currency: Optional[str] = None,
    model:str = 'openai'
)
```

**Назначение**: Инициализирует объект `AliPromoCampaign` для рекламной кампании.

**Параметры**:
- `campaign_name` (str): Название кампании.
- `language` (Optional[str]): Язык, используемый в кампании. По умолчанию `None`.
- `currency` (Optional[str]): Валюта, используемая в кампании. По умолчанию `None`.
- `model` (str): Модель ИИ для использования в кампании. По умолчанию 'openai'.

**Возвращает**:
- `None`

**Примеры**:
```python
campaign = AliPromoCampaign(campaign_name="SummerSale", language="EN", currency="USD")
print(campaign.campaign_name)
```

### `_models_payload`

```python
def _models_payload(self):
    """ """
```

**Назначение**: Загружает полезные данные для моделей AI.

**Параметры**:
- `None`

**Возвращает**:
- `None`

### `process_campaign`

```python
def process_campaign(self):
    """Функция итерируется по категориям рекламной кампании и обрабатывает товары категории через генератор партнерских ссылок.
    """
```

**Назначение**: Итерируется по категориям рекламной кампании и обрабатывает товары категории через генератор партнерских ссылок.

**Параметры**:
- `None`

**Возвращает**:
- `None`

**Пример**:
```python
campaign.process_campaign()
```

### `process_campaign_category`

```python
def process_campaign_category(
    self, category_name: str
) -> list[SimpleNamespace] | None:
```

**Назначение**: Обрабатывает конкретную категорию кампании для всех языков и валют.

**Параметры**:
- `category_name` (str): Категория для обработки.

**Возвращает**:
- `list[SimpleNamespace] | None`: Список товаров в категории или `None` в случае ошибки.

### `process_new_campaign`

```python
def process_new_campaign(
    self,
    campaign_name: str,
    language: Optional[str] = None,
    currency: Optional[str] = None,
):
```

**Назначение**: Создает новую рекламную кампанию.

**Параметры**:
- `campaign_name` (str): Название рекламной кампании.
- `language` (Optional[str]): Язык для кампании. По умолчанию `None`.
- `currency` (Optional[str]): Валюта для кампании. По умолчанию `None`.

**Возвращает**:
- `None`

### `process_llm_category`

```python
def process_llm_category(self, category_name: Optional[str] = None):
```

**Назначение**: Обрабатывает AI-данные для указанной категории.

**Параметры**:
- `category_name` (Optional[str]): Название категории для обработки. Если `None`, обрабатываются все категории. По умолчанию `None`.

**Возвращает**:
- `None`

**Внутренние функции**:

#### `_process_category`

```python
def _process_category(category_name: str):
    """Processes AI-generated category data and updates the campaign category."""
```

**Назначение**: Обрабатывает AI-данные для категории и обновляет данные кампании.

**Параметры**:
- `category_name` (str): Название категории для обработки.

**Возвращает**:
- `None`

#### `get_response`

```python
def get_response(_attempts: int = 5):
    """Gets the response from the AI model."""
```

**Назначение**: Получает ответ от AI-модели.

**Параметры**:
- `_attempts` (int): Количество попыток получения ответа. По умолчанию 5.

**Возвращает**:
- Возвращает `response`

### `process_category_products`

```python
def process_category_products(
    self, category_name: str
) -> Optional[List[SimpleNamespace]]:
```

**Назначение**: Обрабатывает товары в указанной категории.

**Параметры**:
- `category_name` (str): Название категории для обработки.

**Возвращает**:
- `Optional[List[SimpleNamespace]]`: Список объектов `SimpleNamespace`, представляющих товары. Возвращает `None`, если товары не найдены.

**Внутренние функции**:

#### `read_sources`

```python
def read_sources(category_name: str) -> Optional[List[str]]:
    """Reads product sources and extracts product IDs."""
```

**Назначение**: Считывает источники продуктов и извлекает идентификаторы продуктов.

**Параметры**:
- `category_name` (str): Имя категории.

**Возвращает**:
- `Optional[List[str]]`: Список идентификаторов продуктов, если они найдены; в противном случае `None`.

### `dump_category_products_files`

```python
def dump_category_products_files(
    self, category_name: str, products: List[SimpleNamespace]
):
```

**Назначение**: Сохраняет данные о товарах в JSON-файлы.

**Параметры**:
- `category_name` (str): Название категории.
- `products` (List[SimpleNamespace]): Список объектов `SimpleNamespace`, представляющих товары.

**Возвращает**:
- `None`

**Пример**:
```python
campaign.dump_category_products_files("Electronics", products)
```

### `set_categories_from_directories`

```python
def set_categories_from_directories(self):
```

**Назначение**: Устанавливает категории рекламной кампании из названий директорий в `category`.

**Параметры**:
- `None`

**Возвращает**:
- `None`

**Пример**:
```python
self.set_categories_from_directories()
print(self.campaign.category.category1.category_name)
```

### `generate_output`

```python
async def generate_output(self, campaign_name: str, category_path: str | Path, products_list: list[SimpleNamespace] | SimpleNamespace):
```

**Назначение**: Сохраняет данные о товарах в различных форматах.

**Параметры**:
- `campaign_name` (str): Название кампании для выходных файлов.
- `category_path` (str | Path): Путь для сохранения выходных файлов.
- `products_list` (list[SimpleNamespace] | SimpleNamespace): Список товаров или отдельный товар для сохранения.

**Возвращает**:
- `None`

### `generate_html`

```python
async def generate_html(self, campaign_name:str, category_path: str | Path, products_list: list[SimpleNamespace] | SimpleNamespace):
```

**Назначение**: Создает HTML-файл для категории и корневой индексный файл.

**Параметры**:
- `products_list` (list[SimpleNamespace] | SimpleNamespace): Список товаров для включения в HTML.
- `category_path` (str | Path): Путь для сохранения HTML-файла.

**Возвращает**:
- `None`

### `generate_html_for_campaign`

```python
def generate_html_for_campaign(self, campaign_name: str):
```

**Назначение**: Генерирует HTML-страницы для рекламной кампании.

**Параметры**:
- `campaign_name` (str): Имя рекламной кампании.

**Возвращает**:
- `None`

## Параметры класса

- `language` (str): Язык, используемый в кампании.
- `currency` (str): Валюта, используемая в кампании.
- `base_path` (Path): Базовый путь к файлам кампании.
- `campaign_name` (str): Название кампании.
- `campaign` (SimpleNamespace): Объект, представляющий данные кампании.
- `campaign_ai` (SimpleNamespace): Объект, представляющий AI-данные кампании.
- `gemini` (GoogleGenerativeAi): Объект для взаимодействия с моделью Gemini AI.
- `openai` (OpenAIModel): Объект для взаимодействия с моделью OpenAI.

**Примеры**:

```python
campaign = AliPromoCampaign(campaign_name="HolidaySale", language="RU", currency="ILS")
```