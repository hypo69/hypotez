### **Анализ кода модуля `Airforce.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Использование `AsyncGeneratorProvider` и `ProviderModelMixin` для асинхронной генерации контента.
    - Реализация поддержки стриминга.
    - Поддержка системных сообщений и истории сообщений.
    - Использование `aiohttp` для асинхронных запросов.
    - Наличие методов для генерации текста и изображений.
    - Методы фильтрации контента для удаления нежелательной информации.
- **Минусы**:
    - Отсутствуют аннотации типов для параметров и возвращаемых значений функций.
    - Не используется `logger` для логирования ошибок и отладочной информации.
    - Присутствуют повторения кода, например, в блоках `try...except` для получения моделей текста и изображений.
    - Не все комментарии соответствуют требованиям к документации.
    - Не соблюдены PEP8 стандарты (пробелы вокруг операторов).
    - Не используется `j_loads` для загрузки JSON-данных.

#### **Рекомендации по улучшению**:
1.  **Добавить аннотации типов**:
    - Добавить аннотации типов для всех параметров и возвращаемых значений функций.

2.  **Использовать `logger` для логирования**:
    - Заменить `debug.log` на `logger.debug` для логирования отладочной информации.
    - Использовать `logger.error` для логирования ошибок с указанием исключения и трассировки.

3.  **Устранить повторения кода**:
    - Вынести повторяющийся код в отдельные функции для уменьшения дублирования.

4.  **Документировать все функции и классы**:
    - Добавить docstring для всех функций и классов с описанием параметров, возвращаемых значений и возможных исключений.

5.  **Соблюдать PEP8 стандарты**:
    - Добавить пробелы вокруг операторов присваивания и других операторов.

6. **Заменить `requests`  на `aiohttp`**:
    - Так как в коде используется асинхронность, следует заменить синхронные вызовы `requests.get` на асинхронные `aiohttp`.

#### **Оптимизированный код**:

```python
"""
Модуль для работы с Airforce API
======================================

Модуль содержит класс :class:`Airforce`, который используется для взаимодействия с Airforce API для
генерации текста и изображений.

Пример использования:
----------------------

>>> from src.endpoints.gpt4free.g4f.Provider.not_working.Airforce import Airforce
>>> import asyncio
>>> async def main():
>>>     messages = [{"role": "user", "content": "Hello"}]
>>>     result = await Airforce.create_async_generator(model='llama-3.1-70b-chat', messages=messages)
>>>     async for item in result:
>>>         print(item)
>>> asyncio.run(main())
"""
import json
import random
import re
from typing import List, Optional

import aiohttp
from aiohttp import ClientSession

from src.logger import logger #  Используем модуль logger для логирования
from ...typing import AsyncResult, Messages
from ...providers.response import ImageResponse, FinishReason, Usage
from ...requests.raise_for_status import raise_for_status
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin


def split_message(message: str, max_length: int = 1000) -> List[str]:
    """Разбивает сообщение на части длиной не более (max_length).

    Args:
        message (str): Входное сообщение.
        max_length (int): Максимальная длина части сообщения. По умолчанию 1000.

    Returns:
        List[str]: Список частей сообщения.
    """
    chunks = []
    while len(message) > max_length:
        split_point = message.rfind(' ', 0, max_length)
        if split_point == -1:
            split_point = max_length
        chunks.append(message[:split_point])
        message = message[split_point:].strip()
    if message:
        chunks.append(message)
    return chunks


class Airforce(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Провайдер для доступа к API Airforce.

    Поддерживает генерацию текста и изображений.
    """
    url = 'https://api.airforce'
    api_endpoint_completions = 'https://api.airforce/chat/completions'
    api_endpoint_imagine2 = 'https://api.airforce/imagine2'

    working = False
    supports_stream = True
    supports_system_message = True
    supports_message_history = True

    default_model = 'llama-3.1-70b-chat'
    default_image_model = 'flux'

    models: List[str] = []
    image_models: List[str] = []

    hidden_models = {'Flux-1.1-Pro'}
    additional_models_imagine = ['flux-1.1-pro', 'midjourney', 'dall-e-3']
    model_aliases = {
        # Alias mappings for models
        'openchat-3.5': 'openchat-3.5-0106',
        'deepseek-coder': 'deepseek-coder-6.7b-instruct',
        'hermes-2-dpo': 'Nous-Hermes-2-Mixtral-8x7B-DPO',
        'hermes-2-pro': 'hermes-2-pro-mistral-7b',
        'openhermes-2.5': 'openhermes-2.5-mistral-7b',
        'lfm-40b': 'lfm-40b-moe',
        'german-7b': 'discolm-german-7b-v1',
        'llama-2-7b': 'llama-2-7b-chat-int8',
        'llama-3.1-70b': 'llama-3.1-70b-chat',
        'llama-3.1-8b': 'llama-3.1-8b-chat',
        'llama-3.1-70b': 'llama-3.1-70b-turbo',
        'llama-3.1-8b': 'llama-3.1-8b-turbo',
        'neural-7b': 'neural-chat-7b-v3-1',
        'zephyr-7b': 'zephyr-7b-beta',
        'evil': 'any-uncensored',
        'sdxl': 'stable-diffusion-xl-lightning',
        'sdxl': 'stable-diffusion-xl-base',
        'flux-pro': 'flux-1.1-pro',
        'llama-3.1-8b': 'llama-3.1-8b-chat'
    }

    @classmethod
    async def _fetch_models(cls, url: str, model_list: list, additional_models: Optional[List[str]] = None) -> None:
        """Получает список моделей из API.

        Args:
            url (str): URL для запроса списка моделей.
            model_list (list): Список, в который будут добавлены модели.
            additional_models (Optional[List[str]], optional): Дополнительные модели для добавления. Defaults to None.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }
        try:
            async with ClientSession(headers=headers) as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    if isinstance(data, dict) and 'data' in data:
                        models = [model['id'] for model in data['data']]
                        model_list.extend(models)
                    elif isinstance(data, list):
                        model_list.extend(data)
                    else:
                        logger.warning(f'Unexpected data format: {data}')
        except aiohttp.ClientError as ex:
            logger.error(f'Error fetching models from {url}', exc_info=True)
        if additional_models:
            model_list.extend(additional_models)

    @classmethod
    async def get_models(cls) -> List[str]:
        """Получает доступные модели с обработкой ошибок.

        Returns:
            List[str]: Список доступных моделей.
        """
        if not cls.image_models:
            await cls._fetch_models(
                f'{cls.url}/imagine2/models',
                cls.image_models,
                cls.additional_models_imagine
            )
        if not cls.models:
            await cls._fetch_models(
                f'{cls.url}/models',
                cls.models
            )
            cls.models = [model for model in cls.models if model not in cls.hidden_models]
            cls.models.extend(list(cls.model_aliases.keys()))

        return cls.models or list(cls.model_aliases.keys())

    @classmethod
    def get_model(cls, model: str) -> str:
        """Получает фактическое имя модели из alias.

        Args:
            model (str): Alias модели.

        Returns:
            str: Фактическое имя модели.
        """
        return cls.model_aliases.get(model, model or cls.default_model)

    @classmethod
    def _filter_content(cls, part_response: str) -> str:
        """
        Фильтрует нежелательный контент из частичного ответа.
        """
        part_response = re.sub(
            r"One message exceeds the \\d+chars per message limit\\..+https:\\/\\/discord\\.com\\/invite\\/\\S+",
            '',
            part_response
        )

        part_response = re.sub(
            r"Rate limit \\(\\d+\\/minute\\) exceeded\\. Join our discord for more: .+https:\\/\\/discord\\.com\\/invite\\/\\S+",
            '',
            part_response
        )

        return part_response

    @classmethod
    def _filter_response(cls, response: str) -> str:
        """
        Фильтрует полный ответ для удаления системных ошибок и другого нежелательного текста.
        """
        if "Model not found or too long input. Or any other error (xD)" in response:
            raise ValueError(response)

        filtered_response = re.sub(r"\\[ERROR\\] \'\\w{8}-\\w{4}-\\w{4}-\\w{4}-\\w{12}\'", '', response)  # any-uncensored
        filtered_response = re.sub(r\'<\\|im_end\\|>\', '', filtered_response)  # remove <|im_end|> token
        filtered_response = re.sub(r\'</s>\', '', filtered_response)  # neural-chat-7b-v3-1
        filtered_response = re.sub(r'^(Assistant: |AI: |ANSWER: |Output: )', '', filtered_response)  # phi-2
        filtered_response = cls._filter_content(filtered_response)
        return filtered_response

    @classmethod
    async def generate_image(
        cls,
        model: str,
        prompt: str,
        size: str,
        seed: int,
        proxy: Optional[str] = None
    ) -> AsyncResult:
        """Генерирует изображение.

        Args:
            model (str): Модель для генерации изображения.
            prompt (str): Текст запроса.
            size (str): Размер изображения.
            seed (int): Зерно для генерации.
            proxy (Optional[str], optional): Прокси-сервер. По умолчанию None.

        Yields:
            ImageResponse: Сгенерированное изображение.

        Raises:
            RuntimeError: Если генерация изображения не удалась.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
            'Accept': 'image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
        }
        params = {'model': model, 'prompt': prompt, 'size': size, 'seed': seed}

        async with ClientSession(headers=headers) as session:
            try:
                async with session.get(cls.api_endpoint_imagine2, params=params, proxy=proxy) as response:
                    if response.status == 200:
                        image_url = str(response.url)
                        yield ImageResponse(images=image_url, alt=prompt)
                    else:
                        error_text = await response.text()
                        raise RuntimeError(f'Image generation failed: {response.status} - {error_text}')
            except aiohttp.ClientError as ex:
                logger.error('Error during image generation', exc_info=True)
                raise RuntimeError(f'Image generation failed: {ex}')

    @classmethod
    async def generate_text(
        cls,
        model: str,
        messages: Messages,
        max_tokens: int,
        temperature: float,
        top_p: float,
        stream: bool,
        proxy: Optional[str] = None
    ) -> AsyncResult:
        """Генерирует текст, буферизует ответ, фильтрует его и возвращает окончательный результат.

        Args:
            model (str): Модель для генерации текста.
            messages (Messages): Список сообщений.
            max_tokens (int): Максимальное количество токенов.
            temperature (float): Температура.
            top_p (float): Top P.
            stream (bool): Использовать ли стриминг.
            proxy (Optional[str], optional): Прокси-сервер. По умолчанию None.

        Yields:
            str | Usage | FinishReason: Части текста, информация об использовании или причина завершения.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
            'Accept': 'application/json, text/event-stream',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
        }

        final_messages = []
        for message in messages:
            message_chunks = split_message(message['content'], max_length=1000)
            final_messages.extend([{'role': message['role'], 'content': chunk} for chunk in message_chunks])
        data = {
            'messages': final_messages,
            'model': model,
            'temperature': temperature,
            'top_p': top_p,
            'stream': stream,
        }
        if max_tokens != 512:
            data['max_tokens'] = max_tokens

        async with ClientSession(headers=headers) as session:
            try:
                async with session.post(cls.api_endpoint_completions, json=data, proxy=proxy) as response:
                    await raise_for_status(response)

                    if stream:
                        idx = 0
                        async for line in response.content:
                            line = line.decode('utf-8').strip()
                            if line.startswith('data: '):
                                try:
                                    json_str = line[6:]  # Remove 'data: ' prefix
                                    chunk = json.loads(json_str)
                                    if 'choices' in chunk and chunk['choices']:
                                        delta = chunk['choices'][0].get('delta', {})
                                        if 'content' in delta:
                                            chunk = cls._filter_response(delta['content'])
                                            if chunk:
                                                yield chunk
                                                idx += 1
                                except json.JSONDecodeError:
                                    continue
                        if idx == 512:
                            yield FinishReason('length')
                    else:
                        # Non-streaming response
                        result = await response.json()
                        if 'usage' in result:
                            yield Usage(**result['usage'])
                            if result['usage']['completion_tokens'] == 512:
                                yield FinishReason('length')
                        if 'choices' in result and result['choices']:
                            message = result['choices'][0].get('message', {})
                            content = message.get('content', '')
                            filtered_response = cls._filter_response(content)
                            yield filtered_response
            except aiohttp.ClientError as ex:
                logger.error('Error during text generation', exc_info=True)

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        prompt: Optional[str] = None,
        proxy: Optional[str] = None,
        max_tokens: int = 512,
        temperature: float = 1,
        top_p: float = 1,
        stream: bool = True,
        size: str = '1:1',
        seed: Optional[int] = None,
        **kwargs
    ) -> AsyncResult:
        """Создает асинхронный генератор для получения текста или изображений.

        Args:
            model (str): Модель для генерации.
            messages (Messages): Список сообщений.
            prompt (Optional[str], optional): Текст запроса. По умолчанию None.
            proxy (Optional[str], optional): Прокси-сервер. По умолчанию None.
            max_tokens (int, optional): Максимальное количество токенов. По умолчанию 512.
            temperature (float, optional): Температура. По умолчанию 1.
            top_p (float, optional): Top P. По умолчанию 1.
            stream (bool, optional): Использовать ли стриминг. По умолчанию True.
            size (str, optional): Размер изображения. По умолчанию '1:1'.
            seed (Optional[int], optional): Зерно для генерации изображения. По умолчанию None.
            **kwargs: Дополнительные аргументы.

        Yields:
            str | ImageResponse | Usage | FinishReason: Результат генерации.
        """
        model = cls.get_model(model)
        if model in cls.image_models:
            if prompt is None:
                prompt = messages[-1]['content']
            if seed is None:
                seed = random.randint(0, 10000)
            async for result in cls.generate_image(model, prompt, size, seed, proxy):
                yield result
        else:
            async for result in cls.generate_text(model, messages, max_tokens, temperature, top_p, stream, proxy):
                yield result