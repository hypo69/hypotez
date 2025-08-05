# Модуль FreeNetfly
## Обзор

Модуль `FreeNetfly` предоставляет реализацию асинхронного генератора для взаимодействия с API `free.netfly.top`, 
предлагающим доступ к моделям GPT-3.5-turbo и GPT-4. 

## Подробнее

Модуль `FreeNetfly` реализует класс `FreeNetfly`, наследующий от `AsyncGeneratorProvider` и `ProviderModelMixin`. 
Он определяет следующие атрибуты:

- `url`: Базовый URL API `free.netfly.top`.
- `api_endpoint`: Путь к API-методу для генерации текста.
- `working`: Флаг, указывающий на доступность API.
- `default_model`: Название модели по умолчанию (gpt-3.5-turbo).
- `models`: Список доступных моделей (gpt-3.5-turbo, gpt-4).


## Классы

### `class FreeNetfly`
**Описание**: Класс `FreeNetfly` реализует асинхронный генератор для взаимодействия с API `free.netfly.top`.

**Наследует**: 
- `AsyncGeneratorProvider`: Базовый класс для асинхронных генераторов.
- `ProviderModelMixin`: Миксин, добавляющий функциональность для работы с моделями.

**Атрибуты**: 
- `url` (str): Базовый URL API `free.netfly.top`.
- `api_endpoint` (str): Путь к API-методу для генерации текста.
- `working` (bool): Флаг, указывающий на доступность API.
- `default_model` (str): Название модели по умолчанию (gpt-3.5-turbo).
- `models` (list): Список доступных моделей (gpt-3.5-turbo, gpt-4).


**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от API.
- `_process_response`: Обрабатывает ответ от API и выдает его по частям.


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
        Создает асинхронный генератор для получения ответов от API.
        Функция отправляет запрос на API `free.netfly.top` с заданными параметрами 
        и возвращает генератор, который выдает фрагменты ответа по мере их поступления.

        Args:
            model (str): Название модели GPT (gpt-3.5-turbo или gpt-4).
            messages (Messages): Список сообщений в диалоге.
            proxy (str, optional): Прокси-сервер для запроса. По умолчанию `None`.
            **kwargs: Дополнительные параметры для запроса.

        Returns:
            AsyncResult: Асинхронный результат, который содержит генератор, 
            который выдает фрагменты ответа по мере их поступления.

        Raises:
            ClientError: Если произошла ошибка при отправке запроса на API.
            asyncio.TimeoutError: Если запрос был прерван из-за истечения времени ожидания.

        """
        ...
```

**Назначение**: 
- Отправляет запрос на API `free.netfly.top` с заданными параметрами.
- Возвращает асинхронный генератор для получения ответа.
- Использует HTTP-запрос `POST` с заданными заголовками.
- В качестве тела запроса передает словарь с данными, включающими список сообщений в диалоге, 
    название модели, параметры температуры, штрафов за присутствие и частоту, а также 
    флаг потоковой передачи.

**Параметры**: 
- `model` (str): Название модели GPT (gpt-3.5-turbo или gpt-4).
- `messages` (Messages): Список сообщений в диалоге.
- `proxy` (str, optional): Прокси-сервер для запроса. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры для запроса.

**Возвращает**: 
- `AsyncResult`: Асинхронный результат, который содержит генератор, 
    который выдает фрагменты ответа по мере их поступления.

**Вызывает исключения**:
- `ClientError`: Если произошла ошибка при отправке запроса на API.
- `asyncio.TimeoutError`: Если запрос был прерван из-за истечения времени ожидания.



**Как работает функция**:
-  Функция `create_async_generator` отправляет запрос на API `free.netfly.top` с использованием библиотеки `aiohttp`.
-  Запрос отправляется методом `POST` с заданными заголовками и данными.
-  В качестве данных передается словарь с информацией о модели, сообщениями в диалоге, а также 
    параметрами генерации текста (температура, штрафы за присутствие и частоту).
-  Функция использует асинхронный цикл `for` для обработки ответа от API.
-  Ответ от API приходит по частям (строками). 
-  Функция `_process_response` разбирает строчки из ответа, извлекает  данные, формирует и 
    возвращает фрагменты ответа. 
-  Обработка ответа завершается, когда строка "data: [DONE]" будет получена. 
-  В случае, если ошибка при обработке ответа была зафиксирована, функция пытается повторно 
    отправить запрос на API до 5 раз,  с паузой между попытками, которая увеличивается в 
    два раза после каждой неудачной попытки.
-  Если все попытки отправки запроса завершаются неудачей, то будет вызвано последнее исключение.

**Примеры**: 

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.FreeNetfly import FreeNetfly

messages = [
    {"role": "user", "content": "Привет!"},
]

async def main():
    async for chunk in FreeNetfly.create_async_generator(model='gpt-3.5-turbo', messages=messages):
        print(chunk)

asyncio.run(main())
```

### `_process_response`

```python
    @classmethod
    async def _process_response(cls, response) -> AsyncGenerator[str, None]:
        """
        Обрабатывает ответ от API и выдает его по частям.
        Функция читает ответ от API `free.netfly.top` по частям и извлекает фрагменты текста, 
        которые выдает как отдельные строки.

        Args:
            response (aiohttp.ClientResponse): Ответ от API `free.netfly.top`.

        Returns:
            AsyncGenerator[str, None]: Генератор, который выдает фрагменты текста 
            по мере их поступления.

        Raises:
            json.JSONDecodeError: Если строка не является валидным JSON.
            KeyError: Если в JSON отсутствует ожидаемый ключ.

        """
        ...
```

**Назначение**: 
- Разбирает ответ от API, извлекает фрагменты текста.
- Выдает фрагменты текста по частям (как отдельные строки) с использованием асинхронного генератора.
- Обрабатывает данные, закодированные в формате JSON.
- Обрабатывает случай, когда в JSON отсутствует ожидаемый ключ.

**Параметры**: 
- `response` (aiohttp.ClientResponse): Ответ от API `free.netfly.top`.

**Возвращает**: 
- `AsyncGenerator[str, None]`: Генератор, который выдает фрагменты текста 
    по мере их поступления.

**Вызывает исключения**:
- `json.JSONDecodeError`: Если строка не является валидным JSON.
- `KeyError`: Если в JSON отсутствует ожидаемый ключ.

**Как работает функция**:
-  Функция `_process_response` обрабатывает ответ от API, который приходит по частям. 
-  Она читает ответ построчно, анализирует строку, проверяет, является ли она валидным JSON.
-  Если строка является валидным JSON, то функция извлекает из него информацию о 
    фрагменте текста, которая содержится в поле `content` в структуре `data`.
-  Функция  проверяет, есть ли данные в поле `content`,  и если да, то выдает их как 
    отдельную строку.
-  Если строка не является валидным JSON или в ней отсутствует ключ `content`, то 
    функция пропускает эту строку. 
-  Функция `_process_response` выдает данные по частям (как отдельные строки) с 
    использованием асинхронного генератора. 
-  Генератор выдает данные до тех пор, пока не будет получена строка "data: [DONE]".

**Примеры**: 

```python
# Пример использования функции _process_response
import asyncio
from aiohttp import ClientResponse
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.FreeNetfly import FreeNetfly

async def main():
    # Имитация ответа от API
    response_content = [
        b'data: {"choices": [{"delta": {"content": "Привет! "}}], "id": "xxx", "object": "chat.completion.chunk", "created": 1701204399, "model": "gpt-3.5-turbo"}',
        b'data: {"choices": [{"delta": {"content": "Как дела? "}}], "id": "xxx", "object": "chat.completion.chunk", "created": 1701204399, "model": "gpt-3.5-turbo"}',
        b'data: [DONE]',
    ]

    class MockResponse:
        def __init__(self, content):
            self.content = content
            self.encoding = 'utf-8'

        async def __aiter__(self):
            for item in self.content:
                yield item

    response = MockResponse(response_content)
    async for chunk in FreeNetfly._process_response(response):
        print(chunk)

asyncio.run(main())
```

## Параметры класса

- `url` (str): Базовый URL API `free.netfly.top`.
- `api_endpoint` (str): Путь к API-методу для генерации текста.
- `working` (bool): Флаг, указывающий на доступность API.
- `default_model` (str): Название модели по умолчанию (gpt-3.5-turbo).
- `models` (list): Список доступных моделей (gpt-3.5-turbo, gpt-4).

## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.FreeNetfly import FreeNetfly

# Создание асинхронного генератора
async def main():
    messages = [
        {"role": "user", "content": "Привет!"},
    ]
    async for chunk in FreeNetfly.create_async_generator(model='gpt-3.5-turbo', messages=messages):
        print(chunk)

asyncio.run(main())
```

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.FreeNetfly import FreeNetfly

# Создание асинхронного генератора с использованием прокси
async def main():
    messages = [
        {"role": "user", "content": "Привет!"},
    ]
    async for chunk in FreeNetfly.create_async_generator(model='gpt-3.5-turbo', messages=messages, proxy='http://proxy.server:port'):
        print(chunk)

asyncio.run(main())
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.FreeNetfly import FreeNetfly

# Создание асинхронного генератора с использованием модели GPT-4
async def main():
    messages = [
        {"role": "user", "content": "Привет!"},
    ]
    async for chunk in FreeNetfly.create_async_generator(model='gpt-4', messages=messages):
        print(chunk)

asyncio.run(main())