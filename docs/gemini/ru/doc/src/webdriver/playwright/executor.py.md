# Модуль `executor.py`

## Обзор

Модуль `executor.py` предоставляет функциональность для взаимодействия с веб-элементами с использованием Playwright на основе предоставленных локаторов. Он обрабатывает разбор локаторов, взаимодействие с элементами и обработку ошибок.

## Подробнее

Этот модуль является частью проекта `hypotez` и предназначен для автоматизации взаимодействия с веб-страницами с использованием библиотеки Playwright. Он предоставляет класс `PlaywrightExecutor`, который позволяет выполнять различные действия с веб-элементами, такие как клики, ввод текста, получение атрибутов и т.д. Модуль также обеспечивает обработку ошибок и логирование действий.

## Классы

### `PlaywrightExecutor`

**Описание**: Класс `PlaywrightExecutor` выполняет команды на основе локаторов в стиле executor, используя Playwright.

**Атрибуты**:
- `driver`: Драйвер Playwright.
- `browser_type` (str): Тип запускаемого браузера (например, 'chromium', 'firefox', 'webkit'). По умолчанию 'chromium'.
- `page` (Optional[Page]): Текущая страница Playwright. Инициализируется как `None`.
- `config` (SimpleNamespace): Конфигурация Playwright, загруженная из файла `playwrid.json`.

**Методы**:
- `__init__(self, browser_type: str = 'chromium', **kwargs)`: Инициализирует экземпляр класса `PlaywrightExecutor`.
- `start(self) -> None`: Инициализирует Playwright и запускает экземпляр браузера.
- `stop(self) -> None`: Закрывает браузер Playwright и останавливает его экземпляр.
- `execute_locator(self, locator: Union[dict, SimpleNamespace], message: Optional[str] = None, typing_speed: float = 0, timeout: Optional[float] = 0, timeout_for_event: Optional[str] = 'presence_of_element_located') -> Union[str, list, dict, Locator, bool, None]`: Выполняет действия с веб-элементом на основе предоставленного локатора.
- `evaluate_locator(self, attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]`: Оценивает и обрабатывает атрибуты локатора.
- `get_attribute_by_locator(self, locator: dict | SimpleNamespace) -> Optional[str | List[str] | dict]`: Получает указанный атрибут из веб-элемента.
- `get_webelement_by_locator(self, locator: dict | SimpleNamespace) -> Optional[Locator | List[Locator]]`: Получает веб-элемент, используя локатор.
- `get_webelement_as_screenshot(self, locator: dict | SimpleNamespace, webelement: Optional[Locator] = None) -> Optional[bytes]`: Делает скриншот найденного веб-элемента.
- `execute_event(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> Union[str, List[str], bytes, List[bytes], bool]`: Выполняет событие, связанное с локатором.
- `send_message(self, locator: dict | SimpleNamespace, message: str = None, typing_speed: float = 0) -> bool`: Отправляет сообщение веб-элементу.
- `goto(self, url: str) -> None`: Переходит по указанному URL.

### `__init__`
```python
    def __init__(self, browser_type: str = 'chromium', **kwargs):
        """
        Инициализирует Playwright executor.

        Args:
            browser_type (str): Тип браузера для запуска (например, 'chromium', 'firefox', 'webkit').
        """
        self.driver = None
        self.browser_type = browser_type
        self.page: Optional[Page] = None
        self.config: SimpleNamespace = j_loads_ns(
            Path(gs.path.src / 'webdriver' / 'playwright' / 'playwrid.json')
        )
```

**Назначение**: Инициализация экземпляра класса `PlaywrightExecutor`.

**Параметры**:
- `browser_type` (str): Тип браузера для запуска (например, 'chromium', 'firefox', 'webkit'). По умолчанию 'chromium'.
- `**kwargs`: Дополнительные параметры.

**Как работает функция**:
- Устанавливает драйвер в `None`.
- Устанавливает тип браузера из аргумента `browser_type`.
- Устанавливает страницу в `None`.
- Загружает конфигурацию из файла `playwrid.json` с использованием `j_loads_ns` и сохраняет её в атрибуте `config`.

**Примеры**:
```python
executor = PlaywrightExecutor(browser_type='firefox')
```

### `start`
```python
    async def start(self) -> None:
        """
        Инициализирует Playwright и запускает экземпляр браузера.
        """
        try:
            self.driver = await async_playwright().start()
            browser = await getattr(self.driver, self.browser_type).launch(headless=True, args=self.config.options)
            self.page = await browser.new_page()
        except Exception as ex:
            logger.critical('Playwright не удалось запустить браузер', ex)
```

**Назначение**: Инициализация Playwright и запуск экземпляра браузера.

**Как работает функция**:
- Пытается запустить Playwright с помощью `async_playwright().start()`.
- Запускает браузер указанного типа (из атрибута `browser_type`) в режиме `headless` (без графического интерфейса) с дополнительными опциями из конфигурации (`self.config.options`).
- Создает новую страницу в браузере.
- В случае ошибки логирует критическое сообщение об ошибке.

**Примеры**:
```python
await executor.start()
```

### `stop`
```python
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
            logger.error(f'Playwright не удалось закрыть браузер: {ex}')
```

**Назначение**: Закрытие браузера Playwright и остановка его экземпляра.

**Как работает функция**:
- Закрывает текущую страницу, если она существует (`self.page`).
- Останавливает драйвер, если он существует (`self.driver`).
- Устанавливает драйвер в `None`.
- Логирует информационное сообщение об остановке Playwright.
- В случае ошибки логирует сообщение об ошибке.

**Примеры**:
```python
await executor.stop()
```

### `execute_locator`
```python
    async def execute_locator(
            self,
            locator: Union[dict, SimpleNamespace],
            message: Optional[str] = None,
            typing_speed: float = 0,
            timeout: Optional[float] = 0,
            timeout_for_event: Optional[str] = 'presence_of_element_located',
    ) -> Union[str, list, dict, Locator, bool, None]:
        """
        Выполняет действия с веб-элементом на основе предоставленного локатора.

        Args:
            locator (Union[dict, SimpleNamespace]): Данные локатора (словарь или SimpleNamespace).
            message (Optional[str], optional): Необязательное сообщение для событий. Defaults to None.
            typing_speed (Optional[float], optional): Необязательная скорость ввода для событий. Defaults to 0.
            timeout (Optional[float], optional): Таймаут для поиска элемента (в секундах). Defaults to 0.
            timeout_for_event (Optional[str], optional): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). Defaults to 'presence_of_element_located'.

        Returns:
            Union[str, list, dict, Locator, bool, None]: Результат операции, который может быть строкой, списком, словарем, локатором, булевым значением или None.
        """
        if isinstance(locator, dict):
            locator = SimpleNamespace(**locator)

        if not getattr(locator, "attribute", None) and not getattr(locator, "selector", None):
            logger.debug("Предоставлен пустой локатор.")
            return None

        async def _parse_locator(
                locator: SimpleNamespace, message: Optional[str]
        ) -> Union[str, list, dict, Locator, bool, None]:
            """Разбирает и выполняет инструкции локатора."""
            if locator.event and locator.attribute and locator.mandatory is None:
                logger.debug("Локатор с событием и атрибутом, но отсутствует обязательный флаг. Пропускается.")
                return None

            if isinstance(locator.attribute, str) and isinstance(locator.by, str):
                try:
                    if locator.attribute:
                        locator.attribute = await self.evaluate_locator(locator.attribute)
                        if locator.by == "VALUE":
                            return locator.attribute
                except Exception as ex:
                    logger.debug(f"Ошибка получения атрибута по 'VALUE': {locator}, ошибка: {ex}")
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
                            **{
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
                logger.warning("Локатор не содержит списки 'selector' и 'by' или неверное значение 'sorted'.")

        return await _parse_locator(locator, message)
```

**Назначение**: Выполнение действий с веб-элементом на основе предоставленного локатора.

**Параметры**:
- `locator` (Union[dict, SimpleNamespace]): Данные локатора (словарь или `SimpleNamespace`).
- `message` (Optional[str], optional): Необязательное сообщение для событий. По умолчанию `None`.
- `typing_speed` (Optional[float], optional): Необязательная скорость ввода для событий. По умолчанию `0`.
- `timeout` (Optional[float], optional): Таймаут для поиска элемента (в секундах). По умолчанию `0`.
- `timeout_for_event` (Optional[str], optional): Условие ожидания (`'presence_of_element_located'`, `'visibility_of_all_elements_located'`). По умолчанию `'presence_of_element_located'`.

**Возвращает**:
- `Union[str, list, dict, Locator, bool, None]`: Результат операции, который может быть строкой, списком, словарем, локатором, булевым значением или `None`.

**Внутренние функции**:

#### `_parse_locator`
```python
            async def _parse_locator(
                locator: SimpleNamespace, message: Optional[str]
        ) -> Union[str, list, dict, Locator, bool, None]:
            """Разбирает и выполняет инструкции локатора."""
            if locator.event and locator.attribute and locator.mandatory is None:
                logger.debug("Локатор с событием и атрибутом, но отсутствует обязательный флаг. Пропускается.")
                return None

            if isinstance(locator.attribute, str) and isinstance(locator.by, str):
                try:
                    if locator.attribute:
                        locator.attribute = await self.evaluate_locator(locator.attribute)
                        if locator.by == "VALUE":
                            return locator.attribute
                except Exception as ex:
                    logger.debug(f"Ошибка получения атрибута по 'VALUE': {locator}, ошибка: {ex}")
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
                            **{
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
                logger.warning("Локатор не содержит списки 'selector' и 'by' или неверное значение 'sorted'.")
```
**Назначение**: Разбирает и выполняет инструкции локатора.

**Как работает функция**:

- Проверяет, является ли входной `locator` словарем, и преобразует его в `SimpleNamespace`, если это так.
- Если `locator` не содержит атрибутов `attribute` или `selector`, функция регистрирует отладочное сообщение и возвращает `None`.
- Проверяет наличие события и атрибута, при этом отсутствии флага `mandatory`.
- Если `locator.attribute` и `locator.by` являются строками:
  - Пытается получить значение атрибута, используя `self.evaluate_locator`.
  - Если `locator.by == "VALUE"`, возвращает значение атрибута.
  - Если указано событие (`locator.event`), вызывает `self.execute_event` для выполнения этого события.
  - В противном случае пытается получить атрибут с помощью `self.get_attribute_by_locator` или веб-элемент с помощью `self.get_webelement_by_locator`.
- Если `locator.selector` и `locator.by` являются списками и `locator.sorted == "pairs"`, функция создает пары элементов на основе атрибутов, селекторов и событий, а затем рекурсивно вызывает `_parse_locator` для каждой пары.
- Если условия не выполняются, функция логирует предупреждение и ничего не возвращает.

**Примеры**:
```python
result = await executor.execute_locator(locator_data)
```

### `evaluate_locator`
```python
    async def evaluate_locator(self, attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]:
        """
        Оценивает и обрабатывает атрибуты локатора.

        Args:
            attribute (str | List[str] | dict): Атрибут для оценки (может быть строкой, списком строк или словарем).

        Returns:
            Optional[str | List[str] | dict]: Оцененный атрибут, который может быть строкой, списком строк или словарем.
        """

        async def _evaluate(attr: str) -> Optional[str]:
            return attr

        if isinstance(attribute, list):\n            return await asyncio.gather(*[_evaluate(attr) for attr in attribute])
        return await _evaluate(str(attribute))
```

**Назначение**: Оценивает и обрабатывает атрибуты локатора.

**Параметры**:
- `attribute` (str | List[str] | dict): Атрибут для оценки (может быть строкой, списком строк или словарем).

**Возвращает**:
- `Optional[str | List[str] | dict]`: Оцененный атрибут, который может быть строкой, списком строк или словарем.

**Внутренние функции**:

#### `_evaluate`
```python
        async def _evaluate(attr: str) -> Optional[str]:
            return attr
```

**Назначение**: Возвращает атрибут.

**Как работает функция**:

- Возвращает входной атрибут.

**Примеры**:
```python
evaluated_attribute = await executor.evaluate_locator(attribute='example')
```

### `get_attribute_by_locator`
```python
    async def get_attribute_by_locator(self, locator: dict | SimpleNamespace) -> Optional[str | List[str] | dict]:
        """
        Получает указанный атрибут из веб-элемента.

        Args:
            locator (dict | SimpleNamespace): Данные локатора (словарь или SimpleNamespace).

        Returns:
            Optional[str | List[str] | dict]: Атрибут или None.
        """
        locator = (
            locator if isinstance(locator, SimpleNamespace) else SimpleNamespace(**locator) if isinstance(locator, dict) else None
        )
        element = await self.get_webelement_by_locator(locator)

        if not element:
            logger.debug(f"Элемент не найден: {locator=}")
            return None

        def _parse_dict_string(attr_string: str) -> dict | None:
            """Разбирает строку типа '{attr1:attr2}' в словарь."""
            try:
                return {k.strip(): v.strip() for k, v in (pair.split(":") for pair in attr_string.strip("{}").split(","))}\n            except ValueError as ex:\n                logger.debug(f"Недопустимый формат строки атрибута: {attr_string}", ex)\n                return None\n

        async def _get_attribute(el: Locator, attr: str) -> Optional[str]:
            """Извлекает один атрибут из Locator."""
            try:
                return await el.get_attribute(attr)
            except Exception as ex:
                logger.debug(f"Ошибка получения атрибута '{attr}' из элемента: {ex}")
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

        if isinstance(element, list):\n             return await asyncio.gather(*[_get_attribute(el, locator.attribute) for el in element])

        return await _get_attribute(element, locator.attribute)
```

**Назначение**: Получает указанный атрибут из веб-элемента.

**Параметры**:
- `locator` (dict | SimpleNamespace): Данные локатора (словарь или `SimpleNamespace`).

**Возвращает**:
- `Optional[str | List[str] | dict]`: Атрибут или `None`.

**Внутренние функции**:

#### `_parse_dict_string`
```python
        def _parse_dict_string(attr_string: str) -> dict | None:
            """Разбирает строку типа '{attr1:attr2}' в словарь."""
            try:
                return {k.strip(): v.strip() for k, v in (pair.split(":") for pair in attr_string.strip("{}").split(","))}\n            except ValueError as ex:\n                logger.debug(f"Недопустимый формат строки атрибута: {attr_string}", ex)\n                return None
```

**Назначение**: Разбирает строку типа '{attr1:attr2}' в словарь.

**Как работает функция**:

- Разбирает строку в формате `{ключ: значение, ...}` и преобразует её в словарь.

#### `_get_attribute`
```python
        async def _get_attribute(el: Locator, attr: str) -> Optional[str]:
            """Извлекает один атрибут из Locator."""
            try:
                return await el.get_attribute(attr)
            except Exception as ex:
                logger.debug(f"Ошибка получения атрибута '{attr}' из элемента: {ex}")
                return None
```

**Назначение**: Извлекает один атрибут из `Locator`.

**Как работает функция**:

- Пытается получить значение атрибута `attr` из элемента `el`.
- В случае ошибки логирует сообщение об ошибке.

#### `_get_attributes_from_dict`
```python
        async def _get_attributes_from_dict(element: Locator, attr_dict: dict) -> dict:
            """Извлекает несколько атрибутов на основе словаря."""
            result = {}
            for key, value in attr_dict.items():
                result[key] = await _get_attribute(element, key)
                result[value] = await _get_attribute(element, value)

            return result
```

**Назначение**: Извлекает несколько атрибутов на основе словаря.

**Как работает функция**:

- Получает значения атрибутов на основе словаря, где каждый ключ и значение в словаре рассматриваются как имена атрибутов, которые нужно получить.

**Примеры**:
```python
attribute = await executor.get_attribute_by_locator(locator_data)
```

### `get_webelement_by_locator`
```python
    async def get_webelement_by_locator(self, locator: dict | SimpleNamespace) -> Optional[Locator | List[Locator]]:
        """
        Получает веб-элемент, используя локатор.

        Args:
            locator (dict | SimpleNamespace): Данные локатора (словарь или SimpleNamespace).

        Returns:
            Optional[Locator | List[Locator]]: Playwright Locator
        """
        locator = (
            SimpleNamespace(**locator)
            if isinstance(locator, dict)
            else locator
        )
        if not locator:
            logger.error("Предоставлен недействительный локатор.")
            return None
        try:\n             if locator.by.upper() == "XPATH":\n                elements = self.page.locator(f\'xpath={locator.selector}\')\n             else:\n                 elements = self.page.locator(locator.selector)\n\n             if locator.if_list == \'all\':\n                return await elements.all()\n             elif locator.if_list == \'first\':\n                 return elements.first\n             elif locator.if_list == \'last\':\n                return elements.last\n             elif locator.if_list == \'even\':\n                list_elements = await elements.all()\n                return [list_elements[i] for i in range(0, len(list_elements), 2)]\n             elif locator.if_list == \'odd\':\n                list_elements = await elements.all()\n                return [list_elements[i] for i in range(1, len(list_elements), 2)]\n             elif isinstance(locator.if_list, list):\n                 list_elements = await elements.all()\n                 return [list_elements[i] for i in locator.if_list]\n             elif isinstance(locator.if_list, int):\n                 list_elements = await elements.all()\n                 return list_elements[locator.if_list - 1]\n             else:\n                 return elements\n        except Exception as ex:\n            logger.error(f\'Ошибка поиска элемента: {locator=}\', ex)\n            return None
```

**Назначение**: Получает веб-элемент, используя локатор.

**Параметры**:
- `locator` (dict | SimpleNamespace): Данные локатора (словарь или `SimpleNamespace`).

**Возвращает**:
- `Optional[Locator | List[Locator]]`: Playwright `Locator`.

**Как работает функция**:

- Преобразует `locator` в `SimpleNamespace`, если он является словарем.
- Если `locator` недействителен, функция регистрирует ошибку и возвращает `None`.
- В зависимости от значения `locator.by` (верхний регистр):
  - Если `locator.by.upper() == "XPATH"`, использует XPath для поиска элемента.
  - В противном случае использует `locator.selector` для поиска элемента.
- В зависимости от значения `locator.if_list`:
  - Если `locator.if_list == 'all'`, возвращает все элементы, соответствующие локатору.
  - Если `locator.if_list == 'first'`, возвращает первый элемент, соответствующий локатору.
  - Если `locator.if_list == 'last'`, возвращает последний элемент, соответствующий локатору.
  - Если `locator.if_list == 'even'`, возвращает все четные элементы, соответствующие локатору.
  - Если `locator.if_list == 'odd'`, возвращает все нечетные элементы, соответствующие локатору.
  - Если `locator.if_list` является списком, возвращает элементы, соответствующие индексам в списке.
  - Если `locator.if_list` является целым числом, возвращает элемент по указанному индексу (индекс начинается с 1).
  - В противном случае возвращает элемент(ы), соответствующие локатору.
- В случае ошибки функция регистрирует ошибку и возвращает `None`.

**Примеры**:
```python
webelement = await executor.get_webelement_by_locator(locator_data)
```

### `get_webelement_as_screenshot`
```python
    async def get_webelement_as_screenshot(self, locator: dict | SimpleNamespace, webelement: Optional[Locator] = None) -> Optional[bytes]:
        """
        Делает скриншот найденного веб-элемента.

        Args:
            locator (dict | SimpleNamespace): Данные локатора (словарь или SimpleNamespace).
            webelement (Optional[Locator], optional): Веб-элемент Locator. Defaults to None.

        Returns:
            Optional[bytes]: Скриншот в байтах или None.
        """
        locator = (
            locator if isinstance(locator, SimpleNamespace) else SimpleNamespace(**locator) if isinstance(locator, dict) else None
        )

        if not webelement:
            webelement = await self.get_webelement_by_locator(locator)

        if not webelement:
            logger.debug(f"Элемент для скриншота не найден: {locator=}")
            return None
        try:\n             return await webelement.screenshot()\n        except Exception as ex:\n            logger.error(f"Не удалось сделать скриншот: {locator=}", ex)\n            return None
```

**Назначение**: Делает скриншот найденного веб-элемента.

**Параметры**:
- `locator` (dict | SimpleNamespace): Данные локатора (словарь или `SimpleNamespace`).
- `webelement` (Optional[Locator], optional): Веб-элемент `Locator`. По умолчанию `None`.

**Возвращает**:
- `Optional[bytes]`: Скриншот в байтах или `None`.

**Как работает функция**:

- Преобразует `locator` в `SimpleNamespace`, если он является словарем.
- Если `webelement` не предоставлен, пытается получить его с помощью `self.get_webelement_by_locator(locator)`.
- Если `webelement` не найден, функция регистрирует отладочное сообщение и возвращает `None`.
- Пытается сделать скриншот элемента и возвращает его в виде байтов.
- В случае ошибки функция регистрирует ошибку и возвращает `None`.

**Примеры**:
```python
screenshot = await executor.get_webelement_as_screenshot(locator_data)
```

### `execute_event`
```python
    async def execute_event(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> Union[str, List[str], bytes, List[bytes], bool]:
        """
        Выполняет событие, связанное с локатором.

         Args:
            locator (dict | SimpleNamespace): Данные локатора (словарь или SimpleNamespace).
            message (Optional[str], optional): Необязательное сообщение для событий. Defaults to None.
            typing_speed (Optional[float], optional): Необязательная скорость ввода для событий. Defaults to 0.

        Returns:
           Union[str, List[str], bytes, List[bytes], bool]: Execution status.
        """
        locator = (
            locator if isinstance(locator, SimpleNamespace) else SimpleNamespace(**locator) if isinstance(locator, dict) else None
        )
        events = str(locator.event).split(";")
        result: list = []
        element = await self.get_webelement_by_locator(locator)
        if not element:
            logger.debug(f"Элемент для события не найден: {locator=}")
            return False

        element = element[0] if isinstance(element, list) else element

        for event in events:
            if event == "click()":
                try:
                    await element.click()
                    continue
                except Exception as ex:
                     logger.error(f"Ошибка во время события click: {locator=}", ex)\n                     return False

            elif event.startswith("pause("):\n                match = re.match(r"pause\\((\\d+)\\)", event)\n                if match:\n                    pause_duration = int(match.group(1))\n                    await asyncio.sleep(pause_duration)\n                    continue\n                logger.debug(f"Не удалось разобрать событие pause: {locator=}")\n                return False

            elif event == "upload_media()":
                if not message:
                    logger.debug(f"Сообщение обязательно для события upload_media: {message!r}")
                    return False
                try:
                    await element.set_input_files(message)\n                    continue\n                except Exception as ex:\n                     logger.error(f"Ошибка во время загрузки файла: {locator=}, {message=}", ex)\n                     return False\n

            elif event == "screenshot()":
                 try:
                     result.append(await self.get_webelement_as_screenshot(locator, webelement=element))\n                 except Exception as ex:\n                      logger.error(f"Ошибка во время снятия скриншота: {locator=}", ex)\n                      return False

            elif event == "clear()":
                 try:
                     await element.clear()\n                     continue\n                 except Exception as ex:\n                      logger.error(f"Ошибка во время очистки поля: {locator=}", ex)\n                      return False\n

            elif event.startswith("send_keys("):\n                keys_to_send = event.replace("send_keys(", "").replace(")", "").split("+")\n                try:\n                    for key in keys_to_send:\n                        key = key.strip().strip("\'")\n                        if key:\n                            await element.type(key)\n                except Exception as ex:\n                    logger.error(f"Ошибка при отправке ключей: {locator=}", ex)\n                    return False

            elif event.startswith("type("):\n                message = event.replace("type(", "").replace(")", "")\n                if typing_speed:\n                     for character in message:\n                         await element.type(character)\n                         await asyncio.sleep(typing_speed)\n                else:\n                    await element.type(message)
        return result if result else True
```

**Назначение**: Выполняет событие, связанное с локатором.

**Параметры**:
- `locator` (dict | SimpleNamespace): Данные локатора (словарь или `SimpleNamespace`).
- `message` (Optional[str], optional): Необязательное сообщение для событий. По умолчанию `None`.
- `typing_speed` (Optional[float], optional): Необязательная скорость ввода для событий. По умолчанию `0`.

**Возвращает**:
- `Union[str, List[str], bytes, List[bytes], bool]`: Статус выполнения.

**Как работает функция**:

- Преобразует `locator` в `SimpleNamespace`, если он является словарем.
- Разбивает строку событий (`locator.event`) на отдельные события по разделителю `;`.
- Получает веб-элемент с помощью `self.get_webelement_by_locator(locator)`.
- Если элемент не найден, функция регистрирует отладочное сообщение и возвращает `False`.
- Выполняет события в цикле:
  - `click()`: выполняет клик по элементу.
  - `pause(duration)`: приостанавливает выполнение на указанное время в секундах.
  - `upload_media()`: загружает медиафайл. Требует обязательного наличия сообщения (`message`).
  - `screenshot()`: делает скриншот элемента.
  - `clear()`: очищает поле.
  - `send_keys(keys)`: отправляет клавиши элементу.
  - `type(message)`: вводит сообщение в элемент.

**Примеры**:
```python
execution_status = await executor.execute_event(locator_data, message='example')
```

### `send_message`
```python
    async def send_message(self, locator: dict | SimpleNamespace, message: str = None, typing_speed: float = 0) -> bool:
        """Отправляет сообщение веб-элементу.

        Args:
             locator (dict | SimpleNamespace): Информация о местоположении элемента на странице.
             message (str, optional): Сообщение, которое нужно отправить веб-элементу. Defaults to None.
             typing_speed (float, optional): Скорость ввода