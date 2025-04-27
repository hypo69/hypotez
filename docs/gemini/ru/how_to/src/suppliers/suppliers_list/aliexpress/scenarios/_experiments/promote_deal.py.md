## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код создает рекламную кампанию для товаров на AliExpress. Он использует класс `AliPromoDeal` для работы с конкретным предложением ("150624_baseus_deals"). 

Шаги выполнения
-------------------------
1. Импортируются необходимые модули: `header` и `AliPromoDeal` из `src.suppliers.suppliers_list.aliexpress.scenarios`.
2. Создается объект `deal` класса `AliPromoDeal` с указанием идентификатора предложения "150624_baseus_deals".
3. Получаются подробные сведения о всех товарах в этом предложении с помощью `deal.get_all_products_details()`.

Пример использования
-------------------------

```python
## \file /src/suppliers/aliexpress/scenarios/_experiments/promote_deal.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress.scenarios._experiments 
	:platform: Windows, Unix
	:synopsis:

"""

""" Создание рекламной кампании """

import header

from src.suppliers.suppliers_list.aliexpress.scenarios import AliPromoDeal

deal = AliPromoDeal('150624_baseus_deals')

#product = deal.get_next_product()
products = deal.get_all_products_details()

...
```