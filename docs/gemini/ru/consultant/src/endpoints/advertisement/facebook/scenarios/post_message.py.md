### **Анализ кода модуля `post_message.py`**

## \file /src/endpoints/advertisement/facebook/scenarios/post_message.py

Модуль предназначен для публикации сообщений в Facebook, включая заголовок, описание и медиафайлы.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код разбит на функции, каждая из которых выполняет определенную задачу.
    - Используется логирование для отслеживания ошибок и отладки.
    - Присутствуют docstring для функций, что облегчает понимание их назначения и использования.
- **Минусы**:
    - Docstring не полные и не соответствуют требуемому формату.
    - В некоторых местах отсутствует аннотация типов.
    - Не везде используется `logger.error` с передачей исключения.
    - Местами отсутствует обработки исключений, что может приводить к неожиданным сбоям.
    - Не все функции имеют примеры использования.

**Рекомендации по улучшению:**

1.  **Документация**:
    *   Дополнить docstring для всех функций, методов и классов в соответствии с указанным форматом, включая подробное описание аргументов, возвращаемых значений, возможных исключений и примеров использования.
    *   Перевести все docstring на русский язык.
    *   Включить описание и примеры использования для каждой функции, особенно для `publish`, `promote_post` и `post_message`.
2.  **Обработка исключений**:
    *   Убедиться, что все потенциально проблемные места обернуты в блоки `try...except`.
    *   В блоках `except` использовать `logger.error` для логирования ошибок с передачей исключения и трассировки стека (`exc_info=True`).
    *   Использовать `ex` вместо `e` в блоках `except`.
3.  **Аннотация типов**:
    *   Добавить аннотации типов для всех переменных и параметров функций, где они отсутствуют.
4.  **Использование `j_loads_ns`**:
    *   Убедиться, что для чтения JSON файлов используется `j_loads_ns`.
5.  **Улучшение логирования**:
    *   Добавить больше информативных сообщений в логи для облегчения отладки.
6.  **Разбиение на более мелкие функции**:
    *   Рассмотреть возможность разбиения больших функций на более мелкие, чтобы улучшить читаемость и упростить тестирование. Например, функцию `update_images_captions` можно разбить на несколько подфункций.
7.  **Удалить неиспользуемые импорты**:
    *   Удалить импорт `types.SimpleNamespace`, так как он не используется.

**Оптимизированный код:**

```python
## \file /src/endpoints/advertisement/facebook/scenarios/post_message.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для публикации сообщений в Facebook
=================================================

Модуль содержит функции для автоматизации процесса публикации сообщений в Facebook,
включая добавление заголовка, описания и медиафайлов.

Пример использования
----------------------

>>> from src.webdriver.driver import Driver
>>> from src.endpoints.advertisement.facebook.scenarios.post_message import post_message
>>> from types import SimpleNamespace
>>> # Инициализация драйвера и передача необходимых параметров
>>> # driver = Driver(browser_type="chrome")
>>> # message = SimpleNamespace(title="Заголовок", description="Описание", products=[...])
>>> # result = post_message(driver, message)
>>> # print(result)
"""

import time
from pathlib import Path
# from types import SimpleNamespace # Удален неиспользуемый импорт
from typing import Dict, List, Optional
from selenium.webdriver.remote.webelement import WebElement

from src import gs
from src.webdriver.driver import Driver
from src.utils.jjson import j_loads_ns
from src.utils.printer import pprint
from src.logger.logger import logger


# Загрузка локаторов из JSON файла.
locator: SimpleNamespace = j_loads_ns(
    Path(gs.path.src / 'endpoints' / 'advertisement'/ 'facebook' / 'locators'/ 'post_message.json')
)

def post_title(d: Driver, message: SimpleNamespace | str) -> bool:
    """
    Отправляет заголовок и описание кампании в поле сообщения.

    Args:
        d (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
        message (SimpleNamespace | str): Объект SimpleNamespace, содержащий заголовок и описание,
                                         или строка с сообщением.

    Returns:
        bool: True, если заголовок и описание были успешно отправлены, иначе None.

    Raises:
        Exception: Если происходит ошибка при прокрутке страницы или открытии поля добавления сообщения.

    Example:
        >>> from src.webdriver.driver import Driver
        >>> from types import SimpleNamespace
        >>> # Инициализация драйвера
        >>> # driver = Driver(browser_type="chrome")
        >>> # message = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
        >>> # result = post_title(driver, message)
        >>> # print(result)
    """
    # Прокрутка страницы назад
    if not d.scroll(1, 1200, 'backward'):
        logger.error('Ошибка при прокрутке страницы во время отправки заголовка')
        return False

    # Открытие поля "добавить сообщение"
    if not d.execute_locator(locator = locator.open_add_post_box):
        logger.debug('Не удалось открыть поле "добавить сообщение"')
        return False

    # Добавление сообщения в поле сообщения
    m =  f'{message.title}\\n{message.description}' if isinstance(message, SimpleNamespace) else message
    # if isinstance(message, SimpleNamespace) and hasattr( message,'tags'):
    #     m = f"{m}\\nTags: {message.tags}"

    if not d.execute_locator(locator.add_message, message = m, timeout = 5, timeout_for_event = 'element_to_be_clickable'):
        logger.debug(f'Не удалось добавить сообщение в поле сообщения: {m=}')
        return False

    return True

def upload_media(d: Driver, media: SimpleNamespace | List[SimpleNamespace] | str | list[str],   no_video: bool = False, without_captions:bool = False) -> bool:
    """
    Загружает медиафайлы в секцию изображений и обновляет подписи.

    Args:
        d (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
        media (SimpleNamespace | List[SimpleNamespace] | str | list[str]): Список объектов SimpleNamespace, содержащих пути к медиафайлам,
               или список строк с путями к медиафайлам, или строка с путем к медиафайлу.
        no_video (bool): Если True, не загружать видео. По умолчанию False.
        without_captions (bool): Если True, не обновлять подписи. По умолчанию False.

    Returns:
        bool: True, если медиафайлы были успешно загружены, иначе False.

    Raises:
        Exception: Если происходит ошибка во время загрузки медиафайлов или обновления подписей.

    Example:
        >>> from src.webdriver.driver import Driver
        >>> from types import SimpleNamespace
        >>> # Инициализация драйвера
        >>> # driver = Driver(browser_type="chrome")
        >>> # media = [SimpleNamespace(local_image_path='path/to/image.jpg', local_video_path='path/to/video.mp4')]
        >>> # result = upload_media(driver, media)
        >>> # print(result)
    """
    if not media:
        logger.debug('Нет медиа для сообщения!')
        return True

    # Шаг 1: Открытие формы "добавить медиа". Она может быть уже открыта.
    if not d.execute_locator(locator.open_add_foto_video_form):
        return False
    d.wait(0.5)

    # Шаг 2: Преобразование media в список.
    media_list:list = media if  isinstance(media, list) else [media]
    ret: bool = True

    # Итерация по media и загрузка медиафайлов.
    for m in media_list:
        if isinstance(m, SimpleNamespace):
            try:
                media_path = m.local_video_path if hasattr(m, 'local_video_path') and not no_video else m.local_image_path
            except Exception as ex:
                logger.debug(f'Ошибка в поле \'local_image_path\': {ex}', exc_info=True)
                continue # Исправлено на continue, чтобы продолжить загрузку других медиафайлов
        elif isinstance(m, (str, Path)):
            media_path = m
        else:
            logger.error(f'Неподдерживаемый тип медиа: {type(m)}')
            continue # Добавлено для обработки неподдерживаемого типа медиа
        try:
            # Загрузка медиафайла.
            if d.execute_locator(locator = locator.foto_video_input, message = str(media_path) , timeout = 20):
                d.wait(1.5)
            else:
                logger.error(f'Ошибка загрузки изображения {media_path=}')
                return False
        except Exception as ex:
            logger.error('Ошибка при загрузке медиа', ex, exc_info=True)
            return False
    if without_captions:
        return True
    # Шаг 3: Обновление подписей для загруженных медиафайлов.
    if not d.execute_locator(locator.edit_uloaded_media_button):
        logger.error(f'Ошибка при нажатии кнопки редактирования загруженных медиафайлов')
        return False
    uploaded_media_frame = d.execute_locator(locator.uploaded_media_frame)
    if not uploaded_media_frame:
        logger.debug(f'Не нашлись поля ввода подписей к изображениям')
        return False

    uploaded_media_frame = uploaded_media_frame[0] if isinstance(uploaded_media_frame, list) else uploaded_media_frame
    d.wait(0.3)

    textarea_list = d.execute_locator(locator = locator.edit_image_properties_textarea, timeout = 10, timeout_for_event = 'presence_of_element_located' )
    if not textarea_list:
        logger.error('Не нашлись поля ввода подписи к изображениям')
        return False
    # Обновление подписей к изображениям.
    update_images_captions(d, media, textarea_list)

    return ret

def update_images_captions(d: Driver, media: List[SimpleNamespace], textarea_list: List[WebElement]) -> None:
    """
    Добавляет описания к загруженным медиафайлам.

    Args:
        d (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
        media (List[SimpleNamespace]): Список объектов SimpleNamespace с деталями для обновления.
        textarea_list (List[WebElement]): Список элементов textarea, в которые добавляются подписи.

    Raises:
        Exception: Если происходит ошибка при обновлении подписей к медиафайлам.
    """
    local_units = j_loads_ns(Path(gs.path.src / 'advertisement' / 'facebook' / 'scenarios' / 'translations.json'))

    def handle_product(product: SimpleNamespace, textarea_list: List[WebElement], i: int) -> None:
        """
        Обрабатывает обновление подписей к медиафайлам для одного продукта.

        Args:
            product (SimpleNamespace): Продукт для обновления.
            textarea_list (List[WebElement]): Список элементов textarea, в которые добавляются подписи.
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

                # if hasattr(product, 'tags'):
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

                # if hasattr(product, 'tags'):
                #     message += f"\\n{product.tags} :{getattr(local_units.tags, lang)}"\
                # message += f"\\n{getattr(local_units.COPYRIGHT, lang)}"\

        except Exception as ex:
            logger.error("Ошибка при генерации сообщения", ex, exc_info=True)
            return

        # Отправка сообщения в textarea.
        try:
            textarea_list[i].send_keys(message)
            return
        except Exception as ex:
            logger.error("Ошибка при отправке текста в textarea", ex, exc_info=True)
            return

    # Обработка продуктов и обновление их подписей.
    for i, product in enumerate(media):
        handle_product(product, textarea_list, i)

def publish(d:Driver, attempts: int = 5) -> bool:
    """
    Публикует сообщение после редактирования.

    Args:
        d (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
        attempts (int): Количество попыток публикации. По умолчанию 5.

    Returns:
        bool: True, если публикация прошла успешно, иначе False.

    Raises:
        None

    Example:
        >>> from src.webdriver.driver import Driver
        >>> # Инициализация драйвера
        >>> # driver = Driver(browser_type="chrome")
        >>> # result = publish(driver)
        >>> # print(result)
    """
    if attempts < 0:
        return False
    if not d.execute_locator(locator.finish_editing_button, timeout = 1):
        logger.debug(f"Неудача обработки локатора {locator.finish_editing_button}")
        return False
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
        return False

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

def promote_post(d: Driver, category: SimpleNamespace, products: List[SimpleNamespace], no_video: bool = False) -> bool:
    """
    Управляет процессом продвижения поста с заголовком, описанием и медиафайлами.

    Args:
        d (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
        category (SimpleNamespace): Объект SimpleNamespace с деталями категории для заголовка и описания поста.
        products (List[SimpleNamespace]): Список объектов SimpleNamespace, содержащих медиафайлы и детали для публикации.
        no_video (bool): Если True, не загружать видео. По умолчанию False.

    Returns:
        bool: True, если продвижение поста прошло успешно, иначе False.

    Raises:
        None

    Example:
        >>> from src.webdriver.driver import Driver
        >>> from types import SimpleNamespace
        >>> # Инициализация драйвера
        >>> # driver = Driver(browser_type="chrome")
        >>> # category = SimpleNamespace(title="Заголовок", description="Описание")
        >>> # products = [SimpleNamespace(local_image_path='path/to/image.jpg', local_video_path='path/to/video.mp4')]
        >>> # result = promote_post(driver, category, products)
        >>> # print(result)
    """
    if not post_title(d, category):
        return False
    d.wait(0.5)

    if not upload_media(d, products, no_video):
        return False
    if not d.execute_locator(locator = locator.finish_editing_button):
        return False
    if not d.execute_locator(locator.publish, timeout = 20):
        print("Публикуется...")
        return False
    return True

def post_message(d: Driver, message: SimpleNamespace,  no_video: bool = False,  images:Optional[str | list[str]] = None, without_captions:bool = False) -> bool:
    """
    Управляет процессом публикации сообщения с заголовком, описанием и медиафайлами.

    Args:
        d (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
        message (SimpleNamespace): Объект SimpleNamespace с деталями сообщения для заголовка и описания поста.
        no_video (bool): Если True, не загружать видео. По умолчанию False.
        images (Optional[str | list[str]]): Список изображений. По умолчанию None.
        without_captions (bool): Если True, не добавлять подписи. По умолчанию False.

    Returns:
        bool: True, если публикация сообщения прошла успешно, иначе False.

    Raises:
        None

    Example:
        >>> from src.webdriver.driver import Driver
        >>> from types import SimpleNamespace
        >>> # Инициализация драйвера
        >>> # driver = Driver(browser_type="chrome")
        >>> # message = SimpleNamespace(title="Заголовок", description="Описание", products=[...])
        >>> # result = post_message(driver, message)
        >>> # print(result)
    """
    if not post_title(d, message):
        return False
    d.wait(0.5)

    if not upload_media(d, message.products, no_video = no_video, without_captions = without_captions):
        return False
    d.wait(0.5)

    if d.execute_locator(locator = locator.send):
        """ Выход, если было одно изображение """
        return True

    if not d.execute_locator(locator = locator.finish_editing_button):
        return False

    if not publish(d):
        return False

    return True