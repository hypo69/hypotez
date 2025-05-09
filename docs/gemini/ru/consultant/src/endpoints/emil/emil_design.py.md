### Анализ кода модуля `emil_design`

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Четкая структура модуля с использованием dataclasses для конфигурации.
  - Использование `j_loads` и `j_loads_ns` для загрузки JSON-конфигураций.
  - Применение `logger` для логирования.
  - Документирование основных классов и функций.
  - Использование `asyncio` для асинхронных операций.
- **Минусы**:
  - Не все функции и методы имеют подробное описание в docstring.
  - Смешанный стиль кавычек (использование как одинарных, так и двойных).
  - В docstring есть незавершенные предложения и отсутствует единообразие в описании параметров.
  - Некоторые комментарии содержат местоимения, такие как "я".
  - Не все переменные аннотированы типами.
  - Использование двойных кавычек в некоторых местах, тогда как нужно использовать одинарные.
  - В некоторых блоках `try...except` отсутствует конкретная обработка исключений.
  - Не везде используется `exc_info=True` при логировании ошибок.
  - Присутствует код, закомментированный для выполнения.

**Рекомендации по улучшению:**

1.  **Docstrings**:
    *   Дополнить docstrings для всех функций и методов, включая описание аргументов, возвращаемых значений и возможных исключений.
    *   Перевести все docstrings на русский язык и использовать формат, указанный в инструкции.
    *   В docstrings избегать общих фраз, таких как "Функция выполняет некоторое действие". Вместо этого указывать конкретное действие, например, "Функция извлекает данные из API".

2.  **Комментарии**:
    *   Избегать использования местоимений, таких как "я", в комментариях.
    *   Уточнить и конкретизировать комментарии, чтобы они точно описывали назначение кода.

3.  **Форматирование кода**:
    *   Привести весь код к единому стилю с использованием одинарных кавычек.
    *   Убедиться, что все переменные и параметры функций имеют аннотации типов.
    *   Соблюдать PEP8 для форматирования кода, включая пробелы вокруг операторов.

4.  **Обработка исключений**:
    *   Добавить конкретную обработку исключений в блоках `try...except`, где это необходимо.
    *   Всегда использовать `exc_info=True` при логировании ошибок для получения полной информации об исключении.

5.  **Конфигурация**:
    *   Убедиться, что все параметры конфигурации загружаются корректно и имеют понятные значения по умолчанию.

6.  **Использование webdriver**:
    *   Проверить использование `webdriver` и убедиться, что все локаторы определены правильно и эффективно.

7.  **Логирование**:
    *   Проверить, что все важные события и ошибки логируются с достаточным уровнем детализации.

8.  **Удалить неиспользуемый код**:
    *   Удалить или закомментировать неиспользуемый код, чтобы избежать путаницы.

9. **Переименования переменных**:
    *  Переименовать переменные, которые не соответствуют стандартам Python (например, `d` в `driver`).

**Оптимизированный код:**

```python
## \file /src/endpoints/emil/emil_design.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для управления и обработки изображений, а также продвижения в Facebook и PrestaShop. Относится к магазину `emil-design.com`
=================================
Основные возможности:
    - Описание изображений с использованием Gemini AI.
    - Загрузка описаний товаров в PrestaShop.
Классы:
    `Config` - Класс конфигурации для EmilDesign, содержащий параметры API и настройки режима работы.
    `EmilDesign` - Класс для управления и продвижения изображений через различные платформы.
"""

import os
import asyncio
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Optional, List
from dataclasses import dataclass, field

import header
from header import __root__

# External modules
from src import gs
from src.suppliers.suppliers_list import *
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_prefix, get_graber_by_supplier_url
from src.webdriver.driver import Driver
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

from src import USE_ENV  # <- True - использую переменные окружения, False - использую параметры из keepass


@dataclass
class Config:
    """Класс конфигурации для EmilDesign."""

    ENDPOINT: str = 'emil'
    MODE: str = 'dev'
    """
    MODE (str) = определяет конечную точку API
    принимаемые значения:
    `dev` - dev.emil_design.com prestashop 1.7
    `dev8` - dev8.emil_design.com prestashop 8
    `prod` - emil_design.com prestashop 1.7 <- ⚠️ Внимание!  Рабочий магазин!
    """
    POST_FORMAT = 'XML'
    API_DOMAIN: str = ''
    API_KEY: str = ''

    if USE_ENV:
        from dotenv import load_dotenv

        load_dotenv()
        API_DOMAIN = os.getenv('HOST')
        API_KEY = os.getenv('API_KEY')

    elif MODE == 'dev':
        API_DOMAIN = gs.credentials.presta.client.dev_emil_design.api_domain
        API_KEY = gs.credentials.presta.client.dev_emil_design.api_key

    elif MODE == 'dev8':
        API_DOMAIN = gs.credentials.presta.client.dev8_emil_design.api_domain
        API_KEY = gs.credentials.presta.client.dev8_emil_design.api_key

    elif MODE == 'prod':
        API_DOMAIN = gs.credentials.presta.client.emil_design.api_domain
        API_KEY = gs.credentials.presta.client.emil_design.api_key

    else:
        # `DEV` для API устанавливается если MODE пустой или имеет невалидное значение
        MODE = 'dev'
        API_DOMAIN = gs.credentials.presta.client.dev_emil_design.api_domain
        API_KEY = gs.credentials.presta.client.dev_emil_design.api_key

    suppliers: list = j_loads(__root__ / 'src' / 'endpoints' / 'emil' / 'emil.json')['suppliers']


class EmilDesign:
    """Класс для управления и продвижения изображений через различные платформы."""

    gemini: Optional[GoogleGenerativeAi] = None
    openai: Optional[OpenAIModel] = None
    base_path: Path = gs.path.endpoints / Config.ENDPOINT
    config: SimpleNamespace = j_loads_ns(base_path / f'{Config.ENDPOINT}.json')
    data_path: Path = Path(gs.path.external_storage, Config.ENDPOINT)
    gemini_api: str = os.getenv('GEMINI_API') if USE_ENV else gs.credentials.gemini.emil
    presta_api: str = os.getenv('PRESTA_API') if USE_ENV else gs.credentials.presta.client.emil_design.api_key
    presta_domain: str = os.getenv('PRESTA_URL') if USE_ENV else gs.credentials.presta.client.emil_design.api_domain

    async def process_suppliers(self, supplier_prefix: Optional[str | List[str]] = '') -> bool:
        """Обрабатывает поставщиков на основе предоставленного префикса.

        Args:
            supplier_prefix (Optional[str | List[str]], optional): Префикс для поставщиков. По умолчанию ''.

        Returns:
            bool: True, если обработка успешна, False в противном случае.

        Raises:
            Exception: Если произошла ошибка во время обработки поставщиков.
        """
        try:
            if supplier_prefix:
                supplier_prefix = supplier_prefix if isinstance(supplier_prefix, list) else [supplier_prefix]
            else:
                supplier_prefix = Config.suppliers

            for prefix in supplier_prefix:
                graber = get_graber_by_supplier_prefix(prefix)
                if not graber:
                    logger.warning(f'Не найден грабер для префикса: {prefix}')
                    continue
                await graber.process_scenarios_async()
                logger.info(f'Обработка поставщика с префиксом: {prefix}')
                graber.process_supplier_scenarios_async()
            return True
        except Exception as ex:
            logger.error(f'Ошибка при обработке поставщиков: {ex}', exc_info=True)
            return False

    def describe_images(
        self,
        lang: str,
        models: dict = {
            'gemini': {'model_name': 'gemini-1.5-flash'},
            'openai': {'model_name': 'gpt-4o-mini', 'assistant_id': 'asst_uDr5aVY3qRByRwt5qFiMDk43'},
        },
    ) -> None:
        """Описывает изображения на основе предоставленных инструкций и примеров.

        Args:
            lang (str): Язык для описания.
            models (dict, optional): Конфигурация моделей. По умолчанию модели Gemini и OpenAI.

        Returns:
            None

        Raises:
            FileNotFoundError: Если файлы инструкций не найдены.
            Exception: Если произошла ошибка во время обработки изображений.
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
                logger.info(f'Начинаем обработку файла {img}\n')

                raw_img_data = get_raw_image_data(images_dir / img)
                response = self.gemini.describe_image(image=raw_img_data, mime_type='image/jpeg', prompt=prompt)
                #  Обработка ответа
                if not response:
                    logger.debug(f'Не удалось получить описание для {img}')
                    #  Обработка ошибки получения описания
                else:
                    response_dict: dict = (
                        j_loads(response)[0] if isinstance(j_loads(response), list) else j_loads(response)
                    )
                    response_dict['local_image_path'] = str(images_dir / img)
                    j_dumps(response_dict, self.data_path / f'{img}.json')
                    #  Список уже обработанных изображений
                    described_images.append(str(images_dir / img))
                    save_text_file(described_images_path, described_images)

                time.sleep(15)  # Задержка между запросами
        except FileNotFoundError as ex:
            logger.error(f'Файл инструкции не найден: {ex}', exc_info=True)
        except Exception as ex:
            logger.error(f'Ошибка при обработке изображения: {ex}', exc_info=True)

    async def promote_to_facebook(self) -> None:
        """Продвигает изображения и их описания в Facebook.

        Args:
            None

        Returns:
            None

        Raises:
            Exception: Если произошла ошибка во время продвижения в Facebook.
        """
        try:
            driver = Driver(Chrome)
            driver.get_url(r'https://www.facebook.com/groups/1080630957030546')
            messages = j_loads_ns(self.base_path / 'images_descritpions_he.json')

            for m in messages:
                message = SimpleNamespace(
                    title=f'{m.parent}\n{m.category}',
                    description=m.description,
                    products=SimpleNamespace(local_image_path=[m.local_image_path]),
                )
                post_message(driver, message, without_captions=True)
        except Exception as ex:
            logger.error(f'Ошибка при продвижении в Facebook:', ex, exc_info=True)

    def upload_described_products_to_prestashop(
        self, products_list: Optional[List[SimpleNamespace]] = None, id_lang: Optional[int | str] = 2, *args, **kwargs
    ) -> bool:
        """Загружает информацию о товаре в PrestaShop.

        Args:
            products_list (Optional[List[SimpleNamespace]], optional): Список информации о товарах. По умолчанию None.
            id_lang (Optional[int | str], optional): ID языка для базы данных PrestaShop.
            Обычно языки назначаются в таком порядке: 1 - en; 2 - he; 3 - ru.
            Важно проверить порядок языков в целевой базе данных.
            Образец кода для получения словаря языков из конкретной базы данных:
            >>import language
            >>lang_class = PrestaLanguage()
            >>print(lang_class.get_languages_schema())

        Returns:
            bool: True, если загрузка успешна, False в противном случае.

        Raises:
            FileNotFoundError: Если файл локалей не найден.
            Exception: Если произошла ошибка во время загрузки в PrestaShop.
        """
        try:

            products_files_list: list[str] = get_filenames_from_directory(self.data_path, ext='json')
            products_list: list[SimpleNamespace] = [j_loads_ns(self.data_path / f) for f in products_files_list]
            presta_product: PrestaProduct = PrestaProduct(api_domain=Config.API_DOMAIN, api_key=Config.API_KEY)

            """Важно! При загрузке товаров в PrestaShop необходимо указать язык, на котором будут отображаться названия и характеристики товара.
            В данном случае язык по умолчанию - иврит (he = 2), но также можно указать английский (en) или русский (ru).
            Индексы могут меняться в зависимости от настроек магазина. Обычно выставляется индекс `1` для английского, `2` для иврита и `3` для русского.
            Таблица с индексами для` emil-design.com` находится в файле `locales.json` в папке `shop_locales`
            """

            lang_ns: SimpleNamespace = j_loads_ns(
                Path(__root__, 'src', 'endpoints', 'emil', 'shop_locales', 'locales.json')
            )
            if isinstance(id_lang, str) and id_lang in ('en', 'he', 'ru'):
                id_lang = getattr(lang_ns, id_lang)
            else:
                try:
                    id_lang = int(id_lang)
                except Exception as ex:
                    logger.error(f'Неправильный формат маркера языка.', ex)
                    #  Обработка неправильного формата маркера языка

            for product_ns in products_list:
                product_fields: ProductFields = ProductFields(id_lang)
                product_fields.name = product_ns.name
                product_fields.description = product_ns.description
                product_fields.price = 100.000
                product_fields.wholesale_price = 100.000
                product_fields.id_category_default = product_ns.id_category_default
                product_fields.additional_category_append(product_ns.id_category_parent)
                product_fields.id_supplier = 11366
                product_fields.local_image_path = product_ns.local_image_path
                presta_product.add_new_product(product_fields)
            return True
        except FileNotFoundError as ex:
            logger.error(f'Файл локалей не найден:', ex, exc_info=True)
            return False
        except Exception as ex:
            logger.error(f'Ошибка при загрузке в PrestaShop:', ex, exc_info=True)
            return False


if __name__ == '__main__':
    emil = EmilDesign()
    asyncio.run(emil.process_suppliers())
    # emil.describe_images(lang='he')
    # emil.upload_described_products_to_prestashop(id_lang = 2)
    # asyncio.run(emil.upload_described_products_to_prestashop_async(lang='he'))
    # emil.describe_images('he')