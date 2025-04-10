### **Анализ кода модуля `Reka.py`**

---

#### **Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
  - Код достаточно структурирован и логически разделен на функции.
  - Используются аннотации типов.
  - Присутствуют базовые проверки на наличие `api_key` и `cookies`.
- **Минусы**:
  - Отсутствует docstring для класса и методов.
  - Не используются логи.
  - Не все переменные аннотированы типами.
  - Не обрабатываются все возможные исключения.
  - Код содержит много повторений, например, в заголовках запросов.
  - Используются двойные кавычки вместо одинарных.
  - Не используется `j_loads` для обработки JSON.

#### **Рекомендации по улучшению:**

1.  **Документирование кода**:
    - Добавьте docstring для класса `Reka` и каждого из его методов, включая описание параметров, возвращаемых значений и возможных исключений.
    - Опишите назначение каждого метода и его вклад в общий процесс.

2.  **Логирование**:
    - Добавьте логирование для отслеживания хода выполнения программы и выявления ошибок. Используйте `logger.info` для информационных сообщений и `logger.error` для ошибок.

3.  **Обработка исключений**:
    - Улучшите обработку исключений, чтобы предоставлять более информативные сообщения об ошибках.
    - Используйте `logger.error` для записи информации об ошибках.

4.  **Улучшение структуры кода**:
    - Избегайте повторений кода, особенно в части заголовков запросов. Можно создать функцию для формирования заголовков.
    - Повысьте читаемость кода, разделяя логические блоки кода пустыми строками.

5.  **Использование одинарных кавычек**:
    - Замените двойные кавычки на одинарные в Python-коде.

6.  **Использование `j_loads`**:
    - Используйте `j_loads` для обработки JSON-ответов.

7.  **Аннотации типов**:
    - Добавьте аннотации типов для всех переменных, где это необходимо.

#### **Оптимизированный код:**

```python
"""
Модуль для работы с провайдером Reka
======================================

Модуль содержит класс :class:`Reka`, который используется для взаимодействия с Reka AI.
Он включает в себя методы для создания завершений, загрузки изображений и получения токена доступа.

Пример использования
----------------------

>>> reka = Reka()
>>> reka.create_completion(model='reka-core', messages=[{'role': 'user', 'content': 'Hello'}], stream=False)
"""
from __future__ import annotations

import os
import time
import json
from typing import Generator, Optional, List, Dict
from pathlib import Path

import requests

from ...typing import CreateResult, Messages, ImageType
from ..base_provider import AbstractProvider
from ...cookies import get_cookies
from ...image import to_bytes
from src.logger import logger  # Подключаем модуль логирования


class Reka(AbstractProvider):
    """
    Провайдер для взаимодействия с Reka AI.
    """
    domain: str = 'space.reka.ai'
    url: str = f'https://{domain}'
    working: bool = True
    needs_auth: bool = True
    supports_stream: bool = True
    default_vision_model: str = 'reka'
    cookies: dict = {}

    @classmethod
    def create_completion(
        cls,
        model: str,
        messages: Messages,
        stream: bool,
        proxy: Optional[str] = None,
        api_key: Optional[str] = None,
        image: Optional[ImageType] = None,
        **kwargs
    ) -> CreateResult:
        """
        Создает запрос на завершение текста к Reka AI.

        Args:
            model (str): Имя модели для использования.
            messages (Messages): Список сообщений для отправки.
            stream (bool): Флаг, указывающий, использовать ли потоковую передачу.
            proxy (Optional[str]): Прокси-сервер для использования. По умолчанию `None`.
            api_key (Optional[str]): API ключ для аутентификации. По умолчанию `None`.
            image (Optional[ImageType]): Изображение для отправки. По умолчанию `None`.

        Returns:
            CreateResult: Результат запроса.

        Raises:
            ValueError: Если не найдены cookies или `appSession` в cookies.
            Exception: Если произошла ошибка при создании запроса.

        Example:
            >>> Reka.create_completion(model='reka-core', messages=[{'role': 'user', 'content': 'Hello'}], stream=False)
        """
        cls.proxy = proxy

        if not api_key:
            cls.cookies = get_cookies(cls.domain)
            if not cls.cookies:
                msg = f'No cookies found for {cls.domain}'
                logger.error(msg)
                raise ValueError(msg)
            elif 'appSession' not in cls.cookies:
                msg = f'No appSession found in cookies for {cls.domain}, log in or provide bearer_auth'
                logger.error(msg)
                raise ValueError(msg)
            api_key = cls.get_access_token(cls)

        conversation: List[Dict[str, str]] = []
        for message in messages:
            conversation.append({
                'type': 'human',
                'text': message['content'],
            })

        if image:
            image_url = cls.upload_image(cls, api_key, image)
            conversation[-1]['image_url'] = image_url
            conversation[-1]['media_type'] = 'image'

        headers: Dict[str, str] = cls._build_headers(cls, api_key)

        json_data: Dict[str, any] = {
            'conversation_history': conversation,
            'stream': True,
            'use_search_engine': False,
            'use_code_interpreter': False,
            'model_name': 'reka-core',
            'random_seed': int(time.time() * 1000),
        }

        tokens: str = ''

        try:
            response = requests.post(f'{cls.url}/api/chat',
                                    cookies=cls.cookies, headers=headers, json=json_data, proxies=cls.proxy, stream=True)

            for completion in response.iter_lines():
                if b'data' in completion:
                    token_data: str = json.loads(completion.decode('utf-8')[5:])['text']

                    yield (token_data.replace(tokens, ''))

                    tokens = token_data
        except Exception as ex:
            logger.error('Error while creating completion', ex, exc_info=True)
            raise

    def upload_image(cls, access_token: str, image: ImageType) -> str:
        """
        Загружает изображение на сервер Reka AI.

        Args:
            access_token (str): Токен доступа для аутентификации.
            image (ImageType): Изображение для загрузки.

        Returns:
            str: URL загруженного изображения.

        Raises:
            Exception: Если произошла ошибка при загрузке изображения.

        Example:
            >>> Reka.upload_image('access_token', 'image_data')
            'https://example.com/image.png'
        """
        boundary_token: str = os.urandom(8).hex()

        headers: Dict[str, str] = cls._build_headers(cls, access_token, content_type=f'multipart/form-data; boundary=----WebKitFormBoundary{boundary_token}',referer=f'{cls.url}/chat/hPReZExtDOPvUfF8vCPC')

        image_data = to_bytes(image)

        boundary: str = f'----WebKitFormBoundary{boundary_token}'
        data: str = f'--{boundary}\\r\\nContent-Disposition: form-data; name="image"; filename="image.png"\\r\\nContent-Type: image/png\\r\\n\\r\\n'
        data += image_data.decode('latin-1')
        data += f'\\r\\n--{boundary}--\\r\\n'
        try:
            response = requests.post(f'{cls.url}/api/upload-image',
                                        cookies=cls.cookies, headers=headers, proxies=cls.proxy, data=data.encode('latin-1'))

            return response.json()['media_url']
        except Exception as ex:
            logger.error('Error while uploading image', ex, exc_info=True)
            raise

    def get_access_token(cls) -> str:
        """
        Получает токен доступа для Reka AI.

        Returns:
            str: Токен доступа.

        Raises:
            ValueError: Если не удалось получить токен доступа.

        Example:
            >>> Reka.get_access_token()
            'access_token'
        """
        headers: Dict[str, str] = cls._build_headers(cls,referer=f'{cls.url}/chat')

        try:
            response = requests.get(f'{cls.url}/bff/auth/access_token',
                                    cookies=cls.cookies, headers=headers, proxies=cls.proxy)

            return response.json()['accessToken']

        except Exception as ex:
            msg = f'Failed to get access token: {ex}, refresh your cookies / log in into {cls.domain}'
            logger.error(msg, ex, exc_info=True)
            raise ValueError(msg)

    def _build_headers(cls, access_token: str = None, content_type: str = 'application/json', referer: str = None) -> Dict[str, str]:
        """
        Создает и возвращает словарь с заголовками запроса.

        Args:
            access_token (str, optional): Токен доступа. Defaults to None.
            content_type (str, optional): Тип контента. Defaults to 'application/json'.
            referer (str, optional): Referer. Defaults to None.

        Returns:
            Dict[str, str]: Словарь с заголовками запроса.
        """
        headers = {
            'accept': '*/*',
            'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }
        if access_token:
            headers['authorization'] = f'Bearer {access_token}'
        if content_type:
            headers['content-type'] = content_type
        if referer:
            headers['referer'] = referer
        return headers