## \file /src/endpoints/emil/emil_design.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для управления и обработки изображений, а также продвижения в Facebook и PrestaShop. Относится к магазину `emil-design.com`
=================================
Основные возможности:
    - <инструкция для модели gemini:Описание изображений с использованием Gemini AI.>
    - <инструкция для модели gemini:Загрузка описаний товаров в PrestaShop.>
    - ..... <далее, если есть>
Классы:
    `Config` - <инструкция для модели gemini: Дай полное описание и назначение этого класса>
    `EmilDesign` - <инструкция для модели: Дай полное описание и назначение этого класса>

```rst
.. module:: src.endpoints.emil
```
"""
import importlib
import os
import asyncio
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Optional, List, Any
from dataclasses import dataclass, field

import header
from header import __root__

# Internal modules
from src import gs
from src.suppliers.suppliers_list import *
from src.suppliers.get_graber_by_supplier  import get_graber_by_supplier_prefix, get_graber_by_supplier_url
from src.suppliers.graber import Graber
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
from src.webdriver.chrome import Chrome
from src.llm.gemini import GoogleGenerativeAi
from src.llm.openai.model import OpenAIModel
from src.endpoints.prestashop.product import PrestaProduct
from src.endpoints.prestashop.language import PrestaLanguage
from src.endpoints.prestashop.product_fields import ProductFields
from src.endpoints.advertisement.facebook.scenarios.post_message import (
    post_message,
)
from src.utils.file import read_text_file, save_text_file, get_filenames_from_directory

from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.image import get_image_bytes, get_raw_image_data
from src.logger.logger import logger
SupplierInstance:SimpleNamespace = Any

# --- file config.py
class Config:


    ENDPOINT: Path = __root__ /'src' / 'endpoints' / 'emil'
    SUPPLIERS_ENDPOINT: Path = __root__ / 'src' / 'suppliers' / 'suppliers_list'
    config:SimpleNamespace = j_loads_ns(ENDPOINT / 'emil.json')
    GEMINI_API_KEY:str = gs.credentials.gemini.onela.api_key
    PRESTA_API_KEY:str = gs.credentials.prestashop.store_davidka_net.api_key
    PRESTA_DOMAIN:str = gs.credentials.prestashop.store_davidka_net.api_domain
    gemini_model_name:str = config.gemini_model_name
    system_instruction:str = ' ' # <- Это пробел!
    webdriver_window_mode:str = 'headless'
# --- end file config.pt


class EmilDesign:
    """Dataclass for designing and promoting images through various platforms."""

    gemini: Optional[GoogleGenerativeAi] = None
    openai: Optional[OpenAIModel] = None
    product: PrestaProduct = None
    driver: Driver = None

    def __init__(self,
            presta_api_key:Optional[str] = '',
            presta_api_domain:Optional[str] = '',
            gemini_model_name:Optional[str] = '',
            openai_model_name:Optional[str] = '',
            gemini_api_key:Optional[str] = '',
            openai_api_key:Optional[str] = '',
            gemini: Optional[GoogleGenerativeAi] = None, 
            openai: Optional[OpenAIModel] = None,
            system_instruction:str = '', 
            webdriver_window_mode:str = ''
            ):
        """
        Инициализация 
            Args:
                presta_api_key:Optional[str] = '',
                presta_api_domain:Optional[str] = '',
                gemini_model_name:Optional[str] = '',
                openai_model_name:Optional[str] = '',
                gemini_api_key:Optional[str] = '',
                openai_api_key:Optional[str] = '',
                gemini: Optional[GoogleGenerativeAi] = None, 
                openai: Optional[OpenAIModel] = None,
        """
        ...
        self.driver = Driver(Firefox,window_mode=webdriver_window_mode if webdriver_window_mode else Config.webdriver_window_mode)

        if gemini:
            self.gemini = gemini
        else:
            gemini_api_key:str = gemini_api_key if gemini_api_key else Config.GEMINI_API_KEY
            gemini_model_name:str = gemini_model_name if gemini_model_name else Config.gemini_model_name
            system_instruction:str = system_instruction if system_instruction else Config.system_instruction
            if not self._init_gemini(gemini_api_key, gemini_model_name, system_instruction):
                logger.debug('Модель GEMINI не иницаилизирована')

        presta_api_key:str = presta_api_key if presta_api_key else Config.PRESTA_API_KEY
        presta_api_domain:str = presta_api_domain if presta_api_domain else Config.PRESTA_DOMAIN
        if not presta_api_key or not presta_api_domain:
            logger.critical(f'Проверь \nAPI {presta_api_key}\nDomain {presta_api_domain=}')
            return False

        self.product = PrestaProduct(presta_api_key, presta_api_domain )

    def _init_gemini(self, api_key: str, model_name: str, system_instruction: str) -> bool:
        """"""
        try:
            generation_config = dict({'response_mime_type':'application/json'})
            self.gemini = GoogleGenerativeAi(api_key, model_name, generation_config, system_instruction)
            return True
        except Exception as ex:
            logger.error(f'Ошибка иницализации модели!', ex, False)
            return False


    async def process_supplier(self, supplier_prefix:str) -> bool:
        """"""
        ...
        try:
            supplier_path:Path = Config.SUPPLIERS_ENDPOINT / supplier_prefix 
            graber: Graber = get_graber_by_supplier_prefix(self.driver, supplier_prefix)
            scenarios_list: list[dict] = j_loads(Config.SUPPLIERS_ENDPOINT / supplier_prefix / 'scenarios')
            locators_path:Path = supplier_path / 'locators' 
            locator_product:SimpleNamespace = j_loads_ns(locators_path / 'product.json')
            locator_category:SimpleNamespace = j_loads_ns(locators_path / 'category.json')
            categories_crawler:Any = None
            categories_crawler_module_path:str = f"src.suppliers.suppliers_list.{supplier_prefix}.supplier_module"
        except Exception as ex:
            logger.error(f'Непредвиденная ошибка', ex)
            return False

        try:
            categories_crawler = importlib.import_module(categories_crawler_module_path)
        except Exception as ex:
            logger.error(f"Failed to import module `categories_crawler` '{supplier_prefix}'", ex)
            return False
        
        for scenario in scenarios_list:
            self.driver.get_url(scenario.url)

            products_urls_in_category:list = categories_crawler.get_list_products_in_category(self.driver, locator_category)
            for product_url in products_urls_in_category:
                self.driver.get_url(product_url)
                product_fields:ProductFields = await graber.grab_page_async()
                ...

                



    async def process_suppliers_list(self, suppliers_prefixes: str|list) -> bool:
        """
        Process suppliers based on the provided prefix.
        Args:
            suppliers_prefixes (Optional[str | List[str, str]], optional): Prefix for suppliers. Defaults to ''.
        Returns:
            bool: True if processing is successful, False otherwise.
        Raises:
            Exception: If any error occurs during supplier processing.
        """
        
        for supplier_prefix in suppliers_prefixes:
            try:
                await self.process_supplier(supplier_prefix)
            except Exception as ex:
                logger.error(f'Error while processing suppliers: {ex}')
                continue

    def describe_images(
        self,
        lang: str,
        models: dict = {
            'gemini': {'model_name': 'gemini-1.5-flash'},
            'openai': {'model_name': 'gpt-4o-mini', 'assistant_id': 'asst_uDr5aVY3qRByRwt5qFiMDk43'},
        },
    ) -> None:
        """Describe images based on the provided instruction and examples.

        Args:
            lang (str): Language for the description.
            models (dict, optional): Models configuration. Defaults to Gemini and OpenAI models.

        Returns:
            None

        Raises:
            FileNotFoundError: If instruction files are not found.
            Exception: If any error occurs during image processing.

        Example:
            >>> emil = EmilDesign()
            >>> emil.describe_images('he')
        """
        try:
            system_instruction = Path(self.base_path / 'instructions' / f'system_instruction.{lang}.md').read_text(
                encoding='UTF-8'
            )
            prompt = Path(self.base_path / 'instructions' / f'hand_made_furniture.{lang}.md').read_text(
                encoding='UTF-8'
            )
            furniture_categories = (
                Path(self.base_path / 'categories' / 'main_categories_furniture.json')
                .read_text(encoding='UTF-8')
                .replace(r'\n', '')
                .replace(r'\t', '')
            )
            system_instruction += furniture_categories + prompt

            output_json = self.data_path / f'out_{gs.now}_{lang}.json'
            described_images_path = self.data_path / 'described_images.txt'
            described_images: list = read_text_file(described_images_path, as_list=True) or []
            images_dir = self.data_path / 'images' / 'furniture_images'
            images_files_list: list = get_filenames_from_directory(images_dir)
            images_to_process = [
                img for img in images_files_list if str(images_dir / img) not in described_images
            ]

            use_openai: bool = False
            if use_openai:
                self.openai = OpenAIModel(
                    system_instruction=system_instruction,
                    model_name=models['openai']['model_name'],
                    assistant_id=models['openai']['assistant_id'],
                )

            use_gemini: bool = True
            if use_gemini:
                self.gemini = GoogleGenerativeAi(
                    api_key=self.gemini_api,
                    model_name=models['gemini']['model_name'],
                    system_instruction=system_instruction,
                    generation_config={'response_mime_type': 'application/json'},
                )

            for img in images_to_process:
                logger.info(f'Starting process file {img}\n')

                raw_img_data = get_raw_image_data(images_dir / img)
                response = self.gemini.describe_image(image=raw_img_data, mime_type='image/jpeg', prompt=prompt)
                ...
                if not response:
                    logger.debug(f'Failed to get description for {img}')
                    ...
                else:
                    response_dict: dict = (
                        j_loads(response)[0] if isinstance(j_loads(response), list) else j_loads(response)
                    )
                    response_dict['local_image_path'] = str(images_dir / img)
                    j_dumps(response_dict, self.data_path / f'{img}.json')
                    # Список уже обработанных изображений
                    described_images.append(str(images_dir / img))
                    save_text_file(described_images_path, described_images)

                time.sleep(15)  # Задержка между запросами
        except FileNotFoundError as e:
            logger.error(f'Instruction file not found: {e}', exc_info=True)
        except Exception as e:
            logger.error(f'Error while processing image: {e}', exc_info=True)

    async def promote_to_facebook(self) -> None:
        """Promote images and their descriptions to Facebook.

        Args:
            None

        Returns:
            None

        Raises:
            Exception: If any error occurs during Facebook promotion.
        """
        try:
            d = Driver(Chrome)
            d.get_url(r'https://www.facebook.com/groups/1080630957030546')
            messages = j_loads_ns(self.base_path / 'images_descritions_he.json')

            for m in messages:
                message = SimpleNamespace(
                    title=f'{m.parent}\n{m.category}',
                    description=m.description,
                    products=SimpleNamespace(local_image_path=[m.local_image_path]),
                )
                post_message(d, message, without_captions=True)
        except Exception as ex:
            logger.error(f'Error while promoting to Facebook:', ex, exc_info=True)

    def upload_described_products_to_prestashop(
        self, products_list: Optional[List[SimpleNamespace]] = None, id_lang: Optional[int | str] = 2, *args, **kwargs
    ) -> bool:
        """Upload product information to PrestaShop.

        Args:
            products_list (Optional[List[SimpleNamespace]], optional): List of product info. Defaults to None.
            id_lang (Optional[str], optional): Language id for prestasop databases.
            Обычно я назначаю языки в таком порядке 1 - en;2 - he; 3 - ru. 
            Важно проверить порядок якыков целевой базе данных.
            Вот образец кода для получения слопваря языков из конкретной базы данных
            >>import language
            >>lang_class = PrestaLanguage()
            >>print(lang_class.get_languages_schema())


        Returns:
            bool: True if upload succeeds, False otherwise.

        Raises:
            FileNotFoundError: If locales file is not found.
            Exception: If any error occurs during PrestaShop upload.
        """
        try:

            products_files_list: list[str] = get_filenames_from_directory(self.data_path, ext='json')
            products_list: list[SimpleNamespace] = [j_loads_ns(self.data_path / f) for f in products_files_list]
            p: PrestaProduct = PrestaProduct(api_domain=Config.API_DOMAIN , api_key=Config.API_KEY)

            """Важно! При загрузке товаров в PrestaShop, необходимо указать язык, на котором будут отображаться названия и характеристики товара.
            в данном случае, язык по умолчанию - иврит (he = 2), но также можно указать английский (en) или русский (ru)
            индексы могут меняться в зависимости от настроек магазина. Обычно я выставляю индекс `1` для английского, `2` для иврита и `3` для русского.
            таблица с индексами для` emil-design.com` находится в файле `locales.json` в папке `shop_locales`
            """

            lang_ns: SimpleNamespace = j_loads_ns(
                Path(__root__, 'src', 'endpoints', 'emil', 'shop_locales', 'locales.json')
            )
            if isinstance(id_lang, str) and id_lang in ('en','he','ru'):
                id_lang = getattr(lang_ns, id_lang)
            else:
                try:
                    id_lang = int(id_lang)
                except Exception as ex:
                    logger.error(f'Неправильный формат макера языка. ',ex)
                    ...

            for product_ns in products_list:
                f: ProductFields = ProductFields(id_lang)
                f.name = product_ns.name
                f.description = product_ns.description
                f.price = 100.000
                f.wholesale_price = 100.000
                f.id_category_default = product_ns.id_category_default
                f.additional_category_append(product_ns.id_category_parent)
                f.id_supplier = 11366
                f.local_image_path = product_ns.local_image_path
                p.add_new_product(f)
            return True
        except FileNotFoundError as ex:
            logger.error(f'Locales file not found: ',ex, exc_info=True)
            return False
        except Exception as ex:
            logger.error(f'Error while uploading to PrestaShop: ',ex, exc_info=True)
            return False


if __name__ == '__main__':
    emil = EmilDesign()
    suppliers_prefixes_list:list = ['hb']
    asyncio.run(emil.process_suppliers_list(suppliers_prefixes_list))

    # -------------- Другие варианты --------------
    # emil.describe_images(lang='he')
    # emil.upload_described_products_to_prestashop(id_lang = 2)
    # asyncio.run(emil.upload_described_products_to_prestashop_async(lang='he'))
    # emil.describe_images('he')