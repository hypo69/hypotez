# Модуль Jmuz

## Обзор

Модуль `Jmuz` предоставляет реализацию класса `Jmuz`, который  является провайдером доступа к API  [Jmuz](https://jmuz.me/).  Jmuz - это сервис, который предоставляет доступ к различным моделям ИИ, включая GPT-4O, Gemini и другим. 

## Подробнее 

Модуль `Jmuz` использует  `OpenaiTemplate`  в качестве  базового класса и расширяет его для работы с API Jmuz. Класс `Jmuz`  предоставляет методы для  отправки запросов к API  и получения ответов.  

## Классы

### `class Jmuz`

**Описание**:  Класс `Jmuz`  реализует  провайдера доступа к API  [Jmuz](https://jmuz.me/). 

**Наследует**: `OpenaiTemplate`

**Атрибуты**:

- `url` (str):  URL-адрес Discord-сервера Jmuz.
- `api_base` (str):  Базовый URL-адрес API Jmuz.
- `api_key` (str):  Ключ API для доступа к сервису.
- `working` (bool):  Флаг, указывающий, работает ли провайдер.
- `supports_system_message` (bool):  Флаг, указывающий, поддерживает ли  провайдер  системеых сообщений.
- `default_model` (str):  Название модели по умолчанию. 
- `model_aliases` (dict):  Словарь для сопоставления псевдонимов моделей с их реальными названиями. 
- `models` (list):  Список доступных моделей (инициализируется  в методе `get_models`). 

**Методы**:

- `get_models(**kwargs)`:  Получение списка доступных моделей.
- `create_async_generator(model: str, messages: Messages, stream: bool = True, api_key: str = None, **kwargs) -> AsyncResult`:  Асинхронный генератор для получения ответов от модели  Jmuz. 

## Методы класса 

### `get_models(**kwargs)`

```python
    @classmethod
    def get_models(cls, **kwargs):
        if not cls.models:
            cls.models = super().get_models(api_key=cls.api_key, api_base=cls.api_base)
        return cls.models
```

**Описание**:  Метод `get_models`  получает список доступных моделей  от API  Jmuz. 

**Параметры**:

- `kwargs`:  Дополнительные параметры для отправки запроса (не используются в данном методе). 

**Возвращает**:

- `list`:  Список  доступных  моделей. 

**Как работает функция**:

- Метод `get_models`  проверяет,  инициализирован ли  список  моделей  `cls.models`.
- Если  список  не  инициализирован, он  вызывает метод `get_models`  от  базового класса  `OpenaiTemplate`  с  параметрами `api_key`  и  `api_base`  для получения списка моделей от API Jmuz. 
- Метод возвращает список  моделей. 

### `create_async_generator(model: str, messages: Messages, stream: bool = True, api_key: str = None, **kwargs) -> AsyncResult`

```python
    @classmethod
    async def create_async_generator(
            cls,
            model: str,
            messages: Messages,
            stream: bool = True,
            api_key: str = None, # Remove api_key from kwargs
            **kwargs
    ) -> AsyncResult:
        model = cls.get_model(model)
        headers = {
            "Authorization": f"Bearer {cls.api_key}",
            "Content-Type": "application/json",
            "accept": "*/*",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        }

        started = False
        buffer = ""
        async for chunk in super().create_async_generator(
            model=model,
            messages=messages,
            api_base=cls.api_base,
            api_key=cls.api_key,
            stream=cls.supports_stream,
            headers=headers,
            **kwargs
        ):
            if isinstance(chunk, str):
                buffer += chunk
                if "Join for free".startswith(buffer) or buffer.startswith("Join for free"):
                    if buffer.endswith("\\n"):
                        buffer = ""
                    continue
                if "https://discord.gg/".startswith(buffer) or "https://discord.gg/" in buffer:
                    if "..." in buffer:
                        buffer = ""
                    continue
                if "o1-preview".startswith(buffer) or buffer.startswith("o1-preview"):
                    if "\\n" in buffer:
                        buffer = ""
                    continue
                if not started:
                    buffer = buffer.lstrip()
                if buffer:
                    started = True
                    yield buffer
                    buffer = ""
            else:
                yield chunk
```

**Описание**:  Метод `create_async_generator` создает асинхронный генератор, который  отправляет  запросы к API Jmuz и получает  ответы. 

**Параметры**:

- `model` (str):  Название модели, которую необходимо использовать. 
- `messages` (Messages):  Список  сообщений  для отправки  модели. 
- `stream` (bool):  Флаг, указывающий, следует ли  получать  ответ  по частям. 
- `api_key` (str):  Ключ API (не используется, так как  в методе  используется  `cls.api_key`). 
- `kwargs`:  Дополнительные параметры для отправки запроса. 

**Возвращает**:

- `AsyncResult`:  Объект, который  представляет  асинхронный  результат. 

**Как работает функция**:

-  Метод  `create_async_generator`  сначала  получает  название  модели  с  помощью  метода `get_model`. 
-  Затем он создает заголовок HTTP-запроса,  включая  ключ API. 
-  Далее  метод   вызывает   `create_async_generator`  от  базового  класса   `OpenaiTemplate`   для  отправки  запроса  к  API  Jmuz.
-  При  получении  ответа  метод   использует   буфер   `buffer`  для   сборки   кусков   ответа   и   выполняет   очистку   от   ненужных   частей.
-  В  конце  метод   возвращает   `AsyncResult`. 

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Jmuz import Jmuz
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {"role": "user", "content": "Привет!"},
]
async def main():
    response = await Jmuz.create_async_generator(model="gpt-4o", messages=messages)
    async for chunk in response:
        print(chunk)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())