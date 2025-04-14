# Модуль `aliexpress_promote_deal`

## Обзор

Модуль `aliexpress_promote_deal` предназначен для подготовки данных о промо-акциях AliExpress в формате, пригодном для использования в Facebook. В частности, он используется для создания объявлений о скидках и специальных предложениях.

## Подробней

Модуль является экспериментальным и находится в стадии разработки. Он использует класс `AliPromoDeal` для подготовки данных о продуктах и акциях.

## Функции

### `AliPromoDeal`

Класс для работы с промо-акциями AliExpress.

**Описание**:
Класс `AliPromoDeal` используется для подготовки данных о промо-акциях AliExpress, включая подготовку списка продуктов для акций.

**Методы**:

- `prepare_products_for_deal()`: Метод для подготовки продуктов к промо-акции.

## Параметры

В коде определены следующие параметры:

- `deal_name` (str): Имя промо-акции (`'150624_baseus_deals'`).
- `a` (AliPromoDeal): Инстанс класса `AliPromoDeal`, созданный с именем акции `deal_name`.

## Пример использования

```python
import header
from src.suppliers.aliexpress import AliPromoDeal

deal_name = '150624_baseus_deals'
a = AliPromoDeal(deal_name)
# products = a.prepare_products_for_deal()
```

В данном примере создается инстанс класса `AliPromoDeal` с именем акции `'150624_baseus_deals'`, после чего можно использовать метод `prepare_products_for_deal()` для подготовки продуктов к акции.