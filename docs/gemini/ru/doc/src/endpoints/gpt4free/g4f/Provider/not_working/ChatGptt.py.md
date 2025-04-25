# Модуль ChatGptt

## Обзор

Модуль `ChatGptt` предоставляет асинхронный генератор для работы с API chatgptt.me.

## Подробнее

Модуль `ChatGptt` реализует два класса:

- `ChatGptt`: Основной класс, предоставляющий асинхронный генератор для получения ответов от модели.
- `ProviderModelMixin`: Миксин, предоставляющий функции для работы с моделями.

## Классы

### `ChatGptt`

**Описание**: Класс `ChatGptt` предоставляет асинхронный генератор для получения ответов от модели chatgptt.me. Он реализует интерфейс `AsyncGeneratorProvider` и использует миксин `ProviderModelMixin` для управления моделями.

**Наследует**:
- `AsyncGeneratorProvider`
- `ProviderModelMixin`

**Атрибуты**:

- `url` (str): Базовый URL API.
- `api_endpoint` (str): Точка входа API для отправки запросов.
- `working` (bool): Флаг, указывающий на работоспособность API.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи ответов.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Модель по умолчанию.
- `models` (list[str]): Список доступных моделей.

**Методы**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения ответов от модели.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.ChatGptt import ChatGptt

async def main():
    """Пример использования ChatGptt."""
    provider = ChatGptt()
    async for response in provider.create_async_generator(model='gpt-4', messages=[{'role': 'user', 'content': 'Привет!'}]) :
        print(response)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

### `ProviderModelMixin`

**Описание**: Миксин, предоставляющий функции для работы с моделями.

**Атрибуты**:

- `default_model` (str): Модель по умолчанию.
- `models` (list[str]): Список доступных моделей.

**Методы**:

- `get_model(model: str) -> str`: Возвращает модель из списка доступных моделей, либо модель по умолчанию.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.ChatGptt import ProviderModelMixin

class MyProvider(ProviderModelMixin):
    """Пример использования ProviderModelMixin."""
    default_model = 'gpt-3.5-turbo'
    models = ['gpt-3.5-turbo', 'gpt-4']

    async def get_response(self, model: str, prompt: str) -> str:
        """Пример метода, использующего get_model."""
        model = self.get_model(model)
        print(f"Используется модель: {model}")
        # Дальнейший код для получения ответа

if __name__ == '__main__':
    import asyncio
    asyncio.run(MyProvider().get_response('gpt-4', 'Привет!'))
```

## Функции

### `create_async_generator`

**Назначение**: Создает асинхронный генератор для получения ответов от модели.

**Параметры**:

- `model` (str): Имя модели.
- `messages` (Messages): Список сообщений.
- `proxy` (str, optional): Прокси-сервер для запросов. По умолчанию `None`.

**Возвращает**:

- `AsyncResult`: Асинхронный генератор, который возвращает ответы модели.

**Вызывает исключения**:

- `RuntimeError`: Возникает, если не найдены необходимые токены аутентификации.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.ChatGptt import ChatGptt

async def main():
    """Пример использования create_async_generator."""
    provider = ChatGptt()
    async for response in provider.create_async_generator(model='gpt-4', messages=[{'role': 'user', 'content': 'Привет!'}]) :
        print(response)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

**Как работает функция**:

1. Получает начальную страницу HTML с сайта chatgptt.me.
2. Извлекает токены `nonce` и `post_id` из HTML-кода.
3. Формирует payload для запроса к API chatgptt.me.
4. Отправляет POST-запрос к API с помощью `aiohttp`.
5. Обрабатывает ответ API и выдает ответы модели в виде асинхронного генератора.

**Внутренние функции**:

- `get_model(model: str) -> str`: Возвращает модель из списка доступных моделей, либо модель по умолчанию.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.ChatGptt import ChatGptt

async def main():
    """Пример использования create_async_generator."""
    provider = ChatGptt()
    async for response in provider.create_async_generator(model='gpt-4', messages=[{'role': 'user', 'content': 'Привет!'}]) :
        print(response)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```