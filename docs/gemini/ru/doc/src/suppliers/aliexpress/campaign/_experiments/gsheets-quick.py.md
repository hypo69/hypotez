# Модуль gsheets-quick.py

## Обзор

Модуль предназначен для быстрой работы с Google Sheets в контексте рекламных кампаний AliExpress. Он позволяет устанавливать рабочие листы продуктов, сохранять категории и кампании из этих листов.

## Подробней

Этот файл представляет собой эксперимент или скрипт для быстрого запуска задач, связанных с Google Sheets и рекламными кампаниями AliExpress. В коде задаются имя кампании, категория, язык и валюта, а затем создается экземпляр класса `AliCampaignGoogleSheet` для работы с таблицей. Основные функции, выполняемые скриптом, включают установку рабочего листа продуктов, сохранение категорий и сохранение кампании из рабочего листа.

## Классы

### `AliCampaignGoogleSheet`

**Описание**: Класс для работы с Google Sheets, связанными с рекламными кампаниями AliExpress.

**Наследует**:
Не указано.

**Атрибуты**:
- `campaign_name` (str): Имя кампании.
- `language` (str): Язык кампании.
- `currency` (str): Валюта кампании.

**Методы**:
- `set_products_worksheet(category_name)`: Устанавливает рабочий лист продуктов для указанной категории.
- `save_categories_from_worksheet(force)`: Сохраняет категории из рабочего листа.
- `save_campaign_from_worksheet()`: Сохраняет кампанию из рабочего листа.

**Принцип работы**:
Класс `AliCampaignGoogleSheet` инкапсулирует логику взаимодействия с Google Sheets для управления данными рекламных кампаний AliExpress. Он предоставляет методы для установки рабочих листов продуктов, сохранения категорий и сохранения кампаний.

## Методы класса

### `set_products_worksheet`

```python
def set_products_worksheet(category_name):
    """Устанавливает рабочий лист продуктов для указанной категории.

    Args:
        category_name (str): Имя категории.

    Returns:
        None

    Raises:
        None

    """
    ...
```

### `save_categories_from_worksheet`

```python
def save_categories_from_worksheet(force):
    """Сохраняет категории из рабочего листа.

    Args:
        force (bool): Флаг, указывающий на необходимость принудительного сохранения.

    Returns:
        None

    Raises:
        None

    """
    ...
```

### `save_campaign_from_worksheet`

```python
def save_campaign_from_worksheet():
    """Сохраняет кампанию из рабочего листа.

    Args:
        None

    Returns:
        None

    Raises:
        None

    """
    ...
```

## Параметры класса

- `campaign_name` (str): Имя кампании, используемое для идентификации кампании в Google Sheets.
- `language` (str): Язык кампании, например, 'EN' для английского.
- `currency` (str): Валюта кампании, например, 'USD' для долларов США.
- `category_name` (str): Имя категории продуктов, для которой устанавливается рабочий лист.
- `force` (bool): Флаг, определяющий, следует ли принудительно сохранять категории из рабочего листа.

**Примеры**:

```python
campaign_name = "lighting"
category_name = "chandeliers"
language = 'EN'
currency = 'USD'

gs = AliCampaignGoogleSheet(campaign_name=campaign_name, language=language, currency=currency)

gs.set_products_worksheet(category_name)
# gs.save_categories_from_worksheet(False)
gs.save_campaign_from_worksheet()