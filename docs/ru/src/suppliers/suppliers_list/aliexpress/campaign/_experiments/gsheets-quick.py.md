# Модуль для быстрой работы с Google Sheets в кампаниях AliExpress

## Обзор

Модуль предназначен для упрощения и ускорения работы с Google Sheets при управлении кампаниями AliExpress. Он предоставляет функциональность для настройки рабочих листов продуктов, сохранения категорий и кампаний из рабочих листов.

## Подробней

Этот модуль является частью экспериментов по автоматизации работы с Google Sheets в контексте кампаний AliExpress. Он использует классы и функции из других модулей проекта, таких как `AliCampaignGoogleSheet`, `CampaignType`, `CategoryType` и `ProductType`, для организации данных и взаимодействия с Google Sheets.
Расположение файла в проекте: `hypotez/src/suppliers/suppliers_list/aliexpress/campaign/_experiments/gsheets-quick.py` указывает на то, что он предназначен для экспериментов, связанных с кампаниями AliExpress.

## Классы

В данном коде классы отсутствуют.

## Функции

В данном коде функции отсутствуют.

## Переменные

- `campaign_name (str)`: Имя кампании (`"lighting"`).
- `category_name (str)`: Имя категории (`"chandeliers"`).
- `language (str)`: Язык (`"EN"`).
- `currency (str)`: Валюта (`"USD"`).
- `gs (AliCampaignGoogleSheet)`: Объект класса `AliCampaignGoogleSheet`, используемый для работы с Google Sheets. Инициализируется с указанными именем кампании, языком и валютой.

## Принцип работы

1.  **Инициализация переменных**:
    *   Определяются имя кампании, имя категории, язык и валюта.
2.  **Создание объекта `AliCampaignGoogleSheet`**:
    *   Создается экземпляр класса `AliCampaignGoogleSheet` с использованием определенных выше переменных.
3.  **Настройка рабочего листа продуктов**:
    *   Вызывается метод `set_products_worksheet` для настройки рабочего листа продуктов на основе имени категории.
4.  **Сохранение кампании из рабочего листа**:
    *   Вызывается метод `save_campaign_from_worksheet` для сохранения данных кампании из рабочего листа.

## Методы класса

В данном коде методы класса отсутствуют.

## Примеры

Пример использования:

```python
campaign_name = "lighting"
category_name = "chandeliers"
language = 'EN'
currency = 'USD'

gs = AliCampaignGoogleSheet(campaign_name=campaign_name, language=language, currency=currency)

gs.set_products_worksheet(category_name)
gs.save_campaign_from_worksheet()
...
```