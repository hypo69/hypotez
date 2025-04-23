### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код представляет собой класс `Grok`, который является асинхронным провайдером для взаимодействия с API Grok AI. Он предоставляет функциональность для аутентификации, создания запросов и обработки ответов от Grok AI, включая текстовые и графические данные.

Шаги выполнения
-------------------------
1. **Аутентификация**:
   - Метод `on_auth_async` используется для аутентификации пользователя. Он проверяет наличие cookies и, если они отсутствуют, запрашивает URL для логина.
   - Если cookies найдены, метод возвращает `AuthResult` с cookies, заголовками и информацией о прокси.
   - Если cookies отсутствуют, метод возвращает `RequestLogin` с URL для логина, полученным из переменной окружения `G4F_LOGIN_URL`.

2. **Подготовка payload**:
   - Метод `_prepare_payload` подготавливает данные для отправки в API Grok AI. Он принимает модель и сообщение в качестве аргументов и возвращает словарь с параметрами, необходимыми для запроса.
   - В payload включаются параметры, такие как имя модели, сообщение, флаги для включения/выключения поиска и генерации изображений, а также настройки для обработки результатов.

3. **Создание аутентифицированного запроса**:
   - Метод `create_authed` создает аутентифицированный запрос к API Grok AI. Он принимает модель, сообщения, результат аутентификации, cookies и другие параметры.
   - Метод форматирует запрос, определяет URL для нового или существующего диалога, отправляет запрос и обрабатывает ответ.
   - В процессе обработки ответа метод извлекает и возвращает различные типы данных, такие как текстовые токены, сгенерированные изображения и заголовки.

4. **Обработка ответа**:
   - Внутри `create_authed` происходит итерация по строкам ответа от API. Каждая строка парсится как JSON.
   - Из JSON извлекаются данные, такие как идентификатор диалога, текстовые токены, URL изображений и заголовки.
   - В зависимости от типа данных, извлеченных из JSON, генерируются различные типы объектов, такие как `ImagePreview`, `Reasoning`, `ImageResponse` и `TitleGeneration`.

Пример использования
-------------------------

```python
from __future__ import annotations

import os
import json
import time
from typing import Dict, Any, AsyncIterator

from ...typing import Messages, Cookies, AsyncResult
from ...providers.response import JsonConversation, Reasoning, ImagePreview, ImageResponse, TitleGeneration, AuthResult, RequestLogin
from ...requests import StreamSession, get_args_from_nodriver, DEFAULT_HEADERS
from ...requests.raise_for_status import raise_for_status
from ..base_provider import AsyncAuthedProvider, ProviderModelMixin
from ..helper import format_prompt, get_cookies, get_last_user_message

class Conversation(JsonConversation):
    def __init__(self,
        conversation_id: str
    ) -> None:
        self.conversation_id = conversation_id

class Grok(AsyncAuthedProvider, ProviderModelMixin):
    label = "Grok AI"
    url = "https://grok.com"
    cookie_domain = ".grok.com"
    assets_url = "https://assets.grok.com"
    conversation_url = "https://grok.com/rest/app-chat/conversations"

    needs_auth = True
    working = True

    default_model = "grok-3"
    models = [default_model, "grok-3-thinking", "grok-2"]
    model_aliases = {"grok-3-r1": "grok-3-thinking"}

    @classmethod
    async def on_auth_async(cls, cookies: Cookies = None, proxy: str = None, **kwargs) -> AsyncIterator:
        if cookies is None:
            cookies = get_cookies(cls.cookie_domain, False, True, False)
        if cookies is not None and "sso" in cookies:
            yield AuthResult(
                cookies=cookies,
                impersonate="chrome",
                proxy=proxy,
                headers=DEFAULT_HEADERS
            )
            return
        yield RequestLogin(cls.__name__, os.environ.get("G4F_LOGIN_URL") or "")
        yield AuthResult(
            **await get_args_from_nodriver(
                cls.url,
                proxy=proxy,
                wait_for='[href="/chat#private"]'
            )
        )

    @classmethod
    async def _prepare_payload(cls, model: str, message: str) -> Dict[str, Any]:
        return {
            "temporary": False,
            "modelName": "grok-latest" if model == "grok-2" else "grok-3",
            "message": message,
            "fileAttachments": [],
            "imageAttachments": [],
            "disableSearch": False,
            "enableImageGeneration": True,
            "returnImageBytes": False,
            "returnRawGrokInXaiRequest": False,
            "enableImageStreaming": True,
            "imageGenerationCount": 2,
            "forceConcise": False,
            "toolOverrides": {},
            "enableSideBySide": True,
            "isPreset": False,
            "sendFinalMetadata": True,
            "customInstructions": "",
            "deepsearchPreset": "",
            "isReasoning": model.endswith("-thinking") or model.endswith("-r1"),
        }

    @classmethod
    async def create_authed(
        cls,
        model: str,
        messages: Messages,
        auth_result: AuthResult,
        cookies: Cookies = None,
        return_conversation: bool = False,
        conversation: Conversation = None,
        **kwargs
    ) -> AsyncResult:
        conversation_id = None if conversation is None else conversation.conversation_id
        prompt = format_prompt(messages) if conversation_id is None else get_last_user_message(messages)
        async with StreamSession(
            **auth_result.get_dict()
        ) as session:
            payload = await cls._prepare_payload(model, prompt)
            if conversation_id is None:
                url = f"{cls.conversation_url}/new"
            else:
                url = f"{cls.conversation_url}/{conversation_id}/responses"
            async with session.post(url, json=payload) as response:
                await raise_for_status(response)

                thinking_duration = None
                async for line in response.iter_lines():
                    if line:
                        try:
                            json_data = json.loads(line)
                            result = json_data.get("result", {})
                            if conversation_id is None:
                                conversation_id = result.get("conversation", {}).get("conversationId")
                            response_data = result.get("response", {})
                            image = response_data.get("streamingImageGenerationResponse", None)
                            if image is not None:
                                yield ImagePreview(f'{cls.assets_url}/{image["imageUrl"]}', "", {"cookies": cookies, "headers": headers})
                            token = response_data.get("token", result.get("token"))
                            is_thinking = response_data.get("isThinking", result.get("isThinking"))
                            if token:
                                if is_thinking:
                                    if thinking_duration is None:
                                        thinking_duration = time.time()
                                        yield Reasoning(status="🤔 Is thinking...")
                                    yield Reasoning(token)
                                else:
                                    if thinking_duration is not None:
                                        thinking_duration = time.time() - thinking_duration
                                        status = f"Thought for {thinking_duration:.2f}s" if thinking_duration > 1 else "Finished"
                                        thinking_duration = None
                                        yield Reasoning(status=status)
                                    yield token
                            generated_images = response_data.get("modelResponse", {}).get("generatedImageUrls", None)
                            if generated_images:
                                yield ImageResponse([f'{cls.assets_url}/{image}\' for image in generated_images], "", {"cookies": cookies, "headers": headers})
                            title = result.get("title", {}).get("newTitle", "")
                            if title:
                                yield TitleGeneration(title)


                        except json.JSONDecodeError:
                            continue
                if return_conversation and conversation_id is not None:
                    yield Conversation(conversation_id)