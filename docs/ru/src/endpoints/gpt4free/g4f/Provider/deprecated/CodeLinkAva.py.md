# Модуль `CodeLinkAva`

## Обзор

Модуль `CodeLinkAva` предоставляет асинхронный генератор для взаимодействия с API CodeLinkAva. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов и предназначен для работы с моделью `gpt-3.5-turbo`. Модуль позволяет отправлять сообщения и получать ответы в режиме реального времени.

## Подробней

Модуль `CodeLinkAva` является частью устаревших провайдеров GPT4Free. Он реализует асинхронный генератор, который взаимодействует с API CodeLinkAva для получения ответов на основе предоставленных сообщений. API поддерживает потоковую передачу данных, что позволяет получать ответы в режиме реального времени. Этот модуль полезен для интеграции с CodeLinkAva в асинхронных приложениях.

## Классы

### `CodeLinkAva`

**Описание**: Класс `CodeLinkAva` предоставляет функциональность для взаимодействия с API CodeLinkAva. Он наследует класс `AsyncGeneratorProvider` и реализует метод `create_async_generator` для создания асинхронного генератора.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных провайдеров-генераторов.

**Атрибуты**:
- `url` (str): URL API CodeLinkAva.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель `gpt-3.5-turbo`.
- `working` (bool): Указывает, находится ли провайдер в рабочем состоянии.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от API CodeLinkAva.

## Функции

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: list[dict[str, str]],
        **kwargs
    ) -> AsyncGenerator:
        """
        Создает асинхронный генератор для получения ответов от API CodeLinkAva.

        Args:
            model (str): Модель, используемая для генерации ответов.
            messages (list[dict[str, str]]): Список сообщений для отправки в API.
            **kwargs: Дополнительные аргументы для передачи в API.

        Returns:
            AsyncGenerator: Асинхронный генератор, выдающий контент ответов от API CodeLinkAva.

        Raises:
            aiohttp.ClientResponseError: Если возникает ошибка при выполнении HTTP-запроса.
        """
```

**Назначение**: Создает асинхронный генератор, который отправляет сообщения в API CodeLinkAva и возвращает ответы в режиме реального времени.

**Параметры**:
- `cls` (class): Ссылка на класс `CodeLinkAva`.
- `model` (str): Модель, используемая для генерации ответов.
- `messages` (list[dict[str, str]]): Список сообщений для отправки в API. Каждое сообщение представляет собой словарь с ключами `role` и `content`.
- `**kwargs`: Дополнительные аргументы, которые будут переданы в API.

**Возвращает**:
- `AsyncGenerator`: Асинхронный генератор, который выдает контент ответов от API CodeLinkAva.

**Вызывает исключения**:
- `aiohttp.ClientResponseError`: Если возникает ошибка при выполнении HTTP-запроса.

**Как работает функция**:
1. **Установка заголовков**: Функция создает словарь `headers` с необходимыми HTTP-заголовками для запроса.
2. **Создание сессии**: Используется `aiohttp.ClientSession` для выполнения асинхронных HTTP-запросов.
3. **Подготовка данных**: Функция подготавливает данные для отправки в API, включая сообщения, температуру и флаг потоковой передачи.
4. **Выполнение запроса**: Функция выполняет POST-запрос к API CodeLinkAva и обрабатывает ответы в асинхронном режиме.
5. **Обработка ответов**: Функция обрабатывает каждую строку ответа, декодирует ее и извлекает контент из JSON-формата.
6. **Генерация контента**: Функция использует `yield` для генерации контента ответа в режиме реального времени.

**ASCII Flowchart**:

```
    Начало
     ↓
Установка заголовков
     ↓
  Создание сессии (aiohttp.ClientSession)
     ↓
  Подготовка данных (messages, temperature, stream, kwargs)
     ↓
  POST-запрос к API ("https://ava-alpha-api.codelink.io/api/chat")
     ↓
   Обработка ответа
     ├───> Получение строки ответа
     │     ↓
     │   Декодирование строки
     │     ↓
     │   Проверка на "data: "
     │     ↓
     │   Проверка на "data: [DONE]"
     │     ↓
     │   Извлечение контента из JSON
     │     ↓
     └───> yield content (генерация контента)
     ↓
   Конец
```

**Примеры**:

```python
import asyncio
from aiohttp import ClientSession

from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated import CodeLinkAva

async def main():
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    model = "gpt-3.5-turbo"
    
    async for message in CodeLinkAva.create_async_generator(model=model, messages=messages):
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())
```
```python
import asyncio
from aiohttp import ClientSession

from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated import CodeLinkAva

async def main():
    messages = [{"role": "user", "content": "Как создать асинхронный генератор на Python?"}]
    model = "gpt-3.5-turbo"
    
    async for message in CodeLinkAva.create_async_generator(model=model, messages=messages):
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())