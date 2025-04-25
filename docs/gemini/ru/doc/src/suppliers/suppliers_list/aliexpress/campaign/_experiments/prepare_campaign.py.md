# Модуль `prepare_campaign.py`

## Обзор

Модуль `prepare_campaign.py` проверяет наличие рекламной кампании. Если текой рекламной кампании не существует - будет создана новая.  

## Подробнее

Модуль использует функцию `process_campaign` из модуля `src.suppliers.suppliers_list.aliexpress.campaign` для создания или обновления рекламной кампании на AliExpress. Он определяет словарь `locales` с  соответствиями языков и валют, а также устанавливает язык `language` и валюту `currency`. 

Модуль также определяет название кампании `campaign_name`. 

## Функции

### `process_campaign`

**Назначение**: Функция `process_campaign`  создает или обновляет рекламную кампанию на AliExpress.

**Параметры**:

- `campaign_name` (str): Название рекламной кампании. 
- `language` (str): Язык рекламной кампании. По умолчанию `EN`.
- `currency` (str): Валюта рекламной кампании. По умолчанию `USD`.
- `campaign_file` (str): Файл с описанием кампании.

**Возвращает**: 

- `None`: Возвращает `None`.

**Вызывает исключения**: 

- `Exception`:  Возникает исключение, если возникла ошибка при создании или обновлении кампании. 

**Примеры**:

```python
# Создание новой кампании
process_campaign(campaign_name='brands', language='EN', currency='USD', campaign_file='campaign.json')

# Обновление существующей кампании
process_campaign(campaign_name='brands', language='EN', currency='USD', campaign_file='campaign.json')
```