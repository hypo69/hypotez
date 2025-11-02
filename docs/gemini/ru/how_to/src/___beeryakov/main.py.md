## Как использовать блок кода `run()`
=========================================================================================

Описание
-------------------------
Блок кода `run()` запускает парсер для сбора данных с сайта KSP.co.il и сохранения их в Google Таблицы. 

Шаги выполнения
-------------------------
1. **Инициализация:**
    - Задается идентификатор Google Таблицы (sh_id).
    - Устанавливается корневой URL сайта KSP (root).
    - Открывается корневая страница сайта KSP (d.get(root)).
    - Получается словарь с URL-адресами страниц миров и их названиями (worlds_dic) с помощью функции `ksp.get_worlds()`.
2. **Цикл по мирам:**
    - Перебираются все URL-адреса миров (worlds_dic.items()).
    - Создается объект Google Таблицы (GSpreadsheet) для конкретной таблицы (sh).
    - Создается объект Google Рабочего листа (GWorksheet) для конкретного мира (ws).
    - Задается заголовок для рабочего листа (ws.header(ws_title, 'A1:Z1')).
3. **Создание таблицы:**
    - Проверяется, существует ли таблица в Google Таблицах:
        - Если да, таблица очищается от старых данных.
        - Если нет, таблица создается.
    - Возвращается объект Google Рабочего листа (ws).
4. **Сбор данных:**
    - Открывается страница мира (d.get(url)).
    - Получается словарь с URL-адресами категорий и их названиями (subs) с помощью функции `ksp.get_subs_from_world()`.
5. **Цикл по категориям:**
    - Перебираются все URL-адреса категорий (subs.items()).
    - Открывается страница категории (d.get(url)).
    - Добавляется строка с названием категории в таблицу (ws.append_row(ws.category(category_title))).
    - Получается словарь с названиями брендов и их количеством (brands) с помощью функции `ksp.get_all_brands_list()`.
6. **Цикл по брендам:**
    - Перебираются все бренды (brands.items()).
    - Добавляется строка с названием бренда и количеством в таблицу (ws.append_row([brand, qty])).
    - Выводится информация о добавленных брендах.

Пример использования
-------------------------

```python
from src import gs
from src.logger.logger import logger, WebDriverException,  pprint
from src.webdriver.driver import Driver as d
from src.beeryakov.suppliers import ksp
import GSpreadsheet, GWorksheet

def run():
    """
    Старт парсера
    """
    sh_id = '1ZcK74BCgWKVr4kODjPmSvjp5IyO0OxhXdbeHKWzLQiM'
    root: str = 'https://ksp.co.il' 
    d.get(root)
    worlds_dic: dict = ksp.get_worlds()

    sh = GSpreadsheet(sh_id)
    
    for url, ws_title in worlds_dic.items():
        
        ws: GWorksheet = GWorksheet(sh, ws_title)
        ws.header(ws_title, 'A1:Z1')
        
        """
          1. добавляю таблицу в книгу если ее нет,
          иначе очищаю от страых данных
          2.  и возвращаю ее  """
        
        d.get(url)
        """ ныряю в категорию """
        subs = ksp.get_subs_from_world()
        #print('\t\t CATEGORIES: ')

        for url, category_title in subs.items():
            
            d.get(url)
            
            ws.append_row (ws.category (category_title ) )
            brands = ksp.get_all_brands_list()
            print(f'\t\t\t BRANDS:')
            #_ws.append_row([f' category} - BRANDS'])
            i=0
            for brand, qty in brands.items():
                ws.append_row([brand,qty])
                i += 1
                
            print(f'added {i}')
        
        pprint(f' ********************************')

run()
```