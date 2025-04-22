### **Анализ кода модуля `src.webdriver.executor`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Хорошая структура: Код разбит на логические блоки и функции, что облегчает его понимание и поддержку.
    - Использование аннотаций типов: Повышает читаемость и помогает в отладке.
    - Обработка исключений: Код содержит блоки try-except для обработки возможных ошибок.
- **Минусы**:
    - Отсутствие документации модуля в формате Markdown.
    - Не везде используются согласованные стили форматирования.
    - Встречаются `Union[]` вместо `|`

**Рекомендации по улучшению:**

1.  **Документация модуля**:
    - Добавить заголовок и описание модуля в формате Markdown.
    - Описать назначение модуля, основные классы и функции, а также примеры использования.

2.  **Форматирование и стиль кода**:
    - Использовать консистентные отступы и пробелы вокруг операторов.
    - Убедиться, что все строки не превышают 120 символов.
    - Всегда используй одинарные кавычки (`'`) в Python-коде.
    - Не используй `Union[]` в коде. Вместо этого используй `|`

3.  **Комментарии и документация**:
    - Добавить docstring для каждого метода и класса, описывающие их назначение, параметры и возвращаемые значения.
    - Перевести все комментарии и docstring на русский язык в формате UTF-8.
    - Использовать более конкретные и понятные комментарии, избегая общих фраз.

4.  **Обработка исключений**:
    - Использовать `ex` вместо `e` в блоках обработки исключений.

5.  **Использование логгера**:
    - Убедиться, что все ошибки и исключения логируются с использованием `logger` из `src.logger.logger`.

6.  **Улучшение читаемости**:
    - Переименовать переменные и функции для большей ясности и соответствия стандартам PEP8.
    - Избегать использования сокращений, если это ухудшает понимание кода.

7.  **Использование webdriver**:
    - Убедиться, что webdriver инициализируется и используется правильно, с учетом настроек из модулей `Driver`, `Chrome`, `Firefox`, `Playwright`.

**Оптимизированный код:**

```python
## \file /src/webdriver/executor.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для взаимодействия с веб-элементами с использованием Selenium.
========================================================================

Модуль предоставляет функциональность для взаимодействия с веб-элементами с использованием Selenium
на основе предоставленных локаторов. Он обрабатывает разбор локаторов, взаимодействие с элементами
и обработку ошибок.

Модуль является ключевым компонентом для автоматизированного взаимодействия с веб-страницами.
Он позволяет находить элементы на странице по различным локаторам (например, id, class, xpath),
выполнять с ними различные действия (например, клик, ввод текста) и получать значения их атрибутов.
Модуль также включает механизмы ожидания появления элементов и обработки возможных ошибок, таких как таймауты и перехваты кликов.

Пример использования
----------------------

>>> from src.webdriver import Driver, Chrome
>>> from src.webdriver.executor import ExecuteLocator
>>> driver = Driver(Chrome)
>>> executor = ExecuteLocator(driver=driver.driver)
>>> locator = {'by': 'ID', 'selector': 'myElement', 'attribute': 'value'}
>>> result = await executor.execute_locator(locator)
"""

import asyncio
import re
from dataclasses import dataclass, field
from typing import BinaryIO, List, Optional
from types import SimpleNamespace
from itertools import zip_longest
from urllib.parse import urlparse, parse_qs
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import header
from src.logger.logger import logger
from src.utils.printer import pprint as print


@dataclass
class ExecuteLocator:
    """
    Класс для взаимодействия с веб-элементами с использованием Selenium на основе предоставленных локаторов.
    """

    driver: Optional[object] = None
    actions: ActionChains = field(init=False)
    mode: str = "debug"

    def __post_init__(self):
        """
        Инициализация объекта ActionChains после создания экземпляра класса.
        """
        if self.driver:
            self.actions = ActionChains(self.driver)

    async def execute_locator(
        self,
        locator: dict | SimpleNamespace,
        timeout: Optional[float] = 0,
        timeout_for_event: Optional[str] = "presence_of_element_located",
        message: Optional[str] = None,
        typing_speed: Optional[float] = 0,
    ) -> Optional[str | list | dict | WebElement | bool]:
        """
        Выполняет действия над веб-элементом на основе предоставленного локатора.

        Args:
            locator (dict | SimpleNamespace): Данные локатора.
            timeout (Optional[float], optional): Время ожидания для обнаружения элемента (в секундах). По умолчанию 0.
            timeout_for_event (Optional[str], optional): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). По умолчанию "presence_of_element_located".
            message (Optional[str], optional): Сообщение для таких действий, как send_keys или type. По умолчанию None.
            typing_speed (Optional[float], optional): Скорость печати для событий send_keys (в секундах). По умолчанию 0.

        Returns:
            Optional[str | list | dict | WebElement | bool]: Результат операции, который может быть строкой, списком, словарем, WebElement, bool или None.
        """
        if isinstance(locator, dict):
            locator = SimpleNamespace(**locator)

        if not getattr(locator, "attribute", None) and not getattr(locator, "selector", None):
            logger.debug("Предоставлен пустой локатор.", None, False)
            return None

        async def _parse_locator(
            locator: SimpleNamespace,
            message: Optional[str] = None,
            timeout: Optional[float] = 0,
            timeout_for_event: Optional[str] = "presence_of_element_located",
            typing_speed: Optional[float] = 0,
        ) -> Optional[str | list | dict | WebElement | bool]:
            """
            Разбирает и выполняет инструкции локатора.

            Args:
                locator (SimpleNamespace): Данные локатора.
                message (Optional[str], optional): Сообщение для действий. По умолчанию None.
                timeout (Optional[float], optional): Время ожидания для обнаружения элемента (в секундах). По умолчанию 0.
                timeout_for_event (Optional[str], optional): Условие ожидания. По умолчанию "presence_of_element_located".
                typing_speed (Optional[float], optional): Скорость печати для событий send_keys (в секундах). По умолчанию 0.

            Returns:
                Optional[str | list | dict | WebElement | bool]: Результат операции.
            """
            if locator.event and locator.attribute and locator.mandatory is None:
                logger.debug(
                    f"Локатор с событием и атрибутом, но отсутствует обязательный флаг. Пропускается. {print(locator.__dict__, text_color='yellow')} ",
                    None,
                    False,
                )
                return None

            if isinstance(locator.by, str):
                try:
                    locator.by = locator.by.lower()
                    if locator.attribute:
                        locator.attribute = self._evaluate_locator(locator.attribute)

                        if locator.by == "value":
                            return locator.attribute

                        if locator.by == 'url':
                            if not locator.attribute:
                                logger.error(
                                    f"Отсутствует атрибут для локатора 'URL': {print(locator.__dict__, text_color='yellow')}"
                                )
                                return False

                            url = self.driver.current_url
                            parsed_url = urlparse(url)
                            query_params = parse_qs(parsed_url.query)
                            return query_params.get(locator.attribute, None)[0]

                except Exception as ex:
                    logger.error(
                        f"Ошибка получения атрибута по 'VALUE': {print(locator.__dict__, text_color='yellow')}, error:",
                        ex,
                    )
                    return None

                if locator.event:
                    return await self.execute_event(locator, timeout, timeout_for_event, message, typing_speed)

                if locator.attribute:
                    return await self.get_attribute_by_locator(locator, timeout, timeout_for_event)

                return await self.get_webelement_by_locator(locator, timeout, timeout_for_event)

            elif isinstance(locator.selector, list) and isinstance(locator.by, list):
                if locator.sorted == "pairs":
                    elements_pairs = []

                    for n in len(locator.by):
                        l = SimpleNamespace(
                            **{
                                "attribute": locator.attribute[n],
                                "by": locator.by[n],
                                "selector": locator.selector[n],
                                "if_list": locator.if_list if isinstance(locator.if_list, str) else locator.if_list[n],
                                "mandatory": locator.mandatory if isinstance(locator.mandatory, str) else locator.mandatory[n],
                                "event": locator.event if isinstance(locator.event, str) else locator.event[n],
                                "timeout": locator.timeout if isinstance(locator.timeout, str) else locator.timeout[n],
                                "timeout_for_event": locator.timeout_for_event
                                if isinstance(locator.timeout_for_event, str)
                                else locator.timeout_for_event[n],
                                "locator_description": locator.locator_description,
                            }
                        )
                        elements_pairs.append(
                            await _parse_locator(l, message, timeout, timeout_for_event, message, typing_speed)
                        )

                    zipped_pairs = list(zip_longest(*elements_pairs, fillvalue=None))
                    return zipped_pairs

            else:
                logger.warning("Локатор не содержит списки 'selector' и 'by' или неверное значение 'sorted'.")

        return await _parse_locator(locator, message, timeout, timeout_for_event, typing_speed)

    def _evaluate_locator(self, attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]:
        """
        Оценивает и обрабатывает атрибуты локатора.

        Args:
            attribute (str | List[str] | dict): Атрибут для оценки.

        Returns:
            Optional[str | List[str] | dict]: Оцененный атрибут.
        """

        def _evaluate(attr: str) -> Optional[str]:
            """Оценивает строку одного атрибута."""
            return getattr(Keys, re.findall(r"%(\\w+)%", attr)[0], None) if re.match(r"^%\\w+%", attr) else attr

        if isinstance(attribute, list):
            return [_evaluate(attr) for attr in attribute]
        return _evaluate(str(attribute))

    async def get_attribute_by_locator(
        self,
        locator: SimpleNamespace | dict,
        timeout: Optional[float] = 0,
        timeout_for_event: str = "presence_of_element_located",
        message: Optional[str] = None,
        typing_speed: float = 0,
    ) -> Optional[WebElement | list[WebElement]]:
        """
        Извлекает атрибуты из веб-элемента или списка веб-элементов.

        Args:
            locator (SimpleNamespace | dict): Данные локатора.
            timeout (Optional[float], optional): Время ожидания для обнаружения элемента (в секундах). По умолчанию 0.
            timeout_for_event (str, optional): Условие ожидания. По умолчанию "presence_of_element_located".
            message (Optional[str], optional): Не используется в этой функции. По умолчанию None.
            typing_speed (float, optional): Не используется в этой функции. По умолчанию 0.

        Returns:
            Optional[WebElement | list[WebElement]]: Значение атрибута(ов) в виде WebElement, списка WebElements или None, если не найдено.
        """
        locator = (
            locator
            if isinstance(locator, SimpleNamespace)
            else SimpleNamespace(**locator) if isinstance(locator, dict) else None
        )

        web_element: WebElement = await self.get_webelement_by_locator(locator, timeout, timeout_for_event)
        if not web_element:
            if locator.mandatory:
                logger.debug(f"Элемент не найден: {print(locator, text_color='yellow')}")
            return None

        def _parse_dict_string(attr_string: str) -> dict | None:
            """Разбирает строку типа '{attr1:attr2}' в словарь."""
            try:
                return {
                    k.strip(): v.strip()
                    for k, v in (pair.split(":") for pair in attr_string.strip("{}").split(","))
                }
            except ValueError as ex:
                logger.debug(f"Неверный формат строки атрибута: {attr_string!r}", ex)
                return None

        def _get_attributes_from_dict(web_element: WebElement, attr_dict: dict) -> dict:
            """Извлекает значения атрибутов из WebElement на основе словаря."""
            result = {}
            for key, value in attr_dict.items():
                try:
                    attr_key = web_element.get_attribute(key)
                    attr_value = web_element.get_attribute(value)
                    result[attr_key] = attr_value
                except Exception as ex:
                    logger.debug(f"Ошибка при извлечении атрибутов '{key}' или '{value}' из элемента.", ex)
                    return {}
            return result

        if web_element:
            if isinstance(locator.attribute, str) and locator.attribute.startswith("{"):
                attr_dict = _parse_dict_string(locator.attribute)
                if isinstance(web_element, list):
                    return [_get_attributes_from_dict(el, attr_dict) for el in web_element]
                return _get_attributes_from_dict(web_element, attr_dict)

            if isinstance(web_element, list):
                ret: list = []
                try:
                    for e in web_element:
                        ret.append(f'{e.get_attribute(locator.attribute)}')
                    return ret if len(ret) > 1 else ret[0]
                except Exception as ex:
                    logger.debug(f"Ошибка в get_attribute(): {locator=}", ex)
                    return None

            return web_element.get_attribute(locator.attribute)
        return None

    async def get_webelement_by_locator(
        self,
        locator: dict | SimpleNamespace,
        timeout: Optional[float] = 0,
        timeout_for_event: Optional[str] = "presence_of_element_located",
    ) -> Optional[WebElement | List[WebElement]]:
        """
        Извлекает веб-элемент или список элементов на основе предоставленного локатора.

        Args:
            locator (dict | SimpleNamespace): Данные локатора.
            timeout (Optional[float], optional): Время ожидания для обнаружения элемента (в секундах). По умолчанию 0.
            timeout_for_event (Optional[str], optional): Условие ожидания. По умолчанию "presence_of_element_located".

        Returns:
            Optional[WebElement | List[WebElement]]: WebElement, список WebElements или None, если не найдено.
        """
        timeout = timeout if timeout > 0 else getattr(locator, 'timeout', 0)

        async def _parse_elements_list(
            web_elements: WebElement | List[WebElement], locator: SimpleNamespace
        ) -> Optional[WebElement | List[WebElement]]:
            """Фильтрует список веб-элементов на основе атрибута if_list."""
            if not isinstance(web_elements, list):
                return web_elements

            if_list = locator.if_list

            if if_list == "all":
                return web_elements
            elif if_list == "first":
                return web_elements[0]
            elif if_list == "last":
                return web_elements[-1]
            elif if_list == "even":
                return [web_elements[i] for i in range(0, len(web_elements), 2)]
            elif if_list == "odd":
                return [web_elements[i] for i in range(1, len(web_elements), 2)]
            elif isinstance(if_list, list):
                return [web_elements[i] for i in if_list]
            elif isinstance(if_list, int):
                return web_elements[if_list - 1]

            return web_elements

        driver = self.driver
        locator = SimpleNamespace(**locator) if isinstance(locator, dict) else locator

        if not locator:
            logger.error("Предоставлен неверный локатор.")
            return None

        web_elements = None
        try:
            if timeout == 0:
                web_elements = await asyncio.to_thread(
                    driver.find_elements, locator.by, locator.selector
                )
            else:
                condition = (
                    EC.presence_of_all_elements_located
                    if timeout_for_event == "presence_of_all_elements_located"
                    else EC.visibility_of_all_elements_located
                )
                web_elements = await asyncio.to_thread(
                    WebDriverWait(driver, timeout).until,
                    condition((locator.by, locator.selector)),
                )

            return await _parse_elements_list(web_elements, locator) if web_elements else None

        except TimeoutException as ex:
            logger.error(f"Таймаут для локатора: {print(locator.__dict__, text_color='yellow')}", ex, False)
            return None

        except Exception as ex:
            logger.error(f"Ошибка при обнаружении элемента: {print(locator.__dict__, text_color='yellow')}", ex, False)
            return None

    async def get_webelement_as_screenshot(
        self,
        locator: SimpleNamespace | dict,
        timeout: float = 5,
        timeout_for_event: str = "presence_of_element_located",
        message: Optional[str] = None,
        typing_speed: float = 0,
        webelement: Optional[WebElement] = None,
    ) -> Optional[BinaryIO]:
        """
        Делает снимок экрана обнаруженного веб-элемента.

        Args:
            locator (SimpleNamespace | dict): Данные локатора.
            timeout (float, optional): Время ожидания для обнаружения элемента (в секундах). По умолчанию 5.
            timeout_for_event (str, optional): Условие ожидания. По умолчанию "presence_of_element_located".
            message (Optional[str], optional): Не используется в этой функции. По умолчанию None.
            typing_speed (float, optional): Не используется в этой функции. По умолчанию 0.
            webelement (Optional[WebElement], optional): Предварительно полученный веб-элемент. По умолчанию None.

        Returns:
            Optional[BinaryIO]: Бинарный поток снимка экрана или None, если не удалось.
        """
        locator = (
            locator
            if isinstance(locator, SimpleNamespace)
            else SimpleNamespace(**locator) if isinstance(locator, dict) else None
        )

        if not webelement:
            webelement = await self.get_webelement_by_locator(
                locator=locator, timeout=timeout, timeout_for_event=timeout_for_event
            )

        if not webelement:
            return None

        try:
            return webelement.screenshot_as_png
        except Exception as ex:
            logger.error(f"Не удалось сделать снимок экрана", ex)
            return None

    async def execute_event(
        self,
        locator: SimpleNamespace | dict,
        timeout: float = 5,
        timeout_for_event: str = "presence_of_element_located",
        message: str = None,
        typing_speed: float = 0,
    ) -> Optional[str | list[str] | bytes | list[bytes] | bool]:
        """
        Выполняет событие, связанное с локатором.

        Args:
            locator (SimpleNamespace | dict): Данные локатора.
            timeout (float, optional): Время ожидания для обнаружения элемента (в секундах). По умолчанию 5.
            timeout_for_event (str, optional): Условие ожидания. По умолчанию "presence_of_element_located".
            message (str, optional): Сообщение для отправки с событием. По умолчанию None.
            typing_speed (float, optional): Скорость печати для событий send_keys (в секундах). По умолчанию 0.

        Returns:
            Optional[str | list[str] | bytes | list[bytes] | bool]: Результат выполнения события.
        """
        locator = (
            locator
            if isinstance(locator, SimpleNamespace)
            else SimpleNamespace(**locator) if isinstance(locator, dict) else None
        )
        events = str(locator.event).split(";")
        result: list = []

        webelement = await self.get_webelement_by_locator(locator, timeout, timeout_for_event)
        if not webelement:
            return False
        webelement = webelement[0] if isinstance(webelement, list) else webelement

        for event in events:
            if event == "click()":
                try:
                    webelement.click()
                    continue
                except ElementClickInterceptedException as ex:
                    if locator.mandatory:
                        logger.error(f"Клик по элементу перехвачен: {print(locator)}", ex, False)
                        return False
                except Exception as ex:
                    if locator.mandatory:
                        logger.error(f"Ошибка клика по элементу:\\n {print(locator)} \\n", ex, False)
                        # try:
                        #     self.driver.execute_script("arguments[0].click();", webelement)
                        #     continue
                        # except Exception as ex:
                        #     logger.error(f"Element click error after javascript execution: {locator=}", ex)\
                        return False
                    return False

            elif event.startswith("pause("):
                match = re.match(r"pause\\((\\d+)\\)", event)
                if match:
                    pause_duration = int(match.group(1))
                    await asyncio.sleep(pause_duration)
                    result.append(True)
                    continue
                if locator.mandatory:
                    logger.debug(f"Не удалось разобрать событие pause: {print(locator)}")
                    return False

            elif event == "upload_media()":
                if not message and locator.mandatory:
                    logger.debug(f"Требуется сообщение для события upload_media. Message: {print(message)}")
                    return False
                try:
                    await asyncio.to_thread(webelement.send_keys, message)
                    result.append(True)
                    continue
                except Exception as ex:
                    if locator.mandatory:
                        logger.debug(f"Ошибка при загрузке медиа: {message=}", ex)
                        return False

            elif event == "screenshot()":
                try:
                    result.append(await self.get_webelement_as_screenshot(locator, webelement=webelement))
                except Exception as ex:
                    logger.error(f"Ошибка при создании снимка экрана: {locator=}", ex, False)
                    return False

            elif event == "clear()":
                try:
                    await asyncio.to_thread(webelement.clear)
                except Exception as ex:
                    logger.error(f"Ошибка при очистке элемента: {locator=}", ex, False)
                    return False

            elif event.startswith("send_keys("):
                keys_to_send = event.replace("send_keys(", "").replace(")", "").split("+")
                try:
                    actions = ActionChains(self.driver)
                    for key in keys_to_send:
                        key = key.strip().strip("\'")
                        if hasattr(Keys, key):
                            key_to_send = getattr(Keys, key)
                            actions.send_keys(key_to_send)
                    await asyncio.to_thread(actions.perform)
                except Exception as ex:
                    logger.error(f"Ошибка при отправке клавиш: {locator=}", ex, False)
                    return False

            elif event.startswith("type("):
                message = event.replace("type(", "").replace(")", "")
                if typing_speed:
                    for character in message:
                        await asyncio.to_thread(webelement.send_keys, character)
                        await asyncio.sleep(typing_speed)
                else:
                    await asyncio.to_thread(webelement.send_keys, message)

        return result if result else True

    async def send_message(
        self,
        locator: SimpleNamespace | dict,
        timeout: float = 5,
        timeout_for_event: str = "presence_of_element_located",
        message: str = None,
        typing_speed: float = 0,
    ) -> bool:
        """
        Отправляет сообщение веб-элементу.

        Args:
            locator (SimpleNamespace | dict): Данные локатора.
            timeout (float, optional): Время ожидания для обнаружения элемента (в секундах). По умолчанию 5.
            timeout_for_event (str, optional): Условие ожидания. По умолчанию "presence_of_element_located".
            message (str, optional): Сообщение для отправки веб-элементу. По умолчанию None.
            typing_speed (float, optional): Скорость печати для событий send_keys (в секундах). По умолчанию 0.

        Returns:
            bool: True, если сообщение было отправлено успешно, иначе False.
        """
        locator = (
            locator
            if isinstance(locator, SimpleNamespace)
            else SimpleNamespace(**locator) if isinstance(locator, dict) else None
        )

        def type_message(
            el: WebElement,
            message: str,
            replace_dict: dict = {";": "SHIFT+ENTER"},
            typing_speed: float = typing_speed,
        ) -> bool:
            """Печатает сообщение в веб-элемент с указанной скоростью."""
            message = message.split(" ")
            for word in message:
                word += " "
                try:
                    for letter in word:
                        if letter in replace_dict.keys():
                            self.actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT)
                        else:
                            self.actions.send_keys(letter)
                            self.actions.pause(typing_speed)
                            self.actions.perform()
                except Exception as ex:
                    logger.error(
                        f"Ошибка при печати сообщения:/n message={print(message)},/n word={print(letter)},/n letter={print(letter)}/n",
                        ex,
                        False,
                    )
                    continue
            return True

        webelement = await self.get_webelement_by_locator(
            locator=locator, timeout=timeout, timeout_for_event=timeout_for_event
        )
        if not webelement or (isinstance(webelement, list) and len(webelement) == 0):
            logger.debug("Веб-элемент не найден для отправки сообщения.")
            return False
        webelement = webelement[0] if isinstance(webelement, list) else webelement
        self.actions.move_to_element(webelement)
        type_message(
            el=webelement,
            message=message,
            replace_dict={";": "SHIFT+ENTER"},
            typing_speed=typing_speed,
        )
        return True