# Модуль подготовки всех кампаний AliExpress

## Обзор

Модуль `prepare_all_campaigns.py` предназначен для подготовки и обработки всех рекламных кампаний на AliExpress. Он импортирует и запускает функцию `process_all_campaigns` из модуля `src.suppliers.suppliers_list.aliexpress.campaign`, которая выполняет основную логику обработки. Если рекламной кампании не существует, будет создана новая.

## Подробней

Этот модуль служит входной точкой для процесса подготовки всех рекламных кампаний AliExpress. Он обеспечивает запуск основной логики, содержащейся в модуле `process_all_campaigns`.

## Функции

### `process_all_campaigns()`

**Назначение**: Запускает процесс обработки всех рекламных кампаний AliExpress.

**Параметры**:
- Нет.

**Возвращает**:
- Нет.

**Вызывает исключения**:
- Могут возникать исключения в процессе выполнения, которые обрабатываются внутри функции `process_all_campaigns`.

**Как работает функция**:
- Функция `process_all_campaigns()` выполняет основную логику по обработке и подготовке рекламных кампаний AliExpress. Если какая-либо кампания не существует, она будет создана.

**Примеры**:

```python
from src.suppliers.suppliers_list.aliexpress.campaign import process_all_campaigns

process_all_campaigns()
```
```python
import src.suppliers.suppliers_list.aliexpress.campaign as campaign_module

campaign_module.process_all_campaigns()