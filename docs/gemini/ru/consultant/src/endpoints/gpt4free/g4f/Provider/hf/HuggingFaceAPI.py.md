### **Анализ кода модуля `HuggingFaceAPI.py`**

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Использование `StreamSession` для асинхронных запросов.
    - Наличие обработки ошибок с `raise_for_status`.
    - Реализация `fallback_models` для случаев, когда не удается получить список моделей с API.
- **Минусы**:
    - Отсутствие логирования.
    - Смешивание логики получения списка моделей и обработки `provider_mapping`.
    - Использование `requests` вместо `StreamSession` в методе `get_models`.
    - Не все переменные аннотированы типами.

**Рекомендации по улучшению:**

1.  **Добавить логирование**:
    - Добавить логирование с использованием модуля `logger` из `src.logger` для отслеживания ошибок и предупреждений.

2.  **Разделить логику получения списка моделей и обработки `provider_mapping`**:
    - Разделить метод `get_models` на две отдельные функции для улучшения читаемости и поддержки кода.

3.  **Использовать `StreamSession` вместо `requests` в методе `get_models`**:
    - Заменить `requests` на `StreamSession` для единообразия и улучшения производительности.

4.  **Добавить аннотации типов**:
    - Добавить аннотации типов для всех переменных, где это необходимо.

5.  **Улучшить обработку ошибок**:
    - Добавить более конкретную обработку ошибок, чтобы избежать перехвата всех исключений в блоке `except`.

**Оптимизированный код:**

```python
from __future__ import annotations

import requests
from typing import Optional, List, Dict, Any, AsyncGenerator

from ...providers.types import Messages
from ...typing import MediaListType
from ...requests import StreamSession, raise_for_status
from ...errors import ModelNotSupportedError, PaymentRequiredError
from ...providers.response import ProviderInfo
from ..template.OpenaiTemplate import OpenaiTemplate
from .models import model_aliases, vision_models, default_llama_model, default_vision_model, text_models
from src.logger import logger


class HuggingFaceAPI(OpenaiTemplate):
    """
    Класс для взаимодействия с API Hugging Face для генерации текста.
    Наследуется от OpenaiTemplate.
    """
    label: str = 'HuggingFace (Text Generation)'
    parent: str = 'HuggingFace'
    url: str = 'https://api-inference.huggingface.com'
    api_base: str = 'https://api-inference.huggingface.co/v1'
    working: bool = True
    needs_auth: bool = True

    default_model: str = default_llama_model
    default_vision_model: str = default_vision_model
    vision_models: List[str] = vision_models
    model_aliases: Dict[str, str] = model_aliases
    fallback_models: List[str] = text_models + vision_models

    provider_mapping: Dict[str, Dict[str, Dict[str, str]]] = {
        'google/gemma-3-27b-it': {
            'hf-inference/models/google/gemma-3-27b-it': {
                'task': 'conversational',
                'providerId': 'google/gemma-3-27b-it'}}}

    @classmethod
    def get_model(cls, model: str, **kwargs) -> str:
        """
        Возвращает модель. Если модель не поддерживается, возвращает исходную модель.

        Args:
            model (str): Название модели.
            **kwargs: Дополнительные аргументы.

        Returns:
            str: Название модели.

        Raises:
            ModelNotSupportedError: Если модель не поддерживается.
        """
        try:
            return super().get_model(model, **kwargs)
        except ModelNotSupportedError:
            return model

    @classmethod
    def _fetch_models_from_api(cls) -> List[str]:
        """
        Получает список моделей с API Hugging Face.

        Returns:
            List[str]: Список идентификаторов моделей.
        """
        url: str = 'https://huggingface.co/api/models?inference=warm&&expand[]=inferenceProviderMapping'
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверка на HTTP ошибки

            models: List[str] = [
                model['id']
                for model in response.json()
                if [
                    provider
                    for provider in model.get('inferenceProviderMapping', [])
                    if provider.get('status') == 'live' and provider.get('task') == 'conversational'
                ]
            ]
            return models
        except requests.exceptions.RequestException as ex:
            logger.error('Ошибка при получении списка моделей с API Hugging Face', ex, exc_info=True)
            return []

    @classmethod
    def get_models(cls, **kwargs) -> List[str]:
        """
        Возвращает список доступных моделей.

        Args:
            **kwargs: Дополнительные аргументы.

        Returns:
            List[str]: Список доступных моделей.
        """
        if not cls.models:
            api_models: List[str] = cls._fetch_models_from_api()
            cls.models: List[str] = api_models + list(cls.provider_mapping.keys())
        return cls.models

    @classmethod
    async def get_mapping(cls, model: str, api_key: Optional[str] = None) -> Dict[str, Dict[str, str]]:
        """
        Получает mapping для указанной модели.

        Args:
            model (str): Название модели.
            api_key (Optional[str]): API ключ. По умолчанию None.

        Returns:
            Dict[str, Dict[str, str]]: Mapping для модели.
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
                    model_data: Dict[str, Any] = await response.json()
                    cls.provider_mapping[model]: Dict[str, Dict[str, str]] = model_data.get('inferenceProviderMapping', {})
                    return cls.provider_mapping[model]
            except Exception as ex:
                logger.error(f'Ошибка при получении mapping для модели {model}', ex, exc_info=True)
                return {}

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        api_base: Optional[str] = None,
        api_key: Optional[str] = None,
        max_tokens: int = 2048,
        max_inputs_lenght: int = 10000,
        media: Optional[MediaListType] = None,
        **kwargs
    ) -> AsyncGenerator[ProviderInfo | str, None]:
        """
        Создает асинхронный генератор для получения ответов от API Hugging Face.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений.
            api_base (Optional[str]): Базовый URL API. По умолчанию None.
            api_key (Optional[str]): API ключ. По умолчанию None.
            max_tokens (int): Максимальное количество токенов в ответе.
            max_inputs_lenght (int): Максимальная длина входных данных.
            media (Optional[MediaListType]): Список медиафайлов. По умолчанию None.
            **kwargs: Дополнительные аргументы.

        Yields:
            AsyncGenerator[ProviderInfo | str, None]: Асинхронный генератор, возвращающий ProviderInfo или текст ответа.

        Raises:
            ModelNotSupportedError: Если модель не поддерживается.
            PaymentRequiredError: Если требуется оплата.
        """
        if not model and media is not None:
            model: str = cls.default_vision_model
        model: str = cls.get_model(model)
        provider_mapping: Dict[str, Dict[str, str]] = await cls.get_mapping(model, api_key)

        if not provider_mapping:
            raise ModelNotSupportedError(f'Model is not supported: {model} in: {cls.__name__}')

        error: Optional[Exception] = None
        for provider_key in provider_mapping:
            api_path: str = provider_key if provider_key == 'novita' else f'{provider_key}/v1'
            api_base: str = f'https://router.huggingface.co/{api_path}'
            task: str = provider_mapping[provider_key]['task']
            if task != 'conversational':
                raise ModelNotSupportedError(f'Model is not supported: {model} in: {cls.__name__} task: {task}')
            model: str = provider_mapping[provider_key]['providerId']
            yield ProviderInfo(**{**cls.get_dict(), 'label': f'HuggingFace ({provider_key})'})

            try:
                async for chunk in super().create_async_generator(model, messages, api_base=api_base, api_key=api_key, max_tokens=max_tokens, media=media, **kwargs):
                    yield chunk
                return
            except PaymentRequiredError as ex:
                error: Exception = ex
                continue

        if error is not None:
            raise error


def calculate_lenght(messages: Messages) -> int:
    """
    Вычисляет общую длину сообщений.

    Args:
        messages (Messages): Список сообщений.

    Returns:
        int: Общая длина сообщений.
    """
    return sum([len(message['content']) + 16 for message in messages])