## \file /sandbox/davidka/experiments/8_run_suppliers_scenarios_pydoll.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для запуска сценариев поставщиков
================================================================
Сценарии позволеют получить товары по поставщикам и по категориям


 ```rst
 .. module:: sandbox.davidka.experiments.8_run_suppliers_scenarios_pydoll
 ```
"""
import asyncio
import argparse
from pathlib import Path
from types import SimpleNamespace
from typing import Optional, Dict, Any, List

from pydoll.browser.chrome import Chrome
from pydoll.constants import By
from pydoll.browser.page import Page

import header
from header import __root__
from src import gs

from src.llm.gemini import GoogleGenerativeAi # Unused, but kept
from src.endpoints.prestashop.product import PrestaProduct
from src.endpoints.prestashop.product_fields import ProductFields
from src.utils.file import read_text_file, save_text_file, get_filenames_from_directory
from src.utils.jjson import j_loads, j_loads_ns, j_dumps # j_dumps unused
from src.utils.image import get_image_bytes, get_raw_image_data 
from src.logger.logger import logger


class Config:
    """Класс конфигурации скрипта."""
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    SUPPLIERS_ENDPOINT: Path = __root__ / 'src' / 'suppliers' / 'suppliers_list'
    SCENARIOS_DIR: Path = __root__ / 'SANDBOX' / 'davidka' / 'scenarios'
    # config: SimpleNamespace = j_loads_ns(ENDPOINT / 'davidka.json') #  general config.
    scenarios_files: List[str] = get_filenames_from_directory(SCENARIOS_DIR) # SANDBOX/davidka/scenarios/*.json
    PRESTA_API_KEY: str = gs.credentials.prestashop.store_davidka_net.api_key
    PRESTA_API_DOMAIN: str = gs.credentials.prestashop.store_davidka_net.api_domain
    presta_product: PrestaProduct = PrestaProduct(api_key=PRESTA_API_KEY, api_domain=PRESTA_API_DOMAIN)


async def _fetch_produduct_data_from_product_page(page: 'Page', locator_product: SimpleNamespace) -> ProductFields | None:
    """
    Извлекает данные товара со страницы товара.

    Args:
        page (Page): Объект страницы pydoll, на которой находится информация о товаре.
        locator_product (SimpleNamespace): Объект SimpleNamespace, содержащий локаторы для данных товара.

    Returns:
        ProductFields | None: Объект ProductFields с данными товара в случае успеха, иначе None.
    
    Raises:
        AttributeError: Если локатор не содержит ожидаемых полей 'by' или 'selector'.
        Exception: При других ошибках поиска элементов на странице.
    """
    # Определение стратегии поиска элементов
    strategy: Dict[str, By] = {
        'XPATH': By.XPATH,
        'CSS_SELECTOR': By.CSS_SELECTOR,
    }
    fields: Dict[str, Any]

    try:
        # Асинхронное извлечение данных для каждого поля
        fields = {
            'name': await page.find_element(strategy[locator_product.name.by], locator_product.name.selector),
            'price': await page.find_element(strategy[locator_product.price.by], locator_product.price.selector),
            'id_supplier': locator_product.id_supplier.attr, 
            'description_short': await page.find_element(strategy[locator_product.description_short.by], locator_product.description_short.selector),
            'description': await page.find_element(strategy[locator_product.description.by], locator_product.description.selector),
            'specification': await page.find_element(strategy[locator_product.specification.by], locator_product.specification.selector),
            'default_image_url': await page.find_element(strategy[locator_product.default_image_url.by], locator_product.default_image_url.selector),
        }
        return ProductFields(**fields)
    except AttributeError as ex:
        logger.error('Ошибка атрибута при доступе к локатору товара. Проверьте структуру локатора.', ex, exc_info=True)
        return None
    except Exception as ex:
        logger.error('Не удалось извлечь данные о товаре со страницы.', ex, exc_info=True)
        return None


async def execute_scenario(supplier_prefix: str, scenario: Dict[str, Any]) -> bool:
    """
    Выполняет сценарий для указанного поставщика.

    Args:
        supplier_prefix (str): Префикс поставщика, используемый для поиска конфигурационных файлов.
        scenario (Dict[str, Any]): Словарь с данными сценария, должен содержать ключ 'url'.

    Returns:
        bool: True в случае успешного выполнения, False в случае ошибки.
    """
    supplier_alias: str = supplier_prefix.replace('.', '_').replace('-', '_')
    presta_product_api: PrestaProduct = Config.presta_product
    supplier_config_path: Path
    locators_path: Path
    product_locators: Optional[SimpleNamespace] = None
    category_locators: Optional[SimpleNamespace] = None
    # categories_crawler: Any = None # Изначально было, но не используется. Оставлено закомментированным.

    if 'url' not in scenario:
        logger.debug(f"Сценарий для поставщика '{supplier_alias}' не содержит 'url'. Возможно, это новый поставщик без сценария категорий.")
        return False

    try:
        # # Получение экземпляра грабера для поставщика
        # graber_instance = get_graber_by_supplier_prefix(supplier_prefix)
        # if not graber_instance: # Добавлена проверка, что граббер успешно получен
        #      logger.error(f"Не удалось получить граббер для поставщика: {supplier_alias}")
        #      return False

        supplier_config_path:Path = Config.SUPPLIERS_ENDPOINT / supplier_alias
        locators_path:Path = supplier_config_path / 'locators'
        product_locators:SimpleNamespace = j_loads_ns(locators_path / 'product.json')
        category_locators:SimpleNamespace = j_loads_ns(locators_path / 'category.json')

        if not product_locators or not category_locators:
            logger.error(f"Не удалось загрузить локаторы для поставщика: {supplier_alias}. Проверьте файлы product.json и category.json.")
            return False

    except Exception as ex:
        logger.error(f'Ошибка инициализации для сценария поставщика {supplier_alias}.', ex, exc_info=True)
        ... # Точка останова
        return False

    # Определение стратегии поиска элементов
    strategy_map: Dict[str, By] = {
        'XPATH': By.XPATH,
        'CSS_SELECTOR': By.CSS_SELECTOR,
    }

    async with Chrome() as browser:
        await browser.start()
        page = await browser.get_page()
        await page.go_to(scenario['url'])
        
        # Проверка наличия локатора для ссылок на товары
        if not hasattr(category_locators, 'product_links') or \
           not hasattr(category_locators.product_links, 'by') or \
           not hasattr(category_locators.product_links, 'selector'):
            logger.error(f"Локатор 'product_links' не полностью определен для поставщика {supplier_alias}.")
            return False

        products_urls_webelements_list: List[str] = await page.find_elements(
            strategy_map[category_locators.product_links.by],
            category_locators.product_links.selector
        )

        products_urls_list:list = []

        for webelement in products_urls_webelements_list:
            if not webelement:
                logger.warning(f"Обнаружен пустой элемент для поставщика {supplier_alias} на странице {scenario['url']}.")
                continue
            
            # Получение URL товара из элемента
            product_url: str = webelement.get_attribute(category_locators.product_links.attribute)
            if product_url:
                products_urls_list.append(product_url)
            else:
                logger.warning(f"Не удалось получить URL товара из элемента для поставщика {supplier_alias} на странице {scenario['url']}.")

        ... # Точка останова

        for product_url in products_urls_list:
            if not product_url:
                logger.warning(f"Обнаружен пустой URL товара для поставщика {supplier_alias} на странице {scenario['url']}.")
                continue
            
            protocol:dict = {'https' : 'https:', 'file' : 'file:'}
            url:str = f'{protocol['https']}{product_url}'
            result = await page.go_to(url)

            product_data: Optional[ProductFields] = await _fetch_produduct_data_from_product_page(page, product_locators)
            
            if product_data:
                # Добавление нового товара через API PrestaShop
                result = presta_product_api.add_new_product(product_data)
                if result:
                    logger.info(f"товар {product_data.name} от {supplier_alias} обработан.")
                    continue
                ...

    ... # Точка останова
    return True


async def main(scenario_filename: Optional[str] = None) -> None:
    """
    Основная функция для запуска обработки сценариев.

    Args:
        scenario_filename (Optional[str], optional):
            Путь к конкретному файлу сценария для обработки.
            Может быть абсолютным путем, относительным путем или именем файла,
            который будет искаться в `Config.SCENARIOS_DIR`.
            Если `None`, обрабатываются все файлы из `Config.scenarios_files`.
            По умолчанию `None`.

    Returns:
        None
    """
    ... # Точка останова
    paths_to_process: List[Path] = []
    scenario_data: Dict[str, Any] | List[Dict[str, Any]] | None
    supplier_prefix_from_file: str
    # single_scenario: Dict[str,Any] # Объявляется внутри цикла, если необходимо

    if scenario_filename:
        # Если передан конкретный файл, обрабатываем только его.
        path_candidate: Path = Path(scenario_filename)
        # Проверка, является ли указанный путь существующим файлом
        if path_candidate.is_file():
            paths_to_process.append(path_candidate.resolve())
            logger.info(f"Обработка указанного файла сценария: {paths_to_process[0]}")
        # Проверка, существует ли файл с таким именем в директории сценариев по умолчанию
        elif (Config.SCENARIOS_DIR / path_candidate.name).is_file(): # Используем path_candidate.name для корректного поиска в SCENARIOS_DIR
            paths_to_process.append((Config.SCENARIOS_DIR / path_candidate.name).resolve())
            logger.info(f"Обработка указанного файла сценария из директории по умолчанию: {paths_to_process[0]}")
        else:
            logger.error(f"Файл сценария '{scenario_filename}' не найден ни как абсолютный/относительный путь, ни в директории {Config.SCENARIOS_DIR}.")
            return # Выход, если указанный файл не найден
    else:
        # Если имя файла не передано, обрабатываем все файлы из конфигурации.
        logger.info(f"Обработка всех файлов сценариев из директории: {Config.SCENARIOS_DIR}")
        for fname in Config.scenarios_files:
            paths_to_process.append((Config.SCENARIOS_DIR / fname).resolve())

    if not paths_to_process:
        logger.info("Нет файлов сценариев для обработки.")
        return

    for current_scenario_path in paths_to_process:
        ... # Точка останова
        logger.info(f"Начало обработки файла сценария: {current_scenario_path}")
        # Извлечение сценариев из файла
        scenario_data = j_loads(current_scenario_path)

        if not scenario_data:
            # j_loads уже логирует ошибку, дополнительное сообщение для контекста
            logger.warning(f"Не удалось загрузить или пустой файл сценария: {current_scenario_path}")
            continue

        # Извлечение префикса поставщика из имени файла (без расширения)
        supplier_prefix_from_file = current_scenario_path.stem

        if isinstance(scenario_data, dict):
            # Обработка одного сценария из файла (если файл содержит объект JSON)
            logger.info(f"Обработка одиночного сценария для поставщика '{supplier_prefix_from_file}' из файла {current_scenario_path.name}.")
            await execute_scenario(supplier_prefix=supplier_prefix_from_file,
                                   scenario=scenario_data)
        elif isinstance(scenario_data, list):
            # Обработка списка сценариев из файла (если файл содержит массив JSON)
            logger.info(f"Обработка списка сценариев для поставщика '{supplier_prefix_from_file}' из файла {current_scenario_path.name}.")
            for index, single_scenario in enumerate(scenario_data):
                if isinstance(single_scenario, dict):
                    logger.info(f"Обработка сценария #{index + 1} для поставщика '{supplier_prefix_from_file}'.")
                    await execute_scenario(supplier_prefix=supplier_prefix_from_file,
                                           scenario=single_scenario)
                else:
                    logger.warning(f"Элемент #{index + 1} в списке сценариев файла {current_scenario_path.name} не является словарем: {type(single_scenario)}")
        else:
            logger.warning(f"Неизвестный формат данных в файле сценария {current_scenario_path.name}: {type(scenario_data)}")
        ... # Точка останова
        logger.info(f"Завершение обработки файла сценария: {current_scenario_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Запускает обработку сценариев поставщиков.')
    parser.add_argument(
        '--scenario',
        dest='scenario_filename', # Имя атрибута в args
        type=str,
        default=None,
        help='Опциональный путь к файлу сценария или имя файла в директории сценариев. Если не указан, обрабатываются все сценарии.'
    )
    args = parser.parse_args()

    asyncio.run(main(scenario_filename=args.scenario_filename))

if __name__ == '__main__':
    asyncio.run(main('amazon.json'))
