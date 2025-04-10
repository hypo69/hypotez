### **Анализ кода модуля `MicrosoftDesigner.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
  - Асинхронный код, что позволяет эффективно использовать ресурсы.
  - Использование `aiohttp` для асинхронных HTTP-запросов.
  - Класс `MicrosoftDesigner` хорошо структурирован и использует `ProviderModelMixin` для наследования функциональности.
- **Минусы**:
  - Отсутствуют аннотации типов для большинства переменных и параметров функций.
  - Не все функции имеют docstring, что затрудняет понимание их назначения и использования.
  - В коде присутствуют magic strings (например, URL'ы), которые следует вынести в константы.
  - Обработка ошибок выполняется, но логирование не всегда присутствует.

#### **Рекомендации по улучшению**:

1.  **Добавить docstring**:
    - Добавить docstring для всех функций и методов, включая описание аргументов, возвращаемых значений и возможных исключений.
    - Описать назначение модуля в целом в начале файла.

2.  **Добавить аннотации типов**:
    - Добавить аннотации типов для всех переменных и параметров функций для повышения читаемости и облегчения отладки.

3.  **Улучшить обработку ошибок и логирование**:

    *   Добавить логирование с использованием модуля `logger` из `src.logger` для отслеживания ошибок и предупреждений.
    *   Использовать `logger.error` для записи ошибок и `logger.info` для информационных сообщений.

4.  **Вынести константы**:
    - Заменить magic strings (например, URL'ы) константами, чтобы упростить поддержку и изменение кода.

5.  **Улучшить читаемость**:
    - Добавить пробелы вокруг операторов присваивания и других операторов для улучшения читаемости.
    - Использовать более понятные имена переменных.

#### **Оптимизированный код**:

```python
from __future__ import annotations

import uuid
import aiohttp
import random
import asyncio
import json
from typing import AsyncGenerator, Optional, List, Tuple

from src.logger import logger # Добавлен импорт logger
from ...providers.response import ImageResponse
from ...errors import MissingRequirementsError, NoValidHarFileError
from ...typing import AsyncResult, Messages
from ...requests.raise_for_status import raise_for_status
from ...requests.aiohttp import get_connector
from ...requests import get_nodriver
from ..Copilot import get_headers, get_har_files
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..helper import get_random_hex, format_image_prompt
from ... import debug
from pathlib import Path


"""
Модуль для работы с Microsoft Designer
========================================

Модуль содержит класс :class:`MicrosoftDesigner`, который используется для генерации изображений с использованием API Microsoft Designer.

Пример использования
----------------------

>>> provider = MicrosoftDesigner()
>>> async for image in provider.create_async_generator(model='dall-e-3', messages=[{'role': 'user', 'content': 'A cat'}]):
...     print(image)
"""

class MicrosoftDesigner(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Провайдер для генерации изображений через Microsoft Designer.
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
        prompt: str = None,
        proxy: str = None,
        **kwargs
    ) -> AsyncGenerator[ImageResponse, None]:
        """
        Создает асинхронный генератор для получения изображений.

        Args:
            model (str): Модель для генерации изображений.
            messages (Messages): Список сообщений для формирования запроса.
            prompt (str, optional): Дополнительный промпт. По умолчанию None.
            proxy (str, optional): Прокси-сервер. По умолчанию None.

        Yields:
            ImageResponse: Сгенерированное изображение.
        """
        image_size = "1024x1024"
        if model != cls.default_image_model and model in cls.image_models:
            image_size = model
        yield await cls.generate(format_image_prompt(messages, prompt), image_size, proxy)

    @classmethod
    async def generate(cls, prompt: str, image_size: str, proxy: str = None) -> ImageResponse:
        """
        Генерирует изображение на основе заданного промпта.

        Args:
            prompt (str): Текст запроса для генерации изображения.
            image_size (str): Размер изображения.
            proxy (str, optional): Прокси-сервер. По умолчанию None.

        Returns:
            ImageResponse: Объект ImageResponse с сгенерированными изображениями.

        Raises:
            NoValidHarFileError: Если не найден валидный HAR-файл.
            Exception: Если возникает ошибка при создании изображений.
        """
        try:
            access_token, user_agent = readHAR("https://designerapp.officeapps.live.com")
        except NoValidHarFileError as ex:
            debug.log(f"{cls.__name__}: {ex}")
            try:
                access_token, user_agent = await get_access_token_and_user_agent(cls.url, proxy)
            except MissingRequirementsError:
                raise ex
        images = await create_images(prompt, access_token, user_agent, image_size, proxy)
        return ImageResponse(images, prompt)

async def create_images(prompt: str, access_token: str, user_agent: str, image_size: str, proxy: str = None, seed: int = None) -> List[str]:
    """
    Создает изображения на основе заданного промпта и параметров.

    Args:
        prompt (str): Текст запроса для генерации изображения.
        access_token (str): Токен доступа.
        user_agent (str): User-Agent.
        image_size (str): Размер изображения.
        proxy (str, optional): Прокси-сервер. По умолчанию None.
        seed (int, optional): Зерно для случайной генерации. По умолчанию None.

    Returns:
        List[str]: Список URL сгенерированных изображений.

    Raises:
        Exception: Если возникает ошибка при запросе к API.
    """
    url: str = 'https://designerapp.officeapps.live.com/designerapp/DallE.ashx?action=GetDallEImagesCogSci'
    if seed is None:
        seed: int = random.randint(0, 10000)

    headers: dict[str, str] = {
        "User-Agent": user_agent,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US",
        'Authorization': f'Bearer {access_token}',
        "AudienceGroup": "Production",
        "Caller": "DesignerApp",
        "ClientId": "b5c2664a-7e9b-4a7a-8c9a-cd2c52dcf621",
        "SessionId": str(uuid.uuid4()),
        "UserId": get_random_hex(16),
        "ContainerId": "1e2843a7-2a98-4a6c-93f2-42002de5c478",
        "FileToken": "9f1a4cb7-37e7-4c90-b44d-cb61cfda4bb8",
        "x-upload-to-storage-das": "1",
        "traceparent": "",
        "X-DC-Hint": "FranceCentral",
        "Platform": "Web",
        "HostApp": "DesignerApp",
        "ReleaseChannel": "",
        "IsSignedInUser": "true",
        "Locale": "de-DE",
        "UserType": "MSA",
        "x-req-start": "2615401",
        "ClientBuild": "1.0.20241120.9",
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
    form_data.add_field('dalle-seed', str(seed))
    form_data.add_field('ClientFlights', 'EnableBICForDALLEFlight')
    form_data.add_field('dalle-hear-back-in-ms', '1000')
    form_data.add_field('dalle-include-b64-thumbnails', 'true')
    form_data.add_field('dalle-aspect-ratio-scaling-factor-b64-thumbnails', '0.3')
    form_data.add_field('dalle-image-size', image_size)

    async with aiohttp.ClientSession(connector=get_connector(proxy=proxy)) as session:
        async with session.post(url, headers=headers, data=form_data) as response:
            await raise_for_status(response)
            response_data: dict = await response.json()
        form_data.add_field('dalle-boost-count', str(response_data.get('dalle-boost-count', 0)))
        polling_meta_data: dict = response_data.get('polling_response', {}).get('polling_meta_data', {})
        form_data.add_field('dalle-poll-url', polling_meta_data.get('poll_url', ''))

        while True:
            await asyncio.sleep(polling_meta_data.get('poll_interval', 1000) / 1000)
            async with session.post(url, headers=headers, data=form_data) as response:
                await raise_for_status(response)
                response_data: dict = await response.json()
            images: List[str] = [image["ImageUrl"] for image in response_data.get('image_urls_thumbnail', [])]
            if images:
                return images

def readHAR(url: str) -> Tuple[str, str]:
    """
    Читает HAR-файл для получения токена доступа и user-agent.

    Args:
        url (str): URL для поиска в HAR-файле.

    Returns:
        Tuple[str, str]: Токен доступа и user-agent.

    Raises:
        NoValidHarFileError: Если не найден валидный HAR-файл.
    """
    api_key: Optional[str] = None
    user_agent: Optional[str] = None
    for path in get_har_files():
        try:
            with open(path, 'rb') as file:
                try:
                    harFile: dict = json.loads(file.read())
                except json.JSONDecodeError as ex:
                    # Error: not a HAR file!
                    logger.error(f"Invalid HAR file: {path}", ex, exc_info=True)
                    continue
                for v in harFile['log']['entries']:
                    if v['request']['url'].startswith(url):
                        v_headers: dict = get_headers(v)
                        if "authorization" in v_headers:
                            api_key: str = v_headers["authorization"].split(maxsplit=1).pop()
                        if "user-agent" in v_headers:
                            user_agent: str = v_headers["user-agent"]
        except Exception as ex:
            logger.error(f"Error reading HAR file: {path}", ex, exc_info=True)

    if api_key is None:
        raise NoValidHarFileError("No access token found in .har files")

    return api_key, user_agent

async def get_access_token_and_user_agent(url: str, proxy: str = None) -> Tuple[str, str]:
    """
    Получает токен доступа и user-agent с использованием Playwright.

    Args:
        url (str): URL для получения токена доступа и user-agent.
        proxy (str, optional): Прокси-сервер. По умолчанию None.

    Returns:
        Tuple[str, str]: Токен доступа и user-agent.

    Raises:
        Exception: Если возникает ошибка при работе с браузером.
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
        logger.error("Error getting access token and user agent", ex, exc_info=True)
        raise
    finally:
        await stop_browser()