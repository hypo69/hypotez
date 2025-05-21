## \file /src/suppliers/suppliers_list/hb/sceanrio.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""  
Модуль сбора товаров со страницы категорий поставщика hb.co.il через вебдрайвер
=====================================================================================

Определение сценария обработки категорий для каждого поставщика.

- Модуль собирает список категорий со страниц продавца (`get_list_categories_from_site()`).
@todo Сделать проверку на изменение категорий на страницах продавца. 
Продавец может добавлять новые категории, переименовывать или удалять/прятать уже существующие. 
По большому счету надо держать таблицу категории `PrestaShop.categories <-> aliexpress.shop.categoies`
- Собирает список товаров со страницы категории (`get_list_products_in_category()`).
- Итерируясь по списку, передает управление в `grab_product_page()`, отсылая функции текущий URL страницы.  
`grab_product_page()` обрабатывает поля товара и передает управление классу `Product`.

```rst
 .. module:: src.suppliers.suppliers_list.hb.sceanrio
```
"""

import asyncio
from typing import List, Any, Dict # Added Any, Dict
from types import SimpleNamespace # Added SimpleNamespace

import header # Added header import
from header import __root__ # Added __root__ import
from src import gs # Ensured gs import
from src.logger.logger import logger
from src.webdriver.driver import Driver


async def get_list_products_in_category (d: Driver, l: SimpleNamespace) -> List[str] | None:    
    """ 
    Функция извлекает список URL-адресов товаров со страницы категории.
    При необходимости пролистывает страницы категорий.

    Args:
        d (Driver): Экземпляр WebDriver.
        l (SimpleNamespace): Объект с локаторами для страницы категории, 
                             включая локаторы товаров и пагинации.
    
    Returns:
        List[str] | None: Список URL-адресов товаров или `None`, если товары не найдены.
    
    Example:
        >>> # Пример использования (требует настройки d и l)
        >>> # driver = Driver(...) 
        >>> # locators = SimpleNamespace(product_links=..., pagination_locators=...)
        >>> # product_urls = await get_list_products_in_category(driver, locators)
        >>> # if product_urls:
        >>> #     print(f'Найдено {len(product_urls)} товаров.')
    """
    all_product_urls: List[str] = []
    # Извлечение ссылок на товары с текущей (первой) страницы
    initial_links_on_page: List[str] | str | None = await d.execute_locator(l.product_links)

    d.wait(1) # Ожидание после действия
    d.scroll() # Прокрутка страницы
    ...

    if not initial_links_on_page:
        logger.warning('Нет ссылок на товары на первой странице. Так бывает')
        ... # Точка останова или специфическая логика
        # В оригинальном коде здесь был return без значения, что эквивалентно return None
        # Если требуется продолжить пагинацию даже если первая страница пуста, эту логику нужно изменить.
        # Пока что сохраняется поведение возврата None, если первая страница пуста.
        return None 
    
    if isinstance(initial_links_on_page, str):
        all_product_urls.append(initial_links_on_page)
    elif isinstance(initial_links_on_page, list): # Убедиться, что это список (может быть и другой тип)
        all_product_urls.extend(initial_links_on_page)
    
    # Цикл пагинации для сбора ссылок с последующих страниц
    # Условие d.current_url != d.previous_url предполагает, что Driver управляет previous_url,
    # обновляя его перед/после навигационных действий.
    while d.current_url != d.previous_url: 
        navigated_successfully: bool = await paginator(d, l) # Передача основного объекта локаторов 'l'
        if navigated_successfully:
            # Загрузка ссылок с новой страницы после успешной пагинации
            links_on_new_page: List[str] | str | None = await d.execute_locator(l.product_links)
            if isinstance(links_on_new_page, str):
                all_product_urls.append(links_on_new_page)
            elif isinstance(links_on_new_page, list):
                all_product_urls.extend(links_on_new_page)
            # Если links_on_new_page is None, ничего не добавляется, цикл продолжается
            # на основе изменения URL (или другого условия выхода из пагинации).
        else:
            # Пагинация не удалась или достигнут конец страниц
            break
        
    if not all_product_urls:
        logger.warning('Не найдено ссылок на товары во всей категории (включая пагинацию).')
        return None

    logger.debug(f'Найдено {len(all_product_urls)} товаров в категории ({d.current_url})')
    
    return all_product_urls

async def paginator(d: Driver, main_locators: SimpleNamespace) -> bool:
    """ 
    Функция выполняет переход на следующую страницу (пагинацию).

    Args:
        d (Driver): Экземпляр WebDriver.
        main_locators (SimpleNamespace): Основной объект локаторов, содержащий 
                                         `pagination` атрибут, который, в свою очередь,
                                         используется для нахождения локатора кнопки пагинации.
                                         Ожидается, что `main_locators.pagination.__dict__['<-']` 
                                         вернет локатор для клика.
    
    Returns:
        bool: `True`, если переход на следующую страницу (клик по элементу пагинации) 
              был выполнен (не обязательно означает успешную загрузку новой страницы, 
              а лишь успешное выполнение действия клика), иначе `False`.
    
    Example:
        >>> # Внутри get_list_products_in_category:
        >>> # if await paginator(driver_instance, locators_object):
        >>> #     print('Переход на следующую страницу выполнен.')
    """
    # Предполагается, что main_locators.pagination является объектом (например, SimpleNamespace),
    # у которого есть атрибут с именем '<-', доступный через __dict__.
    # Это специфичный способ доступа к локатору.
    pagination_element_locator: Dict | None = None
    if hasattr(main_locators, 'pagination') and isinstance(main_locators.pagination, SimpleNamespace):
        pagination_element_locator = main_locators.pagination.__dict__.get('<-')
    
    if not pagination_element_locator:
        logger.warning('Локатор для пагинации не найден или некорректно сконфигурирован.')
        return False

    response: Any = await d.execute_locator(pagination_element_locator)
    if not response : # Проверка, что клик был как-то зарегистрирован (execute_locator может вернуть None/False при ошибке)
        ... # Точка останова или специфическая логика при неудачной попытке клика
        logger.debug('Элемент пагинации не найден или действие не выполнено.')
        return False
    return True

def build_list_categories_from_site(s: Any) -> Any:
    """ 
    Функция для сбора актуального списка категорий с веб-сайта поставщика.
    (Реализация этой функции не предоставлена в исходном фрагменте).

    Args:
        s (Any): Параметр, представляющий поставщика или конфигурацию поставщика. 
                 Тип требует уточнения в зависимости от реализации.
    
    Returns:
        Any: Результат сбора категорий (например, список словарей или объектов категорий). 
             Тип требует уточнения.
    
    Raises:
        NotImplementedError: Если функция вызвана без реализации.

    Example:
        >>> # supplier_config = ... 
        >>> # categories = build_list_categories_from_site(supplier_config)
        >>> # if categories:
        >>> #     print(f'Собрано {len(categories)} категорий.')
    """
    ... # Точка останова или начало реализации функции
    logger.info(f'Запущена функция build_list_categories_from_site для поставщика: {s}')
    # Здесь должна быть логика сбора категорий
    # raise NotImplementedError('Функция build_list_categories_from_site еще не реализована.')
    return None # Заглушка
