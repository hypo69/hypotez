### **Анализ кода модуля `create_images.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код структурирован и логически разделен на функции.
  - Используются асинхронные операции для неблокирующего выполнения.
  - Обработка ошибок реализована с использованием исключений.
- **Минусы**:
  - Отсутствует полное описание всех функций и их параметров в формате docstring.
  - Не все переменные аннотированы типами.
  - Не используется `logger` для логирования ошибок и информации.

#### **Рекомендации по улучшению**:
1. **Добавить docstring для каждой функции и метода**:
   - Описать назначение, параметры, возвращаемые значения и возможные исключения.
   - Использовать стиль Google Python Docstrings.

2. **Аннотировать типы для всех переменных и параметров функций**:
   - Это улучшит читаемость и облегчит отладку.

3. **Использовать `logger` для логирования**:
   - Заменить `print` на `logger.info` и `logger.error`.
   - Добавить логирование важных этапов выполнения кода.

4. **Обработка исключений**:
   - Использовать `ex` вместо `e` в блоках `except`.
   - Логировать ошибки с использованием `logger.error(..., ex, exc_info=True)`.

5. **Удалить неиспользуемые импорты**:
   - Проверить и удалить неиспользуемые импорты.

6. **Использовать одинарные кавычки**:
   - Заменить двойные кавычки на одинарные, где это необходимо.

#### **Оптимизированный код**:
```python
from __future__ import annotations

import asyncio
import time
import json
from aiohttp import ClientSession, BaseConnector
from urllib.parse import quote
from typing import List, Dict, Optional

try:
    from bs4 import BeautifulSoup
    has_requirements: bool = True
except ImportError:
    has_requirements: bool = False

from ..helper import get_connector
from ...errors import MissingRequirementsError, RateLimitError

from src.logger import logger  # Import logger module

BING_URL: str = "https://www.bing.com"
TIMEOUT_LOGIN: int = 1200
TIMEOUT_IMAGE_CREATION: int = 300
ERRORS: List[str] = [
    "this prompt is being reviewed",
    "this prompt has been blocked",
    "we're working hard to offer image creator in more languages",
    "we can't create your images right now"
]
BAD_IMAGES: List[str] = [
    "https://r.bing.com/rp/in-2zU3AJUdkgFe7ZKv19yPBHVs.png",
    "https://r.bing.com/rp/TX9QuO3WzcCJz1uaaSwQAz39Kb0.jpg",
]


def create_session(cookies: Dict[str, str], proxy: Optional[str] = None, connector: Optional[BaseConnector] = None) -> ClientSession:
    """
    Создает новый клиентский сеанс с указанными куками и заголовками.

    Args:
        cookies (Dict[str, str]): Куки, которые будут использоваться для сеанса.
        proxy (Optional[str]): Прокси-сервер для использования (необязательно).
        connector (Optional[BaseConnector]): Пользовательский коннектор aiohttp (необязательно).

    Returns:
        ClientSession: Созданный клиентский сеанс.
    """
    headers: Dict[str, str] = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "content-type": "application/x-www-form-urlencoded",
        "referrer-policy": "origin-when-cross-origin",
        "referrer": "https://www.bing.com/images/create/",
        "origin": "https://www.bing.com",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54",
        "sec-ch-ua": '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
    }
    if cookies:
        headers["Cookie"] = '; '.join(f'{k}={v}' for k, v in cookies.items())
    return ClientSession(headers=headers, connector=get_connector(connector, proxy))


async def create_images(session: ClientSession, prompt: str, timeout: int = TIMEOUT_IMAGE_CREATION) -> List[str]:
    """
    Создает изображения на основе заданного запроса, используя сервис Bing.

    Args:
        session (ClientSession): Активный клиентский сеанс.
        prompt (str): Запрос для генерации изображений.
        timeout (int, optional): Время ожидания для запроса. По умолчанию TIMEOUT_IMAGE_CREATION.

    Returns:
        List[str]: Список URL-адресов созданных изображений.

    Raises:
        MissingRequirementsError: Если отсутствует пакет "beautifulsoup4".
        RateLimitError: Если закончились монеты для создания изображений.
        RuntimeError: Если создание изображений не удалось или истекло время ожидания.
    """
    if not has_requirements:
        raise MissingRequirementsError('Install "beautifulsoup4" package')
    url_encoded_prompt: str = quote(prompt)
    payload: str = f'q={url_encoded_prompt}&rt=4&FORM=GENCRE'
    url: str = f'{BING_URL}/images/create?q={url_encoded_prompt}&rt=4&FORM=GENCRE'
    try:
        async with session.post(url, allow_redirects=False, data=payload, timeout=timeout) as response:
            response.raise_for_status()
            text: str = (await response.text()).lower()
            if '0 coins available' in text:
                raise RateLimitError('No coins left. Log in with a different account or wait a while')
            for error in ERRORS:
                if error in text:
                    raise RuntimeError(f'Create images failed: {error}')
        if response.status != 302:
            url: str = f'{BING_URL}/images/create?q={url_encoded_prompt}&rt=3&FORM=GENCRE'
            async with session.post(url, allow_redirects=False, timeout=timeout) as response:
                if response.status != 302:
                    raise RuntimeError(f'Create images failed. Code: {response.status}')

        redirect_url: str = response.headers['Location'].replace('&nfy=1', '')
        redirect_url: str = f'{BING_URL}{redirect_url}'
        request_id: str = redirect_url.split('id=')[-1]
        async with session.get(redirect_url) as response:
            response.raise_for_status()

        polling_url: str = f'{BING_URL}/images/create/async/results/{request_id}?q={url_encoded_prompt}'
        start_time: float = time.time()
        while True:
            if time.time() - start_time > timeout:
                raise RuntimeError(f'Timeout error after {timeout} sec')
            async with session.get(polling_url) as response:
                if response.status != 200:
                    raise RuntimeError(f'Polling images faild. Code: {response.status}')
                text: str = await response.text()
                if not text or 'GenerativeImagesStatusPage' in text:
                    await asyncio.sleep(1)
                else:
                    break
        error: Optional[str] = None
        try:
            error = json.loads(text).get('errorMessage')
        except json.JSONDecodeError as ex:
            logger.error('Error decoding JSON', ex, exc_info=True)  # Log JSON decode error
        if error == 'Pending':
            raise RuntimeError('Prompt is been blocked')
        elif error:
            raise RuntimeError(error)
        return read_images(text)
    except MissingRequirementsError as ex:
        logger.error('Missing requirements', ex, exc_info=True)
        raise
    except RateLimitError as ex:
        logger.error('Rate limit error', ex, exc_info=True)
        raise
    except RuntimeError as ex:
        logger.error('Runtime error during image creation', ex, exc_info=True)
        raise
    except Exception as ex:
        logger.error('Unexpected error during image creation', ex, exc_info=True)
        raise


def read_images(html_content: str) -> List[str]:
    """
    Извлекает URL-адреса изображений из HTML-контента.

    Args:
        html_content (str): HTML-контент, содержащий URL-адреса изображений.

    Returns:
        List[str]: Список URL-адресов изображений.

    Raises:
        RuntimeError: Если не удалось найти изображения или обнаружены недопустимые изображения.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    tags = soup.find_all('img', class_='mimg')
    if not tags:
        tags = soup.find_all('img', class_='gir_mmimg')
    images: List[str] = [img['src'].split('?w=')[0] for img in tags]
    if any(im in BAD_IMAGES for im in images):
        raise RuntimeError('Bad images found')
    if not images:
        raise RuntimeError('No images found')
    return images