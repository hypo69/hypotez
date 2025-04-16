### **Анализ кода модуля `emil_design.py`**

## Качество кода:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
  - Код достаточно хорошо структурирован и содержит docstring для большинства функций и классов.
  - Используется логгирование с помощью модуля `logger`.
  - Присутствует обработка исключений.
- **Минусы**:
  - Docstring написаны на английском языке. Требуется перевод на русский.
  - Не все переменные аннотированы типами.
  - Используются устаревшие конструкции, такие как `Union`.
  - Не везде используются `j_loads` и `j_dumps` для работы с JSON.
  - Нарушены стандарты PEP8 в форматировании (отсутствие пробелов вокруг операторов присваивания).

## Рекомендации по улучшению:

1.  **Перевод docstring на русский язык**: Необходимо перевести все docstring на русский язык, чтобы соответствовать требованиям.
2.  **Добавление аннотаций типов**: Добавить аннотации типов для всех переменных и параметров функций.
3.  **Замена `Union` на `|`**: Заменить все экземпляры `Union` на `|` для соответствия современному синтаксису Python.
4.  **Использование `j_loads` и `j_dumps`**: Использовать `j_loads` и `j_dumps` для работы с JSON файлами.
5.  **Форматирование кода**: Исправить форматирование кода в соответствии со стандартами PEP8 (добавить пробелы вокруг операторов присваивания).
6.  **Улучшение комментариев**: Сделать комментарии более подробными и конкретными, избегая общих фраз.
7.  **Обработка исключений**: Использовать `ex` вместо `e` в блоках обработки исключений.
8.  **Удалить неиспользуемые импорты**: Удалить неиспользуемые импорты `header`.

## Оптимизированный код:

```python
                ## \file /src/endpoints/emil/emil_design.py
# -*- coding: utf-8 -*-\
#! .pyenv/bin/python3

"""
Модуль для управления и обработки изображений, а также продвижения в Facebook и PrestaShop. Относится к магазину `emil-design.com`
=================================
Основные возможности:
    - <инструкция для модели gemini:Описание изображений с использованием Gemini AI.>
    - <инструкция для модели gemini:Загрузка описаний продуктов в PrestaShop.>
    - ..... <далее, если есть>
Классы:
    `Config` - <инструкция для модели gemini: Дай полное описание и назначение этого класса>
    `EmilDesign` - <инструкция для модели: Дай полное описание и назначение этого класса>
    - ..... <далее, если есть>
"""

import os
import asyncio
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Optional, List
from dataclasses import dataclass, field

# from header import __root__ # Удален неиспользуемый импорт

# External modules
from src import gs
from src.webdriver.driver import Driver
from src.webdriver.chrome import Chrome
from src.ai.gemini import GoogleGenerativeAi
from src.ai.openai.model import OpenAIModel
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


class Config:
    """Конфигурационный класс для EmilDesign."""

    ENDPOINT: str = 'emil'
    MODE: str = 'dev'
    """
    MODE (str) = определяет конечную точку API
    принимаемые значения:
    `dev` - dev.emil_design.com prestashop 1.7
    `dev8` - dev8.emil_design.com prestashop 8
    `prod` - emil_design.com prestashop 1.7 <- ⚠️ Внимание!  Рабочий магазин!
    """
    POST_FORMAT: str = 'XML'
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


class EmilDesign:
    """Датакласс для разработки и продвижения изображений через различные платформы."""

    gemini: Optional[GoogleGenerativeAi] = None
    openai: Optional[OpenAIModel] = None
    base_path: Path = gs.path.endpoints / Config.ENDPOINT
    config: SimpleNamespace = j_loads_ns(base_path / f'{Config.ENDPOINT}.json')
    data_path: Path = getattr(gs.path, config.storage, 'external_storage') / Config.ENDPOINT
    gemini_api: str = os.getenv('GEMINI_API') if USE_ENV else gs.credentials.gemini.emil
    presta_api: str = os.getenv('PRESTA_API') if USE_ENV else gs.credentials.presta.client.emil_design.api_key
    presta_domain: str = os.getenv('PRESTA_URL') if USE_ENV else gs.credentials.presta.client.emil_design.api_domain

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
            models (dict, optional): Конфигурация моделей. По умолчанию используются модели Gemini и OpenAI.

        Returns:
            None

        Raises:
            FileNotFoundError: Если файлы инструкций не найдены.
            Exception: Если возникает ошибка во время обработки изображений.

        Example:
            >>> emil = EmilDesign()
            >>> emil.describe_images('he')
        """
        try:
            # Чтение системной инструкции
            system_instruction: str = Path(self.base_path / 'instructions' / f'system_instruction.{lang}.md').read_text(
                encoding='UTF-8'
            )
            # Чтение запроса
            prompt: str = Path(self.base_path / 'instructions' / f'hand_made_furniture.{lang}.md').read_text(
                encoding='UTF-8'
            )
            # Чтение категорий мебели
            furniture_categories: str = (
                Path(self.base_path / 'categories' / 'main_categories_furniture.json')
                .read_text(encoding='UTF-8')
                .replace(r'\n', '')
                .replace(r'\t', '')
            )
            system_instruction += furniture_categories + prompt

            output_json: Path = self.data_path / f'out_{gs.now}_{lang}.json'
            described_images_path: Path = self.data_path / 'described_images.txt'
            described_images: list[str] = read_text_file(described_images_path, as_list=True) or []
            images_dir: Path = self.data_path / 'images' / 'furniture_images'
            images_files_list: list[str] = get_filenames_from_directory(images_dir)
            images_to_process: list[str] = [
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

                raw_img_data: bytes = get_raw_image_data(images_dir / img)
                response: str = self.gemini.describe_image(image=raw_img_data, mime_type='image/jpeg', prompt=prompt)
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
        except FileNotFoundError as ex:
            logger.error(f'Instruction file not found: {ex}', exc_info=True)
        except Exception as ex:
            logger.error(f'Error while processing image: {ex}', exc_info=True)

    async def promote_to_facebook(self) -> None:
        """Продвигает изображения и их описания в Facebook.

        Args:
            None

        Returns:
            None

        Raises:
            Exception: Если возникает ошибка во время продвижения в Facebook.
        """
        try:
            # Создание инстанса драйвера Chrome
            d: Driver = Driver(Chrome)
            d.get_url(r'https://www.facebook.com/groups/1080630957030546')
            messages: SimpleNamespace = j_loads_ns(self.base_path / 'images_descritions_he.json')

            for m in messages:
                message: SimpleNamespace = SimpleNamespace(
                    title=f'{m.parent}\n{m.category}',
                    description=m.description,
                    products=SimpleNamespace(local_image_path=[m.local_image_path]),
                )
                post_message(d, message, without_captions=True)
        except Exception as ex:
            logger.error('Error while promoting to Facebook:', ex, exc_info=True)

    def upload_described_products_to_prestashop(
        self, products_list: Optional[List[SimpleNamespace]] = None, id_lang: Optional[int | str] = 2, *args, **kwards
    ) -> bool:
        """Загружает информацию о продукте в PrestaShop.

        Args:
            products_list (Optional[List[SimpleNamespace]], optional): Список информации о продуктах. По умолчанию None.
            id_lang (Optional[int | str], optional): ID языка для баз данных PrestaShop.
            Обычно я назначаю языки в таком порядке 1 - en;2 - he; 3 - ru.
            Важно проверить порядок языков в целевой базе данных.
            Вот образец кода для получения словаря языков из конкретной базы данных
            >>import language
            >>lang_class = PrestaLanguage()
            >>print(lang_class.get_languages_schema())

        Returns:
            bool: True, если загрузка прошла успешно, False в противном случае.

        Raises:
            FileNotFoundError: Если файл locales не найден.
            Exception: Если возникает ошибка во время загрузки в PrestaShop.
        """
        try:

            products_files_list: list[str] = get_filenames_from_directory(self.data_path, ext='json')
            products_list: list[SimpleNamespace] = [j_loads_ns(self.data_path / f) for f in products_files_list]
            p: PrestaProduct = PrestaProduct(api_domain=Config.API_DOMAIN, api_key=Config.API_KEY)

            """Важно! При загрузке товаров в PrestaShop, необходимо указать язык, на котором будут отображаться названия и характеристики товара.
            в данном случае, язык по умолчанию - иврит (he = 2), но также можно указать английский (en) или русский (ru)
            индексы могут меняться в зависимости от настроек магазина. Обычно я выставляю индекс `1` для английского, `2` для иврита и `3` для русского.
            таблица с индексами для` emil-design.com` находится в файле `locales.json` в папке `shop_locales`
            """

            lang_ns: SimpleNamespace = j_loads_ns(
                gs.path.endpoints / 'emil' / 'shop_locales' / 'locales.json'
            )
            if isinstance(id_lang, str) and id_lang in ('en','he','ru'):
                id_lang = getattr(lang_ns, id_lang)
            else:
                try:
                    id_lang = int(id_lang)
                except Exception as ex:
                    logger.error('Неправильный формат маркера языка. ',ex)
                    ...

            for product_ns in products_list:
                f: ProductFields = ProductFields(id_lang)
                f.name = product_ns.name
                f.description = product_ns.description
                f.price = '100'
                f.id_category_default = product_ns.id_category_default
                f.additional_category_append(product_ns.id_category_parent)
                f.id_supplier = 11366
                f.local_image_path = product_ns.local_image_path
                p.add_new_product(f)
            return True
        except FileNotFoundError as ex:
            logger.error('Locales file not found: ',ex, exc_info=True)
            return False
        except Exception as ex:
            logger.error('Error while uploading to PrestaShop: ',ex, exc_info=True)
            return False


if __name__ == '__main__':
    emil: EmilDesign = EmilDesign()
    emil.upload_described_products_to_prestashop(id_lang = 2)
    # asyncio.run(emil.upload_described_products_to_prestashop_async(lang='he'))
    # emil.describe_images('he')