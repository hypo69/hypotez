# Модуль deals_from_xls.py

## Обзор

Модуль `deals_from_xls.py` предназначен для парсинга XLS-таблиц, сгенерированных в личном кабинете portals.aliexpress.com, и извлечения информации о сделках.

## Подробней

Этот модуль используется для автоматизации процесса получения данных о сделках с AliExpress путем обработки XLS-файлов. Он использует класс `DealsFromXLS` для парсинга данных и извлечения информации о каждой сделке.

## Классы

В данном коде не представлены классы для документирования.
В коде используется класс `DealsFromXLS`, импортированный из модуля `src.suppliers.suppliers_list.aliexpress`.
```python
from src.suppliers.suppliers_list.aliexpress import DealsFromXLS
```

## Функции

В данном коде не представлены функции для документирования.
В коде вызывается метод `get_next_deal()` класса `DealsFromXLS`

## Переменные

- `deals_parser`: Инстанс класса `DealsFromXLS`, используемый для парсинга XLS-таблиц и извлечения данных о сделках. Инициализируется с параметрами `language='EN'` и `currency='USD'`.

```python
deals_parser = DealsFromXLS(language='EN', currency= 'USD')
```

## Принцип работы

1.  Импортируются необходимые модули, включая `header`, `DealsFromXLS` из `src.suppliers.suppliers_list.aliexpress` и `pprint` из `src.utils.printer`.
2.  Создается экземпляр класса `DealsFromXLS` с указанием языка (`EN`) и валюты (`USD`).
3.  В цикле перебираются сделки, полученные с помощью метода `get_next_deal()` экземпляра класса `DealsFromXLS`.
4.  Каждая сделка выводится на экран с помощью функции `pprint`.

## Примеры

```python
from src.suppliers.suppliers_list.aliexpress import DealsFromXLS 
from src.utils.printer import pprint

deals_parser = DealsFromXLS(language='EN', currency= 'USD')

for deal in deals_parser.get_next_deal():
    pprint(deal)