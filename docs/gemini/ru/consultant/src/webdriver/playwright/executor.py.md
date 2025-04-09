### **Анализ кода модуля `executor.py`**

## \file /src/webdriver/playwright/executor.py

Модуль предоставляет функциональность для взаимодействия с веб-элементами с использованием Playwright на основе предоставленных локаторов. Он обрабатывает разбор локаторов, взаимодействие с элементами и обработку ошибок.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Использование асинхронности для выполнения операций.
    - Обработка исключений с логированием ошибок.
    - Использование `SimpleNamespace` для удобной работы с данными локаторов.
    - Четкая структура класса `PlaywrightExecutor`.
- **Минусы**:
    - Некоторые docstring написаны на английском языке.
    - Не все функции и методы имеют подробные docstring с описанием аргументов, возвращаемых значений и возможных исключений.
    - Отсутствуют примеры использования в docstring.
    - Не везде используются аннотации типов.
    - Дублирование кода при проверке типа локатора (dict или SimpleNamespace).

**Рекомендации по улучшению:**

1.  **Документация**:
    - Перевести все docstring на русский язык.
    - Добавить подробные описания аргументов, возвращаемых значений и возможных исключений для всех функций и методов.
    - Добавить примеры использования в docstring.
2.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных и параметров функций, где они отсутствуют.
3.  **Упрощение кода**:
    - Избавиться от дублирования кода при проверке типа локатора (dict или SimpleNamespace), вынеся эту логику в отдельную функцию или используя более элегантное решение.
4.  **Обработка ошибок**:
    - Улучшить обработку ошибок, добавив более конкретные исключения и сообщения об ошибках.
5.  **Логирование**:
    - Добавить больше информативных сообщений в логи для облегчения отладки и мониторинга.
6.  **Использование `j_loads`**:
    - Заменить прямое указание пути к файлу конфигурации на использование `gs.path.src / 'webdriver' / 'playwright' / 'playwrid.json'` для загрузки конфигурации с использованием `j_loads_ns`.

**Оптимизированный код:**

```python
## \file /src/webdriver/playwright/executor.py
# -*- coding: utf-8 -*-\n#! .pyenv/bin/python3

"""
Модуль для взаимодействия с веб-элементами с использованием Playwright
========================================================================

Модуль предоставляет класс :class:`PlaywrightExecutor`, который используется для взаимодействия с веб-элементами
с использованием Playwright на основе предоставленных локаторов. Он обрабатывает разбор локаторов,
взаимодействие с элементами и обработку ошибок.

Пример использования
----------------------

>>> executor = PlaywrightExecutor(browser_type='chromium')
>>> await executor.start()
>>> locator = {'by': 'XPATH', 'selector': '//button[@id="myButton"]'}
>>> result = await executor.execute_locator(locator, message='Click!')
>>> await executor.stop()
"""
import asyncio
import re
from typing import Optional, List, Union, Any
from pathlib import Path
from playwright.async_api import async_playwright, Page, Locator
from types import SimpleNamespace
from itertools import zip_longest

from src import gs
from src.logger.logger import logger
from src.utils.jjson import j_loads_ns


class PlaywrightExecutor:
    """
    Выполняет команды на основе команд локаторов в стиле исполнителя, используя Playwright.
    """

    def __init__(self, browser_type: str = 'chromium', **kwargs: Any):
        """
        Инициализирует исполнитель Playwright.

        Args:
            browser_type (str): Тип браузера для запуска (например, 'chromium', 'firefox', 'webkit').
            **kwargs (Any): Дополнительные аргументы.
        """
        self.driver = None
        self.browser_type = browser_type
        self.page: Optional[Page] = None
        self.config: SimpleNamespace = j_loads_ns(
            Path(gs.path.src / 'webdriver' / 'playwright' / 'playwrid.json')
        )

    async def start(self) -> None:
        """
        Инициализирует Playwright и запускает экземпляр браузера.
        """
        try:
            self.driver = await async_playwright().start()
            browser = await getattr(self.driver, self.browser_type).launch(headless=True, args=self.config.options)
            self.page = await browser.new_page()
        except Exception as ex:
            logger.critical('Playwright не удалось запустить браузер', ex, exc_info=True)

    async def stop(self) -> None:
        """
        Закрывает браузер Playwright и останавливает его экземпляр.
        """
        try:
            if self.page:
                await self.page.close()
            if self.driver:
                await self.driver.stop()
                self.driver = None
            logger.info('Playwright остановлен')
        except Exception as ex:
            logger.error(f'Playwright не удалось закрыть браузер: {ex}', exc_info=True)

    async def execute_locator(
            self,
            locator: Union[dict, SimpleNamespace],
            message: Optional[str] = None,
            typing_speed: float = 0,
            timeout: Optional[float] = 0,
            timeout_for_event: Optional[str] = 'presence_of_element_located',
    ) -> Union[str, list, dict, Locator, bool, None]:
        """
        Выполняет действия над веб-элементом на основе предоставленного локатора.

        Args:
            locator (Union[dict, SimpleNamespace]): Данные локатора (словарь или SimpleNamespace).
            message (Optional[str]): Необязательное сообщение для событий.
            typing_speed (float): Необязательная скорость набора текста для событий.
            timeout (float): Время ожидания для обнаружения элемента (в секундах).
            timeout_for_event (str): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located').

        Returns:
            Union[str, list, dict, Locator, bool, None]: Результат операции, который может быть строкой, списком, словарем,
            локатором, булевым значением или None.
        """
        # Преобразуем locator в SimpleNamespace, если это словарь
        if isinstance(locator, dict):
            locator = SimpleNamespace(**locator)

        # Проверяем, что локатор не пустой
        if not getattr(locator, "attribute", None) and not getattr(locator, "selector", None):
            logger.debug("Предоставлен пустой локатор.")
            return None

        async def _parse_locator(
                locator: SimpleNamespace, message: Optional[str]
        ) -> Union[str, list, dict, Locator, bool, None]:
            """Разбирает и выполняет инструкции локатора."""
            if locator.event and locator.attribute and locator.mandatory is None:
                logger.debug("Локатор с событием и атрибутом, но без обязательного флага. Пропускается.")
                return None

            if isinstance(locator.attribute, str) and isinstance(locator.by, str):
                try:
                    if locator.attribute:
                        locator.attribute = await self.evaluate_locator(locator.attribute)
                        if locator.by == "VALUE":
                            return locator.attribute
                except Exception as ex:
                    logger.debug(f"Ошибка при получении атрибута по \'VALUE\': {locator}, ошибка: {ex}")
                    return None

                if locator.event:
                    return await self.execute_event(locator, message, typing_speed)

                if locator.attribute:
                    return await self.get_attribute_by_locator(locator)

                return await self.get_webelement_by_locator(locator)

            elif isinstance(locator.selector, list) and isinstance(locator.by, list):
                if locator.sorted == "pairs":
                    elements_pairs = []

                    for attribute, by, selector, event, timeout, timeout_for_event, locator_description in zip(
                            locator.attribute,
                            locator.by,
                            locator.selector,
                            locator.event,
                            locator.timeout,
                            locator.timeout_for_event,
                            locator.locator_description,
                    ):
                        l = SimpleNamespace(
                            **{\
                                "attribute": attribute,
                                "by": by,
                                "selector": selector,
                                "event": event,
                                "timeout": timeout,
                                "timeout_for_event": timeout_for_event,
                                "locator_description": locator_description,
                            }
                        )
                        elements_pairs.append(await _parse_locator(l, message))

                    zipped_pairs = list(zip_longest(*elements_pairs, fillvalue=None))
                    return zipped_pairs

            else:
                logger.warning("Локатор не содержит списки \'selector\' и \'by\' или неверное значение \'sorted\'.")

        return await _parse_locator(locator, message)

    async def evaluate_locator(self, attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]:
        """
        Оценивает и обрабатывает атрибуты локатора.

        Args:
            attribute (Union[str, List[str], dict]): Атрибут для оценки (может быть строкой, списком строк или словарем).

        Returns:
            Union[str, List[str], dict]: Оцененный атрибут, который может быть строкой, списком строк или словарем.
        """

        async def _evaluate(attr: str) -> Optional[str]:
            """Оценивает атрибут."""
            return attr

        if isinstance(attribute, list):
            return await asyncio.gather(*[_evaluate(attr) for attr in attribute])
        return await _evaluate(str(attribute))

    async def get_attribute_by_locator(self, locator: dict | SimpleNamespace) -> Optional[str | List[str] | dict]:
        """
        Получает указанный атрибут из веб-элемента.

        Args:
            locator (Union[dict, SimpleNamespace]): Данные локатора (словарь или SimpleNamespace).

        Returns:
            Optional[Union[str, List[str], dict]]: Атрибут или None.
        """
        # Преобразуем locator в SimpleNamespace, если это словарь
        locator = (
            locator if isinstance(locator, SimpleNamespace) else SimpleNamespace(**locator) if isinstance(locator, dict) else None
        )
        # Получаем веб-элемент по локатору
        element = await self.get_webelement_by_locator(locator)

        # Если элемент не найден, возвращаем None
        if not element:
            logger.debug(f"Элемент не найден: {locator=}")
            return None

        def _parse_dict_string(attr_string: str) -> dict | None:
            """Разбирает строку типа \'{attr1:attr2}\' в словарь."""
            try:
                return {k.strip(): v.strip() for k, v in (pair.split(":") for pair in attr_string.strip("{}").split(","))}
            except ValueError as ex:
                logger.debug(f"Неверный формат строки атрибута: {attr_string}", ex)
                return None

        async def _get_attribute(el: Locator, attr: str) -> Optional[str]:
            """Извлекает один атрибут из Locator."""
            try:
                return await el.get_attribute(attr)
            except Exception as ex:
                logger.debug(f"Ошибка при получении атрибута \'{attr}\' из элемента: {ex}")
                return None

        async def _get_attributes_from_dict(element: Locator, attr_dict: dict) -> dict:
            """Извлекает несколько атрибутов на основе словаря."""
            result = {}
            for key, value in attr_dict.items():
                result[key] = await _get_attribute(element, key)
                result[value] = await _get_attribute(element, value)

            return result

        if isinstance(locator.attribute, str) and locator.attribute.startswith("{"):
            attr_dict = _parse_dict_string(locator.attribute)
            if attr_dict:
                if isinstance(element, list):
                    return await asyncio.gather(*[_get_attributes_from_dict(el, attr_dict) for el in element])
                return await _get_attributes_from_dict(element, attr_dict)

        if isinstance(element, list):
            return await asyncio.gather(*[_get_attribute(el, locator.attribute) for el in element])

        return await _get_attribute(element, locator.attribute)

    async def get_webelement_by_locator(self, locator: dict | SimpleNamespace) -> Optional[Locator | List[Locator]]:
        """
        Получает веб-элемент с использованием локатора.

        Args:
            locator (Union[dict, SimpleNamespace]): Данные локатора (словарь или SimpleNamespace).

        Returns:
            Optional[Union[Locator, List[Locator]]]: Playwright Locator.
        """
        # Преобразуем locator в SimpleNamespace, если это словарь
        locator = (
            SimpleNamespace(**locator)
            if isinstance(locator, dict)
            else locator
        )
        # Если локатор недействителен, возвращаем None
        if not locator:
            logger.error("Предоставлен недействительный локатор.")
            return None
        try:
            # Получаем элементы на основе типа локатора
            if locator.by.upper() == "XPATH":
                elements = self.page.locator(f'xpath={locator.selector}')
            else:
                elements = self.page.locator(locator.selector)

            # Обрабатываем список элементов на основе значения locator.if_list
            if locator.if_list == 'all':
                return await elements.all()
            elif locator.if_list == 'first':
                return elements.first
            elif locator.if_list == 'last':
                return elements.last
            elif locator.if_list == 'even':
                list_elements = await elements.all()
                return [list_elements[i] for i in range(0, len(list_elements), 2)]
            elif locator.if_list == 'odd':
                list_elements = await elements.all()
                return [list_elements[i] for i in range(1, len(list_elements), 2)]
            elif isinstance(locator.if_list, list):
                list_elements = await elements.all()
                return [list_elements[i] for i in locator.if_list]
            elif isinstance(locator.if_list, int):
                list_elements = await elements.all()
                return list_elements[locator.if_list - 1]
            else:
                return elements
        except Exception as ex:
            logger.error(f'Ошибка поиска элемента: {locator=}', ex, exc_info=True)
            return None

    async def get_webelement_as_screenshot(self, locator: dict | SimpleNamespace, webelement: Optional[Locator] = None) -> Optional[bytes]:
        """
        Делает скриншот расположенного веб-элемента.

        Args:
            locator (Union[dict, SimpleNamespace]): Данные локатора (словарь или SimpleNamespace).
            webelement (Optional[Locator]): Веб-элемент Locator.

        Returns:
            Optional[bytes]: Скриншот в байтах или None.
        """
        # Преобразуем locator в SimpleNamespace, если это словарь
        locator = (
            locator if isinstance(locator, SimpleNamespace) else SimpleNamespace(**locator) if isinstance(locator, dict) else None
        )

        # Если веб-элемент не предоставлен, получаем его по локатору
        if not webelement:
            webelement = await self.get_webelement_by_locator(locator)

        # Если элемент не найден, возвращаем None
        if not webelement:
            logger.debug(f"Элемент не найден для скриншота: {locator=}")
            return None
        try:
            # Делаем скриншот элемента и возвращаем его в байтах
            return await webelement.screenshot()
        except Exception as ex:
            logger.error(f"Не удалось сделать скриншот: {locator=}", ex, exc_info=True)
            return None

    async def execute_event(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> Union[str, List[str], bytes, List[bytes], bool]:
        """
        Выполняет событие, связанное с локатором.

        Args:
            locator (Union[dict, SimpleNamespace]): Данные локатора (словарь или SimpleNamespace).
            message (Optional[str]): Необязательное сообщение для событий.
            typing_speed (float): Необязательная скорость набора текста для событий.

        Returns:
            Union[str, List[str], bytes, List[bytes], bool]: Статус выполнения.
        """
        # Преобразуем locator в SimpleNamespace, если это словарь
        locator = (
            locator if isinstance(locator, SimpleNamespace) else SimpleNamespace(**locator) if isinstance(locator, dict) else None
        )
        # Разбиваем строку событий на отдельные события
        events = str(locator.event).split(";")
        result: list = []
        # Получаем веб-элемент по локатору
        element = await self.get_webelement_by_locator(locator)
        # Если элемент не найден, возвращаем False
        if not element:
            logger.debug(f"Элемент для события не найден: {locator=}")
            return False

        # Если элемент является списком, берем первый элемент
        element = element[0] if isinstance(element, list) else element

        # Выполняем каждое событие
        for event in events:
            # Обрабатываем событие "click()"
            if event == "click()":
                try:
                    await element.click()
                    continue
                except Exception as ex:
                    logger.error(f"Ошибка во время события click: {locator=}", ex, exc_info=True)
                    return False

            # Обрабатываем событие "pause()"
            elif event.startswith("pause("):
                match = re.match(r"pause\\((\\d+)\\)", event)
                if match:
                    pause_duration = int(match.group(1))
                    await asyncio.sleep(pause_duration)
                    continue
                logger.debug(f"Ошибка разбора события pause: {locator=}")
                return False

            # Обрабатываем событие "upload_media()"
            elif event == "upload_media()":
                if not message:
                    logger.debug(f"Сообщение обязательно для события upload_media: {message!r}")
                    return False
                try:
                    await element.set_input_files(message)
                    continue
                except Exception as ex:
                    logger.error(f"Ошибка во время загрузки файла: {locator=}, {message=}", ex, exc_info=True)
                    return False

            # Обрабатываем событие "screenshot()"
            elif event == "screenshot()":
                try:
                    result.append(await self.get_webelement_as_screenshot(locator, webelement=element))
                except Exception as ex:
                    logger.error(f"Ошибка во время создания скриншота: {locator=}", ex, exc_info=True)
                    return False

            # Обрабатываем событие "clear()"
            elif event == "clear()":
                try:
                    await element.clear()
                    continue
                except Exception as ex:
                    logger.error(f"Ошибка во время очистки поля: {locator=}", ex, exc_info=True)
                    return False

            # Обрабатываем событие "send_keys()"
            elif event.startswith("send_keys("):
                keys_to_send = event.replace("send_keys(", "").replace(")", "").split("+")
                try:
                    for key in keys_to_send:
                        key = key.strip().strip("\'")
                        if key:
                            await element.type(key)
                except Exception as ex:
                    logger.error(f"Ошибка при отправке клавиш: {locator=}", ex, exc_info=True)
                    return False

            # Обрабатываем событие "type()"
            elif event.startswith("type("):
                message = event.replace("type(", "").replace(")", "")
                if typing_speed:
                    for character in message:
                        await element.type(character)
                        await asyncio.sleep(typing_speed)
                else:
                    await element.type(message)
        # Возвращаем результат или True, если результат пустой
        return result if result else True

    async def send_message(self, locator: dict | SimpleNamespace, message: str = None, typing_speed: float = 0) -> bool:
        """Отправляет сообщение веб-элементу.

        Args:
            locator (Union[dict, SimpleNamespace]): Информация о местоположении элемента на странице.
            message (str): Сообщение для отправки веб-элементу.
            typing_speed (float): Скорость набора сообщения в секундах.

        Returns:
            bool: Возвращает `True`, если сообщение было успешно отправлено, `False` в противном случае.
        """
        # Преобразуем locator в SimpleNamespace, если это словарь
        locator = (
            locator
            if isinstance(locator, SimpleNamespace)
            else SimpleNamespace(**locator) if isinstance(locator, dict) else None
        )
        # Получаем веб-элемент по локатору
        element = await self.get_webelement_by_locator(locator)
        # Если элемент не найден, возвращаем False
        if not element or (isinstance(element, list) and len(element) == 0):
            logger.debug(f"Элемент для отправки сообщения не найден: {locator=}")
            return False
        # Если элемент является списком, берем первый элемент
        element = element[0] if isinstance(element, list) else element

        # Отправляем сообщение с заданной скоростью набора текста
        if typing_speed:
            for character in message:
                await element.type(character)
                await asyncio.sleep(typing_speed)
        else:
            await element.type(message)

        return True

    async def goto(self, url: str) -> None:
        """
        Переходит по указанному URL.

        Args:
            url (str): URL для перехода.
        """
        # Если страница инициализирована, переходим по URL
        if self.page:
            try:
                await self.page.goto(url)
            except Exception as ex:
                logger.error(f'Ошибка во время перехода к {url=}', ex, exc_info=True)