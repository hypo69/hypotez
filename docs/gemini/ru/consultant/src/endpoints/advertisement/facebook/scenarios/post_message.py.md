### **Анализ кода модуля `post_message.py`**

## \file /src/endpoints/advertisement/facebook/scenarios/post_message.py

Модуль предназначен для публикации сообщений в Facebook, включая текст, медиафайлы и обработку подписей к изображениям.

**Качество кода**:

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код разбит на функции, что улучшает читаемость и упрощает поддержку.
    - Используется модуль `logger` для логирования.
    - Присутствуют docstring для большинства функций.
- **Минусы**:
    - Не все функции имеют docstring.
    - Местами отсутствует аннотация типов.
    - Присутствуют устаревшие конструкции, которые можно улучшить.
    - Есть дублирование кода, которое можно сократить.
    - Отсутствует единый стиль в оформлении docstring.

**Рекомендации по улучшению**:

1.  **Документация**:
    - Дополнить docstring для всех функций, включая `publish`.
    - Привести docstring к единому стилю, используя Markdown-формат.
    - Перевести все docstring на русский язык.
2.  **Типизация**:
    - Добавить аннотации типов для всех переменных и параметров функций, где они отсутствуют.
3.  **Логирование**:
    - Проверить и унифицировать использование `logger` во всех функциях.
    - Указывать `exc_info=True` при логировании ошибок для получения более полной информации.
4.  **Обработка исключений**:
    - Использовать `ex` вместо `e` в блоках `except`.
5.  **Улучшение читаемости**:
    - Заменить множественные проверки `if not d.execute_locator(...)` на более компактное решение.
    - Избавиться от лишних `return` в блоках `if not`, где можно сразу возвращать `False`.
6. **Использование вебдрайвера**:\
   - Убедиться, что вебдрайвер инициализируется и используется в соответствии с принятыми в проекте стандартами (через `Driver`, `Chrome`, `Firefox`, `Playwright`).
7. **Использование `j_loads_ns`**:\
   - Убедиться, что для загрузки JSON используется `j_loads_ns`.
8. **Избегать неясных формулировок**:
    - В комментариях и docstring использовать более конкретные термины, например, "извлекаем", "проверяем", "выполняем" вместо "получаем" или "делаем".

**Оптимизированный код**:

```python
                ## \file /src/endpoints/advertisement/facebook/scenarios/post_message.py
# -*- coding: utf-8 -*-\
# .pyenv/bin/python3
"""
Модуль для публикации сообщения в Facebook
===========================================

Модуль содержит функции для публикации сообщений в Facebook, включая текст и медиафайлы.
"""

import time
from pathlib import Path
from types import SimpleNamespace
from typing import Dict, List, Optional
from selenium.webdriver.remote.webelement import WebElement

from src import gs
from src.webdriver.driver import Driver
from src.utils.jjson import j_loads_ns
from src.utils.printer import pprint
from src.logger.logger import logger

# Загрузка локаторов из JSON-файла.
locator: SimpleNamespace = j_loads_ns(
    Path(gs.path.src / 'endpoints' / 'advertisement'/ 'facebook' / 'locators'/ 'post_message.json')
)

def post_title(d: Driver, message: SimpleNamespace | str) -> bool | None:
    """
    Отправляет заголовок и описание кампании в поле сообщения.

    Args:
        d (Driver): Инстанс драйвера для взаимодействия с веб-страницей.
        message (SimpleNamespace | str): Объект SimpleNamespace с атрибутами `title` и `description` или строка сообщения.

    Returns:
        bool | None: `True`, если заголовок и описание успешно отправлены, иначе `None`.
    
    Example:
        >>> driver = Driver(...)
        >>> message = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
        >>> post_title(driver, message)
        True
    """
    # Прокрутка страницы вверх
    if not d.scroll(1, 1200, 'backward'):
        logger.error("Ошибка при прокрутке страницы")
        return None

    # Открытие поля "добавить пост"
    if not d.execute_locator(locator = locator.open_add_post_box):
        logger.debug("Не удалось открыть поле 'добавить пост'")
        return None

    # Добавление сообщения в поле поста
    m =  f'{message.title}\\n{message.description}' if isinstance(message, SimpleNamespace) else message
    # if isinstance(message, SimpleNamespace) and hasattr( message,\'tags\'):
    #     m = f"{m}\\nTags: {message.tags}"

    if not d.execute_locator(locator.add_message, message = m, timeout = 5, timeout_for_event = 'element_to_be_clickable'):
        logger.debug(f"Не удалось добавить сообщение в поле поста: {m=}")
        return None

    return True

def upload_media(d: Driver, media: SimpleNamespace | List[SimpleNamespace] | str | list[str],   no_video: bool = False, without_captions:bool = False) -> bool | None:
    """
    Загружает медиафайлы в секцию изображений и обновляет подписи.

    Args:
        d (Driver): Инстанс драйвера для взаимодействия с веб-страницей.
        media (SimpleNamespace | List[SimpleNamespace] | str | list[str]): Список объектов SimpleNamespace с путями к медиафайлам или список строк с путями.
        no_video (bool): Флаг, указывающий, что видео не нужно загружать.
        without_captions (bool): Флаг, указывающий, что подписи не нужно добавлять.

    Returns:
        bool | None: `True`, если медиафайлы успешно загружены, иначе `None`.

    Raises:
        Exception: Если возникает ошибка во время загрузки медиафайлов или обновления подписей.

    Example:
        >>> driver = Driver(...)
        >>> media = [SimpleNamespace(local_image_path='path/to/image.jpg', ...)]
        >>> upload_media(driver, media)
        True
    """
    if not media:
        logger.debug("Нет медиа для сообщения!")
        return None

    # Открытие формы "добавить медиа".
    if not d.execute_locator(locator.open_add_foto_video_form):
        return None
    d.wait(0.5)

    # Преобразование media в список, если это не список.
    media_list: list = media if isinstance(media, list) else [media]
    ret: bool = True

    # Итерация по медиафайлам и их загрузка.
    for m in media_list:
        if isinstance(m, SimpleNamespace):
            try:
                media_path = m.local_video_path if hasattr(m, 'local_video_path') and not no_video else m.local_image_path
            except Exception as ex:
                logger.debug("Ошибка в поле 'local_image_path'")
                return None
        elif isinstance(m, (str, Path)):
            media_path = m
        else:
            logger.debug(f"Неподдерживаемый тип медиа: {type(m)}")
            return None
        
        try:
            # Загрузка медиафайла.
            if d.execute_locator(locator = locator.foto_video_input, message = str(media_path) , timeout = 20):
                d.wait(1.5)
            else:
                logger.error(f"Ошибка загрузки изображения {media_path=}")
                return None
        except Exception as ex:
            logger.error("Ошибка при загрузке медиа", ex, exc_info=True)
            return None
    if without_captions:
        return True

    # Обновление подписей для загруженных медиафайлов.
    if not d.execute_locator(locator.edit_uloaded_media_button):
        logger.error(f"Ошибка при нажатии на кнопку редактирования медиа {media_path=}")
        return None

    uploaded_media_frame = d.execute_locator(locator.uploaded_media_frame)
    if not uploaded_media_frame:
        logger.debug("Не нашлись поля ввода подписей к изображениям")
        return None

    uploaded_media_frame = uploaded_media_frame[0] if isinstance(uploaded_media_frame, list) else uploaded_media_frame
    d.wait(0.3)

    textarea_list = d.execute_locator(locator = locator.edit_image_properties_textarea, timeout = 10, timeout_for_event = 'presence_of_element_located' )
    if not textarea_list:
        logger.error("Не нашлись поля ввода подписи к изображениям")
        return None

    # Обновление подписей к изображениям.
    update_images_captions(d, media, textarea_list)

    return ret

def update_images_captions(d: Driver, media: List[SimpleNamespace], textarea_list: List[WebElement]) -> None:
    """
    Добавляет описания к загруженным медиафайлам.

    Args:
        d (Driver): Инстанс драйвера для взаимодействия с веб-страницей.
        media (List[SimpleNamespace]): Список объектов SimpleNamespace с деталями для обновления.
        textarea_list (List[WebElement]): Список текстовых полей, в которые добавляются подписи.

    Raises:
        Exception: Если возникает ошибка при обновлении подписей к медиафайлам.
    """
    local_units = j_loads_ns(Path(gs.path.src / 'advertisement' / 'facebook' / 'scenarios' / 'translations.json'))

    def handle_product(product: SimpleNamespace, textarea_list: List[WebElement], i: int) -> None:
        """
        Обновляет подписи к медиафайлам для одного продукта.

        Args:
            product (SimpleNamespace): Продукт для обновления.
            textarea_list (List[WebElement]): Список текстовых полей, в которые добавляются подписи.
            i (int): Индекс продукта в списке.
        """
        lang = product.language.upper()
        direction = getattr(local_units.LOCALE, lang, "LTR")
        message = ""

        # Добавление деталей продукта в сообщение.
        try:
            if direction == "LTR":
                if hasattr(product, 'product_title'):
                    message += f"{product.product_title}\\n"

                if hasattr(product, 'description'):
                    message += f'{product.description}\\n'

                if hasattr(product, 'original_price'):
                    message += f"{getattr(local_units.original_price, lang)}: {product.original_price} {product.target_original_price_currency}\\n"

                if hasattr(product, 'sale_price') and hasattr(product, 'discount') and product.discount != '0%':
                    message += f"{getattr(local_units.discount, lang)}: {product.discount}\\n"
                    message += f"{getattr(local_units.sale_price, lang)}: {product.sale_price} {product.target_original_price_currency} \\n"

                if hasattr(product, 'evaluate_rate') and product.evaluate_rate != '0.0%':
                    message += f"{getattr(local_units.evaluate_rate, lang)}: {product.evaluate_rate}\\n"

                if hasattr(product, 'promotion_link'):
                    message += f"{getattr(local_units.promotion_link, lang)}: {product.promotion_link}\\n"

                # if hasattr(product, \'tags\'):
                #     message += f"{getattr(local_units.tags, lang)}: {product.tags}\\n"
                # message += f"{getattr(local_units.COPYRIGHT, lang)}"\
                
            else:  # RTL direction
                if hasattr(product, 'product_title'):
                    message += f"\\n{product.product_title}"

                if hasattr(product, 'description'):
                    message += f'{product.description}\\n'

                if hasattr(product, 'original_price'):
                    message += f"\\n {product.target_original_price_currency} {product.original_price} :{getattr(local_units.original_price, lang)}"

                if hasattr(product, 'sale_price') and hasattr(product, 'discount') and product.discount != '0%':
                    message += f"\\n{product.discount} :{getattr(local_units.discount, lang)}"
                    message += f"\\n {product.target_original_price_currency} {product.sale_price} :{getattr(local_units.sale_price, lang)}"

                if hasattr(product, 'evaluate_rate') and product.evaluate_rate != '0.0%':
                    message += f"\\n{product.evaluate_rate} :{getattr(local_units.evaluate_rate, lang)}"

                if hasattr(product, 'promotion_link'):
                    message += f"\\n{product.promotion_link} :{getattr(local_units.promotion_link, lang)}"

                # if hasattr(product, \'tags\'):
                #     message += f"\\n{product.tags} :{getattr(local_units.tags, lang)}"\
                # message += f"\\n{getattr(local_units.COPYRIGHT, lang)}"\
                
        except Exception as ex:
            logger.error("Ошибка при генерации сообщения", ex, exc_info=True)
            return

        # Отправка сообщения в текстовое поле.
        try:
            textarea_list[i].send_keys(message)
            return
        except Exception as ex:
            logger.error("Ошибка при отправке текста в текстовое поле", ex, exc_info=True)
            return

    # Обработка продуктов и обновление их подписей.
    for i, product in enumerate(media):
        handle_product(product, textarea_list, i)

def publish(d:Driver, attempts:int = 5) -> bool | None:
    """
    Публикует сообщение после редактирования.

    Args:
        d (Driver): Инстанс драйвера для взаимодействия с веб-страницей.
        attempts (int): Количество попыток публикации.

    Returns:
        bool | None: `True`, если сообщение успешно опубликовано, иначе `None`.
    """
    if attempts < 0:
        return None
    if not d.execute_locator(locator.finish_editing_button, timeout = 1):
        logger.debug(f"Неудача обработки локатора {locator.finish_editing_button}")
        return None
    d.wait(1)
    if not d.execute_locator(locator.publish, timeout = 5):
        if d.execute_locator(locator.close_pop_up):
            publish(d, attempts -1)
        if d.execute_locator(locator.not_now):
            publish(d, attempts -1)
        if attempts > 0:
           d.wait(5)
           publish(d, attempts -1)

        logger.debug(f"Неудача обработки локатора {locator.finish_editing_button}")
        return None

    while not d.execute_locator(locator = locator.open_add_post_box, timeout = 10, timeout_for_event = 'element_to_be_clickable'):
        logger.debug(f"не освободилось поле ввода {attempts=}",None, False)
        if d.execute_locator(locator.close_pop_up):
            publish(d, attempts -1)
        if d.execute_locator(locator.not_now):
            publish(d, attempts -1)
        if attempts > 0:
           d.wait(2)
           publish(d, attempts -1)

    return True

def promote_post(d: Driver, category: SimpleNamespace, products: List[SimpleNamespace], no_video: bool = False) -> bool | None:
    """
    Управляет процессом продвижения поста с заголовком, описанием и медиафайлами.

    Args:
        d (Driver): Инстанс драйвера для взаимодействия с веб-страницей.
        category (SimpleNamespace): Детали категории, используемые для заголовка и описания поста.
        products (List[SimpleNamespace]): Список продуктов, содержащих медиа и детали для публикации.
        no_video (bool): Флаг, указывающий, что видео не нужно загружать.

    Returns:
        bool | None: `True`, если пост успешно продвинут, иначе `None`.

    Example:
        >>> driver = Driver(...)
        >>> category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
        >>> products = [SimpleNamespace(local_image_path='path/to/image.jpg', ...)]
        >>> promote_post(driver, category, products)
    """
    if not post_title(d, category):
        return None
    d.wait(0.5)

    if not upload_media(d, products, no_video):
        return None
    if not d.execute_locator(locator = locator.finish_editing_button):
        return None
    if not d.execute_locator(locator.publish, timeout = 20):
        print("Публикуется...")
        return None
    return True

def post_message(d: Driver, message: SimpleNamespace,  no_video: bool = False,  images:Optional[str | list[str]] = None, without_captions:bool = False) -> bool | None:
    """
    Управляет процессом публикации сообщения с заголовком, описанием и медиафайлами.

    Args:
        d (Driver): Инстанс драйвера для взаимодействия с веб-страницей.
        message (SimpleNamespace): Детали сообщения, используемые для заголовка и описания поста.
        no_video (bool): Флаг, указывающий, что видео не нужно загружать.
        images (Optional[str | list[str]]): Список изображений для публикации.
        without_captions (bool): Флаг, указывающий, что подписи не нужно добавлять.

    Returns:
        bool | None: `True`, если сообщение успешно опубликовано, иначе `None`.

    Example:
        >>> driver = Driver(...)
        >>> message = SimpleNamespace(title="Заголовок сообщения", description="Описание сообщения")
        >>> post_message(driver, message)
    """
    if not post_title(d, message):
        return None
    d.wait(0.5)

    if not upload_media(d, message.products, no_video = no_video, without_captions = without_captions):
        return None
    d.wait(0.5)

    if d.execute_locator(locator = locator.send):
        # Выход, если было одно изображение
        return True

    if not d.execute_locator(locator = locator.finish_editing_button):
        return None

    if not publish(d):
        return None

    return True