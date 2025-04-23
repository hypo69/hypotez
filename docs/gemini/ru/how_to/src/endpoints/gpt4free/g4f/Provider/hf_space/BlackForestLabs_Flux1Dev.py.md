## \file hypotez/src/endpoints/gpt4free/g4f/Provider/hf_space/BlackForestLabs_Flux1Dev.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для взаимодействия с провайдером BlackForestLabs_Flux1Dev для генерации изображений.
=========================================================================================

Модуль предоставляет асинхронный генератор для создания изображений с использованием
модели BlackForestLabs Flux-1-Dev. Он включает в себя функции для форматирования запросов,
обработки ответов и управления сессиями.

Зависимости:
    - typing
    - json
    - uuid
    - requests
    - ...providers.response
    - ...requests
    - ...image
    - ...errors
    - ..base_provider
    - ..helper
    - .DeepseekAI_JanusPro7b
    - .raise_for_status

 .. module:: src.endpoints.gpt4free.g4f.Provider.hf_space.BlackForestLabs_Flux1Dev
"""

from __future__ import annotations

import json
import uuid

from ...typing import AsyncResult, Messages
from ...providers.response import ImageResponse, ImagePreview, JsonConversation, Reasoning
from ...requests import StreamSession
from ...image import use_aspect_ratio
from ...errors import ResponseError
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..helper import format_image_prompt
from .DeepseekAI_JanusPro7b import get_zerogpu_token
from .raise_for_status import raise_for_status


class BlackForestLabs_Flux1Dev(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Класс для взаимодействия с моделью BlackForestLabs Flux-1-Dev для генерации изображений.

    Атрибуты:
        label (str): Отображаемое имя провайдера.
        url (str): URL главной страницы провайдера.
        space (str): Идентификатор пространства Hugging Face.
        referer (str): Referer для HTTP-запросов.
        working (bool): Указывает, работает ли провайдер.
        default_model (str): Модель, используемая по умолчанию.
        default_image_model (str): Модель для генерации изображений по умолчанию.
        model_aliases (dict): Псевдонимы моделей.
        image_models (list): Список поддерживаемых моделей изображений.
        models (list): Список поддерживаемых моделей.
    """

    label: str = "BlackForestLabs Flux-1-Dev"
    url: str = "https://black-forest-labs-flux-1-dev.hf.space"
    space: str = "black-forest-labs/FLUX.1-dev"
    referer: str = f"{url}/?__theme=light"

    working: bool = True

    default_model: str = 'black-forest-labs-flux-1-dev'
    default_image_model: str = default_model
    model_aliases: dict = {"flux-dev": default_image_model, "flux": default_image_model}
    image_models: list = list(model_aliases.keys())
    models: list = image_models

    @classmethod
    def run(cls, method: str, session: StreamSession, conversation: JsonConversation, data: list = None):
        """
        Выполняет HTTP-запрос к API.

        Args:
            method (str): HTTP-метод ("post" или "get").
            session (StreamSession): Асинхровая сессия для выполнения запросов.
            conversation (JsonConversation): Объект, содержащий данные для общения с API.
            data (list, optional): Данные для отправки в запросе. По умолчанию `None`.

        Returns:
            Объект ответа `session.post` или `session.get`.

        Raises:
            Возможные исключения, связанные с сетевыми запросами.
        """
        headers: dict[str, str] = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-zerogpu-token": conversation.zerogpu_token,
            "x-zerogpu-uuid": conversation.zerogpu_uuid,
            "referer": cls.referer,
        }
        if method == "post":
            return session.post(f"{cls.url}/gradio_api/queue/join?__theme=light", **{
                "headers": {k: v for k, v in headers.items() if v is not None},
                "json": {"data": data, "event_data": None, "fn_index": 2, "trigger_id": 4,
                         "session_hash": conversation.session_hash}

            })
        return session.get(f"{cls.url}/gradio_api/queue/data?session_hash={conversation.session_hash}", **{
            "headers": {
                "accept": "text/event-stream",
                "content-type": "application/json",
                "referer": cls.referer,
            }
        })

    @classmethod
    async def create_async_generator(
            cls,
            model: str,
            messages: Messages,
            prompt: str = None,
            proxy: str = None,
            aspect_ratio: str = "1:1",
            width: int = None,
            height: int = None,
            guidance_scale: float = 3.5,
            num_inference_steps: int = 28,
            seed: int = 0,
            randomize_seed: bool = True,
            cookies: dict = None,
            api_key: str = None,
            zerogpu_uuid: str = "[object Object]",
            **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для генерации изображений.

        Args:
            model (str): Название модели для генерации изображений.
            messages (Messages): Список сообщений для формирования запроса.
            prompt (str, optional): Дополнительный промпт для генерации изображения. По умолчанию `None`.
            proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
            aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию "1:1".
            width (int, optional): Ширина изображения. По умолчанию `None`.
            height (int, optional): Высота изображения. По умолчанию `None`.
            guidance_scale (float, optional): Масштаб соответствия запросу. По умолчанию 3.5.
            num_inference_steps (int, optional): Количество шагов для генерации изображения. По умолчанию 28.
            seed (int, optional): Зерно для случайной генерации. По умолчанию 0.
            randomize_seed (bool, optional): Флаг для рандомизации зерна. По умолчанию `True`.
            cookies (dict, optional): Куки для HTTP-запросов. По умолчанию `None`.
            api_key (str, optional): API ключ для доступа к сервису. По умолчанию `None`.
            zerogpu_uuid (str, optional): UUID для zerogpu. По умолчанию "[object Object]".
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий результаты генерации изображения.

        Raises:
            RuntimeError: Если не удается распарсить сообщение от сервера.
            ResponseError: Если в ответе от сервера содержится ошибка.
        """
        async with StreamSession(impersonate="chrome", proxy=proxy) as session:
            prompt = format_image_prompt(messages, prompt)
            data = use_aspect_ratio({"width": width, "height": height}, aspect_ratio)
            data = [prompt, seed, randomize_seed, data.get("width"), data.get("height"), guidance_scale,
                    num_inference_steps]
            conversation = JsonConversation(zerogpu_token=api_key, zerogpu_uuid=zerogpu_uuid,
                                              session_hash=uuid.uuid4().hex)
            if conversation.zerogpu_token is None:
                conversation.zerogpu_uuid, conversation.zerogpu_token = await get_zerogpu_token(cls.space, session,
                                                                                                   conversation, cookies)
            async with cls.run(f"post", session, conversation, data) as response:
                await raise_for_status(response)
                assert (await response.json()).get("event_id")
                async with cls.run("get", session, conversation) as event_response:
                    await raise_for_status(event_response)
                    async for chunk in event_response.iter_lines():
                        if chunk.startswith(b"data: "):
                            try:
                                json_data = json.loads(chunk[6:])
                                if json_data is None:
                                    continue
                                if json_data.get('msg') == 'log':
                                    yield Reasoning(status=json_data["log"])

                                if json_data.get('msg') == 'progress':
                                    if 'progress_data' in json_data:
                                        if json_data['progress_data']:
                                            progress = json_data['progress_data'][0]
                                            yield Reasoning(
                                                status=f"{progress['desc']} {progress['index']}/{progress['length']}")
                                        else:
                                            yield Reasoning(status=f"Generating")

                                elif json_data.get('msg') == 'process_generating':
                                    for item in json_data['output']['data'][0]:
                                        if isinstance(item, dict) and "url" in item:
                                            yield ImagePreview(item["url"], prompt)
                                        elif isinstance(item, list) and len(item) > 2 and "url" in item[1]:
                                            yield ImagePreview(item[2], prompt)

                                elif json_data.get('msg') == 'process_completed':
                                    if 'output' in json_data and 'error' in json_data['output']:
                                        json_data['output']['error'] = json_data['output']['error'].split(" <a ")[0]
                                        raise ResponseError(json_data['output']['error'])
                                    if 'output' in json_data and 'data' in json_data['output']:
                                        yield Reasoning(status="Finished")
                                        if len(json_data['output']['data']) > 0:
                                            yield ImageResponse(json_data['output']['data'][0]["url"], prompt)
                                    break
                            except (json.JSONDecodeError, KeyError, TypeError) as e:
                                raise RuntimeError(f"Failed to parse message: {chunk.decode(errors='replace')}", e)

"""
Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет класс `BlackForestLabs_Flux1Dev`, который позволяет взаимодействовать
с API BlackForestLabs Flux-1-Dev для генерации изображений. Класс включает методы для
выполнения HTTP-запросов, форматирования данных и обработки ответов от API.

Шаги выполнения
-------------------------
1. **Инициализация класса**:
   - Создание экземпляра класса `BlackForestLabs_Flux1Dev` не требуется, так как используются
     только методы класса (`@classmethod`).

2. **Выполнение HTTP-запроса**:
   - Метод `run` выполняет HTTP-запрос к API с использованием `StreamSession`.
   - Он принимает HTTP-метод (`method`), сессию (`session`), объект общения (`conversation`)
     и данные (`data`) в качестве аргументов.
   - В зависимости от метода (POST или GET), он отправляет запрос к соответствующей конечной
     точке API.

3. **Создание асинхронного генератора**:
   - Метод `create_async_generator` создает асинхронный генератор для генерации изображений.
   - Он принимает параметры модели, сообщения, промпт, настройки изображения и другие
     конфигурационные параметры.
   - Функция форматирует запрос, получает токен zerogpu (если необходимо), отправляет
     запросы к API и обрабатывает ответы, возвращая результаты в виде асинхронного
     генератора.

4. **Обработка ответов**:
   - Генератор обрабатывает чанки данных, поступающие от API, и извлекает из них
     информацию о статусе, прогрессе и сгенерированных изображениях.
   - В случае ошибок в ответе от API, он вызывает исключение `ResponseError`.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.hf_space.BlackForestLabs_Flux1Dev import BlackForestLabs_Flux1Dev
from src.typing import Messages
import asyncio

async def main():
    messages: Messages = [{"role": "user", "content": "Generate a picture of a cat in cyberpunk style"}]
    async for item in BlackForestLabs_Flux1Dev.create_async_generator(
        model="black-forest-labs-flux-1-dev",
        messages=messages,
        width=512,
        height=512
    ):
        print(item)

if __name__ == "__main__":
    asyncio.run(main())
```
"""