## \file hypotez/src/suppliers/scenario/scenario_executor.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Исполнитель сценариев поставщиков
====================================
Модуль может исполнять различные сценарии, такие как:
- Сбор товаров в определенной категории
- Сбор товаров по определенному фильтру
- Сбор товаров по определенному производителю
- ...
- и т.д.
```rst
.. module::  src.suppliers.scenario.scenario_executor
```
"""

import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any, TypeAlias
from types import SimpleNamespace

import header
from header import __root__
from src import gs
from src.utils.jjson import j_loads
from src.endpoints.prestashop.product import PrestaProduct

from src.logger.logger import logger


async def run_scenario_files(
                            s: 'Supplier', 
                            d: 'Driver', 
                            scenario_files_list: List[Path]|Path, 
                            crawl_category_function: Any
                            ) -> bool:
    """
    Функция выполняет список файлов сценариев.

    Args:
        s (SupplierInstance): Экземпляр поставщика.
        d (d): Экземпляр веб-драйвера.
        scenario_files_list (List[Path] | Path): Список путей к файлам сценариев или один путь к файлу.
        crawl_category_function (Any): Функция для обхода категорий, используемая в сценарии (например,
                                      `get_list_products_in_category` из сценария поставщика).

    Returns:
        bool: `True`, если все сценарии выполнены успешно, иначе `False`.

    Raises:
        TypeError: Если `scenario_files_list` не является списком или объектом `Path`.

    Example:
        >>> # Предполагается, что 'supplier_instance', 'd_instance', 'my_crawl_function' определены
        >>> # scenario_paths = [Path('path/to/scenario1.json'), Path('path/to/scenario2.json')]
        >>> # result = await run_scenario_files(supplier_instance, d_instance, scenario_paths, my_crawl_function)
        >>> # print(f'Все сценарии выполнены успешно: {result}')
    """



    for scenario_file in scenario_files_list:
        try:
            if await run_scenario_file(s,d,scenario_file,crawl_category_function ):
                logger.success(f'Сценарий {scenario_file} успешно завершен.')
            else:
                logger.error(f'Сценарий {scenario_file} не удалось выполнить.')
        except Exception as ex:
            logger.critical(f'Произошла ошибка при обработке сценария {scenario_file}', ex, exc_info=True)
    return True # Возвращаем True, если цикл завершился (даже если были ошибки в отдельных файлах)


async def run_scenario_file(
                            s: 'Supplier', 
                            d: 'Driver',
                            scenario_file: Path,
                            crawl_category_function: Any
                            ) -> bool:
    """
    Функция загружает и выполняет сценарии из файла.

    Args:
        s (SupplierInstance): Экземпляр поставщика.
        d (d): Экземпляр веб-драйвера.
        scenario_file (Path): Путь к файлу сценария.
        crawl_category_function (Any): Функция для обхода категорий, используемая в сценарии.

    Returns:
        bool: `True`, если сценарий выполнен успешно, иначе `False`.

    Example:
        >>> # Предполагается, что 'supplier_instance', 'd_instance', 'scenario_file_path', 'my_crawl_function' определены
        >>> # result = await run_scenario_file(supplier_instance, d_instance, scenario_file_path, my_crawl_function)
        >>> # print(f'Сценарий файла выполнен успешно: {result}')
    """
    scenarios_dict: Dict[str, Any] 
    scenario_name: str
    scenario_data: Dict[str, Any]

    try:
        scenarios_dict = j_loads(scenario_file)
        if not scenarios_dict: # j_loads возвращает пустой dict при ошибке
            logger.error(f'Не удалось загрузить или декодировать JSON из файла сценария: {scenario_file}.')
            return False

        for scenario_name, scenario_data in scenarios_dict.items():
            s.current_scenario = scenario_data # Обновление текущего сценария в объекте поставщика
            if await run_scenario(s,d,scenario_data,scenario_name,crawl_category_function):
                logger.success(f'Сценарий "{scenario_name}" из файла {scenario_file} успешно завершен.')
            else:
                logger.error(f'Сценарий "{scenario_name}" из файла {scenario_file} не удалось выполнить.')
        return True

    except Exception as ex:
        logger.critical(f'Непредвиденная ошибка при выполнении сценария из файла {scenario_file}', ex, exc_info=True)
        return False


async def run_scenarios(
                        s: 'Supplier', 
                        d: 'Driver',
                        scenarios: Optional[List[dict] | dict],
                        crawl_category_function: Any
                        ) -> List | dict | bool:
    """
    Функция выполняет список сценариев (НЕ ФАЙЛОВ).

    Args:
        s (SupplierInstance): Экземпляр поставщика.
        d (d): Экземпляр веб-драйвера.
        scenarios (Optional[List[dict] | dict], optional): Принимает список сценариев или один сценарий в виде словаря.
                                                          По умолчанию используется `s.current_scenario`.
        crawl_category_function (Any, optional): Функция для обхода категорий, используемая в сценарии.
                                                  По умолчанию `None`.

    Returns:
        List | dict | bool: Результат выполнения сценариев или `False` в случае ошибки.

    Todo:
        Проверить опцию, когда сценарии не указаны со всех сторон. Например, когда `s.current_scenario`
        не указан и сценарии не указаны.

    Example:
        >>> # Предполагается, что 'supplier_instance', 'd_instance' определены
        >>> # my_scenario = {'url': 'http://example.com/category', 'name': 'MyCategoryScenario'}
        >>> # results = await run_scenarios(supplier_instance, d_instance, scenarios=my_scenario)
        >>> # print(f'Результаты выполнения сценариев: {results}')
    """

    
    results: List[Any] = [] 
    scenarios = scenarios if isinstance(scenarios, list) else [scenarios]
    for scenario_item in scenarios:
        # Генерация уникального имени сценария, если оно отсутствует
        
        result = await run_scenario(s, d, scenario_item,  crawl_category_function)
        results.append(result)
    return results


async def run_scenario(
                        s: 'Supplier', 
                        d: 'Driver',
                        scenario: SimpleNamespace,
                        crawl_category_function: Any
                        ) -> List | dict | bool:
    """
    Функция выполняет полученный сценарий.

    Args:
        s (SupplierInstance): Экземпляр поставщика.
        d (d): Экземпляр веб-драйвера.
        scenario (Dict[str, Any]): Словарь, содержащий детали сценария.
        scenario_name (str): Имя сценария.
        crawl_category_function (Any, optional): Функция для обхода категорий, используемая в сценарии.
                                                  По умолчанию `None`.

    Returns:
        List | dict | bool: Результат выполнения сценария.

    Example:
        >>> # Предполагается, что 'supplier_instance', 'd_instance', 'my_scenario_data', 'my_crawl_function' определены
        >>> # result = await run_scenario(supplier_instance, d_instance, my_scenario_data, 'MyCategoryScenario', my_crawl_function)
        >>> # print(f'Результат выполнения сценария: {result}')
    """

    list_products_in_category: List[str] | None = crawl_category_function(d, s.locator.category)
    f: ProductFields = None


    scenario_url: str = scenario.get('url')
    if not scenario_url:
        logger.error(f'В сценарии "{scenario_name}" отсутствует URL-адрес.')
        return False

    if not d.get_url(scenario_url):
        logger.error(f'Ошибка перехода по URL сценария: {scenario_url} для сценария "{scenario_name}".')
        ...
        return False

    # Извлечение списка товаров в категории
    # Если crawl_category_function предоставлена, используем ее, иначе стандартную функцию поставщика
    if crawl_category_function:
        # Предполагается, что crawl_category_function принимает d и s.locators
        list_products_in_category = await crawl_category_function(d, s.locators)
    else:
        # Предполагается, что s.related_modules.get_list_products_in_category ожидает d и s.locators
        list_products_in_category = await s.related_modules.get_list_products_in_category(d, s.locators)

    # Если в категории нет товаров (или они еще не загрузились)
    if not list_products_in_category:
        logger.warning(f'Список товаров не собран со страницы категории. Возможно, пустая категория: {d.current_url}')
        return False

    for url in list_products_in_category:
        if not d.get_url(url):
            logger.error(f'Ошибка перехода на страницу товара по URL: {url}')
            continue  # Ошибка при переходе на страницу. Пропускаем.

        # Захват полей страницы товара
        # Предполагается, что s.related_modules.grab_page является асинхронной функцией
        f = await s.related_modules.grab_page(s)
        if not f:
            logger.error(f'Не удалось собрать поля товара со страницы: {url}')
            continue

        presta_fields_dict, assist_fields_dict = f.presta_fields_dict, f.assist_fields_dict
        try:
            # Создание экземпляра ProductClass
            product = ProductClass(supplier_prefix=s.supplier_prefix, presta_fields_dict=presta_fields_dict)
            # Вставка захваченных данных в PrestaShop
            await insert_grabbed_data_to_prestashop(f)
        except Exception as ex:
            # Попытка извлечь имя товара для логирования
            product_name_for_log = ''
            if product and hasattr(product, 'fields') and 'name' in product.fields and isinstance(product.fields['name'], tuple):
                product_name_for_log = product.fields['name'][1]
            elif product and hasattr(product, 'name'): # Если у ProductClass есть атрибут 'name'
                product_name_for_log = product.name

            logger.error(f'товар "{product_name_for_log}" не может быть сохранен.', ex, exc_info=True)
            continue

    return list_products_in_category # Возвращаем список URL, которые были обработаны


async def insert_grabbed_data_to_prestashop(
    f: ProductFields, coupon_code: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None
) -> bool:
    """
    Функция добавляет товар в PrestaShop.

    Args:
        f (ProductFields): Экземпляр `ProductFields`, содержащий информацию о товаре.
        coupon_code (Optional[str], optional): Необязательный код купона. По умолчанию `None`.
        start_date (Optional[str], optional): Необязательная дата начала акции. По умолчанию `None`.
        end_date (Optional[str], optional): Необязательная дата окончания акции. По умолчанию `None`.

    Returns:
        bool: `True`, если вставка прошла успешно, иначе `False`.

    Example:
        >>> # product_fields_instance = ProductFields(...)
        >>> # success = await insert_grabbed_data_to_prestashop(product_fields_instance, coupon_code='SAVE10')
        >>> # print(f'Вставка товара в PrestaShop {"успешна" if success else "не удалась"}.')
    """
    presta: PrestaShopClass 
    try:
        # Создание экземпляра класса для взаимодействия с PrestaShop API
        presta = PrestaProductAsync() # Использование PrestaProductAsync
        
        return await presta.post_product_data(
            product_id=f.product_id,
            product_name=f.product_name,
            product_category=f.product_category,
            product_price=f.product_price,
            description=f.description,
            coupon_code=coupon_code,
            start_date=start_date,
            end_date=end_date,
        )

    except Exception as ex:
        logger.error('Не удалось вставить данные товара в PrestaShop.', ex, exc_info=True)
        return False
