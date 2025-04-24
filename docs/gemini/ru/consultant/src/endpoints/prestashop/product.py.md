### **Анализ кода модуля `src.endpoints.prestashop.product`**

## Качество кода:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и разбит на логические блоки.
  - Используются аннотации типов.
  - Присутствует логирование ошибок и отладочная информация.
  - Используются dataclasses для представления данных.
- **Минусы**:
  - Не все функции и классы имеют docstring.
  - Есть участки кода, закомментированные или содержащие `...`.
  - Используется `Union` вместо `|` в аннотациях типов.
  - Не везде используется `j_loads` и `j_dumps` для работы с JSON.
  - Отсутствуют примеры использования в docstring.

## Рекомендации по улучшению:

1. **Документация**:
   - Добавить docstring ко всем классам и функциям, включая описание аргументов, возвращаемых значений и возможных исключений.
   - Добавить примеры использования в docstring для демонстрации работы функций.
   - Перевести все docstring на русский язык.
2. **Использование `j_loads` и `j_dumps`**:
   - Заменить стандартные `open` и `json.load` на `j_loads` для чтения JSON файлов.
   - Использовать `j_dumps` для записи JSON файлов.
3. **Аннотации типов**:
   - Заменить `Union` на `|` в аннотациях типов.
   - Убедиться, что все переменные аннотированы типами.
4. **Обработка исключений**:
   - Использовать `ex` вместо `e` в блоках обработки исключений.
   - Добавить логирование ошибок с использованием `logger.error` во всех блоках `except`.
5. **Конфигурация**:
   - Рассмотреть возможность вынесения конфигурационных параметров в отдельный файл или класс.
6. **Удаление неиспользуемого кода**:
   - Удалить закомментированные участки кода и `...`, если они не несут полезной информации.
7. **Стиль кода**:
   - Следовать стандартам PEP8 для форматирования кода.
   - Использовать осмысленные имена переменных и функций.
8. **Логирование**:
   - Уточнить сообщения логирования, чтобы они были более информативными.
9. **Комментарии**:
   - Избегать неясных формулировок в комментариях, таких как "получаем" или "делаем". Вместо этого использовать более точные описания: "проверяем", "отправляем", "выполняем".

## Оптимизированный код:

```python
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
from typing import List, Dict, Any, Optional, Set

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
    """
    Конфигурационный класс для настроек товаров PrestaShop.
    """

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
    """
    Класс для работы с товарами PrestaShop.

    Изначально грабер собирает данные со страницы товара,
    затем происходит взаимодействие с API PrestaShop.
    """

    def __init__(self, api_key: Optional[str] = '', api_domain: Optional[str] = '', *args, **kwargs) -> None:
        """
        Инициализирует объект Product.

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
        """
        Получает схему ресурса товара из PrestaShop.

        Args:
            resource_id (Optional[str | int], optional): ID ресурса товара. По умолчанию None.
            schema (Optional[str], optional): Тип схемы. По умолчанию 'blank'.
                - blank: Пустой шаблон ресурса: все поля присутствуют, но без значений. Обычно используется для создания нового объекта.
                - synopsis: Минимальный набор полей: только обязательные поля и краткая структура. Подходит для быстрого обзора.
                - null / не передавать параметр: Возвращает полную схему ресурса со всеми возможными полями, типами и ограничениями.

        Returns:
            dict: Схема ресурса товара.
        """
        # Функция возвращает схему ресурса товара
        return self.get_schema(resource='products', resource_id=resource_id, schema=schema)

    def get_parent_category(self, id_category: int) -> Optional[int]:
        """
        Извлекает родительские категории из PrestaShop для заданной категории рекурсивно.

        Args:
            id_category (int): ID категории.

        Returns:
            Optional[int]: ID родительской категории (int).
        """
        try:
            # Функция выполняет запрос к API для получения информации о категории
            category_response: dict = self.read(
                'categories', resource_id=id_category, display='full', data_format='JSON'
            )['categories'][0]
            # Функция возвращает ID родительской категории
            return int(category_response['id_parent'])
        except Exception as ex:
            # Логгирование ошибки при извлечении категории
            logger.error(f'Ошибка при получении категории с ID {id_category}: ', ex, exc_info=True)
            return None

        if not category_response:
            logger.error(f'Категория с ID {id_category} не найдена.')
            return None

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
                    except (ValueError, TypeError) as ex:
                        logger.warning(f"Не удалось конвертировать начальный ID категории в int: {initial_id_val}. Пропуск. {ex}")
            else:
                logger.warning(f"Элемент в начальном списке категорий не является словарем: {initial_cat_dict}. Пропуск.")

        logger.debug(f"Начальные уникальные ID категорий: {seen_ids}")

        # 2. Итерация по начальным категориям для поиска их родителей
        # Снова используем копию для безопасности
        for _c in initial_categories_copy:
            # Безопасное извлечение ID для старта поиска родителей
            if not isinstance(_c, dict):
                continue  # Пропуск не-словарей
            start_cat_id_val = _c.get('id')
            if start_cat_id_val is None:
                continue  # Пропуск, если нет ID

            try:
                # Текущий ID категории, по которому ищем родителя
                current_search_id: int = int(start_cat_id_val)
            except (ValueError, TypeError) as ex:
                logger.warning(
                    f"Не удалось конвертировать стартовый ID категории {start_cat_id_val} в int. Пропуск ветки. {ex}"
                )
                continue

            # Пропуск корневых категорий или некорректных ID
            if current_search_id <= 2:
                continue

            logger.debug(f"Поиск родителей для стартовой категории ID: {current_search_id}")

            # 3. Подъем по иерархии
            while current_search_id > 2:  # Пока не дошли до корня
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
                    break  # Выход из while для текущей start_cat_id_val

            # Конец цикла while
        # Конец цикла for

        logger.debug(f"Финальный набор уникальных ID категорий: {seen_ids}")
        # Теперь f.additional_categories содержит исходные категории + уникальные родительские

    def get_product(self, id_product: int, **kwargs) -> dict:
        """
        Возвращает словарь полей товара из магазина PrestaShop.

        Args:
            id_product (int): Значение поля ID в таблице `product` PrestaShop.

        Returns:
            dict: Словарь с полями товара.
            {
                'product':
                    {... product fields}
            }
        """
        kwargs = {'data_format': 'JSON'}
        # Функция выполняет запрос к API для получения информации о товаре
        return self.read(resource='products', resource_id=id_product, **kwargs)

    def add_new_product(self, f: ProductFields) -> dict:
        """
        Добавляет новый товар в PrestaShop.

        Преобразовывает объект `ProducFields` в словарь формата `Prestashop` и отправляет его в API PrestaShop.

        Args:
            f (ProductFields): Экземпляр класса ProductFields, содержащий информацию о товаре.

        Returns:
            dict: Возвращает объект `ProductFields` с установленным `id_product`, если товар был успешно добавлен, иначе `None`.
        """

        # Дополняю id_category_default в поле `additional_categories` для поиска её родительских категорий
        f.additional_category_append(f.id_category_default)

        # Функция добавляет родительские категории
        self._add_parent_categories(f)

        # schema = self.get_product_schema(resource_id=24, schema='full')

        presta_product_dict: dict = {'prestashop':
                                         {'attrs':
                                          {'xmlns:xlink': 'http://www.w3.org/1999/xlink'},
                                          'value':
                                          {'products': [
                                              f.to_dict()
                                          ]}
                                          }
                                         }

        presta_product_xml: bytes = dict2xml(presta_product_dict)
        # presta_product_xml_str:str = presta_product_xml.decode('utf-8')
        # Функция создает товар в API
        response = self.create('products', data=presta_product_xml)

        # Функция сохраняет XML
        save_xml(presta_product_xml, gs.path.endpoints / 'emil' / '_experiments' / f'{gs.now}_presta_product.xml')

        if response:
            added_product_ns: SimpleNamespace = j_loads_ns(response['products'][0])
            try:
                # f.reference = response['product']['reference'] if isinstance(response['product']['reference'], str) else int(response['product']['reference'])
                if f.local_image_path:
                    img_data = self.create_binary(
                        resource=f'products/{added_product_ns.id}',
                        file_path=f.local_image_path,
                        file_name=f'{gs.now}.png',
                    )
                    logger.info(f'Товар добавлен: /n {print(added_product_ns)}')
                    return added_product_ns
                elif f.default_image_url:
                    self.upload_image_from_url('products', added_product_ns.id, f.default_image_url)
                    logger.info(f'Товар добавлен: /n {print(added_product_ns)}')
                    return added_product_ns
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
        return

    presta_product_xml = dict2xml(example_data)  # <- XML
    save_xml(presta_product_xml, gs.path.endpoints / 'emil' / '_experiments' / f'{gs.now}_presta_product.xml')

    # 1. JSON | XML
    kwargs: dict = {
        'io_format': 'JSON',
    }

    response = p._exec(
        resource='products',
        method='POST',
        data=example_data if kwargs['io_format'] == 'JSON' else presta_product_xml,
        **kwargs,
    )
    # response = p.create('products', data=presta_product_dict  if kwargs['io_format'] == 'JSON' else presta_product_xml, **kwargs)
    # j_dumps(response if kwargs['io_format'] == 'JSON' else xml2dict(response), gs.path.endpoints / 'emil' / '_experiments' / f"{gs.now}_presta_response_new_product_added.json")

    print(response)


def example_get_product(id_product: int, **kwargs) -> None:
    """Пример получения товара из Prestashop"""

    p = PrestaProduct(API_KEY=Config.API_KEY, API_DOMAIN=Config.API_DOMAIN)
    # kwargs: dict = {
    #     'data_format': 'JSON',
    #     'display': 'full',
    #     'schema': 'blank',
    # }
    presta_product = p.get_product(id_product, **kwargs)
    presta_product = presta_product[0] if isinstance(presta_product, list) else presta_product
    j_dumps(
        presta_product, gs.path.endpoints / 'emil' / '_experiments' / f'presta_response_product_{id_product}.json'
    )


if __name__ == '__main__':
    """"""
    # example_add_new_product()
    example_get_product(2191)