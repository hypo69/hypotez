### **Анализ кода модуля `src.endpoints.prestashop.product`**

## Качество кода:

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Использование классов для конфигурации и представления данных.
    - Четкое разделение ответственности между классами.
    - Использование `logger` для логирования.
- **Минусы**:
    - Неполная документация функций и классов.
    - Использование смешанного стиля именования переменных и функций.
    - Отсутствие обработки исключений во всех необходимых местах.
    - Не везде используются аннотации типов.
    - Много закомментированного кода, который нужно удалить.

## Рекомендации по улучшению:

1.  **Документация**:
    - Добавить подробные docstring для всех классов, функций и методов, используя формат, указанный в инструкции.
    - Перевести все комментарии и docstring на русский язык.
    - Описать назначение каждого модуля в начале файла.

2.  **Обработка исключений**:
    - Добавить обработку исключений во все места, где это необходимо, с использованием `logger.error` для логирования ошибок.
    - Использовать `ex` вместо `e` в блоках `except`.

3.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных и параметров функций.

4.  **Форматирование**:
    - Исправить форматирование кода в соответствии со стандартами PEP8.
    - Использовать только одинарные кавычки.
    - Добавить пробелы вокруг операторов присваивания.

5.  **Использование `j_loads` и `j_dumps`**:
    - Убедиться, что для чтения JSON-файлов используется `j_loads` или `j_loads_ns`, а для записи - `j_dumps`.

6.  **Удаление неиспользуемого кода**:
    - Удалить весь закомментированный код и неиспользуемые переменные.

7. **Логирование**:
    - Всегда используй модуль `logger` из `src.logger.logger`.
    - Ошибки должны логироваться с использованием `logger.error`.

8. **Использование `webdriver`**:
    - Если в коде используется `webdriver`, убедиться, что он импортирован из модуля `src.webdriver` и используется в соответствии с инструкциями.

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
    Конфигурационный класс для настроек продукта PrestaShop.
    """

    # 1. Конфигурация API
    USE_ENV: bool = False

    MODE: str = 'dev'
    POST_FORMAT = 'XML'
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

    Изначально предполагает получение данных о товаре,
    а затем взаимодействие с API PrestaShop.
    """

    def __init__(self, api_key: Optional[str] = '', api_domain: Optional[str] = '', *args, **kwargs) -> None:
        """
        Инициализирует объект Product.

        Args:
            api_key (Optional[str], optional): Ключ API PrestaShop. Defaults to ''.
            api_domain (Optional[str], optional): Домен API PrestaShop. Defaults to ''.

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
            resource_id (Optional[str | int], optional): ID ресурса продукта. Defaults to None.
            schema (Optional[str], optional): Тип схемы. Defaults to 'blank'.

        Returns:
            dict: Схема ресурса продукта.
        """
        return self.get_schema(resource='products', resource_id=resource_id, schema=schema, display='full')

    def get_parent_category(self, id_category: int) -> Optional[int]:
        """
        Рекурсивно извлекает родительские категории из PrestaShop для данной категории.

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

    def _add_parent_categories(self, f: ProductFields) -> None:
        """
        Вычисляет и добавляет все родительские категории для списка ID категорий в объект ProductFields.

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

    def get_product(self, id_product: int, **kwargs) -> dict:
        """
        Возвращает словарь полей товара из магазина PrestaShop.

        Args:
            id_product (int): Значение поля ID в таблице `product` PrestaShop.

        Returns:
            dict:
            {
                'product':
                    {... product fields}
            }
        """
        kwargs = {'data_format': 'JSON'}
        kwargs = {'data_format': 'JSON'}
        return self.read(resource='products', resource_id=id_product, **kwargs)

    def add_new_product(self, f: ProductFields) -> dict:
        """
        Добавляет новый продукт в PrestaShop.

        Преобразовывает объект `ProductFields` в словарь формата `Prestashop` и отправляет его в API Престашоп

        Args:
            f (ProductFields): Экземпляр класса ProductFields, содержащий информацию о продукте.

        Returns:
            dict: Возвращает объект `ProductFields` с установленным `id_product`, если продукт был успешно добавлен, иначе `None`.
        """

        # Дополняю id_category_default в поле `additional_categories` для поиска её родительских категорий
        f.additional_category_append(f.id_category_default)

        self._add_parent_categories(f)

        presta_product_dict: dict = f.to_dict()

        kwards = {
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
                logger.error(f'Ошибка при разборе ответа от сервера: {ex}', exc_info=True)
                return {}
        else:
            logger.error(
                f"Ошибка при добавлении товара:\\n{print(print_data=presta_product_dict, text_color='yellow')}",
                exc_info=True,
            )
            return {}


# ##################################################   EXAMPLES ##################################################


def example_add_new_product() -> None:
    """
    Пример добавления товара в Prestashop.
    """

    p = PrestaProduct(API_KEY=Config.API_KEY, API_DOMAIN=Config.API_DOMAIN)

    example_data: dict = j_loads(
        gs.path.endpoints / 'emil' / '_experiments' / 'product_schema.2191_250319224027026.json'
    )  # <- XML like

    if not example_data:
        logger.error('Файл не существует или неправильный формат файла')
        return

    presta_product_xml = presta_fields_to_xml(example_data)  # <- XML
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

    print(response)


def example_get_product(id_product: int, **kwargs) -> None:
    """
    Пример получения товара из Prestashop.
    """

    p = PrestaProduct(API_KEY=Config.API_KEY, API_DOMAIN=Config.API_DOMAIN)
    kwards: dict = {
        'data_format': 'JSON',
        'display': 'full',
        'schema': 'blank',
    }
    presta_product = p.get_product(id_product, **kwards)
    presta_product = presta_product[0] if isinstance(presta_product, list) else presta_product

    j_dumps(
        presta_product, gs.path.endpoints / 'emil' / '_experiments' / f'presta_response_product_{id_product}.json'
    )


if __name__ == '__main__':
    """
    Пример использования.
    """
    example_get_product(2191)