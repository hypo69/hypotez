# Модуль Pizzagpt

## Обзор

Модуль `Pizzagpt` предоставляет реализацию асинхронного генератора ответов с использованием модели Pizzagpt. 

## Подробности

Модуль импортирует необходимые зависимости, включая `aiohttp` для работы с HTTP-запросами и `typing` для аннотации типов.

## Классы

### `class Pizzagpt`

**Описание**: Класс `Pizzagpt` реализует асинхронный генератор ответов от модели Pizzagpt. 

**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:

- `url` (str): Базовый URL API Pizzagpt.
- `api_endpoint` (str): Эндпоинт API Pizzagpt для генерации текста.
- `working` (bool): Флаг, указывающий на то, работает ли генератор.
- `default_model` (str): Название модели по умолчанию.
- `models` (list): Список доступных моделей.

**Методы**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Асинхронный генератор ответов.

**Принцип работы**:

1. **Инициализация**: Класс `Pizzagpt` создает асинхронный генератор, который работает с API Pizzagpt.
2. **Формирование запроса**: Генератор форматирует список сообщений в виде запроса к API Pizzagpt.
3. **Отправка запроса**: Генератор отправляет запрос к API Pizzagpt с помощью `ClientSession`.
4. **Обработка ответа**: Генератор обрабатывает ответ от API Pizzagpt, извлекая текст ответа и вызывая исключение в случае ошибки.
5. **Итерация**: Генератор итерирует по полученному тексту, выдавая текст и состояние завершения (FinishReason).

### `Метод create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        headers = {
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": cls.url,
            "referer": f"{cls.url}/en",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "x-secret": "Marinara"
        }
        async with ClientSession(headers=headers) as session:
            prompt = format_prompt(messages)
            data = {
                "question": prompt
            }
            async with session.post(f"{cls.url}{cls.api_endpoint}", json=data, proxy=proxy) as response:
                response.raise_for_status()
                response_json = await response.json()
                content = response_json.get("answer", response_json).get("content")
                if content:
                    if "Misuse detected. please get in touch" in content:
                        raise ValueError(content)
                    yield content
                    yield FinishReason("stop")
```

**Назначение**: Асинхронный генератор ответов от модели Pizzagpt.

**Параметры**:

- `model` (str): Название модели.
- `messages` (Messages): Список сообщений, которые будут использованы в качестве входных данных для модели.
- `proxy` (str, optional): Прокси-сервер для использования при отправке запросов. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, передаваемые в API Pizzagpt.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор ответов.

**Вызывает исключения**:

- `ValueError`: Если API Pizzagpt возвращает ошибку.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Pizzagpt import Pizzagpt

async def main():
    async for response in Pizzagpt.create_async_generator(model='gpt-4o-mini', messages=[{'role': 'user', 'content': 'Hello, world!'}], proxy=None):
        print(response)
```

**Как работает функция**:

1. **Инициализация**: Функция создает асинхронный генератор с помощью `ClientSession`.
2. **Формирование запроса**: Функция форматирует список сообщений в виде запроса к API Pizzagpt.
3. **Отправка запроса**: Функция отправляет запрос к API Pizzagpt с помощью `session.post`.
4. **Обработка ответа**: Функция обрабатывает ответ от API Pizzagpt, извлекая текст ответа и вызывая исключение в случае ошибки.
5. **Итерация**: Функция итерирует по полученному тексту, выдавая текст и состояние завершения (FinishReason).

**Примеры**:

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.Pizzagpt import Pizzagpt
>>> async for response in Pizzagpt.create_async_generator(model='gpt-4o-mini', messages=[{'role': 'user', 'content': 'Hello, world!'}], proxy=None):
...     print(response)
Hello, world!
>>> async for response in Pizzagpt.create_async_generator(model='gpt-4o-mini', messages=[{'role': 'user', 'content': 'What is the meaning of life?'}], proxy=None):
...     print(response)
The meaning of life is a question that has been pondered by philosophers and theologians for centuries. There is no one answer that everyone agrees on, but some possible answers include:
- To find happiness and fulfillment.
- To make a difference in the world.
- To learn and grow.
- To connect with others.
- To experience love and beauty.
Ultimately, the meaning of life is up to each individual to decide.