# # \file /src/endpoints/prestashop/product.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""Module for interacting with goods in Prestashop.
====================================================================
Determines the logic of interaction with the goods `Prestashop`.
`` `RST
.. Module :: src.endpoints.prestashop.product
`` `"""
import json
from pathlib import Path
from types import SimpleNamespace
from typing import List, Dict, Any, Optional, Set

import header
from src import gs

from src.endpoints.prestashop.api.api import PrestaShop 
from src.endpoints.prestashop.product_fields import ProductFields
from src.endpoints.prestashop.utils.dict2xml import dict2xml

from src.utils.xml import save_xml
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.printer import pprint as print
from src.logger.logger import logger

class PrestaProduct(PrestaShop):
    """Class for managing goods in Prestashop.
    ============================================================"""

    def __init__(self, api_key: str, api_domain: str, *args: Any, **kwargs: Any):
        """Initializes the Product object.

        Args:
            API_KEY (STR): Key API Prestashop.
            API_Domain (str): domain API Prestashop.
            *Args (ANY): Additional positional arguments for the parent class.
            ** KWARGS (ANY): additional named arguments for the parental class."""
        super().__init__(
            api_key = api_key, 
            api_domain = api_domain,
            *args,
            **kwargs,
        )

    def get_product_schema(self, resource_id: Optional[str | int] = None, schema: Optional[str] = None) -> dict:
        """He receives a scheme for a resource `Product` from Prestashop.

        Args:
            Resource_id (Optional [Str | Int], Optional): ID of goods resource. By default None.
            Schema (Optional [Str], Optional): type of scheme. By default 'Blank'.
                - Blank is an empty resource template: all fields are present, but without values. Usually used to create a new object.
                - Synopsis is a minimum set of fields: only compulsory fields and a short structure. Suitable for quick review.
                - Null / not to transmit the parameter returns the full scheme of the resource with all possible fields, types and restrictions.

        Returns:
            DICT: Scheme for the resource of goods."""
        return self.get_schema(resource='products', resource_id=resource_id, schema=schema)

    def get_parent_category(self, id_category: int) -> Optional[int]:
        """Removes parental categories from Prestashop for the specified category of recursively.

        Args:
            ID_Category (int): Categories ID.

        Returns:
            Optional [int]: ID of the parental category (int) or None, if the category is not found,
                           It does not have a parent (except for the root), or an error has occurred."""
        category_response: Optional[dict] = None
        try:
            response_data: dict = self.read(
                'categories', resource_id=id_category, display='full', data_format='JSON'
            )
            if response_data and 'categories' in response_data and response_data['categories']:
                category_response = response_data['categories'][0]
            else:
                logger.error(f'Ответ API не содержит ожидаемых данных для категории ID {id_category}.')
                return None

            if not category_response: # Additional check, although the previous one should cover
                logger.error(f'Категория с ID {id_category} не найдена.')
                return None

            return int(category_response['id_parent'])
        except (KeyError, IndexError, TypeError, ValueError) as ex:
            logger.error(f'Ошибка при обработке ответа API для категории ID {id_category}: ', ex)
            return None
        except Exception as ex:
            logger.error(f'Ошибка при извлечении категории с ID {id_category}: ', ex)
            return None


    def _add_parent_categories(self, f: ProductFields) -> None:
        """Calculates and adds all unique parental categories
        For a list of categories ID to the Productfields object.

        Args:
            F (Productfields): Object Productfields to which are added
                               Unique parental categories."""
        # 1. Creating a set for tracking all categories ID (initial and added),
        # inclusive of a spray category ID 2 by default.
        seen_ids: Set[int] = {2}
        # Announcement of variables at the beginning of the function
        initial_categories_copy: List[Dict[str, Any]]
        initial_id_val: Any
        current_search_id: Optional[int] = None
        parent_id: Optional[int] = None

        # Filling out many IDs from * initial * list F.Additional_categories
        # A copy iteration to avoid problems if F.Additional_category_Append changes the list
        initial_categories_copy = list(f.additional_categories)

        for initial_cat_dict in initial_categories_copy:
            # Checking that this is a dictionary and a key 'id'
            if isinstance(initial_cat_dict, dict):
                initial_id_val = initial_cat_dict.get('id')
                if initial_id_val is not None: # A clear check for NONE is important if 0 can be ID
                    try:
                        # Converting in Int and adding to many
                        seen_ids.add(int(initial_id_val))
                    except (ValueError, TypeError):
                        logger.warning(f"Не удалось конвертировать начальный ID категории в int: {initial_id_val}. Пропуск.")
            else:
                 logger.warning(f"Элемент в начальном списке категорий не является словарем: {initial_cat_dict}. Пропуск.")

        logger.debug(f"Начальные уникальные ID категорий (включая обработанные): {seen_ids}")

        # 2. Iteration in the initial categories for the search for their parents
        # A copy for security is used again
        for _c in initial_categories_copy:
             # Safe ID extraction for the start of parents search
            if not isinstance(_c, dict): continue # Passing non-volumes
            start_cat_id_val: Any = _c.get('id')
            if start_cat_id_val is None: continue # Pass if not ID

            try:
                # Current Category ID for which the parent is performed
                current_search_id = int(start_cat_id_val)
            except (ValueError, TypeError):
                logger.warning(f"Не удалось конвертировать стартовый ID категории {start_cat_id_val} в int. Пропуск ветки.")
                continue

            # Passing root categories or incorrect ID
            if current_search_id <= 2: # ID 2 - usually root, ID <2 - incorrect
                continue

            logger.debug(f"Поиск родителей для стартовой категории ID: {current_search_id}")

            # 3. Lifting by hierarchy
            while current_search_id is not None and current_search_id > 2: # Until the root has reached
                parent_id = self.get_parent_category(current_search_id)

                # Check, whether the parent was found and is he the root
                if parent_id is not None and parent_id > 2:
                    # 4. Checking for duplicate before adding
                    if parent_id not in seen_ids:
                        logger.debug(f"Найден новый родитель ID: {parent_id}. Добавление.")
                        # 5. Add to a parent (it is assumed that the method itself creates dict {'id': parent_id})
                        f.additional_category_append(parent_id)
                        # 6. Adding ID new parent to many tracking
                        seen_ids.add(parent_id)
                    else:
                        # Duplicate found, just logging and crossing up the hierarchy
                        logger.debug(f"Родитель ID {parent_id} уже присутствует/добавлен.")

                    # The transition to the next parent up the hierarchy
                    current_search_id = parent_id
                else:
                    # The parent was not found or is the root - the completion of the rise for this branch
                    logger.debug(f"Завершение поиска родителей для ветки (родитель: {parent_id}, текущий ID для поиска был: {current_search_id})")
                    break # While exit for current Start_cat_id_val
            # The end of the While cycle
        # The end of the cycle for

        logger.debug(f"Финальный набор уникальных ID категорий: {seen_ids}")
        # F.Additional_categories object now contains the initial categories + unique parental categories

    def get_product(self, id_product: int, **kwargs: Any) -> dict:
        """Returns a dictionary of goods from the Prestashop store.

        Args:
            ID_PRODUCT (int): ID field value in the `Product` Prestashop table.
            ** KWARGS (ANY): Additional parameters for API request.

        Returns:
            dict: a dictionary containing product data, for example:
                  `{'Product': {'Id': 1, 'Name': 'Test Product', ...}}}
                  Or an empty dictionary in case of an error."""
        kwargs['data_format'] = 'JSON' # Providing JSON format for consistency
        return self.read(resource='products', resource_id=id_product, **kwargs)

    async def add_new_product_async(self, f: ProductFields) -> SimpleNamespace | dict:
        """Adds a new product to Prestashop.

        The function is transformed by an object `productfields` into a dictionary of format` Prestashop`
        And sends him to the API Prestashop.

        Args:
            F (Productfields): Productfields Data Class copy containing product information.

        Returns:
            Simplenamespace | DICT: Returns the object `simplenamespace` representing the details of the added
                                    goods from the API Prestashop in case of success, or an empty dictionary (`}`),
                                    If the operation has failed."""
        presta_product_dict: dict
        presta_product_xml: bytes
        response: Optional[dict]
        added_product_ns: SimpleNamespace

        # ID_Category_DEFULT addition in the `Additional_categories field to search for its parental categories
        f.additional_category_append(f.id_category_default)

        self._add_parent_categories(f)

        presta_product_dict = {'prestashop': 
                                     {'attrs':
                                      {'xmlns:xlink': 'http://www.w3.org/1999/xlink'}, 
                                      'value':
                                      {'products':[ # API expects a list of goods, even for one
                                        f.to_dict()
                                         ]}
                                      }
                                     }

        presta_product_xml = dict2xml(presta_product_dict)
        
        # Conservation of XML before sending for debugging
        save_xml(presta_product_xml, gs.path.endpoints / 'emil' / '_experiments' / f'{gs.now}_presta_product_add_request.xml')
        
        # --- Todo make an asynchronous call API ---
        response = await self.create_async('products', data=presta_product_xml)
        
        if response and 'products' in response and response['products']:
            # We assume that the API returns a list with one element for the created product
            added_product_ns = j_loads_ns(response['products'][0])
            try:
                # F.reference = response ['product'] ['reference'] if isinstance (response ['product'] ['reference'], str) else int (response ['product'] ['reference']) # proceeding The code is saved
                if f.local_image_path: 
                    _ = self.create_binary( # The result is Create_binary is not used, assignment to _
                        resource=f'products/{added_product_ns.id}',
                        file_path=f.local_image_path,
                        file_name=f'{f.reference}.png',
                    )
                    
                    print(added_product_ns)
                    # Logging information about the added product
                    logger.info(f'Товар добавлен. Детали: {str(added_product_ns)}')
                    return added_product_ns

                # elif f.default_image_url:
                # await self.upload_image_from_url_async('products', added_product_ns.id, f.default_image_url)
                    
                # print(added_product_ns)
                # # Logging information about the added product
                # Logger.info (Fetovar added. Details: {str (aded_product_ns)} ')
                # return added_product_ns
                # else:
                # # If there are no images, the goods are added anyway
                # print(added_product_ns)
                # Logger.info (Fetovar added (without image). Details: {str (adeded_product_ns)} ')
                # return added_product_ns
                    
            except (KeyError, TypeError) as ex:
                logger.error(f'Ошибка при обработке ответа от сервера или загрузке изображения: {ex}', ex, exc_info=True)
                return {}
        else:
            
            print(print_data=presta_product_dict, text_color='yellow')
            # Logging error for adding goods
            logger.error(
                f"Ошибка при добавлении товара. Отправляемые данные: {json.dumps(presta_product_dict, ensure_ascii=False, indent=2)}",
                exc_info=True, # Exc_info = True is usually used with the transfer of an exception object
            )
            # If Response is not None, but does not contain expected data
            if response:
                 logger.error(f"Получен неожиданный ответ от API: {json.dumps(response, ensure_ascii=False, indent=2)}")
            return {}

# ##################################################   EXAMPLES ##################################################


def example_add_new_product() -> None:
    """An example to add goods to Prestashop"""
    # Variables for example
    p: PrestaProduct
    # Schema: Dict # is not used in the current logic of example
    example_data: dict
    presta_product_xml: bytes
    # KWARGS_EXAMPLE: DICT # renamed clarity that this is for an example
    response: Optional[dict]

    # Config definition (it is assumed that config exists and is configured)
    class Config: # Local definition for example, if not imported globally
        API_KEY: str = 'YOUR_API_KEY'
        API_DOMAIN: str = 'YOUR_API_DOMAIN'
        # Set real values or provide config loading

    if Config.API_KEY == 'YOUR_API_KEY': # Default check
        logger.warning("API_KEY и API_DOMAIN не настроены в примере. Используются значения по умолчанию.")
        # Return # can be repacked to interrupt the execution of an example without configuration


    p = PrestaProduct(api_key=Config.API_KEY, api_domain=Config.API_DOMAIN) # Used API_KEY and API_Domain
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEBUG ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # resource_id: int = 2191
    # schema = p.get_product_schema(resource_id = resource_id)
    # j_dumps(schema, gs.path.endpoints / 'emil' / '_experiments' / f'product_schema.{resource_id}_{gs.now}.json')
    # None

    example_data = j_loads(
        gs.path.endpoints / 'emil' / '_experiments' / 'product_schema.2191_250319224027026.json'
    )
    """""" # This comment looks like an artifact, I leave it according to the instructions
    if not example_data:
        logger.error('Файл не существует или неправильный формат файла')
        ...
        return

    presta_product_xml = dict2xml(example_data)
    save_xml(presta_product_xml, gs.path.endpoints / 'emil' / '_experiments' / f'{gs.now}_presta_product.xml')

    # 1. JSON | XML
    kwargs_example = { # Renamed to avoid conflict with ** kwargs functions
        'io_format': 'JSON', # Iley 'XML'
    }

    response = p._exec( # _Exec is a Prestashop method (parental class)
        resource='products',
        method='POST',
        data=example_data if kwargs_example['io_format'] == 'JSON' else presta_product_xml,
        **kwargs_example, # Transfer as named arguments
    )
    # response = p.create('products', data=presta_product_dict  if kwargs_example['io_format'] == 'JSON' else presta_product_xml, **kwargs_example)
    
    # Preservation of the answer
    # output_path = gs.path.endpoints / 'emil' / '_experiments' / f"{gs.now}_presta_response_new_product_added.json"
    # if kwargs_example['io_format'] == 'JSON':
    # j_dumps(response, output_path)
    # else:
    # #
    # # or save as a XML file. XML2DICT is not imported, if necessary, it needs to be imported.
    # # For example, if Response is XML line:
    # # from src.endpoints.prestashop.utils.xml2dict Import XML2DICT # will need import
    # # dict_response = xml2dict(response)
    # # j_dumps(dict_response, output_path)
    # # Or save XML directly:
    # # save_xml(response, gs.path.endpoints / 'emil' / '_experiments' / f"{gs.now}_presta_response_new_product_added.xml")
    # Logger.info ("answer in XML format, to save as JSON requires XML2DICT.")


    print(response)
    ...


def example_get_product(id_product: int, **kwargs: Any) -> None:
    """"""
    p: PrestaProduct = None
    presta_product_data: dict = None

    # Config definition (it is assumed that config exists and is configured)
    class Config: # Local definition for example
        API_KEY: str = 'YOUR_API_KEY'
        API_DOMAIN: str = 'YOUR_API_DOMAIN'
        # Set real values

    if Config.API_KEY == 'YOUR_API_KEY':
        logger.warning("API_KEY и API_DOMAIN не настроены в примере. Используются значения по умолчанию.")
        # return


    p = PrestaProduct(api_key=Config.API_KEY, api_domain=Config.API_DOMAIN)
    # KWARGS for Get_PRODUCT can be transmitted from the outside, for example:
    # kwargs_get = {
    # 'display': 'full', # 'blank', 'synopsis'
    # None
    presta_product_data = p.get_product(id_product, **kwargs) # External transmission kwargs
    
    # The API can return the list of goods, even when requesting ID, although Get_product expects one
    # This behavior depends on the implementation of self.read in Prestashop API
    # If P.Get_PRODUCT always returns DICT {'Product': {...}}, then the extraction of the first element is not needed.
    # Judging by the `response ['products'] [0]` in `Add_new_product`, the API often returns the list.
    # We will clarify that Get_product returns
    # If `self.read` returns {'products': [...]}, then you need to extract:
    # if presta_product_data and 'products' in presta_product_data and isinstance(presta_product_data['products'], list) and presta_product_data['products']:
    # actual_product = presta_product_data['products'][0]
    # else:
    # Actual_product = Presta_product_data # or {} If the structure is not the same

    # Given that get_product just calls self.read, and self.read to Prestashop API usually returns {'Resource_name_Plural': [items ...]}}
    # That, probably, you need to extract the goods from the list.
    # However, the current implementation of Get_product directly returns the result self.read,
    # What could be `{'products': [{'id': ...,}]}`.
    # For consistency, if you need the product itself, not a wrapper:
    
    actual_product_details: Optional[dict] = None
    if presta_product_data and 'products' in presta_product_data and isinstance(presta_product_data['products'], list):
        if presta_product_data['products']:
            actual_product_details = presta_product_data['products'][0]
        else:
            logger.warning(f"Список товаров для ID {id_product} пуст.")
    elif presta_product_data and 'product' in presta_product_data : # If the API returned a single product
         actual_product_details = presta_product_data['product']
    else:
        logger.warning(f"Неожиданная структура ответа для товара ID {id_product}: {presta_product_data}")
        actual_product_details = presta_product_data # We save as it is for debugging

    ...
    j_dumps(
        actual_product_details, gs.path.endpoints / 'emil' / '_experiments' / f'presta_response_product_{id_product}.json'
    )
    ...


if __name__ == '__main__':
    """"""
    # Config definition for __main__ block
    class Config:
        API_KEY: str = os.environ.get('PRESTA_API_KEY', 'YOUR_API_KEY_HERE') # Example load from ENV
        API_DOMAIN: str = os.environ.get('PRESTA_API_DOMAIN', 'YOUR_DOMAIN_HERE')
        # Make sure that these environment variables are installed, or replace the values.
        # Important: OS Import was not removed, as it is needed here. Add it back.
    import os # OS imports here, since it is used in __main__

    if Config.API_KEY == 'YOUR_API_KEY_HERE' or Config.API_DOMAIN == 'YOUR_DOMAIN_HERE':
        logger.error("Переменные окружения PRESTA_API_KEY и PRESTA_API_DOMAIN не установлены.")
        logger.info("Пожалуйста, установите их или измените значения в Config в __main__ блоке.")
    else:
        # example_add_new_product()
        example_get_product(2191) # An example of a call
    ...
