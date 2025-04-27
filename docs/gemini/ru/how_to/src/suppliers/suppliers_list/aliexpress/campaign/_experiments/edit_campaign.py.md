## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода демонстрирует пример использования класса `AliCampaignEditor` для работы с рекламными кампаниями на AliExpress. Он инициализирует объект `AliCampaignEditor` с заданным именем кампании, языком (`EN`) и валютой (`USD`), а затем выполняет ряд действий для обработки кампании.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей:** 
    - `header`:  Импортирует необходимый заголовок.
    - `Path`: Импортирует класс `Path` из модуля `pathlib` для работы с файлами и директориями.
    - `gs`: Импортирует модуль `gs` для работы с Google Sheets.
    - `AliCampaignEditor`: Импортирует класс `AliCampaignEditor` из модуля `aliexpress.campaign` для редактирования рекламных кампаний на AliExpress.
    - `process_campaign`, `process_campaign_category`, `process_all_campaigns`: Импортирует функции для обработки данных рекламных кампаний.
    - `get_filenames`, `get_directory_names`: Импортирует функции для получения имен файлов и директорий.
    - `pprint`: Импортирует функцию `pprint` для красивого вывода данных в консоль.

2. **Определение словаря `locales`:**
    - Содержит соответствие между языками и валютами.
    - В этом примере `EN` соответствует `USD`, `HE` соответствует `ILS`, `RU` соответствует `ILS`.

3. **Задаются имена кампании и категории:**
    - `campaign_name` устанавливается как `"building_bricks"`.
    - `category_name` устанавливается как `"building_bricks"`.

4. **Создание объекта `AliCampaignEditor`:**
    - `a = AliCampaignEditor(campaign_name,\'EN\',\'USD\')` создает объект `AliCampaignEditor` с именем кампании `"building_bricks"`, языком `EN` и валютой `USD`.

5. **Выполнение дальнейших действий:**
    - После создания объекта `AliCampaignEditor` код продолжает выполнение действий для обработки и редактирования рекламной кампании. 

Пример использования
-------------------------

```python
import header
from pathlib import Path

from src import gs
from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignEditor
from src.suppliers.suppliers_list.aliexpress.campaign import  process_campaign, process_campaign_category, process_all_campaigns
from src.utils import get_filenames, get_directory_names
from src.utils.printer import pprint

locales = {'EN': 'USD', 'HE': 'ILS', 'RU': 'ILS'}

# Имя кампании и категории
campaign_name = "building_bricks"
category_name = "building_bricks"

# Создание объекта AliCampaignEditor
a = AliCampaignEditor(campaign_name, 'EN', 'USD')

# Выполнение дальнейших действий
# ...
```