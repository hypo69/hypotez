# Модуль GizAI

## Обзор

Модуль `GizAI` предоставляет асинхронный генератор для взаимодействия с API GizAI. Он позволяет отправлять запросы к модели и получать ответы в асинхронном режиме. Поддерживает стриминг, системные сообщения и историю сообщений.

## Подробней

Модуль предназначен для интеграции с сервисом GizAI, предоставляющим доступ к различным моделям, включая `chat-gemini-flash`. Класс `GizAI` асинхронно взаимодействует с API GizAI для генерации ответов на основе предоставленных сообщений.

## Классы

### `GizAI`

**Описание**: Класс `GizAI` предоставляет функциональность для взаимодействия с API GizAI.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность асинхронного генератора.
- `ProviderModelMixin`: Добавляет методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса GizAI.
- `api_endpoint` (str): URL API для отправки запросов.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер стриминг.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Методы**:
- `get_model(model: str) -> str`: Возвращает имя модели на основе псевдонима или имени, по умолчанию возвращает `default_model`.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения ответов от API GizAI.

## Методы класса

### `get_model`

```python
@classmethod
def get_model(cls, model: str) -> str:
    """Возвращает имя модели на основе псевдонима или имени.

    Args:
        model (str): Имя модели или псевдоним.

    Returns:
        str: Имя модели.
    """
    ...
```

**Назначение**:
Метод `get_model` принимает имя модели в качестве аргумента и возвращает соответствующее имя модели, которое будет использоваться в API-запросах. Если указанная модель есть в списке поддерживаемых моделей (`cls.models`) или имеет псевдоним в `cls.model_aliases`, возвращается соответствующее значение. В противном случае возвращается модель по умолчанию (`cls.default_model`).

**Параметры**:
- `model` (str): Имя модели или псевдоним.

**Возвращает**:
- `str`: Имя модели.

**Как работает функция**:
- Функция проверяет, есть ли указанная модель в списке поддерживаемых моделей (`cls.models`).
- Если модель не найдена в списке, функция проверяет, есть ли у модели псевдоним в словаре `cls.model_aliases`.
- Если псевдоним найден, функция возвращает соответствующее имя модели из словаря `cls.model_aliases`.
- Если модель не найдена ни в списке, ни в словаре псевдонимов, функция возвращает модель по умолчанию (`cls.default_model`).

**Примеры**:
```python
# Пример 1: Модель по умолчанию
model = GizAI.get_model("unknown_model")
print(model)  # Вывод: chat-gemini-flash

# Пример 2: Существующая модель
model = GizAI.get_model("chat-gemini-flash")
print(model)  # Вывод: chat-gemini-flash

# Пример 3: Псевдоним модели
GizAI.model_aliases = {"gemini-1.5-flash": "chat-gemini-flash"}
model = GizAI.get_model("gemini-1.5-flash")
print(model)  # Вывод: chat-gemini-flash
```

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
    """Создает асинхронный генератор для получения ответов от API GizAI.

    Args:
        model (str): Имя модели.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от API GizAI.
    """
    ...
```

**Назначение**:
Метод `create_async_generator` создает асинхронный генератор, который отправляет сообщения в API GizAI и возвращает ответы. Он использует `aiohttp.ClientSession` для выполнения асинхронных HTTP-запросов.

**Параметры**:
- `model` (str): Имя модели для использования.
- `messages` (Messages): Список сообщений, которые нужно отправить в API.
- `proxy` (str, optional): Адрес прокси-сервера (если требуется). По умолчанию `None`.
- `**kwargs`: Дополнительные параметры (не используются в данной реализации).

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от API GizAI.

**Вызывает исключения**:
- `Exception`: Если статус ответа не 201.

**Как работает функция**:
1. **Определение модели**:
   - Сначала вызывается метод `cls.get_model(model)`, чтобы получить правильное имя модели на основе переданного имени или псевдонима.

2. **Формирование заголовков**:
   - Формируются заголовки HTTP-запроса, включающие `User-Agent`, `Content-Type` и другие необходимые параметры.

3. **Создание асинхронной сессии**:
   - Используется `aiohttp.ClientSession` для управления асинхронными HTTP-запросами. Сессия создается с заданными заголовками.

4. **Подготовка данных для запроса**:
   - Формируется словарь `data`, содержащий модель и входные сообщения. Сообщения форматируются в соответствии с требованиями API GizAI. Сообщения пользователя и системы преобразуются в формат `{"content": message.get("content")}`, а сообщения с ролью "user" преобразуются в формат `{"type": "human", "content": message.get("content")}`, а сообщения с любой другой ролью - в формат `{"type": "ai", "content": message.get("content")}`.

5. **Отправка POST-запроса**:
   - Отправляется POST-запрос к `cls.api_endpoint` с использованием `session.post`. В запросе передаются данные `data` в формате JSON и, если указан, `proxy`.

6. **Обработка ответа**:
   - Проверяется статус ответа:
     - Если статус равен 201, извлекается результат из JSON-ответа (`result = await response.json()`), и извлекается текст ответа из поля `result['output']`, удаляя лишние пробелы. Затем текст возвращается через `yield`.
     - Если статус не равен 201, вызывается исключение `Exception` с информацией о статусе ответа и текстом ошибки.

**Примеры**:
```python
import asyncio
from typing import AsyncGenerator, Dict, List, Optional

from aiohttp import ClientSession

from g4f.typing import Messages
from g4f.Provider.GizAI import GizAI  # Укажите правильный путь к классу GizAI


async def make_request(messages: Messages) -> AsyncGenerator[str, None]:
    """
    Функция для выполнения запроса к GizAI.
    """
    async for message in GizAI.create_async_generator(model="chat-gemini-flash", messages=messages):
        yield message

async def main():
    """
    Основная функция для демонстрации работы с GizAI.
    """
    messages: Messages = [
        {"role": "user", "content": "Привет!"},
    ]

    result = []
    async for message in make_request(messages):
        result.append(message)

    print("".join(result))

if __name__ == "__main__":
    asyncio.run(main())