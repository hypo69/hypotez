### **Анализ кода модуля `HuggingFaceAPI.py`**

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код структурирован в соответствии с принципами ООП, используется наследование от `OpenaiTemplate`.
    - Присутствуют аннотации типов.
    - Есть обработка исключений.
- **Минусы**:
    - Не все функции и методы содержат подробные docstring.
    - Отсутствует логирование ошибок.
    - Используются `requests` вместо `StreamSession` в методе `get_models`.
    - Некоторые переменные не имеют аннотации типов.
    - Не везде используется `logger` из `src.logger`.
    - Присутствуют закомментированные участки кода, которые стоит удалить или доработать.

**Рекомендации по улучшению:**

1.  **Документация**:
    *   Добавить подробные docstring для всех функций и методов, включая описание параметров, возвращаемых значений и возможных исключений.
    *   Перевести существующие docstring на русский язык.
    *   Описать внутреннюю функцию `calculate_lenght` в `create_async_generator`.

2.  **Логирование**:
    *   Добавить логирование с использованием `logger` из `src.logger` для отладки и мониторинга работы класса, особенно в блоках обработки исключений.
    *   Логировать ошибки в методах `get_models`, `get_mapping` и `create_async_generator`.

3.  **Использование `StreamSession`**:
    *   Рассмотреть возможность использования `StreamSession` вместо `requests` в методе `get_models` для единообразия и потенциальной оптимизации.

4.  **Аннотации типов**:
    *   Добавить аннотации типов для всех переменных, где они отсутствуют.

5.  **Обработка исключений**:
    *   Улучшить обработку исключений, добавив логирование ошибок с использованием `logger.error` и передачей информации об исключении (`ex`, `exc_info=True`).

6.  **Удаление/Доработка закомментированного кода**:
    *   Удалить неиспользуемый закомментированный код или доработать его и добавить в функциональность, если это необходимо.

7.  **Использовать одинарные кавычки**:
    *   Заменить двойные кавычки на одинарные везде, где это возможно.

**Оптимизированный код:**

```python
from __future__ import annotations

import requests

from ...providers.types import Messages
from ...typing import MediaListType
from ...requests import StreamSession, raise_for_status
from ...errors import ModelNotSupportedError, PaymentRequiredError
from ...providers.response import ProviderInfo
from ..template.OpenaiTemplate import OpenaiTemplate
from .models import model_aliases, vision_models, default_llama_model, default_vision_model, text_models
from src.logger import logger  # Import logger


class HuggingFaceAPI(OpenaiTemplate):
    """
    Модуль для взаимодействия с Hugging Face API для генерации текста.
    =================================================================

    Предоставляет класс :class:`HuggingFaceAPI`, который наследуется от :class:`OpenaiTemplate`
    и реализует методы для получения моделей, создания асинхронного генератора и т.д.

    Пример использования:
    ----------------------

    >>> api = HuggingFaceAPI()
    >>> models = api.get_models()
    >>> print(models)
    """
    label: str = 'HuggingFace (Text Generation)'
    parent: str = 'HuggingFace'
    url: str = 'https://api-inference.huggingface.com'
    api_base: str = 'https://api-inference.huggingface.co/v1'
    working: bool = True
    needs_auth: bool = True

    default_model: str = default_llama_model
    default_vision_model: str = default_vision_model
    vision_models: list[str] = vision_models
    model_aliases: dict[str, str] = model_aliases
    fallback_models: list[str] = text_models + vision_models

    provider_mapping: dict[str, dict] = {
        'google/gemma-3-27b-it': {
            'hf-inference/models/google/gemma-3-27b-it': {
                'task': 'conversational',
                'providerId': 'google/gemma-3-27b-it'}}}

    @classmethod
    def get_model(cls, model: str, **kwargs) -> str:
        """
        Получает имя модели. Если модель не поддерживается, возвращает исходное имя модели.

        Args:
            model (str): Имя модели.
            **kwargs: Дополнительные аргументы.

        Returns:
            str: Имя модели.

        Raises:
            ModelNotSupportedError: Если модель не поддерживается.
        """
        try:
            return super().get_model(model, **kwargs)
        except ModelNotSupportedError:
            return model

    @classmethod
    def get_models(cls, **kwargs) -> list[str]:
        """
        Получает список доступных моделей из Hugging Face API.

        Args:
            **kwargs: Дополнительные аргументы.

        Returns:
            list[str]: Список доступных моделей.
        """
        if not cls.models:
            url: str = 'https://huggingface.co/api/models?inference=warm&&expand[]=inferenceProviderMapping'
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                cls.models = [
                    model['id']
                    for model in response.json()
                    if [
                        provider
                        for provider in model.get('inferenceProviderMapping')
                        if provider.get('status') == 'live' and provider.get('task') == 'conversational'
                    ]
                ] + list(cls.provider_mapping.keys())
            except requests.exceptions.RequestException as ex:
                logger.error('Error while fetching models from Hugging Face API', ex, exc_info=True)
                cls.models = cls.fallback_models
        return cls.models

    @classmethod
    async def get_mapping(cls, model: str, api_key: str = None) -> dict:
        """
        Получает mapping для указанной модели.

        Args:
            model (str): Имя модели.
            api_key (str, optional): API ключ. По умолчанию None.

        Returns:
            dict: Mapping для модели.
        """
        if model in cls.provider_mapping:
            return cls.provider_mapping[model]
        async with StreamSession(
            timeout=30,
            headers=cls.get_headers(False, api_key),
        ) as session:
            try:
                async with session.get(f'https://huggingface.co/api/models/{model}?expand[]=inferenceProviderMapping') as response:
                    await raise_for_status(response)
                    model_data: dict = await response.json()
                    cls.provider_mapping[model]: dict = model_data.get('inferenceProviderMapping')
            except Exception as ex:
                logger.error(f'Error while fetching mapping for model: {model}', ex, exc_info=True)
                return {}  # Return an empty dictionary in case of an error
        return cls.provider_mapping[model]

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        api_base: str = None,
        api_key: str = None,
        max_tokens: int = 2048,
        max_inputs_lenght: int = 10000,
        media: MediaListType = None,
        **kwargs
    ):
        """
        Создает асинхронный генератор для взаимодействия с Hugging Face API.

        Args:
            model (str): Имя модели.
            messages (Messages): Список сообщений.
            api_base (str, optional): Базовый URL API. По умолчанию None.
            api_key (str, optional): API ключ. По умолчанию None.
            max_tokens (int, optional): Максимальное количество токенов. По умолчанию 2048.
            max_inputs_lenght (int, optional): Максимальная длина входных данных. По умолчанию 10000.
            media (MediaListType, optional): Список медиафайлов. По умолчанию None.
            **kwargs: Дополнительные аргументы.

        Yields:
            ProviderInfo: Информация о провайдере.

        Raises:
            ModelNotSupportedError: Если модель не поддерживается.
            PaymentRequiredError: Если требуется оплата.
        """
        if not model and media is not None:
            model: str = cls.default_vision_model
        model: str = cls.get_model(model)
        try:
            provider_mapping: dict = await cls.get_mapping(model, api_key)
            if not provider_mapping:
                raise ModelNotSupportedError(f'Model is not supported: {model} in: {cls.__name__}')
            error: Exception | None = None
            for provider_key in provider_mapping:
                api_path: str = provider_key if provider_key == 'novita' else f'{provider_key}/v1'
                api_base: str = f'https://router.huggingface.co/{api_path}'
                task: str = provider_mapping[provider_key]['task']
                if task != 'conversational':
                    raise ModelNotSupportedError(f'Model is not supported: {model} in: {cls.__name__} task: {task}')
                model: str = provider_mapping[provider_key]['providerId']
                yield ProviderInfo(**{**cls.get_dict(), 'label': f'HuggingFace ({provider_key})'})

            # start = calculate_lenght(messages)
            # if start > max_inputs_lenght:
            #     if len(messages) > 6:
            #         messages = messages[:3] + messages[-3:]
            #     if calculate_lenght(messages) > max_inputs_lenght:
            #         last_user_message = [{'role': 'user', 'content': get_last_user_message(messages)}]
            #         if len(messages) > 2:
            #             messages = [m for m in messages if m['role'] == 'system'] + last_user_message
            #         if len(messages) > 1 and calculate_lenght(messages) > max_inputs_lenght:
            #             messages = last_user_message
            #     debug.log(f'Messages trimmed from: {start} to: {calculate_lenght(messages)}')
            try:
                async for chunk in super().create_async_generator(model, messages, api_base=api_base, api_key=api_key, max_tokens=max_tokens, media=media, **kwargs):
                    yield chunk
                return
            except PaymentRequiredError as ex:
                error: Exception | None = ex
                continue
        except Exception as ex:
            logger.error(f'Error while creating async generator for model: {model}', ex, exc_info=True)
        if error is not None:
            raise error

def calculate_lenght(messages: Messages) -> int:
    """
    Вычисляет длину сообщений.

    Args:
        messages (Messages): Список сообщений.

    Returns:
        int: Суммарная длина сообщений.
    """
    return sum([len(message['content']) + 16 for message in messages])