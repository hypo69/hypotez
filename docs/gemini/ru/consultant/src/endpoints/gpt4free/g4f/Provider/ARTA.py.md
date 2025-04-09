### **Анализ кода модуля `ARTA.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Асинхронная обработка запросов.
  - Использование `ClientSession` для HTTP-запросов.
  - Реализация обновления токена аутентификации.
  - Обработка ошибок и логирование.
- **Минусы**:
  - Отсутствует документация модуля.
  - Жестко заданные URL и ключи.
  - Не все функции и методы документированы.
  - Не используется модуль `logger` для логирования.
  - Не все переменные аннотированы типами

#### **Рекомендации по улучшению**:
- Добавить документацию модуля с описанием назначения и примерами использования.
- Добавить docstring для всех функций и методов.
- Использовать модуль `logger` для логирования ошибок и отладочной информации.
- Вынести URL и ключи в переменные окружения или конфигурационный файл.
- Добавить обработку различных типов ошибок и логирование.
- Улучшить читаемость кода, добавив пробелы и переименовав переменные.
- Использовать более информативные сообщения об ошибках.
- Все переменные должны быть аннотированы типами.

#### **Оптимизированный код**:

```python
"""
Модуль для работы с провайдером ARTA
=====================================

Модуль содержит класс :class:`ARTA`, который используется для взаимодействия с API AI-ARTA
для генерации изображений.

Пример использования
----------------------

>>> provider = ARTA()
>>> async for item in provider.create_async_generator(model='Flux', messages=[{'role': 'user', 'content': 'запрос'}]):
...     print(item)
"""
from __future__ import annotations

import os
import time
import json
import random
from pathlib import Path
from aiohttp import ClientSession
import asyncio
from typing import AsyncGenerator, Optional, List, Dict, Tuple

from ..typing import AsyncResult, Messages
from ..providers.response import ImageResponse, Reasoning
from ..errors import ResponseError
from ..cookies import get_cookies_dir
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin
from .helper import format_image_prompt
from src.logger import logger  # Добавлен импорт logger


class ARTA(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Провайдер для взаимодействия с API AI-ARTA для генерации изображений.
    """
    url: str = 'https://ai-arta.com'
    auth_url: str = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=AIzaSyB3-71wG0fIt0shj0ee4fvx1shcjJHGrrQ'
    token_refresh_url: str = 'https://securetoken.googleapis.com/v1/token?key=AIzaSyB3-71wG0fIt0shj0ee4fvx1shcjJHGrrQ'
    image_generation_url: str = 'https://img-gen-prod.ai-arta.com/api/v1/text2image'
    status_check_url: str = 'https://img-gen-prod.ai-arta.com/api/v1/text2image/{record_id}/status'

    working: bool = True

    default_model: str = 'Flux'
    default_image_model: str = default_model
    model_aliases: Dict[str, str] = {
        'flux': 'Flux',
        'medieval': 'Medieval',
        'vincent_van_gogh': 'Vincent Van Gogh',
        'f_dev': 'F Dev',
        'low_poly': 'Low Poly',
        'dreamshaper_xl': 'Dreamshaper-xl',
        'anima_pencil_xl': 'Anima-pencil-xl',
        'biomech': 'Biomech',
        'trash_polka': 'Trash Polka',
        'no_style': 'No Style',
        'cheyenne_xl': 'Cheyenne-xl',
        'chicano': 'Chicano',
        'embroidery_tattoo': 'Embroidery tattoo',
        'red_and_black': 'Red and Black',
        'fantasy_art': 'Fantasy Art',
        'watercolor': 'Watercolor',
        'dotwork': 'Dotwork',
        'old_school_colored': 'Old school colored',
        'realistic_tattoo': 'Realistic tattoo',
        'japanese_2': 'Japanese_2',
        'realistic_stock_xl': 'Realistic-stock-xl',
        'f_pro': 'F Pro',
        'revanimated': 'RevAnimated',
        'katayama_mix_xl': 'Katayama-mix-xl',
        'sdxl_l': 'SDXL L',
        'cor_epica_xl': 'Cor-epica-xl',
        'anime_tattoo': 'Anime tattoo',
        'new_school': 'New School',
        'death_metal': 'Death metal',
        'old_school': 'Old School',
        'juggernaut_xl': 'Juggernaut-xl',
        'photographic': 'Photographic',
        'sdxl_1_0': 'SDXL 1.0',
        'graffiti': 'Graffiti',
        'mini_tattoo': 'Mini tattoo',
        'surrealism': 'Surrealism',
        'neo_traditional': 'Neo-traditional',
        'on_limbs_black': 'On limbs black',
        'yamers_realistic_xl': 'Yamers-realistic-xl',
        'pony_xl': 'Pony-xl',
        'playground_xl': 'Playground-xl',
        'anything_xl': 'Anything-xl',
        'flame_design': 'Flame design',
        'kawaii': 'Kawaii',
        'cinematic_art': 'Cinematic Art',
        'professional': 'Professional',
        'black_ink': 'Black Ink'
    }
    image_models: List[str] = list(model_aliases.keys())
    models: List[str] = image_models

    @classmethod
    def get_auth_file(cls) -> Path:
        """
        Получает путь к файлу аутентификации.

        Returns:
            Path: Путь к файлу аутентификации.
        """
        path: Path = Path(get_cookies_dir())
        path.mkdir(exist_ok=True)
        filename: str = f'auth_{cls.__name__}.json'
        return path / filename

    @classmethod
    async def create_token(cls, path: Path, proxy: Optional[str] = None) -> Dict:
        """
        Создает токен аутентификации.

        Args:
            path (Path): Путь для сохранения данных аутентификации.
            proxy (Optional[str], optional): Прокси-сервер. По умолчанию None.

        Returns:
            Dict: Данные аутентификации.

        Raises:
            ResponseError: Если не удалось получить токен аутентификации.
        """
        async with ClientSession() as session:
            # Step 1: Generate Authentication Token
            auth_payload: Dict[str, str] = {'clientType': 'CLIENT_TYPE_ANDROID'}
            try:
                async with session.post(cls.auth_url, json=auth_payload, proxy=proxy) as auth_response:
                    auth_data: Dict = await auth_response.json()
                    auth_token: Optional[str] = auth_data.get('idToken')
                    # refresh_token = auth_data.get("refreshToken")
                    if not auth_token:
                        raise ResponseError('Failed to obtain authentication token.')
                    json.dump(auth_data, path.open('w'))
                    return auth_data
            except Exception as ex:
                logger.error('Error while creating token', ex, exc_info=True)
                raise

    @classmethod
    async def refresh_token(cls, refresh_token: str, proxy: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
        """
        Обновляет токен аутентификации.

        Args:
            refresh_token (str): Refresh токен.
            proxy (Optional[str], optional): Прокси-сервер. По умолчанию None.

        Returns:
            Tuple[Optional[str], Optional[str]]: Новый id_token и refresh_token.
        """
        async with ClientSession() as session:
            payload: Dict[str, str] = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
            }
            try:
                async with session.post(cls.token_refresh_url, data=payload, proxy=proxy) as response:
                    response_data: Dict = await response.json()
                    return response_data.get('id_token'), response_data.get('refresh_token')
            except Exception as ex:
                logger.error('Error while refreshing token', ex, exc_info=True)
                return None, None

    @classmethod
    async def read_and_refresh_token(cls, proxy: Optional[str] = None) -> Dict:
        """
        Читает и обновляет токен аутентификации.

        Args:
            proxy (Optional[str], optional): Прокси-сервер. По умолчанию None.

        Returns:
            Dict: Данные аутентификации.
        """
        path: Path = cls.get_auth_file()
        if path.is_file():
            try:
                auth_data: Dict = json.load(path.open('rb'))
                diff: float = time.time() - os.path.getmtime(path)
                expiresIn: int = int(auth_data.get('expiresIn'))
                if diff < expiresIn:
                    if diff > expiresIn / 2:
                        auth_data['idToken'], auth_data['refreshToken'] = await cls.refresh_token(auth_data.get('refreshToken'), proxy)
                        json.dump(auth_data, path.open('w'))
                    return auth_data
            except Exception as ex:
                logger.error('Error while reading and refreshing token', ex, exc_info=True)
                return await cls.create_token(path, proxy)
        return await cls.create_token(path, proxy)

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: Optional[str] = None,
        prompt: Optional[str] = None,
        negative_prompt: str = 'blurry, deformed hands, ugly',
        n: int = 1,
        guidance_scale: int = 7,
        num_inference_steps: int = 30,
        aspect_ratio: str = '1:1',
        seed: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[ImageResponse | Reasoning, None]:
        """
        Создает асинхронный генератор изображений.

        Args:
            model (str): Модель для генерации изображений.
            messages (Messages): Список сообщений.
            proxy (Optional[str], optional): Прокси-сервер. По умолчанию None.
            prompt (Optional[str], optional): Текст запроса. По умолчанию None.
            negative_prompt (str): Негативный текст запроса.
            n (int): Количество изображений.
            guidance_scale (int): Guidance scale.
            num_inference_steps (int): Количество шагов инференса.
            aspect_ratio (str): Соотношение сторон изображения.
            seed (Optional[int], optional): Зерно для генерации случайных чисел. По умолчанию None.

        Yields:
            AsyncGenerator[ImageResponse | Reasoning, None]: Объект ImageResponse с сгенерированными изображениями или объект Reasoning со статусом.

        Raises:
            ResponseError: Если не удалось инициировать генерацию изображения или произошла ошибка в процессе генерации.
        """
        model: str = cls.get_model(model)
        prompt: str = format_image_prompt(messages, prompt)

        # Generate a random seed if not provided
        if seed is None:
            seed: int = random.randint(9999, 99999999)  # Common range for random seeds

        # Step 1: Get Authentication Token
        auth_data: Dict = await cls.read_and_refresh_token(proxy)

        async with ClientSession() as session:
            # Step 2: Generate Images
            image_payload: Dict[str, str] = {
                'prompt': prompt,
                'negative_prompt': negative_prompt,
                'style': model,
                'images_num': str(n),
                'cfg_scale': str(guidance_scale),
                'steps': str(num_inference_steps),
                'aspect_ratio': aspect_ratio,
                'seed': str(seed),
            }

            headers: Dict[str, str] = {
                'Authorization': auth_data.get('idToken'),
            }

            try:
                async with session.post(cls.image_generation_url, data=image_payload, headers=headers, proxy=proxy) as image_response:
                    image_data: Dict = await image_response.json()
                    record_id: Optional[str] = image_data.get('record_id')

                    if not record_id:
                        raise ResponseError(f'Failed to initiate image generation: {image_data}')

                # Step 3: Check Generation Status
                status_url: str = cls.status_check_url.format(record_id=record_id)
                counter: int = 4
                start_time: float = time.time()
                last_status: Optional[str] = None
                while True:
                    async with session.get(status_url, headers=headers, proxy=proxy) as status_response:
                        status_data: Dict = await status_response.json()
                        status: Optional[str] = status_data.get('status')

                        if status == 'DONE':
                            image_urls: List[str] = [image['url'] for image in status_data.get('response', [])]
                            duration: float = time.time() - start_time
                            yield Reasoning(label='Generated', status=f'{n} image(s) in {duration:.2f}s')
                            yield ImageResponse(images=image_urls, alt=prompt)
                            return
                        elif status in ('IN_QUEUE', 'IN_PROGRESS'):
                            if last_status != status:
                                last_status: str = status
                                if status == 'IN_QUEUE':
                                    yield Reasoning(label='Waiting')
                                else:
                                    yield Reasoning(label='Generating')
                            await asyncio.sleep(2)  # Poll every 2 seconds
                        else:
                            raise ResponseError(f'Image generation failed with status: {status}')
            except Exception as ex:
                logger.error('Error during image generation', ex, exc_info=True)
                raise