### **Анализ кода модуля `ARTA.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код асинхронный, что позволяет эффективно обрабатывать запросы.
    - Используется `ClientSession` для управления HTTP-соединениями.
    - Реализована логика обновления токена аутентификации.
    - Добавлены алиасы моделей изображений.
- **Минусы**:
    - Отсутствуют docstring для большинства методов и классов.
    - Не используется `logger` для логирования ошибок и информации.
    - Жестко заданные URL и ключ API.
    - Смешанный стиль кавычек (используются как одинарные, так и двойные).
    - Отсутствуют аннотации типов для параметров методов и возвращаемых значений.

#### **Рекомендации по улучшению**:
- Добавить docstring для всех классов и методов, описывающие их назначение, аргументы, возвращаемые значения и возможные исключения.
- Использовать `logger` для логирования важных событий, ошибок и отладочной информации.
- Вынести URL и ключ API в переменные окружения или конфигурационный файл.
- Привести все строки к одному стилю кавычек (одинарные).
- Добавить аннотации типов для всех переменных и параметров функций.
- Изменить обработку ошибок, чтобы использовать `logger.error` для регистрации ошибок с информацией об исключении.
- Использовать `j_loads` для загрузки JSON из файлов.

#### **Оптимизированный код**:
```python
from __future__ import annotations

import os
import time
import json
import random
from pathlib import Path
from aiohttp import ClientSession
import asyncio
from typing import AsyncGenerator, Optional, Dict, List

from src.logger import logger # Импорт модуля логирования
from ..typing import AsyncResult, Messages
from ..providers.response import ImageResponse, Reasoning
from ..errors import ResponseError
from ..cookies import get_cookies_dir
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin
from .helper import format_image_prompt

class ARTA(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Провайдер для генерации изображений через API ARTA.
    """
    url = "https://ai-arta.com"
    auth_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=AIzaSyB3-71wG0fIt0shj0ee4fvx1shcjJHGrrQ" # Жестко заданный ключ API
    token_refresh_url = "https://securetoken.googleapis.com/v1/token?key=AIzaSyB3-71wG0fIt0shj0ee4fvx1shcjJHGrrQ" # Жестко заданный ключ API
    image_generation_url = "https://img-gen-prod.ai-arta.com/api/v1/text2image"
    status_check_url = "https://img-gen-prod.ai-arta.com/api/v1/text2image/{record_id}/status"

    working = True

    default_model = "Flux"
    default_image_model = default_model
    model_aliases = {
        "flux": "Flux",
        "medieval": "Medieval",
        "vincent_van_gogh": "Vincent Van Gogh",
        "f_dev": "F Dev",
        "low_poly": "Low Poly",
        "dreamshaper_xl": "Dreamshaper-xl",
        "anima_pencil_xl": "Anima-pencil-xl",
        "biomech": "Biomech",
        "trash_polka": "Trash Polka",
        "no_style": "No Style",
        "cheyenne_xl": "Cheyenne-xl",
        "chicano": "Chicano",
        "embroidery_tattoo": "Embroidery tattoo",
        "red_and_black": "Red and Black",
        "fantasy_art": "Fantasy Art",
        "watercolor": "Watercolor",
        "dotwork": "Dotwork",
        "old_school_colored": "Old school colored",
        "realistic_tattoo": "Realistic tattoo",
        "japanese_2": "Japanese_2",
        "realistic_stock_xl": "Realistic-stock-xl",
        "f_pro": "F Pro",
        "revanimated": "RevAnimated",
        "katayama_mix_xl": "Katayama-mix-xl",
        "sdxl_l": "SDXL L",
        "cor_epica_xl": "Cor-epica-xl",
        "anime_tattoo": "Anime tattoo",
        "new_school": "New School",
        "death_metal": "Death metal",
        "old_school": "Old School",
        "juggernaut_xl": "Juggernaut-xl",
        "photographic": "Photographic",
        "sdxl_1_0": "SDXL 1.0",
        "graffiti": "Graffiti",
        "mini_tattoo": "Mini tattoo",
        "surrealism": "Surrealism",
        "neo_traditional": "Neo-traditional",
        "on_limbs_black": "On limbs black",
        "yamers_realistic_xl": "Yamers-realistic-xl",
        "pony_xl": "Pony-xl",
        "playground_xl": "Playground-xl",
        "anything_xl": "Anything-xl",
        "flame_design": "Flame design",
        "kawaii": "Kawaii",
        "cinematic_art": "Cinematic Art",
        "professional": "Professional",
        "black_ink": "Black Ink"
    }
    image_models = list(model_aliases.keys())
    models = image_models

    @classmethod
    def get_auth_file(cls) -> Path:
        """
        Возвращает путь к файлу аутентификации.

        Returns:
            Path: Путь к файлу аутентификации.
        """
        path = Path(get_cookies_dir())
        path.mkdir(exist_ok=True)
        filename = f'auth_{cls.__name__}.json'
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
            auth_payload = {'clientType': 'CLIENT_TYPE_ANDROID'}
            try:
                async with session.post(cls.auth_url, json=auth_payload, proxy=proxy) as auth_response:
                    auth_data = await auth_response.json()
                    auth_token = auth_data.get('idToken')
                    #refresh_token = auth_data.get("refreshToken")
                    if not auth_token:
                        raise ResponseError('Failed to obtain authentication token.')
                    with path.open('w') as f:
                        json.dump(auth_data, f) # Запись данных аутентификации в файл
                    return auth_data
            except Exception as ex:
                logger.error('Error while creating token', ex, exc_info=True) # Логирование ошибки
                raise

    @classmethod
    async def refresh_token(cls, refresh_token: str, proxy: Optional[str] = None) -> tuple[str, str]:
        """
        Обновляет токен аутентификации.

        Args:
            refresh_token (str): Токен обновления.
            proxy (Optional[str], optional): Прокси-сервер. По умолчанию None.

        Returns:
            tuple[str, str]: Новый токен и токен обновления.
        """
        async with ClientSession() as session:
            payload = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
            }
            try:
                async with session.post(cls.token_refresh_url, data=payload, proxy=proxy) as response:
                    response_data = await response.json()
                    return response_data.get('id_token'), response_data.get('refresh_token')
            except Exception as ex:
                logger.error('Error while refreshing token', ex, exc_info=True) # Логирование ошибки
                raise

    @classmethod
    async def read_and_refresh_token(cls, proxy: Optional[str] = None) -> Dict:
        """
        Читает и обновляет токен аутентификации из файла.

        Args:
            proxy (Optional[str], optional): Прокси-сервер. По умолчанию None.

        Returns:
            Dict: Данные аутентификации.
        """
        path = cls.get_auth_file()
        if path.is_file():
            try:
                with path.open('rb') as f:
                    auth_data = json.load(f) # Чтение данных аутентификации из файла
                diff = time.time() - os.path.getmtime(path)
                expiresIn = int(auth_data.get('expiresIn'))
                if diff < expiresIn:
                    if diff > expiresIn / 2:
                        auth_data['idToken'], auth_data['refreshToken'] = await cls.refresh_token(auth_data.get('refreshToken'), proxy)
                        with path.open('w') as f:
                            json.dump(auth_data, f) # Запись обновленных данных аутентификации в файл
                    return auth_data
            except Exception as ex:
                logger.error('Error while reading and refreshing token', ex, exc_info=True) # Логирование ошибки
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
    ) -> AsyncGenerator[AsyncResult, None]:
        """
        Создает асинхронный генератор изображений.

        Args:
            model (str): Модель для генерации изображений.
            messages (Messages): Сообщения для генерации изображения.
            proxy (Optional[str], optional): Прокси-сервер. По умолчанию None.
            prompt (Optional[str], optional): Промт для генерации изображения. По умолчанию None.
            negative_prompt (str): Негативный промт.
            n (int): Количество изображений.
            guidance_scale (int): Масштаб соответствия.
            num_inference_steps (int): Количество шагов вывода.
            aspect_ratio (str): Соотношение сторон.
            seed (Optional[int], optional): Зерно для генерации. По умолчанию None.

        Yields:
            AsyncResult: Результат генерации изображения.

        Raises:
            ResponseError: Если не удалось инициировать генерацию изображения или произошла ошибка при генерации.
        """
        model = cls.get_model(model)
        prompt = format_image_prompt(messages, prompt)

        # Generate a random seed if not provided
        if seed is None:
            seed = random.randint(9999, 99999999)  # Common range for random seeds

        # Step 1: Get Authentication Token
        auth_data = await cls.read_and_refresh_token(proxy)

        async with ClientSession() as session:
            # Step 2: Generate Images
            image_payload = {
                'prompt': prompt,
                'negative_prompt': negative_prompt,
                'style': model,
                'images_num': str(n),
                'cfg_scale': str(guidance_scale),
                'steps': str(num_inference_steps),
                'aspect_ratio': aspect_ratio,
                'seed': str(seed),
            }

            headers = {
                'Authorization': auth_data.get('idToken'),
            }

            try:
                async with session.post(cls.image_generation_url, data=image_payload, headers=headers, proxy=proxy) as image_response:
                    image_data = await image_response.json()
                    record_id = image_data.get('record_id')

                    if not record_id:
                        raise ResponseError(f'Failed to initiate image generation: {image_data}')

                # Step 3: Check Generation Status
                status_url = cls.status_check_url.format(record_id=record_id)
                counter = 4
                start_time = time.time()
                last_status = None
                while True:
                    async with session.get(status_url, headers=headers, proxy=proxy) as status_response:
                        status_data = await status_response.json()
                        status = status_data.get('status')

                        if status == 'DONE':
                            image_urls = [image['url'] for image in status_data.get('response', [])]
                            duration = time.time() - start_time
                            yield Reasoning(label='Generated', status=f'{n} image(s) in {duration:.2f}s')
                            yield ImageResponse(images=image_urls, alt=prompt)
                            return
                        elif status in ('IN_QUEUE', 'IN_PROGRESS'):
                            if last_status != status:
                                last_status = status
                                if status == 'IN_QUEUE':
                                    yield Reasoning(label='Waiting')
                                else:
                                    yield Reasoning(label='Generating')
                            await asyncio.sleep(2)  # Poll every 2 seconds
                        else:
                            raise ResponseError(f'Image generation failed with status: {status}')
            except Exception as ex:
                logger.error('Error while generating image', ex, exc_info=True) # Логирование ошибки
                raise