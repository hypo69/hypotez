# Модуль подготовки кампаний AliExpress

## Обзор

Модуль `prepare_campaigns.py` предназначен для подготовки рекламных кампаний на AliExpress. Он включает в себя обработку категорий, управление данными кампаний и генерацию рекламных материалов.

## Подробней

Модуль предоставляет функциональность для обработки конкретных категорий в рамках кампании, а также для обработки всех кампаний в указанной директории. Он использует классы и функции из других модулей проекта, таких как `AliCampaignEditor`, `locales`, `j_loads_ns` и `logger`.

Примеры использования:

Для запуска скрипта для конкретной кампании:

```
python src/suppliers/aliexpress/campaigns/prepare_campaigns.py summer_sale -c electronics -l EN -cu USD
```

Для обработки всех кампаний:

```
python src/suppliers/aliexpress/campaigns/prepare_campaigns.py --all -l EN -cu USD
```

## Функции

### `process_campaign_category`

**Назначение**: Обрабатывает конкретную категорию в рамках кампании для заданного языка и валюты.

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

**Параметры**:

-   `campaign_name` (str): Название рекламной кампании.
-   `category_name` (str): Категория для кампании.
-   `language` (str): Язык для кампании.
-   `currency` (str): Валюта для кампании.

**Возвращает**:

-   `List[str]`: Список названий товаров в категории.

**Примеры**:

```python
titles: List[str] = process_campaign_category("summer_sale", "electronics", "EN", "USD")
print(titles)
# ['Product 1', 'Product 2']
```

**Как работает функция**:

1.  Функция `process_campaign_category` принимает название кампании, название категории, язык и валюту в качестве аргументов.
2.  Создается экземпляр класса `AliCampaignEditor` с переданными параметрами.
3.  Вызывается метод `process_campaign_category` экземпляра `AliCampaignEditor` с названием категории.
4.  Метод `process_campaign_category` возвращает список названий товаров в указанной категории, который затем возвращается функцией `process_campaign_category`.

### `process_campaign`

**Назначение**: Обрабатывает кампанию и управляет ее настройкой и обработкой.

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

**Параметры**:

-   `campaign_name` (str): Название рекламной кампании.
-   `language` (Optional[str]): Язык для кампании. Если не указан, обрабатываются все локали.
-   `currency` (Optional[str]): Валюта для кампании. Если не указана, обрабатываются все локали.
-   `campaign_file` (Optional[str]): Необязательный путь к конкретному файлу кампании.

**Возвращает**:

-   `bool`: `True`, если кампания обработана успешно, иначе `False`.

**Как работает функция**:

1.  Функция `process_campaign` принимает название кампании, язык, валюту и путь к файлу кампании в качестве аргументов.
2.  Создается список кортежей (язык, валюта) на основе доступных локалей. Если указаны язык и валюта, список фильтруется по ним.
3.  Для каждой пары (язык, валюта) создается экземпляр класса `AliCampaignEditor` с переданными параметрами.
4.  Вызывается метод `process_campaign` экземпляра `AliCampaignEditor`, который выполняет обработку кампании.
5.  Функция возвращает `True`, предполагая, что кампания всегда обрабатывается успешно.

**Примеры**:

```python
res = process_campaign("summer_sale", "EN", "USD", "campaign_file.json")
```

### `process_all_campaigns`

**Назначение**: Обрабатывает все кампании в директории `campaigns` для указанного языка и валюты.

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

**Параметры**:

-   `language` (Optional[str]): Язык для кампаний.
-   `currency` (Optional[str]): Валюта для кампаний.

**Как работает функция**:

1.  Функция `process_all_campaigns` принимает язык и валюту в качестве аргументов.
2.  Если язык и валюта не указаны, создается список кортежей (язык, валюта) на основе всех доступных локалей.
3.  Получается список названий каталогов в директории `campaigns`.
4.  Для каждого названия каталога создается экземпляр класса `AliCampaignEditor` с переданными параметрами.
5.  Вызывается метод `process_campaign` экземпляра `AliCampaignEditor`, который выполняет обработку кампании.

**Примеры**:

```python
process_all_campaigns("EN", "USD")
```

### `main_process`

**Назначение**: Главная функция для обработки кампании.

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

**Параметры**:

-   `campaign_name` (str): Название рекламной кампании.
-   `categories` (List[str] | str): Список категорий для кампании. Если пустой, обрабатывается вся кампания без конкретных категорий.
-   `language` (Optional[str]): Язык для кампании.
-   `currency` (Optional[str]): Валюта для кампании.

**Как работает функция**:

1.  Функция `main_process` принимает название кампании, список категорий, язык и валюту в качестве аргументов.
2.  Определяются локали для обработки на основе предоставленных языка и валюты. Если язык и валюта не указаны, используются все доступные локали.
3.  Для каждой локали проверяется, указаны ли категории. Если категории указаны, вызывается функция `process_campaign_category` для каждой категории. Если категории не указаны, вызывается функция `process_campaign` для обработки всей кампании.

**Примеры**:

```python
main_process("summer_sale", ["electronics"], "EN", "USD")
main_process("summer_sale", [], "EN", "USD")
```

### `main`

**Назначение**: Главная функция для разбора аргументов и инициации обработки.

```python
def main() -> None:
    """Main function to parse arguments and initiate processing.

    Example:
        >>> main()
    """
    ...
```

**Как работает функция**:

1.  Функция `main` не принимает аргументов.
2.  Создается экземпляр класса `argparse.ArgumentParser` для разбора аргументов командной строки.
3.  Определяются аргументы командной строки, такие как название кампании, список категорий, язык, валюта и флаг для обработки всех кампаний.
4.  Вызывается метод `parse_args` экземпляра `ArgumentParser`, который разбирает аргументы командной строки.
5.  Если указан флаг для обработки всех кампаний, вызывается функция `process_all_campaigns` с переданными языком и валютой. В противном случае вызывается функция `main_process` с переданными названием кампании, списком категорий, языком и валютой.

**Примеры**:

```python
main()