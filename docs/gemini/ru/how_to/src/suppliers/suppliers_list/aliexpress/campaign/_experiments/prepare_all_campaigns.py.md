## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода запускает все рекламные кампании для всех языков с поиском названий категорий из директорий. Он использует функции `process_all_campaigns` и `main_process` из модуля `src.suppliers.suppliers_list.aliexpress.campaign.prepare_campaigns` для обработки кампаний и поиска названий категорий.

Шаги выполнения
-------------------------
1. **Импорт модулей**: Импортируется модуль `header` и функции `process_all_campaigns` и `main_process` из модуля `src.suppliers.suppliers_list.aliexpress.campaign.prepare_campaigns`.
2. **Инициализация переменных**: Задаются переменные для хранения информации о кампании (имя, язык, валюта).
3. **Запуск процесса обработки кампании**: Вызывается функция `process_campaign` с параметрами, заданными в переменных.
4. **Запуск поиска названий категорий**: Вызывается функция `main_process` с параметрами, заданными в переменных.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.campaign.prepare_campaigns import process_all_campaigns, main_process

# Инициализация переменных
campaign_name:str = 'rc'
language: str = 'EN'
currency: str = 'USD'
campaign_file:str = None

# Запуск процесса обработки кампании
process_campaign(campaign_name=campaign_name, language=language, currency=currency, campaign_file=campaign_file)

# Запуск поиска названий категорий
main_process('brands', ['mrgreen'])
```