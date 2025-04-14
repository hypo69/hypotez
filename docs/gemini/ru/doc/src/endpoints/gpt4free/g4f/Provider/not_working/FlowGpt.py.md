# Модуль FlowGpt для работы с FlowGPT API
## Обзор

Модуль `FlowGpt` предоставляет класс `FlowGpt`, который является асинхронным генератором для взаимодействия с API FlowGPT. Он позволяет получать ответы от различных моделей, таких как GPT-3.5 Turbo, Google Gemini и Claude, используя асинхронные запросы.

## Подробнее

Этот модуль предназначен для интеграции с API FlowGPT, предоставляя удобный интерфейс для отправки запросов и получения ответов в асинхронном режиме. Он поддерживает различные модели и параметры, такие как температуру и системные сообщения.

## Классы

### `FlowGpt`

**Описание**: Класс `FlowGpt` является асинхронным генератором, который взаимодействует с API FlowGPT для получения ответов от различных моделей.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL для взаимодействия с FlowGPT API.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Методы**:

- `create_async_generator`: Статический асинхронный метод для создания асинхронного генератора.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    temperature: float = 0.7,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с API FlowGPT.

    Args:
        cls (FlowGpt): Класс FlowGpt.
        model (str): Название модели для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию None.
        temperature (float, optional): Температура для генерации ответов. По умолчанию 0.7.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, который выдает ответы от API FlowGPT.
    """
    ...
```

**Назначение**: Создает и возвращает асинхронный генератор для взаимодействия с API FlowGPT. Этот метод подготавливает необходимые заголовки и данные для запроса, а затем отправляет запрос к API FlowGPT. Полученные ответы передаются через асинхронный генератор.

**Параметры**:
- `cls` (FlowGpt): Ссылка на класс `FlowGpt`.
- `model` (str): Имя модели, которую следует использовать для генерации ответов.
- `messages` (Messages): Список сообщений, отправляемых в API FlowGPT. Каждое сообщение содержит роль (например, "user" или "assistant") и содержимое.
- `proxy` (str, optional): URL прокси-сервера, если необходимо использовать прокси для подключения к API. По умолчанию `None`.
- `temperature` (float, optional): Параметр температуры, влияющий на случайность генерируемых ответов. Значение по умолчанию - 0.7.
- `**kwargs`: Дополнительные параметры, которые могут быть переданы в API FlowGPT.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, который выдает ответы от API FlowGPT.

**Как работает функция**:
1. **Подготовка данных**:
   - Получает имя модели с помощью `cls.get_model(model)`.
   - Генерирует timestamp, nonce и signature для заголовков запроса.
   - Формирует заголовки (`headers`) для HTTP-запроса, включая User-Agent, Referer и параметры аутентификации.
2. **Создание сессии**:
   - Использует `aiohttp.ClientSession` для выполнения асинхронных HTTP-запросов.
   - Формирует историю сообщений, исключая системные сообщения.
   - Составляет системное сообщение из всех сообщений с ролью "system". Если таких сообщений нет, используется сообщение по умолчанию.
3. **Формирование тела запроса**:
   - Создает словарь `data`, содержащий модель, флаг NSFW, вопрос пользователя, историю сообщений, системное сообщение, температуру и другие параметры.
4. **Отправка запроса и получение ответа**:
   - Отправляет POST-запрос к API FlowGPT (`https://prod-backend-k8s.flowgpt.com/v3/chat-anonymous`) с сформированными заголовками и данными.
   - Обрабатывает ответ от API FlowGPT в асинхронном режиме.
   - Проверяет наличие данных в каждом чанке ответа.
   - Преобразует чанк в JSON и проверяет наличие события "text".
   - Выдает данные из сообщения, если событие равно "text".

**Примеры**:

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.not_working.FlowGpt import FlowGpt
from src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    messages: Messages = [
        {"role": "user", "content": "Hello, how are you?"}
    ]
    async for message in FlowGpt.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())
```

В этом примере показано, как создать асинхронный генератор с использованием `FlowGpt.create_async_generator` и перебрать его для получения ответов от API FlowGPT.

## Параметры класса

- `url` (str): URL для взаимодействия с FlowGPT API.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

## Примеры

Пример использования класса `FlowGpt` для получения ответа от API FlowGPT:

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.not_working.FlowGpt import FlowGpt
from src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    messages: Messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
    async for message in FlowGpt.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())
```

В этом примере создается список сообщений, содержащий системное сообщение и вопрос пользователя. Затем создается асинхронный генератор с использованием `FlowGpt.create_async_generator` и перебирается для получения ответа от API FlowGPT.