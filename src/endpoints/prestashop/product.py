## \file /src/endpoints/prestashop/product.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для взаимодействия с товарами в PrestaShop.
======================================================
Определяет логику взаимодействия с товарами `Prestashop`.
```rst
.. module:: src.endopoints.prestashop.product
```
"""
import asyncio
import os
from pathlib import Path
from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import List, Dict, Any, Optional

import header
from src import gs
from src.endpoints.prestashop.api import PrestaShop
from src.endpoints.prestashop.category import PrestaCategory
from src.endpoints.prestashop.product_fields import ProductFields
from src.endpoints.prestashop.utils.dict2xml import dict2xml
from src.endpoints.prestashop.utils.xml2dict import xml2dict

from src.utils.xml import save_xml
from src.utils.file import save_text_file
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.printer import pprint as print
from src.logger.logger import logger
from src import USE_ENV  # <- True - использую переменные окружения, False - использую параметры из keepass


class Config:
    """Configuration class for PrestaShop product settings."""


    MODE: str = 'dev'
    API_DOMAIN: str = ''
    API_KEY: str = ''

    if USE_ENV:
        API_DOMAIN = os.getenv('HOST')
        API_KEY = os.getenv('API_KEY')

    elif MODE == 'dev':
        API_DOMAIN = gs.credentials.presta.client.dev_emil_design.api_domain
        API_KEY = gs.credentials.presta.client.dev_emil_design.api_key

    elif MODE == 'dev8':
        API_DOMAIN = gs.credentials.presta.client.dev8_emil_design.api_domain
        API_KEY = gs.credentials.presta.client.dev8_emil_design.api_key

    else:
        API_DOMAIN = gs.credentials.presta.client.emil_design.api_domain
        API_KEY = gs.credentials.presta.client.emil_design.api_key


class PrestaProduct(PrestaShop):
    """Manipulations with the product.

    Initially, I instruct the grabber to fetch data from the product page,
    and then work with the PrestaShop API.
    """

    def __init__(self, api_key: Optional[str] = '', api_domain: Optional[str] = '', *args, **kwargs) -> None:
        """Initializes a Product object.

        Args:
            api_key (Optional[str], optional): PrestaShop API key. Defaults to ''.
            api_domain (Optional[str], optional): PrestaShop API domain. Defaults to ''.

        Returns:
            None
        """
        super().__init__(
            api_key=api_key if api_key else Config.API_KEY,
            api_domain=api_domain if api_domain else Config.API_DOMAIN,
            *args,
            **kwargs,
        )

    def get_product_schema(self, resource_id: Optional[str | int] = None, schema: Optional[str] = None) -> dict:
        """Get the schema for the product resource from PrestaShop.

        Args:
            resource_id (Optional[str  |  int], optional): The ID of the product resource. Defaults to None.
            schema (Optional[str], optional): The schema type. Defaults to 'blank'.
                - blank	Пустой шаблон ресурса: все поля присутствуют, но без значений. Обычно используется для создания нового объекта.
                - synopsis	Минимальный набор полей: только обязательные поля и краткая структура. Подходит для быстрого обзора.
                - null / не передавать параметр	Возвращает полную схему ресурса со всеми возможными полями, типами и ограничениями.

        Returns:
            dict: The schema for the product resource.
        """
        return self.get_schema(resource='products', resource_id=resource_id, schema=schema)

    def get_parent_category(self, id_category: int) -> Optional[int]:
        """Retrieve parent categories from PrestaShop for a given category recursively.

        Args:
            id_category (int): The category ID.

        Returns:
            Optional[int]: parent category id (int).
        """
        try:
            category_response: dict = self.read(
                'categories', resource_id=id_category, display='full', data_format='JSON'
            )['categories'][0]

            return int(category_response['id_parent'])
        except Exception as ex:
            logger.error(f'Error retrieving category with ID {id_category}: ', ex)
            return

        if not category_response:
            logger.error(f'No category found with ID {id_category}.')
            return


    def _add_parent_categories(self, f: ProductFields) -> None:
        """
        Вычисляет и добавляет все уникальные родительские категории
        для списка ID категорий в объект ProductFields.

        Args:
            f (ProductFields): Объект ProductFields, в который добавляются
                               уникальные родительские категории.
        """

        # 1. Создание множества для отслеживания всех ID категорий (начальных и добавленных)
        seen_ids: Set[int] = set()

        # Заполнение множества ID из *начального* списка f.additional_categories
        # Итерируем по копии, чтобы избежать проблем, если append меняет список
        initial_categories_copy: List[Dict[str, Any]] = list(f.additional_categories)

        for initial_cat_dict in initial_categories_copy:
            # Проверяем, что это словарь и есть ключ 'id'
            if isinstance(initial_cat_dict, dict):
                initial_id_val = initial_cat_dict.get('id')
                if initial_id_val is not None:
                    try:
                        # Конвертируем в int и добавляем в множество
                        seen_ids.add(int(initial_id_val))
                    except (ValueError, TypeError):
                        logger.warning(f"Не удалось конвертировать начальный ID категории в int: {initial_id_val}. Пропуск.")
            else:
                 logger.warning(f"Элемент в начальном списке категорий не является словарем: {initial_cat_dict}. Пропуск.")

        logger.debug(f"Начальные уникальные ID категорий: {seen_ids}")

        # 2. Итерация по начальным категориям для поиска их родителей
        # Снова используем копию для безопасности
        for _c in initial_categories_copy:
             # Безопасное извлечение ID для старта поиска родителей
            if not isinstance(_c, dict): continue # Пропуск не-словарей
            start_cat_id_val = _c.get('id')
            if start_cat_id_val is None: continue # Пропуск, если нет ID

            try:
                # Текущий ID категории, по которому ищем родителя
                current_search_id: int = int(start_cat_id_val)
            except (ValueError, TypeError):
                logger.warning(f"Не удалось конвертировать стартовый ID категории {start_cat_id_val} в int. Пропуск ветки.")
                continue

            # Пропуск корневых категорий или некорректных ID
            if current_search_id <= 2:
                continue

            logger.debug(f"Поиск родителей для стартовой категории ID: {current_search_id}")

            # 3. Подъем по иерархии
            while current_search_id > 2: # Пока не дошли до корня
                parent_id: Optional[int] = self.get_parent_category(current_search_id)

                # Проверка, найден ли родитель и не является ли он корнем
                if parent_id is not None and parent_id > 2:
                    # 4. Проверка на дубликат перед добавлением
                    if parent_id not in seen_ids:
                        logger.debug(f"Найден новый родитель ID: {parent_id}. Добавление.")
                        # 5. Добавление родителя (предполагается, что метод сам создает dict {'id': parent_id})
                        f.additional_category_append(parent_id)
                        # 6. Добавление ID нового родителя в множество отслеживания
                        seen_ids.add(parent_id)
                    else:
                        # Дубликат найден, просто логируем и идем дальше вверх
                        logger.debug(f"Родитель ID {parent_id} уже присутствует/добавлен.")

                    # Переход к следующему родителю вверх по иерархии
                    current_search_id = parent_id
                else:
                    # Родитель не найден или является корнем - завершаем подъем для этой ветки
                    logger.debug(f"Завершение поиска родителей для ветки (родитель: {parent_id})")
                    break # Выход из while для текущей start_cat_id_val

            # Конец цикла while
        # Конец цикла for

        logger.debug(f"Финальный набор уникальных ID категорий: {seen_ids}")
        # Теперь f.additional_categories содержит исходные категории + уникальные родительские

    def get_product(self, id_product: int, **kwards) -> dict:
        """Возваращает словарь полей товара из магазина Prestasop

        Args:
            id_product (int): значение поля ID в таблице `product` Preastashop

        Returns:
            dict:
            {
                'product':
                    {... product fields}
            }
        """
        kwards = {'data_format': 'JSON'}
        return self.read(resource='products', resource_id=id_product, **kwards)

    def add_new_product(self, f: ProductFields) -> dict:
        """Add a new product to PrestaShop.

        Преобразовывает объект `ProducFields` в словарь формата `Prestashop` и отрапавлет его в API Престашоп

        Args:
            f (ProductFields): An instance of the ProductFields data class containing the product information.

        Returns:
            dict: Returns the `ProductFields` object with `id_product` set, if the product was added successfully, `None` otherwise.
        """

        # Дополняю id_category_default в поле `additional_categories` для поиска её родительских категорий
        f.additional_category_append(f.id_category_default)

        self._add_parent_categories(f)

        #schema = self.get_product_schema(resource_id=24, schema='full')

        presta_product_dict: dict = {'prestashop': 
                                     {'attrs':
                                      {'xmlns:xlink': 'http://www.w3.org/1999/xlink'}, 
                                      'value':
                                      {'products':[
                                        f.to_dict()
                                         ]}
                                      }
                                     }

        presta_product_xml:bytes = dict2xml(presta_product_dict)
        #presta_product_xml_str:str = presta_product_xml.decode('utf-8')
        response = self.create('products', data=presta_product_xml)
        
        save_xml(presta_product_xml, gs.path.endpoints / 'emil' / '_experiments' / f'{gs.now}_presta_product.xml')
        
        
        if response:
            added_product_ns: SimpleNamespace = j_loads_ns(response['products'][0])
            ...
            try:
                # f.reference = response['product']['reference'] if isinstance(response['product']['reference'], str) else int(response['product']['reference'])
                if f.local_image_path: 
                    img_data = self.create_binary(
                        resource=f'products/{added_product_ns.id}',
                        file_path=f.local_image_path,
                        file_name=f'{gs.now}.png',
                    )
                    logger.info(f'Product added: /n {print(added_product_ns)}')
                    return added_product_ns
                elif f.default_image_url:
                    self.upload_image_from_url('products', added_product_ns.id, f.default_image_url)
                    logger.info(f'Product added: /n {print(added_product_ns)}')
            except (KeyError, TypeError) as ex:
                logger.error(f'Ошибка при разборе ответа от сервера: {ex}', exc_info=True)
                return {}
        else:
            logger.error(
                f"Ошибка при добавлении товара:\n{print(print_data=presta_product_dict, text_color='yellow')}",
                exc_info=True,
            )
            return {}










# ##################################################   EXAMPLES ##################################################


def example_add_new_product() -> None:
    """Пример для добавления товара в Prestashop"""

    p = PrestaProduct(API_KEY=Config.API_KEY, API_DOMAIN=Config.API_DOMAIN)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEBUG ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # resource_id = 2191
    # schema = p.get_product_schema(resource_id = resource_id)
    # j_dumps(schema, gs.path.endpoints / 'emil' / '_experiments' / f'product_schema.{resource_id}_{gs.now}.json')
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    example_data: dict = j_loads(
        gs.path.endpoints / 'emil' / '_experiments' / 'product_schema.2191_250319224027026.json'
    )  # <- XML like
    """"""
    if not example_data:
        logger.error(f'Файл не существует или неправильный формат файла')
        ...
        return

    presta_product_xml = dict2xml(example_data)  # <- XML
    save_xml(presta_product_xml, gs.path.endpoints / 'emil' / '_experiments' / f'{gs.now}_presta_product.xml')

    # 1. JSON | XML
    kwards: dict = {
        'io_format': 'JSON',
    }

    response = p._exec(
        resource='products',
        method='POST',
        data=example_data if kwards['io_format'] == 'JSON' else presta_product_xml,
        **kwards,
    )
    # response = p.create('products', data=presta_product_dict  if kwards['io_format'] == 'JSON' else presta_product_xml, **kwards)
    # j_dumps(response if kwards['io_format'] == 'JSON' else xml2dict(response), gs.path.endpoints / 'emil' / '_experiments' / f"{gs.now}_presta_response_new_product_added.json")

    print(response)
    ...


def example_get_product(id_product: int, **kwards) -> None:
    """"""

    p = PrestaProduct(API_KEY=Config.API_KEY, API_DOMAIN=Config.API_DOMAIN)
    # kwards: dict = {
    #     'data_format': 'JSON',
    #     'display': 'full',
    #     'schema': 'blank',
    # }
    presta_product = p.get_product(id_product, **kwards)
    presta_product = presta_product[0] if isinstance(presta_product, list) else presta_product
    ...
    j_dumps(
        presta_product, gs.path.endpoints / 'emil' / '_experiments' / f'presta_response_product_{id_product}.json'
    )
    ...


if __name__ == '__main__':
    """"""
    #example_add_new_product()
    example_get_product(2191)
    ...