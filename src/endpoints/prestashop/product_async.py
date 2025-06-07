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
import os # Добавлен импорт os для использования в __main__
from pathlib import Path
from types import SimpleNamespace
from typing import List, Dict, Any, Optional, Set

# Импорты по умолчанию
import header
from header import __root__
from src import gs

from src.endpoints.prestashop.api_async import PrestaShopAsync # Изменено на асинхронный API
from src.endpoints.prestashop.product_fields import ProductFields
from src.endpoints.prestashop.utils.dict2xml import dict2xml # Используется для XML

from src.utils.xml import save_xml # Используется
from src.utils.jjson import j_loads, j_loads_ns, j_dumps # Используются
from src.utils.printer import pprint as print # Используется
from src.logger.logger import logger
# from src import USE_ENV # Не используется в переписанном классе, но оставлен если нужен в __main__


class PrestaProductAsync(PrestaShopAsync):
    """
    Асинхронный класс для управления товарами в PrestaShop.
    =======================================================
    Класс взаимодействует с API PrestaShop для управления товарами.
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
            *args, # Передача позиционных аргументов
            **kwargs, # Передача именованных аргументов
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
            >>> # schema = await product_api.get_product_schema_async(resource_id=1, schema='blank')
            >>> # if schema: print(schema)
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
            >>> # parent_id = await product_api.get_parent_category_async(5)
            >>> # if parent_id: print(f'Parent category ID: {parent_id}')
        """
        # Объявление переменных
        category_info: Optional[dict] = None # Изменено имя для ясности
        response_data: Optional[dict] = None
        parent_id_value: Any # Для временного хранения значения перед конвертацией

        try:
            response_data = await self.read_async( # Асинхронный вызов
                'categories', resource_id=id_category, display='full' # data_format управляется PrestaShopAsync
            )
            
            # Проверка структуры ответа
            if response_data and 'category' in response_data: # PrestaShop обычно возвращает {'category': {...}} для одиночного ресурса
                category_info = response_data['category']
            elif response_data and 'categories' in response_data and isinstance(response_data['categories'], list) and response_data['categories']:
                # Если API вернул список, берем первый элемент (нетипично для read по ID)
                category_info = response_data['categories'][0]
                logger.warning(f'API вернул список категорий при запросе по ID {id_category}, использован первый элемент.')
            else:
                logger.error(f'Ответ API не содержит ожидаемых данных для категории ID {id_category}. Ответ: {response_data}')
                return None

            if not category_info or not isinstance(category_info, dict): # Дополнительная проверка
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
        except Exception as ex: # Любые другие исключения
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
        # Объявление переменных
        seen_ids: Set[int] = {2} # ID 2 - обычно корневая категория Home
        initial_categories_copy: List[Dict[str, Any]]
        initial_id_val: Any
        current_search_id: Optional[int] = None
        parent_id: Optional[int] = None

        # 1. Заполнение `seen_ids` начальными категориями из `f.additional_categories`
        initial_categories_copy = list(f.additional_categories) # Копия для безопасной итерации

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

        # 2. Итерация по начальным категориям для поиска их родителей
        for category_dict_to_process in initial_categories_copy:
            if not isinstance(category_dict_to_process, dict): continue
            
            start_category_id_value: Any = category_dict_to_process.get('id')
            if start_category_id_value is None: continue

            try:
                current_search_id = int(start_category_id_value)
            except (ValueError, TypeError):
                logger.warning(f'Не удалось конвертировать стартовый ID категории {start_category_id_value} в int. Пропуск ветки.')
                continue
            
            # Пропуск корневых категорий или некорректных ID (ID < 2)
            if current_search_id <= 2: 
                continue
            
            logger.debug(f'Поиск родителей для стартовой категории ID: {current_search_id}')

            # 3. Подъем по иерархии категорий
            while current_search_id is not None and current_search_id > 2:
                parent_id = await self.get_parent_category_async(current_search_id) # Асинхронный вызов

                if parent_id is not None and parent_id > 2: # Родитель найден и не является корнем
                    if parent_id not in seen_ids:
                        logger.debug(f'Найден новый родитель ID: {parent_id}. Добавление.')
                        f.additional_category_append(parent_id) # Метод добавляет {'id': parent_id}
                        seen_ids.add(parent_id)
                    else:
                        logger.debug(f'Родитель ID {parent_id} уже присутствует/добавлен.')
                    
                    current_search_id = parent_id # Переход к следующему родителю
                else:
                    # Родитель не найден, является корнем, или произошла ошибка
                    logger.debug(f'Завершение поиска родителей для ветки (родитель: {parent_id}, текущий ID для поиска был: {current_search_id})')
                    break # Выход из while для текущей ветки
        
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
            >>> # product_data = await product_api.get_product_async(1, display='full')
            >>> # if product_data: print(product_data.get('product', {}).get('name'))
        """
        # Функция извлекает данные товара
        # data_format='JSON' устанавливается по умолчанию в PrestaShopAsync, если не переопределено
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
            >>> # result = await product_api.add_new_product_async(product_fields)
            >>> # if isinstance(result, SimpleNamespace): print(f'Added product ID: {result.id}')
        """
        # Объявление переменных
        presta_product_dict: dict
        payload_for_api: str | dict # Зависит от data_format
        response: Optional[dict] = None
        added_product_ns: SimpleNamespace
        upload_image_task: Optional[asyncio.Task] = None # Для асинхронной загрузки изображения

        # Добавление категории по умолчанию в список для обработки родительских
        f.additional_category_append(f.id_category_default)
        await self._add_parent_categories_async(f) # Асинхронный вызов

        # Формирование словаря для PrestaShop API
        # API ожидает {'product': product_data} для JSON, или <prestashop><product>...</product></prestashop> для XML.
        # _exec_async с payload=product_data (dict) для JSON отправит {"product": product_data} если product_data это {"product":...}
        # Для XML, dict2xml должен создать правильную структуру.
        # PrestaShop API для создания ОДНОГО продукта ожидает {"product": {...}} в JSON.
        # Если f.to_dict() возвращает {...} (поля продукта), то нужно обернуть:
        product_data_dict: dict = f.to_dict()
        
        # Payload зависит от self.data_format (JSON или XML)
        if self.data_format == 'JSON':
             # Для JSON, API часто ожидает объект 'product' напрямую
            presta_product_dict = {'product': product_data_dict}
            payload_for_api = presta_product_dict # Будет сериализовано в JSON в _exec_async
        elif self.data_format == 'XML':
            # Для XML, dict2xml должен создать <prestashop><product>...</product></prestashop>
            # Передаем product_data_dict в обертке, чтобы dict2xml создал правильный корень
            presta_product_dict = {'prestashop': {'product': product_data_dict}}
            payload_for_api = dict2xml(presta_product_dict) # dict2xml возвращает строку XML
            # Сохранение XML перед отправкой для отладки
            xml_save_path: Path = gs.path.endpoints / 'emil' / '_experiments' / f'{gs.now}_presta_product_add_request.xml'
            save_xml(payload_for_api, xml_save_path) # save_xml ожидает bytes или str
            logger.debug(f'XML запрос для добавления товара сохранен в: {xml_save_path}')
        else:
            logger.error(f'Неподдерживаемый data_format: {self.data_format} для добавления товара.')
            return {}
        
        response = await self.create_async('products', data=payload_for_api) # Передаем payload_for_api
        
        # Обработка ответа API
        # PrestaShop при успешном создании обычно возвращает {'product': {...созданный продукт...}}
        if response and 'product' in response and isinstance(response['product'], dict):
            added_product_info: dict = response['product']
            added_product_ns = j_loads_ns(added_product_info) # Преобразование в SimpleNamespace
            ... # Точка останова
            try:
                # f.reference = added_product_info.get('reference') # Обновление, если нужно
                
                # Асинхронная загрузка изображения, если есть
                if f.local_image_path: 
                    # Используем create_task для неблокирующей загрузки, если это критично по времени,
                    # но здесь просто await, так как это часть процесса добавления товара.
                    img_upload_response = await self.create_binary_async( 
                        resource_path=f'images/products/{added_product_ns.id}', # resource_path, не resource
                        file_path=str(f.local_image_path), # Убедимся, что это строка
                        file_name_in_request=f'{gs.now.strftime("%Y%m%d%H%M%S")}.png', # Уникальное имя файла
                    )
                    if not img_upload_response:
                        logger.warning(f'Не удалось загрузить локальное изображение для товара ID {added_product_ns.id}')
                
                elif f.default_image_url:
                    img_upload_response = await self.upload_image_from_url_async(
                        resource_images_path='images/products', # Базовый путь
                        entity_id=int(added_product_ns.id),
                        img_url=f.default_image_url
                    )
                    if not img_upload_response:
                        logger.warning(f'Не удалось загрузить изображение по URL для товара ID {added_product_ns.id}')
                
                print(added_product_ns) # Используем print (pprint)
                logger.info(f'Товар успешно добавлен. Детали: {str(added_product_ns)}')
                return added_product_ns
                    
            except (KeyError, TypeError, AttributeError) as ex: # AttributeError для ns.id
                logger.error(f'Ошибка при обработке ответа от сервера или загрузке изображения для товара', ex, exc_info=True)
                # Товар мог быть создан, но изображение не загружено. Возвращаем {} как признак частичной неудачи.
                # Или можно вернуть added_product_ns, если основная операция (создание товара) успешна.
                # Для согласованности с исходным кодом, возвращаем {} при любой ошибке здесь.
                return {}
        else: # Ошибка при создании товара
            # Логирование отладочной информации
            if self.data_format == 'JSON': # presta_product_dict уже в нужном формате для JSON
                log_data_dict = presta_product_dict
            else: # Для XML, dict2xml использовал presta_product_dict с оберткой 'prestashop'
                  # Используем product_data_dict для лога, т.к. он чище
                log_data_dict = {'product_data_sent_to_xml_converter': product_data_dict}

            print(print_data=log_data_dict, text_color='yellow')
            logger.error(
                f"Ошибка при добавлении товара. Отправляемые данные (до 최종 преобразования в XML/JSON): {j_dumps(log_data_dict)}",
                exc_info=False, # exc_info=True если есть объект исключения, здесь его нет.
            )
            if response: # Если ответ есть, но он некорректный
                 logger.error(f"Получен неожиданный или ошибочный ответ от API: {j_dumps(response)}")
            return {}

# ##################################################   EXAMPLES ##################################################

# Для асинхронных примеров, они должны быть async def и запускаться через asyncio.run()

async def example_add_new_product_async() -> None:
    """Асинхронный пример для добавления товара в Prestashop."""
    # Объявление переменных
    p_async: PrestaProductAsync
    # schema_example: dict | None # Не используется
    example_data_fields: ProductFields # Используем ProductFields для примера
    result: SimpleNamespace | dict

    # Определение Config (предполагается, что Config существует и настроен)
    class ConfigExample: 
        API_KEY: str = os.environ.get('PRESTA_API_KEY_ASYNC', 'YOUR_API_KEY')
        API_DOMAIN: str = os.environ.get('PRESTA_API_DOMAIN_ASYNC', 'YOUR_API_DOMAIN')
        
    if ConfigExample.API_KEY == 'YOUR_API_KEY' or ConfigExample.API_DOMAIN == 'YOUR_API_DOMAIN':
        logger.warning("API_KEY и API_DOMAIN не настроены для асинхронного примера. Используются значения по умолчанию.")
        # return # Можно прервать, если нет конфигурации

    p_async = PrestaProductAsync(api_key=ConfigExample.API_KEY, api_domain=ConfigExample.API_DOMAIN, data_format='JSON') # Явно JSON для примера

    # Создание ProductFields для примера
    # Убедитесь, что все обязательные поля ProductFields заполнены
    example_data_fields = ProductFields(
        id_manufacturer=1, # Пример
        id_supplier=1, # Пример
        id_category_default=2, # Пример (Home категория)
        name=[{'language_id': 1, 'value': f'Async Test Product {gs.now.strftime("%H%M%S")}'}],
        description=[{'language_id': 1, 'value': 'Async description here.'}],
        description_short=[{'language_id': 1, 'value': 'Async short desc.'}],
        link_rewrite=[{'language_id': 1, 'value': f'async-test-product-{gs.now.strftime("%H%M%S")}'}],
        reference=f'ASYNC_REF_{gs.now.strftime("%H%M%S")}',
        price='19.99',
        quantity=10,
        active='1',
        available_for_order='1',
        state='1', # Новый товар
        # ... другие необходимые поля ProductFields
    )
    # Добавление категорий, если нужно
    example_data_fields.additional_category_append(3) # ID категории 3
    example_data_fields.additional_category_append(4) # ID категории 4

    # Пример с локальным изображением (создайте dummy файл для теста)
    # dummy_image_path = Path('dummy_async_product_image.png')
    # try:
    #     with open(dummy_image_path, 'w') as f_img: f_img.write("dummy data")
    #     example_data_fields.local_image_path = str(dummy_image_path)
    # except IOError as e_io:
    #     logger.error(f"Не удалось создать dummy файл изображения: {e_io}")

    # Вызов асинхронного метода
    result = await p_async.add_new_product_async(example_data_fields)
    
    # if dummy_image_path.exists(): # Очистка dummy файла
    #     try: dummy_image_path.unlink()
    #     except OSError as e_os: logger.error(f"Не удалось удалить dummy файл: {e_os}")

    if isinstance(result, SimpleNamespace):
        logger.info(f"Асинхронно добавлен товар ID: {result.id}, Reference: {result.reference}")
        print(result) # Используем print (pprint)
    else:
        logger.error(f"Ошибка при асинхронном добавлении товара. Ответ: {result}")
    ...


async def example_get_product_async(id_product: int, **kwargs: Any) -> None:
    """Асинхронный пример получения информации о товаре."""
    # Объявление переменных
    p_async: PrestaProductAsync
    product_data_response: dict | None # Ответ от API

    class ConfigExample: 
        API_KEY: str = os.environ.get('PRESTA_API_KEY_ASYNC', 'YOUR_API_KEY')
        API_DOMAIN: str = os.environ.get('PRESTA_API_DOMAIN_ASYNC', 'YOUR_API_DOMAIN')

    if ConfigExample.API_KEY == 'YOUR_API_KEY' or ConfigExample.API_DOMAIN == 'YOUR_API_DOMAIN':
        logger.warning("API_KEY и API_DOMAIN не настроены для асинхронного примера. Используются значения по умолчанию.")
        # return

    p_async = PrestaProductAsync(api_key=ConfigExample.API_KEY, api_domain=ConfigExample.API_DOMAIN)
    
    product_data_response = await p_async.get_product_async(id_product, **kwargs)
    
    actual_product_details: Optional[dict] = None
    if product_data_response and 'product' in product_data_response: # PrestaShop обычно возвращает {'product': {...}}
        actual_product_details = product_data_response['product']
    elif product_data_response: # Если структура другая
        logger.warning(f"Неожиданная структура ответа для товара ID {id_product}: {product_data_response}")
        actual_product_details = product_data_response # Сохраняем как есть для отладки
    else:
        logger.error(f"Товар с ID {id_product} не найден или произошла ошибка API.")


    if actual_product_details:
        print(actual_product_details) # Используем print (pprint)
        # Сохранение JSON ответа
        # output_path: Path = gs.path.endpoints / 'emil' / '_experiments' / f'presta_async_response_product_{id_product}_{gs.now.strftime("%Y%m%d%H%M%S")}.json'
        # j_dumps(actual_product_details, output_path)
        # logger.info(f"Данные товара ID {id_product} сохранены в {output_path}")
    ...


if __name__ == '__main__':
    """"""
    # Конфигурация для __main__
    class ConfigMain:
        API_KEY: str = os.environ.get('PRESTA_API_KEY_ASYNC', 'YOUR_API_KEY_HERE')
        API_DOMAIN: str = os.environ.get('PRESTA_API_DOMAIN_ASYNC', 'YOUR_DOMAIN_HERE')

    if ConfigMain.API_KEY == 'YOUR_API_KEY_HERE' or ConfigMain.API_DOMAIN == 'YOUR_DOMAIN_HERE':
        logger.error("Переменные окружения PRESTA_API_KEY_ASYNC и PRESTA_API_DOMAIN_ASYNC не установлены.")
        logger.info("Пожалуйста, установите их или измените значения в ConfigMain в __main__ блоке.")
    else:
        try:
            # Запуск асинхронных примеров
            # asyncio.run(example_add_new_product_async())
            asyncio.run(example_get_product_async(2191, display='[id,name,reference,price]')) # Пример с kwargs
            
        except KeyboardInterrupt:
            logger.info('Выполнение программы прервано пользователем (Ctrl+C).')
        except Exception as main_ex:
            logger.error('Произошла непредвиденная ошибка при выполнении __main__', main_ex, exc_info=True)
    ...
