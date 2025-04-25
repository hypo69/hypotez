# Модуль Replicate

## Обзор

Модуль `Replicate` предоставляет класс `Replicate` для работы с моделью Replicate в качестве провайдера для асинхронной генерации текста. 

## Подробней

Класс `Replicate` реализует асинхронный генератор текста, используя модель Replicate. 
Он наследует от `AsyncGeneratorProvider` и `ProviderModelMixin`, что позволяет использовать его как провайдера для асинхронной генерации текста, а также определяет модели, с которыми он работает. 
В дополнение к стандартным параметрам, используемым в других провайдерах, `Replicate` требует `api_key` для аутентификации.

## Классы

### `Replicate`

**Описание**: Класс `Replicate` реализует провайдера для асинхронной генерации текста, используя модель Replicate.

**Наследует**:
    - `AsyncGeneratorProvider`: Базовый класс для асинхронных провайдеров текста.
    - `ProviderModelMixin`: Миксин для управления моделями.

**Атрибуты**:
    - `url` (str): Базовый URL для Replicate.
    - `login_url` (str): URL для входа на Replicate.
    - `working` (bool):  Указывает на доступность провайдера.
    - `needs_auth` (bool): Указывает на необходимость аутентификации.
    - `default_model` (str):  Название модели по умолчанию.
    - `models` (list[str]): Список доступных моделей.

**Методы**:
    - `create_async_generator(model: str, messages: Messages, api_key: str = None, proxy: str = None, timeout: int = 180, system_prompt: str = None, max_tokens: int = None, temperature: float = None, top_p: float = None, top_k: float = None, stop: list = None, extra_data: dict = {}, headers: dict = {"accept": "application/json"}, **kwargs) -> AsyncResult`: 
        - Создает асинхронный генератор текста.
        - **Описание**: Функция `create_async_generator` инициализирует асинхронный генератор текста. Она принимает различные параметры, включая модель, сообщения, `api_key`, прокси, таймаут, системный запрос, максимальное количество токенов, температуру, top_p, top_k, список стоп-слов, дополнительные данные и заголовки. 
        - **Параметры**:
            - `model` (str): Имя модели Replicate.
            - `messages` (Messages): Список сообщений.
            - `api_key` (str): API ключ для доступа к Replicate.
            - `proxy` (str): Прокси для соединения.
            - `timeout` (int): Таймаут запроса.
            - `system_prompt` (str): Системный запрос.
            - `max_tokens` (int): Максимальное количество токенов в ответе.
            - `temperature` (float): Температура генерации.
            - `top_p` (float): Параметр top_p для сэмплирования.
            - `top_k` (float): Параметр top_k для сэмплирования.
            - `stop` (list): Список стоп-слов для генерации.
            - `extra_data` (dict): Дополнительные данные для модели.
            - `headers` (dict): Дополнительные заголовки для запросов.
        - **Возвращает**: 
            - `AsyncResult`: Асинхронный генератор текста.

## Методы класса

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        api_key: str = None,
        proxy: str = None,
        timeout: int = 180,
        system_prompt: str = None,
        max_tokens: int = None,
        temperature: float = None,
        top_p: float = None,
        top_k: float = None,
        stop: list = None,
        extra_data: dict = {},
        headers: dict = {
            "accept": "application/json",
        },
        **kwargs
    ) -> AsyncResult:
        model = cls.get_model(model)
        if cls.needs_auth and api_key is None:
            raise MissingAuthError("api_key is missing")
        if api_key is not None:
            headers["Authorization"] = f"Bearer {api_key}"
            api_base = "https://api.replicate.com/v1/models/"
        else:
            api_base = "https://replicate.com/api/models/"
        async with StreamSession(
            proxy=proxy,
            headers=headers,
            timeout=timeout
        ) as session:
            data = {
                "stream": True,
                "input": {
                    "prompt": format_prompt(messages),
                    **filter_none(
                        system_prompt=system_prompt,
                        max_new_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p,
                        top_k=top_k,
                        stop_sequences=",".join(stop) if stop else None
                    ),
                    **extra_data
                },
            }
            url = f"{api_base.rstrip('/')}/{model}/predictions"
            async with session.post(url, json=data) as response:
                message = "Model not found" if response.status == 404 else None
                await raise_for_status(response, message)
                result = await response.json()
                if "id" not in result:
                    raise ResponseError(f"Invalid response: {result}")
                async with session.get(result["urls"]["stream"], headers={"Accept": "text/event-stream"}) as response:
                    await raise_for_status(response)
                    event = None
                    async for line in response.iter_lines():
                        if line.startswith(b"event: "):
                            event = line[7:]
                            if event == b"done":
                                break
                        elif event == b"output":
                            if line.startswith(b"data: "):
                                new_text = line[6:].decode()
                                if new_text:
                                    yield new_text
                                else:
                                    yield "\n"
```

**Описание**: Функция `create_async_generator` инициализирует асинхронный генератор текста. Она принимает различные параметры, включая модель, сообщения, `api_key`, прокси, таймаут, системный запрос, максимальное количество токенов, температуру, top_p, top_k, список стоп-слов, дополнительные данные и заголовки. 
**Параметры**:
    - `model` (str): Имя модели Replicate.
    - `messages` (Messages): Список сообщений.
    - `api_key` (str): API ключ для доступа к Replicate.
    - `proxy` (str): Прокси для соединения.
    - `timeout` (int): Таймаут запроса.
    - `system_prompt` (str): Системный запрос.
    - `max_tokens` (int): Максимальное количество токенов в ответе.
    - `temperature` (float): Температура генерации.
    - `top_p` (float): Параметр top_p для сэмплирования.
    - `top_k` (float): Параметр top_k для сэмплирования.
    - `stop` (list): Список стоп-слов для генерации.
    - `extra_data` (dict): Дополнительные данные для модели.
    - `headers` (dict): Дополнительные заголовки для запросов.
**Возвращает**: 
    - `AsyncResult`: Асинхронный генератор текста.
**Как работает функция**:

- Проверяет наличие `api_key` и устанавливает заголовок авторизации, если он есть.
- Формирует URL для запроса к Replicate.
- Отправляет POST запрос на получение прогноза от модели Replicate.
- Парсит ответ и возвращает асинхронный генератор текста, который выдает текст по частям.

**Пример**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Replicate import Replicate

async def main():
    api_key = "your_api_key"  # Замените на ваш API ключ
    model = "meta/meta-llama-3-70b-instruct"
    messages = [
        {"role": "user", "content": "Привет!"},
    ]
    generator = await Replicate.create_async_generator(
        model=model,
        messages=messages,
        api_key=api_key,
    )
    async for text_chunk in generator:
        print(text_chunk, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())