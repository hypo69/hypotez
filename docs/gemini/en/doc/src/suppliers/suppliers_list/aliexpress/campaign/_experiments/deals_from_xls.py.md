# Модуль для парсинга таблиц xls с AliExpress

## Обзор

Этот модуль содержит код для парсинга таблиц xls, сгенерированных в личном кабинете portals.aliexpress.com. Он использует класс `DealsFromXLS` для извлечения данных из файла xls.

## Детали

Модуль `src.suppliers.suppliers_list.aliexpress.campaign._experiments.deals_from_xls.py`  использует класс `DealsFromXLS` для парсинга таблиц xls.

### Класс `DealsFromXLS`

**Описание**: Класс `DealsFromXLS` предназначен для извлечения данных из таблиц xls, полученных с портала portals.aliexpress.com. 

**Атрибуты**:

- `language` (str): Язык, на котором отображаются данные в таблице xls. По умолчанию используется английский язык (`EN`).
- `currency` (str): Валюта, в которой отображаются цены в таблице xls. По умолчанию используется доллар США (`USD`).

**Методы**:

- `get_next_deal()`: Метод, который итеративно возвращает данные о следующей сделке из таблицы xls.

**Принцип работы**:

Класс `DealsFromXLS` использует библиотеку `pandas` для чтения таблицы xls и обработки ее данных. 

**Пример**:

```python
from src.suppliers.suppliers_list.aliexpress import DealsFromXLS 

deals_parser = DealsFromXLS(language='EN', currency='USD')

for deal in deals_parser.get_next_deal():
    print(deal)
```

## Функции

### `deals_from_xls.py`

**Описание**: Файл `deals_from_xls.py`  создает экземпляр класса `DealsFromXLS` и итеративно выводит данные о сделках из файла xls.

**Принцип работы**:

1. Создается экземпляр класса `DealsFromXLS` с указанием языка и валюты.
2.  С помощью цикла `for`  итеративно вызывается метод `get_next_deal()`, который возвращает данные о следующей сделке.
3.  Данные о сделке выводится на экран с использованием функции `pprint`.

**Пример**:

```python
from src.suppliers.suppliers_list.aliexpress import DealsFromXLS 
from src.utils.printer import pprint

deals_parser = DealsFromXLS(language='EN', currency='USD')

for deal in deals_parser.get_next_deal():
    pprint(deal)
```

## Параметры

- `language` (str): Язык, на котором отображаются данные в таблице xls. По умолчанию используется английский язык (`EN`).
- `currency` (str): Валюта, в которой отображаются цены в таблице xls. По умолчанию используется доллар США (`USD`).

## Примеры

```python
# Импорт необходимых модулей
from src.suppliers.suppliers_list.aliexpress import DealsFromXLS
from src.utils.printer import pprint

# Создание экземпляра класса DealsFromXLS
deals_parser = DealsFromXLS(language='EN', currency='USD')

# Итерация по данным о сделках
for deal in deals_parser.get_next_deal():
    # Вывод данных о сделке на экран
    pprint(deal)
```

```python
# Импорт необходимых модулей
from src.suppliers.suppliers_list.aliexpress import DealsFromXLS
from src.utils.printer import pprint

# Создание экземпляра класса DealsFromXLS с указанием языка и валюты
deals_parser = DealsFromXLS(language='RU', currency='RUB')

# Итерация по данным о сделках
for deal in deals_parser.get_next_deal():
    # Вывод данных о сделке на экран
    pprint(deal)
```

## Дополнительная информация

- Модуль `deals_from_xls.py` предназначен для обработки таблиц xls, сгенерированных в личном кабинете portals.aliexpress.com.
-  Класс `DealsFromXLS`  предоставляет удобный интерфейс для извлечения данных из таблицы xls.
- `pprint` - функция, которая используется для красивого вывода данных на экран.
-  Данный модуль использует библиотеку `pandas` для обработки таблицы xls.

##  Как работает код
 
 1.  **Импорт модулей:**
    -   `header` -  модуль,  в котором могут быть объявлены дополнительные настройки.
    -   `DealsFromXLS` -  класс для парсинга таблиц xls с AliExpress.
    -   `pprint` - функция для красивого вывода данных на экран.

 2.  **Инициализация парсера:**
    -   `deals_parser = DealsFromXLS(language='EN', currency='USD')` -  создание экземпляра класса `DealsFromXLS` с указанием языка (`EN`) и валюты (`USD`).

 3.  **Итерация по сделкам:**
    -   `for deal in deals_parser.get_next_deal():` -  итерация по сделкам из таблицы xls с помощью метода `get_next_deal()`.
    -   `pprint(deal)` -  красивый вывод данных о сделке на экран с помощью функции `pprint`.

 4.  **Доработка:**
    -   `...` -  место,  где  может быть добавлен  дополнительный код для обработки  данных о сделке.