# Модуль тестирования подготовки кампаний Aliexpress

## Обзор

Этот модуль содержит тестовые функции для модуля `src.suppliers.suppliers_list.aliexpress.campaign.prepare_campaigns`. 
Он проверяет функциональность функций, связанных с подготовкой кампаний AliExpress, таких как обновление категорий, обработка категорий кампаний и обработка кампаний. 

## Детали

Модуль использует библиотеку `pytest` для создания тестов. 
Он использует мокирование для изоляции тестируемого кода от зависимостей. 
Тесты проверяют различные сценарии, такие как успешное и неудачное обновление категорий, успешную и неудачную обработку категорий кампаний, обработку кампаний и запуск основного скрипта.

## Функции

### `test_update_category_success`

**Цель**: Проверить успешное обновление категории.

**Параметры**:
- `mock_j_loads`: Мокированный объект для `src.utils.jjson.j_loads`.
- `mock_j_dumps`: Мокированный объект для `src.utils.jjson.j_dumps`.
- `mock_logger`: Мокированный объект для `src.logger.logger`.

**Возвращает**: 
- `None`.

**Как работает**:
- Функция создает мокированный путь к файлу категории.
- Мокированный объект `mock_j_loads` возвращает мокированный словарь с данными категории.
- Функция вызывает функцию `update_category` с мокированными данными.
- Функция проверяет, что `update_category` возвращает `True`, 
что `mock_j_dumps` был вызван с правильными данными и что `mock_logger.error` не был вызван.

**Примеры**:
```python
>>> test_update_category_success(mock_j_loads, mock_j_dumps, mock_logger)
```

### `test_update_category_failure`

**Цель**: Проверить неудачное обновление категории.

**Параметры**:
- `mock_j_loads`: Мокированный объект для `src.utils.jjson.j_loads`.
- `mock_j_dumps`: Мокированный объект для `src.utils.jjson.j_dumps`.
- `mock_logger`: Мокированный объект для `src.logger.logger`.

**Возвращает**:
- `None`.

**Как работает**:
- Функция создает мокированный путь к файлу категории.
- Мокированный объект `mock_j_loads` генерирует исключение.
- Функция вызывает функцию `update_category` с мокированными данными.
- Функция проверяет, что `update_category` возвращает `False`, 
что `mock_j_dumps` не был вызван и что `mock_logger.error` был вызван.

**Примеры**:
```python
>>> test_update_category_failure(mock_j_loads, mock_j_dumps, mock_logger)
```

### `test_process_campaign_category_success`

**Цель**: Проверить успешную обработку категории кампании.

**Параметры**:
- `mock_ali_promo_campaign`: Мокированный объект для `src.suppliers.suppliers_list.aliexpress.campaign.AliPromoCampaign`.
- `mock_logger`: Мокированный объект для `src.logger.logger`.

**Возвращает**:
- `None`.

**Как работает**:
- Функция создает мокированные имена кампании, категории, языка и валюты.
- Мокированный объект `mock_ali_promo_campaign` возвращает мокированный объект `AliPromoCampaign`.
- Мокированный объект `AliPromoCampaign` имеет мокированный метод `process_affiliate_products`.
- Функция вызывает функцию `process_campaign_category` с мокированными данными.
- Функция проверяет, что `process_campaign_category` возвращает не `None`, 
что `mock_logger.error` не был вызван и что `mock_ali_promo_campaign` был вызван с правильными данными.

**Примеры**:
```python
>>> test_process_campaign_category_success(mock_ali_promo_campaign, mock_logger)
```

### `test_process_campaign_category_failure`

**Цель**: Проверить неудачную обработку категории кампании.

**Параметры**:
- `mock_ali_promo_campaign`: Мокированный объект для `src.suppliers.suppliers_list.aliexpress.campaign.AliPromoCampaign`.
- `mock_logger`: Мокированный объект для `src.logger.logger`.

**Возвращает**:
- `None`.

**Как работает**:
- Функция создает мокированные имена кампании, категории, языка и валюты.
- Мокированный объект `mock_ali_promo_campaign` возвращает мокированный объект `AliPromoCampaign`.
- Мокированный объект `AliPromoCampaign` имеет мокированный метод `process_affiliate_products`, 
который генерирует исключение.
- Функция вызывает функцию `process_campaign_category` с мокированными данными.
- Функция проверяет, что `process_campaign_category` возвращает `None`, 
что `mock_logger.error` был вызван и что `mock_ali_promo_campaign` был вызван с правильными данными.

**Примеры**:
```python
>>> test_process_campaign_category_failure(mock_ali_promo_campaign, mock_logger)
```

### `test_process_campaign`

**Цель**: Проверить обработку кампании.

**Параметры**:
- `mock_get_directory_names`: Мокированный объект для `src.utils.get_directory_names`.
- `mock_logger`: Мокированный объект для `src.logger.logger`.

**Возвращает**:
- `None`.

**Как работает**:
- Функция создает мокированные имена кампании, категории, языка, валюты и значения `force`.
- Мокированный объект `mock_get_directory_names` возвращает мокированный список категорий.
- Функция вызывает функцию `process_campaign` с мокированными данными.
- Функция проверяет, что длина результата равна количеству категорий, 
что каждый результат не `None` и что `mock_logger.warning` не был вызван.

**Примеры**:
```python
>>> test_process_campaign(mock_get_directory_names, mock_logger)
```

### `test_main`

**Цель**: Проверить запуск основного скрипта.

**Параметры**:
- `mock_get_directory_names`: Мокированный объект для `src.utils.get_directory_names`.

**Возвращает**:
- `None`.

**Как работает**:
- Функция создает мокированные имена кампании, категории, языка, валюты и значения `force`.
- Мокированный объект `mock_get_directory_names` возвращает мокированный список категорий.
- Функция вызывает функцию `main` с мокированными данными.
- Функция проверяет, что `mock_get_directory_names` был вызван один раз.

**Примеры**:
```python
>>> test_main(mock_get_directory_names)
```

## Заключение

Этот модуль тестов обеспечивает комплексное покрытие функциональности модуля `src.suppliers.suppliers_list.aliexpress.campaign.prepare_campaigns`, гарантируя, что код работает правильно. 
Он включает в себя различные тестовые сценарии, которые проверяют как успешные, так и неудачные случаи, а также работу основных функций и скрипта.