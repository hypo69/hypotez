### **Инструкция по использованию блока кода**

=========================================================================================

Описание
-------------------------
Данный блок кода инициализирует и настраивает редактор рекламных кампаний AliExpress. Он создает экземпляр класса `AliCampaignEditor` для конкретной рекламной кампании, языка и валюты.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `header`, `Path`, `gs`, `AliCampaignEditor`, `process_campaign`, `process_campaign_category`, `process_all_campaigns`, `get_filenames`, `get_directory_names` и `pprint`.
2. **Определение локалей**:
   - Создается словарь `locales`, который сопоставляет языки с валютами. В данном случае, `EN` (английский) соответствует `USD` (доллар США), `HE` (иврит) и `RU` (русский) соответствуют `ILS` (израильский шекель).
3. **Определение имени кампании и категории**:
   - Устанавливаются переменные `campaign_name` и `category_name` для указания конкретной рекламной кампании и категории. В данном случае, кампания называется `"building_bricks"`, и категория также `"building_bricks"`.
4. **Создание экземпляра `AliCampaignEditor`**:
   - Создается экземпляр класса `AliCampaignEditor` с именем `a`, используя имя кампании, язык и валюту. В данном случае, кампания `"building_bricks"` на английском языке (`'EN'`) в долларах США (`'USD'`).

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

campaign_name = "building_bricks"
category_name = "building_bricks"
a = AliCampaignEditor(campaign_name,'EN','USD')