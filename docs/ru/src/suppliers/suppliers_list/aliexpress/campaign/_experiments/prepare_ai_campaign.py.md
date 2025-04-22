# Модуль для подготовки AI кампании

## Обзор

Модуль предназначен для подготовки и обработки рекламных кампаний на платформе AliExpress с использованием AI. Он включает в себя функциональность для чтения, обработки и редактирования данных кампаний.

## Подробней

Модуль предоставляет инструменты для автоматизации процесса создания и настройки рекламных кампаний, используя данные, полученные с помощью AI.

## Импортированные модули

- `header`: Неизвестный модуль (требуется дополнительная информация).
- `pathlib.Path`: Для работы с путями к файлам и директориям.
- `src.suppliers.suppliers_list.aliexpress.campaign.AliCampaignEditor`: Класс для редактирования кампаний AliExpress.
- `src.gs`: Неизвестный модуль (требуется дополнительная информация).
- `src.suppliers.suppliers_list.aliexpress.campaign.process_campaign_category`, `src.suppliers.suppliers_list.aliexpress.campaign.process_campaign`, `src.suppliers.suppliers_list.aliexpress.campaign.process_all_campaigns`: Функции для обработки категорий, отдельных кампаний и всех кампаний соответственно.
- `src.utils.get_filenames`, `src.utils.get_directory_names`: Функции для получения списка файлов и директорий.
- `src.utils.printer.pprint`: Функция для красивой печати данных.
- `src.logger.logger.logger`: Модуль для логирования событий.

## Переменные модуля

- `campaign_name` (str): Название кампании (`'lighting'`).
- `campaign_file` (str): Имя файла кампании (`'EN_US.JSON'`).
- `campaign_editor` (AliCampaignEditor): Экземпляр класса `AliCampaignEditor` для редактирования кампании.

## Функции

### `AliCampaignEditor`

- **Описание**: Класс предназначен для редактирования рекламных кампаний AliExpress.

- **Методы**:
    - `process_llm_campaign(campaign_name)`: Выполняет обработку LLM кампании.

### `process_campaign_category`

- **Описание**: Функция выполняет обработку категорий кампании.

### `process_campaign`

- **Описание**: Функция выполняет обработку кампании.

### `process_all_campaigns`

- **Описание**: Функция выполняет обработку всех кампаний.

## Пример использования

```python
import header
from pathlib import Path
from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignEditor
from src import gs
from src.suppliers.suppliers_list.aliexpress.campaign import process_campaign_category, process_campaign,  process_all_campaigns
from src.utils import get_filenames, get_directory_names
from src.utils.printer import pprint
from src.logger.logger import logger

campaign_name = 'lighting'
campaign_file = 'EN_US.JSON'
campaign_editor = AliCampaignEditor(campaign_name = campaign_name, campaign_file = campaign_file )
campaign_editor.process_llm_campaign(campaign_name)
#process_all_campaigns()