# Модуль тестирования подготовки кампаний AliExpress

## Обзор

Модуль содержит набор тестов pytest для проверки функциональности подготовки кампаний AliExpress, включая обновление категорий, обработку кампаний по категориям, обработку кампаний в целом и основную функцию запуска процесса. Модуль использует mock-объекты для изоляции тестируемых функций и проверки их взаимодействия с другими компонентами системы.

## Подробней

Этот модуль выполняет модульное тестирование функций, отвечающих за подготовку данных для рекламных кампаний на AliExpress. Он включает в себя тесты для успешных и неудачных сценариев, обеспечивая надежность работы основных компонентов, таких как обновление информации о категориях и обработка товаров в категориях.

## Классы

В данном модуле классы отсутствуют. Вместо этого используются pytest-фикстуры для предоставления mock-объектов и управления тестовой средой.

## Функции

### `test_update_category_success`

**Назначение**: Проверяет успешное обновление категории.

**Параметры**:

-   `mock_j_loads`: Mock функция для имитации загрузки JSON.
-   `mock_j_dumps`: Mock функция для имитации сохранения JSON.
-   `mock_logger`: Mock объект логгера.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Определяет mock-путь к JSON-файлу и mock-категорию.
2.  Устанавливает возвращаемое значение `mock_j_loads` в виде словаря с категорией.
3.  Вызывает функцию `update_category` с mock-путем и mock-категорией.
4.  Проверяет, что функция вернула `True`.
5.  Проверяет, что `mock_j_dumps` была вызвана с ожидаемыми аргументами.
6.  Проверяет, что `mock_logger.error` не был вызван.

**Примеры**:

```python
# Пример вызова функции test_update_category_success с mock-объектами
test_update_category_success(mock_j_loads, mock_j_dumps, mock_logger)
```

### `test_update_category_failure`

**Назначение**: Проверяет сценарий неудачного обновления категории.

**Параметры**:

-   `mock_j_loads`: Mock функция для имитации загрузки JSON.
-   `mock_j_dumps`: Mock функция для имитации сохранения JSON.
-   `mock_logger`: Mock объект логгера.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Определяет mock-путь к JSON-файлу и mock-категорию.
2.  Устанавливает `side_effect` для `mock_j_loads`, чтобы вызвать исключение.
3.  Вызывает функцию `update_category` с mock-путем и mock-категорией.
4.  Проверяет, что функция вернула `False`.
5.  Проверяет, что `mock_j_dumps` не была вызвана.
6.  Проверяет, что `mock_logger.error` был вызван один раз.

**Примеры**:

```python
# Пример вызова функции test_update_category_failure с mock-объектами
test_update_category_failure(mock_j_loads, mock_j_dumps, mock_logger)
```

### `test_process_campaign_category_success`

**Назначение**: Проверяет успешную обработку категории кампании.

**Параметры**:

-   `mock_ali_promo_campaign`: Mock класс для имитации `AliPromoCampaign`.
-   `mock_logger`: Mock объект логгера.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Определяет mock-название кампании, категории, языка и валюты.
2.  Получает mock-объект `mock_ali_promo` через `mock_ali_promo_campaign.return_value`.
3.  Устанавливает `MagicMock` для `mock_ali_promo.process_affiliate_products`.
4.  Вызывает асинхронную функцию `process_campaign_category` с mock-параметрами.
5.  Проверяет, что результат не `None`.
6.  Проверяет, что `mock_logger.error` не был вызван.

**Примеры**:

```python
# Пример вызова функции test_process_campaign_category_success с mock-объектами
await test_process_campaign_category_success(mock_ali_promo_campaign, mock_logger)
```

### `test_process_campaign_category_failure`

**Назначение**: Проверяет сценарий неудачной обработки категории кампании.

**Параметры**:

-   `mock_ali_promo_campaign`: Mock класс для имитации `AliPromoCampaign`.
-   `mock_logger`: Mock объект логгера.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Определяет mock-название кампании, категории, языка и валюты.
2.  Получает mock-объект `mock_ali_promo` через `mock_ali_promo_campaign.return_value`.
3.  Устанавливает `side_effect` для `mock_ali_promo.process_affiliate_products`, чтобы вызвать исключение.
4.  Вызывает асинхронную функцию `process_campaign_category` с mock-параметрами.
5.  Проверяет, что результат равен `None`.
6.  Проверяет, что `mock_logger.error` был вызван один раз.

**Примеры**:

```python
# Пример вызова функции test_process_campaign_category_failure с mock-объектами
await test_process_campaign_category_failure(mock_ali_promo_campaign, mock_logger)
```

### `test_process_campaign`

**Назначение**: Проверяет обработку кампании.

**Параметры**:

-   `mock_get_directory_names`: Mock функция для имитации получения списка категорий.
-   `mock_logger`: Mock объект логгера.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Определяет mock-название кампании, список категорий, язык, валюту и флаг `force`.
2.  Устанавливает возвращаемое значение `mock_get_directory_names` в виде списка категорий.
3.  Вызывает функцию `process_campaign` с mock-параметрами.
4.  Проверяет, что длина списка результатов равна 2.
5.  Проверяет, что каждая категория присутствует в списке mock-категорий и что результат для каждой категории не `None`.
6.  Проверяет, что `mock_logger.warning` не был вызван.

**Примеры**:

```python
# Пример вызова функции test_process_campaign с mock-объектами
test_process_campaign(mock_get_directory_names, mock_logger)
```

### `test_main`

**Назначение**: Проверяет основную функцию `main`.

**Параметры**:

-   `mock_get_directory_names`: Mock функция для имитации получения списка категорий.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Определяет mock-название кампании, список категорий, язык, валюту и флаг `force`.
2.  Устанавливает возвращаемое значение `mock_get_directory_names` в виде списка категорий.
3.  Вызывает асинхронную функцию `main` с mock-параметрами.
4.  Проверяет, что `mock_get_directory_names` была вызвана один раз.

**Примеры**:

```python
# Пример вызова функции test_main с mock-объектами
await test_main(mock_get_directory_names)
```

## Pytest фикстуры

### `mock_j_loads`

**Назначение**: Создает mock для функции `j_loads` из модуля `src.utils.jjson`.

**Как работает фикстура**:

Использует `patch` для замены `src.utils.jjson.j_loads` mock-объектом.

### `mock_j_dumps`

**Назначение**: Создает mock для функции `j_dumps` из модуля `src.utils.jjson`.

**Как работает фикстура**:

Использует `patch` для замены `src.utils.jjson.j_dumps` mock-объектом.

### `mock_logger`

**Назначение**: Создает mock для объекта `logger` из модуля `src.logger`.

**Как работает фикстура**:

Использует `patch` для замены `src.logger.logger` mock-объектом.

### `mock_get_directory_names`

**Назначение**: Создает mock для функции `get_directory_names` из модуля `src.utils`.

**Как работает фикстура**:

Использует `patch` для замены `src.utils.get_directory_names` mock-объектом.

### `mock_ali_promo_campaign`

**Назначение**: Создает mock для класса `AliPromoCampaign` из модуля `src.suppliers.suppliers_list.aliexpress.campaign`.

**Как работает фикстура**:

Использует `patch` для замены `src.suppliers.suppliers_list.aliexpress.campaign.AliPromoCampaign` mock-объектом.