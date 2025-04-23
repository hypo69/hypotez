# Модуль для подготовки новой рекламной кампании AliExpress
## Обзор

Модуль содержит скрипт для подготовки и запуска новой рекламной кампании на платформе AliExpress. Он использует класс `AliCampaignEditor` для обработки и настройки параметров кампании.

## Подробнее

Этот модуль предназначен для автоматизации процесса создания и настройки рекламных кампаний на AliExpress. Он выполняет такие задачи, как:

-   Инициализация редактора кампании.
-   Обработка новой кампании с заданным именем.

Модуль использует другие модули и классы из проекта `hypotez`, такие как:
-   `AliCampaignEditor` из `src.suppliers.suppliers_list.aliexpress.campaign` для редактирования кампании.
-   `get_filenames` и `get_directory_names` из `src.utils` для получения списка файлов и директорий.
-   `pprint` из `src.utils.printer` для форматированного вывода в консоль.
-   `logger` из `src.logger.logger` для логирования событий и ошибок.

## Классы

### `AliCampaignEditor`

**Описание**: Класс для редактирования и управления рекламными кампаниями AliExpress.

**Атрибуты**:

-   `campaign_name` (str): Имя рекламной кампании.

**Методы**:

-   `process_new_campaign(campaign_name)`: Метод для обработки и настройки новой рекламной кампании.

## Переменные

-   `campaign_name` (str): Имя рекламной кампании, которое будет использоваться в скрипте. По умолчанию установлено значение `'rc'`.
-   `aliexpress_editor` (AliCampaignEditor): Инстанс класса `AliCampaignEditor`, используемый для обработки и настройки рекламной кампании.

## Функции

В данном коде нет явно определенных функций, но используются методы класса `AliCampaignEditor`.

### `AliCampaignEditor.process_new_campaign(campaign_name: str)`

**Назначение**: Обработка и настройка новой рекламной кампании.

**Параметры**:

-   `campaign_name` (str): Имя рекламной кампании, которую необходимо обработать.

**Возвращает**:

-   `None`: Функция ничего не возвращает явно.

**Как работает функция**:

1.  Вызывается метод `process_new_campaign` у экземпляра класса `AliCampaignEditor`, который выполняет всю логику по подготовке и настройке новой рекламной кампании с заданным именем.

**Примеры**:

```python
from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignEditor

campaign_name = 'test_campaign'
aliexpress_editor = AliCampaignEditor(campaign_name)
aliexpress_editor.process_new_campaign(campaign_name)
```
В данном примере создается экземпляр класса `AliCampaignEditor` с именем кампании `'test_campaign'`, после чего вызывается метод `process_new_campaign` для обработки и настройки этой кампании.