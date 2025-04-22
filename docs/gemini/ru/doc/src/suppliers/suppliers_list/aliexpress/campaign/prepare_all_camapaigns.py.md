# Модуль подготовки рекламных кампаний AliExpress

## Обзор

Модуль `prepare_all_camapaigns.py` предназначен для подготовки и обработки всех рекламных кампаний AliExpress. Он вызывает функцию `process_all_campaigns` из модуля `src.suppliers.suppliers_list.aliexpress.campaign` для выполнения основной работы.

## Подробнее

Этот модуль служит точкой входа для запуска процесса подготовки рекламных кампаний. Он импортирует необходимые модули и затем вызывает функцию, которая выполняет всю необходимую логику для обработки кампаний.

## Функции

### `process_all_campaigns`

**Назначение**: Функция вызывает функцию `process_all_campaigns` из модуля `src.suppliers.suppliers_list.aliexpress.campaign`.

```python
from src.suppliers.suppliers_list.aliexpress.campaign import process_all_campaigns
process_all_campaigns()
```

**Как работает функция**:

- Импортирует модуль `header` (хотя он не используется в представленном коде).
- Импортирует функцию `process_all_campaigns` из модуля `src.suppliers.suppliers_list.aliexpress.campaign`.
- Вызывает функцию `process_all_campaigns` для запуска процесса обработки рекламных кампаний.

**Примеры**:

```python
# Пример вызова функции process_all_campaigns
process_all_campaigns()