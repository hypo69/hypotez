### **Анализ кода модуля `HuggingFaceInference.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Использование асинхронности для неблокирующих операций.
  - Наличие обработки исключений.
  - Использование `StreamSession` для стриминга ответов.
  - Реализация выбора формата промпта для разных моделей.
- **Минусы**:
  - Смешанный стиль форматирования строк (использование как `""`, так и `''`).
  - Некоторые участки кода выглядят сложными для понимания из-за большого количества условий.
  - Отсутствуют аннотации типов для локальных переменных.
  - Не все функции и методы имеют docstring.
  - Отсутствует логирование ошибок с использованием `logger`.

#### **Рекомендации по улучшению**:
- **Унификация форматирования строк**: Использовать только одинарные кавычки (`''`).
- **Добавление аннотаций типов**: Добавить аннотации типов для всех переменных, аргументов и возвращаемых значений функций.
- **Упрощение логики**: Разбить сложные условия на более простые и понятные блоки.
- **Добавление документации**: Добавить docstring для всех функций и методов, включая описание аргументов, возвращаемых значений и возможных исключений.
- **Логирование ошибок**: Добавить логирование ошибок с использованием `logger` из `src.logger`.
- **Использовать `j_loads` или `j_loads_ns`**: для чтения json файлов.
- **Рефакторинг**: Упростить логику выбора формата промпта, возможно, с использованием словаря соответствий `model_type: format_function`.
- **Избегать `Union`**: Использовать `|` вместо `Union[]`

#### **Оптимизированный код**:

```python
from __future__ import annotations

import json
import base64
import random
import requests
from typing import AsyncGenerator, Optional, List, Dict, Any

from ...typing import AsyncResult, Messages
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin, format_prompt
from ...errors import ModelNotSupportedError, ResponseError
from ...requests import StreamSession, raise_for_status
from ...providers.response import FinishReason, ImageResponse
from ...image.copy_images import save_response_media
from ...image import use_aspect_ratio
from ..helper import format_image_prompt, get_last_user_message
from .models import default_model, default_image_model, model_aliases, text_models, image_models, vision_models
from ... import debug
from src.logger import logger  # Import logger

provider_together_urls: Dict[str, str] = {
    'black-forest-labs/FLUX.1-dev': 'https://router.huggingface.co/together/v1/images/generations',
    'black-forest-labs/FLUX.1-schnell': 'https://router.huggingface.co/together/v1/images/generations',
}


class HuggingFaceInference(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Класс для взаимодействия с Hugging Face Inference API.
    Предоставляет асинхронный генератор для получения ответов от моделей Hugging Face.
    """
    url: str = 'https://huggingface.co'
    parent: str = 'HuggingFace'
    working: bool = True

    default_model: str = default_model
    default_image_model: str = default_image_model
    model_aliases: Dict[str, str] = model_aliases
    image_models: List[str] = image_models

    model_data: Dict[str, Dict] = {}

    @classmethod
    def get_models(cls) -> list[str]:
        """
        Получает список поддерживаемых моделей.

        Returns:
            list[str]: Список идентификаторов моделей.
        """
        if not cls.models:
            models: List[str] = text_models.copy()
            url: str = 'https://huggingface.co/api/models?inference=warm&pipeline_tag=text-generation'
            response = requests.get(url)
            if response.ok:
                extra_models: List[str] = [
                    model['id'] for model in response.json() if model.get('trendingScore', 0) >= 10
                ]
                models = extra_models + vision_models + [model for model in models if model not in extra_models]
            url = 'https://huggingface.co/api/models?pipeline_tag=text-to-image'
            response = requests.get(url)
            cls.image_models: List[str] = image_models.copy()
            if response.ok:
                extra_models: List[str] = [
                    model['id'] for model in response.json() if model.get('trendingScore', 0) >= 20
                ]
                cls.image_models.extend([model for model in extra_models if model not in cls.image_models])
            models.extend([model for model in cls.image_models if model not in models])
            cls.models: List[str] = models
        return cls.models

    @classmethod
    async def get_model_data(cls, session: StreamSession, model: str) -> dict:
        """
        Получает данные о модели из Hugging Face API.

        Args:
            session (StreamSession): Асинхровая сессия для выполнения запросов.
            model (str): Идентификатор модели.

        Returns:
            dict: Данные о модели в формате JSON.

        Raises:
            ModelNotSupportedError: Если модель не поддерживается.
            ResponseError: Если произошла ошибка при выполнении запроса.
        """
        if model in cls.model_data:
            return cls.model_data[model]
        try:
            async with session.get(f'https://huggingface.co/api/models/{model}') as response:
                if response.status == 404:
                    raise ModelNotSupportedError(f'Model is not supported: {model} in: {cls.__name__}')
                await raise_for_status(response)
                cls.model_data[model] = await response.json()
            return cls.model_data[model]
        except Exception as ex:
            logger.error(f'Error while fetching model data for {model}', ex, exc_info=True)
            raise

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool = True,
        proxy: Optional[str] = None,
        timeout: int = 600,
        api_base: str = 'https://api-inference.huggingface.co',
        api_key: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: Optional[float] = None,
        prompt: Optional[str] = None,
        action: Optional[str] = None,
        extra_data: dict = {},
        seed: Optional[int] = None,
        aspect_ratio: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[str | ImageResponse | FinishReason, None]:
        """
        Создает асинхронный генератор для получения ответов от моделей Hugging Face.

        Args:
            model (str): Идентификатор модели.
            messages (Messages): Список сообщений для отправки в модель.
            stream (bool, optional): Флаг стриминга ответов. По умолчанию True.
            proxy (Optional[str], optional): Адрес прокси-сервера. По умолчанию None.
            timeout (int, optional): Время ожидания ответа. По умолчанию 600.
            api_base (str, optional): Базовый URL API. По умолчанию 'https://api-inference.huggingface.co'.
            api_key (Optional[str], optional): API ключ. По умолчанию None.
            max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию 1024.
            temperature (float, optional): Температура для генерации текста. По умолчанию None.
            prompt (Optional[str], optional): Промпт для генерации изображения. По умолчанию None.
            action (Optional[str], optional): Действие, которое необходимо выполнить. По умолчанию None.
            extra_data (dict, optional): Дополнительные данные для отправки в модель. По умолчанию {}.
            seed (Optional[int], optional): Зерно для воспроизводимости результатов. По умолчанию None.
            aspect_ratio (Optional[str], optional): Соотношение сторон изображения. По умолчанию None.
            width (Optional[int], optional): Ширина изображения. По умолчанию None.
            height (Optional[int], optional): Высота изображения. По умолчанию None.
            **kwargs: Дополнительные аргументы.

        Yields:
            str | ImageResponse | FinishReason: Части ответа от модели.

        Raises:
            ModelNotSupportedError: Если модель не поддерживается.
            ResponseError: Если произошла ошибка при выполнении запроса.
        """
        try:
            model = cls.get_model(model)
        except ModelNotSupportedError:
            pass

        headers: Dict[str, str] = {
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/json',
        }
        if api_key is not None:
            headers['Authorization'] = f'Bearer {api_key}'

        image_extra_data: Dict[str, Any] = use_aspect_ratio({
            'width': width,
            'height': height,
            **extra_data
        }, aspect_ratio)

        async with StreamSession(
            headers=headers,
            proxy=proxy,
            timeout=timeout
        ) as session:
            try:
                if model in provider_together_urls:
                    data: Dict[str, Any] = {
                        'response_format': 'url',
                        'prompt': format_image_prompt(messages, prompt),
                        'model': model,
                        **image_extra_data
                    }
                    async with session.post(provider_together_urls[model], json=data) as response:
                        if response.status == 404:
                            raise ModelNotSupportedError(f'Model is not supported: {model}')
                        await raise_for_status(response)
                        result: Dict[str, Any] = await response.json()
                        yield ImageResponse([item['url'] for item in result['data']], data['prompt'])
                    return
            except ModelNotSupportedError:
                pass
            except Exception as ex:
                logger.error(f'Error while processing image generation for model {model}', ex, exc_info=True)
                raise

            payload: Optional[Dict[str, Any]] = None
            params: Dict[str, Any] = {
                'return_full_text': False,
                'max_new_tokens': max_tokens,
                'temperature': temperature,
                **extra_data
            }
            do_continue: bool = action == 'continue'

            if payload is None:
                try:
                    model_data: Dict[str, Any] = await cls.get_model_data(session, model)
                    pipeline_tag: Optional[str] = model_data.get('pipeline_tag')

                    if pipeline_tag == 'text-to-image':
                        stream = False
                        inputs: str = format_image_prompt(messages, prompt)
                        payload = {'inputs': inputs, 'parameters': {'seed': random.randint(0, 2**32) if seed is None else seed, **image_extra_data}}
                    elif pipeline_tag in ('text-generation', 'image-text-to-text'):
                        model_type: Optional[str] = None
                        if 'config' in model_data and 'model_type' in model_data['config']:
                            model_type = model_data['config']['model_type']
                        debug.log(f'Model type: {model_type}')
                        inputs: str = get_inputs(messages, model_data, model_type, do_continue)
                        debug.log(f'Inputs len: {len(inputs)}')
                        if len(inputs) > 4096:
                            if len(messages) > 6:
                                messages = messages[:3] + messages[-3:]
                            else:
                                messages = [m for m in messages if m['role'] == 'system'] + [{'role': 'user', 'content': get_last_user_message(messages)}]
                            inputs = get_inputs(messages, model_data, model_type, do_continue)
                            debug.log(f'New len: {len(inputs)}')
                        if model_type == 'gpt2' and max_tokens >= 1024:
                            params['max_new_tokens'] = 512
                        if seed is not None:
                            params['seed'] = seed
                        payload = {'inputs': inputs, 'parameters': params, 'stream': stream}
                    else:
                        raise ModelNotSupportedError(f'Model is not supported: {model} in: {cls.__name__} pipeline_tag: {pipeline_tag}')
                except Exception as ex:
                    logger.error(f'Error while preparing payload for model {model}', ex, exc_info=True)
                    raise
            try:
                async with session.post(f'{api_base.rstrip("/")}/models/{model}', json=payload) as response:
                    if response.status == 404:
                        raise ModelNotSupportedError(f'Model is not supported: {model}')
                    await raise_for_status(response)
                    if stream:
                        first: bool = True
                        is_special: bool = False
                        async for line in response.iter_lines():
                            if line.startswith(b'data:'):
                                data = json.loads(line[5:])
                                if 'error' in data:
                                    raise ResponseError(data['error'])
                                if not data['token']['special']:
                                    chunk: str = data['token']['text']
                                    if first and not do_continue:
                                        first = False
                                        chunk = chunk.lstrip()
                                    if chunk:
                                        yield chunk
                                else:
                                    is_special = True
                        debug.log(f'Special token: {is_special}')
                        yield FinishReason('stop' if is_special else 'length')
                    else:
                        async for chunk in save_response_media(response, inputs, [aspect_ratio, model]):
                            yield chunk
                            return
                        yield (await response.json())[0]['generated_text'].strip()
            except Exception as ex:
                logger.error(f'Error during response processing for model {model}', ex, exc_info=True)
                raise


def format_prompt_mistral(messages: Messages, do_continue: bool = False) -> str:
    """
    Форматирует промпт для модели Mistral.

    Args:
        messages (Messages): Список сообщений.
        do_continue (bool): Флаг продолжения генерации.

    Returns:
        str: Сформированный промпт.
    """
    system_messages: List[str] = [message['content'] for message in messages if message['role'] == 'system']
    question: str = ' '.join([messages[-1]['content'], *system_messages])
    history: str = '\\n'.join([
        f'<s>[INST]{messages[idx-1]["content"]} [/INST] {message["content"]}</s>'
        for idx, message in enumerate(messages)
        if message['role'] == 'assistant'
    ])
    if do_continue:
        return history[:-len('</s>')]
    return f'{history}\\n<s>[INST] {question} [/INST]'


def format_prompt_qwen(messages: Messages, do_continue: bool = False) -> str:
    """
    Форматирует промпт для модели Qwen.

    Args:
        messages (Messages): Список сообщений.
        do_continue (bool): Флаг продолжения генерации.

    Returns:
        str: Сформированный промпт.
    """
    prompt: str = ''.join([
        f'<|im_start|>{message["role"]}\\n{message["content"]}\\n<|im_end|>\\n' for message in messages
    ]) + ('' if do_continue else '<|im_start|>assistant\\n')
    if do_continue:
        return prompt[:-len('\\n<|im_end|>\\n')]
    return prompt


def format_prompt_qwen2(messages: Messages, do_continue: bool = False) -> str:
    """
    Форматирует промпт для модели Qwen2.

    Args:
        messages (Messages): Список сообщений.
        do_continue (bool): Флаг продолжения генерации.

    Returns:
        str: Сформированный промпт.
    """
    prompt: str = ''.join([
        f'\\u003C｜{message["role"].capitalize()}｜\\u003E{message["content"]}\\u003C｜end of sentence｜\\u003E' for message in messages
    ]) + ('' if do_continue else '\\u003C｜Assistant｜\\u003E')
    if do_continue:
        return prompt[:-len('\\u003C｜Assistant｜\\u003E')]
    return prompt


def format_prompt_llama(messages: Messages, do_continue: bool = False) -> str:
    """
    Форматирует промпт для модели Llama.

    Args:
        messages (Messages): Список сообщений.
        do_continue (bool): Флаг продолжения генерации.

    Returns:
        str: Сформированный промпт.
    """
    prompt: str = '<|begin_of_text|>' + ''.join([
        f'<|start_header_id|>{message["role"]}<|end_header_id|>\\n\\n{message["content"]}\\n<|eot_id|>\\n' for message in messages
    ]) + ('' if do_continue else '<|start_header_id|>assistant<|end_header_id|>\\n\\n')
    if do_continue:
        return prompt[:-len('\\n<|eot_id|>\\n')]
    return prompt


def format_prompt_custom(messages: Messages, end_token: str = '</s>', do_continue: bool = False) -> str:
    """
    Форматирует промпт с использованием кастомного токена завершения.

    Args:
        messages (Messages): Список сообщений.
        end_token (str): Токен завершения.
        do_continue (bool): Флаг продолжения генерации.

    Returns:
        str: Сформированный промпт.
    """
    prompt: str = ''.join([
        f'<|{message["role"]}|>\\n{message["content"]}{end_token}\\n' for message in messages
    ]) + ('' if do_continue else '<|assistant|>\\n')
    if do_continue:
        return prompt[:-len(end_token + '\\n')]
    return prompt


def get_inputs(messages: Messages, model_data: dict, model_type: Optional[str], do_continue: bool = False) -> str:
    """
    Получает входные данные для модели.

    Args:
        messages (Messages): Список сообщений.
        model_data (dict): Данные о модели.
        model_type (str): Тип модели.
        do_continue (bool): Флаг продолжения генерации.

    Returns:
        str: Входные данные для модели.
    """
    if model_type in ('gpt2', 'gpt_neo', 'gemma', 'gemma2'):
        inputs: str = format_prompt(messages, do_continue=do_continue)
    elif model_type == 'mistral' and model_data.get('author') == 'mistralai':
        inputs: str = format_prompt_mistral(messages, do_continue)
    elif 'config' in model_data and 'tokenizer_config' in model_data['config'] and 'eos_token' in model_data['config']['tokenizer_config']:
        eos_token: str = model_data['config']['tokenizer_config']['eos_token']
        if eos_token in ('<|endoftext|>', '<eos>', '</s>'):
            inputs = format_prompt_custom(messages, eos_token, do_continue)
        elif eos_token == '<|im_end|>':
            inputs = format_prompt_qwen(messages, do_continue)
        elif 'content' in eos_token and eos_token['content'] == '\\u003C｜end of sentence｜\\u003E':
            inputs = format_prompt_qwen2(messages, do_continue)
        elif eos_token == '<|eot_id|>':
            inputs = format_prompt_llama(messages, do_continue)
        else:
            inputs = format_prompt(messages, do_continue=do_continue)
    else:
        inputs = format_prompt(messages, do_continue=do_continue)
    return inputs