### **Анализ кода модуля `ali_campaign_editor.py`**

## \file /src/suppliers/aliexpress/campaign/ali_campaign_editor.py

Модуль предоставляет редактор для рекламных кампаний на AliExpress.

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Наличие docstring для большинства функций и классов.
    - Использование аннотаций типов.
    - Использование `logger` для логирования.
- **Минусы**:
    - Не все функции имеют docstring.
    - Встречаются участки кода с `...`, что затрудняет понимание полной функциональности.
    - Не все переменные аннотированы типами.
    - Есть неиспользуемые импорты (например, `header`).
    - Docstring частично на английском языке

**Рекомендации по улучшению**:

1.  **Документация**:
    - Дополнить docstring для всех функций и методов, включая описание параметров, возвращаемых значений и возможных исключений.
    - Перевести все docstring на русский язык.
    - Описать назначение каждого атрибута класса в docstring класса.

2.  **Логирование**:
    - Указывать `exc_info=True` при логировании ошибок, чтобы получить полную трассировку стека.
    - Проверить и унифицировать стиль логирования, чтобы все сообщения были информативными и полезными для отладки.

3.  **Обработка исключений**:
    - Использовать `ex` вместо `e` в блоках `except`.

4.  **Импорты**:
    - Удалить неиспользуемые импорты (например, `header`).
    - Проверить и оптимизировать импорты, чтобы они были организованы и понятны.

5.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных, где это возможно.

6.  **Код с `...`**:
    - Заменить `...` конкретной реализацией, если это возможно, или добавить комментарии, объясняющие, что должно быть реализовано в этих местах.

7.  **Форматирование**:
    - Использовать одинарные кавычки (`'`) вместо двойных (`"`) в Python-коде.
    - Добавить пробелы вокруг операторов присваивания (`=`).

8.  **Комментарии**:
    - Сделать комментарии более подробными и понятными, избегая расплывчатых формулировок.

**Оптимизированный код**:

```python
## \file /src/suppliers/aliexpress/campaign/ali_campaign_editor.py
# -*- coding: utf-8 -*-\n

#! .pyenv/bin/python3\n

"""
Модуль для работы с редактором рекламных кампаний AliExpress
==============================================================

Модуль содержит класс :class:`AliCampaignEditor`, который используется для редактирования рекламных кампаний AliExpress,
включая добавление, удаление и обновление информации о товарах и категориях.

Пример использования:
----------------------

>>> editor = AliCampaignEditor(campaign_name="Summer Sale", language="EN", currency="USD")
>>> editor.delete_product("12345")
"""

import asyncio
import re
import shutil
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import List, Optional

from src import gs
from src.suppliers.aliexpress.campaign.ali_promo_campaign import AliPromoCampaign
from src.suppliers.aliexpress.campaign.gsheet import AliCampaignGoogleSheet
from src.suppliers.aliexpress.utils import extract_prod_ids, ensure_https
from src.utils.jjson import j_loads_ns, j_loads, j_dumps
from src.utils.convertors.csv import csv2dict
from src.utils.printer import pprint
from src.utils.file import (
    read_text_file,
    get_filenames_from_directory,
    get_directory_names,
)
from src.logger.logger import logger


class AliCampaignEditor(AliPromoCampaign):
    """Редактор для рекламных кампаний."""

    def __init__(
        self,
        campaign_name: str,
        language: Optional[str | dict] = None,
        currency: Optional[str] = None,
    ) -> None:
        """
        Инициализирует AliCampaignEditor с заданными параметрами.

        Args:
            campaign_name (str): Название кампании.
            language (Optional[str | dict], optional): Язык кампании. По умолчанию 'EN'.
            currency (Optional[str], optional): Валюта кампании. По умолчанию 'USD'.

        Raises:
            CriticalError: Если не указано ни `campaign_name`, ни `campaign_file`.

        Example:
            # 1. По параметрам кампании
            >>> editor = AliCampaignEditor(campaign_name="Summer Sale", language="EN", currency="USD")
            # 2. Загрузка из файла
            >>> editor = AliCampaignEditor(campaign_name="Summer Sale", campaign_file="EN_USD.JSON")
        """
        super().__init__(campaign_name=campaign_name, language=language, currency=currency)
        # self.google_sheet = AliCampaignGoogleSheet(campaign_name = campaign_name, language = language, currency = currency, campaign_editor = self)

    def delete_product(self, product_id: str, exc_info: bool = False) -> None:
        """
        Удаляет товар, у которого нет партнерской ссылки.

        Args:
            product_id (str): ID товара для удаления.
            exc_info (bool): Включать ли информацию об исключении в логи. По умолчанию `False`.

        Example:
            >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
            >>> editor.delete_product("12345")
        """
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
                        # TODO: save_text_file не определена. Заменить на корректную функцию.
                        # save_text_file((products_list, '\n'), prepared_product_path)
                        break
                else:
                    if record == str(product_id):
                        products_list.remove(record)
                        # TODO: save_text_file не определена. Заменить на корректную функцию.
                        # save_text_file((products_list, '\n'), product_path)
        else:
            product_path = self.category_path / 'sources' / f'{product_id}.html'
            try:
                product_path.rename(self.category_path / 'sources' / f'{product_id}_.html')
                logger.success(f'Product file {product_path=} renamed successfully.')
            except FileNotFoundError as ex:
                logger.error(f'Product file {product_path=} not found.', ex, exc_info=exc_info)
            except Exception as ex:
                logger.critical(
                    f'An error occurred while deleting the product file {product_path}.', ex, exc_info=True
                )

    def update_product(self, category_name: str, lang: str, product: dict) -> None:
        """
        Обновляет детали товара в категории.

        Args:
            category_name (str): Название категории, в которой нужно обновить товар.
            lang (str): Язык кампании.
            product (dict): Словарь с деталями товара.

        Example:
            >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
            >>> editor.update_product("Electronics", "EN", {"product_id": "12345", "title": "Smartphone"})
        """
        self.dump_category_products_files(category_name, lang, product)

    def update_campaign(self) -> None:
        """
        Обновляет свойства кампании, такие как `description`, `tags` и т.д.

        Example:
            >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
            >>> editor.update_campaign()
        """
        ...

    def update_category(self, json_path: Path, category: SimpleNamespace) -> bool:
        """
        Обновляет категорию в JSON файле.

        Args:
            json_path (Path): Путь к JSON файлу.
            category (SimpleNamespace): Объект категории для обновления.

        Returns:
            bool: True, если обновление успешно, False в противном случае.

        Example:
            >>> category = SimpleNamespace(name="New Category", description="Updated description")
            >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
            >>> result = editor.update_category(Path("category.json"), category)
            >>> print(result)  # True, если успешно
        """
        try:
            data: dict = j_loads(json_path)  # Чтение JSON данных из файла
            data['category'] = category.__dict__  # Преобразование SimpleNamespace в dict
            j_dumps(data, json_path)  # Запись обновленных JSON данных обратно в файл
            return True
        except Exception as ex:
            logger.error(f'Failed to update category {json_path}: {ex}', ex, exc_info=True)
            return False

    def get_category(self, category_name: str) -> Optional[SimpleNamespace]:
        """
        Возвращает объект SimpleNamespace для заданного имени категории.

        Args:
            category_name (str): Название категории для получения.

        Returns:
            Optional[SimpleNamespace]: Объект SimpleNamespace, представляющий категорию, или None, если категория не найдена.

        Example:
            >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
            >>> category = editor.get_category("Electronics")
            >>> print(category)  # SimpleNamespace или None
        """
        try:
            if hasattr(self.campaign.category, category_name):
                return getattr(self.campaign.category, category_name)
            else:
                logger.warning(f'Category {category_name} not found in the campaign.')
                return None
        except Exception as ex:
            logger.error(f'Error retrieving category {category_name}.', ex, exc_info=True)
            return None

    @property
    def list_categories(self) -> Optional[List[str]]:
        """
        Получает список категорий в текущей кампании.

        Returns:
            Optional[List[str]]: Список названий категорий или None, если категории не найдены.

        Example:
            >>> editor = AliCampaignEditor(campaign_name="Summer Sale")
            >>> categories = editor.categories_list
            >>> print(categories)  # ['Electronics', 'Fashion', 'Home']
        """
        try:
            # Убедимся, что кампания имеет атрибут category и это SimpleNamespace
            if hasattr(self.campaign, 'category') and isinstance(self.campaign.category, SimpleNamespace):
                return list(vars(self.campaign.category).keys())
            else:
                logger.warning('No categories found in the campaign.')
                return None
        except Exception as ex:
            logger.error(f'Error retrieving categories list: {ex}', ex, exc_info=True)
            return None

    async def get_category_products(
        self, category_name: str
    ) -> Optional[List[SimpleNamespace]]:
        """
        Чтение данных о товарах из JSON файлов для конкретной категории.

        Args:
            category_name (str): Имя категории.

        Returns:
            Optional[List[SimpleNamespace]]: Список объектов SimpleNamespace, представляющих товары.

        Example:
            >>> products = campaign.get_category_products("Electronics")
            >>> print(len(products))
            15
        """
        category_path: Path = (
            self.base_path
            / 'category'
            / category_name
            / f'{self.language}_{self.currency}'
        )
        json_filenames: list[str] | None = await get_filenames_from_directory(category_path, extensions='json')
        products: list[SimpleNamespace] = []

        if json_filenames:
            for json_filename in json_filenames:
                product_data = j_loads_ns(category_path / json_filename)
                product = SimpleNamespace(**vars(product_data))
                products.append(product)
            return products
        else:
            logger.error(
                f'No JSON files found for {category_name=} at {category_path=}.\nStart prepare category',
                exc_info=True
            )
            self.process_category_products(category_name)
            return None