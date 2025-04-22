### **Анализ кода модуля `ali_campaign_editor.py`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Использование аннотаций типов.
  - Четкая структура классов и методов.
  - Использование `logger` для логирования.
- **Минусы**:
  - Не все функции и методы имеют docstring.
  - Отсутствие обработки ошибок во всех функциях.
  - Встречаются смешанные стили кавычек (следует использовать одинарные).
  - Не все переменные объявлены в начале функции.

**Рекомендации по улучшению:**

1. **Документирование кода**:
   - Добавить docstring к каждой функции и методу, описывающие их назначение, аргументы, возвращаемые значения и возможные исключения.
   - Перевести все docstring на русский язык и использовать формат UTF-8.
     ```python
     def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
         """ Функция выполняет некоторое действия... <Тут Ты пишешь что именно делает функция> 
         Args:
             param (str): Описание параметра `param`.
             param1 (Optional[str | dict | str], optional): Описание параметра `param1`. По умолчанию `None`.

         Returns:
             dict | None: Описание возвращаемого значения. Возвращает словарь или `None`.

         Raises:
             SomeError: Описание ситуации, в которой возникает исключение `SomeError`.
            ...
            <Выводить тело функции НЕ НАДО. Только docstring>
         """
     ```

2. **Обработка ошибок**:
   - Добавить блоки `try...except` для обработки возможных исключений в каждой функции и методе.
   - Логировать ошибки с использованием `logger.error` и передавать информацию об исключении (`ex`) и трассировку (`exc_info=True`).
     ```python
     try:
         ...
     except SomeError as ex:
         logger.error('Some error message', ex, exc_info=True)
     ```

3. **Форматирование кода**:
   - Использовать только одинарные кавычки (`'`) для строк.
   - Объявлять все переменные в начале функции.

4. **Именование переменных**:
   - Убедиться, что имена переменных и параметров функций соответствуют PEP8.

5. **Использовать `j_loads` или `j_loads_ns`**:
   - Заменить стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns` для чтения JSON или конфигурационных файлов.

**Оптимизированный код:**

```python
## \file /src/suppliers/aliexpress/campaign/ali_campaign_editor.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для редактирования рекламных кампаний Aliexpress.
========================================================

Этот модуль предоставляет редактор для управления рекламными кампаниями на платформе Aliexpress.
Он включает в себя функциональность для добавления, удаления и обновления товаров, а также
для управления категориями и другими параметрами кампании.

"""

import asyncio
import re
import shutil
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import List, Optional

import header
from src import gs
from src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign import AliPromoCampaign
from src.suppliers.suppliers_list.aliexpress.campaign.gsheet import AliCampaignGoogleSheet
from src.suppliers.suppliers_list.aliexpress.utils import extract_prod_ids, ensure_https
from src.utils.jjson import j_loads_ns, j_loads, j_dumps
from src.utils.convertors.csv import csv2dict
from src.utils.printer import pprint
from src.utils.file import (read_text_file,
                        get_filenames_from_directory,
                        get_directory_names,
                        save_text_file
                        )
from src.logger.logger import logger

class AliCampaignEditor(AliPromoCampaign):
    """Редактор для рекламных кампаний."""

    def __init__(self, 
                 campaign_name: str, 
                 language: Optional[str | dict] = None, 
                 currency: Optional[str] = None):
        """Инициализирует редактор кампании с заданными параметрами.
        
        Args:
            campaign_name (str): Название кампании.
            language (Optional[str | dict]): Язык кампании. По умолчанию 'EN'.
            currency (Optional[str]): Валюта кампании. По умолчанию 'USD'.
            campaign_file (Optional[str | Path]): Путь к файлу `<lang>_<currency>.json` из корневой папки кампании. По умолчанию None.

        Raises:
            ValueError: Если не указано ни `campaign_name`, ни `campaign_file`.

        Example:
            # 1. По параметрам кампании
            >>> editor = AliCampaignEditor(campaign_name='Summer Sale', language='EN', currency='USD')
            # 2. Загрузка из файла
            >>> editor = AliCampaignEditor(campaign_name='Summer Sale', campaign_file='EN_USD.JSON')
        """
        super().__init__(campaign_name = campaign_name, language = language, currency = currency)
        #self.google_sheet = AliCampaignGoogleSheet(campaign_name = campaign_name, language = language, currency = currency, campaign_editor = self)

    def delete_product(self, product_id: str, exc_info: bool = False):
        """Удаляет товар, у которого нет партнерской ссылки.
        
        Args:
            product_id (str): ID товара, который нужно удалить.
            exc_info (bool): Включать ли информацию об исключении в логи. По умолчанию False.

        Example:
            >>> editor = AliCampaignEditor(campaign_name='Summer Sale')
            >>> editor.delete_product('12345')
        """
        _product_id = None
        product_path = None
        prepared_product_path = None
        products_list = None
        try:
            _product_id = extract_prod_ids(product_id)
            product_path = self.category_path / 'sources.txt'
            prepared_product_path = self.category_path / '_sources.txt'
            products_list = read_text_file(product_path)
            
            if products_list:
                for record in products_list:
                    if _product_id:
                        record_id = extract_prod_ids(record)
                        if record_id == str(product_id):
                            products_list.remove(record)
                            save_text_file((products_list, '\n'), prepared_product_path)
                            break
                    else:
                        if record == str(product_id):
                            products_list.remove(record)
                            save_text_file((products_list, '\n'), product_path)
            else:
                product_path = self.category_path / 'sources' / f'{product_id}.html'
                try:
                    product_path.rename(self.category_path / 'sources' / f'{product_id}_.html')
                    logger.success(f"Product file {product_path=} renamed successfully.")
                except FileNotFoundError as ex:
                    logger.error(f"Product file {product_path=} not found.", exc_info=exc_info)
                except Exception as ex:
                    logger.critical(f"An error occurred while deleting the product file {product_path}.", ex)
        except Exception as ex:
            logger.error(f'Ошибка при удалении товара {product_id}: {ex}', exc_info=True)

    def update_product(self, category_name: str, lang: str, product: dict):
        """Обновляет информацию о товаре в заданной категории.

        Args:
            category_name (str): Название категории, в которой нужно обновить товар.
            lang (str): Язык кампании.
            product (dict): Словарь с данными о товаре.

        Example:
            >>> editor = AliCampaignEditor(campaign_name='Summer Sale')
            >>> editor.update_product('Electronics', 'EN', {'product_id': '12345', 'title': 'Smartphone'})
        """
        try:
            self.dump_category_products_files(category_name, lang, product)
        except Exception as ex:
            logger.error(f'Ошибка при обновлении товара в категории {category_name}: {ex}', exc_info=True)

    def update_campaign(self):
        """Обновляет свойства кампании, такие как описание, теги и т.д.

        Example:
            >>> editor = AliCampaignEditor(campaign_name='Summer Sale')
            >>> editor.update_campaign()
        """
        try:
            ... # TODO: Add implementation here
        except Exception as ex:
            logger.error(f'Ошибка при обновлении кампании: {ex}', exc_info=True)

    def update_category(self, json_path: Path, category: SimpleNamespace) -> bool:
        """Обновляет категорию в JSON файле.

        Args:
            json_path (Path): Путь к JSON файлу.
            category (SimpleNamespace): Объект категории для обновления.

        Returns:
            bool: True, если обновление успешно, иначе False.

        Example:
            >>> category = SimpleNamespace(name='New Category', description='Updated description')
            >>> editor = AliCampaignEditor(campaign_name='Summer Sale')
            >>> result = editor.update_category(Path('category.json'), category)
            >>> print(result)  # True, если успешно
        """
        data = None
        try:
            data = j_loads(json_path)  # Чтение JSON данных из файла
            data['category'] = category.__dict__  # Преобразование SimpleNamespace в dict
            j_dumps(data, json_path)  # Запись обновленных JSON данных обратно в файл
            return True
        except Exception as ex:
            logger.error(f"Не удалось обновить категорию {json_path}: {ex}", exc_info=True)
            return False

    def get_category(self, category_name: str) -> Optional[SimpleNamespace]:
        """Возвращает объект SimpleNamespace для заданной категории.

        Args:
            category_name (str): Название категории для получения.

        Returns:
            Optional[SimpleNamespace]: Объект SimpleNamespace, представляющий категорию, или None, если не найдена.

        Example:
            >>> editor = AliCampaignEditor(campaign_name='Summer Sale')
            >>> category = editor.get_category('Electronics')
            >>> print(category)  # SimpleNamespace или None
        """
        try:
            if hasattr(self.campaign.category, category_name):
                return getattr(self.campaign.category, category_name)
            else:
                logger.warning(f"Категория {category_name} не найдена в кампании.")
                return None
        except Exception as ex:
            logger.error(f"Ошибка при получении категории {category_name}.", ex, exc_info=True)
            return None

    @property
    def list_categories(self) -> Optional[List[str]]:
        """Получает список категорий в текущей кампании.

        Returns:
            Optional[List[str]]: Список названий категорий или None, если категории не найдены.

        Example:
            >>> editor = AliCampaignEditor(campaign_name='Summer Sale')
            >>> categories = editor.categories_list
            >>> print(categories)  # ['Electronics', 'Fashion', 'Home']
        """
        try:
            # Убедимся, что у кампании есть атрибут category и это SimpleNamespace
            if hasattr(self.campaign, 'category') and isinstance(self.campaign.category, SimpleNamespace):
                return list(vars(self.campaign.category).keys())
            else:
                logger.warning("Категории не найдены в кампании.")
                return None
        except Exception as ex:
            logger.error(f"Ошибка при получении списка категорий: {ex}", exc_info=True)
            return None

    async def get_category_products(
        self, category_name: str
    ) -> Optional[List[SimpleNamespace]]:
        """Чтение данных о товарах из JSON файлов для конкретной категории.

        Args:
            category_name (str): Имя категории.

        Returns:
            Optional[List[SimpleNamespace]]: Список объектов SimpleNamespace, представляющих товары.

        Example:
            >>> products = campaign.get_category_products("Electronics")
            >>> print(len(products))
            15
        """
        category_path = None
        json_filenames = None
        products = []
        try:
            category_path = (
                self.base_path
                / "category"
                / category_name
                / f"{self.language}_{self.currency}"
            )
            json_filenames = await get_filenames_from_directory (category_path, extensions="json")

            if json_filenames:
                for json_filename in json_filenames:
                    product_data = j_loads_ns(category_path / json_filename)
                    product = SimpleNamespace(**vars(product_data))
                    products.append(product)
                return products
            else:
                logger.error(
                    f"JSON файлы не найдены для {category_name=} в {category_path=}.\nНачинаем подготовку категории"
                )
                self.process_category_products(category_name)
                return None
        except Exception as ex:
            logger.error(f"Ошибка при получении товаров категории {category_name}: {ex}", exc_info=True)
            return None