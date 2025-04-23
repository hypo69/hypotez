# Модуль для быстрой работы с Google Sheets для AliExpress кампаний

## Обзор

Этот модуль предназначен для ускорения работы с Google Sheets в контексте управления рекламными кампаниями на AliExpress. Он предоставляет функциональность для чтения и сохранения данных кампаний и категорий товаров из Google Sheets.

## Подробнее

Модуль предоставляет класс `AliCampaignGoogleSheet`, который упрощает взаимодействие с Google Sheets, используемыми для хранения информации о рекламных кампаниях и категориях товаров на AliExpress. Он позволяет устанавливать рабочий лист с продуктами, сохранять категории и информацию о кампании из этого листа.

## Классы

### `AliCampaignGoogleSheet`

**Описание**: Класс для работы с Google Sheets, содержащими информацию о рекламных кампаниях AliExpress.

**Наследует**:
- Отсутствует явное наследование в предоставленном коде.

**Атрибуты**:
- `campaign_name` (str): Название рекламной кампании.
- `language` (str): Язык кампании.
- `currency` (str): Валюта кампании.

**Методы**:
- `set_products_worksheet(category_name)`: Устанавливает рабочий лист для определенной категории товаров.
- `save_categories_from_worksheet(save)`: Сохраняет категории из рабочего листа (не реализовано в предоставленном коде).
- `save_campaign_from_worksheet()`: Сохраняет информацию о кампании из рабочего листа.

## Функции

### `AliCampaignGoogleSheet.__init__`

```python
def __init__(campaign_name: str, language: str, currency: str) -> None:
    """
    Инициализирует объект AliCampaignGoogleSheet с указанным именем кампании, языком и валютой.

    Args:
        campaign_name (str): Название рекламной кампании.
        language (str): Язык кампании.
        currency (str): Валюта кампании.

    Returns:
        None

    Raises:
        Отсутствуют явные исключения.

    Как работает функция:
        - Функция инициализирует объект класса `AliCampaignGoogleSheet`, сохраняя переданные значения имени кампании, языка и валюты в атрибуты экземпляра класса.
    """
```

### `AliCampaignGoogleSheet.set_products_worksheet`

```python
def set_products_worksheet(category_name: str) -> None:
    """
    Устанавливает рабочий лист (worksheet) для продуктов указанной категории.

    Args:
        category_name (str): Название категории товаров.

    Returns:
        None

    Raises:
        Отсутствуют явные исключения.

     Как работает функция:
        - Устанавливает активный рабочий лист в Google Sheets для заданной категории товаров. Это подготавливает класс для дальнейшей работы с данными товаров из этого листа, например, для сохранения или обновления информации о товарах.
    """
```

### `AliCampaignGoogleSheet.save_categories_from_worksheet`

```python
def save_categories_from_worksheet(save: bool) -> None:
    """
    Сохраняет категории товаров из текущего рабочего листа. (Функциональность не реализована).

    Args:
        save (bool): Флаг, указывающий, нужно ли сохранять категории.

    Returns:
        None

    Raises:
        Отсутствуют явные исключения.

     Как работает функция:
        - Функция предназначена для сохранения категорий товаров из Google Sheets. Однако, в предоставленном коде реализация этой функции отсутствует.
    """
```

### `AliCampaignGoogleSheet.save_campaign_from_worksheet`

```python
def save_campaign_from_worksheet() -> None:
    """
    Сохраняет информацию о рекламной кампании из текущего рабочего листа.

    Args:
        Отсутствуют.

    Returns:
        None

    Raises:
        Отсутствуют явные исключения.

     Как работает функция:
        - Функция отвечает за сохранение информации о рекламной кампании, извлеченной из Google Sheets. В коде не указана конкретная реализация, но предполагается, что функция считывает данные из текущего активного листа и сохраняет их в соответствующем формате для дальнейшего использования.
    """
```

## Переменные

- `campaign_name` (str): Название рекламной кампании ("lighting").
- `category_name` (str): Название категории товаров ("chandeliers").
- `language` (str): Язык кампании ('EN').
- `currency` (str): Валюта кампании ('USD').
- `gs` (AliCampaignGoogleSheet): Экземпляр класса AliCampaignGoogleSheet, используемый для работы с Google Sheets.

## Примеры

```python
campaign_name = "lighting"
category_name = "chandeliers"
language = 'EN'
currency = 'USD'

gs = AliCampaignGoogleSheet(campaign_name=campaign_name, language=language, currency=currency)

gs.set_products_worksheet(category_name)
# gs.save_categories_from_worksheet(False)
gs.save_campaign_from_worksheet()
...