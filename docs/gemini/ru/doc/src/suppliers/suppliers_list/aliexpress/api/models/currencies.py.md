# Модуль `src.suppliers.suppliers_list.aliexpress.api.models.currencies`

## Обзор

Модуль содержит класс `Currency`, который определяет список доступных валют для работы с API AliExpress. 

## Классы

### `Currency`

**Описание**: Класс `Currency` предоставляет набор констант, представляющих различные валюты, используемые на платформе AliExpress.

**Атрибуты**:

- `USD` (str): Код валюты - **USD**
- `GBP` (str): Код валюты - **GBP**
- `CAD` (str): Код валюты - **CAD**
- `EUR` (str): Код валюты - **EUR**
- `UAH` (str): Код валюты - **UAH**
- `MXN` (str): Код валюты - **MXN**
- `TRY` (str): Код валюты - **TRY**
- `RUB` (str): Код валюты - **RUB**
- `BRL` (str): Код валюты - **BRL**
- `AUD` (str): Код валюты - **AUD**
- `INR` (str): Код валюты - **INR**
- `JPY` (str): Код валюты - **JPY**
- `IDR` (str): Код валюты - **IDR**
- `SEK` (str): Код валюты - **SEK**
- `KRW` (str): Код валюты - **KRW**
- `ILS` (str): Код валюты - **ILS**

**Примеры**:

```python
from src.suppliers.suppliers_list.aliexpress.api.models.currencies import Currency

# Получение кода валюты USD
usd_currency = Currency.USD

# Проверка, является ли валюта UAH
is_uah_currency = Currency.UAH == 'UAH'

# Использование в вызовах API AliExpress
# ...
```