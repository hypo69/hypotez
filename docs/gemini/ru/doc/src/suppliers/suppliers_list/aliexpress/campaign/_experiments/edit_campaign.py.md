# Модуль для редактирования рекламной кампании на AliExpress

## Обзор

Модуль предназначен для редактирования рекламных кампаний на платформе AliExpress. Он предоставляет функциональность для управления кампаниями, категориями кампаний и обработки данных, связанных с рекламными кампаниями.

## Подробнее

Модуль `edit_campaign.py` является частью проекта `hypotez` и предназначен для автоматизации процесса редактирования рекламных кампаний на AliExpress. Он использует другие модули проекта, такие как `AliCampaignEditor`, `process_campaign`, `process_campaign_category` и `process_all_campaigns`, чтобы обеспечить полный цикл управления рекламными кампаниями.

## Классы

В данном модуле нет классов.

## Функции

В данном модуле нет функций. Он использует функции из других модулей.

## Переменные

- `locales (dict)`: Словарь, содержащий соответствия между локалями (`EN`, `HE`, `RU`) и валютами (`USD`, `ILS`).
- `campaign_name (str)`: Имя рекламной кампании, с которой необходимо работать. В данном случае `"building_bricks"`.
- `category_name (str)`: Имя категории рекламной кампании. В данном случае `"building_bricks"`.
- `a (AliCampaignEditor)`: Объект класса `AliCampaignEditor`, предназначенный для редактирования рекламной кампании. Инициализируется с именем кампании, локалью и валютой.

```python
a = AliCampaignEditor(campaign_name,'EN','USD')
```

## Подключаемые модули
- `header`: <описание модуля header>
- `pathlib.Path`: <описание модуля pathlib>
- `src.gs`: <описание модуля gs>
- `src.suppliers.suppliers_list.aliexpress.campaign.AliCampaignEditor`: <описание модуля AliCampaignEditor>
- `src.suppliers.suppliers_list.aliexpress.campaign.process_campaign`: <описание модуля process_campaign>
- `src.suppliers.suppliers_list.aliexpress.campaign.process_campaign_category`: <описание модуля process_campaign_category>
- `src.suppliers.suppliers_list.aliexpress.campaign.process_all_campaigns`: <описание модуля process_all_campaigns>
- `src.utils.get_filenames`: <описание модуля get_filenames>
- `src.utils.get_directory_names`: <описание модуля get_directory_names>
- `src.utils.printer.pprint`: <описание модуля pprint>