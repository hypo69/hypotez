### **Анализ кода модуля `create_images.py`**

#### **Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код структурирован и логически разделен на функции.
    - Используются асинхронные операции для неблокирующего выполнения.
    - Обработка ошибок присутствует, включая специфические исключения (`RateLimitError`, `MissingRequirementsError`).
- **Минусы**:
    - Отсутствует логирование.
    - Не все переменные аннотированы типами.
    - Жестко заданы URL и параметры запросов, что усложняет изменение конфигурации.
    - Docstring на английском языке.
    - Не используется модуль `logger` для логирования.
    - Нет обработки исключений при загрузке json.

#### **Рекомендации по улучшению:**

1.  **Добавить логирование**:
    - Использовать модуль `logger` для записи информации об операциях, ошибках и предупреждениях.
    - Логировать важные этапы выполнения функций, например, успешное создание сессии, отправку запроса, получение ответа, извлечение URL изображений.
    - Логировать ошибки с трассировкой (`exc_info=True`) для облегчения отладки.

2.  **Аннотировать типы переменных**:
    - Добавить аннотации типов для всех переменных, где это возможно, чтобы улучшить читаемость и предотвратить ошибки.
    - Включить аннотации для локальных переменных в функциях.

3.  **Вынести конфигурационные параметры**:
    - URL, заголовки и другие константы вынести в отдельный конфигурационный файл или переменные окружения, чтобы упростить изменение параметров без изменения кода.

4.  **Перевести Docstring на русский язык**:
    - Весь Docstring должен быть переведен на русский язык.

5. **Обработка JSON**:
    - Добавить обработку исключений при загрузке json. Использовать конструкцию `try...except`

6.  **Обработка исключений**:
   - Использовать `ex` вместо `e` в блоках обработки исключений.

#### **Оптимизированный код:**

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
from src.logger import logger  # Импортируем модуль логирования

BING_URL: str = "https://www.bing.com"
TIMEOUT_LOGIN: int = 1200
TIMEOUT_IMAGE_CREATION: int = 300
ERRORS: List[str] = [
    "this prompt is being reviewed",
    "this prompt has been blocked",
    "we\'re working hard to offer image creator in more languages",
    "we can\'t create your images right now"
]
BAD_IMAGES: List[str] = [
    "https://r.bing.com/rp/in-2zU3AJUdkgFe7ZKv19yPBHVs.png",
    "https://r.bing.com/rp/TX9QuO3WzcCJz1uaaSwQAz39Kb0.jpg",
]

def create_session(cookies: Dict[str, str], proxy: Optional[str] = None, connector: Optional[BaseConnector] = None) -> ClientSession:
    """
    Создает новую клиентскую сессию с указанными куки и заголовками.

    Args:
        cookies (Dict[str, str]): Куки, используемые для сессии.
        proxy (Optional[str], optional): Прокси-сервер для сессии. По умолчанию None.
        connector (Optional[BaseConnector], optional): Кастомный коннектор. По умолчанию None.

    Returns:
        ClientSession: Созданная клиентская сессия.
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
        "sec-ch-ua": "\"Microsoft Edge\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
    }
    if cookies:
        headers["Cookie"] = "; ".join(f"{k}={v}" for k, v in cookies.items())
    logger.info('Создание новой сессии') # Логирование создания сессии
    return ClientSession(headers=headers, connector=get_connector(connector, proxy))

async def create_images(session: ClientSession, prompt: str, timeout: int = TIMEOUT_IMAGE_CREATION) -> List[str]:
    """
    Создает изображения на основе заданного запроса, используя сервис Bing.

    Args:
        session (ClientSession): Активная клиентская сессия.
        prompt (str): Запрос для генерации изображений.
        timeout (int, optional): Время ожидания запроса в секундах. По умолчанию TIMEOUT_IMAGE_CREATION.

    Returns:
        List[str]: Список URL-адресов созданных изображений.

    Raises:
        MissingRequirementsError: Если отсутствует библиотека beautifulsoup4.
        RateLimitError: Если закончились доступные монеты.
        RuntimeError: Если создание изображений завершилось неудачей или истекло время ожидания.
    """
    if not has_requirements:
        logger.error('Отсутствует необходимый пакет beautifulsoup4') # Логирование ошибки
        raise MissingRequirementsError('Install "beautifulsoup4" package')
    url_encoded_prompt: str = quote(prompt)
    payload: str = f"q={url_encoded_prompt}&rt=4&FORM=GENCRE"
    url: str = f"{BING_URL}/images/create?q={url_encoded_prompt}&rt=4&FORM=GENCRE"
    try:
        async with session.post(url, allow_redirects=False, data=payload, timeout=timeout) as response:
            response.raise_for_status()
            text: str = (await response.text()).lower()
            if "0 coins available" in text:
                logger.error('Нет доступных монет. Требуется другой аккаунт или подождать.') # Логирование ошибки
                raise RateLimitError("No coins left. Log in with a different account or wait a while")
            for error in ERRORS:
                if error in text:
                    logger.error(f'Создание изображений не удалось: {error}') # Логирование ошибки
                    raise RuntimeError(f"Create images failed: {error}")
        if response.status != 302:
            url: str = f"{BING_URL}/images/create?q={url_encoded_prompt}&rt=3&FORM=GENCRE"
            async with session.post(url, allow_redirects=False, timeout=timeout) as response:
                if response.status != 302:
                    logger.error(f'Создание изображений не удалось. Код: {response.status}') # Логирование ошибки
                    raise RuntimeError(f"Create images failed. Code: {response.status}")

        redirect_url: str = response.headers["Location"].replace("&nfy=1", "")
        redirect_url: str = f"{BING_URL}{redirect_url}"
        request_id: str = redirect_url.split("id=")[-1]
        async with session.get(redirect_url) as response:
            response.raise_for_status()

        polling_url: str = f"{BING_URL}/images/create/async/results/{request_id}?q={url_encoded_prompt}"
        start_time: float = time.time()
        while True:
            if time.time() - start_time > timeout:
                logger.error(f'Превышено время ожидания {timeout} сек') # Логирование ошибки
                raise RuntimeError(f"Timeout error after {timeout} sec")
            async with session.get(polling_url) as response:
                if response.status != 200:
                    logger.error(f'Ошибка при опросе изображений. Код: {response.status}') # Логирование ошибки
                    raise RuntimeError(f"Polling images faild. Code: {response.status}")
                text: str = await response.text()
                if not text or "GenerativeImagesStatusPage" in text:
                    await asyncio.sleep(1)
                else:
                    break
        error: Optional[str] = None
        try:
            error = json.loads(text).get("errorMessage")
        except Exception as ex:
            logger.error('Ошибка при загрузке JSON', ex, exc_info = True) # Логирование ошибки парсинга JSON
            pass
        if error == "Pending":
            logger.error('Запрос заблокирован') # Логирование ошибки
            raise RuntimeError("Prompt is been blocked")
        elif error:
            logger.error(f'Ошибка: {error}') # Логирование ошибки
            raise RuntimeError(error)
        logger.info('Изображения успешно созданы') # Логирование успеха
        return read_images(text)
    except Exception as ex:
        logger.error('Произошла ошибка при создании изображений', ex, exc_info=True)
        raise

def read_images(html_content: str) -> List[str]:
    """
    Извлекает URL-адреса изображений из HTML-контента.

    Args:
        html_content (str): HTML-контент, содержащий URL-адреса изображений.

    Returns:
        List[str]: Список URL-адресов изображений.

    Raises:
        RuntimeError: Если не удалось найти изображения или обнаружены плохие изображения.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    tags = soup.find_all("img", class_="mimg")
    if not tags:
        tags = soup.find_all("img", class_="gir_mmimg")
    images: List[str] = [img["src"].split("?w=")[0] for img in tags]
    if any(im in BAD_IMAGES for im in images):
        logger.error('Обнаружены плохие изображения') # Логирование ошибки
        raise RuntimeError("Bad images found")
    if not images:
        logger.error('Изображения не найдены') # Логирование ошибки
        raise RuntimeError("No images found")
    logger.info('URL-адреса изображений успешно извлечены') # Логирование успеха
    return images