### **Анализ кода модуля `product.py`**

## Качество кода:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код разбит на классы и функции, что облегчает его понимание и поддержку.
    - Используются аннотации типов, что улучшает читаемость и помогает в отладке.
    - Присутствует базовая структура логирования.
- **Минусы**:
    - Не все функции и классы имеют подробные docstring-и, что затрудняет понимание их назначения и использования.
    - В коде встречаются неконсистентные подходы к форматированию и стилю (например, использование `Config.POST_FORMAT` вместо константы).
    - Есть дублирование кода (например, `kwards = {'data_format': 'JSON'}` встречается дважды в `get_product`).
    - Не все переменные аннотированы типами.
    - Некоторые комментарии отсутствуют или неинформативны.

## Рекомендации по улучшению:
- Дополнить docstring-и для всех функций, классов и методов, включая подробное описание аргументов, возвращаемых значений и возможных исключений.
- Привести код в соответствие со стандартами PEP8, включая пробелы вокруг операторов и именование переменных.
- Устранить дублирование кода, вынеся повторяющиеся блоки в отдельные функции или переменные.
- Использовать константы вместо прямого указания значений в коде (например, для `data_format`).
- Добавить больше информативных комментариев, объясняющих сложные участки кода и логику работы.
- Перевести все комментарии и docstring-и на русский язык.
- Исправить опечатки и неточности в комментариях и docstring-ах.
- Использовать `logger.error` с передачей исключения `ex` и `exc_info=True` для более полной информации об ошибках.
- Избавиться от не нужных строк `kwards = {'data_format': 'JSON'}`
- Обеспечить консистентность в использовании кавычек (использовать одинарные кавычки).
- Аннотировать все переменные типами.

## Оптимизированный код:

```python
                ## \file /src/endpoints/prestashop/product.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для взаимодействия с товарами в PrestaShop.
======================================================
Определяет логику взаимодействия с товарами в проекте.
"""
import asyncio
import os
from dataclasses import dataclass, field
# from re import U
from types import SimpleNamespace
from typing import List, Dict, Any, Optional

import header
from src import gs
from src.endpoints.prestashop.api import PrestaShop
from src.endpoints.prestashop.category import PrestaCategory
from src.endpoints.prestashop.product_fields import ProductFields
from src.endpoints.prestashop.utils.xml_json_convertor import dict2xml, xml2dict, presta_fields_to_xml

from src.utils.xml import save_xml
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.printer import pprint as print
from src.logger.logger import logger
from src import USE_ENV  # <- True - использую переменные окружения, False - использую параметры из keepass


class Config:
    """
    Конфигурационный класс для настроек продуктов PrestaShop.
    """

    # 1. Конфигурация API
    USE_ENV: bool = False

    MODE: str = 'dev'
    POST_FORMAT: str = 'XML'
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
    """
    Класс для управления товарами в PrestaShop.

    Изначально, граббер собирает данные со страницы товара,
    а затем происходит взаимодействие с API PrestaShop.
    """

    def __init__(self, api_key: Optional[str] = '', api_domain: Optional[str] = '', *args, **kwargs) -> None:
        """
        Инициализирует объект Product.

        Args:
            api_key (Optional[str], optional): PrestaShop API ключ. По умолчанию ''.
            api_domain (Optional[str], optional): PrestaShop API домен. По умолчанию ''.

        Returns:
            None
        """
        super().__init__(
            api_key=api_key if api_key else Config.API_KEY,
            api_domain=api_domain if api_domain else Config.API_DOMAIN,
            *args,
            **kwargs,
        )

    def get_product_schema(self, resource_id: Optional[str | int] = None, schema: Optional[str] = 'blank') -> dict:
        """
        Получает схему ресурса продукта из PrestaShop.

        Args:
            resource_id (Optional[str | int], optional): ID ресурса продукта. По умолчанию None.
            schema (Optional[str], optional): Тип схемы. По умолчанию 'blank'.

        Returns:
            dict: Схема ресурса продукта.
        """
        return self.get_schema(resource='products', resource_id=resource_id, schema=schema, display='full')

    def get_parent_category(self, id_category: int) -> Optional[int]:
        """
        Рекурсивно извлекает родительские категории из PrestaShop для заданной категории.

        Args:
            id_category (int): ID категории.

        Returns:
            Optional[int]: ID родительской категории (int).
        """
        try:
            category_response: dict = self.read(
                'categories', resource_id=id_category, display='full', data_format='JSON'
            )['categories'][0]

            return int(category_response['id_parent'])
        except Exception as ex:
            logger.error(f'Ошибка при получении категории с ID {id_category}: ', ex, exc_info=True)
            return None

        if not category_response:
            logger.error(f'Категория с ID {id_category} не найдена.')
            return None

    def _add_parent_categories(self, f: ProductFields) -> None:
        """
        Вычисляет и добавляет все родительские категории для списка ID категорий к объекту ProductFields.

        Args:
            f (ProductFields): Объект ProductFields для добавления родительских категорий.
        """
        for _c in f.additional_categories:
            cat_id: int = int(_c['id'])  # {'id':'value'}
            if cat_id in (1, 2):  # <-- корневые категории prestashop Здесь можно добавить другие фильтры
                continue

            while cat_id > 2:
                cat_id: Optional[int] = self.get_parent_category(cat_id)
                if cat_id:
                    f.additional_category_append(cat_id)
                else:
                    break

    def get_product(self, id_product: int, **kwards) -> dict:
        """
        Возвращает словарь полей товара из магазина Prestasop

        Args:
            id_product (int): значение поля ID в таблице `product` Preastashop

        Returns:
            dict:
            {
                'product':
                    {... product fields}
            }
        """
        kwards: dict = {'data_format': 'JSON'}
        return self.read(resource='products', resource_id=id_product, **kwards)

    def add_new_product(self, f: ProductFields) -> dict | None:
        """
        Добавляет новый продукт в PrestaShop.

        Преобразовывает объект `ProducFields` в словарь формата `Prestashop` и отрапавлет его в API Престашоп

        Args:
            f (ProductFields): Экземпляр класса ProductFields, содержащий информацию о продукте.

        Returns:
            dict: Возвращает объект `ProductFields` с установленным `id_product`, если продукт был успешно добавлен, иначе `None`.
        """

        # Дополняю id_category_default в поле `additional_categories` для поиска её родительских категорий
        f.additional_category_append(f.id_category_default)

        self._add_parent_categories(f)

        presta_product_dict: dict = f.to_dict()

        ...
        kwards: dict = {
            'data_format': Config.POST_FORMAT,
            'language': 2,
        }

        """ XML"""
        if Config.POST_FORMAT == 'XML':
            # Convert the dictionary to XML format for PrestaShop.
            xml_data: str = presta_fields_to_xml({'product': presta_product_dict})
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEBUG ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
            save_xml(xml_data, gs.path.endpoints / 'emil' / '_experiments' / f'{gs.now}_presta_product.xml')
            kwards['data_format'] = 'XML'
            response = self.create('products', data=xml_data, **kwards)
        else:  # elif post_format == 'JSON':
            response = self.create('products', data={'product': presta_product_dict}, **kwards)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEBUG ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
        j_dumps(
            response,
            gs.path.endpoints / 'emil' / '_experiments' / f'{gs.now}_presta_response_new_product_added.json',
        )

        # Upload the product image to PrestaShop.
        if response:
            added_product_ns: SimpleNamespace = j_loads_ns(response)
            added_product_ns = added_product_ns.product
            ...
            try:
                # f.reference = response['product']['reference'] if isinstance(response['product']['reference'], str) else int(response['product']['reference'])
                img_data = self.create_binary(
                    resource=f'products/{added_product_ns.id}',
                    file_path=f.local_image_path,
                    file_name=f'{gs.now}.png',
                )

                logger.info(f'Product added: /n {print(added_product_ns)}')
                return f
            except (KeyError, TypeError) as ex:
                logger.error(f'Ошибка при разборе ответа от сервера: {ex}', ex, exc_info=True)
                return None
        else:
            logger.error(
                f"Ошибка при добавлении товара:\\n{print(print_data=presta_product_dict, text_color='yellow')}",
                exc_info=True,
            )
            return None


# ##################################################   EXAMPLES ##################################################


def example_add_new_product() -> None:
    """Пример для добавления товара в Prestashop"""

    p = PrestaProduct(API_KEY=Config.API_KEY, API_DOMAIN=Config.API_DOMAIN)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEBUG ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
    # resource_id = 2191
    # schema = p.get_product_schema(resource_id = resource_id)
    # j_dumps(schema, gs.path.endpoints / 'emil' / '_experiments' / f'product_schema.{resource_id}_{gs.now}.json')
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\

    example_data: dict = j_loads(
        gs.path.endpoints / 'emil' / '_experiments' / 'product_schema.2191_250319224027026.json'
    )  # <- XML like
    """"""
    if not example_data:
        logger.error(f'Файл не существует или неправильный формат файла')
        ...
        return

    presta_product_xml: str = presta_fields_to_xml(example_data)  # <- XML
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
    """ """

    p = PrestaProduct(API_KEY=Config.API_KEY, API_DOMAIN=Config.API_DOMAIN)
    kwards: dict = {
        'data_format': 'JSON',
        'display': 'full',
        'schema': 'blank',
    }
    presta_product: dict = p.get_product(id_product, **kwards)
    presta_product = presta_product[0] if isinstance(presta_product, list) else presta_product
    ...
    j_dumps(
        presta_product, gs.path.endpoints / 'emil' / '_experiments' / f'presta_response_product_{id_product}.json'
    )
    ...


if __name__ == '__main__':
    """ """
    # example_add_new_product()
    example_get_product(2191)
    ...