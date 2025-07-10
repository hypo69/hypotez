## \file /src/endpoints/prestashop/product.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для взаимодействия с товарами в PrestaShop.
======================================================
Определяет логику взаимодействия с товарами `Prestashop`.
```rst
.. module:: src.endpoints.prestashop.product
```
"""
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
    """
    Класс для управления товарами в PrestaShop.
    ===========================================
    """

    def __init__(self, api_key: str, api_domain: str, *args: Any, **kwargs: Any):
        """
        Инициализирует объект Product.

        Args:
            api_key (str): Ключ API PrestaShop.
            api_domain (str): Домен API PrestaShop.
            *args (Any): Дополнительные позиционные аргументы для родительского класса.
            **kwargs (Any): Дополнительные именованные аргументы для родительского класса.
        """
        super().__init__(
            api_key = api_key, 
            api_domain = api_domain,
            *args,
            **kwargs,
        )

    def get_product_schema(self, resource_id: Optional[str | int] = None, schema: Optional[str] = None) -> dict:
        """
        Получает схему для ресурса `product` из PrestaShop.

        Args:
            resource_id (Optional[str | int], optional): ID ресурса товара. По умолчанию None.
            schema (Optional[str], optional): Тип схемы. По умолчанию 'blank'.
                - blank	Пустой шаблон ресурса: все поля присутствуют, но без значений. Обычно используется для создания нового объекта.
                - synopsis	Минимальный набор полей: только обязательные поля и краткая структура. Подходит для быстрого обзора.
                - null / не передавать параметр	Возвращает полную схему ресурса со всеми возможными полями, типами и ограничениями.

        Returns:
            dict: Схема для ресурса товара.
        """
        return self.get_schema(resource='products', resource_id=resource_id, schema=schema)

    def get_parent_category(self, id_category: int) -> Optional[int]:
        """
        Извлекает родительские категории из PrestaShop для указанной категории рекурсивно.

        Args:
            id_category (int): ID категории.

        Returns:
            Optional[int]: ID родительской категории (int) или None, если категория не найдена,
                           не имеет родителя (кроме корневых), или произошла ошибка.
        """
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

            if not category_response: # Дополнительная проверка, хотя предыдущая должна покрывать
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
        """
        Вычисляет и добавляет все уникальные родительские категории
        для списка ID категорий в объект ProductFields.

        Args:
            f (ProductFields): Объект ProductFields, в который добавляются
                               уникальные родительские категории.
        """
        # 1. Создание множества для отслеживания всех ID категорий (начальных и добавленных),
        #    включая корневую категорию ID 2 по умолчанию.
        seen_ids: Set[int] = {2}
        # Объявление переменных в начале функции
        initial_categories_copy: List[Dict[str, Any]]
        initial_id_val: Any
        current_search_id: Optional[int] = None
        parent_id: Optional[int] = None

        # Заполнение множества ID из *начального* списка f.additional_categories
        # Итерация по копии, чтобы избежать проблем, если f.additional_category_append изменяет список
        initial_categories_copy = list(f.additional_categories)

        for initial_cat_dict in initial_categories_copy:
            # Проверка, что это словарь и есть ключ 'id'
            if isinstance(initial_cat_dict, dict):
                initial_id_val = initial_cat_dict.get('id')
                if initial_id_val is not None: # Явная проверка на None важна, если 0 может быть ID
                    try:
                        # Конвертация в int и добавление в множество
                        seen_ids.add(int(initial_id_val))
                    except (ValueError, TypeError):
                        logger.warning(f"Не удалось конвертировать начальный ID категории в int: {initial_id_val}. Пропуск.")
            else:
                 logger.warning(f"Элемент в начальном списке категорий не является словарем: {initial_cat_dict}. Пропуск.")

        logger.debug(f"Начальные уникальные ID категорий (включая обработанные): {seen_ids}")

        # 2. Итерация по начальным категориям для поиска их родителей
        # Снова используется копия для безопасности
        for _c in initial_categories_copy:
             # Безопасное извлечение ID для старта поиска родителей
            if not isinstance(_c, dict): continue # Пропуск не-словарей
            start_cat_id_val: Any = _c.get('id')
            if start_cat_id_val is None: continue # Пропуск, если нет ID

            try:
                # Текущий ID категории, по которому выполняется поиск родителя
                current_search_id = int(start_cat_id_val)
            except (ValueError, TypeError):
                logger.warning(f"Не удалось конвертировать стартовый ID категории {start_cat_id_val} в int. Пропуск ветки.")
                continue

            # Пропуск корневых категорий или некорректных ID
            if current_search_id <= 2: # ID 2 - обычно корень, ID < 2 - некорректны
                continue

            logger.debug(f"Поиск родителей для стартовой категории ID: {current_search_id}")

            # 3. Подъем по иерархии
            while current_search_id is not None and current_search_id > 2: # Пока не достигнут корень
                parent_id = self.get_parent_category(current_search_id)

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
                        # Дубликат найден, просто логирование и переход вверх по иерархии
                        logger.debug(f"Родитель ID {parent_id} уже присутствует/добавлен.")

                    # Переход к следующему родителю вверх по иерархии
                    current_search_id = parent_id
                else:
                    # Родитель не найден или является корнем - завершение подъема для этой ветки
                    logger.debug(f"Завершение поиска родителей для ветки (родитель: {parent_id}, текущий ID для поиска был: {current_search_id})")
                    break # Выход из while для текущей start_cat_id_val
            # Конец цикла while
        # Конец цикла for

        logger.debug(f"Финальный набор уникальных ID категорий: {seen_ids}")
        # Объект f.additional_categories теперь содержит исходные категории + уникальные родительские

    def get_product(self, id_product: int, **kwargs: Any) -> dict:
        """
        Возвращает словарь полей товара из магазина Prestashop.

        Args:
            id_product (int): Значение поля ID в таблице `product` Prestashop.
            **kwargs (Any): Дополнительные параметры для API запроса.

        Returns:
            dict: Словарь, содержащий данные товара, например:
                  `{'product': {'id': 1, 'name': 'Test Product', ...}}`
                  или пустой словарь в случае ошибки.
        """
        kwargs['data_format'] = 'JSON' # Обеспечение JSON формата для консистентности
        return self.read(resource='products', resource_id=id_product, **kwargs)

    async def add_new_product_async(self, f: ProductFields) -> SimpleNamespace | dict:
        """
        Добавляет новый товар в PrestaShop.

        Функция преобразует объект `ProductFields` в словарь формата `Prestashop`
        и отправляет его в API PrestaShop.

        Args:
            f (ProductFields): Экземпляр дата-класса ProductFields, содержащий информацию о товаре.

        Returns:
            SimpleNamespace | dict: Возвращает объект `SimpleNamespace`, представляющий детали добавленного
                                    товара из API PrestaShop в случае успеха, или пустой словарь (`{}`),
                                    если операция не удалась.
        """
        presta_product_dict: dict
        presta_product_xml: bytes
        response: Optional[dict]
        added_product_ns: SimpleNamespace

        # Дополнение id_category_default в поле `additional_categories` для поиска её родительских категорий
        f.additional_category_append(f.id_category_default)

        self._add_parent_categories(f)

        presta_product_dict = {'prestashop': 
                                     {'attrs':
                                      {'xmlns:xlink': 'http://www.w3.org/1999/xlink'}, 
                                      'value':
                                      {'products':[ # API ожидает список товаров, даже для одного
                                        f.to_dict()
                                         ]}
                                      }
                                     }

        presta_product_xml = dict2xml(presta_product_dict)
        
        # Сохранение XML перед отправкой для отладки
        save_xml(presta_product_xml, gs.path.endpoints / 'emil' / '_experiments' / f'{gs.now}_presta_product_add_request.xml')
        
        # --- TODO Сделать асинхронным вызов API ---
        response = await self.create_async('products', data=presta_product_xml)
        
        if response and 'products' in response and response['products']:
            # Предполагаем, что API возвращает список с одним элементом для созданного товара
            added_product_ns = j_loads_ns(response['products'][0])
            try:
                # f.reference = response['product']['reference'] if isinstance(response['product']['reference'], str) else int(response['product']['reference']) # Закомментированный код сохранен
                if f.local_image_path: 
                    _ = self.create_binary( # Результат create_binary не используется, присвоение к _
                        resource=f'products/{added_product_ns.id}',
                        file_path=f.local_image_path,
                        file_name=f'{f.reference}.png',
                    )
                    
                    print(added_product_ns)
                    # Логирование информации о добавленном товаре
                    logger.info(f'Товар добавлен. Детали: {str(added_product_ns)}')
                    return added_product_ns

                # elif f.default_image_url:
                #     await self.upload_image_from_url_async('products', added_product_ns.id, f.default_image_url)
                    
                #     print(added_product_ns)
                #     # Логирование информации о добавленном товаре
                #     logger.info(f'Товар добавлен. Детали: {str(added_product_ns)}')
                #     return added_product_ns
                # else:
                #     # Если изображений нет, все равно товар добавлен
                #     print(added_product_ns)
                #     logger.info(f'Товар добавлен (без изображения). Детали: {str(added_product_ns)}')
                #     return added_product_ns
                    
            except (KeyError, TypeError) as ex:
                logger.error(f'Ошибка при обработке ответа от сервера или загрузке изображения: {ex}', ex, exc_info=True)
                return {}
        else:
            
            print(print_data=presta_product_dict, text_color='yellow')
            # Логирование ошибки добавления товара
            logger.error(
                f"Ошибка при добавлении товара. Отправляемые данные: {json.dumps(presta_product_dict, ensure_ascii=False, indent=2)}",
                exc_info=True, # exc_info=True обычно используется с передачей объекта исключения
            )
            # Если response не None, но не содержит ожидаемых данных
            if response:
                 logger.error(f"Получен неожиданный ответ от API: {json.dumps(response, ensure_ascii=False, indent=2)}")
            return {}

# ##################################################   EXAMPLES ##################################################


def example_add_new_product() -> None:
    """Пример для добавления товара в Prestashop"""
    # Переменные для примера
    p: PrestaProduct
    # schema: dict # Не используется в текущей логике примера
    example_data: dict
    presta_product_xml: bytes
    # kwargs_example: dict # Переименовано для ясности, что это для примера
    response: Optional[dict]

    # Определение Config (предполагается, что Config существует и настроен)
    class Config: # Локальное определение для примера, если не импортируется глобально
        API_KEY: str = 'YOUR_API_KEY'
        API_DOMAIN: str = 'YOUR_API_DOMAIN'
        # Установите реальные значения или обеспечьте загрузку Config

    if Config.API_KEY == 'YOUR_API_KEY': # Проверка на значения по умолчанию
        logger.warning("API_KEY и API_DOMAIN не настроены в примере. Используются значения по умолчанию.")
        # return # Можно раскомментировать, чтобы прервать выполнение примера без конфигурации


    p = PrestaProduct(api_key=Config.API_KEY, api_domain=Config.API_DOMAIN) # Используется api_key и api_domain
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEBUG ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # resource_id: int = 2191
    # schema = p.get_product_schema(resource_id = resource_id)
    # j_dumps(schema, gs.path.endpoints / 'emil' / '_experiments' / f'product_schema.{resource_id}_{gs.now}.json')
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    example_data = j_loads(
        gs.path.endpoints / 'emil' / '_experiments' / 'product_schema.2191_250319224027026.json'
    )
    """""" # Этот комментарий выглядит как артефакт, оставляю по инструкции
    if not example_data:
        logger.error('Файл не существует или неправильный формат файла')
        ...
        return

    presta_product_xml = dict2xml(example_data)
    save_xml(presta_product_xml, gs.path.endpoints / 'emil' / '_experiments' / f'{gs.now}_presta_product.xml')

    # 1. JSON | XML
    kwargs_example = { # Переименовано для избежания конфликта с **kwargs функции
        'io_format': 'JSON', # или 'XML'
    }

    response = p._exec( # _exec - это метод PrestaShop (родительского класса)
        resource='products',
        method='POST',
        data=example_data if kwargs_example['io_format'] == 'JSON' else presta_product_xml,
        **kwargs_example, # Передаем как именованные аргументы
    )
    # response = p.create('products', data=presta_product_dict  if kwargs_example['io_format'] == 'JSON' else presta_product_xml, **kwargs_example)
    
    # Сохранение ответа
    # output_path = gs.path.endpoints / 'emil' / '_experiments' / f"{gs.now}_presta_response_new_product_added.json"
    # if kwargs_example['io_format'] == 'JSON':
    #     j_dumps(response, output_path)
    # else:
    #     # Если ответ XML (строка или байты), его нужно сначала преобразовать в dict для j_dumps
    #     # или сохранить как XML-файл. xml2dict не импортируется, если он нужен, его нужно импортировать.
    #     # Для примера, если response это XML строка:
    #     # from src.endpoints.prestashop.utils.xml2dict import xml2dict # Потребуется импорт
    #     # dict_response = xml2dict(response) 
    #     # j_dumps(dict_response, output_path)
    #     # Либо сохранить XML напрямую:
    #     # save_xml(response, gs.path.endpoints / 'emil' / '_experiments' / f"{gs.now}_presta_response_new_product_added.xml")
    #     logger.info("Ответ в формате XML, для сохранения как JSON требуется xml2dict.")


    print(response)
    ...


def example_get_product(id_product: int, **kwargs: Any) -> None:
    """"""
    p: PrestaProduct = None
    presta_product_data: dict = None

    # Определение Config (предполагается, что Config существует и настроен)
    class Config: # Локальное определение для примера
        API_KEY: str = 'YOUR_API_KEY'
        API_DOMAIN: str = 'YOUR_API_DOMAIN'
        # Установите реальные значения

    if Config.API_KEY == 'YOUR_API_KEY':
        logger.warning("API_KEY и API_DOMAIN не настроены в примере. Используются значения по умолчанию.")
        # return


    p = PrestaProduct(api_key=Config.API_KEY, api_domain=Config.API_DOMAIN)
    # kwargs для get_product могут быть переданы извне, например:
    # kwargs_get = {
    #     'display': 'full', # 'blank', 'synopsis'
    # }
    presta_product_data = p.get_product(id_product, **kwargs) # Передаем внешние kwargs
    
    # API может вернуть список товаров, даже при запросе по ID, хотя get_product ожидает один
    # Это поведение зависит от реализации self.read в PrestaShop API
    # Если p.get_product всегда возвращает dict{'product': {...}}, то извлечение первого элемента не нужно.
    # Судя по `response['products'][0]` в `add_new_product`, API часто возвращает список.
    # Уточним, что get_product возвращает
    # Если `self.read` возвращает {'products': [...]}, то нужно извлечь:
    # if presta_product_data and 'products' in presta_product_data and isinstance(presta_product_data['products'], list) and presta_product_data['products']:
    #    actual_product = presta_product_data['products'][0]
    # else:
    #    actual_product = presta_product_data # Или {} если структура не та

    # Учитывая, что get_product просто вызывает self.read, а self.read в PrestaShop API обычно возвращает {'resource_name_plural': [items...]}
    # то, вероятно, нужно извлекать товар из списка.
    # Однако, текущая реализация get_product напрямую возвращает результат self.read,
    # что может быть `{'products': [{'id': ...,}]}`.
    # Для консистентности, если нужен сам товар, а не обертка:
    
    actual_product_details: Optional[dict] = None
    if presta_product_data and 'products' in presta_product_data and isinstance(presta_product_data['products'], list):
        if presta_product_data['products']:
            actual_product_details = presta_product_data['products'][0]
        else:
            logger.warning(f"Список товаров для ID {id_product} пуст.")
    elif presta_product_data and 'product' in presta_product_data : # Если API вернул одиночный товар
         actual_product_details = presta_product_data['product']
    else:
        logger.warning(f"Неожиданная структура ответа для товара ID {id_product}: {presta_product_data}")
        actual_product_details = presta_product_data # Сохраняем как есть для отладки

    ...
    j_dumps(
        actual_product_details, gs.path.endpoints / 'emil' / '_experiments' / f'presta_response_product_{id_product}.json'
    )
    ...


if __name__ == '__main__':
    """"""
    # Определение Config для __main__ блока
    class Config:
        API_KEY: str = os.environ.get('PRESTA_API_KEY', 'YOUR_API_KEY_HERE') # Пример загрузки из env
        API_DOMAIN: str = os.environ.get('PRESTA_API_DOMAIN', 'YOUR_DOMAIN_HERE')
        # Убедитесь, что эти переменные окружения установлены, или замените значениями.
        # Важно: os импорт не был удален, так как он нужен здесь. Добавим его обратно.
    import os # Импорт os здесь, так как он используется в __main__

    if Config.API_KEY == 'YOUR_API_KEY_HERE' or Config.API_DOMAIN == 'YOUR_DOMAIN_HERE':
        logger.error("Переменные окружения PRESTA_API_KEY и PRESTA_API_DOMAIN не установлены.")
        logger.info("Пожалуйста, установите их или измените значения в Config в __main__ блоке.")
    else:
        # example_add_new_product()
        example_get_product(2191) # Пример вызова
    ...
