# Модуль `languages`

## Обзор

Модуль содержит класс `Language`, который определяет константы для различных языков, используемых в API AliExpress.

## Подробней

Этот модуль предоставляет централизованный способ определения языковых кодов, используемых при взаимодействии с API AliExpress. Использование класса `Language` помогает обеспечить консистентность и избежать ошибок при работе с разными языками.

## Классы

### `Language`

**Описание**: Класс, содержащий константы для представления различных языков.

**Атрибуты**:

- `EN` (str): Константа для английского языка ('EN').
- `RU` (str): Константа для русского языка ('RU').
- `PT` (str): Константа для португальского языка ('PT').
- `ES` (str): Константа для испанского языка ('ES').
- `FR` (str): Константа для французского языка ('FR').
- `ID` (str): Константа для индонезийского языка ('ID').
- `IT` (str): Константа для итальянского языка ('IT').
- `TH` (str): Константа для тайского языка ('TH').
- `JA` (str): Константа для японского языка ('JA').
- `AR` (str): Константа для арабского языка ('AR').
- `VI` (str): Константа для вьетнамского языка ('VI').
- `TR` (str): Константа для турецкого языка ('TR').
- `DE` (str): Константа для немецкого языка ('DE').
- `HE` (str): Константа для иврита ('HE').
- `KO` (str): Константа для корейского языка ('KO').
- `NL` (str): Константа для нидерландского языка ('NL').
- `PL` (str): Константа для польского языка ('PL').
- `MX` (str): Константа для мексиканского испанского языка ('MX').
- `CL` (str): Константа для чилийского испанского языка ('CL').
- `IW` (str): Константа для иврита (старое обозначение, 'IW').
- `IN` (str): Константа для индийского языка ('IN').

**Принцип работы**:
Класс `Language` содержит набор статических атрибутов, каждый из которых представляет собой строковый код языка. Эти константы используются для указания языка при выполнении запросов к API AliExpress. Класс не имеет методов и служит исключительно для хранения констант.

## Примеры

### Использование констант языка

```python
from src.suppliers.aliexpress.api.models.languages import Language

# Пример использования константы для английского языка
english_code = Language.EN
print(english_code)  # Вывод: EN

# Пример использования константы для русского языка
russian_code = Language.RU
print(russian_code)  # Вывод: RU