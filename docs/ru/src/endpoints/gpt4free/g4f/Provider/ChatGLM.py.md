# Модуль `ChatGLM`

## Обзор

Модуль `ChatGLM` предоставляет асинхронный интерфейс для взаимодействия с моделью ChatGLM. Он позволяет генерировать текст на основе предоставленных сообщений, используя API ChatGLM. Модуль поддерживает потоковую передачу данных и предоставляет возможность использования прокси.

## Подробнее

Модуль предназначен для использования в асинхронных приложениях, где требуется взаимодействие с моделью ChatGLM для генерации текста. Он использует библиотеку `aiohttp` для выполнения асинхронных HTTP-запросов и предоставляет удобный интерфейс для работы с API ChatGLM.

## Классы

### `ChatGLM`

**Описание**: Класс `ChatGLM` является поставщиком асинхронного генератора и миксином для моделей.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями провайдера.

**Атрибуты**:
- `url` (str): URL сервиса ChatGLM (`https://chatglm.cn`).
- `api_endpoint` (str): URL API для взаимодействия с ChatGLM (`https://chatglm.cn/chatglm/mainchat-api/guest/stream`).
- `working` (bool): Указывает, работает ли провайдер (по умолчанию `True`).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных (по умолчанию `True`).
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения (по умолчанию `False`).
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений (по умолчанию `False`).
- `default_model` (str): Модель, используемая по умолчанию (`glm-4`).
- `models` (list): Список поддерживаемых моделей (содержит только `default_model`).

**Методы**:

- `create_async_generator`: Создает асинхронный генератор для получения ответов от ChatGLM.

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
    Создает асинхронный генератор для получения ответов от ChatGLM.

    Args:
        cls (ChatGLM): Класс ChatGLM.
        model (str): Используемая модель.
        messages (Messages): Список сообщений для отправки в ChatGLM.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от ChatGLM.

    Raises:
        Exception: Если возникает ошибка при взаимодействии с API ChatGLM.

    
        1. Генерирует уникальный `device_id`.
        2. Определяет заголовки запроса, включая `device_id`.
        3. Создает асинхронную сессию `ClientSession` с заданными заголовками.
        4. Формирует данные для отправки в API, включая `assistant_id`, `conversation_id`, `meta_data` и `messages`.
        5. Отправляет POST-запрос к `api_endpoint` с использованием `session.post`.
        6. Обрабатывает чанки данных, полученные из ответа, декодирует их и извлекает содержимое.
        7. Генерирует текст из полученных частей и передает его через `yield`.
        8. Если статус ответа равен `'finish'`, генерирует `FinishReason("stop")`.

    Внутренние функции:
        - Отсутствуют
    """
```

## Параметры класса

- `cls` (ChatGLM): Класс ChatGLM.
- `model` (str): Используемая модель.
- `messages` (Messages): Список сообщений для отправки в ChatGLM.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

## Примеры

Пример использования `create_async_generator`:

```python
async def main():
    messages = [
        {"role": "user", "content": "Hello, ChatGLM!"}
    ]
    async for response in ChatGLM.create_async_generator(model="glm-4", messages=messages):
        print(response)

# Пример запуска (необходим асинхронный контекст)
# asyncio.run(main())