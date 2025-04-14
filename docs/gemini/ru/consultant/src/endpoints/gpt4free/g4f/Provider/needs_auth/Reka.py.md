### **Анализ кода модуля `Reka.py`**

---

#### **Качество кода**:

- **Соответствие стандартам**: 6/10
- **Плюсы**:
  - Код достаточно хорошо структурирован и использует классы для организации функциональности.
  - Присутствуют проверки на наличие кукис и `appSession`.
  - Используется `requests` для выполнения HTTP-запросов, что является стандартной практикой.
- **Минусы**:
  - Отсутствуют docstring для методов, что затрудняет понимание их назначения и использования.
  - Много повторяющегося кода, особенно в заголовках HTTP-запросов.
  - Не используются аннотации типов для параметров и возвращаемых значений.
  - Обработка исключений не логирует ошибки с использованием `logger`.
  - Не используется `j_loads` для обработки JSON-ответов.
  - Не все переменные аннотированы типами.

#### **Рекомендации по улучшению**:

1.  **Добавить docstring для всех методов**:
    - Описать назначение каждого метода, параметры и возвращаемые значения.

2.  **Улучшить обработку ошибок**:
    - Использовать `logger.error` для логирования ошибок с `exc_info=True`.

3.  **Устранить дублирование кода**:
    - Вынести повторяющиеся заголовки в отдельную функцию или переменную.

4.  **Использовать аннотации типов**:
    - Добавить аннотации типов для всех параметров и возвращаемых значений функций.

5.  **Использовать `j_loads` для JSON**:
    - Заменить `json.loads` на `j_loads` для чтения JSON-ответов.

6. **Улучшить форматирование строк**:
   - Использовать f-строки для более читаемого форматирования.

#### **Оптимизированный код**:

```python
from __future__ import annotations

import os
import time
from typing import Generator, Optional, List, Dict, Union
import requests
from src.typing import CreateResult, Messages, ImageType
from src.endpoints.gpt4free.g4f.Provider.base_provider import AbstractProvider
from src.endpoints.gpt4free.g4f.cookies import get_cookies
from src.endpoints.gpt4free.g4f.image import to_bytes
from src.logger import logger  # Import logger
from pathlib import Path
from src.utils.json_utils import j_loads


"""
Модуль для работы с провайдером Reka
======================================

Модуль содержит класс :class:`Reka`, который используется для взаимодействия с AI-моделью Reka.
"""


class Reka(AbstractProvider):
    """
    Провайдер для взаимодействия с AI-моделью Reka.
    """

    domain = 'space.reka.ai'
    url = f'https://{domain}'
    working = True
    needs_auth = True
    supports_stream = True
    default_vision_model = 'reka'
    cookies: Dict = {}

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
        Создает запрос к Reka для получения completion.

        Args:
            model (str): Модель для использования.
            messages (Messages): Список сообщений для отправки.
            stream (bool): Использовать ли стриминг.
            proxy (Optional[str], optional): Прокси для использования. По умолчанию None.
            api_key (Optional[str], optional): API ключ. По умолчанию None.
            image (Optional[ImageType], optional): Изображение для отправки. По умолчанию None.

        Returns:
            CreateResult: Результат запроса.

        Raises:
            ValueError: Если не найдены кукис или appSession.
            Exception: При возникновении других ошибок.
        """
        cls.proxy = proxy

        if not api_key:
            cls.cookies = get_cookies(cls.domain)
            if not cls.cookies:
                raise ValueError(f'No cookies found for {cls.domain}')
            elif 'appSession' not in cls.cookies:
                raise ValueError(f'No appSession found in cookies for {cls.domain}, log in or provide bearer_auth')
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

        headers: Dict[str, str] = {
            'accept': '*/*',
            'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
            'authorization': f'Bearer {api_key}',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': cls.url,
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

        json_data: Dict[str, Union[List[Dict[str, str]], bool, str, int]] = {
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
                    token_data: str = j_loads(completion.decode('utf-8')[5:])['text']

                    yield (token_data.replace(tokens, ''))

                    tokens = token_data

        except Exception as ex:
            logger.error('Error while processing data', ex, exc_info=True)
            raise

    @classmethod
    def upload_image(cls, access_token: str, image: ImageType) -> str:
        """
        Загружает изображение на сервер Reka.

        Args:
            access_token (str): Токен доступа.
            image (ImageType): Изображение для загрузки.

        Returns:
            str: URL изображения.
        """
        boundary_token: str = os.urandom(8).hex()

        headers: Dict[str, str] = {
            'accept': '*/*',
            'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
            'cache-control': 'no-cache',
            'authorization': f'Bearer {access_token}',
            'content-type': f'multipart/form-data; boundary=----WebKitFormBoundary{boundary_token}',
            'origin': cls.url,
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': f'{cls.url}/chat/hPReZExtDOPvUfF8vCPC',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        image_data: bytes = to_bytes(image)

        boundary: str = f'----WebKitFormBoundary{boundary_token}'
        data: str = f'--{boundary}\r\nContent-Disposition: form-data; name="image"; filename="image.png"\r\nContent-Type: image/png\r\n\r\n'
        data += image_data.decode('latin-1')
        data += f'\r\n--{boundary}--\r\n'

        try:
            response = requests.post(f'{cls.url}/api/upload-image',
                                        cookies=cls.cookies, headers=headers, proxies=cls.proxy, data=data.encode('latin-1'))

            return j_loads(response.text)['media_url']

        except Exception as ex:
            logger.error('Error while uploading image', ex, exc_info=True)
            raise

    @classmethod
    def get_access_token(cls) -> str:
        """
        Получает access token для Reka.

        Returns:
            str: Access token.

        Raises:
            ValueError: Если не удалось получить access token.
        """
        headers: Dict[str, str] = {
            'accept': '*/*',
            'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': f'{cls.url}/chat',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        try:
            response = requests.get(f'{cls.url}/bff/auth/access_token',
                                        cookies=cls.cookies, headers=headers, proxies=cls.proxy)

            return j_loads(response.text)['accessToken']

        except Exception as ex:
            logger.error('Failed to get access token', ex, exc_info=True)
            raise ValueError(f'Failed to get access token: {ex}, refresh your cookies / log in into {cls.domain}')