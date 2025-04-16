# Модуль для подготовки кампаний AliExpress

## Обзор

Модуль `prepare_campaigns.py` предназначен для автоматизации подготовки рекламных кампаний на платформе AliExpress. Он включает в себя обработку категорий товаров, управление данными кампаний и генерацию рекламных материалов. Модуль позволяет обрабатывать как отдельные категории в рамках кампании, так и кампании целиком, поддерживая различные языки и валюты.

## Подробней

Этот модуль является частью проекта `hypotez` и отвечает за подготовку рекламных кампаний для AliExpress. Он использует другие модули проекта, такие как `AliCampaignEditor` для редактирования кампаний и `locales` для определения языковых и валютных настроек.

## Классы

В данном модуле классы отсутствуют.

## Функции

### `process_campaign_category`

```python
def process_campaign_category(
    campaign_name: str, category_name: str, language: str, currency: str
) -> List[str]:
    """Processes a specific category within a campaign for a given language and currency.

    Args:
        campaign_name (str): Name of the advertising campaign.
        category_name (str): Category for the campaign.
        language (str): Language for the campaign.
        currency (str): Currency for the campaign.

    Returns:
        List[str]: List of product titles within the category.

    Example:
        >>> titles: List[str] = process_campaign_category("summer_sale", "electronics", "EN", "USD")
        >>> print(titles)
        [\'Product 1\', \'Product 2\']
    """
    ...
```

**Назначение**: Обрабатывает заданную категорию в рамках рекламной кампании для указанного языка и валюты.

**Параметры**:

-   `campaign_name` (str): Название рекламной кампании.
-   `category_name` (str): Название категории для кампании.
-   `language` (str): Язык кампании.
-   `currency` (str): Валюта кампании.

**Возвращает**:

-   `List[str]`: Список наименований продуктов в рамках категории.

**Как работает функция**:

1.  Инициализирует экземпляр класса `AliCampaignEditor` с указанными параметрами кампании (название, язык, валюта).
2.  Вызывает метод `process_campaign_category` экземпляра `AliCampaignEditor` для обработки заданной категории.
3.  Возвращает список наименований продуктов, полученных в результате обработки категории.

**Примеры**:

```python
titles: List[str] = process_campaign_category("summer_sale", "electronics", "EN", "USD")
print(titles)
# Вывод: ['Product 1', 'Product 2']
```

### `process_campaign`

```python
def process_campaign(
    campaign_name: str,
    language: Optional[str] = None,
    currency: Optional[str] = None,
    campaign_file: Optional[str] = None,
) -> bool:
    """Processes a campaign and handles the campaign's setup and processing.

    Args:
        campaign_name (str): Name of the advertising campaign.
        language (Optional[str]): Language for the campaign. If not provided, process for all locales.
        currency (Optional[str]): Currency for the campaign. If not provided, process for all locales.
        campaign_file (Optional[str]): Optional path to a specific campaign file.

    Example:
        >>> res = process_campaign("summer_sale", "EN", "USD", "campaign_file.json")

    Returns:
        bool: True if campaign processed, else False.
    """
    ...
```

**Назначение**: Обрабатывает рекламную кампанию, выполняя её настройку и обработку.

**Параметры**:

-   `campaign_name` (str): Название рекламной кампании.
-   `language` (Optional[str]): Язык кампании. Если не указан, обрабатываются все локали.
-   `currency` (Optional[str]): Валюта кампании. Если не указана, обрабатываются все локали.
-   `campaign_file` (Optional[str]): Необязательный путь к файлу кампании.

**Возвращает**:

-   `bool`: `True`, если кампания обработана успешно, иначе `False`.

**Как работает функция**:

1.  Формирует список локалей (`_l`) на основе доступных языков и валют, определенных в `locales`.
2.  Если указаны язык и валюта, фильтрует список локалей, чтобы оставить только указанную пару.
3.  Перебирает список локалей, обрабатывая каждую пару язык-валюта.
4.  Для каждой локали инициализирует экземпляр класса `AliCampaignEditor` с указанными параметрами кампании (название, язык, валюта).
5.  Вызывает метод `process_campaign` экземпляра `AliCampaignEditor` для обработки кампании.
6.  Предполагается, что кампания всегда обрабатывается успешно, поэтому функция всегда возвращает `True`.

**Примеры**:

```python
res = process_campaign("summer_sale", "EN", "USD", "campaign_file.json")
```

### `process_all_campaigns`

```python
def process_all_campaigns(language: Optional[str] = None, currency: Optional[str] = None) -> None:
    """Processes all campaigns in the \'campaigns\' directory for the specified language and currency.

    Args:
        language (Optional[str]): Language for the campaigns.
        currency (Optional[str]): Currency for the campaigns.

    Example:
        >>> process_all_campaigns("EN", "USD")
    """
    ...
```

**Назначение**: Обрабатывает все кампании, находящиеся в директории 'campaigns', для указанного языка и валюты.

**Параметры**:

-   `language` (Optional[str]): Язык для кампаний.
-   `currency` (Optional[str]): Валюта для кампаний.

**Как работает функция**:

1.  Определяет список локалей (`_l`) для обработки. Если язык и валюта не указаны, обрабатываются все доступные локали.
2.  Получает список названий директорий кампаний из директории `campaigns_directory` с помощью функции `get_directory_names`.
3.  Перебирает список названий кампаний.
4.  Для каждой кампании инициализирует экземпляр класса `AliCampaignEditor` с указанными параметрами кампании (название, язык, валюта).
5.  Вызывает метод `process_campaign` экземпляра `AliCampaignEditor` для обработки кампании.

**Примеры**:

```python
process_all_campaigns("EN", "USD")
```

### `main_process`

```python
def main_process(campaign_name: str, categories: List[str] | str, language: Optional[str] = None, currency: Optional[str] = None) -> None:
    """Main function to process a campaign.

    Args:
        campaign_name (str): Name of the advertising campaign.
        categories (List[str]): List of categories for the campaign. If empty, process the campaign without specific categories.
        language (Optional[str]): Language for the campaign.
        currency (Optional[str]): Currency for the campaign.

    Example:
        >>> main_process("summer_sale", ["electronics"], "EN", "USD")
        >>> main_process("summer_sale", [], "EN", "USD")
    """
    ...
```

**Назначение**: Главная функция для обработки кампании.

**Параметры**:

-   `campaign_name` (str): Название рекламной кампании.
-   `categories` (List[str] | str): Список категорий для кампании. Если пустой, обрабатывается вся кампания без указания конкретных категорий.
-   `language` (Optional[str]): Язык кампании.
-   `currency` (Optional[str]): Валюта кампании.

**Как работает функция**:

1.  Определяет список локалей для обработки на основе предоставленных языка и валюты. Если язык и валюта не указаны, используются все доступные локали.
2.  Перебирает список локалей.
3.  Если указаны категории, перебирает их и вызывает функцию `process_campaign_category` для каждой категории.
4.  Если категории не указаны, вызывает функцию `process_campaign` для обработки всей кампании.

**Примеры**:

```python
main_process("summer_sale", ["electronics"], "EN", "USD")
main_process("summer_sale", [], "EN", "USD")
```

### `main`

```python
def main() -> None:
    """Main function to parse arguments and initiate processing.

    Example:
        >>> main()
    """
    ...
```

**Назначение**: Главная функция для разбора аргументов командной строки и запуска обработки кампании.

**Как работает функция**:

1.  Создает экземпляр класса `ArgumentParser` для разбора аргументов командной строки.
2.  Добавляет аргументы:
    -   `campaign_name`: Название кампании.
    -   `-c, --categories`: Список категорий.
    -   `-l, --language`: Язык кампании.
    -   `-cu, --currency`: Валюта кампании.
    -   `--all`: Флаг для обработки всех кампаний.
3.  Разбирает аргументы командной строки с помощью метода `parse_args`.
4.  Если указан флаг `--all`, вызывает функцию `process_all_campaigns` с указанными языком и валютой.
5.  Иначе вызывает функцию `main_process` с указанными названием кампании, списком категорий (или пустым списком, если категории не указаны), языком и валютой.

**Примеры**:

```python
main()