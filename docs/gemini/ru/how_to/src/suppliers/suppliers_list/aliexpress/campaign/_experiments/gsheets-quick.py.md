### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для работы с Google Sheets в контексте рекламных кампаний AliExpress. Он инициализирует объект `AliCampaignGoogleSheet`, устанавливает рабочий лист продуктов и сохраняет данные о кампаниях из рабочего листа.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются классы и модули, необходимые для работы с Google Sheets, типами данных и логирования.
2. **Определение параметров**: Задаются параметры рекламной кампании, такие как `campaign_name`, `category_name`, `language` и `currency`.
3. **Инициализация `AliCampaignGoogleSheet`**: Создается экземпляр класса `AliCampaignGoogleSheet` с использованием заданных параметров. Этот класс предназначен для работы с Google Sheets, специфичными для рекламных кампаний AliExpress.
4. **Установка рабочего листа продуктов**: Вызывается метод `set_products_worksheet` для установки текущего рабочего листа, с которым будет работать объект `AliCampaignGoogleSheet`. В качестве параметра передается `category_name`.
5. **Сохранение кампании из рабочего листа**: Вызывается метод `save_campaign_from_worksheet` для сохранения данных о кампании из установленного рабочего листа. Этот метод извлекает данные из Google Sheets и сохраняет их в соответствующем формате.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignGoogleSheet
from src.utils.printer import pprint
from src.logger.logger import logger

campaign_name = "lighting"
category_name = "chandeliers"
language = 'EN'
currency = 'USD'

# Инициализация объекта AliCampaignGoogleSheet для работы с Google Sheets
gs = AliCampaignGoogleSheet(campaign_name=campaign_name, language=language, currency=currency)

# Установка рабочего листа продуктов
gs.set_products_worksheet(category_name)

# Сохранение кампании из рабочего листа
gs.save_campaign_from_worksheet()