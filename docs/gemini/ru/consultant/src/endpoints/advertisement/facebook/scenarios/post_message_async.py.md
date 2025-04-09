### **Анализ кода модуля `post_message_async.py`**

## \file /src/endpoints/advertisement/facebook/scenarios/post_message_async.py

Модуль содержит функции для автоматизации процесса публикации рекламных сообщений в Facebook, включая загрузку медиафайлов и добавление описаний.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код разбит на отдельные функции, что облегчает понимание и поддержку.
  - Используется асинхронность для выполнения задач, что позволяет повысить производительность.
  - Присутствуют логирование ошибок с использованием `logger`.
  - Используются `SimpleNamespace` для хранения данных, что упрощает доступ к атрибутам.
- **Минусы**:
  - В некоторых местах отсутствуют аннотации типов.
  - Docstrings на английском языке.
  - Не везде используется `j_loads_ns` для загрузки JSON файлов.
  - Не все ошибки обрабатываются с логированием.
  - Не всегда передается ошибка в logger.error

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов**: Добавить аннотации типов для всех переменных и параметров функций.
2.  **Перевести docstrings на русский язык**: Перевести все docstrings на русский язык для соответствия стандартам проекта.
3.  **Использовать `j_loads_ns` для загрузки JSON**: Заменить стандартное открытие файла и `json.load` на `j_loads_ns`.
4.  **Добавить логирование ошибок**: Добавить логирование ошибок во все блоки `try...except` с передачей информации об исключении.
5.  **Улучшить обработку ошибок**: Проверять возвращаемые значения `d.execute_locator` и логировать ошибки, если операция не удалась.
6.  **Улучшить docstring для внутренних функций** Добавить docstring для `handle_product` c подробным описанием работы функции, ее аргументов и возвращаемых значений.
7.  **Исправить опечатку**: Исправить опечатку в `edit_uloaded_media_button`. Правильно `edit_uploaded_media_button`.
8.  **Передавать ошибки в `logger.error`** Всегда передавать ошибки в `logger.error` вторым аргументом `logger.error("Error in media upload", ex, exc_info=True)`.

**Оптимизированный код:**

```python
## \file /src/endpoints/advertisement/facebook/scenarios/post_message_async.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для публикации сообщения из `aliexpress` промо
=====================================================

Модуль содержит асинхронные функции для автоматизации процесса публикации рекламных сообщений в Facebook,
включая загрузку медиафайлов и добавление описаний.
"""

import time
import asyncio
from pathlib import Path
from types import SimpleNamespace
from typing import Dict, List, Optional
from selenium.webdriver.remote.webelement import WebElement
from src import gs
from src.webdriver.driver import Driver
from src.utils.jjson import j_loads_ns
from src.logger.logger import logger

# Загрузка локаторов из JSON файла.
locator: SimpleNamespace = j_loads_ns(
    Path(gs.path.src / 'endpoints' / 'advertisement' / 'facebook' / 'locators' / 'post_message.json')
)

def post_title(d: Driver, category: SimpleNamespace) -> Optional[bool]:
    """Отправляет заголовок и описание кампании в поле сообщения.

    Args:
        d (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
        category (SimpleNamespace): Объект, содержащий заголовок и описание для отправки.

    Returns:
        Optional[bool]: `True`, если заголовок и описание были успешно отправлены, иначе `None`.

    Example:
        >>> driver = Driver(...)
        >>> category = SimpleNamespace(title="Campaign Title", description="Campaign Description")
        >>> post_title(driver, category)
        True
    """
    # Прокрутка страницы назад
    if not d.scroll(1, 1200, 'backward'):
        logger.error('Scroll failed during post title')
        return None

    # Открытие поля "add post"
    if not d.execute_locator(locator.open_add_post_box):
        logger.error('Failed to open \'add post\' box')
        return None

    # Формирование сообщения с заголовком и описанием
    message: str = f"{category.title}; {category.description};"

    # Добавление сообщения в поле "post box"
    if not d.execute_locator(locator.add_message, message):
        logger.error(f'Failed to add message to post box: {message=}')
        return None

    return True


async def upload_media(d: Driver, products: List[SimpleNamespace], no_video: bool = False) -> Optional[bool]:
    """Асинхронно загружает медиафайлы в секцию изображений и обновляет подписи.

    Args:
        d (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
        products (List[SimpleNamespace]): Список продуктов, содержащих пути к медиафайлам.
        no_video (bool): Флаг, указывающий, следует ли избегать загрузки видео. По умолчанию `False`.

    Returns:
        Optional[bool]: `True`, если медиафайлы были успешно загружены, иначе `None`.

    Raises:
        Exception: Если произошла ошибка во время загрузки медиафайлов или обновления подписей.

    Example:
        >>> driver = Driver(...)
        >>> products = [SimpleNamespace(local_image_path='path/to/image.jpg', ...)]
        >>> await upload_media(driver, products)
        True
    """
    # Шаг 1: Открытие формы "add media". Она может быть уже открыта.
    if not d.execute_locator(locator.open_add_foto_video_form):
        logger.error('Не удалось открыть форму добавления медиа')
        return None
    d.wait(0.5)

    # Шаг 2: Проверка, что products является списком.
    products: List[SimpleNamespace] = products if isinstance(products, list) else [products]
    ret: bool = True

    # Итерация по продуктам и загрузка медиа.
    for product in products:
        media_path: str = product.local_video_path if hasattr(product, 'local_video_path') and not no_video else product.local_image_path
        try:
            # Загрузка медиафайла.
            if d.execute_locator(locator.foto_video_input, media_path):
                d.wait(1.5)
            else:
                logger.error(f'Ошибка загрузки изображения {media_path=}')
                return None
        except Exception as ex:
            logger.error('Error in media upload', ex, exc_info=True)
            return None

    # Шаг 3: Обновление подписей для загруженных медиа.
    if not d.execute_locator(locator.edit_uploaded_media_button):
        logger.error(f'Ошибка нажатия на кнопку редактирования медиа {media_path=}')
        return None
    uploaded_media_frame: WebElement | List[WebElement] | None = d.execute_locator(locator.uploaded_media_frame)
    uploaded_media_frame: WebElement = uploaded_media_frame[0] if isinstance(uploaded_media_frame, list) else uploaded_media_frame
    d.wait(0.3)

    textarea_list: List[WebElement] | None = d.execute_locator(locator.edit_image_properties_textarea)
    if not textarea_list:
        logger.error('Не нашлись поля ввода подписи к изображениям')
        return None
    # Асинхронное обновление подписей к изображениям.
    await update_images_captions(d, products, textarea_list)

    return ret


async def update_images_captions(d: Driver, products: List[SimpleNamespace], textarea_list: List[WebElement]) -> None:
    """Асинхронно добавляет описания к загруженным медиафайлам.

    Args:
        d (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
        products (List[SimpleNamespace]): Список продуктов с деталями для обновления.
        textarea_list (List[WebElement]): Список текстовых полей, куда добавляются подписи.

    Raises:
        Exception: Если произошла ошибка при обновлении подписей медиафайлов.
    """
    local_units: SimpleNamespace = j_loads_ns(Path(gs.path.src / 'advertisement' / 'facebook' / 'scenarios' / 'translations.json'))

    def handle_product(product: SimpleNamespace, textarea_list: List[WebElement], i: int) -> Optional[bool]:
        """Обрабатывает обновление подписей медиафайлов для одного продукта синхронно.

        Args:
            product (SimpleNamespace): Продукт для обновления.
            textarea_list (List[WebElement]): Список текстовых полей, куда добавляются подписи.
            i (int): Индекс продукта в списке.

        Returns:
            Optional[bool]: Возвращает `True` в случае успешного обновления подписи, иначе `None`.
        """
        direction: str = getattr(local_units.LOCALE, product.language, "LTR")
        message: str = ""

        # Добавление деталей продукта в сообщение.
        try:
            if direction == "LTR":
                if hasattr(product, 'product_title'):
                    message += f"{product.product_title}\n"
                if hasattr(product, 'original_price'):
                    message += f"{getattr(local_units.original_price, product.language)}: {product.original_price}\n"
                if hasattr(product, 'sale_price'):
                    message += f"{getattr(local_units.sale_price, product.language)}: {product.sale_price}\n"
                if hasattr(product, 'discount'):
                    message += f"{getattr(local_units.discount, product.language)}: {product.discount}\n"
                if hasattr(product, 'evaluate_rate'):
                    message += f"{getattr(local_units.evaluate_rate, product.language)}: {product.evaluate_rate}\n"
                if hasattr(product, 'promotion_link'):
                    message += f"{getattr(local_units.promotion_link, product.language)}: {product.promotion_link}\n"
                if hasattr(product, 'tags'):
                    message += f"{getattr(local_units.tags, product.language)}: {product.tags}\n"
                message += f"{getattr(local_units.COPYRIGHT, product.language)}"

            else:  # RTL direction
                if hasattr(product, 'product_title'):
                    message += f"\n{product.product_title}"
                if hasattr(product, 'original_price'):
                    message += f"\n{product.original_price} :{getattr(local_units.original_price, product.language)}"
                if hasattr(product, 'discount'):
                    message += f"\n{product.discount} :{getattr(local_units.discount, product.language)}"
                if hasattr(product, 'sale_price'):
                    message += f"\n{product.sale_price} :{getattr(local_units.sale_price, product.language)}"
                if hasattr(product, 'evaluate_rate'):
                    message += f"\n{product.evaluate_rate} :{getattr(local_units.evaluate_rate, product.language)}"
                if hasattr(product, 'promotion_link'):
                    message += f"\n{product.promotion_link} :{getattr(local_units.promotion_link, product.language)}"
                if hasattr(product, 'tags'):
                    message += f"\n{product.tags} :{getattr(local_units.tags, product.language)}"
                message += f"\n{getattr(local_units.COPYRIGHT, product.language)}"

        except Exception as ex:
            logger.error("Error in message generation", ex, exc_info=True)
            return None

        # Отправка сообщения в textarea.
        try:
            textarea_list[i].send_keys(message)
            return True
        except Exception as ex:
            logger.error("Error in sending keys to textarea", ex, exc_info=True)
            return None

    # Обработка продуктов и обновление их подписей асинхронно.
    for i, product in enumerate(products):
        await asyncio.to_thread(handle_product, product, textarea_list, i)


async def promote_post(d: Driver, category: SimpleNamespace, products: List[SimpleNamespace], no_video: bool = False) -> Optional[bool]:
    """Управляет процессом продвижения поста с заголовком, описанием и медиафайлами.

    Args:
        d (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
        category (SimpleNamespace): Детали категории, используемые для заголовка и описания поста.
        products (List[SimpleNamespace]): Список продуктов, содержащих медиа и детали для публикации.
        no_video (bool): Флаг, указывающий, следует ли избегать загрузки видео. По умолчанию `False`.

    Returns:
        Optional[bool]: `True`, если пост был успешно продвинут, иначе `None`.

    Example:
        >>> driver = Driver(...)
        >>> category = SimpleNamespace(title="Campaign Title", description="Campaign Description")
        >>> products = [SimpleNamespace(local_image_path='path/to/image.jpg', ...)]
        >>> await promote_post(driver, category, products)
    """
    if not post_title(d, category):
        logger.error("Не удалось установить заголовок поста")
        return None
    d.wait(0.5)

    if not await upload_media(d, products, no_video):
        logger.error("Не удалось загрузить медиа")
        return None
    if not d.execute_locator(locator.finish_editing_button):
        logger.error("Не удалось нажать на кнопку завершения редактирования")
        return None
    if not d.execute_locator(locator.publish):
        logger.error("Не удалось нажать на кнопку публикации")
        return None
    return True