## \file /src/endpoints/prestashop/product_async.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Асинхронный модуль для взаимодействия с товарами в PrestaShop.
==============================================================
Определяет логику асинхронного взаимодействия с товарами `Prestashop`.
```rst
.. module:: src.endpoints.prestashop.product_async
```
"""
import json
import os 
import asyncio # Added for asyncio.run in examples
from pathlib import Path
from types import SimpleNamespace
from typing import List, Dict, Any, Optional, Set

# Импорты по умолчанию
import header
from header import __root__
from src import gs

# Используется асинхронный базовый класс
from src.endpoints.prestashop.api.api_async import PrestaShopAsync 
from src.endpoints.prestashop.product_fields import ProductFields
from src.endpoints.prestashop.utils.dict2xml import dict2xml

from src.utils.xml import save_xml
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.printer import pprint as print
from src.logger.logger import logger

class PrestaProductAsync(PrestaShopAsync):
    """
    Асинхронный класс для управления товарами в PrestaShop.
    =======================================================
    Класс взаимодействует с API PrestaShop для управления товарами.
    Для корректной работы экземпляр этого класса должен использоваться
    как асинхронный контекстный менеджер (`async with`).
    """

    def __init__(self, api_key: str, api_domain: str, *args: Any, **kwargs: Any) -> None:
        """
        Инициализирует асинхронный объект Product.

        Args:
            api_key (str): Ключ API PrestaShop.
            api_domain (str): Домен API PrestaShop.
            *args (Any): Дополнительные позиционные аргументы для родительского класса `PrestaShopAsync`.
            **kwargs (Any): Дополнительные именованные аргументы для родительского класса `PrestaShopAsync`.
        """
        super().__init__(
            api_key=api_key, 
            api_domain=api_domain,
            *args, 
            **kwargs,
        )

    async def get_product_schema_async(self, resource_id: Optional[str | int] = None, schema: Optional[str] = None) -> dict | None:
        """
        Асинхронно получает схему для ресурса товара из PrestaShop.

        Args:
            resource_id (Optional[str | int], optional): ID ресурса товара. По умолчанию `None`.
            schema (Optional[str], optional): Тип схемы ('blank', 'synopsis', `None` для полной). 
                                              По умолчанию 'blank'.

        Returns:
            dict | None: Схема для ресурса товара в виде словаря, или `None` в случае ошибки.
        
        Example:
            >>> # async with PrestaProductAsync(api_key="key", api_domain="domain") as product_api:
            ... #     schema = await product_api.get_product_schema_async(resource_id=1, schema='blank')
            ... #     if schema: print(schema)
        """
        # Функция извлекает схему ресурса товара
        return await self.get_schema_async(resource='products', resource_id=resource_id, schema=schema)

    async def get_parent_category_async(self, id_category: int) -> Optional[int]:
        """
        Асинхронно извлекает родительскую категорию из PrestaShop для указанной категории.

        Args:
            id_category (int): ID категории.

        Returns:
            Optional[int]: ID родительской категории или `None`, если категория не найдена,
                           не имеет родителя (кроме корневых), или произошла ошибка.
        
        Example:
            >>> # async with PrestaProductAsync(api_key="key", api_domain="domain") as product_api:
            ... #     parent_id = await product_api.get_parent_category_async(5)
            ... #     if parent_id: print(f'Parent category ID: {parent_id}')
        """
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
        """
        Асинхронно вычисляет и добавляет все уникальные родительские категории
        для списка ID категорий в объект ProductFields.

        Args:
            f (ProductFields): Объект ProductFields, в который добавляются
                               уникальные родительские категории.
        """
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
        """
        Асинхронно возвращает словарь полей товара из магазина Prestashop.

        Args:
            id_product (int): ID товара в Prestashop.
            **kwargs (Any): Дополнительные параметры для API запроса (например, `display`).

        Returns:
            dict | None: Словарь, содержащий данные товара (например, `{'product': {'id': ..., 'name': ...}}`),
                         или `None` в случае ошибки или если товар не найден.
        
        Example:
            >>> # async with PrestaProductAsync(api_key="key", api_domain="domain") as product_api:
            ... #     product_data = await product_api.get_product_async(1, display='full')
            ... #     if product_data: print(product_data.get('product', {}).get('name'))
        """
        # Функция извлекает данные товара
        return await self.read_async(resource='products', resource_id=id_product, **kwargs)


    async def add_new_product_async(self, f: ProductFields) -> SimpleNamespace | dict:
        """
        Асинхронно добавляет новый товар в PrestaShop.

        Функция преобразует объект `ProductFields` в словарь формата `Prestashop`
        и отправляет его в API PrestaShop.

        Args:
            f (ProductFields): Экземпляр дата-класса ProductFields, содержащий информацию о товаре.

        Returns:
            SimpleNamespace | dict: `SimpleNamespace` с деталями добавленного товара в случае успеха,
                                    или пустой словарь (`{}`) при ошибке.
        
        Example:
            >>> # product_fields = ProductFields(name='New Async Product', ...)
            >>> # async with PrestaProductAsync(api_key="key", api_domain="domain") as product_api:
            ... #     result = await product_api.add_new_product_async(product_fields)
            ... #     if isinstance(result, SimpleNamespace): print(f'Added product ID: {result.id}')
        """
        presta_product_dict: dict
        payload_for_api: str | dict 
        response: Optional[dict] = None
        added_product_ns: SimpleNamespace
        # upload_image_task: Optional[asyncio.Task] = None # Закомментировано, т.к. не используется напрямую

        f.additional_category_append(f.id_category_default)
        await self._add_parent_categories_async(f) 

        product_data_dict: dict = f.to_dict()
        
        if self.data_format == 'JSON':
            presta_product_dict = {'product': product_data_dict}
            payload_for_api = presta_product_dict 
        elif self.data_format == 'XML':
            presta_product_dict = {'prestashop': {'product': product_data_dict}}
            # dict2xml ожидает dict, который он преобразует в XML строку.
            # Если dict2xml возвращает bytes, их нужно будет декодировать перед сохранением или отправкой,
            # но обычно такие утилиты возвращают str. payload_for_api должен быть str или dict.
            xml_payload_str: str = dict2xml(presta_product_dict) 
            payload_for_api = xml_payload_str 
            
            xml_save_path: Path = gs.path.endpoints / 'emil' / '_experiments' / f'{gs.now}_presta_product_add_request.xml'
            # save_xml ожидает bytes или str. Если dict2xml вернул str, то все ок.
            save_xml(xml_payload_str, xml_save_path) 
            logger.debug(f'XML запрос для добавления товара сохранен в: {xml_save_path}')
        else:
            logger.error(f'Неподдерживаемый data_format: {self.data_format} для добавления товара.')
            return {}
        
        # Здесь self.client должен быть уже инициализирован, если используется `async with`
        response = await self.create_async('products', data=payload_for_api)
        
        if response and 'product' in response and isinstance(response['product'], dict):
            added_product_info: dict = response['product']
            added_product_ns = j_loads_ns(added_product_info) 
            ... 
            try:
                img_upload_response: Optional[dict] = None # Инициализация переменной
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
    """Асинхронный пример для добавления товара в Prestashop."""
    example_data_fields: ProductFields 
    result: SimpleNamespace | dict

    class ConfigExample: 
        API_KEY: str = os.environ.get('PRESTA_API_KEY', 'YOUR_API_KEY_EXAMPLE') 
        API_DOMAIN: str = os.environ.get('PRESTA_API_DOMAIN', 'YOUR_API_DOMAIN_EXAMPLE')
        
    if ConfigExample.API_KEY == 'YOUR_API_KEY_EXAMPLE' or ConfigExample.API_DOMAIN == 'YOUR_API_DOMAIN_EXAMPLE':
        logger.warning("API_KEY и API_DOMAIN не настроены для асинхронного примера. Используются значения по умолчанию.")
        # return # Можно прервать, если нет конфигурации

    # ИСПОЛЬЗОВАНИЕ ASYNC WITH ДЛЯ ИНИЦИАЛИЗАЦИИ КЛИЕНТА
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
            logger.info(f"Асинхронно добавлен товар ID: {result.id}, Reference: {getattr(result, 'reference', 'N/A')}") # getattr для безопасности
            print(result) 
        else:
            logger.error(f"Ошибка при асинхронном добавлении товара. Ответ: {result}")
    

async def example_get_product_async(id_product: int, **kwargs: Any) -> None:
    """Асинхронный пример получения информации о товаре."""
    product_data_response: dict | None 

    class ConfigExample: 
        API_KEY: str = os.environ.get('PRESTA_API_KEY_ASYNC', 'YOUR_API_KEY_EXAMPLE')
        API_DOMAIN: str = os.environ.get('PRESTA_API_DOMAIN_ASYNC', 'YOUR_API_DOMAIN_EXAMPLE')

    if ConfigExample.API_KEY == 'YOUR_API_KEY_EXAMPLE' or ConfigExample.API_DOMAIN == 'YOUR_API_DOMAIN_EXAMPLE':
        logger.warning("API_KEY и API_DOMAIN не настроены для асинхронного примера. Используются значения по умолчанию.")
        # return

    # ИСПОЛЬЗОВАНИЕ ASYNC WITH ДЛЯ ИНИЦИАЛИЗАЦИИ КЛИЕНТА
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
            # logger.info(f"Данные товара ID {id_product} сохранены в {output_path}")
    

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
