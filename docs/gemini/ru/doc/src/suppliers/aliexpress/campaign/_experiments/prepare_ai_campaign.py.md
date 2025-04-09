# Модуль для подготовки AI кампании

## Обзор

Модуль `prepare_ai_campaign.py` предназначен для подготовки и обработки рекламных кампаний AliExpress с использованием AI. Он включает в себя функции для создания, редактирования и обработки кампаний, категорий и всех кампаний в целом.

## Подробней

Модуль предоставляет инструменты для автоматизации процесса подготовки рекламных кампаний, используя класс `AliCampaignEditor` и другие функции для обработки данных кампаний. Расположение файла в проекте указывает на его роль в подготовке AI-кампаний для AliExpress.

## Классы

### `AliCampaignEditor`

**Описание**: Класс `AliCampaignEditor` предназначен для редактирования и обработки рекламных кампаний AliExpress.

**Наследует**:

**Атрибуты**:
- `campaign_name` (str): Название кампании.
- `campaign_file` (str): Файл кампании.

**Методы**:
- `process_ai_campaign(campaign_name)`: Обрабатывает AI кампанию.

## Функции

### `process_campaign_category`

**Назначение**: Обрабатывает категорию кампании.

**Параметры**:
- Нет явных параметров в предоставленном коде.

**Возвращает**:
- Нет явного возвращаемого значения в предоставленном коде.

**Вызывает исключения**:
- Нет явных исключений в предоставленном коде.

### `process_campaign`

**Назначение**: Обрабатывает кампанию.

**Параметры**:
- Нет явных параметров в предоставленном коде.

**Возвращает**:
- Нет явного возвращаемого значения в предоставленном коде.

**Вызывает исключения**:
- Нет явных исключений в предоставленном коде.

### `process_all_campaigns`

**Назначение**: Обрабатывает все кампании.

**Параметры**:
- Нет явных параметров в предоставленном коде.

**Возвращает**:
- Нет явного возвращаемого значения в предоставленном коде.

**Вызывает исключения**:
- Нет явных исключений в предоставленном коде.

## Переменные

- `campaign_name` (str): Название кампании (`'lighting'`).
- `campaign_file` (str): Имя файла кампании (`'EN_US.JSON'`).
- `campaign_editor` (AliCampaignEditor): Экземпляр класса `AliCampaignEditor`, используемый для обработки кампании.

## Пример использования

```python
import header
from pathlib import Path
from src.suppliers.aliexpress.campaign import AliCampaignEditor
from src import gs
from src.suppliers.aliexpress.campaign import process_campaign_category, process_campaign,  process_all_campaigns
from src.utils import get_filenames, get_directory_names
from src.utils.printer import pprint
from src.logger.logger import logger

#locales = {\'EN\': \'USD\', \'HE\': \'ILS\', \'RU\': \'ILS\'}
campaign_name = 'lighting'
campaign_file = 'EN_US.JSON'
campaign_editor = AliCampaignEditor(campaign_name = campaign_name, campaign_file = campaign_file )
campaign_editor.process_ai_campaign(campaign_name)
#process_all_campaigns()