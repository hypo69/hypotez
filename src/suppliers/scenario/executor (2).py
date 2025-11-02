## \file /src/scenario/executor (2).py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.scenario 
	:platform: Windows, Unix
	:synopsis:

"""


"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""
  
""" module: src.scenario """



"""    Исполнитель сценариеев
@details Функции экзекьютера:
- `run_scenario_files()` - Принимает список файлов сценария. Разбирает список и отдает испонителю файла
- `run_scenario_file()` - разбирает файл сценария на список сценариев и отдает каждый в екзекьютор `run_scenario()` 
- `run_scenario()`  - исполняет сценарий. Типичный сценарий содержит информацию об одной категории товаров. Драйвер переводит URl на страницу категории,
с нее получает ссылки на товары в категории, переходит по каждой из них и отдает граберу конкретного поставщика собрать информацию с полей страницы товара. 
Получив поля функция передает их в обработчик престашоп
- `run_scenarios()` - Добавляет гибкость: я могу собрать список сценариев из разных файлов

@image html executor.png
"""
...

import os
import sys
import requests
import asyncio
import time
from datetime import datetime
from math import log, prod
from pathlib import Path
from typing import Dict, List
...
from src import gs
from src.utils.printer import  pprint, j_loads, j_dumps
from src.product import Product, ProductFields, translate_presta_fields_dict
from src.endpoints.PrestaShop import PrestaShop
from src.db import ProductCampaignsManager
from src.utils.convertors import list2string
from src.logger.logger import logger
from src.logger.exceptions import ProductFieldException


_journal: dict = {'scenario_files':''}
_journal['name'] = timestamp = gs.now


def dump_journal(s, journal:dict):
    """ Журналирование процесса выполнения сценария 
    @param journal `dict`: словарь, хранящий состояние выполнения сценария
    """
    ...
    _journal_file_path = Path(s.supplier_abs_path, '_journal', f"{journal['name']}.json")
    j_dumps(journal, _journal_file_path)
    ...

def run_scenario_files(s, scenario_files_list: List[Path, Path]) -> bool:
    """ 
    Function to run a list of scenario files one after another.

    @param s Supplier instance.
    @param scenario_files_list_paths List of file paths for the JSON scenario files.
    @returns True if all scenarios were executed successfully, else False.

    @details The set of scenarios can be passed via scenario_files_list_paths. If the list of scenarios is not passed,
    it is taken from the default settings of the supplier. For each scenario in the list, the function
    run_scenario_file() will be called, which loads the scenario file in JSON format and executes each scenario using
    the run_scenario() function.

    locator_description If scenario_files_list_paths is not passed, all scenarios from the supplier settings will be executed by default.

    @todo 1. Make logging more detailed.
          2. Implement logic for gathering scenarios after a crash.
          3. If an empty value is allowed in scenario_files_list_paths - execute all scenarios by default.
    """

    scenario_files_list = [scenario_files_list] if isinstance(scenario_files_list, str) else s.scenario_files
    _journal['scenario_files']: dict = {}
    for scenario_file in scenario_files_list:
        #_journal['scenario_files'].update({'scenario_file':scenario_file.name})
        dump_journal(s, _journal)
        if run_scenario_file(s, scenario_file):
            _journal['scenario_files'][scenario_file]['message'] = f"{scenario_file} completed successfully!"
            dump_journal(s, _journal)
            logger.success(f'Scenario {scenario_file} completed successfully!')
        else:
            _journal['scenario_files'][scenario_file]['message'] = f"{scenario_file} FAILED !"
            dump_journal(s, _journal)
            logger.error(f'Scenario {scenario_file} failed to execute!')

    return True

def run_scenario_file (s, scenario_filex:Path | str ) -> bool:
    """
    Loads the scenario from a file.

    @param s Supplier instance.
    @param scenario_file Path to the scenario file.
    @returns True if the scenario was executed successfully, False otherwise.
    @code
    @code
    from pathlib import Path
    
    # Path to the scenario file
    file_path = Path("scenarios", "scenario1.json")

    # Running the scenario
    result = run_scenario_file(supplier_instance, file_path)

    # Checking the result
    if result:
        print("Scenario executed successfully.")
    else:
        print("An error occurred while executing the scenario.")
    @endcode
    """
    logger.info(f'Starting scenario file {str(Path(scenario_filex).namex)}')
    # s.supplier_settings['just_runned_scenario_filename'] = str(Path(scenario_filex).namex)
    # j_dumps(s.supplier_settings, Path(s.supplier_abs_path, f'{s.supplier_prefix}.json'))
    
    scenarios_dict = j_loads(scenario_filex)['scenarios']
    _journal['scenario_files'][Path(scenario_filex).name]: dict = {}

    for scenario_name, scenario in scenarios_dict.items():
        
        s.current_scenario = scenario
        _journal['scenario_files'][Path(scenario_filex).name]:dict = {}
        
        if run_scenario(s, scenario, scenario_name, _journal):
            _journal['scenario_files'][Path(scenario_filex).name].update({scenario_namex:'success'})
            dump_journal(s, _journal)
            #s.supplier_settings['runned_scenario'].append(scenario_namex)
            logger.success(f'Last executed scenario: {scenario_name}')
            ...
        else:
            _journal['scenario_files'][Path(scenario_filex).name].update({scenario_namex:'failed'})
            dump_journal(s, _journal)
            logger.critical(f"""
            Scenario {scenario} 
            {str(Path(scenario_filex).namex)}
            interrupted with an error
            """)

    return True

def run_scenarios(s, scenarios: List[dict, dict] = None, _journal = None) -> List | dict | None:
    """
    Function to execute a list of scenarios (NOT FILES).

    @param scenarios Accepts a list of scenarios or a single scenario as a dictionary.
                     The run_scenario(s, scenario) function is called to execute scenarios.
    @param s Supplier instance.
    @returns The result of executing the scenarios as a list or dictionary, depending on the input data type,
             or False in case of an error.

    @todo Check the option when no scenarios are specified from all sides. For example, when s.current_scenario
          is not specified and scenarios are not specified.
    """

    if not scenarios:
        scenarios = [s.current_scenario]
        """
        If no scenarios are specified, take them from s.current_scenario.
        @todo Check this option from all sides. For example, when s.current_scenario is not specified and scenarios are not specified.
        """
        
    scenarios = scenarios if isinstance(scenarios, list) else [scenarios]
    res = []
    for scenario in scenarios:
        #_journal['scenario_files'][-1].append(scenario)
        #dump_journal(s, _journal)
        res = run_scenario(s, scenario)
        _journal['scenario_files'][-1][scenario] = str(res)
        dump_journal(s, _journal)
    return res


def run_scenario(s, scenario: dict, scenario_name: str = None, _journal = None) -> List | dict | None:
    """
    Function to execute the received scenario.

    @param s Supplier instance.
    @param scenario Dictionary containing scenario details.
    @param scenario_name Name of the scenario. What is this parameter for? (TODO check the need for scenario_namex).

    @returns The result of executing the scenario.

    @todo Check the need for the scenario_name parameter.

    """
    # 1.
    logger.info(f'Starting scenario: {scenario_name}')
    s.current_scenario = scenario
    d = s.driver
    d.get_url(scenario['url'])
    
    # 2.
    list_products_in_category: list = s.related_modules.get_list_products_in_category(s)

    # No products in the category (or they haven't loaded yet)
    if not list_products_in_category:
        logger.warning('No product list collected from the category page. Possibly an empty category - ', d.current_url)
        return

    # 3.
    for url in list_products_in_category:
        """
        Go to the product url and extract data from the page.
        """
        if not d.get_url(url):
            logger.error(f'Error navigating to product page at: {url}' )
            continue  # <- Error navigating to the page. Skip

        # 4.
        #grabbed_fields = s.related_modules.grab_product_page(s)
        f: ProductFields = asyncio.run(s.related_modules.grab_page(s))
        if not f:
            logger.error(f"""Не удалось собрать поля товара """)
            continue
        
        #presta_fields_dict, assist_fields_dict = f.presta_fields_dict, f.assist_fields_dict
        """
        Gather values of elements from the product page and convert them to ProductFields.
        Attention! The `product_fields` dictionary contains a utility dictionary `assist_fields_dict`.
        It needs to be separated into a separate dictionary.

        locator_description All multilingual fields are gathered using a separate algorithm. The scraper should not deal with translations.
        The value of a multilingual field is entered with the key `1`. For examplex:
        "name":[{"id":"1","value":"text as it was on the site"}]
        Key values must be in quotes - this is due to XML validation.
        """


            
        #asyncio.run(execute_PrestaShop_insert(presta_fields_dict, assist_fields_dict))
        asyncio.run(execute_PrestaShop_insert(f))
        ...

async def execute_PrestaShop_insert_async(f: ProductFields, coupon_code:str = None, start_date:str = None , end_date: str = None) -> bool:
    await execute_PrestaShop_insert(f, coupon_code, start_date, end_date)
    
def execute_PrestaShop_insert(f: ProductFields, coupon_code:str = None, start_date:str = None , end_date: str = None) -> bool:        
    """
    Adds or checks for the existence of a product. Makes sequential connection to the PrestaShop API.

    @param presta_fields_dict Dictionary of product fields for addition.
    @param assist_fields_dict Dictionary of auxiliary fields.

    @return True if the product was successfully added or checked, False in case of an error.

     This is a very bad solution. But this is not a hack, but a check of operability.
    locator_description In this solution, I sequentially connect to the PrestaShop connectors emil-design.com / e-cat.co.il.
    @todo Make multithreading (or asynchronous) here.
    @todo The nose for the caribou.
    """
    ...
    presta_fields_dict, assist_fields_dict = f.presta_fields_dict, f.assist_fields_dict
    
    # 5.1 build API request filter
    reference = presta_fields_dict['reference']
    if not reference:
        logger.critical(f'reference {reference} is invalid. ')
        ...
        raise ProductFieldException
    ...
     #""" @debug """
    def create_debug_files():
        #timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS
        filename_presta = f"{gs.now}_{presta_fields_dict['reference']}_dict_presta.json"
        j_dumps(presta_fields_dict, Path(gs.dir_tmp, filename_presta))
            
        filename_assist = f"{gs.now}_{presta_fields_dict['reference']}_assist_fields.json"
        j_dumps(assist_fields_dict, Path(gs.dir_tmp, filename_assist))
    #create_debug_files()
    ...
    
    search_filter: Dict = {'filter[reference]': '[' + reference + ']'}
    """ For `V3` I can pass the filter as a string `filter[id] = [5]` and as a dictionary `{'filter[id]':'[5]'}`.
    By default, I use a dictionary."""
    display: Dict = {'display': 'full'}
    search_filter.update(display)
   
    ...
    
    # 5.2 check for the presence of the product in the client's database
    """ @todo Bad solution. I'm making too many connections """
    for credentials in gs.presta_credentials:  ## <- I'm working with several clients (emil-design, e-cat, sergey.mymaster)
        """ Connecting to each!!! client in turn. 
        @todo Good only for testing, bad in production """

        presta_client = PrestaShop(credentials)
        logger.info(f"""Presta client: {credentials['api_domain']}""")

        # 5.2.1 Get response from PrestaShop.
        check_prod_presence: None | dict = presta_client.get('products', search_filter = search_filter)
        """ 
        - If the product does not yet exist in the database, an empty value will be returned.  (None)
        - If the product already exists, I get a dictionary of fields and edit the fields if they have changed (price, description, etc.)
        - If there was an error adding the product to PrestaShop, False will be returned.        
        @todo - write the logic for saving price history
        """

        if not check_prod_presence or len(check_prod_presence) == 0:  
            """ An empty response came back from the server. 
            Adding a new product to the client's database """
            
            # 6.1 Translations
            try:
                """ I get a dictionary with all translations of product fields into all client languages """
                client_languages_schema = presta_client.get_languages_schema()
            except Exception as ex:
                logger.error(f"""Не получил  client_languages_schema """, ex)
                """ @todo добавить обработку ситуации """
                ...
            try:
                presta_fields_dict = translate_presta_fields_dict(presta_fields_dict,  client_languages_schema, assist_fields_dict['locale'])   
            except Exception as ex:
                logger.error(f'Error translating product fields', ex)
                """ @todo добавить обработку ситуации """
                ...

            try:
                """ Add a new product to the client's PrestaShop database 
                I get a dictionary with the parameters of the added product in response
                - get a dictionary of fields of the newly added product
                - If there was an error adding the product to PrestaShop, False will be returned"""
                ... 
                
                if 'quantity' in presta_fields_dict:
                    del presta_fields_dict['quantity']
                    """ `quantity` Why can't it be set when adding a new product? """
                if 'link_to_video' in presta_fields_dict:
                    del presta_fields_dict['link_to_video']
                """ Убрал из словаря поля, которые я не заношу в данный момент.
                Поле  'quantity' заполняется позже. Остальные поля в разработке """                    
                ...
                
                response: dict | None = presta_client.add(resource='products', data={'product': presta_fields_dict}, io_format='JSON')
                if not response:
                    logger.debug(f"""Что - то пошло не так""")
                    ...
                    return
                else:
                    new_product_dict = response['products'][0]
                    logger.success(f"""Product successfully added reference: - {new_product_dict['reference']}""")
                ...

            except Exception as ex:
                logger.error(f""" Error adding a new product """, ex)
                ...
                return

            #############################################################################
            #                                                                           #
            #                           IMAGES                                          #
            #                                                                           #
            #############################################################################

            _start_time = int(time.time())
            try:
                pprint (assist_fields_dict['images_urls'])
                additional_images_list: List = list2string( assist_fields_dict['images_urls'])
                default_image_url: list = assist_fields_dict['default_image_url'] if isinstance(assist_fields_dict['default_image_url'], list) else [assist_fields_dict['default_image_url']]                                                                          
                imgs_urls_list: List = default_image_url +  additional_images_list
            except Exception as ex:
                logger.error(f"""Проблема загрузки картинок, 
                             {pprint(assist_fields_dict['default_image_url'])}
                            {pprint(assist_fields_dict['default_image_url'])}
                             """)
                ...
            for img_url in imgs_urls_list:
                
                uploaded_image_dict: dict = presta_client.upload_image('products', new_product_dict['id'], img_url, new_product_dict['reference'])
                #uploaded_image_dict: dict = await presta_client.upload_image_async('products', new_product_dict['id'], img_url, new_product_dict['reference'])
                
                pprint(uploaded_image_dict)
                """ @code
                {
                    'product_id':'int', 
                    'image_id':'int', 
                    'cover':'int', 
                    'position':'int', 
                    'legend':'{dict}'}
            
                @endcode
                """
                if not uploaded_image_dict:
                    logger.error(f"Image did not add\n{assist_fields_dict['default_image_url']}")
                    ...
                logger.warning(f""" ... one image was added in {int(time.time()) - _start_time} seconds """)    
            
            
            """ @debug """
            logger.success(f"""Images successfully uploaded in {int(time.time()) - _start_time} seconds """)
            if os.path.exists(f'{presta_fields_dict["reference"]}_presta_fields_dict.json'):  # remove tmp files
                os.remove(f'{presta_fields_dict["reference"]}_presta_fields_dict.json')
            if os.path.exists(f'{presta_fields_dict["reference"]}_assist_fields_dict.json'):  # remove tmp files
                os.remove(f'{presta_fields_dict["reference"]}_assist_fields_dict.json')
                
            ### ... <- Additional actions with fields. Add logic here
            ...

                
            
        # 8. The product already exists in the PrestaShop db    
        else:

            """ Edit product """
            ### ...   <- Additional actions with fields. Add logic here
            logger.success(f"The product {reference} is already in the client's database")
            """ @todo The product is in the db. Implement editing """
        ...
        
        # 9. coupons
        if coupon_code and start_date and end_date:
            """ добацляю купоны """
            add_coupon(credentials, reference, coupon_code, start_date, end_date)
        
def add_coupon(credentials, reference, coupon_code, start_date, end_date):
    """ Нет модуля - запердоливаю напямуь в бд """
    manager = ProductCampaignsManager(credentials)
    manager.insert_record({
        'reference':reference,
        'coupon_code':coupon_code,
        'campaign_start_date':start_date,
        'campaign_end_date':end_date,
        })
    ...
    

