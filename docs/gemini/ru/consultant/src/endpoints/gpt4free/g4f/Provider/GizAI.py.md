### **Анализ кода модуля `GizAI`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Класс хорошо структурирован и следует принципам наследования.
  - Четкое разделение ответственности между методами.
  - Использование асинхронных операций для неблокирующего выполнения.
- **Минусы**:
  - Отсутствует документация класса и методов.
  - Жёстко заданы заголовки, что может затруднить адаптацию к изменениям API.
  - Не все переменные аннотированы типами.

#### **Рекомендации по улучшению**:

1. **Добавить документацию**:
   - Добавить docstring для класса `GizAI` с описанием его назначения, основных атрибутов и методов.
   - Добавить docstring для каждого метода, включая описание параметров, возвращаемых значений и возможных исключений.

2. **Улучшить обработку ошибок**:
   - Логировать ошибки с использованием `logger.error` из модуля `src.logger`.
   - Предоставить более конкретные сообщения об ошибках, чтобы облегчить отладку.

3. **Типизация**:
   - Указать типы для всех переменных, чтобы улучшить читаемость и предотвратить ошибки.

4. **Рефакторинг заголовков**:
   - Вынести заголовки в отдельную константу или переменную, чтобы упростить их изменение и поддержку.
   - Рассмотреть возможность использования библиотеки для управления заголовками, чтобы избежать дублирования.

5. **Добавить обработку прокси**:
   - Учесть возможность передачи прокси через аргументы, чтобы повысить гибкость использования.

6. **Улучшить структуру данных**:
   - Использовать более явные структуры данных для представления запросов и ответов API.

#### **Оптимизированный код**:

```python
from __future__ import annotations

from aiohttp import ClientSession
from typing import AsyncGenerator, Dict, Any, Optional

from ..typing import AsyncResult, Messages
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin
from src.logger import logger  # Добавлен импорт logger
from .helper import format_prompt


class GizAI(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Провайдер GizAI для асинхронной генерации текста.
    ====================================================

    Этот класс предоставляет асинхронный интерфейс для взаимодействия с API GizAI.
    Он поддерживает стриминг, системные сообщения и историю сообщений.

    Пример использования:
    ----------------------

    >>> model = 'chat-gemini-flash'
    >>> messages = [{'role': 'user', 'content': 'Hello, GizAI!'}]
    >>> async for message in GizAI.create_async_generator(model=model, messages=messages):
    ...     print(message)
    """
    url: str = "https://app.giz.ai/assistant"
    api_endpoint: str = "https://app.giz.ai/api/data/users/inferenceServer.infer"

    working: bool = True
    supports_stream: bool = False
    supports_system_message: bool = True
    supports_message_history: bool = True

    default_model: str = 'chat-gemini-flash'
    models: list[str] = [default_model]
    model_aliases: dict[str, str] = {"gemini-1.5-flash": "chat-gemini-flash", }

    @classmethod
    def get_model(cls, model: str) -> str:
        """
        Получает имя модели на основе предоставленного алиаса или возвращает модель по умолчанию.

        Args:
            model (str): Имя модели или алиас.

        Returns:
            str: Имя модели.
        """
        if model in cls.models:
            return model
        elif model in cls.model_aliases:
            return cls.model_aliases[model]
        else:
            return cls.default_model

    @classmethod
    async def create_async_generator(
            cls,
            model: str,
            messages: Messages,
            proxy: Optional[str] = None,
            **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с API GizAI.

        Args:
            model (str): Имя модели.
            messages (Messages): Список сообщений для отправки.
            proxy (Optional[str]): Адрес прокси-сервера (необязательный).

        Returns:
            AsyncResult: Асинхронный генератор, выдающий ответы от API.

        Raises:
            Exception: В случае неожиданного статуса ответа от API.
        """
        model = cls.get_model(model)

        headers: dict[str, str] = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'DNT': '1',
            'Origin': 'https://app.giz.ai',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not?A_Brand";v="99", "Chromium";v="130"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"'
        }

        async with ClientSession(headers=headers) as session:
            data: dict[str, Any] = {
                "model": model,
                "input": {
                    "messages": [
                        {"content": message.get("content")}
                        if message.get("role") == "system" else
                        {"type": "human" if message.get("role") == "user" else "ai", "content": message.get("content")}
                        for message in messages
                    ],
                    "mode": "plan"
                },
                "noStream": True
            }
            try:
                async with session.post(cls.api_endpoint, json=data, proxy=proxy) as response:
                    if response.status == 201:
                        result: dict[str, str] = await response.json()
                        yield result['output'].strip()
                    else:
                        raise Exception(f"Unexpected response status: {response.status}\n{await response.text()}")
            except Exception as ex:
                logger.error('Error while processing GizAI request', ex, exc_info=True)
                raise