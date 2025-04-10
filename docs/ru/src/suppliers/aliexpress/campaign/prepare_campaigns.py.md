# Модуль для подготовки кампаний AliExpress

## Обзор

Модуль `prepare_campaigns.py` предназначен для автоматизации процесса подготовки рекламных кампаний для AliExpress. Он включает в себя функции для обработки категорий товаров, управления данными кампаний и генерации рекламных материалов.

## Подробнее

Этот модуль предоставляет инструменты для запуска процесса подготовки кампаний AliExpress, позволяя обрабатывать как отдельные категории товаров, так и кампании целиком. Он также поддерживает мультиязычность и разные валюты, что делает его гибким для использования в различных регионах.

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
        ['Product 1', 'Product 2']
    """
    ...
```

**Назначение**: Обрабатывает заданную категорию в рамках рекламной кампании для указанного языка и валюты.

**Параметры**:

-   `campaign_name` (str): Название рекламной кампании.
-   `category_name` (str): Категория товаров для кампании.
-   `language` (str): Язык кампании.
-   `currency` (str): Валюта кампании.

**Возвращает**:

-   `List[str]`: Список наименований товаров в указанной категории.

**Пример**:

```python
titles: List[str] = process_campaign_category("summer_sale", "electronics", "EN", "USD")
print(titles)
# ['Product 1', 'Product 2']
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

-   `bool`: `True`, если кампания успешно обработана, иначе `False`.

**Как работает функция**:

1.  Преобразует список словарей с локалями в список пар (язык, валюта).
2.  Если указаны язык и валюта, фильтрует список локалей по ним.
3.  Для каждой пары (язык, валюта) создается экземпляр `AliCampaignEditor` и вызывается метод `process_campaign`.

**Пример**:

```python
res = process_campaign("summer_sale", "EN", "USD", "campaign_file.json")
```

### `process_all_campaigns`

```python
def process_all_campaigns(language: Optional[str] = None, currency: Optional[str] = None) -> None:
    """Processes all campaigns in the 'campaigns' directory for the specified language and currency.

    Args:
        language (Optional[str]): Language for the campaigns.
        currency (Optional[str]): Currency for the campaigns.

    Example:
        >>> process_all_campaigns("EN", "USD")
    """
    ...
```

**Назначение**: Обрабатывает все кампании, находящиеся в директории `'campaigns'`, для указанного языка и валюты.

**Параметры**:

-   `language` (Optional[str]): Язык для кампаний.
-   `currency` (Optional[str]): Валюта для кампаний.

**Как работает функция**:

1.  Определяет список локалей для обработки на основе предоставленных языка и валюты. Если язык и валюта не указаны, обрабатываются все доступные локали.
2.  Получает список названий всех директорий в каталоге кампаний.
3.  Для каждой кампании создается экземпляр `AliCampaignEditor` и вызывается метод `process_campaign`.

**Пример**:

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
-   `categories` (List[str] | str): Список категорий для кампании. Если список пуст, обрабатывается вся кампания без привязки к категориям.
-   `language` (Optional[str]): Язык кампании.
-   `currency` (Optional[str]): Валюта кампании.

**Как работает функция**:

1.  Определяет локали для обработки на основе предоставленных языка и валюты. Если язык и валюта не указаны, обрабатываются все доступные локали.
2.  Если указаны категории, обрабатывает каждую категорию отдельно, вызывая функцию `process_campaign_category`.
3.  Если категории не указаны, обрабатывает всю кампанию целиком, вызывая функцию `process_campaign`.

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

**Назначение**: Главная функция для разбора аргументов командной строки и запуска процесса обработки кампании.

**Как работает функция**:

1.  Создает парсер аргументов командной строки с описанием параметров.
2.  Разбирает аргументы командной строки, переданные при запуске скрипта.
3.  Если указан аргумент `--all`, запускает обработку всех кампаний.
4.  В противном случае запускает обработку указанной кампании с заданными категориями, языком и валютой.

**Пример**:

```python
main()