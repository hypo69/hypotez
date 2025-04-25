# Модуль Qwen_Qwen_2_5_Max

## Обзор

Модуль `Qwen_Qwen_2_5_Max` предоставляет реализацию асинхронного генератора ответов для модели Qwen Qwen-2.5-Max, 
доступной через сервис Hugging Face Spaces. 

## Подробнее

Данный модуль реализует асинхронный генератор ответов для модели `Qwen Qwen-2.5-Max`, 
доступной через сервис Hugging Face Spaces, используя API `gradio_api` сервиса. 

- `Qwen_Qwen_2_5_Max`  наследует классы `AsyncGeneratorProvider` и `ProviderModelMixin`.
- Класс поддерживает асинхронный генератор (`supports_stream`), системные сообщения (`supports_system_message`) 
и не поддерживает историю сообщений (`supports_message_history`).
- Модуль использует `aiohttp` для отправки запросов на API.
- Для генерации уникального идентификатора сессии используется `uuid`.
- Для обработки ответов используется `json`.
- Для форматирования запроса используется `format_prompt` из модуля `helper`.

## Классы

### `class Qwen_Qwen_2_5_Max`

**Описание**: Класс для асинхронного генератора ответов от модели Qwen Qwen-2.5-Max, 
доступной через сервис Hugging Face Spaces.

**Наследует**: 
- `AsyncGeneratorProvider`: Базовый класс для асинхронных генераторов ответов.
- `ProviderModelMixin`: Базовый класс для моделей.

**Атрибуты**:

- `label`: Наименование модели.
- `url`: URL-адрес сервиса Hugging Face Spaces, где размещена модель.
- `api_endpoint`: URL-адрес конечной точки API для взаимодействия с моделью.
- `working`: Флаг, указывающий на доступность модели.
- `supports_stream`: Флаг, указывающий на поддержку потокового генерирования ответа.
- `supports_system_message`: Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history`: Флаг, указывающий на поддержку истории сообщений.
- `default_model`: Название модели по умолчанию.
- `model_aliases`: Словарь, содержащий псевдонимы для модели.
- `models`: Список доступных моделей.

**Методы**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: 
Асинхронный генератор ответов от модели.

#### `create_async_generator`

**Назначение**:  Метод создает асинхронный генератор ответов, используемый для получения 
ответов от модели Qwen Qwen-2.5-Max. 

**Параметры**:

- `model` (str): Наименование модели.
- `messages` (Messages): Список сообщений для модели.
- `proxy` (str, optional): Прокси-сервер для подключения к модели. По умолчанию None.
- `kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный результат, который содержит генератор ответов.

**Как работает функция**:

- Генерирует уникальный идентификатор сессии `session_hash` для текущего запроса.
- Формирует заголовки запроса `headers_join` и данные запроса `payload_join` для отправки 
в API `gradio_api` сервиса Hugging Face Spaces.
- Использует `aiohttp` для отправки запроса на API `gradio_api` сервиса.
- Получает `event_id` для отслеживания прогресса генерации ответа.
- Отправляет запрос на API `gradio_api` сервиса для получения потоковых ответов.
- Парсит полученные данные и возвращает генератор ответов.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.Qwen_Qwen_2_5_Max import Qwen_Qwen_2_5_Max
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages = [
    {"role": "user", "content": "Привет! Как дела?"}
]

async def main():
    provider = Qwen_Qwen_2_5_Max()
    async_result = await provider.create_async_generator(model="qwen-2-5-max", messages=messages)
    async for response in async_result.response:
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.Qwen_Qwen_2_5_Max import Qwen_Qwen_2_5_Max
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages = [
    {"role": "user", "content": "Напиши рассказ про кота"}
]

async def main():
    provider = Qwen_Qwen_2_5_Max()
    async_result = await provider.create_async_generator(model="qwen-2-5-max", messages=messages)
    async for response in async_result.response:
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Внутренние функции

### `generate_session_hash()`

**Назначение**: Внутренняя функция, которая генерирует уникальный идентификатор сессии 
для текущего запроса.

**Параметры**:

- Отсутствуют

**Возвращает**:
- str: Уникальный идентификатор сессии.

**Как работает функция**:

- Использует `uuid.uuid4()` для генерации случайного уникального идентификатора.
- Преобразует полученный идентификатор в строку и удаляет символы `-`.
- Возвращает первые 12 символов из полученного идентификатора.
```markdown