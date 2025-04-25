# Модуль для редактирования рекламных кампаний AliExpress

## Обзор

Модуль `edit_campaign.py` предназначен для редактирования рекламных кампаний на AliExpress. Он предоставляет набор инструментов для управления параметрами кампаний, включая выбор языка, валюты и других опций.

## Подробней

Данный модуль используется в контексте проекта `hypotez` для автоматизации процесса управления рекламными кампаниями на AliExpress. Он позволяет модифицировать настройки кампаний в соответствии с заданными требованиями, такими как язык, валюта, и другие параметры.

## Функции

### `process_campaign`

**Назначение**: Обработка рекламной кампании.

**Параметры**: 
- `campaign_name` (str): Имя рекламной кампании.

**Возвращает**: 
- None

**Как работает**: 
- Функция `process_campaign`  выполняет серию действий, связанных с редактированием рекламной кампании. Она принимает имя кампании в качестве параметра и выполняет необходимые действия для ее модификации.

**Примеры**:
```python
process_campaign('example_campaign_name')
```

### `process_campaign_category`

**Назначение**: Обработка категории рекламной кампании.

**Параметры**: 
- `category_name` (str): Имя категории рекламной кампании.

**Возвращает**: 
- None

**Как работает**: 
- Функция `process_campaign_category` выполняет действия, связанные с обработкой категории рекламной кампании. Она принимает имя категории в качестве параметра и выполняет необходимые действия для ее модификации.

**Примеры**:
```python
process_campaign_category('example_category_name')
```

### `process_all_campaigns`

**Назначение**: Обработка всех рекламных кампаний.

**Параметры**: 
- None

**Возвращает**: 
- None

**Как работает**: 
- Функция `process_all_campaigns` выполняет действия, связанные с обработкой всех рекламных кампаний. Она проходит по списку кампаний и выполняет необходимые действия для их модификации.

**Примеры**:
```python
process_all_campaigns()
```

## Классы

### `AliCampaignEditor`

**Описание**: Класс `AliCampaignEditor` используется для редактирования рекламных кампаний AliExpress.

**Атрибуты**: 
- `campaign_name` (str): Имя рекламной кампании.
- `locale` (str): Язык рекламной кампании (например, 'EN', 'RU', 'HE').
- `currency` (str): Валюта рекламной кампании (например, 'USD', 'ILS').

**Методы**:
- `edit_campaign()`:  Метод для редактирования рекламной кампании.

**Принцип работы**: 
- Класс `AliCampaignEditor` предоставляет набор инструментов для изменения параметров рекламных кампаний. Он используется для редактирования различных аспектов кампании, таких как язык, валюта и другие настройки.

**Примеры**:
```python
# Создание объекта AliCampaignEditor
editor = AliCampaignEditor('example_campaign_name', 'EN', 'USD')
# Вызов метода edit_campaign для редактирования кампании
editor.edit_campaign()
```

## Параметры

- `campaign_name` (str): Имя рекламной кампании.
- `category_name` (str): Имя категории рекламной кампании.
- `locales` (dict): Словарь, хранящий соответствие между языком и валютой. 

## Примеры

```python
# Пример редактирования кампании
from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignEditor

# Создание объекта AliCampaignEditor
editor = AliCampaignEditor('example_campaign_name', 'EN', 'USD')
# Вызов метода edit_campaign для редактирования кампании
editor.edit_campaign()

# Пример обработки категории
from src.suppliers.suppliers_list.aliexpress.campaign import process_campaign_category

# Вызов функции process_campaign_category для обработки категории
process_campaign_category('example_category_name')

# Пример обработки всех кампаний
from src.suppliers.suppliers_list.aliexpress.campaign import process_all_campaigns

# Вызов функции process_all_campaigns для обработки всех кампаний
process_all_campaigns()
```