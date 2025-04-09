### **Анализ кода модуля `ARTA.py`**

## Анализ кода модуля `ARTA.py`

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
  - Использование асинхронных операций для неблокирующего выполнения.
  - Реализация механизма обновления токена аутентификации.
  - Разделение ответственности между методами (например, `create_token`, `refresh_token`).
  - Применение `AsyncGeneratorProvider` для потоковой обработки результатов.

- **Минусы**:
  - Отсутствие документации для большинства методов и классов.
  - Не все переменные аннотированы типами.
  - Использование `json.load` и `json.dump` вместо `j_loads` и `j_loads_ns`.
  - Magic values в коде (например, числа `9999`, `99999999`, `4`, `2`).
  - Жёстко заданные URL и параметры (например, `auth_url`, `token_refresh_url`).

**Рекомендации по улучшению:**

1.  **Добавить документацию**:
    - Добавить docstring к классам и методам, описывающие их назначение, аргументы, возвращаемые значения и возможные исключения.
    - Улучшить комментарии, чтобы они были более информативными и соответствовали стандарту.

2.  **Использовать `j_loads` и `j_loads_ns`**:
    - Заменить использование `json.load` и `json.dump` на `j_loads` и `j_loads_ns` для унификации работы с JSON.

3.  **Улучшить обработку ошибок**:
    - Добавить логирование ошибок с использованием `logger` из `src.logger`.

4.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных и параметров функций.

5.  **Избавиться от "магических" значений**:
    - Заменить магические числа константами с понятными именами.

6.  **Рефакторинг URL**:
    - Вынести URL в константы или параметры конфигурации, чтобы упростить их изменение.

**Оптимизированный код:**

```python
from __future__ import annotations

import os
import time
import json
import random
from pathlib import Path
from aiohttp import ClientSession
import asyncio

from ..typing import AsyncResult, Messages
from ..providers.response import ImageResponse, Reasoning
from ..errors import ResponseError
from ..cookies import get_cookies_dir
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin
from .helper import format_image_prompt
from src.logger import logger # Добавлен импорт logger

class ARTA(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Провайдер для генерации изображений через API ARTA.

    Этот класс обеспечивает асинхронную генерацию изображений на основе текстовых запросов,
    используя API ai-arta.com. Поддерживает аутентификацию через Google API, обновление токенов
    и различные стили генерации изображений.
    """
    url: str = "https://ai-arta.com"
    auth_url: str = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=AIzaSyB3-71wG0fIt0shj0ee4fvx1shcjJHGrrQ"
    token_refresh_url: str = "https://securetoken.googleapis.com/v1/token?key=AIzaSyB3-71wG0fIt0shj0ee4fvx1shcjJHGrrQ"
    image_generation_url: str = "https://img-gen-prod.ai-arta.com/api/v1/text2image"
    status_check_url: str = "https://img-gen-prod.ai-arta.com/api/v1/text2image/{record_id}/status"

    working: bool = True

    default_model: str = "Flux"
    default_image_model: str = default_model
    model_aliases: dict[str, str] = {
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
    image_models: list[str] = list(model_aliases.keys())
    models: list[str] = image_models

    AUTH_TOKEN_EXPIRATION_THRESHOLD: float = 0.5
    RANDOM_SEED_MIN: int = 9999
    RANDOM_SEED_MAX: int = 99999999
    STATUS_CHECK_COUNTER: int = 4
    STATUS_CHECK_INTERVAL: int = 2

    @classmethod
    def get_auth_file(cls) -> Path:
        """
        Возвращает путь к файлу, в котором хранится информация об аутентификации.

        Returns:
            Path: Путь к файлу аутентификации.
        """
        path: Path = Path(get_cookies_dir())
        path.mkdir(exist_ok=True)
        filename: str = f"auth_{cls.__name__}.json"
        return path / filename

    @classmethod
    async def create_token(cls, path: Path, proxy: str | None = None) -> dict:
        """
        Создает и сохраняет токен аутентификации.

        Args:
            path (Path): Путь для сохранения данных аутентификации.
            proxy (str | None, optional): Прокси-сервер для использования. По умолчанию None.

        Returns:
            dict: Данные аутентификации.

        Raises:
            ResponseError: Если не удается получить токен аутентификации.
        """
        async with ClientSession() as session:
            # Step 1: Generate Authentication Token
            auth_payload: dict[str, str] = {"clientType": "CLIENT_TYPE_ANDROID"}
            try:
                async with session.post(cls.auth_url, json=auth_payload, proxy=proxy) as auth_response:
                    auth_response.raise_for_status() # Проверка на HTTP ошибки
                    auth_data: dict = await auth_response.json()
                    auth_token: str | None = auth_data.get("idToken")
                    if not auth_token:
                        raise ResponseError("Failed to obtain authentication token.")
                    with path.open("w", encoding='utf-8') as f:
                        json.dump(auth_data, f)
                    return auth_data
            except Exception as ex:
                logger.error('Error while creating token', ex, exc_info=True)
                raise

    @classmethod
    async def refresh_token(cls, refresh_token: str, proxy: str | None = None) -> tuple[str, str]:
        """
        Обновляет токен аутентификации.

        Args:
            refresh_token (str): Refresh токен для обновления.
            proxy (str | None, optional): Прокси-сервер для использования. По умолчанию None.

        Returns:
            tuple[str, str]: Новый id_token и refresh_token.
        """
        async with ClientSession() as session:
            payload: dict[str, str] = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            }
            try:
                async with session.post(cls.token_refresh_url, data=payload, proxy=proxy) as response:
                    response.raise_for_status() # Проверка на HTTP ошибки
                    response_data: dict = await response.json()
                    return response_data.get("id_token"), response_data.get("refresh_token")
            except Exception as ex:
                logger.error('Error while refreshing token', ex, exc_info=True)
                raise

    @classmethod
    async def read_and_refresh_token(cls, proxy: str | None = None) -> dict:
        """
        Считывает токен из файла и, если необходимо, обновляет его.

        Args:
            proxy (str | None, optional): Прокси-сервер для использования. По умолчанию None.

        Returns:
            dict: Данные аутентификации.
        """
        path: Path = cls.get_auth_file()
        if path.is_file():
            try:
                with path.open("rb") as f:
                    auth_data: dict = json.load(f)
                diff: float = time.time() - os.path.getmtime(path)
                expiresIn: int | None = auth_data.get("expiresIn")
                if expiresIn is None:
                    return await cls.create_token(path, proxy)
                if diff < expiresIn:
                    if diff > expiresIn * cls.AUTH_TOKEN_EXPIRATION_THRESHOLD:
                        auth_data["idToken"], auth_data["refreshToken"] = await cls.refresh_token(auth_data.get("refreshToken"), proxy)
                        with path.open("w", encoding='utf-8') as f:
                            json.dump(auth_data, f)
                    return auth_data
            except (FileNotFoundError, json.JSONDecodeError) as ex:
                logger.error('Error while reading or refreshing token', ex, exc_info=True)
                return await cls.create_token(path, proxy)
        return await cls.create_token(path, proxy)

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str | None = None,
        prompt: str | None = None,
        negative_prompt: str = "blurry, deformed hands, ugly",
        n: int = 1,
        guidance_scale: int = 7,
        num_inference_steps: int = 30,
        aspect_ratio: str = "1:1",
        seed: int | None = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для генерации изображений.

        Args:
            model (str): Модель для генерации изображений.
            messages (Messages): Список сообщений для формирования запроса.
            proxy (str | None, optional): Прокси-сервер для использования. По умолчанию None.
            prompt (str | None, optional): Дополнительный текст запроса. По умолчанию None.
            negative_prompt (str, optional): Негативный текст запроса. По умолчанию "blurry, deformed hands, ugly".
            n (int, optional): Количество генерируемых изображений. По умолчанию 1.
            guidance_scale (int, optional): Масштаб соответствия запросу. По умолчанию 7.
            num_inference_steps (int, optional): Количество шагов для генерации. По умолчанию 30.
            aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию "1:1".
            seed (int | None, optional): Зерно для генерации случайных чисел. По умолчанию None.

        Yields:
            Reasoning | ImageResponse: Объекты Reasoning и ImageResponse с информацией о процессе генерации и результатами.

        Raises:
            ResponseError: Если не удается инициировать генерацию изображения или возникает ошибка в процессе.
        """
        model = cls.get_model(model)
        prompt = format_image_prompt(messages, prompt)

        # Generate a random seed if not provided
        if seed is None:
            seed = random.randint(cls.RANDOM_SEED_MIN, cls.RANDOM_SEED_MAX)  # Common range for random seeds

        # Step 1: Get Authentication Token
        auth_data: dict = await cls.read_and_refresh_token(proxy)

        async with ClientSession() as session:
            # Step 2: Generate Images
            image_payload: dict[str, str] = {
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "style": model,
                "images_num": str(n),
                "cfg_scale": str(guidance_scale),
                "steps": str(num_inference_steps),
                "aspect_ratio": aspect_ratio,
                "seed": str(seed),
            }

            headers: dict[str, str] = {
                "Authorization": auth_data.get("idToken"),
            }
            try:
                async with session.post(cls.image_generation_url, data=image_payload, headers=headers, proxy=proxy) as image_response:
                    image_response.raise_for_status()  # Проверка на HTTP ошибки
                    image_data: dict = await image_response.json()
                    record_id: str | None = image_data.get("record_id")

                    if not record_id:
                        raise ResponseError(f"Failed to initiate image generation: {image_data}")

                # Step 3: Check Generation Status
                status_url: str = cls.status_check_url.format(record_id=record_id)
                counter: int = cls.STATUS_CHECK_COUNTER
                start_time: float = time.time()
                last_status: str | None = None
                while True:
                    async with session.get(status_url, headers=headers, proxy=proxy) as status_response:
                        status_response.raise_for_status()  # Проверка на HTTP ошибки
                        status_data: dict = await status_response.json()
                        status: str | None = status_data.get("status")

                        if status == "DONE":
                            image_urls: list[str] = [image["url"] for image in status_data.get("response", [])]
                            duration: float = time.time() - start_time
                            yield Reasoning(label="Generated", status=f"{n} image(s) in {duration:.2f}s")
                            yield ImageResponse(images=image_urls, alt=prompt)
                            return
                        elif status in ("IN_QUEUE", "IN_PROGRESS"):
                            if last_status != status:
                                last_status = status
                                if status == "IN_QUEUE":
                                    yield Reasoning(label="Waiting")
                                else:
                                    yield Reasoning(label="Generating")
                            await asyncio.sleep(cls.STATUS_CHECK_INTERVAL)  # Poll every 2 seconds
                        else:
                            raise ResponseError(f"Image generation failed with status: {status}")
            except Exception as ex:
                logger.error('Error during image generation', ex, exc_info=True)
                raise