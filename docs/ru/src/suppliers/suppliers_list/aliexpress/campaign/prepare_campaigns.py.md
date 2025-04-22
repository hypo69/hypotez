# Модуль подготовки кампаний AliExpress

## Обзор

Модуль `prepare_campaigns.py` предназначен для подготовки рекламных кампаний на AliExpress. Он включает в себя обработку категорий, управление данными кампаний и генерацию рекламных материалов. Модуль позволяет обрабатывать как отдельные кампании, так и все кампании в указанной директории.

## Подробнее

Этот модуль является частью проекта `hypotez` и отвечает за автоматизацию процесса подготовки рекламных кампаний для AliExpress. Он использует другие модули проекта, такие как `AliCampaignEditor`, `locales`, `j_loads_ns` и `logger`, для выполнения своих задач.
Модуль принимает аргументы командной строки, такие как название кампании, список категорий, язык и валюта, и на основе этих аргументов запускает процесс подготовки кампании.

## Классы

В данном модуле классы отсутствуют.

## Функции

### `process_campaign_category`

**Назначение**: Обрабатывает определенную категорию в рамках кампании для заданного языка и валюты.

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
    return AliCampaignEditor(
        campaign_name=campaign_name, language=language, currency=currency
    ).process_campaign_category(category_name)
```

**Параметры**:

-   `campaign_name` (str): Название рекламной кампании.
-   `category_name` (str): Категория для кампании.
-   `language` (str): Язык для кампании.
-   `currency` (str): Валюта для кампании.

**Возвращает**:

-   `List[str]`: Список наименований товаров в рамках категории.

**Как работает функция**:

Функция создает экземпляр класса `AliCampaignEditor` с переданными параметрами и вызывает метод `process_campaign_category` этого экземпляра, передавая название категории. Результат работы этого метода возвращается как результат работы функции `process_campaign_category`.
Функция отвечает за обработку конкретной категории в рамках заданной рекламной кампании для определенного языка и валюты. Она использует класс `AliCampaignEditor` для выполнения этой задачи.

**Примеры**:

```python
titles: List[str] = process_campaign_category("summer_sale", "electronics", "EN", "USD")
print(titles)
# Результат: ['Product 1', 'Product 2'] (пример)
```

### `process_campaign`

**Назначение**: Обрабатывает кампанию, настраивает и обрабатывает ее.

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
    # Преобразуем список словарей в список пар (language, currency)
    _l = [(lang, curr) for locale in locales for lang, curr in locale.items()]
    # pprint(_l)

    # Если указаны язык и валюта, фильтруем список по ним
    if language and currency:
        _l = [(language, currency)]

    # Обрабатываем каждую пару (language, currency)
    for language, currency in _l:
        logger.info(f"Processing campaign: {campaign_name=}, {language=}, {currency=}")
        editor = AliCampaignEditor(
            campaign_name=campaign_name,
            language=language,
            currency=currency,
        )

        editor.process_campaign()

    return True  # Предполагаем, что кампания всегда успешно обрабатывается
```

**Параметры**:

-   `campaign_name` (str): Название рекламной кампании.
-   `language` (Optional[str]): Язык для кампании. Если не указан, обрабатываются все локали.
-   `currency` (Optional[str]): Валюта для кампании. Если не указана, обрабатываются все локали.
-   `campaign_file` (Optional[str]): Необязательный путь к конкретному файлу кампании.

**Возвращает**:

-   `bool`: `True`, если кампания обработана, иначе `False`.

**Как работает функция**:

Функция `process_campaign` выполняет следующие действия:

1.  Определяет список локалей (`_l`) для обработки. Если указаны язык и валюта, список содержит только их. В противном случае, он генерируется на основе всех доступных локалей из модуля `locales`.
2.  Для каждой локали (языка и валюты) создается экземпляр класса `AliCampaignEditor` с указанным названием кампании, языком и валютой.
3.  Вызывается метод `process_campaign` для созданного экземпляра `AliCampaignEditor`, который выполняет основную обработку кампании.
4.  В конце функция возвращает `True`, предполагая, что кампания всегда обрабатывается успешно.

**Примеры**:

```python
res = process_campaign("summer_sale", "EN", "USD", "campaign_file.json")
# res будет True после успешной обработки
```

### `process_all_campaigns`

**Назначение**: Обрабатывает все кампании в директории `'campaigns'` для указанного языка и валюты.

```python
def process_all_campaigns(language: Optional[str] = None, currency: Optional[str] = None) -> None:
    """Processes all campaigns in the 'campaigns' directory for the specified language and currency.

    Args:
        language (Optional[str]): Language for the campaigns.
        currency (Optional[str]): Currency for the campaigns.

    Example:
        >>> process_all_campaigns("EN", "USD")
    """
    if not language and not currency:
        # Process all locales if language or currency is not provided
        _l = [(lang, curr) for locale in locales for lang, curr in locale.items()]
    else:
        _l = [(language, currency)]
    pprint(f"{_l=}")
    for lang, curr in _l:
        campaigns_dir = get_directory_names(campaigns_directory)
        pprint(f"{campaigns_dir=}")
        for campaign_name in campaigns_dir:
            logger.info(f"Start processing {campaign_name=}, {lang=}, {curr=}")
            editor = AliCampaignEditor(
                campaign_name=campaign_name,
                language=lang,
                currency=curr
            )
            editor.process_campaign()
```

**Параметры**:

-   `language` (Optional[str]): Язык для кампаний.
-   `currency` (Optional[str]): Валюта для кампаний.

**Как работает функция**:

Функция `process_all_campaigns` выполняет следующие действия:

1.  Определяет список локалей (`_l`) для обработки. Если `language` и `currency` не указаны, обрабатываются все локали из модуля `locales`. В противном случае, список содержит только указанные язык и валюту.
2.  Получает список названий директорий кампаний из директории `campaigns_directory` с помощью функции `get_directory_names`.
3.  Для каждой кампании в списке и для каждой локали создается экземпляр класса `AliCampaignEditor` с указанным названием кампании, языком и валютой.
4.  Вызывается метод `process_campaign` для созданного экземпляра `AliCampaignEditor`, который выполняет основную обработку кампании.

**Примеры**:

```python
process_all_campaigns("EN", "USD")
# Будут обработаны все кампании для английского языка и доллара США
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
    # Determine locales based on provided language and currency
    locales_to_process = [(language, currency)] if language and currency else [(lang, curr) for locale in locales for lang, curr in locale.items()]

    for lang, curr in locales_to_process:
        if categories:
            # Process each specified category
            for category in categories:
                logger.info(f"Processing specific category {category=}, {lang=}, {curr=}")
                process_campaign_category(campaign_name, category, lang, curr)
        else:
            # Process the entire campaign if no specific categories are provided
            logger.info(f"Processing entire campaign {campaign_name=}, {lang=}, {curr=}")
            process_campaign(campaign_name, lang, curr)
```

**Параметры**:

-   `campaign_name` (str): Название рекламной кампании.
-   `categories` (List[str] | str): Список категорий для кампании. Если пустой, обрабатывается вся кампания без указания конкретных категорий.
-   `language` (Optional[str]): Язык для кампании.
-   `currency` (Optional[str]): Валюта для кампании.

**Как работает функция**:

Функция `main_process` выполняет следующие действия:

1.  Определяет список локалей (`locales_to_process`) для обработки на основе предоставленных языка и валюты. Если язык и валюта указаны, список содержит только их. В противном случае, он генерируется на основе всех доступных локалей из модуля `locales`.
2.  Для каждой локали (языка и валюты) проверяется, указаны ли категории для обработки.
3.  Если категории указаны, функция перебирает их и вызывает функцию `process_campaign_category` для каждой категории.
4.  Если категории не указаны, функция вызывает функцию `process_campaign` для обработки всей кампании.

**Примеры**:

```python
main_process("summer_sale", ["electronics"], "EN", "USD")
# Будет обработана категория "electronics" кампании "summer_sale" для английского языка и доллара США

main_process("summer_sale", [], "EN", "USD")
# Будет обработана вся кампания "summer_sale" для английского языка и доллара США
```

### `main`

**Назначение**: Основная функция для разбора аргументов и инициации обработки.

```python
def main() -> None:
    """Main function to parse arguments and initiate processing.

    Example:
        >>> main()
    """
    parser = argparse.ArgumentParser(description="Prepare AliExpress Campaign")
    parser.add_argument("campaign_name", type=str, help="Name of the campaign")
    parser.add_argument(
        "-c",
        "--categories",
        nargs="+",
        help="List of categories (if not provided, all categories will be used)",
    )
    parser.add_argument(
        "-l", "--language", type=str, default=None, help="Language for the campaign"
    )
    parser.add_argument(
        "-cu", "--currency", type=str, default=None, help="Currency for the campaign"
    )
    parser.add_argument("--all", action="store_true", help="Process all campaigns")

    args = parser.parse_args()

    if args.all:
        process_all_campaigns(args.language, args.currency)
    else:
        main_process(
            args.campaign_name, args.categories or [], args.language, args.currency
        )
```

**Как работает функция**:

Функция `main` выполняет следующие действия:

1.  Инициализирует парсер аргументов командной строки с помощью `argparse.ArgumentParser`.
2.  Определяет аргументы, которые можно передать скрипту:
    -   `campaign_name`: Название кампании (обязательный аргумент).
    -   `-c`, `--categories`: Список категорий для обработки (необязательный аргумент).
    -   `-l`, `--language`: Язык для кампании (необязательный аргумент).
    -   `-cu`, `--currency`: Валюта для кампании (необязательный аргумент).
    -   `--all`: Флаг, указывающий на необходимость обработки всех кампаний (необязательный аргумент).
3.  Разбирает аргументы командной строки с помощью `parser.parse_args()`.
4.  Проверяет, установлен ли флаг `--all`.
5.  Если флаг установлен, вызывает функцию `process_all_campaigns` с указанными языком и валютой.
6.  Если флаг не установлен, вызывает функцию `main_process` с указанным названием кампании, списком категорий (или пустым списком, если категории не указаны), языком и валютой.

**Примеры**:

Запуск скрипта с аргументами:

```bash
python prepare_campaigns.py summer_sale -c electronics -l EN -cu USD
# Будет обработана категория "electronics" кампании "summer_sale" для английского языка и доллара США

python prepare_campaigns.py summer_sale -l EN -cu USD
# Будет обработана вся кампания "summer_sale" для английского языка и доллара США

python prepare_campaigns.py --all -l EN -cu USD
# Будут обработаны все кампании для английского языка и доллара США
```