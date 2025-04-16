# Модуль для работы с H2o API (устаревший)

## Обзор

Модуль `H2o.py` предназначен для взаимодействия с API H2o для генерации текста на основе предоставленных сообщений. Он использует асинхронные запросы для обмена данными с сервером H2o. Этот модуль является устаревшим.

## Подробней

Модуль предоставляет класс `H2o`, который является асинхронным генератором. Он отправляет запросы к API H2o и возвращает сгенерированный текст частями. Для работы требуется указание модели, сообщений и прокси (опционально).

## Классы

### `H2o`

**Описание**: Класс `H2o` предоставляет функциональность для взаимодействия с API H2o.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL-адрес API H2o.
- `model` (str): Название модели, используемой для генерации текста.

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для получения сгенерированного текста от API H2o.

## Методы класса

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для получения сгенерированного текста от API H2o.

        Args:
            model (str): Название модели, используемой для генерации текста.
            messages (Messages): Список сообщений для отправки в API.
            proxy (str, optional): URL-адрес прокси-сервера. По умолчанию `None`.
            **kwargs: Дополнительные параметры для передачи в API.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий сгенерированный текст.

        Raises:
            aiohttp.ClientResponseError: Если возникает ошибка при выполнении HTTP-запроса.

        Как работает функция:
        ----------------------

        1.  **Подготовка данных**:
            -   Если `model` не указана, используется значение по умолчанию из атрибута `cls.model`.
            -   Формируются заголовки запроса, включающие Referer.

        2.  **Создание сессии**:
            -   Создается асинхронная сессия `aiohttp.ClientSession` с заданными заголовками.

        3.  **Настройка параметров**:
            -   Отправляется POST-запрос к `/settings` для установки параметров, таких как принятие условий использования, разрешение обмена данными с авторами модели, выбор активной модели и включение поиска.

        4.  **Запуск диалога**:
            -   Отправляется POST-запрос к `/conversation` для начала нового диалога с указанной моделью.
            -   Из ответа извлекается `conversationId`, который будет использоваться в последующих запросах.

        5.  **Генерация текста**:
            -   Формируются данные для запроса, включающие отформатированные сообщения, параметры генерации (температура, максимальное количество токенов и т.д.), а также опции, такие как уникальные идентификаторы запроса.
            -   Отправляется POST-запрос к `/conversation/{conversationId}` с данными для генерации текста.
            -   Полученные данные обрабатываются построчно:
                -   Каждая строка декодируется из UTF-8.
                -   Если строка начинается с `data:`, она преобразуется из JSON.
                -   Если токен не является специальным, он возвращается как часть сгенерированного текста.

        6.  **Завершение диалога**:
            -   После завершения генерации текста отправляется DELETE-запрос к `/conversation/{conversationId}` для удаления диалога.

        Примеры:
        ---------

        ```python
        # Пример использования асинхронного генератора
        import asyncio
        from typing import AsyncGenerator, List, Dict, Any

        from aiohttp import ClientSession

        from ...typing import Messages
        from ..base_provider import format_prompt

        class H2o(AsyncGeneratorProvider):
            url = "https://gpt-gm.h2o.ai"
            model = "h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1"

            @classmethod
            async def create_async_generator(
                cls,
                model: str,
                messages: Messages,
                proxy: str = None,
                **kwargs
            ) -> AsyncGenerator[str, None]:
                model = model if model else cls.model
                headers = {"Referer": f"{cls.url}/"}

                async with ClientSession(headers=headers) as session:
                    data = {
                        "ethicsModalAccepted": "true",
                        "shareConversationsWithModelAuthors": "true",
                        "ethicsModalAcceptedAt": "",
                        "activeModel": model,
                        "searchEnabled": "true",
                    }
                    async with session.post(
                        f"{cls.url}/settings", proxy=proxy, data=data
                    ) as response:
                        response.raise_for_status()

                    async with session.post(
                        f"{cls.url}/conversation", proxy=proxy, json={"model": model}
                    ) as response:
                        response.raise_for_status()
                        conversationId = (await response.json())["conversationId"]

                    data = {
                        "inputs": format_prompt(messages),
                        "parameters": {
                            "temperature": 0.4,
                            "truncate": 2048,
                            "max_new_tokens": 1024,
                            "do_sample": True,
                            "repetition_penalty": 1.2,
                            "return_full_text": False,
                            **kwargs,
                        },
                        "stream": True,
                        "options": {
                            "id": str(uuid.uuid4()),
                            "response_id": str(uuid.uuid4()),
                            "is_retry": False,
                            "use_cache": False,
                            "web_search_id": "",
                        },
                    }
                    async with session.post(
                        f"{cls.url}/conversation/{conversationId}", proxy=proxy, json=data
                    ) as response:
                        start = "data:"
                        async for line in response.content:
                            line = line.decode("utf-8")
                            if line and line.startswith(start):
                                line = json.loads(line[len(start) : -1])
                                if not line["token"]["special"]:
                                    yield line["token"]["text"]

                    async with session.delete(
                        f"{cls.url}/conversation/{conversationId}", proxy=proxy
                    ) as response:
                        response.raise_for_status()

        async def main():
            messages: Messages = [
                {"role": "user", "content": "Напиши стихотворение о весне."}
            ]
            async for token in H2o.create_async_generator(model="h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1", messages=messages):
                print(token, end="", flush=True)

        if __name__ == "__main__":
            asyncio.run(main())
        ```
        """
```

## Параметры класса

- `url` (str): URL-адрес API H2o.
- `model` (str): Название модели, используемой для генерации текста.

## Переменные

- `start` (str): Строка, используемая для определения начала полезных данных в ответе от API.