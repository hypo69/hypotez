## Как использовать этот блок кода
=========================================================================================

### Описание
-------------------------
Блок кода импортирует необходимые модули и создает экземпляр класса `AliCampaignEditor`. Затем он объявляет переменные `locales`, `campaign_name` и `campaign_file`. В конце концов, код запускает функции `process_campaign` и `process_all_campaigns`, но эти вызовы закомментированы.

### Шаги выполнения
-------------------------
1. Импортирует необходимые модули: `header`, `Path`, `AliCampaignEditor`, `gs`, `process_campaign_category`, `process_campaign`, `process_all_campaigns`, `get_filenames`, `get_directory_names`, `pprint` и `logger`.
2. Объявляет словарь `locales`, содержащий информацию о валютах для разных языков.
3. Объявляет строковую переменную `campaign_name` с именем кампании.
4. Объявляет строковую переменную `campaign_file` с именем файла кампании.
5. Создает экземпляр класса `AliCampaignEditor` с именем `campaign_editor` и передаёт в него значения `campaign_name` и `campaign_file`.
6. Выводит значение переменной `campaign_file`.
7. Запускает функции `process_campaign` и `process_all_campaigns`, но эти вызовы закомментированы.

### Пример использования
-------------------------
```python
import header
from pathlib import Path
from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignEditor
from src import gs
from src.suppliers.suppliers_list.aliexpress.campaign import process_campaign_category, process_campaign,  process_all_campaigns
from src.utils import get_filenames, get_directory_names
from src.utils.printer import pprint
from src.logger.logger import logger

#locales = {'EN': 'USD', 'HE': 'ILS', 'RU': 'ILS'}
campaign_name = 'lighting'
campaign_file = 'EN_US.JSON'
campaign_editor = AliCampaignEditor(campaign_name = campaign_name, campaign_file = campaign_file )
campaign_file
#process_campaign(campaign_name)
#process_all_campaigns()

```