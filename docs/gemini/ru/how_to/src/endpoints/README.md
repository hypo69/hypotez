## Как использовать модуль `endpoints`
=========================================================================================

Описание
-------------------------
Модуль `endpoints` предоставляет API для взаимодействия с различными потребителями данных. Он содержит подмодули для интеграции с различными системами, обеспечивая бесшовную интеграцию с внешними сервисами. Этот модуль предназначен для организации API-интерфейсов, специфичных для разных клиентов и сервисов.

Шаги выполнения
-------------------------
1. **Установка зависимостей**:
   - Убедитесь, что все зависимости проекта установлены. Используйте команду `pip install -r requirements.txt` для установки необходимых пакетов.

2. **Импорт модуля**:
   - Импортируйте необходимые классы API из соответствующих подмодулей, таких как `PrestashopAPI` из `src.endpoints.prestashop` или `AdvertisementAPI` из `src.endpoints.advertisement`.

3. **Конфигурация и использование**:
   - Настройте необходимые параметры для выбранного API, такие как ключи API, токены доступа и другие параметры конфигурации.
   - Используйте методы API для выполнения необходимых операций, таких как создание, чтение, обновление и удаление данных.

Пример использования
-------------------------

```python
from src.endpoints.prestashop import PrestashopAPI
from src.endpoints.advertisement import AdvertisementAPI

# Пример использования PrestashopAPI
prestashop_api = PrestashopAPI(api_key='your_api_key', api_url='your_prestashop_api_url')
products = prestashop_api.get_products()
print(products)

# Пример использования AdvertisementAPI
advertisement_api = AdvertisementAPI(account_id='your_account_id', access_token='your_access_token')
campaigns = advertisement_api.get_campaigns()
print(campaigns)