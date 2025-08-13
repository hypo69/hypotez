# # \file /src/endpoints/prestashop/product_async.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""Asynchronous module for interacting with goods in Prestashop.
=============================================================================
Determines the logic of asynchronous interaction with `Prestashop` goods.
`` `RST
.. Module :: src.endpoints.prestashop.product_async
`` `"""
import json
import os 
import asyncio # Added for asyncio.run in examples
from pathlib import Path
from types import SimpleNamespace
from typing import List, Dict, Any, Optional, Set

# Default imports
import header
from header import __root__
from src import gs

# Asynchronous basic class is used
from src.endpoints.prestashop.api.api_async import PrestaShopAsync 
from src.endpoints.prestashop.product_fields import ProductFields
from src.endpoints.prestashop.utils.dict2xml import dict2xml

from src.utils.xml import save_xml
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.printer import pprint as print
from src.logger.logger import logger

class PrestaProductAsync(PrestaShopAsync):
    """Asynchronous class for managing goods in Prestashop.
    =================================================================
    The class interacts with the API Prestashop to manage goods.
    For the correct operation, a copy of this class should be used
    Like an asynchronous context manager (`async with`)."""

    def __init__(self, api_key: str, api_domain: str, *args: Any, **kwargs: Any) -> None:
        """Initializes the asynchronous object Product.

        Args:
            API_KEY (STR): Key API Prestashop.
            API_Domain (str): domain API Prestashop.
            *Args (ANY): Additional positional arguments for the parent class `Prestashopasync`.
            ** KWARGS (ANY): additional named arguments for the parent class `Prestashopasync`."""
        super().__init__(
            api_key=api_key, 
            api_domain=api_domain,
            *args, 
            **kwargs,
        )

    async def get_product_schema_async(self, resource_id: Optional[str | int] = None, schema: Optional[str] = None) -> dict | None:
        """Asynchronously receives a scheme for the resource of goods from Prestashop.

        Args:
            Resource_id (Optional [Str | Int], Optional): ID of goods resource. By default `none`.
            Schema (Optional [Str], Optional): type of scheme ('Blank', 'synopsis', `none` for complete). 
                                              By default 'Blank'.

        Returns:
            dict | NONE: a scheme for a product resource in the form of a dictionary, or `none` in the case of an error.
        
        Example:
            >>> # async with Prestaproductasync (API_KEY = "KEY", API_Domain = "Domain") As Product_api:
            ... # Schema = AWAIT PRODUCT_API.GET_PRODUCT_SCHEMA_ASYNC (Resource_id = 1, Schema = 'Blank')
            ... # If Schema: Print (Schema)"""
        # The function extracts the product resource scheme
        return await self.get_schema_async(resource='products', resource_id=resource_id, schema=schema)

    async def get_parent_category_async(self, id_category: int) -> Optional[int]:
        """Asynchronously extracts the parental category from Prestashop for the specified category.

        Args:
            ID_Category (int): Categories ID.

        Returns:
            Optional [int]: ID of the parental category or `none`, if the category is not found,
                           It does not have a parent (except for the root), or an error has occurred.
        
        Example:
            >>> # async with Prestaproductasync (API_KEY = "KEY", API_Domain = "Domain") As Product_api:
            ... # Parent_id = Await Product_api.get_part_category_async (5)
            ... # If Parent_id: Print (F'PARENT CATEGORY ID: {PARENT_ID} ')"""
        category_info: Optional[dict] = None
        response_data: Optional[dict] = None
        parent_id_value: Any 

        try:
            response_data = await self.read_async(
                'categories', resource_id=id_category, display='full'
            )
            
            if response_data and 'category' in response_data: 
                category_info = response_data['category']
            elif response_data and 'categories' in response_data and isinstance(response_data['categories'], list) and response_data['categories']:
                category_info = response_data['categories'][0]
                logger.warning(f'API вернул список категорий при запросе по ID {id_category}, использован первый элемент.')
            else:
                logger.error(f'Ответ API не содержит ожидаемых данных для категории ID {id_category}. Ответ: {response_data}')
                return None

            if not category_info or not isinstance(category_info, dict): 
                logger.error(f'Данные категории с ID {id_category} не найдены или имеют неверный формат.')
                return None
            
            parent_id_value = category_info.get('id_parent')
            if parent_id_value is None:
                logger.info(f'Категория ID {id_category} не имеет родителя (id_parent отсутствует).')
                return None
                
            return int(parent_id_value)
        
        except (KeyError, IndexError, TypeError, ValueError) as ex:
            logger.error(f'Ошибка при обработке ответа API для категории ID {id_category}', ex, exc_info=True)
            return None
        except Exception as ex: 
            logger.error(f'Неожиданная ошибка при извлечении категории с ID {id_category}', ex, exc_info=True)
            return None


    async def _add_parent_categories_async(self, f: ProductFields) -> None:
        """Asynchronously calculates and adds all unique parental categories
        For a list of categories ID to the Productfields object.

        Args:
            F (Productfields): Object Productfields to which are added
                               Unique parental categories."""
        seen_ids: Set[int] = {2} 
        initial_categories_copy: List[Dict[str, Any]]
        initial_id_val: Any
        current_search_id: Optional[int] = None
        parent_id: Optional[int] = None

        initial_categories_copy = list(f.additional_categories) 

        for initial_cat_dict in initial_categories_copy:
            if isinstance(initial_cat_dict, dict):
                initial_id_val = initial_cat_dict.get('id')
                if initial_id_val is not None:
                    try:
                        seen_ids.add(int(initial_id_val))
                    except (ValueError, TypeError):
                        logger.warning(f'Не удалось конвертировать начальный ID категории в int: {initial_id_val}. Пропуск.')
            else:
                 logger.warning(f'Элемент в начальном списке категорий не является словарем: {initial_cat_dict}. Пропуск.')
        
        logger.debug(f'Начальные уникальные ID категорий (включая обработанные): {seen_ids}')

        for category_dict_to_process in initial_categories_copy:
            if not isinstance(category_dict_to_process, dict): continue
            
            start_category_id_value: Any = category_dict_to_process.get('id')
            if start_category_id_value is None: continue

            try:
                current_search_id = int(start_category_id_value)
            except (ValueError, TypeError):
                logger.warning(f'Не удалось конвертировать стартовый ID категории {start_category_id_value} в int. Пропуск ветки.')
                continue
            
            if current_search_id <= 2: 
                continue
            
            logger.debug(f'Поиск родителей для стартовой категории ID: {current_search_id}')

            while current_search_id is not None and current_search_id > 2:
                parent_id = await self.get_parent_category_async(current_search_id) 

                if parent_id is not None and parent_id > 2: 
                    if parent_id not in seen_ids:
                        logger.debug(f'Найден новый родитель ID: {parent_id}. Добавление.')
                        f.additional_category_append(parent_id) 
                        seen_ids.add(parent_id)
                    else:
                        logger.debug(f'Родитель ID {parent_id} уже присутствует/добавлен.')
                    
                    current_search_id = parent_id 
                else:
                    logger.debug(f'Завершение поиска родителей для ветки (родитель: {parent_id}, текущий ID для поиска был: {current_search_id})')
                    break 
        
        logger.debug(f'Финальный набор уникальных ID категорий: {seen_ids}')


    async def get_product_async(self, id_product: int, **kwargs: Any) -> dict | None:
        """Asynchronously returns a dictionary of goods from the Prestashop store.

        Args:
            ID_PRODUCT (int): product ID in Prestashop.
            ** KWARGS (ANY): Additional parameters for API request (for example, `Display`).

        Returns:
            dict | NONE: a dictionary containing goods (for example, `{'product': {'id': ..., 'name': ...}` `),
                         Or `none` in case of error or if the product is not found.
        
        Example:
            >>> # async with Prestaproductasync (API_KEY = "KEY", API_Domain = "Domain") As Product_api:
            ... # Product_DATA = AWAIT PRODUCT_API.GET_PRODUCT_ASYNC (1, Display = 'Full')
            ... # If Product_Data: Product (Product_Data.geta ('Product', {}). Get ('name'))"""
        # The function extracts goods
        return await self.read_async(resource='products', resource_id=id_product, **kwargs)


    async def add_new_product_async(self, f: ProductFields) -> SimpleNamespace | dict:
        """Asynchronously adds a new product to Prestashop.

        The function is transformed by an object `productfields` into a dictionary of format` Prestashop`
        And sends him to the API Prestashop.

        Args:
            F (Productfields): Productfields Data Class copy containing product information.

        Returns:
            Simplenamespace | dict: `simplenamespace` with the details of the added goods in case of success,
                                    Or an empty dictionary (`}`) with an error.
        
        Example:
            >>> # Product_fields = Productfields (Name = 'New async Product', ...)
            >>> # async with Prestaproductasync (API_KEY = "KEY", API_Domain = "Domain") As Product_api:
            ... # Result = Await Product_api.add_new_product_async (Product_fields)
            ... # If ISINSTANCE (Result, Simplenamespace): Print (F'ADDEDDUCT ID: {Result.id} ')"""
        presta_product_dict: dict
        payload_for_api: str | dict 
        response: Optional[dict] = None
        added_product_ns: SimpleNamespace
        # Upload_image_Task: Optional [asyncio.task] = None # is made, because Not used directly

        f.additional_category_append(f.id_category_default)
        await self._add_parent_categories_async(f) 

        product_data_dict: dict = f.to_dict()
        
        if self.data_format == 'JSON':
            presta_product_dict = {'product': product_data_dict}
            payload_for_api = presta_product_dict 
        elif self.data_format == 'XML':
            presta_product_dict = {'prestashop': {'product': product_data_dict}}
            # Dict2xml expects Dict, which it converts into XML a line.
            # If Dict2xml returns bytes, they will need to be decoded before saving or sending,
            # But usually such utilities are returned by StR. Payload_for_api should be str or dict.
            xml_payload_str: str = dict2xml(presta_product_dict) 
            payload_for_api = xml_payload_str 
            
            xml_save_path: Path = gs.path.endpoints / 'emil' / '_experiments' / f'{gs.now}_presta_product_add_request.xml'
            # Save_xml expects bytes or str. If Dict2xml has returned STR, then everything is OK.
            save_xml(xml_payload_str, xml_save_path) 
            logger.debug(f'XML запрос для добавления товара сохранен в: {xml_save_path}')
        else:
            logger.error(f'Неподдерживаемый data_format: {self.data_format} для добавления товара.')
            return {}
        
        # Here Self.Client should already be initialized if `async with
        response = await self.create_async('products', data=payload_for_api)
        
        if response and 'product' in response and isinstance(response['product'], dict):
            added_product_info: dict = response['product']
            added_product_ns = j_loads_ns(added_product_info) 
            ... 
            try:
                img_upload_response: Optional[dict] = None # The initialization of the variable
                if f.local_image_path: 
                    img_upload_response = await self.create_binary_async( 
                        resource_path=f'images/products/{added_product_ns.id}', 
                        file_path=str(f.local_image_path), 
                        file_name_in_request=f'{gs.now.strftime("%Y%m%d%H%M%S")}.png', 
                    )
                    if not img_upload_response:
                        logger.warning(f'Не удалось загрузить локальное изображение для товара ID {added_product_ns.id}')
                
                elif f.default_image_url:
                    img_upload_response = await self.upload_image_from_url_async(
                        resource_images_path='images/products', 
                        entity_id=int(added_product_ns.id),
                        img_url=f.default_image_url
                    )
                    if not img_upload_response:
                        logger.warning(f'Не удалось загрузить изображение по URL для товара ID {added_product_ns.id}')
                
                print(added_product_ns) 
                logger.info(f'Товар успешно добавлен. Детали: {str(added_product_ns)}')
                return added_product_ns
                    
            except (KeyError, TypeError, AttributeError) as ex: 
                logger.error(f'Ошибка при обработке ответа от сервера или загрузке изображения для товара', ex, exc_info=True)
                return {}
        else: 
            log_data_dict_display: dict
            if self.data_format == 'JSON': 
                log_data_dict_display = presta_product_dict
            else: 
                log_data_dict_display = {'product_data_sent_to_xml_converter': product_data_dict}

            print(print_data=log_data_dict_display, text_color='yellow')
            logger.error(
                f"Ошибка при добавлении товара. Отправляемые данные (до 최종 преобразования в XML/JSON): {j_dumps(log_data_dict_display)}",
                exc_info=False, 
            )
            if response: 
                 logger.error(f"Получен неожиданный или ошибочный ответ от API: {j_dumps(response)}")
            return {}

# ##################################################   EXAMPLES ##################################################

async def example_add_new_product_async() -> None:
    """Asynchronous example for adding goods to Prestashop."""
    example_data_fields: ProductFields 
    result: SimpleNamespace | dict

    class ConfigExample: 
        API_KEY: str = os.environ.get('PRESTA_API_KEY', 'YOUR_API_KEY_EXAMPLE') 
        API_DOMAIN: str = os.environ.get('PRESTA_API_DOMAIN', 'YOUR_API_DOMAIN_EXAMPLE')
        
    if ConfigExample.API_KEY == 'YOUR_API_KEY_EXAMPLE' or ConfigExample.API_DOMAIN == 'YOUR_API_DOMAIN_EXAMPLE':
        logger.warning("API_KEY и API_DOMAIN не настроены для асинхронного примера. Используются значения по умолчанию.")
        # Return # can be interrupted if there is no configuration

    # Using Async with to initialize the client
    async with PrestaProductAsync(api_key=ConfigExample.API_KEY, api_domain=ConfigExample.API_DOMAIN, data_format_init='JSON') as p_async:
        example_data_fields = ProductFields(
            id_manufacturer=1, 
            id_supplier=1, 
            id_category_default=2, 
            name=[{'language_id': 1, 'value': f'Async Test Product {gs.now.strftime("%H%M%S")}'}],
            description=[{'language_id': 1, 'value': 'Async description here.'}],
            description_short=[{'language_id': 1, 'value': 'Async short desc.'}],
            link_rewrite=[{'language_id': 1, 'value': f'async-test-product-{gs.now.strftime("%H%M%S")}'}],
            reference=f'ASYNC_REF_{gs.now.strftime("%H%M%S")}',
            price='19.99',
            quantity=10,
            active='1',
            available_for_order='1',
            state='1', 
        )
        example_data_fields.additional_category_append(3) 
        example_data_fields.additional_category_append(4) 

        result = await p_async.add_new_product_async(example_data_fields)
        
        if isinstance(result, SimpleNamespace):
            logger.info(f"Асинхронно добавлен товар ID: {result.id}, Reference: {getattr(result, 'reference', 'N/A')}") # getttr for security
            print(result) 
        else:
            logger.error(f"Ошибка при асинхронном добавлении товара. Ответ: {result}")
    

async def example_get_product_async(id_product: int, **kwargs: Any) -> None:
    """Asynchronous example of obtaining information about the product."""
    product_data_response: dict | None 

    class ConfigExample: 
        API_KEY: str = os.environ.get('PRESTA_API_KEY_ASYNC', 'YOUR_API_KEY_EXAMPLE')
        API_DOMAIN: str = os.environ.get('PRESTA_API_DOMAIN_ASYNC', 'YOUR_API_DOMAIN_EXAMPLE')

    if ConfigExample.API_KEY == 'YOUR_API_KEY_EXAMPLE' or ConfigExample.API_DOMAIN == 'YOUR_API_DOMAIN_EXAMPLE':
        logger.warning("API_KEY и API_DOMAIN не настроены для асинхронного примера. Используются значения по умолчанию.")
        # return

    # Using Async with to initialize the client
    async with PrestaProductAsync(api_key=ConfigExample.API_KEY, api_domain=ConfigExample.API_DOMAIN) as p_async:
        product_data_response = await p_async.get_product_async(id_product, **kwargs)
        
        actual_product_details: Optional[dict] = None
        if product_data_response and 'product' in product_data_response: 
            actual_product_details = product_data_response['product']
        elif product_data_response: 
            logger.warning(f"Неожиданная структура ответа для товара ID {id_product}: {product_data_response}")
            actual_product_details = product_data_response 
        else:
            logger.error(f"Товар с ID {id_product} не найден или произошла ошибка API.")

        if actual_product_details:
            print(actual_product_details) 
            # output_path: Path = gs.path.endpoints / 'emil' / '_experiments' / f'presta_async_response_product_{id_product}_{gs.now.strftime("%Y%m%d%H%M%S")}.json'
            # j_dumps(actual_product_details, output_path)
            # logger.info (f "Data data ID {id_product} are saved in {output_path}")
    

if __name__ == '__main__':
    """"""
    class ConfigMain:
        API_KEY: str = os.environ.get('PRESTA_API_KEY_ASYNC', 'YOUR_API_KEY_EXAMPLE')
        API_DOMAIN: str = os.environ.get('PRESTA_API_DOMAIN_ASYNC', 'YOUR_DOMAIN_EXAMPLE')

    if ConfigMain.API_KEY == 'YOUR_API_KEY_EXAMPLE' or ConfigMain.API_DOMAIN == 'YOUR_DOMAIN_EXAMPLE':
        logger.error("Переменные окружения PRESTA_API_KEY_ASYNC и PRESTA_API_DOMAIN_ASYNC не установлены.")
        logger.info("Пожалуйста, установите их или измените значения в ConfigMain в __main__ блоке.")
    else:
        try:
            # asyncio.run(example_add_new_product_async())
            asyncio.run(example_get_product_async(2191, display='[id,name,reference,price]')) 
            
        except KeyboardInterrupt:
            logger.info('Выполнение программы прервано пользователем (Ctrl+C).')
        except Exception as main_ex:
            logger.error('Произошла непредвиденная ошибка при выполнении __main__', main_ex, exc_info=True)
    ...
