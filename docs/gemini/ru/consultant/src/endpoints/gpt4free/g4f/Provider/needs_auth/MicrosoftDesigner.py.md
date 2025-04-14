### **Анализ кода модуля `MicrosoftDesigner.py`**

---

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код асинхронный, что позволяет эффективно обрабатывать запросы.
    - Используются `aiohttp` для асинхронных HTTP-запросов.
    - Присутствует обработка исключений.
    - Код разбит на отдельные функции, что улучшает читаемость.
    - Используются аннотации типов.
- **Минусы**:
    - Некоторые docstring отсутствуют или не соответствуют требованиям.
    - Используется `Union[]` вместо `|`
    - Не везде используется `logger` для логирования ошибок.
    - Не все переменные аннотированы типами.
    - В некоторых местах отсутствует описание функциональности кода.
    - Жестко закодированные значения, такие как `ClientId`, `ContainerId`, `FileToken` и другие параметры, которые могут изменяться.
    - Дублирование кода при формировании `form_data`.
    - Отсутствуют логи для отладки и мониторинга.
    - magic numbers

**Рекомендации по улучшению:**

1.  **Документирование кода**:
    *   Добавить docstring для всех функций и методов, включая описание аргументов, возвращаемых значений и возможных исключений.
    *   Перевести существующие docstring на русский язык и привести их к требуемому формату.
    *   Подробно описать назначение каждой функции, чтобы было понятно, что она делает.

2.  **Обработка исключений**:
    *   Использовать `logger.error` для логирования ошибок с передачей информации об исключении (`ex`, `exc_info=True`).
    *   Добавить обработку исключений в функции `readHAR` и `get_access_token_and_user_agent`.

3.  **Форматирование кода**:
    *   Привести все строки к использованию одинарных кавычек (`'`).
    *   Добавить пробелы вокруг операторов присваивания.

4.  **Безопасность и конфигурация**:
    *   Заменить жестко закодированные значения (`ClientId`, `ContainerId`, `FileToken` и другие) на переменные, которые можно задавать через конфигурационные файлы или переменные окружения.

5.  **Улучшение структуры**:
    *   Упростить создание `form_data` чтобы избежать дублирования кода.
    *   Разделить функцию `create_images` на более мелкие, чтобы улучшить читаемость и повторное использование кода.

6.  **Логирование**:
    *   Добавить логирование для отладки и мониторинга работы функций, особенно в циклах и при обработке данных.
    *   Добавить логирование важных шагов, таких как получение токена доступа, отправка запроса и получение ответа.

7.  **Типизация**:
    *   Добавить аннотации типов для всех переменных, где это возможно.
    *   Использовать `|` вместо `Union[]`.

**Оптимизированный код:**

```python
from __future__ import annotations

import uuid
import aiohttp
import random
import asyncio
import json

from typing import AsyncResult, Messages, Optional, List
from ...providers.response import ImageResponse
from ...errors import MissingRequirementsError, NoValidHarFileError
from ...requests.raise_for_status import raise_for_status
from ...requests.aiohttp import get_connector
from ...requests import get_nodriver
from ..Copilot import get_headers, get_har_files
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..helper import get_random_hex, format_image_prompt
from ... import debug
from src.logger import logger  # Добавлен импорт logger


class MicrosoftDesigner(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Модуль для работы с Microsoft Designer для генерации изображений.
    ===============================================================

    Этот модуль содержит класс :class:`MicrosoftDesigner`, который используется для взаимодействия
    с API Microsoft Designer для создания изображений на основе текстовых запросов.

    Пример использования:
    ----------------------
    >>> provider = MicrosoftDesigner()
    >>> result = await provider.create_async_generator(model='dall-e-3', messages=[{'role': 'user', 'content': 'A cat'}])
    """
    label: str = "Microsoft Designer"
    url: str = "https://designer.microsoft.com"
    working: bool = True
    use_nodriver: bool = True
    needs_auth: bool = True
    default_image_model: str = "dall-e-3"
    image_models: List[str] = [default_image_model, "1024x1024", "1024x1792", "1792x1024"]
    models: List[str] = image_models

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        prompt: Optional[str] = None,
        proxy: Optional[str] = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для генерации изображений.

        Args:
            model (str): Модель для генерации изображений.
            messages (Messages): Список сообщений для формирования запроса.
            prompt (Optional[str], optional): Дополнительный промпт. Defaults to None.
            proxy (Optional[str], optional): Прокси-сервер. Defaults to None.

        Yields:
            AsyncResult: Результат генерации изображения.
        """
        image_size: str = "1024x1024"
        if model != cls.default_image_model and model in cls.image_models:
            image_size = model
        yield await cls.generate(format_image_prompt(messages, prompt), image_size, proxy)

    @classmethod
    async def generate(cls, prompt: str, image_size: str, proxy: Optional[str] = None) -> ImageResponse:
        """
        Генерирует изображение на основе заданного промпта.

        Args:
            prompt (str): Текстовый промпт для генерации изображения.
            image_size (str): Размер изображения.
            proxy (Optional[str], optional): Прокси-сервер. Defaults to None.

        Returns:
            ImageResponse: Ответ сгенерированным изображением.

        Raises:
            NoValidHarFileError: Если не найден валидный HAR-файл.
        """
        try:
            access_token: str, user_agent: str = readHAR("https://designerapp.officeapps.live.com")
        except NoValidHarFileError as h:
            debug.log(f"{cls.__name__}: {h}")
            try:
                access_token, user_agent = await get_access_token_and_user_agent(cls.url, proxy)
            except MissingRequirementsError:
                raise h
        images: List[str] = await create_images(prompt, access_token, user_agent, image_size, proxy)
        return ImageResponse(images, prompt)


async def create_images(prompt: str, access_token: str, user_agent: str, image_size: str, proxy: Optional[str] = None, seed: Optional[int] = None) -> List[str]:
    """
    Создает изображения на основе заданного промпта, используя API Microsoft Designer.

    Args:
        prompt (str): Текстовый промпт для генерации изображений.
        access_token (str): Токен доступа для аутентификации.
        user_agent (str): User-Agent для HTTP-запросов.
        image_size (str): Размер изображения.
        proxy (Optional[str], optional): Прокси-сервер. Defaults to None.
        seed (Optional[int], optional): Зерно для случайной генерации. Defaults to None.

    Returns:
        List[str]: Список URL сгенерированных изображений.
    """
    url: str = 'https://designerapp.officeapps.live.com/designerapp/DallE.ashx?action=GetDallEImagesCogSci'
    if seed is None:
        seed = random.randint(0, 10000)

    headers: dict = {
        "User-Agent": user_agent,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US",
        'Authorization': f'Bearer {access_token}',
        "AudienceGroup": "Production",
        "Caller": "DesignerApp",
        "ClientId": "b5c2664a-7e9b-4a7a-8c9a-cd2c52dcf621",  # TODO: Вынести в конфиг
        "SessionId": str(uuid.uuid4()),
        "UserId": get_random_hex(16),
        "ContainerId": "1e2843a7-2a98-4a6c-93f2-42002de5c478",  # TODO: Вынести в конфиг
        "FileToken": "9f1a4cb7-37e7-4c90-b44d-cb61cfda4bb8",  # TODO: Вынести в конфиг
        "x-upload-to-storage-das": "1",
        "traceparent": "",
        "X-DC-Hint": "FranceCentral",
        "Platform": "Web",
        "HostApp": "DesignerApp",
        "ReleaseChannel": "",
        "IsSignedInUser": "true",
        "Locale": "de-DE",
        "UserType": "MSA",
        "x-req-start": "2615401",  # TODO: Что это?
        "ClientBuild": "1.0.20241120.9",  # TODO: Вынести в конфиг
        "ClientName": "DesignerApp",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Referer": "https://designer.microsoft.com/"
    }

    form_data: aiohttp.FormData = aiohttp.FormData()
    form_data.add_field('dalle-caption', prompt)
    form_data.add_field('dalle-scenario-name', 'TextToImage')
    form_data.add_field('dalle-batch-size', '4')
    form_data.add_field('dalle-image-response-format', 'UrlWithBase64Thumbnail')
    form_data.add_field('dalle-seed', str(seed))  # dalle-seed должен быть строкой
    form_data.add_field('ClientFlights', 'EnableBICForDALLEFlight')
    form_data.add_field('dalle-hear-back-in-ms', '1000')  # как строка
    form_data.add_field('dalle-include-b64-thumbnails', 'true')
    form_data.add_field('dalle-aspect-ratio-scaling-factor-b64-thumbnails', '0.3')  # как строка
    form_data.add_field('dalle-image-size', image_size)

    async with aiohttp.ClientSession(connector=get_connector(proxy=proxy)) as session:
        async with session.post(url, headers=headers, data=form_data) as response:
            try:
                await raise_for_status(response)
                response_data: dict = await response.json()
            except aiohttp.ClientResponseError as ex:
                logger.error(f'Ошибка при запросе к API: {ex}', exc_info=True)
                return []

        form_data.add_field('dalle-boost-count', str(response_data.get('dalle-boost-count', 0)))  # как строка
        polling_meta_data: dict = response_data.get('polling_response', {}).get('polling_meta_data', {})
        form_data.add_field('dalle-poll-url', polling_meta_data.get('poll_url', ''))

        while True:
            await asyncio.sleep(polling_meta_data.get('poll_interval', 1000) / 1000)
            async with session.post(url, headers=headers, data=form_data) as response:
                try:
                    await raise_for_status(response)
                    response_data: dict = await response.json()
                except aiohttp.ClientResponseError as ex:
                    logger.error(f'Ошибка при запросе к API: {ex}', exc_info=True)
                    return []
            images: List[str] = [image["ImageUrl"] for image in response_data.get('image_urls_thumbnail', [])]
            if images:
                return images


def readHAR(url: str) -> tuple[str, str]:
    """
    Читает HAR-файл и извлекает access_token и user_agent.

    Args:
        url (str): URL для поиска в HAR-файле.

    Returns:
        tuple[str, str]: access_token и user_agent.

    Raises:
        NoValidHarFileError: Если access_token не найден в HAR-файлах.
    """
    api_key: Optional[str] = None
    user_agent: Optional[str] = None
    for path in get_har_files():
        try:
            with open(path, 'rb') as file:
                try:
                    harFile: dict = json.loads(file.read())
                except json.JSONDecodeError as ex:
                    logger.error(f'Ошибка при чтении HAR-файла: {path}', exc_info=True)
                    continue
                for v in harFile['log']['entries']:
                    if v['request']['url'].startswith(url):
                        v_headers: dict = get_headers(v)
                        if "authorization" in v_headers:
                            api_key = v_headers["authorization"].split(maxsplit=1).pop()
                        if "user-agent" in v_headers:
                            user_agent = v_headers["user-agent"]
        except Exception as ex:
            logger.error(f'Ошибка при обработке HAR-файла: {path}', ex, exc_info=True)

    if api_key is None:
        raise NoValidHarFileError("No access token found in .har files")

    return api_key, user_agent


async def get_access_token_and_user_agent(url: str, proxy: Optional[str] = None) -> tuple[str, str]:
    """
    Получает access_token и user_agent, используя playwright.

    Args:
        url (str): URL для получения access_token и user_agent.
        proxy (Optional[str], optional): Прокси-сервер. Defaults to None.

    Returns:
        tuple[str, str]: access_token и user_agent.

    Raises:
        MissingRequirementsError: Если не удалось получить access_token.
    """
    browser, stop_browser = await get_nodriver(proxy=proxy, user_data_dir="designer")
    try:
        page = await browser.get(url)
        user_agent: str = await page.evaluate("navigator.userAgent")
        access_token: Optional[str] = None
        while access_token is None:
            access_token = await page.evaluate("""
                (() => {
                    for (var i = 0; i < localStorage.length; i++) {
                        try {
                            item = JSON.parse(localStorage.getItem(localStorage.key(i)));
                            if (item.credentialType == "AccessToken"
                                && item.expiresOn > Math.floor(Date.now() / 1000)
                                && item.target.includes("designerappservice")) {
                                return item.secret;
                            }
                        } catch(e) {}
                    }
                })()
            """)
            if access_token is None:
                await asyncio.sleep(1)
        await page.close()
        return access_token, user_agent
    except Exception as ex:
        logger.error('Ошибка при получении access_token и user_agent', ex, exc_info=True)
        raise
    finally:
        stop_browser()