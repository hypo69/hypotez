# Модуль Ylokh
## Обзор
Модуль содержит класс `Ylokh`, который реализует асинхронный генератор ответов от модели GPT-3.5-turbo с помощью API `Ylokh`. 
Данный класс наследует от `AsyncGeneratorProvider`.

## Подробности
- `Ylokh` использует API `Ylokh` для получения ответов от модели GPT-3.5-turbo
- Поддерживает как потоковые ответы (с использованием `stream=True`), так и полные ответы.
- Имеет встроенную поддержку истории сообщений (`supports_message_history = True`).
- Использует `StreamSession` для асинхронного взаимодействия с API.
- Логирует ошибки с использованием `logger` из `src.logger`.

## Классы
### `Ylokh`
**Описание**: Класс `Ylokh`  реализует асинхронный генератор ответов от модели GPT-3.5-turbo с помощью API `Ylokh`. 
**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL-адрес API `Ylokh`.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели GPT-3.5-turbo.

**Методы**:
- `create_async_generator()`: Асинхронный метод, который создает генератор ответов от модели GPT-3.5-turbo. 

## Методы класса
### `create_async_generator`
```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool = True,
        proxy: str = None,
        timeout: int = 120,
        **kwargs
    ) -> AsyncResult:
        model = model if model else "gpt-3.5-turbo"
        headers = {"Origin": cls.url, "Referer": f"{cls.url}/"}
        data = {
            "messages": messages,
            "model": model,
            "temperature": 1,
            "presence_penalty": 0,
            "top_p": 1,
            "frequency_penalty": 0,
            "allow_fallback": True,
            "stream": stream,
            **kwargs
        }
        async with StreamSession(
                headers=headers,
                proxies={"https": proxy},
                timeout=timeout
            ) as session:
            async with session.post("https://chatapi.ylokh.xyz/v1/chat/completions", json=data) as response:
                response.raise_for_status()
                if stream:
                    async for line in response.iter_lines():
                        line = line.decode()
                        if line.startswith("data: "):
                            if line.startswith("data: [DONE]"):
                                break
                            line = json.loads(line[6:])
                            content = line["choices"][0]["delta"].get("content")
                            if content:
                                yield content
                else:
                    chat = await response.json()
                    yield chat["choices"][0]["message"].get("content")
```

**Назначение**: Метод создает асинхронный генератор ответов от модели GPT-3.5-turbo.

**Параметры**:
- `model` (str): Имя модели. По умолчанию используется `gpt-3.5-turbo`.
- `messages` (Messages): Список сообщений для отправки в модель.
- `stream` (bool): Флаг, указывающий на использование потокового режима. По умолчанию `True`.
- `proxy` (str): URL-адрес прокси-сервера.
- `timeout` (int): Таймаут в секундах.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор ответов от модели.

**Как работает функция**:
- Метод формирует запрос к API `Ylokh` с использованием предоставленных параметров.
- В случае потокового режима (`stream=True`) метод читает данные из ответа по частям и генерирует текст по мере его получения.
- В противном случае метод ожидает полный ответ и затем генерирует текст из него.

**Примеры**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Ylokh import Ylokh
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {"role": "user", "content": "Привет, как дела?"},
    {"role": "assistant", "content": "Хорошо, спасибо за вопрос. А у тебя как?"},
    {"role": "user", "content": "Тоже хорошо."},
]
async for text in Ylokh.create_async_generator(messages=messages):
    print(text)
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Ylokh import Ylokh
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {"role": "user", "content": "Привет, как дела?"},
    {"role": "assistant", "content": "Хорошо, спасибо за вопрос. А у тебя как?"},
    {"role": "user", "content": "Тоже хорошо."},
]
text = await Ylokh.create_async_generator(messages=messages, stream=False)
print(text)