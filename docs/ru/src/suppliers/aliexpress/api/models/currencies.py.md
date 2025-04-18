# Модуль `currencies`

## Обзор

Модуль содержит класс `Currency`, который определяет константы для различных валют. Этот класс используется для стандартизации валютных обозначений в рамках проекта.

## Подробней

Этот модуль предоставляет централизованный способ определения кодов валют, используемых в API AliExpress. Он помогает избежать использования "магических строк" в коде, делая его более читаемым и поддерживаемым.

## Классы

### `Currency`

**Описание**: Класс, содержащий константы, представляющие различные валюты.
**Наследует**: Нет.
**Атрибуты**: Нет.
**Методы**: Нет.

**Принцип работы**:
Класс `Currency` содержит статические атрибуты, каждый из которых представляет собой код валюты. Значения этих атрибутов - строковые литералы, соответствующие общепринятым обозначениям валют (например, `'USD'` для доллара США).

## Параметры класса

- `USD` (str): Доллар США.
- `GBP` (str): Фунт стерлингов.
- `CAD` (str): Канадский доллар.
- `EUR` (str): Евро.
- `UAH` (str): Украинская гривна.
- `MXN` (str): Мексиканский песо.
- `TRY` (str): Турецкая лира.
- `RUB` (str): Российский рубль.
- `BRL` (str): Бразильский реал.
- `AUD` (str): Австралийский доллар.
- `INR` (str): Индийская рупия.
- `JPY` (str): Японская иена.
- `IDR` (str): Индонезийская рупия.
- `SEK` (str): Шведская крона.
- `KRW` (str): Южнокорейская вона.
- `ILS` (str): Израильский шекель.

**Примеры**

```python
# Использование констант валют
currency_code = Currency.USD
print(currency_code)  # Вывод: USD

if currency_code == Currency.EUR:
    print("Это евро")
else:
    print("Это не евро")  # Вывод: Это не евро