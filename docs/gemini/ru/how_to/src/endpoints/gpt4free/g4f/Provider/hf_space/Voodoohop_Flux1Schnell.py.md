## \file hypotez/src/endpoints/gpt4free/g4f/Provider/hf_space/Voodoohop_Flux1Schnell.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для асинхронного взаимодействия с сервисом Voodoohop Flux-1-Schnell для генерации изображений.
=====================================================================================================
Модуль предоставляет класс `Voodoohop_Flux1Schnell`, который позволяет отправлять запросы к API
сервиса Voodoohop Flux-1-Schnell для генерации изображений на основе текстовых описаний.
Он поддерживает настройку параметров генерации, таких как размеры изображения, seed и количество шагов.

Зависимости:
    - aiohttp
    - json

 .. module:: src.endpoints.gpt4free.g4f.Provider.hf_space.Voodoohop_Flux1Schnell
"""
from __future__ import annotations

from aiohttp import ClientSession
import json

from ...typing import AsyncResult, Messages
from ...providers.response import ImageResponse
from ...errors import ResponseError
from ...requests.raise_for_status import raise_for_status
from ..helper import format_image_prompt
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin


class Voodoohop_Flux1Schnell(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Класс для взаимодействия с сервисом Voodoohop Flux-1-Schnell для генерации изображений.

    Args:
        AsyncGeneratorProvider: Базовый класс для асинхронных провайдеров.
        ProviderModelMixin: Миксин для работы с моделями провайдера.
    """

    label = "Voodoohop Flux-1-Schnell"
    url = "https://voodoohop-flux-1-schnell.hf.space"
    api_endpoint = "https://voodoohop-flux-1-schnell.hf.space/call/infer"

    working = True

    default_model = "voodoohop-flux-1-schnell"
    default_image_model = default_model
    model_aliases = {"flux-schnell": default_model, "flux": default_model}
    image_models = list(model_aliases.keys())
    models = image_models

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        prompt: str = None,
        width: int = 768,
        height: int = 768,
        num_inference_steps: int = 2,
        seed: int = 0,
        randomize_seed: bool = True,
        **kwargs,
    ) -> AsyncResult:
        """
        Асинхронно генерирует изображения на основе текстового описания, используя API Voodoohop Flux-1-Schnell.

        Args:
            model (str): Название модели для генерации изображения.
            messages (Messages): Список сообщений, используемых для формирования запроса.
            proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
            prompt (str, optional): Текстовое описание для генерации изображения. По умолчанию `None`.
            width (int, optional): Ширина изображения. По умолчанию 768.
            height (int, optional): Высота изображения. По умолчанию 768.
            num_inference_steps (int, optional): Количество шагов для генерации изображения. По умолчанию 2.
            seed (int, optional): Seed для генерации изображения. По умолчанию 0.
            randomize_seed (bool, optional): Флаг для рандомизации seed. По умолчанию `True`.
            **kwargs: Дополнительные аргументы.

        Yields:
            ImageResponse: Объект `ImageResponse` с URL сгенерированного изображения.

        Raises:
            ResponseError: Если происходит ошибка при генерации изображения.

        Example:
            >>> model = "voodoohop-flux-1-schnell"
            >>> messages = [{"role": "user", "content": "A cat"}]
            >>> async for response in Voodoohop_Flux1Schnell.create_async_generator(model=model, messages=messages):
            ...     print(response.images)
            ['https://example.com/image.png']
        """
        width = max(32, width - (width % 8))
        height = max(32, height - (height % 8))
        prompt = format_image_prompt(messages, prompt)
        payload = {
            "data": [prompt, seed, randomize_seed, width, height, num_inference_steps]
        }
        async with ClientSession() as session:
            async with session.post(cls.api_endpoint, json=payload, proxy=proxy) as response:
                await raise_for_status(response)
                response_data = await response.json()
                event_id = response_data["event_id"]
                while True:
                    async with session.get(
                        f"{cls.api_endpoint}/{event_id}", proxy=proxy
                    ) as status_response:
                        await raise_for_status(status_response)
                        while not status_response.content.at_eof():
                            event = await status_response.content.readuntil(b"\n\n")
                            if event.startswith(b"event:"):
                                event_parts = event.split(b"\ndata: ")
                                if len(event_parts) < 2:
                                    continue
                                event_type = event_parts[0].split(b": ")[1]
                                data = event_parts[1]
                                if event_type == b"error":
                                    raise ResponseError(f"Error generating image: {data}")
                                elif event_type == b"complete":
                                    json_data = json.loads(data)
                                    image_url = json_data[0]["url"]
                                    yield ImageResponse(images=[image_url], alt=prompt)
                                    return


"""
Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет класс `Voodoohop_Flux1Schnell`, который является асинхронным провайдером для генерации изображений с использованием API Voodoohop Flux-1-Schnell. 
Класс предоставляет метод `create_async_generator`, который отправляет запрос к API и возвращает URL сгенерированного изображения.

Шаги выполнения
-------------------------
1. Подготавливаются параметры запроса, такие как ширина и высота изображения, текстовое описание и seed.
2. Формируется полезная нагрузка (payload) с данными для запроса к API.
3. Отправляется POST-запрос к API с использованием `aiohttp.ClientSession`.
4. Полученный ответ обрабатывается для извлечения URL сгенерированного изображения.
5. Возвращается объект `ImageResponse` с URL изображения.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.hf_space import Voodoohop_Flux1Schnell
import asyncio

async def main():
    model = "voodoohop-flux-1-schnell"
    messages = [{"role": "user", "content": "A cat playing guitar"}]
    async for response in Voodoohop_Flux1Schnell.create_async_generator(model=model, messages=messages):
        print(response.images)

if __name__ == "__main__":
    asyncio.run(main())
```
"""