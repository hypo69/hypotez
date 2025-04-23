### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предназначен для подготовки JSON-файлов для рекламных кампаний AliExpress. Он использует модуль `AliCampaignEditor` для управления и обработки данных кампаний, а также функции для обработки категорий и самих кампаний.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули `header`, `Path`, `AliCampaignEditor`, `gs`, функции `process_campaign_category`, `process_campaign`, `process_all_campaigns`, `get_filenames`, `get_directory_names`, `pprint` и `logger`.
2. **Инициализация переменных**:
   - Задается имя кампании (`campaign_name`) как `'lighting'`.
   - Задается имя файла кампании (`campaign_file`) как `'EN_US.JSON'`.
3. **Создание экземпляра `AliCampaignEditor`**: Создается экземпляр класса `AliCampaignEditor` с именем кампании и файлом кампании.
4. **Вывод имени файла кампании**: Выводится значение переменной `campaign_file`.
5. **Закомментированные вызовы функций**: В коде закомментированы вызовы функций `process_campaign` и `process_all_campaigns`, что указывает на то, что они могут быть использованы для обработки кампании или всех кампаний соответственно.

Пример использования
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

campaign_name = 'lighting'
campaign_file = 'EN_US.JSON'
campaign_editor = AliCampaignEditor(campaign_name = campaign_name, campaign_file = campaign_file)

# Пример вызова функции для обработки конкретной кампании
# process_campaign(campaign_name)

# Пример вызова функции для обработки всех кампаний
# process_all_campaigns()