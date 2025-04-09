### **Анализ кода модуля `post_message_async.py`**

## \file /src/endpoints/advertisement/facebook/scenarios/post_message_async.py

Модуль содержит асинхронные функции для публикации рекламных сообщений в Facebook, включая загрузку медиафайлов и добавление описаний к ним.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Четкая структура функций, разделение задач.
    - Использование `SimpleNamespace` для хранения данных.
    - Логирование ошибок.
- **Минусы**:
    - Некоторые docstring на английском языке.
    - Не все переменные аннотированы типами.
    - Не везде используется `logger.error` с передачей исключения `ex`.
    - Отсутствует обработка некоторых возможных исключений.

**Рекомендации по улучшению:**

1.  **Документация**:
    *   Перевести все docstring на русский язык, следуя инструкциям.
    *   Улучшить описание `Args` и `Returns` в docstring, чтобы они были более информативными.
    *   Добавить примеры использования для всех функций, где это возможно.

2.  **Обработка ошибок**:
    *   Убедиться, что все блоки `try...except` содержат `logger.error` с передачей исключения `ex` и `exc_info=True`.
    *   Рассмотреть возможность добавления обработки специфических исключений вместо общего `Exception`.

3.  **Аннотации типов**:
    *   Добавить аннотации типов для всех переменных, где это возможно.
    *   Убедиться, что аннотации типов соответствуют фактическим типам данных.

4.  **Использование `j_loads_ns`**:
    *   Убедиться, что для чтения JSON файлов используется `j_loads_ns`.

5.  **Улучшение читаемости**:
    *   Добавить пробелы вокруг операторов присваивания.
    *   Использовать более понятные имена переменных, где это необходимо.

6.  **Сокращение дублирования кода**:
    *   Рассмотреть возможность вынесения повторяющегося кода в отдельные функции.

7.  **Улучшение логирования**:
    *   Добавить больше информативных сообщений в логи, чтобы облегчить отладку.
    *   Использовать разные уровни логирования (DEBUG, INFO, WARNING, ERROR) в зависимости от ситуации.

8.  **Использование webdriver**:
    *   Убедиться, что webdriver используется правильно, с учетом рекомендаций в инструкции.

**Оптимизированный код:**

```python
## \file /src/endpoints/advertisement/facebook/scenarios/post_message_async.py
# -*- coding: utf-8 -*

#! .pyenv/bin/python3

"""
Модуль для публикации сообщений в Facebook
==========================================

Модуль содержит асинхронные функции для публикации рекламных сообщений в Facebook, включая загрузку медиафайлов и добавление описаний к ним.
"""

import asyncio
import time
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


def post_title(d: Driver, category: SimpleNamespace) -> bool:
    """Отправляет заголовок и описание кампании в поле сообщения.

    Args:
        d (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        category (SimpleNamespace): Категория, содержащая заголовок и описание для отправки.

    Returns:
        bool: `True`, если заголовок и описание были успешно отправлены, иначе `False`.

    Example:
        >>> driver = Driver(...)
        >>> category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
        >>> post_title(driver, category)
        True
    """
    # Прокрутка страницы вверх
    if not d.scroll(1, 1200, 'backward'):
        logger.error('Ошибка при прокрутке страницы вверх во время публикации заголовка', exc_info=False)
        return False

    # Открытие поля "Добавить пост"
    if not d.execute_locator(locator.open_add_post_box):
        logger.error('Не удалось открыть поле "Добавить пост"', exc_info=False)
        return False

    # Формирование сообщения с заголовком и описанием
    message: str = f'{category.title}; {category.description};'

    # Добавление сообщения в поле поста
    if not d.execute_locator(locator.add_message, message):
        logger.error(f'Не удалось добавить сообщение в поле поста: {message=}', exc_info=False)
        return False

    return True


async def upload_media(d: Driver, products: List[SimpleNamespace], no_video: bool = False) -> bool:
    """Асинхронно загружает медиафайлы в раздел изображений и обновляет подписи.

    Args:
        d (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        products (List[SimpleNamespace]): Список продуктов, содержащих пути к медиафайлам.
        no_video (bool, optional): Если True, видео не загружаются. По умолчанию False.

    Returns:
        bool: `True`, если медиафайлы были успешно загружены, иначе `False`.

    Raises:
        Exception: Если произошла ошибка во время загрузки медиафайлов или обновления подписей.

    Example:
        >>> driver = Driver(...)
        >>> products = [SimpleNamespace(local_image_path='путь/к/изображению.jpg', ...)]
        >>> await upload_media(driver, products)
        True
    """
    # Шаг 1: Открытие формы "Добавить медиа". Она может быть уже открыта.
    if not d.execute_locator(locator.open_add_foto_video_form):
        return False
    d.wait(0.5)

    # Шаг 2: Проверка, является ли products списком.
    products: List[SimpleNamespace] = products if isinstance(products, list) else [products]
    ret: bool = True

    # Перебор продуктов и загрузка медиафайлов.
    for product in products:
        media_path: str = product.local_video_path if hasattr(product, 'local_video_path') and not no_video else product.local_image_path
        try:
            # Загрузка медиафайла.
            if d.execute_locator(locator.foto_video_input, media_path):
                d.wait(1.5)
            else:
                logger.error(f'Ошибка загрузки изображения {media_path=}')
                return False
        except Exception as ex:
            logger.error('Ошибка при загрузке медиафайла', ex, exc_info=True)
            return False

    # Шаг 3: Обновление подписей для загруженных медиафайлов.
    if not d.execute_locator(locator.edit_uloaded_media_button):
        logger.error(f'Ошибка при нажатии кнопки редактирования загруженного изображения {media_path=}')
        return False
    uploaded_media_frame = d.execute_locator(locator.uploaded_media_frame)
    uploaded_media_frame = uploaded_media_frame[0] if isinstance(uploaded_media_frame, list) else uploaded_media_frame
    d.wait(0.3)

    textarea_list: List[WebElement] = d.execute_locator(locator.edit_image_properties_textarea)
    if not textarea_list:
        logger.error('Не найдены поля ввода подписи к изображениям')
        return False
    # Асинхронное обновление подписей к изображениям.
    await update_images_captions(d, products, textarea_list)

    return ret


async def update_images_captions(d: Driver, products: List[SimpleNamespace], textarea_list: List[WebElement]) -> None:
    """Асинхронно добавляет описания к загруженным медиафайлам.

    Args:
        d (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        products (List[SimpleNamespace]): Список продуктов с деталями для обновления.
        textarea_list (List[WebElement]): Список текстовых полей, в которые добавляются подписи.

    Raises:
        Exception: Если произошла ошибка при обновлении подписей медиафайлов.
    """
    local_units: SimpleNamespace = j_loads_ns(Path(gs.path.src / 'advertisement' / 'facebook' / 'scenarios' / 'translations.json'))

    def handle_product(product: SimpleNamespace, textarea_list: List[WebElement], i: int) -> Optional[bool]:
        """Обрабатывает обновление подписей медиафайлов для одного продукта синхронно.

        Args:
            product (SimpleNamespace): Продукт для обновления.
            textarea_list (List[WebElement]): Список текстовых полей, в которые добавляются подписи.
            i (int): Индекс продукта в списке.
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
            logger.error("Ошибка при формировании сообщения", ex, exc_info=True)

        # Отправка сообщения в текстовое поле.
        try:
            textarea_list[i].send_keys(message)
            return True
        except Exception as ex:
            logger.error("Ошибка при отправке текста в textarea", ex, exc_info=True)
            return False

    # Обработка продуктов и обновление их подписей асинхронно.
    for i, product in enumerate(products):
        await asyncio.to_thread(handle_product, product, textarea_list, i)


async def promote_post(d: Driver, category: SimpleNamespace, products: List[SimpleNamespace], no_video: bool = False) -> Optional[bool]:
    """Управляет процессом продвижения поста с заголовком, описанием и медиафайлами.

    Args:
        d (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        category (SimpleNamespace): Детали категории, используемые для заголовка и описания поста.
        products (List[SimpleNamespace]): Список продуктов, содержащих медиафайлы и детали для публикации.
        no_video (bool, optional): Если True, видео не загружаются. По умолчанию False.

    Example:
        >>> driver = Driver(...)
        >>> category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
        >>> products = [SimpleNamespace(local_image_path='путь/к/изображению.jpg', ...)]
        >>> await promote_post(driver, category, products)
    """
    if not post_title(d, category):
        return False
    d.wait(0.5)

    if not await upload_media(d, products, no_video):
        return False
    if not d.execute_locator(locator.finish_editing_button):
        return False
    if not d.execute_locator(locator.publish):
        return False
    return True