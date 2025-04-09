# Модуль для подготовки кампаний AliExpress

## Обзор

Модуль `prepare_campaigns.py` предназначен для автоматизации подготовки рекламных кампаний на платформе AliExpress. Он обрабатывает категории товаров, управляет данными кампаний и генерирует рекламные материалы. Модуль позволяет запускать обработку как отдельных кампаний и категорий, так и всех кампаний целиком.

## Подробнее

Этот модуль является частью проекта `hypotez` и отвечает за автоматизацию процесса подготовки рекламных кампаний на AliExpress. Он использует другие модули проекта, такие как `AliCampaignEditor` для обработки данных кампаний и `locales` для поддержки различных языков и валют.

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

**Назначение**: Обрабатывает заданную категорию в рамках кампании для указанного языка и валюты.

**Параметры**:
- `campaign_name` (str): Название рекламной кампании.
- `category_name` (str): Категория для кампании.
- `language` (str): Язык для кампании.
- `currency` (str): Валюта для кампании.

**Возвращает**:
- `List[str]`: Список названий продуктов в категории.

**Как работает функция**:

1.  Функция создает экземпляр класса `AliCampaignEditor` с указанными параметрами кампании (название, язык, валюта).
2.  Вызывает метод `process_campaign_category` у созданного экземпляра `AliCampaignEditor`, передавая название категории.
3.  Возвращает список названий продуктов, полученных в результате обработки категории.

```
Создание AliCampaignEditor   -->  Вызов process_campaign_category  --> Возврат списка названий продуктов
```

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

**Назначение**: Обрабатывает кампанию, выполняя её настройку и обработку.

**Параметры**:
- `campaign_name` (str): Название рекламной кампании.
- `language` (Optional[str]): Язык для кампании. Если не указан, обрабатываются все локали.
- `currency` (Optional[str]): Валюта для кампании. Если не указана, обрабатываются все локали.
- `campaign_file` (Optional[str]): Необязательный путь к файлу кампании.

**Возвращает**:
- `bool`: `True`, если кампания обработана успешно, иначе `False`.

**Как работает функция**:

1.  Формирует список локалей (`_l`) для обработки на основе переданных языка и валюты. Если язык и валюта не указаны, используются все доступные локали из `locales`.
2.  Итерируется по списку локалей (`_l`).
3.  Для каждой локали создает экземпляр класса `AliCampaignEditor` с указанными параметрами кампании (название, язык, валюта).
4.  Вызывает метод `process_campaign` у созданного экземпляра `AliCampaignEditor`.
5.  Предполагает успешную обработку кампании и возвращает `True`.

```
Формирование списка локалей -->  Итерация по локалям  -->  Создание AliCampaignEditor  -->  Вызов process_campaign  -->  Возврат True
```

**Примеры**:

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

**Назначение**: Обрабатывает все кампании в директории `campaigns` для указанного языка и валюты.

**Параметры**:
- `language` (Optional[str]): Язык для кампаний.
- `currency` (Optional[str]): Валюта для кампаний.

**Возвращает**:
- `None`

**Как работает функция**:

1.  Определяет список локалей для обработки. Если язык и валюта не указаны, используются все доступные локали из `locales`.
2.  Получает список названий директорий кампаний из директории `campaigns_directory` с помощью функции `get_directory_names`.
3.  Итерируется по списку названий кампаний.
4.  Для каждой кампании создает экземпляр класса `AliCampaignEditor` с указанными параметрами кампании (название, язык, валюта).
5.  Вызывает метод `process_campaign` у созданного экземпляра `AliCampaignEditor`.

```
Определение списка локалей -->  Получение списка директорий кампаний  -->  Итерация по кампаниям  -->  Создание AliCampaignEditor  -->  Вызов process_campaign
```

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
- `campaign_name` (str): Название рекламной кампании.
- `categories` (List[str] | str): Список категорий для кампании. Если пуст, обрабатывается вся кампания без указания категорий.
- `language` (Optional[str]): Язык для кампании.
- `currency` (Optional[str]): Валюта для кампании.

**Возвращает**:
- `None`

**Как работает функция**:

1.  Определяет список локалей для обработки на основе переданных языка и валюты. Если язык и валюта не указаны, используются все доступные локали из `locales`.
2.  Итерируется по списку локалей.
3.  Если указаны категории, то для каждой категории вызывается функция `process_campaign_category`.
4.  Если категории не указаны, вызывается функция `process_campaign` для обработки всей кампании.

```
Определение списка локалей -->  Итерация по локалям  -->  Проверка категорий  -->  Вызов process_campaign_category или process_campaign
```

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

**Назначение**: Главная функция для разбора аргументов командной строки и инициации обработки кампаний.

**Возвращает**:
- `None`

**Как работает функция**:

1.  Создает парсер аргументов командной строки с помощью `argparse.ArgumentParser`.
2.  Определяет аргументы, которые можно передать скрипту:
    -   `campaign_name`: Название кампании.
    -   `-c`, `--categories`: Список категорий (если не указан, используются все категории).
    -   `-l`, `--language`: Язык для кампании.
    -   `-cu`, `--currency`: Валюта для кампании.
    -   `--all`: Флаг для обработки всех кампаний.
3.  Разбирает переданные аргументы с помощью `parser.parse_args()`.
4.  Если указан флаг `--all`, вызывается функция `process_all_campaigns`.
5.  В противном случае вызывается функция `main_process` с переданными аргументами.

```
Создание парсера аргументов  -->  Определение аргументов  -->  Разбор аргументов  -->  Вызов process_all_campaigns или main_process
```

**Примеры**:

Запуск скрипта для обработки конкретной кампании с указанием категорий, языка и валюты:

```bash
python src/suppliers/aliexpress/campaigns/prepare_campaigns.py summer_sale -c electronics -l EN -cu USD
```

Запуск скрипта для обработки всех кампаний с указанием языка и валюты:

```bash
python src/suppliers/aliexpress/campaigns/prepare_campaigns.py --all -l EN -cu USD