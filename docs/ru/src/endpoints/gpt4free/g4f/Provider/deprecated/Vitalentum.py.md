# Модуль Vitalentum

## Обзор

Модуль Vitalentum предоставляет асинхронный генератор для взаимодействия с API Vitalentum.io. Он позволяет использовать модель gpt-3.5-turbo для генерации текста на основе предоставленных сообщений. Этот модуль предназначен для интеграции с другими частями проекта, требующими доступа к указанному API.

## Подробней

Модуль использует библиотеку `aiohttp` для выполнения асинхронных HTTP-запросов. Он отправляет сообщения пользователей в API Vitalentum и возвращает сгенерированный контент в виде асинхронного генератора.

## Классы

### `Vitalentum`

**Описание**:
Класс `Vitalentum` является провайдером асинхронного генератора, который взаимодействует с API Vitalentum.io.

**Принцип работы**:
Класс использует `aiohttp.ClientSession` для отправки POST-запросов к API `Vitalentum` и получает ответы в виде потока событий (`text/event-stream`). Затем он извлекает контент из этих событий и генерирует его как асинхронный поток.

**Аттрибуты**:
- `url` (str): URL API Vitalentum.io.
- `supports_gpt_35_turbo` (bool): Поддерживает ли провайдер модель gpt-3.5-turbo.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от API.

## Функции

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
    Создает асинхронный генератор для получения ответов от API Vitalentum.

    Args:
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры для передачи в API.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий контент, сгенерированный моделью.
    """
```

**Назначение**:
Функция `create_async_generator` создает и возвращает асинхронный генератор, который отправляет сообщения в API Vitalentum и извлекает сгенерированный контент.

**Параметры**:
- `cls`: Ссылка на класс `Vitalentum`.
- `model` (str): Имя используемой модели.
- `messages` (Messages): Список сообщений для отправки в API. Каждое сообщение содержит роль (`user` или `bot`) и контент.
- `proxy` (str, optional): URL прокси-сервера для использования при подключении к API. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры, которые будут переданы в API.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, который выдает контент, сгенерированный моделью.

**Как работает функция**:
1. **Подготовка заголовков**: Создаются HTTP-заголовки, включающие User-Agent, Accept, Origin, Referer и другие.
2. **Преобразование сообщений**: Список сообщений преобразуется в JSON-формат, где роль `user` становится `human`, а роль `bot` становится `bot`.
3. **Формирование данных**: Создается словарь `data` с преобразованными сообщениями, температурой и дополнительными аргументами.
4. **Создание сессии**: Создается асинхронная сессия `ClientSession` с заданными заголовками.
5. **Отправка запроса**: Отправляется POST-запрос к API Vitalentum с данными в формате JSON.
6. **Обработка ответа**: Читаются строки из ответа, декодируются и извлекается контент из JSON-объектов.
7. **Генерация контента**: Извлеченный контент генерируется как асинхронный поток.

**Внутренние функции**:

Внутри функции `create_async_generator` используется асинхронный генератор, который обрабатывает ответ от API Vitalentum.
Этот генератор читает ответ построчно, декодирует строки, и извлекает контент из JSON-объектов, отправляя его как асинхронный поток.

**ASCII Flowchart**:

```
[Подготовка заголовков и данных]
    ↓
[Создание асинхронной сессии]
    ↓
[Отправка POST-запроса к API]
    ↓
[Получение ответа в виде потока]
    ↓
[Обработка каждой строки ответа]
    ├──> startswith("data: ") == True? --> [startswith("data: [DONE]") == True? --> Выход]
    │   ↓ no
    │   [Пропуск строки]
    │
    └──> yes
        ↓
    [Загрузка JSON из строки]
        ↓
    [Извлечение контента из JSON]
        ↓
    [Генерация контента]
```

**Примеры**:

```python
# Пример использования асинхронного генератора
import asyncio
from typing import AsyncGenerator, List, Dict

async def main():
    messages: List[Dict[str, str]] = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "bot", "content": "I am doing well, thank you for asking."}
    ]
    async for message in Vitalentum.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())
```
```python
# Использование прокси-сервера
import asyncio
from typing import AsyncGenerator, List, Dict

async def main():
    messages: List[Dict[str, str]] = [
        {"role": "user", "content": "Tell me a joke."},
    ]
    proxy = "http://your_proxy:8080"
    async for message in Vitalentum.create_async_generator(model="gpt-3.5-turbo", messages=messages, proxy=proxy):
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())