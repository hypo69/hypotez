# Модуль FakeGpt
## Обзор
Модуль предоставляет класс `FakeGpt`, который эмулирует работу с GPT-моделями, предоставляя возможность отправки запросов к фейковому API и получения синтезированных ответов. 
## Подробнее
Этот модуль используется для тестирования и разработки, позволяя эмулировать поведение реальной системы без необходимости подключения к реальному API. `FakeGpt` - это класс, наследующий `AsyncGeneratorProvider`. Он использует фейковый API для отправки запросов и получения синтезированных ответов. Этот подход позволяет разработчикам тестировать код, полагающийся на API GPT-модели, без зависимости от реальной инфраструктуры.
## Классы
### `class FakeGpt`
**Описание**: Класс `FakeGpt` предоставляет методы для эмуляции взаимодействия с GPT-моделями.
**Наследует**:  `AsyncGeneratorProvider` 
**Атрибуты**: 
- `url`: URL фейкового API, к которому отправляются запросы.
- `supports_gpt_35_turbo`: Флаг, указывающий на то, поддерживает ли эта модель GPT-3.5 Turbo.
- `working`: Флаг, указывающий на то, является ли этот провайдер доступным.
- `_access_token`: Токен доступа к фейковому API.
- `_cookie_jar`: Cookie-jar для сеансов с фейковым API.
**Методы**:
- `create_async_generator()`: Асинхронный метод для создания генератора ответов.
## Методы класса
### `create_async_generator()`
```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """ Асинхронный метод для создания генератора ответов.
        Args:
            model (str): Имя модели GPT, которую эмулирует этот провайдер.
            messages (Messages): Список сообщений, отправляемых в модель.
            proxy (str, optional): Прокси-сервер для подключения к API. По умолчанию `None`.
        Returns:
            AsyncResult: Асинхронный результат, представляющий собой генератор ответов.
        """
        headers = {
            "Accept-Language": "en-US",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Referer": "https://chat-shared2.zhile.io/?v=2",
            "sec-ch-ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-platform": '"Linux"',
            "sec-ch-ua-mobile": "?0",
        }
        async with ClientSession(headers=headers, cookie_jar=cls._cookie_jar) as session:
            if not cls._access_token:
                async with session.get(f"{cls.url}/api/loads", params={"t": int(time.time())}, proxy=proxy) as response:
                    response.raise_for_status()
                    list = (await response.json())["loads"]
                    token_ids = [t["token_id"] for t in list]
                data = {
                    "token_key": random.choice(token_ids),
                    "session_password": get_random_string()
                }
                async with session.post(f"{cls.url}/auth/login", data=data, proxy=proxy) as response:
                    response.raise_for_status()
                async with session.get(f"{cls.url}/api/auth/session", proxy=proxy) as response:
                    response.raise_for_status()
                    cls._access_token = (await response.json())["accessToken"]
                    cls._cookie_jar = session.cookie_jar
            headers = {
                "Content-Type": "application/json",
                "Accept": "text/event-stream",
                "X-Authorization": f"Bearer {cls._access_token}",
            }
            prompt = format_prompt(messages)
            data = {
                "action": "next",
                "messages": [
                    {
                        "id": str(uuid.uuid4()),
                        "author": {"role": "user"},
                        "content": {"content_type": "text", "parts": [prompt]},
                        "metadata": {},
                    }
                ],
                "parent_message_id": str(uuid.uuid4()),
                "model": "text-davinci-002-render-sha",
                "plugin_ids": [],
                "timezone_offset_min": -120,
                "suggestions": [],
                "history_and_training_disabled": True,
                "arkose_token": "",
                "force_paragen": False,
            }
            last_message = ""
            async with session.post(f"{cls.url}/api/conversation", json=data, headers=headers, proxy=proxy) as response:
                async for line in response.content:
                    if line.startswith(b"data: "):
                        line = line[6:]
                        if line == b"[DONE]":
                            break
                        try:
                            line = json.loads(line)
                            if line["message"]["metadata"]["message_type"] == "next":
                                new_message = line["message"]["content"]["parts"][0]
                                yield new_message[len(last_message):]
                                last_message = new_message
                        except:
                            continue
            if not last_message:
                raise RuntimeError("No valid response")
```
**Назначение**: Метод создает асинхронный генератор ответов, которые эмулируют ответы GPT-модели. 
**Параметры**: 
- `model` (str): Имя модели GPT, которую эмулирует этот провайдер.
- `messages` (Messages): Список сообщений, отправляемых в модель.
- `proxy` (str, optional): Прокси-сервер для подключения к API. По умолчанию `None`.
**Возвращает**: 
- `AsyncResult`: Асинхронный результат, представляющий собой генератор ответов.
**Как работает функция**:
- Метод создает HTTP-сессию с помощью `aiohttp.ClientSession`.
- Если `_access_token` не установлен, он отправляет запрос к фейковому API для получения токена доступа и записывает его в `_access_token`.
- Он отправляет запрос к API с заданным `prompt` и `messages`.
- Он обрабатывает ответ, получая информацию о новых сообщениях и возвращая их как генератор. 
**Примеры**: 
```python
# Пример использования метода create_async_generator
from ...typing import Messages

messages: Messages = [
  {
    "id": str(uuid.uuid4()),
    "author": {"role": "user"},
    "content": {"content_type": "text", "parts": ["Привет, как дела?"]},
    "metadata": {},
  },
]
async_result = await FakeGpt.create_async_generator(model="text-davinci-002-render-sha", messages=messages)
# Получение ответов от генератора
async for response in async_result:
  print(response)