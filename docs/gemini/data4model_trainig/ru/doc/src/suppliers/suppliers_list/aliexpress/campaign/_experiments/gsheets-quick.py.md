# Модуль для работы с Google Sheets в кампаниях AliExpress (Быстрая версия)

## Обзор

Модуль `gsheets-quick.py` предназначен для быстрой работы с Google Sheets в контексте управления кампаниями AliExpress. Он автоматизирует чтение данных из Google Sheets и сохранение их для использования в кампаниях, фокусируясь на скорости и простоте использования.

## Подробней

Модуль предоставляет инструменты для извлечения данных о категориях и кампаниях из Google Sheets и сохранения их для дальнейшего использования. Он использует классы и функции из других модулей проекта `hypotez`, таких как `AliCampaignGoogleSheet`, `CampaignType`, `CategoryType` и `ProductType`, чтобы структурировать и обрабатывать данные.

## Классы

В данном коде классы не определены. Используются классы из других модулей.

## Функции

В данном коде функции не определены. Код выполняет последовательность действий по настройке и сохранению данных из Google Sheets.

## Параметры модуля

- `campaign_name` (str): Имя кампании AliExpress. В данном случае `"lighting"`.
- `category_name` (str): Имя категории товара. В данном случае `"chandeliers"`.
- `language` (str): Язык, используемый в кампании. В данном случае `'EN'`.
- `currency` (str): Валюта, используемая в кампании. В данном случае `'USD'`.
- `gs` (AliCampaignGoogleSheet): Объект класса `AliCampaignGoogleSheet`, используемый для взаимодействия с Google Sheets.

## Основные этапы работы

1.  **Инициализация параметров**:
    -   Определяются основные параметры кампании, такие как имя, категория, язык и валюта.

2.  **Создание экземпляра `AliCampaignGoogleSheet`**:
    -   Создается объект `gs` класса `AliCampaignGoogleSheet` с указанием параметров кампании.
    -   `gs = AliCampaignGoogleSheet(campaign_name=campaign_name, language=language, currency=currency)`

3.  **Настройка и сохранение данных**:
    -   Вызываются методы объекта `gs` для настройки и сохранения данных из Google Sheets.
    -   `gs.set_products_worksheet(category_name)`: Устанавливает рабочий лист продуктов.
    -   `gs.save_campaign_from_worksheet()`: Сохраняет данные кампании.

## Примеры использования

Пример использования для настройки и сохранения данных кампании AliExpress из Google Sheets:

```python
campaign_name = "lighting"
category_name = "chandeliers"
language = 'EN'
currency = 'USD'

gs = AliCampaignGoogleSheet(campaign_name=campaign_name, language=language, currency=currency)

gs.set_products_worksheet(category_name)
gs.save_campaign_from_worksheet()
...