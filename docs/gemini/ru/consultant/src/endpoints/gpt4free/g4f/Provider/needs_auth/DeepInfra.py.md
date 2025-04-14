### **Анализ кода модуля `DeepInfra.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код достаточно хорошо структурирован и следует основным принципам ООП.
  - Используются асинхронные функции, что хорошо для неблокирующего выполнения операций.
  - Есть обработка ошибок через `raise_for_status`.
  - Класс наследуется от `OpenaiTemplate`, что предполагает использование общих шаблонов.
- **Минусы**:
  - Отсутствует полная документация. Многие методы и классы не имеют docstring.
  - Magic values в коде (например, User-Agent, версии Chrome).
  - Не используется модуль `logger` для логирования ошибок и важной информации.
  - Нет аннотаций типов для параметров и возвращаемых значений функций, что снижает читаемость и поддерживаемость кода.

#### **Рекомендации по улучшению**:
1. **Добавить docstring для всех классов и методов**:
   - Описать назначение каждого метода, принимаемые аргументы и возвращаемые значения.
   - Указать, какие исключения могут быть выброшены.

2. **Использовать `logger` для логирования**:
   - Заменить `print` на `logger.info`, `logger.warning`, `logger.error` в зависимости от ситуации.
   - Логировать важные этапы выполнения программы и ошибки.

3. **Удалить Magic values**:
   - Заменить константы User-Agent и версии Chrome переменными или константами, чтобы их было легче поддерживать.

4. **Добавить аннотации типов**:
   -  Указывать типы аргументов и возвращаемых значений для всех функций и методов.

5. **Улучшить обработку ошибок**:
   - Добавить более конкретные исключения и их обработку.
   - Логировать ошибки с использованием `logger.error` и передавать информацию об исключении.

6. **Обновить комментарии**:
   - Убедиться, что комментарии актуальны и соответствуют коду.
   - Добавить комментарии, где это необходимо, чтобы объяснить сложные участки кода.

7. **Изменить способ получения моделей**:
   - Сделать получение моделей более надежным и отказоустойчивым.
   - Добавить обработку ошибок при запросе моделей.
   - Кэшировать модели с использованием `@functools.lru_cache`.

#### **Оптимизированный код**:

```python
"""
Модуль для взаимодействия с DeepInfra API
===========================================

Модуль содержит класс :class:`DeepInfra`, который используется для взаимодействия с API DeepInfra
для получения моделей и генерации текста и изображений.
"""
from __future__ import annotations

import functools
import requests
from typing import AsyncGenerator, Optional, List, Dict, Any

from src.logger import logger  # Import logger
from ...typing import AsyncResult, Messages
from ...requests import StreamSession, raise_for_status
from ...providers.response import ImageResponse
from ..template import OpenaiTemplate
from ..helper import format_image_prompt


class DeepInfra(OpenaiTemplate):
    """
    Класс для взаимодействия с DeepInfra API.
    """
    url: str = 'https://deepinfra.com'
    login_url: str = 'https://deepinfra.com/dash/api_keys'
    api_base: str = 'https://api.deepinfra.com/v1/openai'
    working: bool = True
    needs_auth: bool = True

    default_model: str = 'meta-llama/Meta-Llama-3.1-70B-Instruct'
    default_image_model: str = 'stabilityai/sd3.5'

    @classmethod
    @functools.lru_cache(maxsize=1)
    def get_models(cls, **kwargs: Any) -> List[str]:
        """
        Получает список доступных моделей из DeepInfra API.

        Args:
            **kwargs (Any): Дополнительные аргументы.

        Returns:
            List[str]: Список имен моделей.
        """
        if not cls.models:
            url: str = 'https://api.deepinfra.com/models/featured'
            try:
                response = requests.get(url)
                response.raise_for_status()  # Проверка на HTTP ошибки
                models: List[Dict[str, Any]] = response.json()

                cls.models: List[str] = []
                cls.image_models: List[str] = []

                for model in models:
                    if model['type'] == 'text-generation':
                        cls.models.append(model['model_name'])
                    elif model['reported_type'] == 'text-to-image':
                        cls.image_models.append(model['model_name'])

                cls.models.extend(cls.image_models)
            except requests.exceptions.RequestException as ex:
                logger.error(f'Error while fetching models from DeepInfra: {ex}', exc_info=True)
                return []  # Возвращаем пустой список в случае ошибки

        return cls.models

    @classmethod
    @functools.lru_cache(maxsize=1)
    def get_image_models(cls, **kwargs: Any) -> List[str]:
        """
        Получает список доступных моделей для генерации изображений из DeepInfra API.

        Args:
            **kwargs (Any): Дополнительные аргументы.

        Returns:
            List[str]: Список имен моделей для генерации изображений.
        """
        if not cls.image_models:
            cls.get_models()
        return cls.image_models

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool,
        prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1028,
        **kwargs: Any
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для получения текста или изображения от DeepInfra API.

        Args:
            model (str): Имя модели.
            messages (Messages): Список сообщений для отправки.
            stream (bool): Флаг стриминга.
            prompt (Optional[str]): Дополнительный промпт.
            temperature (float): Температура для генерации.
            max_tokens (int): Максимальное количество токенов.
            **kwargs (Any): Дополнительные аргументы.

        Yields:
            AsyncResult: Части ответа от API.
        """
        if model in cls.get_image_models():
            yield cls.create_async_image(
                format_image_prompt(messages, prompt),
                model,
                **kwargs
            )
            return

        headers: Dict[str, str] = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US',
            'Origin': 'https://deepinfra.com',
            'Referer': 'https://deepinfra.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',  # todo: вынести в константы
            'X-Deepinfra-Source': 'web-embed',
        }
        async for chunk in super().create_async_generator(
            model, messages,
            stream=stream,
            temperature=temperature,
            max_tokens=max_tokens,
            headers=headers,
            **kwargs
        ):
            yield chunk

    @classmethod
    async def create_async_image(
        cls,
        prompt: str,
        model: str,
        api_key: Optional[str] = None,
        api_base: str = 'https://api.deepinfra.com/v1/inference',
        proxy: Optional[str] = None,
        timeout: int = 180,
        extra_data: Dict[str, Any] = {},
        **kwargs: Any
    ) -> ImageResponse:
        """
        Создает асинхронный запрос для генерации изображения от DeepInfra API.

        Args:
            prompt (str): Промпт для генерации изображения.
            model (str): Имя модели.
            api_key (Optional[str]): API ключ.
            api_base (str): Базовый URL API.
            proxy (Optional[str]): Прокси сервер.
            timeout (int): Время ожидания.
            extra_data (Dict[str, Any]): Дополнительные данные.
            **kwargs (Any): Дополнительные аргументы.

        Returns:
            ImageResponse: Объект с изображением и промптом.
        """
        headers: Dict[str, str] = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US',
            'Connection': 'keep-alive',
            'Origin': 'https://deepinfra.com',
            'Referer': 'https://deepinfra.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36', # todo: вынести в константы
            'X-Deepinfra-Source': 'web-embed',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',  # todo: вынести в константы
            'sec-ch-ua-mobile': '?0', # todo: вынести в константы
            'sec-ch-ua-platform': '"macOS"', # todo: вынести в константы
        }
        if api_key is not None:
            headers['Authorization'] = f'Bearer {api_key}'
        async with StreamSession(
            proxies={'all': proxy},
            headers=headers,
            timeout=timeout
        ) as session:
            model = cls.get_model(model)
            data: Dict[str, Any] = {'prompt': prompt, **extra_data}
            data = {'input': data} if model == cls.default_model else data
            try:
                async with session.post(f"{api_base.rstrip('/')}/{model}", json=data) as response:
                    await raise_for_status(response)
                    data = await response.json()
                    images = data.get('output', data.get('images', data.get('image_url')))
                    if not images:
                        raise RuntimeError(f'Response: {data}')
                    images = images[0] if len(images) == 1 else images
                    return ImageResponse(images, prompt)
            except Exception as ex:
                logger.error(f'Error while generating image: {ex}', exc_info=True)
                raise  # Перебрасываем исключение после логирования